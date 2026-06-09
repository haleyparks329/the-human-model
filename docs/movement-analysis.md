# Movement Analysis

Movement analysis is the part of The Human Model focused on how physical performance is expressed through motion quality, consistency, fatigue, and control.

## Early Concepts

Potential metrics:

- Range of motion
- Tempo consistency
- Rep timing
- Stability variance
- Fatigue drift
- Left/right asymmetry
- Execution quality

## Why It Matters

Training data often captures what was performed: load, reps, sets, and perceived difficulty.

Movement analysis asks a different question: how was it performed?

That distinction matters for:

- Injury prevention
- Rehab-style feedback
- Exercise technique
- Performance consistency
- Human-machine interaction

## Future Workflow

```text
capture movement
-> extract signal
-> identify movement features
-> compare across reps or sessions
-> provide feedback
```

The first practical prototype will likely use a simple IMU-based joint angle tracker before expanding into richer sensing or computer vision.

## Relationship to Current Work

Movement analysis is not implemented yet. The current recovery and training-log work is building the context layer that movement data will eventually connect to:

- Recovery state before the session
- Training plan and exercise selection
- Logged sets, reps, load, and notes
- Future movement-quality features such as ROM, tempo, and fatigue drift

The first movement prototype should answer one narrow question well, such as whether range of motion or tempo changes across a set.
