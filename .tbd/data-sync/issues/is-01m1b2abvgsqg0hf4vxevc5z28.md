---
type: is
id: is-01m1b2abvgsqg0hf4vxevc5z28
title: "Lane B gate: measure exact-LP cost at the n=11 cell scale"
kind: task
status: closed
priority: 2
version: 4
spec_path: packing/campaign/explorations/X-010-two-lanes-two-ladders.md
labels:
  - x-010
  - lane-b
dependencies:
  - type: blocks
    target: is-01m1b2ac6fw0dw674sd1tz5q7q
created_at: 2026-08-31T04:47:52.687Z
updated_at: 2026-08-31T06:21:45.658Z
closed_at: 2026-08-31T06:21:45.658Z
close_reason: "BC-095 and BC-096 discharged by session-051. The stage-1 price exists as devtools/price_stage1_chunks.py (counted 4.357e20 raw at K<=6, orbit floor 2.763e18; K<=3 slice 2.25e6 orbit floor; prefilter 0.457 measured on 300 size-5 scaffolds; transfer ASSUMED and named): exhaustive enumeration is out of reach above K<=3, Trump's decomposition outside the exhaustive range. Exact LP at Trump's full cell measured first-hand: 0.41s assembly, 58.8s/42-pivot phase 1, 22.1s/16-pivot phase 2, published side exact; float-seeded ~2.6s -- so sweep in float, certify winners exactly."
resolution: null
duplicate_of: null
---
sqpack.exact_lp decides a cell without tolerance (the D-021 fix) with its own phase-1 feasibility, tested at promote scale. The restricted-class peak needs it at Trump's full cell, where T-2's float LP is 1.28 ms over 55 pairs; the exact pivot cost there is unmeasured. One afternoon: exact solve plus certificate check, wall time and pivot count, Fraction vs FieldElement coefficients, on the exact Trump cell. Decides whether Lane B5 certifies strata by exact LP directly or through the interval route. X-010 Lane B gate.

## Notes

agenda-010 BC-096 (block 2 second).
