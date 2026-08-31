---
type: is
id: is-01m1b2abvgsqg0hf4vxevc5z28
title: "Lane B gate: measure exact-LP cost at the n=11 cell scale"
kind: task
status: open
priority: 2
version: 3
spec_path: packing/campaign/explorations/X-010-two-lanes-two-ladders.md
labels:
  - x-010
  - lane-b
dependencies:
  - type: blocks
    target: is-01m1b2ac6fw0dw674sd1tz5q7q
created_at: 2026-08-31T04:47:52.687Z
updated_at: 2026-08-31T05:14:45.710Z
---
sqpack.exact_lp decides a cell without tolerance (the D-021 fix) with its own phase-1 feasibility, tested at promote scale. The restricted-class peak needs it at Trump's full cell, where T-2's float LP is 1.28 ms over 55 pairs; the exact pivot cost there is unmeasured. One afternoon: exact solve plus certificate check, wall time and pivot count, Fraction vs FieldElement coefficients, on the exact Trump cell. Decides whether Lane B5 certifies strata by exact LP directly or through the interval route. X-010 Lane B gate.

## Notes

agenda-010 BC-096 (block 2 second).
