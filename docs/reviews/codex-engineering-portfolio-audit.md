# Codex Engineering Portfolio Audit

Review date: 2026-07-13

Repositories reviewed:

- `haleyparks329/the-human-model`
- `haleyparks329/human-model`
- `haleyparks329/human-model-chatbot`

Repo visibility checked with GitHub CLI:

- `the-human-model`: public
- `human-model`: private
- `human-model-chatbot`: private

Validation run during this audit:

- `python3 -m unittest discover -s examples/tests` in `the-human-model`: 21 passed
- `apps/coach-dashboard/backend/.venv/bin/python -m pytest apps/coach-dashboard/backend/tests/test_apple_health_import.py apps/coach-dashboard/backend/tests/test_bridget_import.py apps/coach-dashboard/backend/tests/test_movement.py apps/coach-dashboard/backend/tests/test_training_output.py apps/coach-dashboard/backend/tests/test_modeling_service.py` in `human-model`: 17 passed
- `.venv/bin/python -m unittest test_pipeline_boundaries.py test_workout_files.py test_workout_recommendations.py test_main.py` in `human-model-chatbot`: 98 passed

Note: both private implementation repos had existing local dirty state during review. This audit treats those files as current local evidence, but does not recommend publishing uncommitted private work without a separate sanitization pass.

## 1. Executive Verdict

This work provides strong evidence for AI Product Engineer, Applied AI Engineer, systems-oriented Product Engineer, and early-stage full-stack engineer roles where the job is not just "call an LLM," but design a reliable workflow around messy human data.

The memorable story is not a chatbot. It is a local-first human-performance data spine:

```text
Apple Health / Telegram / Zenfit / workout files / video
-> typed or structured evidence
-> SQLite, Notion, JSONL, CSV, and model artifacts
-> transparent readiness, training-load, and movement-quality reasoning
-> Bridget and Coach Dashboard review surfaces
-> correction and feedback loops
```

The project feels like a real personal system plus several prototype frontiers. It is more than a collection of scripts because there are stable contracts, tests, persistence layers, migrations, service boundaries, and repeated commits that harden behavior. It is not yet a polished public product, and the public repository alone still undersells the implementation depth because the strongest code lives in private repos.

The best public strategy is option C: assemble several existing components into one runnable public vertical slice. Do not create a new miniature implementation from scratch. The vertical slice should reuse the strongest private architecture shape while replacing private data, Notion IDs, tokens, and local paths with mock adapters.

Recommended public vertical slice:

```text
mock Apple Health recovery + mock planned workout + mock training-load predictions
-> validate and persist locally
-> build readiness and workout-sheet recommendations
-> expose a small FastAPI API
-> render a compact review output or static dashboard summary
-> include tests and one-command local run
```

This is the smallest slice that shows real engineering depth: ingestion, validation, persistence, transparent decision logic, service boundary, output, correction fields, and tests.

## 2. Hiring-Manager Assessment

### Strong Role Evidence

Strong evidence for:

- AI Product Engineer: the system turns ambiguous human behavior into product loops, not just model calls.
- Applied AI Engineer: model outputs are transparent, guarded, and coupled to real data contracts.
- Product Engineer: Bridget and Coach Dashboard show user-facing workflow thinking, low-friction capture, and correction loops.
- Systems-oriented software engineer: the work spans ingestion, persistence, migrations, tests, service APIs, local automation, and cross-repo boundaries.
- Data/ML-adjacent engineer: training-load modeling, readiness scoring, and movement analysis are reviewable and reproducible rather than black-box.

Less direct evidence for:

- Production platform engineer: there is limited deployed infra, observability, multi-user auth, or cloud operations.
- Pure ML research engineer: the models are deliberately simple and transparent rather than novel algorithms.
- Visual/frontend specialist: the dashboard is functional and useful, but visual polish is not the main signal.

### What Would Make Me Interview You

