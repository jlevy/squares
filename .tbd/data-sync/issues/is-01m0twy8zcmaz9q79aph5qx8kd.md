---
type: is
id: is-01m0twy8zcmaz9q79aph5qx8kd
title: Stabilize n4 and n10 fixed-cell acceptance without weakening the screen
kind: bug
status: in_progress
priority: 0
version: 6
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - correctness
  - solver-boundary
dependencies: []
parent_id: is-01m0t4phe1905yy2jk7czp1391
child_order_hints:
  - is-01m0tyazcycsqvm34fyxb4hdtx
  - is-01m0tyazqn3sgwvee1yfv2b3yf
created_at: 2026-08-24T22:06:02.731Z
updated_at: 2026-08-25T10:25:25.772Z
---
Narrow D-162 implementation slice. The post-exp-036 strict gate and an isolated one-worker rerun reproduce typed postcheck_rejection outcomes: n=4 finishes only 3/4 converged, and n=10 rejects pair row 61 at residual 1.503e-10 after the one complete-offending-set repair. This is not a wall deadline, so a D-126 work-budget patch alone cannot close it. Capture the first and repaired LP receipts, identify whether a new row becomes offending or the same row remains outside, and implement a deterministic conservative solve/postprocess that replays every original row. Acceptance: n=4 and n=10 known-answer paths reproduce across pool widths 1 and 10, all residuals are <=1e-10, no tolerance or committed golden is weakened, solver calls remain finitely capped, and failure stays typed if the cap is exhausted.

## Notes

2026-08-24: cumulative all-row residual repair restored n=10 across PACK_JOBS=10 and PACK_JOBS=1, while n=4 remained 3/4 and seed 0 isolated a HiGHS status-4 solve error. 2026-08-25: D-203 is now fixed by the identical-LP status-4-only strict-IPM fallback. The bounded seed-0 replay reaches proved side 2 with 3,692/3,692 fixed points settled, and the direct blocking macOS deep golden reaches n=4 at 4/4; both PR jobs pass at b582fe1. This combined bead remains open because its acceptance requires controlled n=4 and n=10 known-answer receipts across pool widths 1 and 10; the repaired n=4 path has not been rerun at both widths in one post-fix comparison.
