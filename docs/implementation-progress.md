# Implementation Progress

Last updated: 2026-07-05.

This page summarizes what has been built across the active Human Model repositories. It is intentionally written as a progress log, not a product claim.

## Foundation Repo

Repository: [haleyparks329/human-model](https://github.com/haleyparks329/human-model)

Implemented:

- Project README and repository structure
- Recovery Tracking V1 schema
- Weekly Review V1 template
- Chatbot Logging Contract V1
- Separation of responsibilities between the foundation repo and chatbot repo
- Local Coach Dashboard V1 app using FastAPI, SQLite, and Next.js
- Dashboard data audit defining source ownership, conflict policy, SQLite mappings, and blocked/unavailable states
- Readiness Dashboard V1 documentation for the push/maintain/modify/rest training decision loop
- Screenshot documentation for Coach Dashboard V1 across overview, recovery, training, body, signals, and reviews
- Body-measurement progress charts
- Standalone readiness-modeling layer with daily feature generation, a transparent baseline model, report generation, tests, and a dashboard page
- Readiness vs Actual training-output review that compares baseline readiness calls with Apple Watch movement output
- Local MediaPipe movement-quality pipeline for RDL video, including pose extraction, rep metrics, annotated playback, and dashboard review flags
- Training-load modeling pipeline with normalized load history, set-role-aware V2 evaluation, model reports, and guarded next-session recommendation output

Remaining active integration work reviewed:

- Structured lifting schema for sessions, exercises, sets, and training-plan days
- Structured training-session summaries for exercise count, work sets, volume load, muscle groups, parse warnings, weekly volume, and progression signals
- Dashboard V2 API/UI payload for today's lift call, evidence stack, risk/progression cards, weekly training strip, recent-session detail, and recommendations
- Bridget editable workout-sheet flow for reviewing or correcting model-suggested loads in the same format used during training, with active hardening around exercise order, suggested reps, and non-modelable planned sets
- Broader integration between readiness, planned-vs-actual training review, and movement-quality signals

Key commits reviewed:

- `776f507c` - Add project README
- `d2066aa5` - Add Recovery Tracking V1 schema
- `c934b6a5` - Add weekly review template
- `bbdf6619` - Document chatbot logging contract
- `59523704` - Add local coach dashboard app
- `1ac8be43` - Add body measurement progress charts
- `a6bf60d7` - Add standalone readiness model dashboard
- `fd259d2d` - Add readiness vs training output review
- `f13993f2` - Add local MediaPipe form analysis pipeline
- `ce2d810e` - Add movement quality dashboard
- `97490d3f` - Add set-role V2 training load reports
- `c56319f8` - Add guarded next-session recommendations

## Chatbot Repo

Repository: [haleyparks329/human-model-chatbot](https://github.com/haleyparks329/human-model-chatbot)

Implemented:

- Telegram bot backed by a local Ollama model
- Recovery check-in parser
- Notion recovery entry creation/update
- Apple Health import for sleep, HRV, resting heart rate, and weight
- Morning check-in prompt with Apple Watch context
- macOS `launchd` one-shot job for reliable scheduled prompts
- Duplicate prevention for daily check-ins
- Missing sleep and suspiciously low sleep handling
- Zenfit screenshot OCR/import for workouts, weekly coach check-ins, and body measurements
- Parser hardening for Zenfit UI noise, supersets, unilateral exercises, low-confidence OCR, and multi-screenshot merges
- Telegram workout logging
- Per-set workout weight parsing
- Copy-forward workout logging for stable weekly training templates
- Non-numeric load handling, such as bodyweight or machine-weight notes
- Workout-level and exercise-level notes in Telegram logs
- Bridget rhythm prompts and preference calibration
- Bridget planned-workout logging for lower-typing training follow-up
- Bridget daily card generation for a chat-friendly readiness summary
- Append-only Bridget training event ledger for planned-vs-actual review
- Modular app, integration, pipeline, and storage boundaries for the chatbot layer
- Telegram workout file exchange for sending and importing structured workout spreadsheets
- Bridget V2 training recommendations using the Human Model training-load prediction output
- Editable workout sheets for capturing actual weights, reps, and notes while keeping model/debug prediction files separate
- Unit tests for core parser and scheduling behavior

Key commits reviewed:

- `fb3689a` - Add recovery check-in logging
- `d3a4e68` - Add Zenfit screenshot importer with Notion sync
- `ada76a8` - Add Apple Health import and daily morning Telegram check-in
- `9d7097a` - Fix morning check-ins and Zenfit parsing
- `275d65a` - Run morning check-in via launchd one-shot
- `68700a8` - Handle morning sleep data edge cases
- `f286eeb` - Add Telegram workout logging
- `2345ef9` - Fix workout set parsing with per-set weights
- `68b54d3` - Add copy-forward workout logging
- `a69448e` - Support non-numeric workout loads
- `0bbc1c7` - Support workout notes in Telegram logging
- `38c59a3` - Add Bridget rhythm prompts and readiness tracking
- `313ecc6` - Add planned Bridget workout logging
- `7bcde69` - Add Bridget daily card
- `7543262` - Add Bridget workout recommendation ledger
- `0101607` - Add modular Human Model pipeline foundation
- `0a1aee7` - Wire workout file exchange into Telegram
- `49d5cbc` - Document pipeline boundaries and future matching
- `e69d547` - Add Bridget V2 training recommendations
- `6cf6467` - Import generated workout sheets

## Current Working System

The current system can:

1. Import Apple Watch recovery metrics from Health Auto Export JSON files.
2. Write or update a daily Notion recovery row.
3. Send a scheduled morning Telegram prompt with sleep, HRV, and resting heart rate context when available.
4. Avoid using stale sleep data when Apple sleep is missing.
5. Parse a manual recovery reply into structured fields.
6. OCR Zenfit screenshots and convert them into structured workout, progress, and check-in records.
7. Log workout summaries through Telegram.
8. Reuse previous workout templates through Telegram copy-forward logging.
9. Generate and send a Bridget daily card through Telegram.
10. Run a local Coach Dashboard V1 app backed by SQLite, with Notion sync/backfill paths and app-native body/review entry surfaces.
11. Show body-measurement progress charts and dashboard-level trend summaries.
12. Build daily modeling features, score a baseline readiness model, generate a readable report, and expose the model output in a standalone local dashboard view.
13. Import Apple Watch workout and active-energy rows into SQLite for training-output context.
14. Review whether the readiness call aligned with actual movement output through the dashboard's Readiness vs Actual view.
15. Analyze a local RDL video into rep-level movement-quality metrics and inspect the results through a dashboard review page.
16. Generate guarded next-session training-load recommendations from the modeling pipeline.
17. Send Bridget's pre-gym recommendation summary with an editable workout sheet and a separate model/debug CSV.

## Coach Dashboard V1 Screenshots

The current local dashboard is documented in [Coach Dashboard V1](coach-dashboard-v1.md). The screenshots show the working review surface across:

- Operating call and recovery trend
- Recovery table and manual recovery entry
- Training output and training log audit views
- Body composition trends and raw measurements
- Import/sync signal health
- Weekly review creation/edit surface

## Public Example Code

The overview repo now includes sanitized example code under [`examples/`](../examples/README.md). These examples use mock data and no private Notion credentials or personal health records.

Included examples:

- Readiness scoring from recovery inputs, training context, and confidence metadata
- Bridget prompt timing, missing-data wording, prompt budgets, and quick replies
- A dependency-light SVG daily card renderer for a chat-friendly readiness summary
- Dashboard data shaping for body trend deltas, training session volume, weekly load, parse warnings, progression signals, and import health
- Baseline readiness modeling with personal HRV/resting-HR baselines, data-quality labels, limiting factors, and report-style output
- Movement-quality interpretation with mock rep traces, range-of-motion flags, tempo checks, and set-level review wording
- Training-prediction sheet shaping that preserves workout order, recommended reps, qualitative loads, guardrails, and blank actual-result fields for Bridget follow-up

## What Is Still Early

- The readiness model is a transparent V0 baseline, not a validated predictive model.
- Coach Dashboard V1 exists, but it is still a local working dashboard rather than a polished product.
- Structured dashboard backfill/session work is partly implemented and still being hardened across training-plan and session-detail paths.
- Notion Weekly Review historical backfill is blocked until the database is shared with the integration or replaced with a confirmed ID.
- Analytics notebooks are still future work.
- Movement-quality analysis has a first local computer-vision prototype, but it is narrow, exercise-specific, and not yet a generalized sensing system.
- Training-load recommendations are guarded and inspectable, but still early; the model is useful for review and correction, not autonomous coaching.
- Editable workout sheets are the current bridge between recommendations and real training notes; the important product behavior is keeping uncertain rows visible instead of hiding them.
- Private health/training data lives in Notion and local files, not in public GitHub.

## Portfolio Takeaway

The important engineering story is the progression from idea to data spine:

```text
project concept
-> schema and contract design
-> natural-language capture
-> Notion persistence
-> wearable import
-> scheduled automation
-> OCR import for training context
-> copy-forward training logs
-> Bridget daily cards
-> local dashboard, readiness data model, structured trend/session summaries, and transparent baseline modeling
-> Apple Watch movement-output review against readiness calls
-> local movement-quality prototype for explainable rep review
-> guarded training-load recommendations and editable Bridget workout sheets
-> future calibration, stronger analytics, and broader sensing
```

That path shows practical systems integration around a real personal workflow.
