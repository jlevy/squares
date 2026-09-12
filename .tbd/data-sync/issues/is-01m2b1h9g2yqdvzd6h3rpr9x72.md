---
type: is
id: is-01m2b1h9g2yqdvzd6h3rpr9x72
title: Bind calibration worker settings to the seeded receipt and readback
kind: bug
status: closed
priority: 1
version: 7
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
updated_at: 2026-09-12T15:49:30.708Z
closed_at: 2026-09-12T15:49:30.708Z
close_reason: Source-distinct integrated review at d924a4bf accepted the original CAL-1 terminal-route repair and CAL-7 invocation-identity repair; retained review records exact scope and no scientific target ran.
resolution: null
duplicate_of: null
---
CAL-7 from the Astra Max source-distinct review. run_worker can execute with workers=1 while the seeded receipt declares requested_workers=4 because actual arguments are not compared with frozen settings. Bind workers, allowances, grace, origin, deadlines, run metadata, and the full invocation identity before dispatch and during independent readback. Retain worker-count and allowance-drift controls. This blocks calibration admission and all profiles.

## Notes

Source-distinct integrated review at `d924a4bf` accepted the original CAL-7 repair. The invocation identity binds the worker count, both allowances, grace, monotonic origin and deadlines, run order, cache note, and background-load note before source work and again at terminal readback. Review: `/private/tmp/bc329-calibration-integrated-correction-review.md`. This closes CAL-7 only; no positive full-shape profile or BC329 target ran.
