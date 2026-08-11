# NeoMundi Continuous Control Launcher

[🇫🇷 Français](#français) | [🇬🇧 English](#english)

**FR — Lanceur minimal de contrôle continu pour transformer les signaux de mesure NeoMundi en actions opérationnelles traçables.**

**EN — Minimal runtime launcher to turn NeoMundi measurement signals into continuous AI control actions with traceability.**

---

## Français

### Objectif

Le NeoMundi Continuous Control Launcher fournit une couche légère de contrôle entre les systèmes d’IA et les infrastructures opérationnelles.

Il ne remplace pas l’infrastructure existante.

Il consomme les signaux de mesure runtime produits par NeoMundi, applique des règles de contrôle configurables et produit des actions opérationnelles traçables.

```text
Exécution IA
     ↓
Signaux de mesure NeoMundi
     ↓
Continuous Control Launcher
     ↓
Politique de contrôle
     ↓
ALLOW
FLAG
REROUTE
HUMAN_REVIEW
STOP
     ↓
Reçu de contrôle traçable
```

### Principe central

**Mesurer d’abord. Décider ensuite.**

NeoMundi produit des mesures comportementales et des signaux runtime.

L’organisation qui utilise le launcher définit :

- les seuils ;
- les politiques ;
- les règles d’escalade ;
- les règles de reroutage ;
- les exigences de supervision humaine ;
- les conditions d’arrêt.

Un signal NeoMundi n’est pas un verdict.

Il constitue une entrée pour une politique de contrôle runtime configurable.

### Profils fournisseurs par défaut

La première configuration du launcher cible 10 profils fournisseurs/modèles :

1. OpenAI
2. Anthropic
3. Google Gemini
4. Mistral AI
5. Infomaniak / Mistral
6. Cohere
7. DeepSeek
8. xAI / Grok
9. Groq / Llama
10. Perplexity / Sonar

Documentation d’intégration des fournisseurs :

https://github.com/neomundi-io/controltowerai-docs/blob/main/providers.md

L’architecture reste indépendante des fournisseurs. D’autres profils peuvent être ajoutés par configuration sans modifier la logique de contrôle.

### Actions de contrôle

Le contrat initial prend en charge cinq actions :

- `ALLOW`
- `FLAG`
- `REROUTE`
- `HUMAN_REVIEW`
- `STOP`

### MVP

La première version doit :

1. recevoir un payload de mesure compatible NeoMundi ;
2. lire une politique de contrôle locale ;
3. évaluer les signaux mesurés ;
4. produire une action runtime ;
5. générer un reçu de contrôle traçable.

### Architecture

```text
measurement.json
        +
control_policy.json
        ↓
    launcher.py
        ↓
control_decision.json
```

Aucune clé API n’est stockée dans le dépôt.

### Statut

MVP expérimental — développement actif.

Fait partie de l’infrastructure NeoMundi de mesure et de gouvernance runtime.

https://neomundi.org

---

## English

### Purpose

The NeoMundi Continuous Control Launcher provides a lightweight control layer between AI systems and operational infrastructure.

It does not replace existing infrastructure.

It consumes NeoMundi runtime measurement signals, applies configurable control rules, and produces traceable operational actions.

```text
AI execution
     ↓
NeoMundi measurement signals
     ↓
Continuous Control Launcher
     ↓
Control policy
     ↓
ALLOW
FLAG
REROUTE
HUMAN_REVIEW
STOP
     ↓
Traceable control receipt
```

### Core principle

**Measurement first. Decision second.**

NeoMundi produces behavioral measurements and runtime signals.

The organization using the launcher defines:

- thresholds;
- policies;
- escalation rules;
- rerouting rules;
- human supervision requirements;
- stop conditions.

A NeoMundi signal is not a verdict.

It is an input to a configurable runtime control policy.

### Default provider profiles

The first launcher configuration targets 10 AI provider/model profiles:

1. OpenAI
2. Anthropic
3. Google Gemini
4. Mistral AI
5. Infomaniak / Mistral
6. Cohere
7. DeepSeek
8. xAI / Grok
9. Groq / Llama
10. Perplexity / Sonar

Provider integration documentation:

https://github.com/neomundi-io/controltowerai-docs/blob/main/providers.md

The architecture is provider-agnostic. Additional providers can be added through configuration without modifying the control logic.

### Control actions

The initial control contract supports five actions:

- `ALLOW`
- `FLAG`
- `REROUTE`
- `HUMAN_REVIEW`
- `STOP`

### MVP

The first version will:

1. receive a NeoMundi-compatible measurement payload;
2. read a local control policy;
3. evaluate the measurement signals;
4. return a runtime action;
5. generate a traceable control receipt.

### Architecture

```text
measurement.json
        +
control_policy.json
        ↓
    launcher.py
        ↓
control_decision.json
```

No API key is stored in the repository.

### Status

Experimental MVP — under active development.

Part of the NeoMundi runtime measurement and governance infrastructure.

https://neomundi.org
