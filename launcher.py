import argparse
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import requests


STREAM_ENDPOINT = "/v1/govern/stream"
GOVERN_ENDPOINT = "/v1/govern"

JOURNAL_DIR = Path("journal")


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def estimate_token_count(text):
    if not text:
        return 0

    return max(1, round(len(text) / 4))


def get_nested(data, path):
    current = data

    for part in path.split("."):
        if not isinstance(current, dict):
            return None

        current = current.get(part)

        if current is None:
            return None

    return current


def first_non_null(*values):
    for value in values:
        if value is not None and value != "":
            return value

    return None


def resolve_provider_key(payload):
    """
    Provider keys are never stored in example_request.json.

    The launcher resolves the correct provider environment variable
    from the provider declared in the request.
    """

    provider = str(payload.get("provider", "")).lower()

    provider_env_map = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GOOGLE_API_KEY",
        "gemini": "GOOGLE_API_KEY",
        "mistral": "MISTRAL_API_KEY",
        "cohere": "COHERE_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "xai": "XAI_API_KEY",
        "grok": "XAI_API_KEY",
        "perplexity": "PERPLEXITY_API_KEY",
        "together": "TOGETHER_API_KEY",
        "qwen": "QWEN_API_KEY",
        "apertus": "APERTUS_API_KEY",
        "euria": "EURIA_API_KEY"
    }

    env_name = provider_env_map.get(provider)

    if not env_name:
        sys.exit(
            f"Unsupported provider '{provider}'. "
            "Add its environment-variable mapping in resolve_provider_key()."
        )

    provider_key = os.getenv(env_name)

    if not provider_key:
        sys.exit(
            f"Missing provider API key. "
            f"Set environment variable: {env_name}"
        )

    return provider_key, env_name


def parse_stream_response(response):
    """
    Parse NeoMundi /v1/govern/stream SSE events.

    Returns:
      - complete event list
      - generated LLM response text
      - token count
      - latency and selected stream metadata
    """

    events = []
    response_text = ""

    started = time.perf_counter()

    for raw_line in response.iter_lines(decode_unicode=True):

        if not raw_line:
            continue

        line = raw_line.strip()

        print(line)

        if line.startswith("data:"):
            payload_text = line[5:].strip()

            if payload_text == "[DONE]":
                continue

            try:
                event = json.loads(payload_text)
            except json.JSONDecodeError:
                continue

        elif line.startswith("{") or line.startswith("["):

            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

        else:
            continue

        events.append({
            "timestamp": utc_now(),
            "payload": event
        })

        chunk = first_non_null(
            get_nested(event, "content"),
            get_nested(event, "delta.content"),
            get_nested(event, "text"),
            get_nested(event, "chunk")
        )

        if chunk is not None:
            response_text += str(chunk)

        complete_text = first_non_null(
            get_nested(event, "response_text"),
            get_nested(event, "llm_response"),
            get_nested(event, "output_text"),
            get_nested(event, "response"),
            get_nested(event, "provider_response.text")
        )

        if complete_text is not None:
            response_text = str(complete_text)

    measured_latency_ms = (
        time.perf_counter() - started
    ) * 1000

    if not events:
        raise RuntimeError(
            "No parseable JSON event received from /v1/govern/stream."
        )

    if not response_text.strip():
        raise RuntimeError(
            "The stream endpoint returned no LLM response text."
        )

    last_event = events[-1]["payload"]

    raw_token_count = first_non_null(
        get_nested(last_event, "token_count"),
        get_nested(last_event, "total_tokens"),
        get_nested(last_event, "tokens_so_far"),
        get_nested(last_event, "usage.total_tokens"),
        get_nested(last_event, "usage.output_tokens"),
        get_nested(last_event, "provider_usage.total_tokens"),
        get_nested(last_event, "provider_usage.output_tokens"),
        get_nested(last_event, "token_position")
    )

    try:
        token_count = int(raw_token_count)
        token_count_source = "stream"
    except (TypeError, ValueError):
        token_count = estimate_token_count(response_text)
        token_count_source = "estimated_chars_div_4"

    latency_ms = first_non_null(
        get_nested(last_event, "latency_ms"),
        get_nested(last_event, "processing_time_ms"),
        measured_latency_ms
    )

    try:
        latency_ms = float(latency_ms)
    except (TypeError, ValueError):
        latency_ms = measured_latency_ms

    return {
        "events": events,
        "response_text": response_text,
        "token_count": token_count,
        "token_count_source": token_count_source,
        "latency_ms": round(latency_ms, 3),
        "stream_request_id": get_nested(
            last_event,
            "request_id"
        ),
        "stream_decision": get_nested(
            last_event,
            "decision"
        ),
        "stream_stability_score": get_nested(
            last_event,
            "stability_score"
        ),
        "stream_r_score": get_nested(
            last_event,
            "r_score"
        ),
        "event_count": len(events)
    }


