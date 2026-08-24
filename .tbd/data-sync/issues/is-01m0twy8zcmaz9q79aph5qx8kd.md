---
type: is
id: is-01m0twy8zcmaz9q79aph5qx8kd
title: Stabilize n4 and n10 fixed-cell acceptance without weakening the screen
kind: bug
status: in_progress
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - correctness
  - solver-boundary
dependencies: []
parent_id: is-01m0t4phe1905yy2jk7czp1391
created_at: 2026-08-24T22:06:02.731Z
updated_at: 2026-08-24T22:10:20.230Z
---
Narrow D-162 implementation slice. The post-exp-036 strict gate and an isolated one-worker rerun reproduce typed postcheck_rejection outcomes: n=4 finishes only 3/4 converged, and n=10 rejects pair row 61 at residual 1.503e-10 after the one complete-offending-set repair. This is not a wall deadline, so a D-126 work-budget patch alone cannot close it. Capture the first and repaired LP receipts, identify whether a new row becomes offending or the same row remains outside, and implement a deterministic conservative solve/postprocess that replays every original row. Acceptance: n=4 and n=10 known-answer paths reproduce across pool widths 1 and 10, all residuals are <=1e-10, no tolerance or committed golden is weakened, solver calls remain finitely capped, and failure stays typed if the cap is exhausted.

## Notes

2026-08-24 bounded implementation loop: 10 minutes to expose first-versus-repaired residual evidence; at most 20 additional minutes for a deterministic conservative correction only if the receipt supports it. No deep-golden retry, tolerance change, or golden rewrite before a focused fixture passes.
