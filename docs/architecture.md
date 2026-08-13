# Architecture

## Purpose

The Human Model represents changing human-domain state without confusing an observation, an inference, or a model output with settled fact. It is a domain system, not an interface. Its architecture is organized around evidence lineage, reviewable canonical state, and bounded projections.

## The state loop

```text
source
  -> observation
  -> evidence
  -> interpretation
  -> claim
  -> review / confirmation policy
  -> canonical state

canonical state + hypothesis
  -> prediction
  -> human judgment
  -> intervention
  -> outcome
  -> correction or learning update
```

The arrows mean “may inform,” not “automatically becomes.” A source can be unreliable. An observation can be incomplete. Evidence is question-dependent. An interpretation can be wrong. A claim remains a claim even when a model states it fluently.

## Ontology

### Source

The origin of information: a person, device, file, service, resident, or derived process. Source identity and acquisition time belong in provenance.

### Observation

A source-bound account of something measured or reported. Observations should be appendable and correctable. They should not be silently rewritten into interpretations.

### Evidence

Observations selected or transformed for a particular question. Derived evidence retains links to its inputs, method or version, and relevant uncertainty.

### Interpretation

Meaning assigned to evidence by a person or computational process. Interpretations identify their author and should be revisable.

### Claim

A reviewable assertion about the person or situation. A claim has support, scope, time, and epistemic status. Model generation is provenance, not proof.

### Hypothesis

A provisional explanation that can guide a prediction or intervention. Competing hypotheses may coexist.

### Prediction

An expected future observation or outcome, recorded before the result where possible. Predictions make learning claims testable.

### Canonical state

The Human Model's accepted, versioned account for operational use. Canonical means authoritative inside the domain, not metaphysically true. State can be superseded or corrected while history remains traceable.

### Intervention

A deliberate action intended to affect state or test a hypothesis. It records who proposed it, who authorized it, what was done, and when.

### Outcome

Evidence observed after an intervention or passage of time. An outcome does not by itself establish causality.

### Correction

A traceable amendment, rejection, or supersession. A correction points to what it changes and why. Downstream derived state must be reviewable or recomputable when its support changes.

### Projection

A bounded view of canonical state and evidence prepared for one consumer, purpose, and authority. Projections should minimize disclosure and prevent consumers from accidentally becoming competing sources of truth.

## Epistemic status

Important values should be distinguishable as:

- **observed** — directly reported or measured, with a source;
- **inferred** — derived or interpreted from evidence;
- **confirmed** — explicitly accepted by an authorized human or policy.

These labels answer different questions from confidence. A confirmed preference may have high authority but limited duration. A highly reliable measurement is observed, not human-confirmed. Missing values remain missing. Conflicting sources remain visible until a policy or person resolves them.

Confidence, decay, and revalidation are useful design concepts, but they are not claimed as generalized implemented capabilities. Where used, they need explicit scope, rationale, and review behavior.

## Ownership

### Human Model

Owns canonical human-domain state and its provenance: accepted training and nutrition state, measurements, evidence, corrections, and other scoped human facts. It exposes reads and bounded projections and accepts writes only through defined authority and validation.

### Coach

Consumes a fitness-relevant projection. It owns specialized interpretation, coaching judgment, and proposals. A coaching plan may be produced by Coach as a proposal; after acceptance, its canonical representation and history belong to the Human Model.

Coach does not silently write canonical state. The current private action path records confirmation but does not yet apply every confirmed proposal as a canonical mutation. That incomplete mutation work is **planned**.

### Bridget

Supports continuity, reconciliation, attention, and conversational coordination. Bridget may help gather or reconcile information, but does not own the Human Model and is not a mandatory gateway. The Human Model remains usable without Bridget.

### Wonderful Digital World

WDW is the broader persistent environment in which multiple domain systems and residents can operate. It does not absorb Human Model ownership. Residents receive minimum-sufficient projections appropriate to role, task, and authority.

## Plan and schedule semantics

Program content, program order, an intended plan, and an actual schedule are different claims.

- Imported program order is source evidence.
- Coach may interpret that evidence and propose a plan.
- A person confirms the operative plan and any scheduling anchor.
- The Human Model stores the accepted plan or schedule as canonical, versioned state.
- Later changes supersede rather than silently overwrite earlier decisions.

This avoids manufacturing a schedule from an import and makes the difference between “suggested,” “accepted,” and “performed” inspectable.

## Interfaces

Dashboards, chat surfaces, spreadsheets, messaging bots, voice, and movement-analysis tools can all read projections or contribute observations. None defines the model.

An interface can be replaced without migrating ownership. Its output does not become canonical merely because it is convenient or visually polished. Historical interfaces in this repository are kept as design evidence and labeled accordingly.

## Learning and correction

The architecture supports learning as a disciplined update process:

1. record the hypothesis or expectation;
2. preserve the evidence available at the time;
3. record the intervention and authorization;
4. observe outcomes;
5. compare outcome with prediction;
6. update, retain, or reject the hypothesis;
7. allow the person to inspect and correct the resulting state.

This is narrower than claiming the system “learns the person” automatically. Behavioral traces, corrections, and repeated workflow friction can be evidence. They are not self-interpreting, and they do not grant authority for high-impact action.

## Public/private boundary

This repository publishes concepts and synthetic examples. It intentionally omits private schemas, data, prompts, operational thresholds, calibration logic, and cross-system contracts. The public evidence-review toy demonstrates provenance and explicit lack of support in a deliberately narrow fixture without claiming production parity.

## Invariants

1. Canonical human-domain state has one owner.
2. Every important derived claim can identify its support.
3. Missingness and conflict are represented explicitly.
4. Model-generated claims are not facts by default.
5. Corrections are traceable and do not erase history.
6. Projections are purpose-bound and authority-bound.
7. Higher-impact mutations require stronger confirmation.
8. Interfaces do not acquire domain ownership.
9. The Human Model works independently of any resident.
10. Historical artifacts never establish current implementation status.
