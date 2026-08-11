# NeoMundi Runtime Signals

[🇫🇷 Français](#français) | [🇬🇧 English](#english)

---

# Français

## 1. Objet

NeoMundi produit des mesures et des signaux sur le comportement d’un système d’IA pendant ou à l’issue de son exécution.

Ces signaux permettent notamment d’observer :

- la stabilité runtime ;
- les variations de stabilité ;
- les zones de tension ou de rupture ;
- la cohérence sémantique ;
- les signaux de risque factuel ;
- le régime comportemental ;
- les décisions runtime `ALLOW` ou `FLAG`.

Le Continuous Control Launcher expose ces informations et les journalise afin qu’elles puissent être interprétées ou utilisées par le système client.

> **Un signal NeoMundi n’est pas un verdict.**

NeoMundi mesure et signale.

Le système client reste responsable de l’interprétation opérationnelle et des actions éventuellement déclenchées.

---

## 2. Principe de lecture

La lecture recommandée est multi-signal.

Un indicateur isolé ne doit pas être utilisé comme preuve suffisante de qualité, de factualité ou de risque.

```text
Requête
   ↓
Exécution IA
   ↓
Mesures NeoMundi
   ↓
G / stabilité
∆G
profil ∆G
ALLOW / FLAG
cohérence
signal factuel
régime
   ↓
Journal
   ↓
Interprétation / politique client
```

---

## 3. ALLOW

`ALLOW` indique que les conditions métrologiques évaluées par le moteur n’ont pas produit de signal justifiant un `FLAG` selon la logique runtime NeoMundi utilisée.

### Lecture

`ALLOW` peut être lu comme :

- absence de signal runtime déclencheur dans cette exécution ;
- comportement compatible avec la zone attendue par le moteur ;
- information utilisable dans une logique de monitoring ou de gouvernance.

### Attention

`ALLOW` ne signifie pas automatiquement :

- que la réponse est vraie ;
- que la réponse est complète ;
- que la réponse est sûre dans tous les contextes ;
- qu’aucune validation externe n’est nécessaire.

Une sortie peut être comportementalement stable tout en restant factuellement incorrecte.

---

## 4. FLAG

`FLAG` est un signal runtime indiquant qu’une exécution mérite une attention particulière.

Selon le contexte, un `FLAG` peut conduire le système client à :

- journaliser l’événement ;
- renforcer une vérification ;
- demander une validation factuelle ;
- déclencher une revue humaine ;
- comparer avec une seconde génération ;
- rerouter la requête ;
- interrompre ou suspendre un flux.

Ces actions appartiennent à la politique du client.

### Important

`FLAG` ne constitue pas en lui-même une preuve automatique d’erreur.

```text
FLAG ≠ erreur certaine
FLAG = signal d’attention runtime
```

---

## 5. Stabilité / G-score

Le G-score renseigne sur une propriété de stabilité ou de cohérence du processus génératif observé.

Une valeur élevée peut correspondre à une génération stable.

Une valeur plus faible peut signaler une fragilité ou une variabilité accrue.

### Limite fondamentale

```text
Stabilité ≠ vérité
```

Une réponse peut être très stable et néanmoins factuellement incorrecte.

La stabilité ne doit donc pas être utilisée seule comme validation d’une réponse.

---

## 6. ∆G

`∆G` décrit la dynamique de variation du signal de stabilité au cours de l’exécution.

Il permet d’observer non seulement un état, mais également une transition.

Il peut faire apparaître :

- une stabilité persistante ;
- une dégradation ;
- une récupération ;
- une rupture locale ;
- une zone de tension runtime.

`∆G` doit être lu conjointement avec les autres signaux disponibles.

---

## 7. Profils ∆G

NeoMundi peut résumer certaines dynamiques de variation sous forme de profils.

### DROP

`DROP` indique une chute du signal sans récupération suffisante dans la fenêtre observée.

Il peut matérialiser une zone de tension ou de dégradation runtime.

Un profil `DROP` associé à un `FLAG` constitue une zone d’attention renforcée.

### FLAT

`FLAT` indique une dynamique relativement constante.

Il renseigne sur la stabilité de la trajectoire mais ne constitue pas une validation factuelle.

### V_SHAPE

`V_SHAPE` indique une chute suivie d’une récupération partielle ou significative du signal.

Ce profil peut être utile pour distinguer une rupture persistante d’une variation transitoire.

---

## 8. Cohérence

Le signal de cohérence renseigne sur la cohérence sémantique ou structurelle de la génération observée.

Il peut être utilisé comme une dimension complémentaire de la lecture runtime.

Une forte cohérence n’implique toutefois pas automatiquement une factualité élevée.

---

## 9. Signal de risque factuel

NeoMundi peut exposer un signal associé au risque factuel ou à l’hallucination.

Ce signal complète la mesure de stabilité.

Cette séparation est importante :

```text
Stabilité runtime
        ≠
Validation factuelle
```

Une génération peut être :

```text
stable + factuellement solide
stable + factuellement fragile
instable + factuellement correcte
instable + factuellement fragile
```

La combinaison des dimensions fournit donc davantage d’information qu’un score isolé.

---

## 10. Régime runtime

Le régime fournit une lecture synthétique du contexte comportemental observé.

Un régime tel que `STABLE` fournit un contexte utile mais ne doit pas servir seul de déclencheur opérationnel.

Il doit être croisé avec :

- la stabilité ;
- ∆G ;
- le profil ∆G ;
- `ALLOW` / `FLAG` ;
- la cohérence ;
- les signaux factuels disponibles.

---

## 11. Lecture multi-signal

La logique recommandée est :

```text
Signal isolé
     ↓
information partielle

Plusieurs signaux
     ↓
contexte métrologique plus riche

Contexte + politique client
     ↓
action éventuelle
```

Par exemple, `FLAG + DROP` peut représenter une zone d’attention runtime plus forte que `FLAG` seul.

De même, `stabilité élevée + risque factuel` peut révéler une situation de stabilité trompeuse.

---

## 12. Du signal à l’action

NeoMundi ne prescrit pas automatiquement l’action opérationnelle du système client.

Le même signal peut être utilisé différemment selon le contexte.

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

Le rôle du Continuous Control Launcher est de rendre cette articulation simple :

```text
ACTIVATE
   ↓
MEASURE
   ↓
SIGNAL
   ↓
JOURNAL
   ↓
CLIENT ACTION
```

---

## 13. Traçabilité

Chaque exécution du launcher peut produire un journal contenant notamment :

- un identifiant d’exécution ;
- l’horodatage ;
- le provider ;
- le modèle ;
- la requête ;
- la réponse générée ;
- les événements runtime disponibles ;
- les mesures NeoMundi ;
- la décision `ALLOW` ou `FLAG` ;
- les métadonnées techniques disponibles.

Les clés API ne doivent jamais être enregistrées dans les journaux.

La journalisation permet de conserver une trace exploitable pour :

- l’investigation ;
- l’audit ;
- la comparaison entre exécutions ;
- la supervision ;
- la reconstruction d’un événement ;
- l’intégration dans des systèmes de gouvernance externes.

---

## 14. Statut des règles d’interprétation

Les règles présentées ici constituent une aide à la lecture des signaux.

Elles ne constituent pas :

- une certification ;
- une garantie de factualité ;
- une politique universelle de gouvernance ;
- une validation automatique d’une sortie ;
- une prescription d’action pour tous les systèmes.

La politique opérationnelle reste dépendante du contexte d’usage, du niveau de risque et des exigences du système client.

---

# English

## 1. Purpose

NeoMundi produces measurements and signals describing the behavior of an AI system during or after execution.

These signals can expose:

- runtime stability;
- stability variations;
- tension or transition zones;
- semantic coherence;
- factual-risk signals;
- behavioral regimes;
- runtime `ALLOW` or `FLAG` decisions.

The Continuous Control Launcher exposes and journals these measurements so that they can be interpreted or consumed by the client system.

> **A NeoMundi signal is not a verdict.**

NeoMundi measures and signals.

The client system remains responsible for operational interpretation and any resulting action.

---

## 2. Reading principle

The recommended approach is multi-signal interpretation.

A single indicator should not be treated as sufficient proof of quality, factual correctness or risk.

```text
Request
   ↓
AI execution
   ↓
NeoMundi measurements
   ↓
G / stability
∆G
∆G profile
ALLOW / FLAG
coherence
factual signal
regime
   ↓
Journal
   ↓
Client interpretation / policy
```

---

## 3. ALLOW

`ALLOW` indicates that the metrological conditions evaluated by the engine did not produce a signal resulting in a `FLAG` under the NeoMundi runtime logic being used.

### Interpretation

`ALLOW` may indicate:

- no runtime triggering signal during this execution;
- behavior compatible with the region expected by the measurement engine;
- information usable by monitoring or governance systems.

### Important

`ALLOW` does not automatically mean:

- the answer is factually correct;
- the answer is complete;
- the answer is safe in every context;
- external validation is unnecessary.

An output can remain behaviorally stable while being factually incorrect.

---

## 4. FLAG

`FLAG` is a runtime signal indicating that an execution deserves additional attention.

Depending on the client context, a `FLAG` may be used to:

- journal the event;
- strengthen verification;
- request factual validation;
- trigger human review;
- compare another generation;
- reroute the request;
- suspend or stop a workflow.

These actions belong to the client policy.

### Important

`FLAG` is not automatic proof of an error.

```text
FLAG ≠ confirmed error
FLAG = runtime attention signal
```

---

## 5. Stability / G-score

The G-score provides information about a stability or coherence property of the observed generative process.

A high value may correspond to a stable generation.

A lower value may indicate increased fragility or variability.

### Fundamental limitation

```text
Stability ≠ truth
```

A response can be highly stable and still be factually incorrect.

Stability should therefore not be used alone to validate an answer.

---

## 6. ∆G

`∆G` describes the dynamics of variation in the stability signal during execution.

It makes it possible to observe not only a state, but also a transition.

It can expose:

- persistent stability;
- degradation;
- recovery;
- local rupture;
- runtime tension.

`∆G` should be interpreted together with the other available signals.

---

## 7. ∆G profiles

NeoMundi can summarize some variation dynamics as profiles.

### DROP

`DROP` indicates a drop in the signal without sufficient recovery in the observed window.

It may identify a runtime tension or degradation zone.

A `DROP` profile associated with a `FLAG` represents a stronger attention zone.

### FLAT

`FLAT` indicates a relatively constant trajectory.

It provides information about stability dynamics but does not constitute factual validation.

### V_SHAPE

`V_SHAPE` indicates a drop followed by partial or significant recovery.

This profile can help distinguish persistent degradation from a transient variation.

---

## 8. Coherence

The coherence signal provides information about the semantic or structural coherence of the observed generation.

It can be used as a complementary runtime dimension.

High coherence does not automatically imply factual correctness.

---

## 9. Factual-risk signal

NeoMundi can expose a signal associated with factual risk or hallucination.

This signal complements stability measurement.

The distinction is fundamental:

```text
Runtime stability
       ≠
Factual validation
```

A generation may therefore be:

```text
stable + factually sound
stable + factually fragile
unstable + factually correct
unstable + factually fragile
```

Combining dimensions provides more information than relying on a single score.

---

## 10. Runtime regime

The regime provides a synthetic view of the observed behavioral context.

A regime such as `STABLE` provides useful context but should not be used alone as an operational trigger.

It should be interpreted together with:

- stability;
- ∆G;
- ∆G profile;
- `ALLOW` / `FLAG`;
- coherence;
- available factual signals.

---

## 11. Multi-signal interpretation

The recommended logic is:

```text
Single signal
     ↓
partial information

Multiple signals
     ↓
richer metrological context

Context + client policy
     ↓
possible action
```

For example, `FLAG + DROP` may represent a stronger runtime attention zone than `FLAG` alone.

Likewise, `high stability + factual risk` may reveal a misleading-stability situation.

---

## 12. From signal to action

NeoMundi does not automatically prescribe the operational action of the client system.

The same signal can support different actions depending on context.

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

The Continuous Control Launcher makes this articulation simple:

```text
ACTIVATE
   ↓
MEASURE
   ↓
SIGNAL
   ↓
JOURNAL
   ↓
CLIENT ACTION
```

---

## 13. Traceability

Each launcher execution can produce a journal containing, when available:

- execution identifier;
- timestamp;
- provider;
- model;
- request;
- generated response;
- runtime events;
- NeoMundi measurements;
- `ALLOW` or `FLAG` decision;
- technical metadata.

API keys must never be stored in journals.

Journaling provides an exploitable trace for:

- investigation;
- audit;
- execution comparison;
- supervision;
- event reconstruction;
- integration with external governance systems.

---

## 14. Status of interpretation guidance

The guidance described in this document is intended to support signal interpretation.

It does not constitute:

- certification;
- a guarantee of factual correctness;
- a universal governance policy;
- automatic validation of an AI output;
- a prescribed action for every system.

Operational policy remains dependent on the use case, risk level and requirements of the client system.

---

## References

NeoMundi Research — exploratory work on runtime signal interpretation and actionability:

https://neomundi.org

Provider integration documentation:

https://github.com/neomundi-io/controltowerai-docs/blob/main/providers.md
