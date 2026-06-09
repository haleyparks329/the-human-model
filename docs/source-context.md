# Source Context

This overview was synthesized from active project repositories, GitHub commit history, Codex chat summaries, and private Notion planning pages available during setup.

Some links may require access. The public overview is designed to stand on its own even when implementation details depend on private Notion databases or local health/training data.

## Notion Pages Reviewed

- [The Human Model Notion overview](https://www.notion.so/350cf4d8ba18802db664cb170a45248a)
- [Evolution of the Idea](https://app.notion.com/p/37acf4d8ba1881b1a5c3c0a56e9262b2)
- [Long-Term Expansion Path](https://app.notion.com/p/37acf4d8ba18817ab88ac9307f00aade)
- [Next Sprint: Recovery Tracking V1](https://www.notion.so/35ecf4d8ba1881cc8b52f397187ded25)
- [Next Sprint: Recovery Loop Review V1](https://app.notion.com/p/367cf4d8ba18810fa13dd79471d333fd)

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

Chatbot repo:

- `fb3689a` - Add recovery check-in logging
- `d3a4e68` - Add Zenfit screenshot importer with Notion sync
- `ada76a8` - Add Apple Health import and daily morning Telegram check-in
- `9d7097a` - Fix morning check-ins and Zenfit parsing
- `275d65a` - Run morning check-in via launchd one-shot
- `68700a8` - Handle morning sleep data edge cases
- `f286eeb` - Add Telegram workout logging

## Codex Chats Reviewed

- Planning next Human Model steps
- Fixing chatbot schedule and Apple Health references
- Handling Apple Health sleep edge cases
- Investigating Zenfit sync/import behavior
- Adding the idea evolution and long-term expansion framing

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
