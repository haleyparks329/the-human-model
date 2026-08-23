# Public Evidence Map

This map limits what the repository claims and points to the public evidence a reader can inspect. Private systems were consulted to reconcile boundaries, not copied here.

| Public claim | Status | Public evidence | Important limit |
| --- | --- | --- | --- |
| The project addresses longitudinal, provenance-aware, reviewable human state | Current research definition | [README](../README.md), [architecture](architecture.md) | A definition is not proof of generality. |
| Source observations can retain provenance through review | Implemented public example | [toy example](../examples/README.md) and tests | Synthetic explanatory labels, not production parity. |
| Missing or unsupported claims can remain explicit | Implemented public example | [toy fixture](../examples/toy_observations.json) and tests | Covers only a narrow evidence-review case. |
| Corrections should be retained rather than overwrite history | Architectural invariant | [architecture](architecture.md), [design principles](design-principles.md) | No public end-to-end correction implementation is claimed. |
| The Human Model owns canonical human-domain state | Current architecture | [architecture](architecture.md) | Detailed private contract intentionally omitted. |
| Coach interprets bounded evidence and proposes actions | Current architecture | [architecture](architecture.md) | No canonical write or private-runtime maturity claim. |
| [Bridget](https://github.com/haleyparks329/bridget-architecture) supports continuity and reconciliation without being a gateway | Current architecture | [architecture](architecture.md), [project evolution](project-evolution.md) | No claim that every continuity problem is solved. |
| Accepted plan and schedule state belongs to the Human Model | Current architecture | [architecture](architecture.md), [roadmap](roadmap.md) | Public runtime proof is absent; private contracts are not inferred. |
| Dashboards and chat are replaceable interfaces | Historical evidence | [asset manifest](../assets/asset-manifest.md) | Screenshots do not show current runtime. |
| Movement-video analysis is promising | Experimental | [demo note](../demo/mediapipe-rdl-form/README.md) | No validation or assessment claim. |
| The system learns preferences, intent, or behavior generally | Not claimed | [research notes](research-notes.md) | Observations and corrections do not establish generalized learning. |
| The system is medically valid or broadly generalizable | Not claimed | — | Current evidence is mainly a personal performance workflow. |

## Evidence hierarchy used in reconciliation

For current implementation claims, running code, tests, migrations, current contracts, and operational evidence outrank older narrative documents and screenshots. Historical artifacts remain useful for lineage but cannot establish present ownership or capability.

## Claim discipline

Every public capability should use one of: **implemented**, **dogfooded**, **experimental**, **historical**, **planned**, or **rejected**. If no evidence supports one of those labels, the claim should be narrowed or removed.
