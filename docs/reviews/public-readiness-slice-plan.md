# Public Readiness Slice Extraction Plan

Review date: 2026-07-13

Scope:

```text
mock Apple Health recovery export
-> validation and normalization
-> SQLite persistence
-> transparent readiness model
-> FastAPI endpoints
-> daily review JSON
-> tests
```

This plan narrows the reference implementation from the broader portfolio audit to one first vertical slice. It intentionally excludes Telegram, Notion, training-load predictions, workout sheets, MediaPipe, Next.js, auth, deployment, and generalized pipeline abstractions.

## Recommendation

Build a small public readiness reference implementation inside `haleyparks329/the-human-model` as a self-contained folder. It should reuse the shape of the real private system, but publish only mock data and public-safe adapters.

The slice is small enough to complete without becoming a separate product. It has one input, one persistence layer, one transparent model, one API surface, and one daily review output. That is enough to show engineering depth without pulling in the rest of the Human Model system.

## Existing Code To Reuse

### `haleyparks329/human-model`

Source files:

- `apps/coach-dashboard/backend/app/apple_health.py`
- `apps/coach-dashboard/backend/app/readiness.py`
- `apps/coach-dashboard/backend/app/repository.py`
- `apps/coach-dashboard/backend/app/db.py`
- `apps/coach-dashboard/backend/app/schemas.py`
- `apps/coach-dashboard/backend/app/main.py`
- `apps/coach-dashboard/backend/migrations/001_initial.sql`
- `apps/coach-dashboard/backend/migrations/005_apple_watch_workouts.sql`
- `apps/coach-dashboard/backend/migrations/006_apple_watch_daily_energy.sql`
- `apps/coach-dashboard/backend/tests/test_apple_health_import.py`
- `apps/coach-dashboard/backend/tests/test_readiness.py`

Functions/classes to reuse or adapt:

| Source | Function or class | Use in public slice | Copy or adapt |
|---|---|---|---|
| `apple_health.py` | `DailyHealth` | Normalized daily recovery record from mock export | Copy with minor rename/field cleanup |
| `apple_health.py` | `WatchWorkout` | Optional movement-output context; include only if fixture keeps it small | Adapt or defer |
| `apple_health.py` | `DailyActiveEnergy` | Daily movement-output fallback for review JSON | Adapt if included |
| `apple_health.py` | `parse_health_datetime` | Parse Health Auto Export timestamps | Copy |
| `apple_health.py` | `local_date` | Normalize timestamps into configured timezone | Adapt to accept timezone parameter or settings |
| `apple_health.py` | `load_metrics` | Read mock JSON safely | Adapt: remove temp-copy/iCloud retry complexity unless fixture loader needs malformed JSON behavior |
| `apple_health.py` | `_first_present`, `_float_or_none`, `_minutes_from_duration`, `_energy_kcal` | Input normalization helpers | Copy selected helpers only if workout/energy fixture uses them |
| `apple_health.py` | `normalize_workout_type` | Normalize workout names when fixture includes a workout row | Copy if workout row stays in scope |
| `apple_health.py` | `aggregate_files` | Core mock Health Auto Export aggregation | Adapt: accept explicit fixture paths, return validation warnings |
| `apple_health.py` | `upsert_health_day` | SQLite upsert with source preservation | Adapt into repository layer; remove live recompute side effect or make explicit |
| `apple_health.py` | `backfill_apple_health` | Import orchestration and import-run record | Adapt heavily: rename to `import_mock_health_export`, remove private inbox discovery |
| `readiness.py` | `RecoveryDay` | Domain input for readiness model | Copy |
| `readiness.py` | `TrainingContext` | Drop from first slice or freeze as default empty context | Do not expose publicly unless needed |
| `readiness.py` | `ReadinessResult` | Domain output | Copy and consider structured `factors: list[str]` instead of semicolon string |
| `readiness.py` | `_avg`, `_linear`, `_hrv_score`, `_rhr_score`, `_mood_score`, `_confidence` | Transparent model helpers | Copy |
| `readiness.py` | `calculate_readiness` | Main decision logic | Adapt to remove training component or keep fixed neutral recovery-only component |
| `repository.py` | `upsert_recovery` | Public recovery upsert | Adapt to narrow fields and explicit `changed` behavior |
| `repository.py` | `list_recovery` | API list endpoint | Copy/adapt |
| `repository.py` | `recovery_history_through` | Model history fetch | Copy/adapt |
| `repository.py` | `recompute_readiness` | Readiness persistence boundary | Adapt |
| `repository.py` | `dashboard_summary` | Daily review JSON inspiration | Do not copy wholesale; adapt a tiny `daily_review` service |
| `db.py` | `connect`, `apply_migrations`, `rows_to_dicts` | SQLite boundary | Copy/adapt |
| `schemas.py` | `RecoveryDayIn` | Pydantic request model style | Adapt |
| `main.py` | `/health`, `/recovery`, `/readiness/{target_date}` endpoint shape | API shape | Adapt into smaller `api.py` |
| migrations | `recovery_days`, `readiness_results`, `import_runs`, Apple Watch tables | SQLite schema basis | Adapt and narrow |
| tests | Apple Health and readiness tests | Regression coverage template | Adapt with public fixtures |

