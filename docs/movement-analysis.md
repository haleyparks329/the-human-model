# Movement Analysis

**Status: experimental and historical prototype.**

Movement analysis asks how a training movement was performed, not only what load and repetitions were logged. Candidate signals include range of motion, tempo consistency, stability, asymmetry, tracking quality, and fatigue drift.

## Prototype lineage

An early Romanian-deadlift experiment used pose landmarks to produce angle traces, rep-level summaries, and an annotated review. It established a useful evidence pattern: retain camera context, tracking quality, and raw review material rather than presenting a derived flag as ground truth.

[The demo recording](../demo/mediapipe-rdl-form/) preserves that experiment. It is not a validated movement assessment, generalized coach, injury-prevention tool, or current production interface.

## Research questions

- Does a narrow movement signal explain a real training decision better than load, repetitions, and notes alone?
- Which camera views support which measurements?
- How should low tracking confidence suppress or qualify an interpretation?
- Can a user review and correct segmentation or rep detection?
- What evaluation set would justify moving a signal beyond experimental status?

Computer vision, IMUs, force sensing, and output tests remain candidate evidence sources. Any future integration must preserve provenance, uncertainty, consent, and reviewability.
