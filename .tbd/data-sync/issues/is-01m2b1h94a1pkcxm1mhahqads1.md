---
type: is
id: is-01m2b1h94a1pkcxm1mhahqads1
title: Require interpretable CPU and RSS evidence in completed calibration profiles
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
dependencies:
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
parent_id: is-01m2app5e71qnp9z5vfp9vppbp
created_at: 2026-09-12T14:49:52.521Z
updated_at: 2026-09-12T14:50:20.251Z
---
CAL-6 from the Astra Max source-distinct review. Completed calibration records may omit all CPU observations and pass with one preflight RSS sample, while the baseline and end observations needed to interpret differences are not retained. Define and enforce terminal CPU and minimum RSS coverage, retain the observation scope and missing intervals, validate ordering against invocation lifetime, and preserve the stated sampling and shared-page limits. This is operational admission evidence only and cannot bound BC329 search time.
