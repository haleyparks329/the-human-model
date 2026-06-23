# Roadmap

## Phase 1: Foundation

Status: mostly complete.

- Create the public overview repo
- Establish project purpose and architecture
- Define the main repo structure
- Document Recovery Tracking V1
- Document Chatbot Logging Contract V1
- Create a weekly review workflow

## Phase 2: Recovery Tracking V1

Status: implemented and being hardened through real use.

- Create Recovery Tracking V1 schema
- Document the minimum chatbot data contract
- Parse simple recovery check-ins
- Connect chatbot entries to Notion
- Import Apple Watch sleep, HRV, resting heart rate, and weight
- Send scheduled morning Telegram prompts
- Handle missing/suspicious Apple sleep data
- Use real entries and review patterns

## Phase 3: Training Context Capture

Status: implemented for core capture paths and still being hardened.

- Import Zenfit screenshots through OCR
- Write workouts to Notion Training Log
- Write weekly coach check-ins to Notion
- Write progress/body measurement screenshots to Notion
- Log workout summaries through Telegram
- Reuse stable weekly training plans through copy-forward Telegram logging
- Support per-set weights, qualitative loads, and workout notes
- Improve date handling for delayed screenshot imports
- Shape raw workout rows into sessions, sets, weekly volume, review flags, and progression signals for the dashboard
- Compare training context against recovery trends

## Phase 4: Analytics

Status: started.

- Export or query structured recovery/training data
- Build first local dashboard
- Map source ownership and data health for dashboard fields
- Compute basic readiness state and confidence
- Build a standalone transparent readiness baseline using daily features, personal baselines, data quality, and report output
- Import Apple Watch workout duration, workout type, and daily active energy as training-output context
- Compare readiness model calls with actual movement output in the dashboard
- Build a dashboard V2 payload that combines readiness, weekly volume, recent session detail, review warnings, and progression signals
- Analyze recovery and training trends
- Compare subjective recovery with performance outputs
- Identify useful weekly review metrics

Current implementation note: Coach Dashboard V1 now exists as a local FastAPI/SQLite + Next.js app in the foundation repo. It is a working dashboard foundation, not a finished analytics product. The first standalone readiness-modeling layer has landed as a transparent V0 baseline, and the dashboard now has Apple Watch movement-output context for Readiness vs Actual review. Structured lifting and dashboard V2 data shaping remain active local integration work, not public release claims yet.

## Phase 5: Movement Quality Prototype

Status: planned.

- Build a simple IMU joint angle tracker
- Log movement data
- Estimate range of motion and rep timing
- Explore tempo consistency and fatigue drift
- Evaluate a VBT-inspired output test, such as bar speed or a controlled jump/pod protocol, as an intermediate performance signal
- Compare movement-quality features across sessions

## Phase 6: Closed-Loop Feedback

Status: future.

- Convert analysis into recommendations or cues
- Test simple interventions
- Explore sensor-driven feedback
- Evaluate whether the feedback improves adherence, recovery, or movement quality

## Active Repositories

- [haleyparks329/human-model](https://github.com/haleyparks329/human-model)
- [haleyparks329/human-model-chatbot](https://github.com/haleyparks329/human-model-chatbot)
- [haleyparks329/the-human-model-overview](https://github.com/haleyparks329/the-human-model-overview)

## Near-Term Next Steps

- Keep the morning recovery loop stable in daily use.
- Finish and commit the structured lifting and dashboard V2 integration after local verification.
- Finish committing and verifying the chatbot readiness writeback path.
- Use Coach Dashboard V1 and the baseline modeling layer against real recovery/training rows, then tighten data freshness and calibration states.
- Resolve Notion Weekly Review access or keep that dashboard section visibly blocked.
- Decide whether the next prototype should be VBT-inspired output testing, IMU movement sensing, or dashboard analytics hardening.
- Keep public docs current as implementation changes land.
