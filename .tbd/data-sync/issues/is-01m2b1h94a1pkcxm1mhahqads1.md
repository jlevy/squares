---
type: is
id: is-01m2b1h94a1pkcxm1mhahqads1
title: Require interpretable CPU and RSS evidence in completed calibration profiles
kind: bug
status: closed
priority: 1
version: 10
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol xhigh implementation or source-distinct review; root integration
labels:
  - n11
  - calibration
dependencies:
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
  - type: blocks
    target: is-01m2b4yfx3th5wcdaw9apr0vn5
parent_id: is-01m2app5e71qnp9z5vfp9vppbp
created_at: 2026-09-12T14:49:52.521Z
updated_at: 2026-09-12T16:31:20.126Z
closed_at: 2026-09-12T16:31:20.126Z
close_reason: Astra Max source-distinct correction review at exact head b6260970 accepts CAL-2, CAL-3, CAL-4, and CAL-6. The review independently checked the repairs and representative regression sensitivity; 176 target-free tests passed with one environment-dependent test explicitly deselected, and Ruff passed. The distinct CAL-5 staging-acquisition signal window remains open. No full-shape profile or BC329 target ran.
resolution: null
duplicate_of: null
---
CAL-6 from the Astra Max source-distinct review. Completed calibration records may omit all CPU observations and pass with one preflight RSS sample, while the baseline and end observations needed to interpret differences are not retained. Define and enforce terminal CPU and minimum RSS coverage, retain the observation scope and missing intervals, validate ordering against invocation lifetime, and preserve the stated sampling and shared-page limits. This is operational admission evidence only and cannot bound BC329 search time.

## Notes

Implementation correction is retained at 0533ebaeb90cf42acf20e0029535356282a5624c. RSS summaries now reconstruct and byte-bind positive_sample_count, where a positive sample is error-free with a nonempty PID set and positive RSS. Terminal admission requires at least two positive samples; one-positive plus zero is refused, two positives pass, and a forged count is refused. Author validation: combined suites 177 passed in 18.07s; repository-wide Ruff and BasedPyright clean; edit tier passed in 50.83s. No full profile or BC329 target ran. Leave open for source-distinct re-review.
