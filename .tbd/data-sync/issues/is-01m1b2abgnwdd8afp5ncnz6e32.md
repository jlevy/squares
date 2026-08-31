---
type: is
id: is-01m1b2abgnwdd8afp5ncnz6e32
title: "Lane B0: reprice chunk-level enumeration with the measured orbit quotient and realizability prefilter"
kind: task
status: closed
priority: 1
version: 6
spec_path: packing/campaign/explorations/X-010-two-lanes-two-ladders.md
labels:
  - x-010
  - lane-b
dependencies:
  - type: blocks
    target: is-01m1b2ac6fw0dw674sd1tz5q7q
  - type: blocks
    target: is-01m0ye766eey2pvt86f8vj85zz
created_at: 2026-08-31T04:47:52.341Z
updated_at: 2026-08-31T06:21:45.648Z
closed_at: 2026-08-31T06:21:45.648Z
close_reason: "BC-095 and BC-096 discharged by session-051. The stage-1 price exists as devtools/price_stage1_chunks.py (counted 4.357e20 raw at K<=6, orbit floor 2.763e18; K<=3 slice 2.25e6 orbit floor; prefilter 0.457 measured on 300 size-5 scaffolds; transfer ASSUMED and named): exhaustive enumeration is out of reach above K<=3, Trump's decomposition outside the exhaustive range. Exact LP at Trump's full cell measured first-hand: 0.41s assembly, 58.8s/42-pivot phase 1, 22.1s/16-pivot phase 2, published side exact; float-seeded ~2.6s -- so sweep in float, certify winners exactly."
resolution: null
duplicate_of: null
---
BC-092 was stopped on '9.3e9 raw orbit work at n=5', a figure tracing to no artifact (D-405). Recorded: 1,533,696 size-five coloring candidates collapse to 11,013 orbits (139x quotient); contact_realization's prefilter is unpriced; MAX_SCAFFOLD_SIZE=5 is a typed cap, not a wall. Reprice X-003 stage-1 at the chunk level (k<=5 assemblies over ~11 squares, 8^C(5,2)~1e9 raw) in counted LP solves (D-126), with an orbit count and an omission-control design, and state what lifting the size cap costs. Exit: a measured go/no-go for reopening stage-1 (think-sfzh), replacing the impression the stop rests on. X-010 Lane B rung 0.

## Notes

agenda-010 BC-095 (block 2 first).
