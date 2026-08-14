# Design Principles

## 1. Model change, not just current values

Important state needs time, validity, and supersession semantics. A latest-value record is useful as a projection, not a complete history.

## 2. Keep provenance attached

Observations identify their sources. Derived evidence and claims retain lineage to inputs and method. A displayed number without provenance should not silently become domain truth.

## 3. Separate observed, inferred, and confirmed

These are different epistemic and authority states. Confidence does not replace the distinction.

## 4. Represent missingness, conflict, and uncertainty

Unknown is not zero. Missing is not normal. Disagreement is not an invitation to average sources without policy. Uncertainty belongs in the model and interface.

## 5. Make claims reviewable

A model-generated assertion is a claim, not a fact. Important claims expose support, scope, author or process, and review state.

## 6. Correct by amendment and supersession

Do not erase history to make the present look clean. Corrections should state what changed and why; affected derived state should be invalidated, reviewed, or recomputed.

## 7. Keep one canonical domain owner

The Human Model owns canonical human-domain state. Consumers can interpret projections and submit proposals, but should not maintain competing truth stores.

## 8. Minimize projections

Give a consumer the least context sufficient for its purpose, role, and authority. Projection boundaries are privacy and correctness boundaries.

## 9. Require confirmation in proportion to impact

Reading evidence, suggesting a low-risk adjustment, scheduling a plan, and changing canonical state are different authorities. Higher impact and ambiguity require stronger review.

## 10. Keep interfaces replaceable

Dashboards, chat, Telegram, spreadsheets, and sensing tools are surfaces. The interface is disposable; the model persists.

## 11. Learn through explicit loops

Record hypotheses and predictions, interventions, outcomes, and updates. Do not infer generalized learning merely because the system stores behavior or produces personalized prose.

## 12. Treat friction as evidence

Repeated corrections, workarounds, ignored prompts, and duplicated entry can signal system mismatch. Investigate with the person. Do not label desire paths as user failure or automatic intent.

## 13. Design for independent use

The Human Model must remain usable without [Bridget](https://github.com/haleyparks329/bridget-architecture), Coach, or [WDW](https://github.com/Wonderful-Digital-World/wonderful-digital-world). Integration should add bounded capability, not transfer ownership.

## 14. State evidence precisely

Implemented, dogfooded, experimental, historical, planned, and rejected are not interchangeable. Public claims should identify which applies.

## 15. Publish architecture without publishing the person

Synthetic examples can demonstrate lineage, review, and uncertainty. Private data, schemas, prompts, calibration, operational thresholds, and private cross-system contracts are not required for public credibility.
