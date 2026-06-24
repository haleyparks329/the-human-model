# Recovery Modeling

Recovery modeling is the first active system because it creates the simplest useful feedback loop.

## Goal

Build a lightweight system that turns wearable metrics and daily recovery check-ins into structured data that can be reviewed over time.

Example input:

```text
Slept 6 hours, energy 4, stress 7, mood okay.
```

Current structured fields:

- Sleep duration
- HRV
- Resting heart rate
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

## Current Implementation

The current recovery loop combines:

- Apple Watch data exported through Health Auto Export
- A local Apple Health importer
- A scheduled Telegram morning prompt
- Manual energy, stress, mood, and context replies
- Notion as the early recovery database
- A weekly review template for interpretation

The morning prompt intentionally avoids stale sleep data. If Apple sleep data is missing, it says that directly; if sleep is suspiciously low, it asks for manual correction.

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

## Current Modeling Discipline

The project now has a transparent V0 readiness baseline, but it is not presented as a validated predictive model. The current discipline is to keep the score auditable, expose missing inputs, and calibrate it against actual training outcomes before making stronger recommendations.