- The project is built around a real operating loop with actual constraints: missing Apple Watch data, private health records, messy workout logs, screenshots, and video artifacts.
- The implementation shows judgment about separating capture, storage, reasoning, and presentation. Examples: `app/pipelines/contracts.py`, `app/human_model/evidence.py`, `apps/coach-dashboard/backend/app/schemas.py`, SQLite migrations, and Bridget JSONL events.
- The public repo is honest about status boundaries. It labels public runnable examples, private implementation, experimental work, and future plans in `docs/evidence-map.md`.
- The training-load flow has especially good product judgment: raw model/debug output stays separate from editable workout notes, and guardrails prevent the model from inventing unsafe or incoherent progression.
- The movement-quality work shows restraint: MediaPipe RDL analysis is presented as review context, not generalized autonomous coaching.

### What Might Make Me Hesitate

- The strongest implementation is split across private repos. A reviewer who only scans the public repo sees narrative, mock examples, and screenshots before seeing real app architecture.
- The foundation repo README still says "most directories are placeholders right now," which is stale relative to the current FastAPI, SQLite, modeling, and MediaPipe work.
- There is no CI in the private implementation repos. Tests exist and pass locally, but a hiring reviewer cannot see a green public check for those deeper systems.
- The dashboard backend has many useful endpoints, but the public repo does not provide a runnable sanitized equivalent.
- Error handling is pragmatic but uneven. Some paths record parse errors and import runs well; others still rely on print output, broad exception handling, or local operational knowledge.

### Two-Minute Scan

Within two minutes, a reader can understand:

- The public thesis from `README.md`.
- The major capability map from `docs/evidence-map.md`.
- The sanitized runnable demos from `examples/README.md`.
- That the public repo has CI through `.github/workflows/public-repo-checks.yml`.
- Screenshots of Bridget and Coach Dashboard in `assets/screenshots/`.

What is buried or undersold:

- The actual FastAPI endpoints and SQLite schema in `human-model/apps/coach-dashboard/backend/`.
- The Bridget event ledger and planned-vs-actual comparison tables.
- The training-load model pipeline and its guardrail logic.
- The multi-angle RDL batch tooling and camera-view provenance.
- The fact that tests exist for real private workflows, not only public mock examples.

## 3. Engineering-Lead Assessment

### Strong

- Architecture: clear separation between public overview, foundation/dashboard/modeling repo, and Bridget chatbot repo.
- Service boundaries: `apps/coach-dashboard/backend/app/main.py` exposes explicit FastAPI routes for recovery, readiness, training, movement, sync, modeling, and imports.
- Persistence: SQLite migrations define durable tables for recovery, readiness, training, body metrics, import runs, Bridget events, Apple Watch workouts, and daily active energy.
- Domain modeling: Pydantic request models, Python dataclasses, R modeling datasets, and CSV schemas preserve domain concepts instead of flattening everything into free text.
- Testing: public examples, dashboard importer/review paths, movement routes, training-output summaries, workout file import, pipeline boundaries, and Bridget send paths all have tests.
- Model transparency: readiness scoring and training-load recommendations expose factors, confidence, guardrails, and debug output.
- Privacy boundaries: public repo uses mock data and explicitly omits credentials, Notion IDs where needed, private health records, and local automation paths.
- Product judgment: Bridget is the low-friction capture/delivery surface; dashboard is the review/audit surface.

### Acceptable For Current Stage

- Local-first deployment: macOS launchd, local SQLite, private Notion, and local files are reasonable for a single-user research system.
- Simple models: readiness and training-load baselines are appropriate because outputs are inspectable and framed cautiously.
- Mixed languages: R for training-load modeling and Python/TypeScript for app layers is acceptable because the boundary is artifact-based CSV/RDS output.
- Mock public examples: they preserve representative interfaces and behavior even though they omit private data.

### Weak

- Public navigation to implementation depth is weaker than the implementation itself.
- Private repos lack visible CI workflows.
- Some root-level compatibility shims and newer `app/` modules coexist, which is understandable but makes architecture harder to scan.
- Observability is partial: import runs, parse statuses, and signal health exist, but there is not a consistent logging/error-reporting pattern across every pipeline.
- Reproducibility is good in narrow tests but not yet packaged as one public vertical slice.

### Missing

- A single command that runs a representative public app-like workflow end to end.
- Public sanitized SQLite/FastAPI slice showing real interfaces rather than only standalone scripts.
- Architecture diagram tied directly to files and tests.
- Public evidence of private repo CI.
- A clear "start here if you are hiring me" path that takes under five minutes.

