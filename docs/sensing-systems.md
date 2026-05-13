# Sensing Systems

The sensing layer is the bridge between software and physical movement.

The near-term hardware direction is intentionally simple: one clean sensor-to-data-to-insight project before attempting a larger robotics or rehab system.

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

