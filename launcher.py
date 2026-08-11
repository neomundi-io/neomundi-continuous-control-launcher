import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import requests


DEFAULT_ENDPOINT = "/v1/govern/stream"
JOURNAL_DIR = Path("journal")


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="NeoMundi Continuous Control Launcher"
    )

    parser.add_argument(
        "request",
        help="Path to the JSON request to send to NeoMundi"
    )

    args = parser.parse_args()

    api_key = os.getenv("NEOMUNDI_API_KEY")
    base_url = os.getenv("NEOMUNDI_BASE_URL")

    if not api_key:
        sys.exit("Missing environment variable: NEOMUNDI_API_KEY")

    if not base_url:
        sys.exit("Missing environment variable: NEOMUNDI_BASE_URL")

    payload = load_json(args.request)

    run_id = str(uuid.uuid4())

    journal = {
        "run_id": run_id,
        "started_at": utc_now(),
        "endpoint": DEFAULT_ENDPOINT,
        "request": payload,
        "http_status": None,
        "events": [],
        "completed_at": None
    }

    journal_path = JOURNAL_DIR / f"{run_id}.json"

    headers = {
        "X-API-Key": api_key,
        "Accept": "text/event-stream",
        "Content-Type": "application/json"
    }

    url = base_url.rstrip("/") + DEFAULT_ENDPOINT

    print()
    print("NeoMundi Continuous Control Launcher")
    print("------------------------------------")
    print(f"Run ID: {run_id}")
    print(f"Endpoint: {url}")
    print()

    try:
        with requests.post(
            url,
            headers=headers,
            json=payload,
            stream=True,
            timeout=120
        ) as response:

            journal["http_status"] = response.status_code

            if response.status_code != 200:
                journal["error"] = response.text
                journal["completed_at"] = utc_now()

                write_json(journal_path, journal)

                print(f"HTTP {response.status_code}")
                print(response.text)
                print()
                print(f"Journal: {journal_path}")

                sys.exit(1)

            print("Runtime stream activated.")
            print()

            for raw_line in response.iter_lines(decode_unicode=True):

                if not raw_line:
                    continue

                event = {
                    "timestamp": utc_now(),
                    "raw": raw_line
                }

                journal["events"].append(event)

                print(raw_line)

    except requests.RequestException as exc:

        journal["error"] = str(exc)
        journal["completed_at"] = utc_now()

        write_json(journal_path, journal)

        print(f"Connection error: {exc}")

        sys.exit(1)

    journal["completed_at"] = utc_now()

    write_json(journal_path, journal)

    print()
    print("------------------------------------")
    print("Runtime measurement completed.")
    print(f"Journal: {journal_path}")


if __name__ == "__main__":
    main()
