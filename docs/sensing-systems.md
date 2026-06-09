# Sensing Systems

The sensing layer is the bridge between software and physical movement.

The near-term hardware direction is intentionally simple: one clean sensor-to-data-to-insight project before attempting a larger robotics, rehab, or assistive-technology system.

## Current Hardware Context

The current setup combines consumer wearable data with a local development environment:

- Mac mini for local development, chatbot operation, data scripts, and future always-on workflows
- Apple Watch as the first wearable data source for recovery and activity signals
- Health Auto Export for moving Apple Watch metrics into local JSON files
- Planned Arduino / IMU setup for direct movement-quality sensing

## Candidate Prototypes

### Joint Angle Tracker

Use an IMU sensor, such as an MPU6050, to estimate joint angle during a movement.

What it explores:

- Acceleration and gyroscope data
- Noise and filtering
- Calibration
- Range of motion estimates
- Rep consistency

### Force / Pressure Measurement

Use a force sensor or load cell to measure pressure, grip, or weight distribution.

What it explores:

- Analog signal reading
- Calibration
- Mapping voltage to physical meaning
- Strength or pressure trends

### Simple EMG Experiment

Use a muscle sensor to explore muscle activation signals.

What it explores:

- Biosignals
- Noisy data handling
- Threshold detection
- Human-machine control concepts

### Closed-Loop Feedback

Use a sensor and feedback output, such as vibration, sound, or a motor, to guide behavior.

What it explores:

- Feedback loops
- Control systems
- System response
- Human-in-the-loop design

## Recommended First Build

The strongest first hardware milestone is:

```text
IMU joint angle tracker
-> Python data logging
-> basic visualization
-> simple feedback cue
```

That keeps the project coherent and directly connected to recovery, movement quality, and adaptive feedback.

## Product Direction

The longer-term sensing idea is a modular pod rather than a fixed wearable form factor: one sensor package that can move to the body location relevant to the question.

Examples:

- Sleep: ring-like or wrist attachment
- Squats: thigh strap
- Deadlifts: lower-back clip
- Running: shoe attachment

The key principle is adaptive sensor placement: measure from the location that best answers the performance question.
