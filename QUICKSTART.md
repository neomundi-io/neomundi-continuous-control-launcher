# NeoMundi Continuous Control Launcher — Quickstart

[🇫🇷 Français](#français) | [🇬🇧 English](#english)

---

# Français

## En 30 secondes : c’est quoi, pourquoi, pour qui ?

### C’est quoi ?

Le **NeoMundi Continuous Control Launcher** est un petit lanceur qui permet d’ajouter une couche NeoMundi autour d’un appel à une IA.

Il prend une requête, la fait passer par NeoMundi, récupère les signaux runtime et conserve une trace de ce qui s’est passé.

En version très simple :

```text
Votre requête
     ↓
Votre IA
     ↓
NeoMundi regarde ce qui se passe
     ↓
NeoMundi renvoie des mesures et des signaux
     ↓
Le launcher garde une trace
```

### Pourquoi ?

Parce qu’une IA peut produire une réponse qui semble fluide et convaincante sans que son comportement soit forcément stable ou sans que tout soit factuellement correct.

NeoMundi ajoute une **couche de mesure**.

Le launcher permet ensuite de garder les signaux et la trace de chaque exécution afin qu’ils puissent être utilisés pour :

- surveiller ;
- investiguer ;
- comparer ;
- vérifier ;
- déclencher une revue humaine ;
- rerouter ;
- arrêter un flux si le système client le décide.

> **NeoMundi mesure et signale. Le client décide quoi faire.**

### Pour qui ?

Ce launcher est destiné aux personnes et organisations qui utilisent déjà des modèles d’IA et souhaitent ajouter une couche de mesure et de traçabilité sans reconstruire leur infrastructure.

Par exemple :

- développeurs ;
- équipes IA ;
- intégrateurs ;
- responsables sécurité ;
- équipes conformité ;
- équipes gouvernance IA ;
- chercheurs ;
- entreprises utilisant plusieurs providers d’IA.

---

# Quickstart

## 1. Cloner le dépôt

```bash
git clone https://github.com/neomundi-io/neomundi-continuous-control-launcher.git
cd neomundi-continuous-control-launcher
```

## 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 3. Créer le fichier local `.env`

Copier le fichier d’exemple :

```bash
cp .env.example .env
```

Sous Windows PowerShell :

```powershell
Copy-Item .env.example .env
```

Puis renseigner localement les clés nécessaires.

Exemple :

```env
NEOMUNDI_API_KEY=your_neomundi_key
NEOMUNDI_BASE_URL=https://api.neomundi.io

OPENAI_API_KEY=your_openai_key
```

> Le fichier `.env` ne doit jamais être poussé sur GitHub.

Les clés appartiennent au client et restent dans son environnement local.

---

## 4. Vérifier la requête d’exemple

Le fichier `example_request.json` contient une requête minimale :

```json
{
  "prompt": "Explain why runtime stability should not be confused with factual correctness.",
  "model": "gpt-4o-2024-11-20",
  "provider": "openai"
}
```

La clé du provider n’est pas stockée dans ce fichier.

Elle est récupérée depuis l’environnement du client.

---

## 5. Charger les variables d’environnement

Le launcher lit les variables d’environnement du système.

Si votre environnement ne charge pas automatiquement le fichier `.env`, exportez les variables avant l’exécution.

### Linux / macOS

```bash
export NEOMUNDI_API_KEY="your_neomundi_key"
export NEOMUNDI_BASE_URL="https://api.neomundi.io"
export OPENAI_API_KEY="your_openai_key"
```

### Windows PowerShell

```powershell
$env:NEOMUNDI_API_KEY="your_neomundi_key"
$env:NEOMUNDI_BASE_URL="https://api.neomundi.io"
$env:OPENAI_API_KEY="your_openai_key"
```

---

## 6. Activer la couche NeoMundi

Lancer :

```bash
python launcher.py example_request.json
```

Le flux est volontairement simple :

```text
REQUÊTE
   ↓
EXÉCUTION IA
   ↓
MESURE RUNTIME NEOMUNDI
   ↓
SIGNAUX
   ↓
JOURNAL
   ↓
ACTION ÉVENTUELLE CÔTÉ CLIENT
```

Le launcher n’ajoute pas de nouveaux seuils métrologiques.

Il utilise les signaux produits par NeoMundi.

---

## 7. Lire le résultat

Chaque exécution reçoit un identifiant unique `run_id`.

Le journal correspondant est enregistré localement dans :

```text
journal/<run_id>.json
```

Selon les informations disponibles, le journal peut contenir :

- l’identifiant d’exécution ;
- les horodatages ;
- le provider ;
- le modèle ;
- la requête ;
- la réponse générée ;
- les événements runtime ;
- les mesures NeoMundi ;
- la décision `ALLOW` ou `FLAG` ;
- les métadonnées techniques disponibles.

Les clés API ne doivent jamais être enregistrées dans le journal.

---

## 8. Comprendre les signaux

La documentation d’interprétation se trouve ici :

```text
docs/SIGNALS.md
```

Principe essentiel :

```text
SIGNAL ≠ VERDICT
```

NeoMundi fournit des informations sur le comportement observé.

Le système client choisit ensuite comment les utiliser.

Par exemple :

```text
Signal NeoMundi
      ↓
Politique client
      ├── continuer
      ├── journaliser
      ├── vérifier
      ├── régénérer
      ├── rerouter
      ├── revue humaine
      └── arrêter
```

---

## 9. Providers

Le launcher est conçu pour être utilisé avec plusieurs providers.

Documentation d’intégration :

https://github.com/neomundi-io/controltowerai-docs/blob/main/providers.md

Les clés providers restent fournies et contrôlées par le client.

---

## 10. Sécurité

Ne jamais placer une vraie clé API dans :

- `README.md` ;
- `QUICKSTART.md` ;
- `example_request.json` ;
- `config.example.json` ;
- le code source ;
- un commit GitHub.

Les secrets doivent rester dans l’environnement local du client.

Le dépôt ignore notamment :

```text
.env
journal/
logs/
output/
```

---

## 11. Statut

Cette version est un **MVP expérimental**.

Avant toute utilisation en production, le launcher doit être validé sur l’API NeoMundi réelle et dans l’environnement cible.

---

# English

## In 30 seconds: what is it, why does it exist, and who is it for?

### What is it?

The **NeoMundi Continuous Control Launcher** is a lightweight launcher designed to add a NeoMundi layer around an AI request.

It sends the request through NeoMundi, receives runtime signals and keeps a trace of what happened.

In very simple terms:

```text
Your request
     ↓
Your AI
     ↓
NeoMundi observes what happens
     ↓
NeoMundi returns measurements and signals
     ↓
The launcher keeps a trace
```

### Why?

Because an AI can produce a fluent and convincing answer while its behavior may not be fully stable or its content may not be factually correct.

NeoMundi adds a **measurement layer**.

The launcher keeps the resulting signals and execution trace so they can be used to:

- monitor;
- investigate;
- compare;
- verify;
- trigger human review;
- reroute;
- stop a workflow if the client system decides to do so.

> **NeoMundi measures and signals. The client decides what action to take.**

### Who is it for?

This launcher is intended for people and organizations already using AI models who want to add measurement and traceability without rebuilding their infrastructure.

For example:

- developers;
- AI teams;
- integrators;
- security teams;
- compliance teams;
- AI governance teams;
- researchers;
- organizations using multiple AI providers.

---

# Quickstart

## 1. Clone the repository

```bash
git clone https://github.com/neomundi-io/neomundi-continuous-control-launcher.git
cd neomundi-continuous-control-launcher
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Create the local `.env` file

Copy the example file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Then add the required keys locally.

Example:

```env
NEOMUNDI_API_KEY=your_neomundi_key
NEOMUNDI_BASE_URL=https://api.neomundi.io

OPENAI_API_KEY=your_openai_key
```

> The `.env` file must never be committed to GitHub.

The keys belong to the client and remain in the client environment.

---

## 4. Check the example request

The `example_request.json` file contains a minimal request:

```json
{
  "prompt": "Explain why runtime stability should not be confused with factual correctness.",
  "model": "gpt-4o-2024-11-20",
  "provider": "openai"
}
```

The provider API key is not stored in this file.

It is resolved from the client environment.

---

## 5. Load environment variables

The launcher reads system environment variables.

If your environment does not automatically load the `.env` file, export the variables before execution.

### Linux / macOS

```bash
export NEOMUNDI_API_KEY="your_neomundi_key"
export NEOMUNDI_BASE_URL="https://api.neomundi.io"
export OPENAI_API_KEY="your_openai_key"
```

### Windows PowerShell

```powershell
$env:NEOMUNDI_API_KEY="your_neomundi_key"
$env:NEOMUNDI_BASE_URL="https://api.neomundi.io"
$env:OPENAI_API_KEY="your_openai_key"
```

---

## 6. Activate the NeoMundi layer

Run:

```bash
python launcher.py example_request.json
```

The flow is intentionally simple:

```text
REQUEST
   ↓
AI EXECUTION
   ↓
NEOMUNDI RUNTIME MEASUREMENT
   ↓
SIGNALS
   ↓
JOURNAL
   ↓
OPTIONAL CLIENT-SIDE ACTION
```

The launcher does not introduce new metrological thresholds.

It uses the signals produced by NeoMundi.

---

## 7. Read the result

Each execution receives a unique `run_id`.

The corresponding journal is stored locally in:

```text
journal/<run_id>.json
```

Depending on the available information, the journal may contain:

- execution identifier;
- timestamps;
- provider;
- model;
- request;
- generated response;
- runtime events;
- NeoMundi measurements;
- `ALLOW` or `FLAG` decision;
- available technical metadata.

API keys must never be stored in the journal.

---

## 8. Understand the signals

Signal interpretation documentation is available here:

```text
docs/SIGNALS.md
```

Core principle:

```text
SIGNAL ≠ VERDICT
```

NeoMundi provides information about observed behavior.

The client system then decides how to use it.

For example:

```text
NeoMundi signal
      ↓
Client policy
      ├── continue
      ├── log
      ├── verify
      ├── regenerate
      ├── reroute
      ├── human review
      └── stop
```

---

## 9. Providers

The launcher is designed to support multiple providers.

Provider integration documentation:

https://github.com/neomundi-io/controltowerai-docs/blob/main/providers.md

Provider keys remain supplied and controlled by the client.

---

## 10. Security

Never place a real API key inside:

- `README.md`;
- `QUICKSTART.md`;
- `example_request.json`;
- `config.example.json`;
- source code;
- a GitHub commit.

Secrets must remain in the client environment.

The repository ignores, among other things:

```text
.env
journal/
logs/
output/
```

---

## 11. Status

This version is an **experimental MVP**.

Before production use, the launcher must be validated against the real NeoMundi API and in the target environment.