### `haleyparks329/human-model-chatbot`

Source files:

- `app/pipelines/apple_health/importer.py`
- `app/pipelines/apple_health/pipeline.py`
- `app/pipelines/contracts.py`
- `readiness.py`
- `test_readiness.py`

Functions/classes to reuse or adapt:

| Source | Function or class | Use in public slice | Copy or adapt |
|---|---|---|---|
| `app/pipelines/apple_health/importer.py` | `parse_hae_datetime`, `local_date_of`, `DailyHealth`, `aggregate_files` | Simpler Notion-era importer shape | Use as cross-check, but prefer dashboard `apple_health.py` because it already targets SQLite |
| `app/pipelines/apple_health/pipeline.py` | `daily_health_to_evidence` | Missing-data quality flag idea | Adapt concept only; do not add evidence log in first slice |
| `app/pipelines/contracts.py` | `PipelineResult` | Import result shape | Adapt a tiny public `ImportResult`; do not import the full protocol |
| `readiness.py` | `calculate_readiness` with coach override | Historical model variant | Do not copy live Notion/update code; use tests as behavioral reference |
| `test_readiness.py` | missing manual check-in tests | Useful missing-data coverage | Adapt |

### `haleyparks329/the-human-model`

Source files:

- `examples/readiness_scoring_demo.py`
- `examples/readiness_modeling_demo.py`
- `examples/dashboard_data_shaping_demo.py`
- `examples/tests/test_public_examples.py`
- `.github/workflows/public-repo-checks.yml`

Functions/classes to reuse or adapt:

| Source | Function or class | Use in public slice | Copy or adapt |
|---|---|---|---|
| `examples/readiness_scoring_demo.py` | public-safe readiness dataclasses and helper style | Public-facing readability | Adapt naming and docstrings |
| `examples/readiness_modeling_demo.py` | `BaselineResult`, `score_day`, `report_lines`, `movement_output_summary` | Daily review JSON tone and transparent output | Adapt concepts only; avoid parallel model definitions |
| `examples/dashboard_data_shaping_demo.py` | `ImportRun`, `signal_health` | Import health summary | Adapt a narrow version |
| public CI workflow | compile/test pattern | Add tests later in implementation | Adapt after implementation |

## Copy Versus Adapt

Copy nearly unchanged:

- `parse_health_datetime`
- `DailyHealth.finalize_hrv`
- `_avg`
- `_linear`
- `_hrv_score`
- `_rhr_score`
- `_mood_score`
- `_confidence`
- `connect`
- `rows_to_dicts`

Adapt:

- `aggregate_files`: keep Health Auto Export metric parsing, but add explicit validation warnings and remove private inbox defaults.
- `load_metrics`: use normal JSON file loading for committed fixtures; keep malformed JSON as a handled error in import orchestration.
- `backfill_apple_health`: rename and narrow to `import_mock_health_export(paths: list[Path])`; return a typed import result.
- `upsert_health_day`: move into `repository.py`, return whether the row was inserted, updated, or unchanged.
- `calculate_readiness`: keep transparent scoring, but remove or neutralize training context for this first slice.
- `recompute_readiness`: keep persistence behavior, but return typed response data and not a raw SQLite row only.
- `dashboard_summary`: replace with a much smaller `daily_review_for_date`.
- `main.py`: create a new small `api.py`, not a copied dashboard app.

Do not copy:

- Notion request/query/update code.
- Telegram code.
- Scheduler/lifespan sync code.
- Training, body, weekly review, movement, and modeling-service endpoints.
- Local absolute path defaults.
- Real data files or generated private SQLite databases.

