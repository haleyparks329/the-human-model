# Coach Dashboard V1

Coach Dashboard V1 is the local review surface for The Human Model. It turns the recovery, training, body, review, and import pipelines into a single coach-style operating view.

This is not presented as a finished SaaS product. It is a local-first working dashboard built to make the data spine easier to audit, review, and improve.

## What It Shows

- Daily operating call with readiness context and missing-data flags
- Recovery history from Apple Watch metrics and subjective check-ins
- Training output summaries from logged sessions
- Body measurement trends from imported and app-entered records
- Body-measurement progress charts on the active dashboard branch
- Structured training-session summaries, weekly volume, review flags, and progression signals in active integration work
- Signal health for Notion sync and backfill jobs
- Weekly review creation/edit surface

## Implementation Context

The dashboard lives in the foundation repo and uses:

- FastAPI backend
- SQLite canonical local store
- Next.js frontend
- Notion as a selected mirror and review layer
- Apple Health, Telegram, and OCR-derived records as upstream context

The V1 design priority is operational usefulness: one place to see the current call, the evidence behind it, and whether the data feeding the system is trustworthy. Bridget remains the daily delivery surface; the dashboard is the deeper review and audit layer.

Active local integration work is making the dashboard less like a raw table viewer and more like a coaching data spine. The private working tree now includes Health Auto Export backfill into SQLite, structured lifting tables, training-plan import, a dashboard V2 payload, and UI panels for today's lift call, risk/progression, weekly training status, and recent-session detail. Those pieces are documented here as directionally current but should be read as in-progress until the private implementation is committed and verified.

## Screenshots

### Overview

![Coach Dashboard V1 overview](../assets/screenshots/coach-dashboard-01-overview.png)

### Recovery

![Coach Dashboard V1 recovery page](../assets/screenshots/coach-dashboard-02-recovery.png)

### Training Output

![Coach Dashboard V1 training output page](../assets/screenshots/coach-dashboard-03-training-output.png)

### Training Log

![Coach Dashboard V1 training log page](../assets/screenshots/coach-dashboard-04-training-log.png)

### Body

![Coach Dashboard V1 body page](../assets/screenshots/coach-dashboard-05-body.png)

### Signals

![Coach Dashboard V1 signals page](../assets/screenshots/coach-dashboard-06-signals.png)

### Reviews

![Coach Dashboard V1 reviews page](../assets/screenshots/coach-dashboard-07-reviews.png)

## Current Limits

- The dashboard is still local-only.
- The readiness call is a V1 interpretation layer, not a validated predictive model.
- Structured Apple Health backfill and training-session normalization are still in active integration.
- Some Notion backfill paths depend on database sharing and integration access.
- Private health and training data remain outside this public repository.