def call_stream(
    base_url,
    neomundi_key,
    payload,
    provider_key
):
    url = base_url.rstrip("/") + STREAM_ENDPOINT

    stream_payload = {
        "prompt": payload["prompt"],
        "model": payload["model"],
        "provider": payload["provider"],
        "provider_api_key": provider_key
    }

    headers = {
        "X-API-Key": neomundi_key,
        "Accept": "text/event-stream",
        "Content-Type": "application/json; charset=utf-8"
    }

    print()
    print("STEP 1 — Runtime stream")
    print("-----------------------")
    print(f"POST {url}")
    print()

    started = time.perf_counter()

    response = requests.post(
        url,
        headers=headers,
        json=stream_payload,
        stream=True,
        timeout=120
    )

    request_latency_ms = (
        time.perf_counter() - started
    ) * 1000

    if response.status_code != 200:
        raise RuntimeError(
            f"/stream returned HTTP {response.status_code}: "
            f"{response.text}"
        )

    parsed = parse_stream_response(response)

    if not parsed["latency_ms"]:
        parsed["latency_ms"] = round(
            request_latency_ms,
            3
        )

    return parsed


def call_govern(
    base_url,
    neomundi_key,
    prompt,
    response_text,
    token_count,
    latency_ms
):
    url = base_url.rstrip("/") + GOVERN_ENDPOINT

    govern_payload = {
        "source_type": "llm",
        "mode": "OBS",
        "llm_prompt": prompt,
        "llm_response": response_text,
        "raw_metrics": {
            "token_count": int(token_count),
            "latency_ms": int(round(latency_ms))
        }
    }

    headers = {
        "X-API-Key": neomundi_key,
        "Content-Type": "application/json; charset=utf-8"
    }

    print()
    print("STEP 2 — Complete measurement")
    print("-----------------------------")
    print(f"POST {url}")
    print()

    response = requests.post(
        url,
        headers=headers,
        json=govern_payload,
        timeout=120
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"/govern returned HTTP {response.status_code}: "
            f"{response.text}"
        )

    try:
        return response.json()

    except json.JSONDecodeError:
        raise RuntimeError(
            "/govern returned a non-JSON response."
        )