### Unclear Because Private Or Not Inspectable Publicly

- Real Notion schemas and data quality in production use.
- Real Apple Health export volume and longitudinal reliability.
- Live Telegram operational behavior and schedule reliability.
- Full Coach Dashboard UI behavior beyond screenshots.
- Full private MediaPipe artifact quality on real videos.

## 4. End-To-End Workflow Traces

### Workflow A: Apple Health / Recovery Data To Storage, Modeling, And Presentation

Entry points:

- Chatbot/private Notion path: `human-model-chatbot/app/pipelines/apple_health/pipeline.py`
- Legacy/importer path: `human-model-chatbot/app/pipelines/apple_health/importer.py`
- Dashboard SQLite path: `human-model/apps/coach-dashboard/backend/app/apple_health.py`
- Dashboard API: `human-model/apps/coach-dashboard/backend/app/main.py`

Data structures:

- `DailyHealth` dataclasses in both Apple Health importers.
- `RecoveryDayIn` in `apps/coach-dashboard/backend/app/schemas.py`.
- `recovery_days`, `readiness_results`, `apple_watch_workouts`, and `apple_watch_daily_energy` SQLite tables.
- `EvidenceRecord` emitted by the chatbot modular pipeline.

Transformations:

- Health Auto Export JSON files are discovered by date.
- Timestamps are normalized into the configured timezone.
- Sleep, HRV, resting HR, steps, weight, workout duration, active energy, and daily energy are extracted.
- HRV is averaged inside the sleep window when possible, falling back to a daily mean.
- Workout types are normalized into labels such as `strength`, `run`, `walk`, `cycling`, and `mobility`.
- Readiness recomputation combines recovery history with recent training context.

Persistence:

- Dashboard path writes to SQLite through migrations and repository functions.
- Chatbot path can upsert Notion recovery rows and emit local evidence/import-run records.
- Apple Watch workout rows use an `import_key` hash for idempotency.

Service boundaries and outputs:

- `GET /recovery`, `POST /recovery`, `POST /readiness/{target_date}`, `GET /dashboard`, and `GET /training/output-summary`.
- Dashboard summary includes today, readiness, recent recovery, recent training, body trends, import signals, and V2 payload.
- Public evidence is represented by `examples/readiness_scoring_demo.py`, `examples/readiness_modeling_demo.py`, `examples/bridget_prompt_demo.py`, screenshots, and docs.

Tests:

- `apps/coach-dashboard/backend/tests/test_apple_health_import.py`
- `apps/coach-dashboard/backend/tests/test_readiness.py`
- `apps/coach-dashboard/backend/tests/test_training_output.py`
- `examples/tests/test_public_examples.py`

Failure handling:

- Missing inbox returns no files.
- JSON/iCloud read errors are retried through temporary copies.
- Dashboard import is idempotent.
- Readiness can return low confidence when critical data is missing.
- Training-output review labels incomplete comparisons as unknown/provisional.

Fragile or unfinished:

- Public repo does not expose the full importer.
- Notion writeback depends on private integration access.
- Operational monitoring is local and partial.

### Workflow B: Training-Load Prediction Through Bridget And Editable Workout Sheets

Entry points:

- R model pipeline in `human-model/scripts/modeling/01_clean_training_log.R` through `07_analyze_prediction_errors.R`.
- Prediction generation in `human-model/scripts/modeling/06_generate_predictions.R`.
- Bridget integration in `human-model-chatbot/main.py`.
- Recommendation/sheet shaping in `human-model-chatbot/workout_recommendations.py`.
- Workout-file import in `human-model-chatbot/app/pipelines/workout_files/`.
- Dashboard planned-vs-actual import in `human-model/apps/coach-dashboard/backend/app/bridget_import.py`.

Data structures:

- `training_model_dataset.csv`, `training_log_long.csv`, `training_load_linear_model_v2.rds`.
- `next_session_predictions.csv` and dated history snapshots.
- `WorkoutRecommendation`, `ExerciseRecommendation`, `SetRecord`.
- Bridget append-only `.bridget_training_events.jsonl`.
- SQLite tables `bridget_training_events`, `bridget_recommendations`, `bridget_recommended_exercises`, `bridget_recommended_sets`, `bridget_workout_feedback`, and `bridget_training_comparisons`.