## Private Dependencies To Replace

| Private dependency | Existing location | Replacement |
|---|---|---|
| Health Auto Export iCloud inbox path | `health_inbox_path()` and chatbot `DEFAULT_INBOX` | Committed mock fixture path under `reference-implementation/data/` |
| `LOCAL_TIMEZONE` from private environment | dashboard/chatbot config | Public default `Europe/Copenhagen`, override by env var |
| Notion token/database IDs | chatbot Apple Health/readiness modules | Remove entirely |
| Notion `find_page_by_date`, `upsert_page`, `notion_headers` | chatbot importer/readiness | Remove entirely |
| Private recovery rows | private Notion/SQLite/local files | Mock fixture rows only |
| Existing dashboard SQLite file | `apps/coach-dashboard/backend/data/coach_dashboard.sqlite3` | Generated local `.sqlite3` under `reference-implementation/.local/`, gitignored |
| Training context | `training_entries` and Notion training log | Omit from first slice |
| App scheduler/sync | dashboard `scheduler.py` | No scheduler |

## Mock Fixtures Required

Create public fixtures under `reference-implementation/data/fixtures/`.

Required:

1. `health_export_recovery_complete.json`
   - Health Auto Export shape: `{"data": {"metrics": [...]}}`
   - Includes `sleep_analysis`, `heart_rate_variability`, `resting_heart_rate`, `step_count`, `weight_body_mass`.
   - Includes at least three prior days plus one target day so baselines are meaningful.

2. `health_export_missing_sleep.json`
   - Includes HRV/resting HR/steps but no sleep row for one date.
   - Demonstrates missing-data handling and lower confidence without treating missing sleep as bad recovery.

3. `health_export_malformed_metric.json`
   - Optional if implementation supports partial metric errors.
   - Better alternative: keep a malformed JSON test fixture generated in test temp dirs, not committed.

Optional but still in scope:

4. `health_export_active_energy.json`
   - Includes `active_energy` daily samples.
   - Use only if daily review JSON should show movement output context. Do not add workout-session matching.

Recommended fixture values should be obviously synthetic:

- Dates: `2026-06-16` through `2026-06-23`
- Sleep: `6.4` to `7.8`
- HRV: `72` to `85`
- Resting HR: `51` to `55`
- Steps: small rounded values like `6400`, `8200`
- Weight: optional synthetic values like `68.4`
- Source names: `Mock Apple Watch`, not personal device names.

## Proposed Public Database Schema

