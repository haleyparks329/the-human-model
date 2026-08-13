# The Human Model

The Human Model is an engineering and research project for representing a changing person as longitudinal, provenance-aware, reviewable state.

Its central question is:

> How can a system remain useful across time without reducing a person to a static profile or treating uncertain evidence as fact?

The project began in bodybuilding and performance coaching, where training, nutrition, recovery, measurements, plans, and lived context change continually. That origin remains a demanding test case. The architecture is broader: any long-running human-facing system must distinguish what was observed, what was inferred, what was confirmed, what changed, and why.

“I am not a Markdown file” is the shorthand. The engineering consequence is not that documents are useless; it is that a person cannot be faithfully represented by one timeless summary.

## What it is now

The Human Model is an independent domain system. It owns canonical human-domain state: the accepted, reviewable account of relevant observations, claims, corrections, plans, interventions, and outcomes. Canonical means authoritative within this domain, not objectively or permanently true.

It is not a chatbot, dashboard, prompt, database table, or autonomous digital person. Those can be interfaces or experiments around it. The interface is disposable; the model persists.

The current architecture is built around four requirements:

1. **Longitudinal state.** Represent change over time rather than overwrite history with a latest value.
2. **Provenance.** Retain where information came from and how derived state was produced.
3. **Reviewability.** Let a person inspect, correct, confirm, supersede, or reject important claims.
4. **Bounded use.** Give each consumer only the projection it needs for its role and authority.

## The model loop

```text
source -> observation -> evidence -> interpretation
                                  -> claim -> canonical state

canonical state + hypothesis -> prediction -> human judgment
                             -> intervention -> outcome
                             -> correction / learning update
```

This is a review loop, not a pipeline that converts every input into truth. A wearable reading may become an observation. Several observations may support evidence. A model or human may interpret that evidence and make a claim. Only explicit policy and, where appropriate, human confirmation can make that claim part of canonical state.

Outcomes can support, weaken, or leave a hypothesis unresolved. Corrections remain traceable instead of silently rewriting the past. Missing data stays missing; uncertainty is represented rather than filled with confidence-shaped prose.

See [Architecture](docs/architecture.md) for the ontology and ownership rules.

## System boundaries

The Human Model can be used on its own. In the wider Wonderful Digital World (WDW), it is one domain system inside a persistent environment.

| Component | Owns | Does not own |
| --- | --- | --- |
| **Human Model** | Canonical human-domain evidence and accepted state | General conversation, resident identity, every application workflow |
| **WDW** | The broader persistent environment and cross-domain coordination | Human-domain canonical state |
| **Coach** | Specialized interpretation, coaching judgment, plans as proposals, and proposed actions | Canonical Human Model writes or silent scheduling decisions |
| **Bridget** | Continuity, reconciliation, attention, and conversational coordination | The Human Model, all domain state, or mandatory access to the system |
| **Interfaces** | Presentation and task-specific interaction | Durable truth merely because they display or collect it |

WDW residents receive bounded projections: the minimum sufficient context for their role, task, and authority. A projection is a purpose-built view, not a second canonical record.

### Plan ownership

Coach may interpret evidence and formulate a coaching plan or proposed change. Once a plan or schedule is accepted as the person's operative state, the Human Model owns its canonical representation, including provenance and supersession history.

The current private implementation records confirmed proposed actions but does not yet apply every approved action as a canonical mutation. That gap is documented as **planned**, not presented here as completed automation. Imported program order is not silently treated as an actual schedule; scheduling requires an explicit, confirmed anchor.

## Ontology in brief

| Term | Meaning |
| --- | --- |
| **Source** | An origin such as a person, device, file, service, or resident |
| **Observation** | A source-bound record of something reported or measured |
| **Evidence** | One or more observations made usable for a question, with lineage |
| **Interpretation** | A meaning assigned to evidence by a human or model |
| **Claim** | A reviewable assertion; model-generated does not mean fact |
| **Hypothesis** | A provisional explanation that could be tested or revised |
| **Prediction** | An expected future observation or outcome |
| **Canonical state** | The domain's accepted, versioned account for current use |
| **Intervention** | A deliberate action intended to affect state or test a hypothesis |
| **Outcome** | What was observed after an intervention or passage of time |
| **Correction** | A traceable challenge, amendment, rejection, or supersession |
| **Projection** | A bounded view prepared for a specific consumer and purpose |

Information should also carry an epistemic status where relevant: **observed**, **inferred**, or **confirmed**. These statuses must not be collapsed into one generic “known” field.

