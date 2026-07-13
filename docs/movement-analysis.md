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

## Current Prototype

A first local computer-vision prototype now exists for one narrow movement-analysis use case: Romanian deadlift review. The private implementation uses MediaPipe-derived pose landmarks to create rep-level metrics, annotated playback, angle trends, and explainable dashboard flags. This public repository represents that work through an approved demo video and a mock movement-quality review example.

The prototype now also includes multi-angle batch handling for RDL review. Each video remains its own view-specific observation, with camera view and side inferred from filenames or a small metadata file. Side-view and unknown-view clips can use the current hinge metrics; front, rear, and oblique clips are retained as review evidence but are not forced through side-view formulas. The multi-angle behavior is documented here but does not yet have a separate public artifact.

This is useful implementation progress, but it is not a generalized movement coach. The current value is narrower and more honest: turn exercise video into reviewable evidence about range of motion, tempo, tracking quality, camera context, and consistency.

Demo asset: [MediaPipe RDL form demo](../demo/mediapipe-rdl-form/) shows the early overlay and movement-chart view from the first prototype steps.

## Workflow

```text
exercise video
-> pose landmarks and angle traces
-> rep-level metrics
-> annotated playback and dashboard flags
-> review alongside recovery and training context
```

For multi-angle sessions, the batch layer adds a provenance step before interpretation:

```text
camera-specific video files
-> metadata template and filename-based view inference
-> one summary row per video/view
-> later comparison without averaging incompatible camera angles
```

The longer-term sensing path may still include a simple IMU-based joint angle tracker, VBT-style output tests, or other sensors. The current landed prototype starts with computer vision because it can reuse normal training video without requiring new hardware.

Recent VBT research adds an intermediate option: a controlled output test that asks whether today's physical output is above, near, or below the personal baseline. That could be a bar-speed test, jump test, or simple movable-pod protocol before the system attempts broad exercise-quality coverage.

## Relationship to Current Work

Movement analysis is now connected to the same product direction as readiness and training review:

- Recovery state before the session
- Training plan and exercise selection
- Logged sets, reps, load, and notes
- Readiness state and data freshness from Coach Dashboard V1
- Movement-quality features such as ROM, tempo, tracking confidence, and fatigue drift
- Camera-view provenance so front/rear/oblique evidence is stored without being treated as side-view hinge data

The next useful step is not a broader claim. It is to test whether this narrow movement signal helps explain real training decisions better than load/reps alone.
