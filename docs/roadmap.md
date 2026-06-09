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

Status: partially implemented.

- Import Zenfit screenshots through OCR
- Write workouts to Notion Training Log
- Write weekly coach check-ins to Notion
- Write progress/body measurement screenshots to Notion
- Log workout summaries through Telegram
- Improve date handling for delayed screenshot imports
- Compare training context against recovery trends

## Phase 4: Analytics

Status: planned.

- Export or query structured recovery/training data
- Analyze recovery and training trends
- Build first dashboard
- Compare subjective recovery with performance outputs
- Identify useful weekly review metrics

## Phase 5: Movement Quality Prototype

Status: planned.

- Build a simple IMU joint angle tracker
- Log movement data
- Estimate range of motion and rep timing
- Explore tempo consistency and fatigue drift
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
- Review a week of recovery entries against training context.
- Decide whether the next automation target should be dashboarding, better Zenfit date handling, or the first movement-quality sensor prototype.
- Keep public docs current as implementation changes land.
