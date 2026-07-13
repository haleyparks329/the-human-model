# Public Readiness Slice Review

Review target: `reference-implementation/readiness-slice/`

Review date: 2026-07-13

## 1. Executive Verdict

Yes: this slice successfully demonstrates a real end-to-end engineering system at a portfolio-appropriate size.

The strongest evidence is that the workflow is runnable, typed, tested, and split along meaningful boundaries:

```text
mock Apple Health fixture -> validation/normalization -> SQLite -> readiness model -> FastAPI -> daily review JSON
```

This is not just a collection of examples. It has migrations, repository functions, idempotent imports, error handling, deterministic scoring, API response contracts, and temporary database tests. A reviewer can see that the private Human Model work has been reduced into a public-safe slice without exposing private records or dragging in unrelated systems.

Required fixes before presenting publicly are small:

1. Surface this slice from the root README/evidence map so reviewers can find it quickly.
2. Harden fixture-name resolution so API callers cannot request paths outside `data/fixtures/`.
3. Strengthen date validation so calendar-invalid dates such as `2026-99-99` return a controlled `422` instead of leaking a downstream parsing error.
4. Add one or two focused tests for thin-baseline confidence and update-versus-unchanged import counts.
5. Resolve the stale root `.python-version` pin.

## 2. Five-Minute Reviewer Assessment

A hiring reviewer can understand what this demonstrates in under five minutes if they start in `reference-implementation/readiness-slice/README.md`.

The slice README leads with the exact workflow, then lists engineering evidence: parsing, timestamp normalization, validation, idempotent persistence, import runs, deterministic scoring, API models, daily review JSON, and tests. That is the right order. It does not bury the implementation under product narrative.

The quickest useful reading path should be made explicit from the root repo:

1. `reference-implementation/readiness-slice/README.md`
2. `reference-implementation/readiness-slice/readiness_slice/health_import.py`
3. `reference-implementation/readiness-slice/readiness_slice/repository.py`
4. `reference-implementation/readiness-slice/readiness_slice/readiness.py`
5. `reference-implementation/readiness-slice/readiness_slice/api.py`
6. `reference-implementation/readiness-slice/tests/`

The implementation is easy to run. I reran the install, tests, and demo with:

```bash
cd reference-implementation/readiness-slice
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
python -m readiness_slice.demo
```

Result: `15 passed in 0.51s`, and the demo printed a daily review JSON for `2026-06-23`.

The README makes public/private boundaries clear: synthetic fixtures only, no Telegram, no Notion, no private health export, no local paths, no credentials. The only reviewer-experience gap is discoverability from the root project page.

## 3. Architecture Assessment

The module boundaries are justified for this scope.

`readiness_slice/health_import.py` owns Health Auto Export-style parsing, timestamp normalization, fixture loading, validation, daily aggregation, warnings, and import result counts.

`readiness_slice/repository.py` owns SQLite persistence and converts database rows back into domain dataclasses.

`readiness_slice/readiness.py` owns deterministic readiness scoring and keeps model assumptions close to code.

`readiness_slice/review.py` composes persisted recovery data, readiness results, import-run health, missing-data summaries, and the public boundary note.

`readiness_slice/api.py` exposes a narrow FastAPI surface without pulling validation or scoring logic directly into route handlers.

`readiness_slice/models.py` carries both internal dataclasses and API-facing Pydantic models. That is reasonable here. The dataclasses keep domain/repository code lightweight; the Pydantic models make API responses explicit.

There is little over-abstraction. The repository is a function-level persistence boundary rather than a class hierarchy, which fits the slice. The migration system is minimal but real. The service layer in `review.py` is thin, but it earns its existence by keeping compute-if-missing and daily review composition out of `api.py`.

The main coupling concern is that `health_import.import_mock_health_export()` calls `upsert_recovery_day()` directly once aggregation succeeds. This is fine for the slice. If persistence ever needs all-row transaction semantics for database-write failures, the importer would need a repository function that persists a batch in a single connection. For the current public promise, malformed input avoids partial persistence because aggregation happens before any recovery rows are written.