## Evidence and implementation status

This repository uses a strict vocabulary:

- **Implemented** — exists in running code with relevant tests or operational evidence.
- **Dogfooded** — used in the maintainer's own workflow; this is evidence of use, not general validation.
- **Experimental** — being explored; its shape or value remains unsettled.
- **Historical** — useful lineage, but not the current interface or contract.
- **Planned** — intended work without a completed implementation claim.
- **Rejected** — explicitly not part of the architecture.

At the public level:

| Area | Status | Evidence represented here |
| --- | --- | --- |
| Evidence and provenance review toy | Implemented | Runnable synthetic example and tests |
| Current private Human Model evidence core | Implemented | Public claim limited to boundaries; private schema and contracts are not reproduced |
| Bounded resident projections | Dogfooded | Architectural relationship is current; private contracts are intentionally omitted |
| General confidence decay and revalidation | Planned | Design direction, not a system-wide capability claim |
| Automatic learning from all behavior | Rejected | Behavioral traces may be evidence; they are not permission or truth |
| Dashboard as the product | Historical | Screenshots are retained as lineage |
| Telegram/Bridget as the required gateway | Rejected | Historical screenshots do not define the current architecture |
| Movement-video analysis | Experimental | A historical prototype, not validated assessment |

For the claim-by-claim audit, see the [Evidence map](docs/evidence-map.md).

## Three public layers

### 1. Research question

The durable problem is representing changing human context without false certainty, memory drift, or accidental authority. Start with [Why the Human Model](docs/why-the-human-model.md), [Philosophy](docs/philosophy.md), and [Research notes](docs/research-notes.md).

### 2. Architecture

The architecture defines domain ownership, evidence lineage, review, corrections, projections, and human authority. Read [Architecture](docs/architecture.md), [Design principles](docs/design-principles.md), and [Source context](docs/source-context.md).

### 3. Applications and experiments

Bodybuilding, recovery, readiness, dashboards, chat, sensing, and movement analysis are applications or experiments around the core question. Their presence does not make any one interface the Human Model. See [Project evolution](docs/project-evolution.md) and the [asset manifest](assets/asset-manifest.md).

## Runnable public reference

[`examples/toy_evidence_review.py`](examples/toy_evidence_review.py) is a synthetic, self-contained example of a narrow architectural property:

- claims remain linked to source observations;
- unsupported claims remain explicitly unsupported;
- deterministic behavior is covered by tests.

It is a public teaching artifact, not a readiness algorithm or a mirror of private production code, schema, thresholds, prompts, data, or WDW contracts.

Run it with:

```bash
python3 examples/toy_evidence_review.py
python3 -m unittest examples/tests/test_toy_evidence_review.py
```

Additional [examples](examples/README.md) are synthetic demonstrations. Some intentionally preserve historical interface ideas so their lineage can be examined without claiming current parity.

## What this repository protects

This public repository documents the research direction, architectural boundaries, historical evolution, and synthetic examples. It does not publish private personal data, production schemas, private prompts, behavioral calibration, operational thresholds, or private cross-system contracts.

That boundary matters technically. A model about a person should make access, purpose, provenance, and authority legible—not normalize exporting a complete person-shaped record everywhere.

## Human-centered adaptation

The system should adapt, but not mistake surveillance for understanding. Repeated manual corrections, workaround spreadsheets, ignored prompts, and workflow friction can signal that the model or interface is wrong. They are evidence to review with the person, not defects in the person and not automatic consent to infer more.

Useful adaptation preserves judgment:

- make uncertainty visible;
- expose why a claim exists;
- let corrections change future behavior without erasing history;
- treat desire paths as design evidence;
- require stronger confirmation as impact and ambiguity increase.

## Navigation

- [Architecture](docs/architecture.md)
- [Design principles](docs/design-principles.md)
- [Project evolution](docs/project-evolution.md)
- [Evidence map](docs/evidence-map.md)
- [Roadmap](docs/roadmap.md)
- [Public examples](examples/README.md)
- [Asset manifest](assets/asset-manifest.md)

## Current limits

The Human Model does not claim to model a whole person, remove the need for judgment, or infer intent reliably from behavior. It does not make medical diagnoses. Its current strongest evidence comes from a single maintainer's performance and health workflow, so generality remains a research question.

The immediate work is less glamorous and more important: strengthen correction and supersession semantics, complete confirmation-gated canonical mutations, evaluate projection sufficiency, and test whether the model remains understandable over longer time horizons.
