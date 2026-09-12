---
type: is
id: is-01m2b1h94a1pkcxm1mhahqads1
title: Require interpretable CPU and RSS evidence in completed calibration profiles
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
created_at: 2026-09-12T14:49:52.521Z
updated_at: 2026-09-12T15:25:34.345Z
---
CAL-6 from the Astra Max source-distinct review. Completed calibration records may omit all CPU observations and pass with one preflight RSS sample, while the baseline and end observations needed to interpret differences are not retained. Define and enforce terminal CPU and minimum RSS coverage, retain the observation scope and missing intervals, validate ordering against invocation lifetime, and preserve the stated sampling and shared-page limits. This is operational admission evidence only and cannot bound BC329 search time.

## Notes

Repair implemented in d6bbe20172d4048a9f156b1c3c4fcfe8f1b64014. Terminal admission requires finite CPU differences reconstructed from retained coordinator/direct-child start and end observations plus at least two positive, error-free RSS samples. RSS records now retain observation lifetime, actual gaps, observed/missing phases, and leading/trailing unobserved intervals; ordering and lifetime relationships are validated. The scope still excludes parent readback CPU and labels shared-page and missed-peak limits honestly. Leave open for source-distinct closure review.
