# Implementation Progress

Last updated: 2026-06-18.

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

Key commits reviewed:

- `776f507c` - Add project README
- `d2066aa5` - Add Recovery Tracking V1 schema
- `c934b6a5` - Add weekly review template
- `bbdf6619` - Document chatbot logging contract
- `59523704` - Add local coach dashboard app

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

Local in-progress work reviewed but not counted as committed release state:

- Python readiness computation for Coach Dashboard V1 in the chatbot repo working tree
- Notion schema setup/repair for readiness fields, steps, and weight
- Readiness refresh hooks after Telegram recovery check-ins and Apple Health imports
- Focused readiness tests covering scoring, low-sleep caps, missing-data confidence, bad-mood rest calls, and coach overrides

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
9. Run a local Coach Dashboard V1 app backed by SQLite, with Notion sync/backfill paths and app-native body/review entry surfaces.

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

## What Is Still Early

- The recovery score is not yet a stable model.
- Coach Dashboard V1 exists, but it is still a local working dashboard rather than a polished product.
- The Python readiness pipeline is under active local integration and should be treated as in progress until committed.
- Notion Weekly Review historical backfill is blocked until the database is shared with the integration or replaced with a confirmed ID.
- Analytics notebooks are still future work.
- Movement-quality sensing is planned but not implemented yet.
- Recommendations are intentionally limited until the data spine has enough real use.
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
-> local dashboard and readiness data model
-> future modeling and sensing
```

That path shows practical systems integration around a real personal workflow.
