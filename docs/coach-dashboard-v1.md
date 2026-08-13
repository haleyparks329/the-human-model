# Coach Dashboard V1

**Status: historical prototype.** Coach Dashboard V1 was an early local review surface for recovery, training, body, signal, and review data. It helped expose useful interaction patterns, but it is not the current canonical architecture or a public production product.

## What the prototype explored

- A compact daily overview with visible missing-data state.
- Recovery and training views that kept source context near derived output.
- Body and signal pages for longitudinal review.
- Review queues for warnings, parse uncertainty, and corrections.
- Separation between raw observations and interpreted recommendations.

## Historical screenshots

- [Overview](../assets/screenshots/coach-dashboard-01-overview.png)
- [Recovery](../assets/screenshots/coach-dashboard-02-recovery.png)
- [Training output](../assets/screenshots/coach-dashboard-03-training-output.png)
- [Training log](../assets/screenshots/coach-dashboard-04-training-log.png)
- [Body](../assets/screenshots/coach-dashboard-05-body.png)
- [Signals](../assets/screenshots/coach-dashboard-06-signals.png)
- [Reviews](../assets/screenshots/coach-dashboard-07-reviews.png)

The images contain previously approved, sanitized captures. Their inclusion preserves design lineage; it does not establish that the UI, fields, or calculations remain current.

## Current lesson

A review surface is a projection over owned state, not the owner of that state. Coach can interpret performance evidence and produce proposals. Accepted human-domain changes belong in the Human Model and require an explicit application path.
