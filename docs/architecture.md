# Architecture

The Human Model is organized as a layered system.

```mermaid
flowchart TD
    A[Inputs] --> B[Capture Layer]
    B --> C[Structured Data Layer]
    C --> D[Analysis Layer]
    D --> E[Feedback Layer]
    E --> F[Behavior and Training Adjustments]
    F --> A

    A1[Manual check-ins] --> A
    A2[Training logs] --> A
    A3[Wearable metrics] --> A
    A4[Future IMU / sensor data] --> A

    B1[Telegram chatbot] --> B
    B2[Notion databases] --> C
    B3[Python scripts and notebooks] --> D
```

## Repository Roles

### `human-model`

The foundation repo defines the project structure and source-of-truth documentation.

It is responsible for:

- Tracking schemas
- Data contracts
- Weekly review workflows
- Experiment design
- Research notes
- Future notebooks, dashboards, and hardware notes

### `human-model-chatbot`

The chatbot repo is the interface and automation layer.

It is responsible for:

- Accepting natural-language inputs
- Calling a local LLM through Ollama
- Returning useful coaching-style responses
- Parsing structured check-ins
- Sending future entries to Notion or another data store

## Current Technical Stack

- Python
- Telegram bot API
- Ollama running a local model
- Notion as the early knowledge and database layer
- GitHub issues for sprint planning
- Future analytics stack: pandas, NumPy, matplotlib, Plotly, scikit-learn, Jupyter, Streamlit
- Future sensing stack: Arduino, IMU sensors, force sensors, possible EMG experiments

## First Closed Loop

The first meaningful system loop is Recovery Tracking V1:

```text
natural-language check-in
-> parsed recovery fields
-> Notion recovery entry
-> weekly review
-> next training / recovery adjustment
```

This gives the project a working data spine before adding more advanced modeling or hardware.