Transformations:

- Raw workout logs are cleaned and normalized.
- Exercise-specific load rules preserve `logged_weight_kg` while deriving `effective_load_kg`.
- V2 linear model predicts effective load using exercise identity, set role, set number, reps, previous load, previous reps, and days since last set.
- Predictions are converted back into logged-weight recommendations.
- Guardrails preserve warmups, prevent regressions below previous logged load, and enforce warmup <= working <= top set.
- Bridget filters recommendations to the selected workout and creates editable sheets with blank actual result columns.
- Completed sheets are parsed back into evidence records.

Persistence:

- Model/debug CSVs live under `human-model/data/predictions/`.
- Editable sheets live under `human-model/data/workout_sheets/`.
- Bridget recommendation events are append-only JSONL.
- Dashboard imports event ledger rows into normalized SQLite tables.

Service boundaries and outputs:

- Bridget sends a Telegram pre-gym summary, editable workout sheet, and separate model/debug CSV.
- Dashboard `GET /training/planned-vs-actual` exposes planned-vs-actual comparisons.
- Public repo exposes a sanitized slice in `examples/training_prediction_sheet_demo.py`.

Tests:

- `human-model-chatbot/test_main.py`
- `human-model-chatbot/test_workout_files.py`
- `human-model-chatbot/test_workout_recommendations.py`
- `human-model/apps/coach-dashboard/backend/tests/test_bridget_import.py`
- `examples/tests/test_public_examples.py`

Failure handling:

- Bridget tells the user to refresh the training model if predictions are missing.
- Workout sheet parsing validates required columns.
- Dashboard importer tolerates missing and malformed ledgers.
- Event append deduplicates by event ID.
- Evidence append is additive and does not break Telegram if it fails.

Fragile or unfinished:

- The full R pipeline is not exposed publicly.
- Some orchestration still sits in large root-level `main.py`.
- There is no public one-command run for the whole training recommendation loop.

### Workflow C: Movement Video Through MediaPipe Analysis And Dashboard Review

Entry points:

- Single-video utilities: `human-model/scripts/data-ingestion/pose_extraction.py`, `scripts/utilities/rdl_metrics.py`, `scripts/utilities/batch_analyze_rdl.py`.
- Refactored movement-quality package: `human-model/modeling/movement-quality/`.
- Multi-angle RDL batch entry: `modeling/movement-quality/tracks/rdl/scripts/batch_analyze_rdl.py`.
- Dashboard review API: `apps/coach-dashboard/backend/app/movement.py`.
- Dashboard UI: `apps/coach-dashboard/frontend/app/movement/page.tsx`.

Data structures:

- Raw video files under `videos/raw/`.
- Pose landmarks in `data/pose_landmarks/`.
- RDL metrics and rep summaries in `data/form_metrics/`.
- Metadata in `data/set_metadata/sets.csv` and `rdl_video_metadata.csv`.
- Annotated video exports in `output/exports/`.
- Plot artifacts in `output/charts/`.

Transformations:

- MediaPipe extracts landmarks.
- RDL metrics derive hip, knee, and torso angles.
- Rep windows produce duration, ROM proxy, tempo flags, ROM drop flags, and interpretation notes.
- Multi-angle batch inference preserves camera view and side metadata.
- Only side and unknown views use side-view hinge metrics; other camera views are preserved as separate observations instead of forced into invalid metrics.

Persistence:

- CSV artifact files and video/plot exports on local disk.
- Dashboard reads artifacts rather than hiding them behind opaque model state.

Service boundaries and outputs:

- `GET /movement/videos`
- `GET /movement/videos/{video_id}`
- `GET /movement/videos/{video_id}/annotated-video`
- Dashboard page can review tracking quality, rep rows, interpretation, plots, and annotated playback.
- Public repo exposes a demo video under `demo/mediapipe-rdl-form/` and mock review logic in `examples/movement_quality_demo.py`.

Tests:

- `human-model/apps/coach-dashboard/backend/tests/test_movement.py`
- `human-model/modeling/tests/test_movement_quality_refactor.py`
- `examples/tests/test_public_examples.py`

Failure handling:

- Dashboard rejects unsafe video IDs.
- Missing artifacts return empty lists or 404s.
- Low tracking coverage is surfaced as a caution note.
- Metadata templates can be created when batch metadata is missing.

Fragile or unfinished:

- Narrow RDL-specific implementation.
- Public repo does not include a runnable real MediaPipe pipeline.
- Multi-angle public evidence is currently mostly documentation rather than an inspectable public artifact.

## 5. Public Evidence Audit

| Capability | Repository | Existing evidence | Publicly safe | Engineering depth | Easy to evaluate | Recommended action |
|---|---|---|---|---|---|---|
| Public project thesis and status map | `the-human-model` | `README.md`, `docs/evidence-map.md`, `docs/implementation-progress.md` | Yes | Medium | Yes | Feature prominently |
| Public runnable examples | `the-human-model` | `examples/*.py`, `examples/tests/test_public_examples.py`, CI | Yes | Medium | Yes | No action needed |
| Public CI | `the-human-model` | `.github/workflows/public-repo-checks.yml` | Yes | Medium | Yes | Feature prominently |
| Apple Health recovery import | `human-model`, `human-model-chatbot` | Apple Health importers, SQLite tables, Notion upsert path, tests | Partly | High | No, private | Create sanitized reference version |
| Readiness modeling | all three | Dashboard readiness, public demos, tests | Yes | Medium-high | Yes | Feature prominently |
| Coach Dashboard FastAPI/SQLite backend | `human-model` | `apps/coach-dashboard/backend/app/*`, migrations, tests | Partly | High | No, private | Copy/sanitize vertical slice |
| Coach Dashboard Next.js frontend | `human-model` | `apps/coach-dashboard/frontend/app/*`, screenshots | Partly | Medium | Partly | Add architecture explanation |
| Bridget Telegram workflows | `human-model-chatbot` | `main.py`, `app/bridget/*`, screenshots, tests | Partly | High | No, private | Add architecture explanation and public slice |
| Bridget event ledger | `human-model-chatbot`, `human-model` | `bridget_events.py`, `bridget_import.py`, SQLite migrations, tests | Yes if mocked | High | No, private | Create sanitized reference version |
| Training-load modeling | `human-model` | R scripts, model artifacts, reports, prediction CSVs | Partly | High | No, private | Feature in docs; sanitize one output-driven slice |
| Editable workout sheets | `human-model-chatbot`, `the-human-model` | Private generator/importer plus public demo/test | Yes | High | Partly | Feature prominently |
| Zenfit OCR/parsing | `human-model-chatbot` | `app/pipelines/zenfit/*`, `zenfit/*`, tests | Partly | High | No, private | Add architecture explanation; leave private data private |
| Apple Watch output review | `human-model` | `training_output.py`, tests, dashboard route | Yes if mocked | High | No, private | Include in vertical slice only if scope stays small |
| MediaPipe RDL analysis | `human-model`, `the-human-model` | Movement package, dashboard API, demo video, public mock example | Partly | High | Partly | Add architecture explanation; keep public demo narrow |
| Multi-angle RDL batch | `human-model` | `batch_analyze_rdl.py`, metadata columns, summary logic | Partly | Medium-high | No, private | Create public artifact or doc excerpt |
| Media ingestion boundary | both | `docs/media-ingestion-architecture.md`, public router demo | Yes | Medium | Yes | Keep as architecture/design; do not over-feature |
| Notion integration | `human-model-chatbot`, `human-model` | Recovery, Zenfit, dashboard sync adapters | No for live IDs/data | Medium-high | No | Leave private; document adapter shape |
| Privacy/sanitization boundary | `the-human-model` | Evidence map, examples README, mock outputs | Yes | Medium | Yes | Feature prominently |

## 6. Recommended Public Strategy

Primary recommendation: C. Assemble several existing components into one runnable public vertical slice.

Why:

- Option A is not enough. The public repo is honest and useful, but it does not let an engineering lead inspect the real system shape quickly.
- Option B is close, but copying only one subsystem would either expose too much private implementation or miss the cross-boundary engineering signal.
- Option C preserves the actual architecture while replacing private adapters with mocks.
- Option D would waste effort and risk making the public example look toy-like even though the real system is stronger.

Exact workflow:

```text
Mock recovery export + mock planned workout + mock prediction CSV
-> validation and local SQLite persistence
-> readiness score and guarded workout sheet
-> FastAPI endpoints
-> static review summary
-> tests
```

Existing files or modules to reuse:

- From `the-human-model`:
  - `examples/readiness_modeling_demo.py`
  - `examples/training_prediction_sheet_demo.py`
  - `examples/dashboard_data_shaping_demo.py`
  - `examples/media_ingestion_router_demo.py` only for style of mock boundary, not as core scope
- From `human-model`:
  - `apps/coach-dashboard/backend/app/schemas.py`
  - `apps/coach-dashboard/backend/app/readiness.py`
  - `apps/coach-dashboard/backend/app/training_output.py` concepts
  - `apps/coach-dashboard/backend/migrations/001_initial.sql`
  - `apps/coach-dashboard/backend/migrations/005_apple_watch_workouts.sql`
  - `apps/coach-dashboard/backend/migrations/006_apple_watch_daily_energy.sql`
- From `human-model-chatbot`:
  - `workout_recommendations.py` sheet-shaping logic
  - `app/pipelines/contracts.py`
  - `app/pipelines/workout_files/*`
  - `bridget_events.py` event shape, with local mock storage

What must remain private:

- Real Apple Health export files.
- Real Notion tokens, database IDs, and private page contents.
- Telegram tokens, chat IDs, launchd paths, and private Bridget state.
- Raw workout history unless explicitly sanitized.
- Raw videos and identifiable health/training media.

What should be replaced with mock data or adapters:

- Apple Health inbox reader.
- Notion API adapters.
- Telegram send/receive calls.
- Local absolute paths.
- Real model artifacts if they encode private training history.
- Real movement video files unless explicitly approved as public.

Strongest signal with least unnecessary work:

- A small FastAPI + SQLite public reference slice beats another standalone script.
- It should be runnable without credentials and should use committed mock data.
- It should include tests that prove idempotent import, missing-data handling, guarded recommendations, and editable correction fields.

## 7. Recommended Public Vertical Slice

Proposed folder structure in `the-human-model`:

```text
reference-implementation/
  README.md
  pyproject.toml
  app/
    __init__.py
    api.py
    db.py
    schemas.py
    importers/
      mock_health.py
      mock_training_plan.py
      mock_predictions.py
    models/
      readiness.py
      workout_sheet.py
    services/
      review_summary.py
  data/
    mock_health_export.json
    mock_training_plan.csv
    mock_next_session_predictions.csv
  tests/
    test_health_import.py
    test_readiness.py
    test_workout_sheet.py
    test_api.py
```

Files to reuse:

- Adapt `examples/readiness_modeling_demo.py` into `app/models/readiness.py`.
- Adapt `examples/training_prediction_sheet_demo.py` into `app/models/workout_sheet.py`.
- Reuse the Pydantic schema style from `human-model/apps/coach-dashboard/backend/app/schemas.py`.
- Reuse the SQLite migration shape from `human-model/apps/coach-dashboard/backend/migrations/001_initial.sql`.
- Reuse the validation expectations from `human-model-chatbot/test_workout_files.py`.

Files to sanitize:

- `workout_recommendations.py`: retain guarded sheet shaping, remove private paths and Telegram-specific send logic.
- `apple_health.py` importer concepts: retain timestamp parsing, HRV-in-sleep-window rule, idempotency, and missing-data handling; replace Health Auto Export paths with committed mock JSON.
- Bridget event shape: retain event ID/hash/provenance shape; write to a local test fixture or SQLite table.

Files newly created:

- Public `reference-implementation/README.md`
- `app/api.py` with a small FastAPI surface
- `app/db.py` with local SQLite setup
- mock fixture files under `reference-implementation/data/`
- focused tests under `reference-implementation/tests/`

Expected command:

```bash
cd reference-implementation
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest
uvicorn app.api:app --reload --port 8010
```

