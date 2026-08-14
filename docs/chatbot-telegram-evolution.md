# Telegram and [Bridget](https://github.com/haleyparks329/bridget-architecture): Historical Interface Lineage

**Status: historical.** This page records how conversational prototypes influenced the project. Telegram is not the canonical Human Model, and Bridget is not a mandatory gateway to it.

## Evolution of the prototype

1. **Free-form recovery coaching** tested whether conversation could lower the friction of reflecting on training and recovery.
2. **Personal context notes** showed that useful advice depends on longitudinal context rather than a single message.
3. **Structured recovery logging** explored turning conversational input into reviewable fields.
4. **Morning check-ins** tested concise prompts and missing-data language.
5. **Training capture and workout summaries** explored parsing unstructured reports into candidate records.
6. **Flexible plan logging** exposed a crucial distinction: plan order does not establish a real calendar schedule.
7. **Calibration and daily cards** explored preferences, concise summaries, and quick corrections.

The screenshots in this repository document those stages. They are retained as historical evidence of interface learning, not current product screenshots or proof of a production contract.

## What survived architecturally

- Conversation can be a low-friction observation and clarification surface.
- Structured state needs provenance and review after conversational extraction.
- A summary should disclose missing or stale evidence.
- Correction must be easier than silently preserving a bad inference.

## What changed

The Human Model now stands on its own as the owner of canonical human-domain state. Bridget owns continuity, reconciliation, attention, and coordination. She may surface projections or help route a proposed change, but she does not replace the Human Model, silently write accepted state, or own specialist judgment produced by Coach.

See [Architecture](architecture.md) for the current boundary and [Asset Manifest](../assets/asset-manifest.md) for the screenshots' classification.
