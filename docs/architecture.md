# Architecture

The Human Model is organized as a layered system.

```mermaid
flowchart TD
    A[Inputs] --> B[Capture Layer]
    B --> C[Structured Data Layer]
    C --> D[Analysis and Review Layer]
    D --> E[Feedback Layer]
    E --> F[Behavior and Training Adjustments]
    F --> A

    A1[Manual check-ins] --> A
    A2[Training logs] --> A
    A3[Apple Watch metrics] --> A
    A6[Apple Watch workouts / active energy] --> A
    A4[Zenfit screenshots] --> A
    A7[Training videos / media uploads] --> A
    A5[Future IMU / sensor data] --> A

    B1[Telegram chatbot] --> B
    B2[Apple Health import] --> B
    B3[Zenfit OCR import] --> B
    C1[SQLite dashboard store] --> C
    C2[Notion databases] --> C
    C3[Postgres canonical data foundation] --> C
    C4[Schema docs and contracts] --> C
    D1[Weekly review] --> D
    D2[Coach Dashboard V1] --> D
    D3[Baseline readiness modeling] --> D
    D5[Movement-quality review] --> D
    D4[Future notebooks] --> D
```

## Repository Roles

### `human-model`

The foundation repo defines the source-of-truth project structure.

It is responsible for:

- Tracking schemas
- Data contracts
- Weekly review workflows
- Experiment design
- Research notes
- Future notebooks, dashboards, and hardware notes

The private foundation repo now also contains the first local Coach Dashboard V1 app and a standalone readiness-modeling layer, represented publicly here through screenshots, documentation, and sanitized examples. For the dashboard, SQLite is the canonical local store and Notion is treated as a mirror, review, and selected manual-input layer. The modeling layer builds daily features, scores a transparent baseline model, and writes reviewable outputs before any LLM explanation layer touches the result.

The private foundation repo also contains the training-load modeling pipeline. It normalizes historical load conventions, evaluates set-role-aware predictions, and writes guarded next-session recommendation files that downstream tools can inspect or attach. This public repo includes a sanitized workout-sheet shaping example, not the full private model pipeline.

The private foundation repo also now holds a narrow movement-quality prototype. The current implementation is local, exercise-specific, and review-oriented: it extracts pose-derived RDL metrics, annotates video, and exposes dashboard flags without turning those flags into automated coaching claims. This public repo includes experimental visual evidence and mock movement-quality summaries.

Recent architecture work also defines a shared media-intake boundary for future desktop drops, Apple Shortcuts, Bridget uploads, and manual imports. That boundary is design-only today: it describes the canonical request shape, manifest/review records, dedupe strategy, metadata inference, and provider seams before live file movement or model routing is enabled.

The private foundation repo now also has a canonical Postgres data foundation for source-of-truth records that previously lived across separate Notion databases. The current implementation uses focused loader scripts and validation checks for body measurement sessions, daily nutrition, weekly coach check-ins, training logs, and training plans. This is data-foundation work rather than a public product surface: private rows and database IDs stay out of this repo, while the public examples show the normalization and source-health behavior with mock data.

### `human-model-chatbot`

The chatbot repo is the capture and automation layer.

It is responsible for:

- Accepting natural-language Telegram inputs
- Calling a local LLM through Ollama
- Parsing structured recovery and workout logs
- Writing recovery entries to Notion
- Importing Apple Health exports into daily recovery rows
- OCR/importing Zenfit screenshots into structured Notion databases
- Running local scheduled jobs through macOS `launchd`
- Supporting Telegram workout logging, copy-forward templates, flexible load parsing, workout notes, and Bridget daily cards
- Supporting Bridget readiness context and daily-card behavior
- Reading training-load prediction output and sending editable workout sheets while keeping model/debug files separate from training notes

### `the-human-model`

This repository is the official public home for The Human Model. It acts as the public narrative and demonstration layer: it explains the system, implementation progress, roadmap, and product/research reasoning without exposing private health data or Notion database contents.

## Current Technical Stack

- Python
- Telegram bot API
- Ollama running a local model
- Notion as the early database and review layer
- SQLite as the local canonical store for Coach Dashboard V1
- PostgreSQL as the private canonical data foundation for migrated source-of-truth records
- FastAPI backend for the local dashboard
- Next.js frontend for the local dashboard UI
- Transparent readiness-modeling scripts for feature generation, baseline scoring, and report output
- Training-load modeling scripts for normalized load history, set-role-aware evaluation, and guarded next-session recommendations
- Local MediaPipe movement-analysis scripts and dashboard review endpoints
- Design-only media-ingestion contracts for future local media review and routing
- Health Auto Export for Apple Health JSON exports
- Apple Vision/OCR flow through the Zenfit importer
- macOS `launchd` for local scheduled automation
- GitHub issues and repos for implementation planning
- Future analytics stack: pandas, NumPy, matplotlib, Plotly, scikit-learn, Jupyter, Streamlit
- Future sensing stack: Arduino, IMU sensors, force sensors, possible EMG experiments

## First Working Loops

### Recovery Loop

```text
Apple Watch metrics + Telegram check-in
-> daily Recovery Tracking V1 row
-> weekly review
-> next training / recovery adjustment
```

### Training Context Loop

```text
Zenfit screenshots or Telegram workout log
-> OCR / parser / structured workout fields
-> Notion training log
-> future comparison against recovery and performance trends
```

### Local Dashboard Loop

```text
Notion / Telegram / Health exports / app entry
-> SQLite dashboard store
-> readiness result, structured sessions, data-health context, and progression signals
-> coach-style daily review
-> future weekly analysis
```

### Baseline Modeling Loop

```text
SQLite dashboard rows
-> daily recovery/training features
-> transparent baseline readiness score and data-quality notes
-> report and local model dashboard
-> later calibration against actual training outcomes
```

### Bridget Daily Surface

```text
Health sync + readiness context + Bridget state
-> daily card schema
-> chat-friendly image and short prompt
-> one small reply or correction
-> updated context for later review
```

### Training Prediction Loop

```text
historical workout rows
-> normalized load and set-role features
-> guarded next-session recommendation file
-> Bridget pre-gym summary and editable workout sheet
-> actual weights, reps, and notes for later model review
```

### Readiness vs Actual Review

```text
Baseline readiness call + Apple Watch movement output
-> alignment label
-> recent 14-day review table
-> calibration questions for later model improvement
```

### Movement-Quality Review

```text
RDL training video
-> pose landmarks and rep metrics
-> annotated playback, angle trends, and explainable flags
-> dashboard review alongside readiness and training context
```

### Media Intake Boundary

```text
desktop drop / shortcut / Bridget upload / manual import
-> canonical intake request
-> dedupe, metadata inference, manifest, and review queue
-> later routing to movement-quality or body-progress analysis
```

### Canonical Source Data Loop

```text
Notion source databases
-> focused loader scripts
-> Postgres tables, constraints, and validation checks
-> dashboard/modeling-ready source records
-> review of missing values, duplicates, and coverage gaps
```

See [Coach Dashboard V1](coach-dashboard-v1.md) for the current local UI screenshots.

These loops give the project a working data spine before advanced modeling or hardware.
