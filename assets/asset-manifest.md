# Asset Manifest

This manifest is the canonical source for public asset provenance in this repository. It covers committed screenshots, generated visuals, and video assets used as public evidence for The Human Model.

## Policy

- Private health exports, raw Notion database exports, credentials, local paths, and private automation files do not belong in this repository.
- Public assets must be intentionally public.
- Personal metrics, chat content, and training data must be mock, redacted, or explicitly approved before publication.
- Metadata should be reviewed before publication.
- The current committed screenshots and RDL video are approved for public use by Haley as of 2026-07-13; future assets should still be reviewed before publication.

## Assets

| Asset path | Subsystem | Asset type | Provenance | Data classification | Sanitization status | Public-use status | Notes |
|---|---|---|---|---|---|---|---|
| `assets/screenshots/coach-dashboard-01-overview.png` | Coach Dashboard | PNG screenshot | Approved real public UI capture | Approved visible dashboard/recovery data | PNG metadata stripped in this pass; visible content unchanged | Approved for current docs, README, and public promotion | Overview page evidence for local dashboard. |
| `assets/screenshots/coach-dashboard-02-recovery.png` | Coach Dashboard | PNG screenshot | Approved real public UI capture | Approved visible recovery data | PNG metadata stripped in this pass; visible content unchanged | Approved for current docs and public promotion | Recovery page evidence. |
| `assets/screenshots/coach-dashboard-03-training-output.png` | Coach Dashboard | PNG screenshot | Approved real public UI capture | Approved visible training-output data | PNG metadata stripped in this pass; visible content unchanged | Approved for current docs and public promotion | Training output evidence. |
| `assets/screenshots/coach-dashboard-04-training-log.png` | Coach Dashboard | PNG screenshot | Approved real public UI capture | Approved visible training-log data | PNG metadata stripped in this pass; visible content unchanged | Approved for current docs and public promotion | Training log evidence. |
| `assets/screenshots/coach-dashboard-05-body.png` | Coach Dashboard | PNG screenshot | Approved real public UI capture | Approved visible body metrics | PNG metadata stripped in this pass; visible content unchanged | Approved for current docs and public promotion | Body-measurement evidence approved for public use by Haley. |
| `assets/screenshots/coach-dashboard-06-signals.png` | Coach Dashboard | PNG screenshot | Approved real public UI capture | Approved visible signal/source state | PNG metadata stripped in this pass; visible content unchanged | Approved for current docs and public promotion | Signal-health evidence. |
| `assets/screenshots/coach-dashboard-07-reviews.png` | Coach Dashboard | PNG screenshot | Approved real public UI capture | Approved visible review workflow | PNG metadata stripped in this pass; visible content unchanged | Approved for current docs and public promotion | Review page evidence. |
| `assets/screenshots/telegram-01-recovery-coaching-outline.png` | Bridget / Telegram | PNG screenshot | Approved real public UI capture | Approved visible chat content | PNG metadata stripped in this pass; visible content unchanged | Approved for current docs and public promotion | Early recovery conversation evidence. |
| `assets/screenshots/telegram-02-shoulder-recovery-note.png` | Bridget / Telegram | PNG screenshot | Approved real public UI capture | Approved visible chat content | PNG metadata stripped in this pass; visible content unchanged | Approved for current docs and public promotion | Recovery note evidence. |
| `assets/screenshots/telegram-03-recovery-json-logging.png` | Bridget / Telegram | PNG screenshot | Approved real public UI capture | Approved visible chat content and structured recovery fields | PNG metadata stripped in this pass; visible content unchanged | Approved for current docs and public promotion | Structured logging evidence. |
| `assets/screenshots/telegram-04-morning-checkin-update.png` | Bridget / Telegram | PNG screenshot | Approved real public UI capture | Approved visible chat content and health-context fields | PNG metadata stripped in this pass; visible content unchanged | Approved for current docs and public promotion | Morning check-in evidence. |
| `assets/screenshots/telegram-05-health-context-and-workout-log.png` | Bridget / Telegram | PNG screenshot | Approved real public UI capture | Approved visible chat content, health context, and workout content | PNG metadata stripped in this pass; visible content unchanged | Approved for current docs and public promotion | Health-context and workout-log evidence. |
| `assets/screenshots/telegram-06-workout-summary.png` | Bridget / Telegram | PNG screenshot | Approved real public UI capture | Approved visible workout summary | PNG metadata stripped in this pass; visible content unchanged | Approved for current docs and public promotion | Parsed workout summary evidence. |
| `assets/screenshots/telegram-07-bridget-calibration.png` | Bridget / Telegram | PNG screenshot | Approved real public UI capture | Approved visible preference-calibration chat content | PNG metadata stripped in this pass; visible content unchanged | Approved for current docs and public promotion | Bridget calibration evidence. |
| `examples/daily_card_demo.svg` | Bridget daily card | SVG generated visual | Generated from mock data | Mock data | Text SVG; no binary metadata review needed | Public canonical generated output | `examples/daily_card_demo.py` regenerates this committed file deterministically. Promoted into README via `examples/sample-output/bridget-daily-card.svg`. |
| `examples/sample-output/bridget-daily-card.svg` | Bridget daily card | SVG generated visual | Generated from mock data | Mock data | Text SVG; no binary metadata review needed | Public README visual and sample output | Curated copy of `examples/daily_card_demo.svg` for the sample-output evidence layer. |
| `demo/mediapipe-rdl-form/rdl-form-mediapipe-overlay-demo.mov` | Movement analysis | MOV screen recording | Approved real public UI capture | Approved visible training-video demo content | Container metadata reviewed; left intact by choice | Approved for current docs and public promotion | MOV metadata was reviewed and intentionally left intact for now. |

## Generated Output Policy

`examples/daily_card_demo.svg` is a canonical committed output. Running `python3 examples/daily_card_demo.py` regenerates that file deterministically from mock data. Future ad hoc generated files should go under `examples/output/`, whose contents are ignored by Git.
