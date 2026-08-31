---
type: is
id: is-01m108eembwpb78c4h26kb7b43
title: Reduce PR 45 known-best census validation latency
kind: task
status: closed
priority: 0
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
delegate: codex@spud10.local
labels:
  - packing
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
hold: null
hold_until: null
created_at: 2026-08-27T00:03:19.297Z
updated_at: 2026-08-27T01:32:22.761Z
started_at: 2026-08-27T00:03:27.642Z
closed_at: 2026-08-27T01:32:22.760Z
close_reason: The five-command atlas improved from 743.07s to 123.93s (6.00x) with exact differential/oracle controls; clean strict completed in 372.24s and final-head Linux/macOS CI are green.
resolution: null
duplicate_of: null
---
Profile and remove repeated bounded-partition computation introduced by PR 45. The first strict receipt spent 743.07 seconds in the known-best n=1..100 atlas step and 1,589.65 seconds total. Acceptance: preserve the exact 3/2/23/8 calibration distribution, per-n certificates, typed cap/minimality semantics, candidate universe, deterministic artifacts, and no-geometry/no-feasibility boundaries; add equivalence and invalidation controls; reduce a clean census check by at least 5x or document the next measured bottleneck; keep strict complete and fail-closed.
