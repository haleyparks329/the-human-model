# Toy Evidence Review

This deliberately incomplete example demonstrates one public idea: a claim should remain attached to evidence, provenance, and uncertainty.

```bash
python3 examples/toy_evidence_review.py
python3 -m unittest examples/tests/test_toy_evidence_review.py
```

The fictional input contains three claims:

- one supported by two observations;
- one supported by a single observation and therefore partial;
- one with no supporting observation.

The example has no domain scoring, weights, thresholds, calibration, prompt, persistence, routing, recommendation, or production schema. The three labels are explanatory output for this toy fixture, not a reusable decision policy.
