# Recovery Modeling

Recovery modeling is the first active sprint because it creates the simplest useful feedback loop.

## Goal

Build a lightweight system that turns daily recovery check-ins into structured data that can be reviewed over time.

Example input:

```text
Slept 6 hours, energy 4, stress 7, mood okay.
```

Expected structured fields:

- Sleep duration
- Energy
- Stress
- Mood
- Notes
- Date

## Why Recovery Comes First

The larger Human Model idea depends on having enough structured data to reason from. Recovery tracking is a good first target because it is:

- Easy to log daily
- Directly connected to training performance
- Useful even with a small dataset
- A natural fit for natural-language chatbot input

## Future Model Inputs

Potential recovery and readiness inputs include:

- Sleep duration and quality
- HRV
- Resting heart rate
- Energy
- Stress
- Mood
- Soreness
- Training load
- Adherence
- Subjective readiness

## Future Outputs

Potential outputs include:

- Weekly recovery summaries
- Training-readiness trends
- Fatigue flags
- Pattern recognition between sleep, stress, and performance
- Suggested adjustments for training intensity, volume, or recovery behaviors

