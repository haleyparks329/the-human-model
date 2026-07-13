# Human Model Readiness Slice

This is a small public reference implementation for one Human Model workflow:

```text
mock Apple Health recovery export
-> validation and normalization
-> SQLite persistence
-> transparent readiness model
-> FastAPI endpoints
-> daily review JSON
-> tests
```

It is not a new product. It is a runnable engineering slice showing the shape of
the private Human Model system without publishing private health records,
Notion databases, Telegram state, local paths, or credentials.

## What It Demonstrates

- Health Auto Export-style JSON parsing from synthetic fixtures
- Timestamp normalization
- Validation and quality flags for missing signals
- Idempotent SQLite persistence
- Import-run records
- Deterministic readiness scoring
- FastAPI endpoints with typed response models
- A daily review JSON payload suitable for a review surface
- API and unit tests using temporary databases

## What It Omits

This slice intentionally excludes Telegram, Notion, training-load predictions,
workout sheets, MediaPipe, Next.js, authentication, deployment configuration,
schedulers, Docker, and generalized ingestion frameworks.

## Mapping To The Private System

The code is adapted from the private Human Model dashboard and chatbot recovery
paths:

- `human-model/apps/coach-dashboard/backend/app/apple_health.py`
- `human-model/apps/coach-dashboard/backend/app/readiness.py`
- `human-model/apps/coach-dashboard/backend/app/db.py`
- `human-model/apps/coach-dashboard/backend/app/repository.py`
- `human-model-chatbot/app/pipelines/apple_health/importer.py`

Private adapters were replaced with public-safe mock fixtures and local SQLite.

## Install

```bash
cd reference-implementation/readiness-slice
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Run The Demo

```bash
python -m readiness_slice.demo
```

The demo creates `.local/readiness_slice.sqlite3`, imports the synthetic mock
fixtures, computes readiness for the latest date, and prints the daily review
JSON.

## Run The API

```bash
uvicorn readiness_slice.api:app --reload --port 8010
```

Available endpoints:

- `GET /health`
- `POST /imports/mock-health`
- `GET /imports`
- `GET /recovery`
- `GET /recovery/{date}`
- `POST /readiness/{date}`
- `GET /readiness/{date}`
- `GET /daily-review/{date}`

## Run Tests

```bash
pytest
```

Tests use temporary SQLite databases and do not write real health data.

## Data

All fixture values in `data/fixtures/` are synthetic. Device names, private
Health Auto Export files, Notion IDs, and local user paths are intentionally not
included.

## Known Limitations

- The readiness model is a transparent baseline, not a validated medical or
training prescription model.
- The slice uses mock Apple Health-style fixtures only.
- Manual subjective check-ins and training context are excluded in this first
public slice to keep the boundary narrow.
