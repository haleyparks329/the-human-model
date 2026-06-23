# Source Context

This overview was synthesized from active project repositories, GitHub commit history, Codex chat summaries, and private Notion planning pages available during setup.

Some links may require access. The public overview is designed to stand on its own even when implementation details depend on private Notion databases or local health/training data.

## Notion Pages Reviewed

- [The Human Model Notion overview](https://www.notion.so/350cf4d8ba18802db664cb170a45248a)
- [Evolution of the Idea](https://app.notion.com/p/37acf4d8ba1881b1a5c3c0a56e9262b2)
- [Long-Term Expansion Path](https://app.notion.com/p/37acf4d8ba18817ab88ac9307f00aade)
- [Next Sprint: Recovery Tracking V1](https://www.notion.so/35ecf4d8ba1881cc8b52f397187ded25)
- [Next Sprint: Recovery Loop Review V1](https://app.notion.com/p/367cf4d8ba18810fa13dd79471d333fd)
- [Coach Dashboard V1](https://app.notion.com/p/37bcf4d8ba1881d28a0bc7658ccdcbe3)
- [Product Research](https://app.notion.com/p/37bcf4d8ba1880d0be52c355b2947695)
- [Competitive Teardown](https://app.notion.com/p/37bcf4d8ba1880daba34d201c8a62181)
- [VBT Product Research](https://app.notion.com/p/37dcf4d8ba188170a1b6ec3b4ada0465)

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

Local uncommitted chatbot work reviewed on 2026-06-14:

- `readiness.py` readiness computation and Notion schema setup
- Telegram and Apple Health hooks that refresh readiness after new recovery data
- Tests for readiness scoring, data confidence, low-sleep caps, bad-mood rest calls, and coach override behavior

Foundation work reviewed on 2026-06-23:

- Apple Watch workout and active-energy import path for training-output context
- Training output dashboard view connecting readiness calls, watch movement output, and recent alignment labels
- Additional modeling feature/report updates around readiness quality and daily output review

## Codex Chats Reviewed

- Planning next Human Model steps
- Fixing chatbot schedule and Apple Health references
- Handling Apple Health sleep edge cases
- Investigating Zenfit sync/import behavior
- Adding the idea evolution and long-term expansion framing
- Planning Coach Dashboard V1
- Capturing Human Model research logs around local dashboard direction, product positioning, VBT/product research, copy-forward workout logging, readiness writeback, and the local dashboard app
- Syncing chatbot workout parsing with the training plan

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
