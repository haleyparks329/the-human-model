# Recovery Modeling

**Status: current modeling discipline; public scoring examples are synthetic demonstrations.**

Recovery was the first modeling domain because training decisions are sensitive to sleep, soreness, stress, recent workload, and data freshness. It provided a concrete way to test longitudinal evidence without pretending that one score represents the whole person.

## Modeling boundary

Recovery inputs are observations with source, time, and quality. A readiness value is an interpretation produced for a purpose. It should not erase the underlying evidence or become an unquestioned canonical fact.

A responsible loop is:

```text
source evidence
-> normalized observations
-> transparent interpretation
-> review or proposal
-> explicit correction or accepted change
-> later evaluation
```

## Current discipline

- Preserve missingness instead of converting it to a neutral value.
- Keep personal baselines separate from population assumptions.
- Show limiting factors and freshness with derived output.
- Compare recommendations with later outcomes where possible.
- Route canonical changes through the Human Model rather than allowing a model or interface to write silently.

## Limits

The public repository does not publish a readiness algorithm or a production-like recovery slice. Its toy evidence-review example demonstrates only provenance and explicit lack of support with synthetic data. Historical dashboard and chat screenshots show interface lineage, not current runtime behavior or clinical validity.

Future work should test whether a recovery interpretation changes a decision usefully, whether its uncertainty is calibrated, and whether it remains valid as routines change.