## 4. Model Assessment

The readiness model is deterministic and inspectable.

`readiness_slice/readiness.py::calculate_readiness` uses explicit component weights:

- sleep: `0.35`
- HRV: `0.35`
- resting heart rate: `0.30`

It uses visible status thresholds:

- `Push`: score `>= 80`
- `Maintain`: score `>= 65`
- `Modify`: score `>= 50`
- `Rest`: score `< 50`

Missing critical data downgrades the call and lowers confidence. Thin baselines are represented through confidence and explanatory factors such as `HRV present but baseline is thin`. The returned `factors` and `data_freshness` make the decision auditable rather than mystical.

The model does not overclaim medical or scientific validity. README language says it is a transparent baseline, not a validated prescription model. That boundary is important and should stay.

There is some conceptual overlap with the existing public readiness demos, but the slice is different enough to justify keeping it. The demos explain model ideas in isolated scripts; this slice proves the surrounding engineering: import, persistence, API, idempotency, and testable contracts.

One small improvement: add a direct thin-baseline test so the confidence behavior is not only implicit in the implementation.

## 5. Import And Persistence Assessment

The importer handles the core behavior well.

Timestamp parsing supports Health Auto Export-style timestamps such as `2026-06-18 06:30:00 +0200` in `parse_health_datetime()`, then converts to the configured local timezone in `local_date()`. This is the right direction for daily recovery aggregation.

Unknown metrics are warnings, not fatal errors. That is correct for a narrow public importer because real exports often contain extra signals, and unsupported signals should not block known recovery data.

Validation errors are fatal for the import run and avoid partial recovery persistence for malformed JSON or invalid metric values. Tests cover malformed JSON and non-numeric sleep values. The import run itself is still recorded, which is useful operationally.

Idempotency is implemented through `repository.upsert_recovery_day()`, which compares the persisted normalized row against the incoming normalized row and returns `inserted`, `updated`, or `unchanged`. Re-importing the same fixture returns `rows_unchanged == 6` and leaves the recovery row count unchanged.

Counts are mostly well represented. The current tests prove inserted and unchanged counts. They do not yet prove an actual `updated` count, so add one small test with the same date and changed value.

Two small persistence/validation issues should be fixed before public presentation:

- `health_import._fixture_paths()` joins user-provided fixture names to the fixture root without rejecting `../` path traversal or absolute paths.
- `models.require_iso_date()` checks only the `YYYY-MM-DD` shape, not calendar validity. `recovery_history_through()` later calls `date.fromisoformat()`, so invalid calendar dates can fail below the API validation layer.

## 6. API Assessment

The API is coherent and intentionally narrow:

- `GET /health`
- `POST /imports/mock-health`
- `GET /imports`
- `GET /recovery`
- `GET /recovery/{date}`
- `POST /readiness/{date}`
- `GET /readiness/{date}`
- `GET /daily-review/{date}`

The endpoint set maps directly to the vertical slice. There are no unrelated auth, deployment, dashboard, Telegram, Notion, or training features.

Status codes are mostly correct:

- missing fixture: `404`
- malformed fixture payload: `422`
- invalid date shape: `422`
- missing recovery day: `404`
- successful import/readiness/review: `200`

Response models are explicit for the main public shapes: import result, recovery day, readiness result, and daily review. Error details are useful without exposing secrets.

The one API behavior that should be documented more clearly is compute-if-missing: `GET /readiness/{date}` and `GET /daily-review/{date}` can persist a readiness result if one does not already exist. This is acceptable for a local reference slice, but reviewers should not have to infer it from `review.get_or_compute_readiness()`.

## 7. Test Assessment

Current test result: `15 passed in 0.51s`.

High-value behavior tests:

- `test_api_import_and_fetch_flow`: proves import -> recovery -> readiness -> daily review through FastAPI.
- `test_import_complete_fixture_normalizes_recovery_day`: proves fixture normalization and persisted values.
- `test_import_missing_sleep_sets_quality_flag_not_failure`: proves missing-data handling.
- `test_import_is_idempotent`: proves re-import unchanged behavior.
- `test_malformed_json_records_error_without_rows`: proves malformed input records an error without recovery rows.
- `test_non_numeric_metric_records_error_without_partial_rows`: proves validation failure avoids recovery persistence.
- `test_daily_review_json_has_public_boundary_and_missing_data`: proves public/private boundary and review payload composition.

Useful edge-case tests:

- `test_parse_health_datetime_accepts_health_auto_export_offset`: covers export timestamp format.
- `test_import_records_unknown_metric_warning`: covers warning versus error behavior.
- `test_invalid_fixture_handling_returns_404`: covers API fixture error status.
- `test_invalid_date_returns_validation_response`: covers malformed date shape.
- `test_missing_recovery_returns_404`: covers missing domain resource.
- `test_readiness_with_missing_data_low_confidence`: covers missing critical data.
- `test_readiness_with_sufficient_baseline_returns_push_or_maintain`: covers deterministic scoring at a coarse behavior level.
- `test_readiness_persistence_is_idempotent`: covers persisted readiness upsert behavior.

Low-value implementation tests:

- None are obviously low-value. The suite is behavior-heavy and appropriately small.

Missing coverage worth adding:

- Fixture path traversal or absolute-path rejection.
- Calendar-invalid date validation, for example `2026-99-99`.
- Update-versus-unchanged import counts for the same date with changed normalized values.
- Thin-baseline confidence without missing critical inputs.
- `GET /readiness/{date}` compute-if-missing behavior, if that behavior remains.

The suite already covers temporary database isolation through `tests/conftest.py`, which sets `READINESS_SLICE_DB` to a per-test temporary SQLite path and applies migrations.

## 8. Privacy Assessment

The public boundary is strong.

The slice uses committed synthetic fixtures under `data/fixtures/`, not private Apple Health export files. The code does not depend on Telegram tokens, Notion IDs, private local paths, real device data, screenshots, or credentials.

`review.PUBLIC_BOUNDARY_NOTE` makes the public/private boundary visible in the API-facing daily review payload. That is an excellent portfolio choice because it demonstrates not only engineering skill, but judgment about what not to expose.

The only privacy-adjacent hardening needed is fixture path confinement. Even in a local public demo, an API parameter that can point outside the fixture directory is not a good public-safe boundary.

## 9. Interview Decision Map

1. `readiness_slice/health_import.py::aggregate_files`
   - Likely question: Why aggregate all fixture rows before writing to SQLite?
   - Strong answer: This separates validation/normalization from persistence and prevents malformed input from partially writing recovery rows.
   - Skeptical follow-up: What failure modes could still create partial writes?

2. `readiness_slice/health_import.py::_DailyHealthBucket.finalize_hrv`
   - Likely question: Why prefer HRV samples inside the sleep window?
   - Strong answer: Recovery HRV is more meaningful when aligned to rest; when no sleep window exists, the model falls back to a daily mean and flags that reduced data quality.
   - Skeptical follow-up: How would you communicate that fallback to users without overstating confidence?

3. `readiness_slice/health_import.py::_fixture_paths`
   - Likely question: Why restrict imports to fixture names instead of arbitrary paths?
   - Strong answer: This is a public-safe mock importer, so the API should only read committed fixtures; arbitrary paths would blur public/private boundaries.
   - Skeptical follow-up: How would you prove path traversal is blocked?

4. `readiness_slice/repository.py::upsert_recovery_day`
   - Likely question: Why return `inserted`, `updated`, or `unchanged` instead of just upserting?
   - Strong answer: Import runs need operational transparency; idempotency is more convincing when unchanged rows are counted separately from inserts and updates.
   - Skeptical follow-up: What fields should be compared to decide whether a row changed?

5. `readiness_slice/migrations/001_initial.sql`
   - Likely question: Why use SQLite and a migration file for such a small slice?
   - Strong answer: SQLite keeps local setup simple while still demonstrating schema ownership, persistence boundaries, uniqueness constraints, and foreign keys.
   - Skeptical follow-up: Where would transaction handling need to change if this became multi-user?