Use SQLite. Keep migrations small and explicit.

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
  version TEXT PRIMARY KEY,
  applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recovery_days (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL UNIQUE,
  sleep_hours REAL,
  hrv_ms REAL,
  resting_hr_bpm REAL,
  steps REAL,
  weight_kg REAL,
  source TEXT NOT NULL DEFAULT 'mock_apple_health',
  quality_flags TEXT NOT NULL DEFAULT '',
  raw_metrics TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS readiness_results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL UNIQUE,
  score INTEGER,
  status TEXT NOT NULL,
  confidence TEXT NOT NULL,
  factors TEXT NOT NULL DEFAULT '',
  data_freshness TEXT NOT NULL DEFAULT '',
  final_call TEXT NOT NULL,
  computed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (date) REFERENCES recovery_days(date) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS import_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  status TEXT NOT NULL,
  files_seen INTEGER NOT NULL DEFAULT 0,
  rows_seen INTEGER NOT NULL DEFAULT 0,
  rows_inserted INTEGER NOT NULL DEFAULT 0,
  rows_updated INTEGER NOT NULL DEFAULT 0,
  rows_unchanged INTEGER NOT NULL DEFAULT 0,
  warnings TEXT NOT NULL DEFAULT '',
  errors TEXT NOT NULL DEFAULT '',
  started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  finished_at TEXT
);
```

Do not include:

- `notion_page_id`
- `training_entries`
- `body_metrics`
- `weekly_reviews`
- `sync_events`
- `apple_watch_workouts`
- `apple_watch_daily_energy` unless active energy is included in daily review v1

If active energy is included, add only:

```sql
CREATE TABLE IF NOT EXISTS daily_movement (
  date TEXT PRIMARY KEY,
  active_energy_kcal REAL,
  sample_count INTEGER NOT NULL DEFAULT 0,
  source TEXT NOT NULL DEFAULT 'mock_apple_health',
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## Proposed Pydantic And Domain Models

Domain dataclasses:

```python
@dataclass(frozen=True)
class DailyHealth:
    date: str
    sleep_hours: float | None = None
    hrv_ms: float | None = None
    resting_hr_bpm: float | None = None
    steps: float | None = None
    weight_kg: float | None = None
    raw_metrics: tuple[str, ...] = ()
    quality_flags: tuple[str, ...] = ()

@dataclass(frozen=True)
class RecoveryDay:
    date: str
    sleep_hours: float | None = None
    hrv_ms: float | None = None
    resting_hr_bpm: float | None = None
    steps: float | None = None
    weight_kg: float | None = None
    source: str = "mock_apple_health"
    quality_flags: tuple[str, ...] = ()

@dataclass(frozen=True)
class ReadinessResult:
    date: str
    score: int | None
    status: str
    confidence: str
    factors: tuple[str, ...]
    data_freshness: tuple[str, ...]
    final_call: str

@dataclass(frozen=True)
class ImportResult:
    status: str
    files_seen: int
    rows_seen: int
    rows_inserted: int
    rows_updated: int
    rows_unchanged: int
    warnings: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
```

Pydantic models:

```python
class ImportRequest(BaseModel):
    fixture_names: list[str] | None = None

class RecoveryDayOut(BaseModel):
    date: str
    sleep_hours: float | None = None
    hrv_ms: float | None = None
    resting_hr_bpm: float | None = None
    steps: float | None = None
    weight_kg: float | None = None
    source: str
    quality_flags: list[str] = []
    raw_metrics: list[str] = []

class ReadinessOut(BaseModel):
    date: str
    score: int | None
    status: Literal["Push", "Maintain", "Modify", "Rest"]
    confidence: Literal["Low", "Medium", "High"]
    factors: list[str]
    data_freshness: list[str]
    final_call: Literal["Push", "Maintain", "Modify", "Rest"]

class DailyReviewOut(BaseModel):
    date: str
    recovery: RecoveryDayOut | None
    readiness: ReadinessOut | None
    import_health: dict
    review_summary: str
    missing_data: list[str]
    public_boundary: str
```

Validation rules:

- Dates must be ISO `YYYY-MM-DD`.
- Sleep must be between `0` and `24` if present.
- HRV, resting HR, steps, and weight must be non-negative if present.
- Mood/energy/stress are excluded in v1 because the input is Apple Health only.
- Unknown metrics are ignored but reported as warnings.
- Missing critical signals should not reject the import; they should create quality flags.

## API Endpoints

Minimal FastAPI surface:

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | App liveness |
| `POST` | `/imports/mock-health` | Import committed mock Health Auto Export fixtures into SQLite |
| `GET` | `/imports` | Show recent import runs |
| `GET` | `/recovery` | List recovery days |
| `GET` | `/recovery/{date}` | Fetch one normalized recovery day |
| `POST` | `/readiness/{date}` | Compute and persist readiness for a date |
| `GET` | `/readiness/{date}` | Fetch persisted readiness; optionally compute if missing |
| `GET` | `/daily-review/{date}` | Return one review JSON with recovery, readiness, missing data, import health, and boundary note |

Endpoint behavior:

- `POST /imports/mock-health` should default to all committed fixtures if `fixture_names` is omitted.
- Import should recompute readiness for imported dates after persistence.
- `GET /daily-review/{date}` may compute readiness if recovery exists but readiness is missing.
- Missing recovery day should return `404` with a clear message.

## Error Cases

Import errors:

- Fixture name not found.
- JSON is malformed.
- JSON exists but does not contain `data.metrics`.
- Metric row has an invalid timestamp.
- Metric row has non-numeric quantity where numeric is required.

Validation warnings:

- No sleep row for a date.
- No HRV row for a date.
- No resting HR row for a date.
- Unknown metric name ignored.
- HRV present but no sleep window, so daily mean was used.

API errors:

- `404`: recovery date not found.
- `422`: invalid request payload or invalid date format.
- `500`: unexpected internal error; tests should avoid depending on this.

Model/data-quality behavior:

- Missing sleep/HRV/resting HR lowers confidence and adds factors.
- Missing Apple Health data should never produce a fake bad recovery call.
- Thin baseline should produce a confidence/factor note.
- A low score or red flag should downgrade the status through explicit readable rules.

## Idempotency Behavior

Import idempotency:

- `recovery_days.date` is unique.
- Re-importing the same fixture should not duplicate rows.
- If normalized values are identical, count as `rows_unchanged`.
- If normalized values differ for an existing date, update the row and count as `rows_updated`.
- Insert new dates as `rows_inserted`.

Readiness idempotency:

- `readiness_results.date` is unique.
- Recomputing readiness for the same unchanged recovery history should overwrite the same row, not insert a duplicate.
- `computed_at` may change; tests should assert row count and stable score/status, not exact timestamp.

Import-run behavior:

- Every import attempt records an `import_runs` row.
- Failed imports record `status='error'` and do not partially persist rows unless parsing has completed successfully.
- Blocked/missing fixture imports should record `status='blocked'` or `error`, depending on implementation preference. Prefer `blocked` for no selected files found, `error` for malformed selected files.

## Minimum Test Suite

Use `pytest` plus FastAPI `TestClient`.

Tests:

1. `test_parse_health_datetime_accepts_health_auto_export_offset`
   - Verifies `2026-06-18 06:30:00 +0200` parsing.

2. `test_import_complete_fixture_normalizes_recovery_day`
   - Imports complete fixture.
   - Asserts sleep, HRV in sleep window, resting HR, steps, weight, source, raw metrics.

3. `test_import_missing_sleep_sets_quality_flag_not_failure`
   - Imports missing-sleep fixture.
   - Asserts row persisted with `missing_sleep` quality flag.

4. `test_import_is_idempotent`
   - Imports same fixture twice.
   - Asserts one recovery row per date and second result reports unchanged rows.

5. `test_readiness_good_baseline_returns_push_or_maintain`
   - Uses fixture history.
   - Asserts transparent score/status/confidence/factors.

6. `test_readiness_missing_data_low_confidence`
   - Uses missing-sleep date.
   - Asserts low confidence and missing-data factors.

7. `test_daily_review_json_has_public_boundary_and_missing_data`
   - Calls daily review endpoint.
   - Asserts response includes recovery, readiness, import health, `public_boundary`, and `missing_data`.

8. `test_api_import_and_fetch_flow`
   - `POST /imports/mock-health`
   - `GET /recovery/{date}`
   - `POST /readiness/{date}`
   - `GET /daily-review/{date}`

9. `test_unknown_fixture_returns_404_or_422`
   - Ensures bad fixture names are handled cleanly.

10. `test_malformed_json_records_error_without_rows`
   - Creates malformed temp fixture in test-only directory.
   - Asserts no recovery rows persisted and import run records error.

This is enough. Do not add browser tests, UI snapshots, auth tests, Telegram tests, Notion tests, training tests, or movement tests.

## One-Command Local Run Approach

Keep the local path simple.

Recommended command:

```bash
cd reference-implementation/readiness-slice
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m readiness_slice.demo
```

`python -m readiness_slice.demo` should:

1. Create/reset a local demo SQLite database under `.local/readiness_slice.sqlite3`.
2. Apply migrations.
3. Import the committed mock fixtures.
4. Compute readiness for the latest date.
5. Print the daily review JSON.

API run:

```bash
cd reference-implementation/readiness-slice
source .venv/bin/activate
uvicorn readiness_slice.api:app --reload --port 8010
```

Test run:

```bash
cd reference-implementation/readiness-slice
source .venv/bin/activate
pytest
```

Avoid Makefile or Docker for the first slice. A tiny `README.md` with these commands is enough.

## Estimated Implementation Size

Expected size:

- 9 to 12 Python source files.
- 2 SQL migration files.
- 2 to 3 JSON fixtures.
- 8 to 12 tests.
- 1 README.
- Roughly 700 to 1,100 lines of source and tests combined.

Implementation effort:

- Small-to-medium.
- Likely 1 focused implementation pass plus 1 cleanup/verification pass.
- It should not require frontend work, credentials, real data, or cross-repo runtime dependencies.

Risk controls:

- Keep all private adapters out.
- Keep the model deterministic.
- Keep the API narrow.
- Keep fixture data synthetic.
- Do not build a general ingestion framework yet.

## Proposed File Tree

```text
reference-implementation/
  readiness-slice/
    README.md
    pyproject.toml
    .gitignore
    readiness_slice/
      __init__.py
      api.py
      config.py
      db.py
      demo.py
      health_import.py
      models.py
      readiness.py
      repository.py
      review.py
      migrations/
        001_initial.sql
    data/
      fixtures/
        health_export_recovery_complete.json
        health_export_missing_sleep.json
    tests/
      conftest.py
      test_api.py
      test_health_import.py
      test_readiness.py
      test_repository.py
      test_review.py
```

Possible later CI addition:

```text
.github/workflows/public-repo-checks.yml
```

Add the readiness-slice tests to existing CI only after implementation passes locally.

## Exact Implementation Order

1. Create `reference-implementation/readiness-slice/README.md` with scope and commands.
2. Add `pyproject.toml` with `fastapi`, `uvicorn`, `pydantic`, `pytest`, and `httpx` for `TestClient`.
3. Add `config.py` with public-safe defaults:
   - `READINESS_SLICE_DB`
   - `READINESS_SLICE_TIMEZONE`
   - fixture directory path
4. Add `db.py` copied/adapted from dashboard `db.py`.
5. Add `migrations/001_initial.sql` with only recovery/readiness/import tables.
6. Add `models.py` with domain dataclasses and Pydantic models.
7. Add fixtures under `data/fixtures/`.
8. Add `health_import.py`:
   - timestamp parsing
   - JSON metric loading
   - aggregation
   - validation warnings
   - import result creation
9. Add `repository.py`:
   - recovery upsert/list/get
   - import run insert
   - readiness upsert/get
10. Add `readiness.py`:
   - copied/adapted transparent scoring
   - no training context in v1
11. Add `review.py`:
   - `daily_review_for_date`
   - missing-data summary
   - public/private boundary note
12. Add `api.py` with minimal FastAPI endpoints.
13. Add `demo.py` for one-command local demo.
14. Add tests in the order of the workflow:
   - importer
   - repository/idempotency
   - readiness
   - review
   - API
15. Run:
   - `pytest`
   - `python -m readiness_slice.demo`
   - `uvicorn readiness_slice.api:app --reload --port 8010` smoke if needed
16. Add CI workflow command only if the user asks for implementation and verification lands cleanly.

## Files That Should Not Be Copied

Do not copy these files into the public slice:

- `human-model/apps/coach-dashboard/backend/app/notion_import.py`
- `human-model/apps/coach-dashboard/backend/app/scheduler.py`
- `human-model/apps/coach-dashboard/backend/app/bridget_import.py`
- `human-model/apps/coach-dashboard/backend/app/lifting.py`
- `human-model/apps/coach-dashboard/backend/app/movement.py`
- `human-model/apps/coach-dashboard/backend/app/modeling_service.py`
- `human-model/apps/coach-dashboard/backend/app/training_output.py`
- `human-model/apps/coach-dashboard/frontend/**`
- `human-model/apps/coach-dashboard/backend/migrations/003_structured_lifting.sql`
- `human-model/apps/coach-dashboard/backend/migrations/004_bridget_training_events.sql`
- `human-model-chatbot/main.py`
- `human-model-chatbot/bridget.py`
- `human-model-chatbot/bridget_events.py`
- `human-model-chatbot/daily_card.py`
- `human-model-chatbot/notion_client.py`
- `human-model-chatbot/app/integrations/**`
- `human-model-chatbot/app/pipelines/zenfit/**`
- `human-model-chatbot/app/pipelines/workout_files/**`
- `human-model-chatbot/workout_recommendations.py`
- `human-model-chatbot/zenfit/**`
- Any `.env`, `.sqlite3`, `.jsonl`, `.bridget_*`, real Health Auto Export JSON, private screenshots, raw videos, or Notion-derived exports.

Why:

- They contain private adapters, live delivery surfaces, unrelated domains, local operational paths, or product complexity outside the first slice.
- Copying them would make the reference implementation look larger and less intentional.

## Final Recommendation

Yes, this slice is small enough to complete without becoming a separate product.

The right shape is a public reference implementation, not a new application. It should be framed as a runnable engineering slice that demonstrates the real Human Model architecture:

- input ingestion
- validation and normalization
- SQLite persistence
- typed contracts
- transparent readiness logic
- API boundary
- daily review JSON
- public/private data boundary
- tests

Stop there for v1. The strength is in the clean boundary and the reviewer being able to run it quickly, not in adding more Human Model subsystems.