Expected output:

- `GET /health` returns `{"ok": true}`.
- `POST /imports/mock-health` imports mock recovery rows idempotently.
- `GET /readiness/latest` returns score, band, confidence/data-quality notes, and limiting factors.
- `POST /workout-sheet` creates an editable sheet payload with recommended fields and blank actual fields.
- `POST /feedback/workout-sheet` accepts corrected actuals and stores a planned-vs-actual comparison.
- `GET /review/daily` returns a human-readable JSON summary suitable for a small dashboard card.

Minimum useful test suite:

- Health import parses sleep, HRV, resting HR, steps, and active energy.
- Re-import is idempotent.
- Missing sleep lowers confidence without treating missing data as bad recovery.
- Readiness score exposes factors and data quality.
- Workout sheet preserves exercise order, set role, recommended reps, qualitative loads, and blank actual fields.
- Feedback import validates required actual fields and stores planned-vs-actual comparison.
- API smoke tests cover the main routes.

## 8. Prioritized Plan

### Phase 0: No-Code Improvements

| Repository | File or folder | Intended change | Why it matters | Effort | Required |
|---|---|---|---|---|---|
| `the-human-model` | `README.md` | Add a short "For hiring reviewers" path linking evidence map, examples, screenshots, and private implementation summary | Reduces two-minute scan friction | small | required |
| `the-human-model` | `docs/evidence-map.md` | Add a "strongest engineering evidence" subsection naming the three end-to-end workflows | Makes actual implementation depth easier to see | small | required |
| `the-human-model` | `docs/implementation-progress.md` | Add local test evidence summary for public and private workflow tests | Shows reliability without publishing private code | small | required |
| `human-model` | `README.md` | Replace stale "most directories are placeholders" language with current dashboard/modeling/movement status | Avoids underselling implemented work | small | required |
| `the-human-model` | `docs/source-context.md` | Clarify that private repos contain real implementation and public repo contains sanitized evidence | Helps reviewers interpret mock demos correctly | small | optional |

### Phase 1: Expose Existing Engineering

| Repository | File or folder | Intended change | Why it matters | Effort | Required |
|---|---|---|---|---|---|
| `the-human-model` | `reference-implementation/` | Add the small runnable FastAPI/SQLite vertical slice described above | Gives reviewers a real inspectable subsystem | medium | required |
| `the-human-model` | `reference-implementation/data/` | Add mock health, training plan, and prediction fixtures | Keeps private data private while preserving workflow shape | small | required |
| `the-human-model` | `reference-implementation/tests/` | Add focused tests for import, readiness, sheet shaping, feedback, and API routes | Converts claims into verifiable evidence | medium | required |
| `the-human-model` | `.github/workflows/public-repo-checks.yml` | Add reference implementation tests to CI | Makes public engineering evidence visible | small | required |
| `the-human-model` | `docs/evidence-map.md` | Link each public vertical-slice endpoint/test to the private capability it represents | Prevents the mock slice from looking disconnected | small | optional |

### Phase 2: Improve Engineering Evidence

| Repository | File or folder | Intended change | Why it matters | Effort | Required |
|---|---|---|---|---|---|
| `human-model` | `.github/workflows/` | Add private CI for backend/modeling tests if feasible | Improves maintainability and confidence | medium | optional |
| `human-model-chatbot` | `.github/workflows/` | Add private CI for unit tests if feasible | Shows Bridget workflows are protected | medium | optional |
| `human-model-chatbot` | `main.py` and `app/` | Continue moving orchestration from root `main.py` into narrower modules | Improves scanability and maintainability | large | optional |
| `human-model` | `docs/media-ingestion-architecture.md` or public doc excerpt | Add one small sample manifest and review record | Makes design boundary more concrete without live uploads | small | optional |
| `the-human-model` | `demo/mediapipe-rdl-form/` | Add a tiny public metadata/summary artifact for the existing demo video | Strengthens movement evidence without exposing private videos | small | optional |

Required work should stay intentionally small: Phase 0 plus the narrow Phase 1 vertical slice is enough to materially improve hiring signal. Phase 2 is worthwhile only after the public reviewer path is clear.
