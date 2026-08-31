---
type: is
id: is-01m0w4xmf6zpvw01t897n8f49y
title: Keep status4-to-status2 disagreement numerical
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - soundness
  - solver-boundary
dependencies: []
parent_id: is-01m0tyazcycsqvm34fyxb4hdtx
created_at: 2026-08-25T09:44:44.762Z
updated_at: 2026-08-25T09:46:40.185Z
closed_at: 2026-08-25T09:46:40.184Z
close_reason: "D-266 fixed before commit: only a sole primary status2 is infeasible; primary status4 followed by IPM status2 remains solver_failure with both indexed receipts. Deterministic controls cover both classifications and identical fallback inputs."
resolution: null
duplicate_of: null
---
The first D-203 fallback draft classified primary highs status4 followed by highs-ipm status2 as mathematical infeasibility. That solver disagreement follows a numerical failure and cannot establish infeasibility. Return solver_failure with both attempts; classify status2 as infeasible only when it is the sole primary attempt; add deterministic status4-to-status2 and identical-input controls.
