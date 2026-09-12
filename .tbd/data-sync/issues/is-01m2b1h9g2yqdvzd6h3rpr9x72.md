---
type: is
id: is-01m2b1h9g2yqdvzd6h3rpr9x72
title: Bind calibration worker settings to the seeded receipt and readback
kind: bug
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol xhigh implementation or source-distinct review; root integration
labels:
  - n11
  - calibration
dependencies:
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
parent_id: is-01m2app5e71qnp9z5vfp9vppbp
created_at: 2026-09-12T14:49:52.898Z
updated_at: 2026-09-12T15:25:34.722Z
---
CAL-7 from the Astra Max source-distinct review. run_worker can execute with workers=1 while the seeded receipt declares requested_workers=4 because actual arguments are not compared with frozen settings. Bind workers, allowances, grace, origin, deadlines, run metadata, and the full invocation identity before dispatch and during independent readback. Retain worker-count and allowance-drift controls. This blocks calibration admission and all profiles.

## Notes

Repair implemented in d6bbe20172d4048a9f156b1c3c4fcfe8f1b64014. One retained invocation identity binds implementation revision, workers, calibration/external allowances, grace, monotonic origin and both deadlines, run order, cache observation, and background load across the seed, worker, supervisor, child readback, and final admission. Worker-count drift is refused before source loading or kernel dispatch, and reader identity drift is refused before artifact reconstruction. Leave open for source-distinct closure review.
