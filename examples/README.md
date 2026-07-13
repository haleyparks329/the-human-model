# Public Code Examples

These examples are sanitized slices of the private Human Model implementation.
They use mock data and omit private Notion database IDs, health records, secrets,
local file paths, and automation credentials.

The goal is to show the shape of the system without publishing the whole working
prototype:

- `readiness_scoring_demo.py` shows a small recovery/readiness scoring loop.
- `readiness_modeling_demo.py` shows a transparent baseline model with
  personal baselines, data quality, limiting factors, and a report summary.
- `bridget_prompt_demo.py` shows rhythm-aware prompt decisions and quick replies.
- `daily_card_demo.py` renders a simple SVG daily card from mock readiness data.
- `dashboard_data_shaping_demo.py` shows dashboard aggregation for body trends,
  training-session summaries, weekly volume, parse warnings, progression
  signals, and import health.
- `movement_quality_demo.py` shows how rep-level movement metrics can become
  explainable dashboard flags without publishing video or pose data.
- `training_prediction_sheet_demo.py` shows how guarded model output becomes an
  editable Bridget workout sheet while preserving order, reps, and qualitative
  loads.
- `media_ingestion_router_demo.py` shows how future media uploads can be
  normalized into reviewable manifests without touching private files.

## Evidence Table

| Example | Capability | Output | Evidence level |
|---|---|---|---|
| [`readiness_scoring_demo.py`](readiness_scoring_demo.py) | Small recovery/readiness scoring loop | Console `ReadinessResult` | Public runnable algorithm |
| [`readiness_modeling_demo.py`](readiness_modeling_demo.py) | Transparent baseline readiness modeling | [Sample readiness report](sample-output/readiness-modeling-report.md) | Public runnable algorithm |
| [`bridget_prompt_demo.py`](bridget_prompt_demo.py) | Bridget prompt timing, missing-data wording, and quick replies | Console prompt and quick-reply update | Public runnable slice representing private Bridget behavior |
| [`daily_card_demo.py`](daily_card_demo.py) | Bridget daily-card visual format | [Sample daily-card SVG](sample-output/bridget-daily-card.svg) | Public runnable visual from mock data |
| [`dashboard_data_shaping_demo.py`](dashboard_data_shaping_demo.py) | Dashboard aggregation for trends, training, signals, and review hints | [Sample dashboard summary](sample-output/dashboard-data-shaping-summary.json) | Public runnable shaping slice |
| [`movement_quality_demo.py`](movement_quality_demo.py) | Mock rep-level movement-quality review | [Sample movement summary](sample-output/movement-quality-review-summary.json) | Public runnable experimental slice |
| [`training_prediction_sheet_demo.py`](training_prediction_sheet_demo.py) | Editable workout sheet shaping from guarded recommendations | [Sample workout sheet](sample-output/training-workout-sheet.csv) | Public runnable shaping slice representing private model output |
| [`media_ingestion_router_demo.py`](media_ingestion_router_demo.py) | Mock media-intake routing and dedupe boundary | Console manifest rows | Architecture/design demo |

## Setup

Clone the repository and run commands from the repository root.

The public examples use only the Python standard library. There is no install
step and no package environment is required.

The examples were verified with Python 3.9.6. Check your local version:

```bash
python3 --version
```

## Run Examples

Run all examples:

```bash
python3 examples/readiness_scoring_demo.py
python3 examples/readiness_modeling_demo.py
python3 examples/bridget_prompt_demo.py
python3 examples/daily_card_demo.py
python3 examples/dashboard_data_shaping_demo.py
python3 examples/movement_quality_demo.py
python3 examples/training_prediction_sheet_demo.py
python3 examples/media_ingestion_router_demo.py
```

`examples/daily_card_demo.py` regenerates the canonical committed output
`examples/daily_card_demo.svg` from mock data. Future scratch outputs should go
under `examples/output/`; generated files there are ignored by Git.

Curated mock outputs live in [`examples/sample-output/`](sample-output/README.md).

Run tests:

```bash
python3 -m unittest discover -s examples/tests
```

GitHub Actions runs these public examples, tests, local Markdown link checks,
and curated sample-output validation on pushes and pull requests to `main`.

Clean generated scratch output:

```bash
rm -rf examples/output/*
```

These files are intentionally small. They are portfolio examples, not the live
private automation system.
