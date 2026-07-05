# Source Context

This overview was synthesized from active project repositories, GitHub commit history, and private Notion planning pages available during setup.

The public overview is designed to stand on its own even when implementation details depend on private Notion databases or local health/training data.

## Notion Pages Reviewed

- The Human Model overview
- Evolution of the Idea
- Long-Term Expansion Path
- Next Sprint: Recovery Tracking V1
- Next Sprint: Recovery Loop Review V1
- Coach Dashboard V1
- Product Research
- Competitive Teardown
- VBT Product Research
- Live Project Log updates titled "Movement Quality Enters the Dashboard" and "Bridget Gets a Modular Spine"
- Tone and Identity guidance for public Human Model voice and confidence calibration
- Current Systems pages for Bridget and Predictive Models
- Live Project Log updates titled "Bridget Can Use Training Predictions" and "Workout Sheets Become Editable"

## Repositories Reviewed

- [haleyparks329/human-model](https://github.com/haleyparks329/human-model)
- [haleyparks329/human-model-chatbot](https://github.com/haleyparks329/human-model-chatbot)
- [haleyparks329/the-human-model-overview](https://github.com/haleyparks329/the-human-model-overview)

## Implementation Commits Reviewed

Main repo:

- `776f507c` - Add project README
- `d2066aa5` - Add Recovery Tracking V1 schema
- `c934b6a5` - Add weekly review template
- `bbdf6619` - Document chatbot logging contract
- `59523704` - Add local coach dashboard app
- `a6bf60d7` - Add standalone readiness model dashboard
- `fd259d2d` - Add readiness vs training output review
- `f13993f2` - Add local MediaPipe form analysis pipeline
- `ce2d810e` - Add movement quality dashboard
- `97490d3f` - Add set-role V2 training load reports
- `c56319f8` - Add guarded next-session recommendations

Chatbot repo:

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
- `7543262` - Add Bridget workout recommendation ledger
- `0101607` - Add modular Human Model pipeline foundation
- `0a1aee7` - Wire workout file exchange into Telegram
- `49d5cbc` - Document pipeline boundaries and future matching
- `e69d547` - Add Bridget V2 training recommendations
- `6cf6467` - Import generated workout sheets

Foundation work reviewed on 2026-06-23:

- Apple Watch workout and active-energy import path for training-output context
- Training output dashboard view connecting readiness calls, watch movement output, and recent alignment labels
- Additional modeling feature/report updates around readiness quality and daily output review

Additional work reviewed on 2026-06-28:

- Local MediaPipe movement-quality pipeline and dashboard page for RDL review
- Bridget modularization across app, integration, pipeline, and storage boundaries
- Telegram workout file exchange and future matching boundaries

Additional work reviewed on 2026-07-02:

- Training-load model V2 reports using set-role features
- Guarded next-session recommendations that preserve warmup/feeder logic, progression floors, and set ordering
- Bridget pre-gym recommendation flow with editable workout sheets and separate model/debug prediction files
- Public Tone and Identity guidance emphasizing confidence without exaggeration

Additional local diffs reviewed on 2026-07-05:

- Training prediction generation preserving raw exercise order so generated sheets can follow the planned workout instead of model output order alone
- Bridget workout-sheet parsing preserving suggested reps and text-only load notes, such as machine-weight rows
- Workout-sheet import tests covering ordered exercises, retained non-modelable rows, and separate actual-vs-recommended fields

## Public/Private Boundary

This repo should stay public-facing. It can describe:

- System architecture
- Project vision
- Implementation progress
- Schemas and contracts
- General workflows
- Future roadmap

It should not include:

- Personal health records
- Private Notion database exports
- Telegram tokens, Notion tokens, or local `.env` values
- Raw screenshots from Zenfit or Apple Health exports
