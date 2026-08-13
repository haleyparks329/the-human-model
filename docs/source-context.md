# Source Context

Source context is the information needed to understand where an observation came from, what it can support, and how much authority it has. Without it, systems turn convenient values into unattributed truth.

## Source is not truth

A person, wearable, import, resident, file, and derived process can all be sources. Each has different failure modes. The Human Model preserves source identity while allowing later evidence and policy to resolve conflicts.

Useful source context can include:

- source type and stable identifier;
- acquisition method and time;
- the period the observation describes;
- original units or representation;
- validation or parse result;
- revision or import version;
- links to upstream observations;
- stated uncertainty or missingness;
- authority to report, propose, confirm, or mutate.

The exact private schema is intentionally not published here.

## Source, observation, and evidence

These terms are deliberately separate.

```text
source: a wearable export
observation: the export reports a sleep duration for a date
evidence: that observation is available and valid for today's readiness question
interpretation: reduced sleep may increase recovery risk
claim: readiness is probably lower than baseline
```

The final claim is not a fact merely because the earlier observation was measured. Each transition adds assumptions.

## Conflict

When sources disagree, retain the disagreement until an explicit policy or authorized person resolves it. Resolution can consider recency, directness, known reliability, and purpose, but should preserve the losing source and reason.

Example: imported program order, a coaching proposal, a calendar entry, and a person's confirmation are not equivalent evidence of an actual training schedule.

## Missingness and invalidity

At minimum, distinguish:

- not provided;
- source unavailable;
- present but invalid;
- outside the relevant time window;
- conflicting;
- withheld or not authorized for this consumer;
- not applicable.

Collapsing these into `null` can erase operational and ethical differences. Public examples demonstrate a subset without claiming complete production semantics.

## Derived lineage

A derived value should be able to identify:

1. the observations or evidence it used;
2. the transformation or model version;
3. the time and purpose of derivation;
4. uncertainty and missing inputs;
5. what correction would invalidate or require recomputation.

This applies to readiness scores, summaries, projections, and model-generated claims.

## Bounded projections

A projection includes the minimum source-backed context a consumer needs. It may omit sensitive or irrelevant evidence and can expose absence without exposing why data was withheld. Projection policy is part of system design, not just serialization.

Coach, Bridget, and other WDW residents do not need identical context. Their views should reflect role and authority rather than convenience.

## Public source policy

This repository uses synthetic fixtures and sanitized conceptual descriptions. Public examples must not reproduce private personal records, production schemas, prompts, thresholds, or private WDW contracts. Historical screenshots are classified as lineage and should not be read as current source or ownership contracts.
