# Project Evolution

The Human Model did not begin as a clean abstraction. It emerged through repeated attempts to make a real bodybuilding and performance workflow retain context. This history is valuable because it shows which concerns persisted as interfaces changed.

## 1. Documents and spreadsheets

**Status: Historical**

Early plans, logs, and summaries lived in documents and sheets. They were practical but fragmented. The same information was repeatedly copied, reconciled, and re-explained.

Lesson: durable continuity needs structured ownership and provenance, not only better summaries.

## 2. Recovery and readiness models

**Status: Historical foundation / current research question**

Recovery modeling introduced explicit inputs, missingness, weighting, and daily decisions. It also exposed how easily a score can overstate certainty or hide conflicting sources.

Lesson: derived values need lineage and review; a score is evidence for judgment, not a verdict.

## 3. Bridget and Telegram workflows

**Status: Historical interface; universal gateway rejected**

Conversation and messaging reduced interaction cost and created useful continuity experiments. Over time, too much architecture was described through one assistant and one transport.

Lesson: conversational continuity is useful, but canonical domain state should not belong to a chatbot or require it as a gateway.

## 4. Coach dashboard

**Status: Historical prototype**

The dashboard brought training, recovery, body, signals, and reviews into one view. It helped reveal missing provenance, ambiguous status, and the need to distinguish evidence from interpretation.

Lesson: a dashboard can make a model legible, but it is not the model.

## 5. Sensing and movement experiments

**Status: Experimental / historical prototypes**

Media ingestion and movement overlays explored richer observations. These experiments were not validated as assessment systems.

Lesson: new sensing increases the provenance and uncertainty burden; video does not become a trustworthy conclusion merely because a model can process it.

## 6. Canonical Human Model domain

**Status: Implemented and dogfooded in a bounded performance domain**

The architecture separated canonical human-domain evidence from interfaces and specialist judgment. Source normalization, explicit scheduling state, provenance-aware derived evidence, and bounded reads became domain responsibilities.

Lesson: one owner for accepted domain state prevents dashboards, agents, and notes from becoming competing truths.

## 7. Resident and world boundaries

**Status: Current architecture; partly dogfooded**

The Wonderful Digital World introduced a broader environment with specialist residents. Coach owns coaching judgment and proposals. Bridget owns continuity and reconciliation. Each consumes bounded context without absorbing Human Model ownership.

Lesson: useful persistence comes from stable boundaries and minimum-sufficient projections, not universal access to a person-shaped context blob.

## What remained stable

- The bodybuilding and performance origin supplies the strongest evidence.
- Human correction matters more than polished prediction.
- State changes over time and must retain history.
- Interfaces are replaceable.
- Source, interpretation, accepted state, and action authority must be separated.

## What was narrowed or rejected

- The project is not a dashboard product.
- Bridget is not the Human Model and is not a mandatory gateway.
- Telegram is not the current architecture.
- A model-generated claim is not automatically knowledge.
- Behavior is not automatically intent or consent.
- Confirmed action recording is not the same as completed canonical mutation.

Historical documents, screenshots, and examples remain in the repository with explicit classifications. They show the path to the current architecture without being allowed to define it.
