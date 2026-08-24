---
type: is
id: is-01m0twy8zcmaz9q79aph5qx8kd
title: Stabilize n4 and n10 fixed-cell acceptance without weakening the screen
kind: bug
status: in_progress
priority: 0
version: 5
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
updated_at: 2026-08-24T22:30:28.283Z
---
Narrow D-162 implementation slice. The post-exp-036 strict gate and an isolated one-worker rerun reproduce typed postcheck_rejection outcomes: n=4 finishes only 3/4 converged, and n=10 rejects pair row 61 at residual 1.503e-10 after the one complete-offending-set repair. This is not a wall deadline, so a D-126 work-budget patch alone cannot close it. Capture the first and repaired LP receipts, identify whether a new row becomes offending or the same row remains outside, and implement a deterministic conservative solve/postprocess that replays every original row. Acceptance: n=4 and n=10 known-answer paths reproduce across pool widths 1 and 10, all residuals are <=1e-10, no tolerance or committed golden is weakened, solver calls remain finitely capped, and failure stays typed if the cap is exhausted.

## Notes

2026-08-24 bounded implementation result: the retained n=10 cell moves from first-call offenders 49/66 (about 7.26e-10) to new row 61 (1.503e-10), then settles with zero all-original-row residual on solver call 3. PACK_JOBS=10 deep replay finishes in 23.94s and PACK_JOBS=1 in 79.66s; all seven ladder rungs, including n=10, converge at both widths. The overall golden still fails identically at n=4 (3/4 converged, extra valid side-2.0205018999 row). A 13.70s four-seed diagnostic isolates seed 0 as typed HiGHS status-4 Solve error, not postcheck rejection; the new n4 child owns it. D-199 can close as a defect, but this combined bead stays open until the n4 child is resolved.
