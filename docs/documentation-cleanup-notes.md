# Documentation Cleanup Notes

This file captures documentation-structure debt found during the first editorial cleanup pass. It is a planning note only; no documents were deleted or reorganized in this pass.

## Duplication Found

- `README.md`, `docs/implementation-progress.md`, `docs/architecture.md`, and `docs/roadmap.md` all describe current system status. The README now points readers to the deeper pages, but the deeper pages still repeat several implementation details.
- `docs/implementation-progress.md` and `docs/source-context.md` both maintain commit-level implementation inventories.
- `docs/vision.md` and `docs/project-evolution.md` overlap on the core thesis and long-term expansion path.
- `docs/recovery-modeling.md`, `docs/architecture.md`, and `docs/roadmap.md` all describe the readiness loop at different levels of detail.
- `docs/chatbot-telegram-evolution.md`, `docs/implementation-progress.md`, and the README all describe Bridget's current role.
- `docs/movement-analysis.md`, `docs/architecture.md`, and `docs/implementation-progress.md` all describe the MediaPipe/RDL movement-quality prototype.

## Suggested Merges

- Merge `docs/vision.md` and selected parts of `docs/project-evolution.md` into a single `docs/product-thesis.md` or `docs/vision-and-evolution.md`.
- Merge commit-level detail from `docs/source-context.md` into `docs/implementation-progress.md`, then let `source-context.md` focus on public/private boundary and evidence sources.
- Fold repeated readiness descriptions into one canonical `docs/readiness-modeling.md` page, replacing or renaming `docs/recovery-modeling.md`.
- Keep `docs/coach-dashboard-v1.md` as the screenshot-heavy dashboard page and remove duplicate dashboard inventory from other docs over time.

## Suggested Renames

- Rename `docs/recovery-modeling.md` to `docs/readiness-modeling.md` if it continues to describe the readiness decision loop rather than only recovery-data capture.
- Rename `docs/chatbot-telegram-evolution.md` to `docs/bridget.md` or `docs/bridget-evolution.md` now that Bridget is the named product surface.
- Rename `docs/implementation-progress.md` to `docs/current-status.md` if it remains the main status page.
- Rename `docs/source-context.md` to `docs/public-private-boundary.md` if commit inventories move elsewhere.
- Repository rename is complete: the public repository now lives at `haleyparks329/the-human-model`.

## Possible Archival Candidates

- Older implementation commit lists in `docs/source-context.md` may eventually move to an archive if they stop being useful for public readers.
- `experiments/` should remain, but early sketches may eventually be labeled as archived concepts versus active research directions.
- `docs/project-evolution.md` may become an archive page if the current thesis is consolidated into a shorter canonical vision page.
- Very detailed current-status bullets in `docs/implementation-progress.md` may eventually move behind dated progress notes.

## Broken Or Questionable Links

- Links to `https://github.com/haleyparks329/the-human-model` now point at the renamed public repository.
- Older references to `https://github.com/haleyparks329/the-human-model-overview` were updated in public docs where obvious, but external sites may still point to the old slug.
- The Notion portfolio link in `README.md` should be rechecked after any public Notion URL or title changes.
- Relative links in the current Markdown set were checked locally during this pass; no missing local targets were found.

## Proposed Final Documentation Structure

- `README.md`: canonical public introduction, thesis, high-level architecture, demos, and repository links.
- `docs/product-thesis.md`: why the project exists, why bodybuilding is the first test environment, broader research direction.
- `docs/architecture.md`: durable system architecture and repository boundaries.
- `docs/current-status.md`: implemented, experimental, and future work, kept concise.
- `docs/bridget.md`: Bridget as the daily conversational surface and low-friction model-acquisition layer.
- `docs/readiness-modeling.md`: recovery inputs, readiness scoring, confidence, and review discipline.
- `docs/training-load-modeling.md`: guarded next-session recommendations and editable workout sheets.
- `docs/movement-analysis.md`: MediaPipe/RDL prototype and future sensing path.
- `docs/coach-dashboard.md`: dashboard screenshots and review/audit role.
- `docs/public-private-boundary.md`: what can be public, what stays private, and source/evidence policy.
- `examples/README.md`: runnable public-safe examples with mock data.
- `experiments/README.md`: early sensing and data-pipeline sketches.