6. `readiness_slice/readiness.py::calculate_readiness`
   - Likely question: Why use a transparent weighted model instead of an LLM or opaque score?
   - Strong answer: Readiness decisions should be inspectable; weights, thresholds, missing data, and confidence are visible and testable.
   - Skeptical follow-up: How would you validate or recalibrate these thresholds over time?

7. `readiness_slice/readiness.py::_confidence`
   - Likely question: Why separate score from confidence?
   - Strong answer: A plausible score from thin or incomplete data should not imply certainty; confidence communicates data sufficiency.
   - Skeptical follow-up: Should missing sleep always downgrade the call even when HRV and resting HR look good?

8. `readiness_slice/review.py::daily_review_for_date`
   - Likely question: Why have a daily review service instead of returning raw readiness only?
   - Strong answer: The real product needs reviewable JSON that combines signals, import health, missing data, model output, and public/private boundary metadata.
   - Skeptical follow-up: Is it surprising that daily review can compute and persist readiness?

9. `readiness_slice/api.py::import_mock_health`
   - Likely question: Why map blocked fixture import to `404` and malformed fixture data to `422`?
   - Strong answer: Missing fixture is a missing resource; malformed fixture content is an unprocessable request for this importer.
   - Skeptical follow-up: Should the API return the import run record even when the HTTP response is an error?

10. `tests/conftest.py::isolated_db`
    - Likely question: Why force every test onto a temporary SQLite database?
    - Strong answer: It proves persistence behavior without shared state, protects local demo data, and keeps tests deterministic.
    - Skeptical follow-up: How would you catch migration bugs if every test starts from a fresh database?

## 10. Required Fixes Before Presenting Publicly

Keep these small:

1. Add a root-level pointer to the slice in `README.md` and likely `docs/evidence-map.md`, so the public reviewer path is obvious.
2. In `health_import._fixture_paths()`, reject absolute paths, path separators, `..`, and non-JSON names; resolve the candidate and ensure it stays under `fixture_dir()`.
3. In `models.require_iso_date()`, call `date.fromisoformat(value)` after the regex shape check and convert failures to the same controlled validation error.
4. Add tests for fixture path confinement, calendar-invalid dates, update counts, and thin-baseline confidence.
5. Fix or remove the stale root `.python-version`.

## 11. Optional Improvements

- Document compute-if-missing behavior for `GET /readiness/{date}` and `GET /daily-review/{date}` in the slice README.
- Add a small `README` reading path for reviewers who have only three minutes.
- Consider wrapping successful multi-day recovery persistence in one repository batch transaction if the importer later grows beyond fixtures.
- Add return annotations to API route functions for consistency.
- Add one comment near the readiness weights explaining that they are illustrative, transparent defaults rather than validated physiological constants.

## 12. Things Not To Add Yet

Do not add Telegram, Notion, training-load prediction, workout sheets, MediaPipe, Next.js, authentication, deployment, Docker, schedulers, generalized ingestion plugins, or a frontend.

Do not turn the slice into a product. Its strength is that it proves real engineering depth without broadening the surface area.

## 13. Recommended Handling Of `.python-version`

The root `.python-version` currently contains `3.9.6`. On this machine, plain `python --version` fails because pyenv is pointed at that missing version, while `pyenv versions --bare` shows `3.12.8`. `python3 --version` succeeds and reports `Python 3.9.6`, which is why the documented venv command still works.

Smallest appropriate fix: remove the root `.python-version` unless the public repo intentionally requires pyenv. The project already states package compatibility through `pyproject.toml` (`>=3.9`) and CI tests both `3.9` and `3.12` through `actions/setup-python`.

If you want a local pyenv pin anyway, update `.python-version` to an installed version such as `3.12.8`. But for a public portfolio repo, removing the stale local pin is cleaner because it avoids surprising reviewers while keeping CI and README setup aligned.
