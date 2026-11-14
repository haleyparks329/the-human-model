# Coach Dashboard V1

**Status: historical prototype.** Coach Dashboard V1 was an early local review surface for recovery, training, body, signal, and review data. It helped expose useful interaction patterns, but it is not the current canonical architecture or a public production product.

## What the prototype explored

- A compact daily overview with visible missing-data state.
- Recovery and training views that kept source context near derived output.
- Body and signal pages for longitudinal review.
- Review queues for warnings, parse uncertainty, and corrections.
- Separation between raw observations and interpreted recommendations.

## Current lesson

A review surface is a projection over owned state, not the owner of that state. Coach can interpret performance evidence and produce proposals. Accepted human-domain changes belong in the Human Model and require an explicit application path.
