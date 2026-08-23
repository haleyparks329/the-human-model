# Roadmap

This roadmap follows the current ownership model: the Human Model owns canonical human-domain state, Coach produces specialized interpretations and proposals, [Bridget](https://github.com/haleyparks329/bridget-architecture) supports continuity and coordination, and [Wonderful Digital World](https://github.com/Wonderful-Digital-World/wonderful-digital-world) supplies the broader environment. It is not a promise of dates or a claim that every concept below is implemented.

Status words use the repository-wide vocabulary: **implemented**, **dogfooded**, **experimental**, **historical**, **planned**, and **rejected**.

## Now: strengthen the canonical performance model

**Current architecture, with bounded public evidence.**

- Keep source provenance, timestamps, review state, and correction history visible.
- Preserve imported plan order separately from a confirmed schedule anchor.
- Treat Coach outputs as proposals until the Human Model accepts a canonical change.
- Continue exercising resident projections without making a resident the owner of human state.
- Audit ambiguous or stale evidence rather than turning it into false certainty.

## Next: close the confirmation-to-mutation gap

**Planned.**

Confirmation is not the same as canonical mutation. The next public architectural milestone is an explicit, reviewable application pattern for supported proposal types, including failure behavior and provenance, without claiming private implementation completeness.

## Next: improve public evidence

**Planned.**

- Define small public contracts for claims, corrections, projections, and evaluations without copying private schemas.
- Add synthetic longitudinal fixtures that demonstrate contradiction, correction, staleness, and revalidation.
- Separate implemented reference code from historical interface examples more visibly.
- Reassess old screenshots and videos; retain them only when their historical value is clear.

## Later: broaden carefully

**Planned research.**

- Test whether the model generalizes beyond one performance domain and one primary user.
- Evaluate bounded confidence, decay, and revalidation rules before presenting them as general infrastructure.
- Study preference, routine, and intent learning with explicit consent and correction paths.
- Explore privacy-preserving local and shared projections for additional residents.

## Experimental directions

Movement video, IMUs, readiness scores, and other sensing or modeling ideas remain experiments. A useful experiment must identify its source, uncertainty, review path, and decision value. It does not become part of the canonical model merely because it can produce a number.

## Explicit non-goals

- A universal chatbot gateway is **rejected**.
- Silent cross-system writes are **rejected**.
- Treating a Coach recommendation as accepted human state is **rejected**.
- Inferring a real schedule from imported plan order alone is **rejected**.
- Claiming a complete digital replica of a person is **rejected**.

See the [Evidence Map](evidence-map.md) for public claim support and [Architecture](architecture.md) for ownership boundaries.