def validate_request(payload):
    required = [
        "prompt",
        "model",
        "provider"
    ]

    missing = [
        field
        for field in required
        if not payload.get(field)
    ]

    if missing:
        sys.exit(
            "Missing required request field(s): "
            + ", ".join(missing)
        )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "NeoMundi Continuous Control Launcher — "
            "activate runtime measurement, expose signals "
            "and journal the complete execution."
        )
    )

    parser.add_argument(
        "request",
        help="Path to the JSON request file."
    )

    args = parser.parse_args()

    neomundi_key = os.getenv(
        "NEOMUNDI_API_KEY"
    )

    base_url = os.getenv(
        "NEOMUNDI_BASE_URL",
        "https://api.neomundi.io"
    )

    if not neomundi_key:
        sys.exit(
            "Missing environment variable: "
            "NEOMUNDI_API_KEY"
        )

    payload = load_json(args.request)

    validate_request(payload)

    provider_key, provider_env_name = (
        resolve_provider_key(payload)
    )

    run_id = str(uuid.uuid4())

    journal_path = (
        JOURNAL_DIR /
        f"{run_id}.json"
    )

    journal = {
        "launcher": {
            "name": (
                "neomundi-continuous-control-launcher"
            ),
            "version": "0.1.0"
        },

        "run_id": run_id,

        "started_at": utc_now(),

        "provider": payload["provider"],

        "model": payload["model"],

        "request": {
            "prompt": payload["prompt"],
            "model": payload["model"],
            "provider": payload["provider"]
        },

        "credentials": {
            "neomundi_api_key": "ENV",
            "provider_api_key": provider_env_name
        },

        "stream": None,

        "measurement": None,

        "status": "RUNNING",

        "error": None,

        "completed_at": None
    }

    print()
    print("NeoMundi Continuous Control Launcher")
    print("====================================")
    print(f"Run ID   : {run_id}")
    print(f"Provider : {payload['provider']}")
    print(f"Model    : {payload['model']}")
    print()

    try:

        stream_result = call_stream(
            base_url=base_url,
            neomundi_key=neomundi_key,
            payload=payload,
            provider_key=provider_key
        )

        journal["stream"] = {
            "request_id": (
                stream_result[
                    "stream_request_id"
                ]
            ),
            "event_count": (
                stream_result[
                    "event_count"
                ]
            ),
            "decision": (
                stream_result[
                    "stream_decision"
                ]
            ),
            "stability_score": (
                stream_result[
                    "stream_stability_score"
                ]
            ),
            "r_score": (
                stream_result[
                    "stream_r_score"
                ]
            ),
            "token_count": (
                stream_result[
                    "token_count"
                ]
            ),
            "token_count_source": (
                stream_result[
                    "token_count_source"
                ]
            ),
            "latency_ms": (
                stream_result[
                    "latency_ms"
                ]
            ),
            "response_text": (
                stream_result[
                    "response_text"
                ]
            ),
            "events": (
                stream_result[
                    "events"
                ]
            )
        }

        write_json(
            journal_path,
            journal
        )

        measurement = call_govern(
            base_url=base_url,
            neomundi_key=neomundi_key,
            prompt=payload["prompt"],
            response_text=(
                stream_result[
                    "response_text"
                ]
            ),
            token_count=(
                stream_result[
                    "token_count"
                ]
            ),
            latency_ms=(
                stream_result[
                    "latency_ms"
                ]
            )
        )

        journal["measurement"] = measurement

        journal["status"] = "COMPLETED"

        journal["completed_at"] = utc_now()

        write_json(
            journal_path,
            journal
        )

        print()
        print("RESULT")
        print("------")

        decision = first_non_null(
            get_nested(
                measurement,
                "decision"
            ),
            stream_result[
                "stream_decision"
            ]
        )

        stability = first_non_null(
            get_nested(
                measurement,
                "stability_score"
            ),
            get_nested(
                measurement,
                "scores.stability_score"
            ),
            stream_result[
                "stream_stability_score"
            ]
        )

        print(
            f"Decision  : {decision}"
        )

        print(
            f"Stability : {stability}"
        )

        print(
            f"Tokens    : "
            f"{stream_result['token_count']}"
        )

        print(
            f"Events    : "
            f"{stream_result['event_count']}"
        )

        print()
        print(
            "Measurement and runtime trace "
            "successfully journaled."
        )

        print(
            f"Journal: {journal_path}"
        )

    except Exception as exc:

        journal["status"] = "ERROR"

        journal["error"] = str(exc)

        journal["completed_at"] = utc_now()

        write_json(
            journal_path,
            journal
        )

        print()
        print("ERROR")
        print("-----")
        print(str(exc))
        print()
        print(
            f"Journal: {journal_path}"
        )

        sys.exit(1)


if __name__ == "__main__":
    main()
