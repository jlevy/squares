---
type: is
id: is-01m0y081bfavkgmmjsq9qx6aeq
title: Tier packing CI into fast Linux and selected macOS lanes
kind: feature
status: in_progress
priority: 0
version: 6
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
labels:
  - packing
  - focus-efficiency
  - performance
dependencies:
  - type: blocks
    target: is-01m0y083cqkdjbbzfjxc5j7wpd
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
child_order_hints:
  - is-01m0ycwz9g10ckxpgghd62z2qf
created_at: 2026-08-26T03:01:31.629Z
updated_at: 2026-08-26T06:42:51.494Z
---
Shorten the required packing pull-request signal while retaining complete assurance at declared integration boundaries. Acceptance: a required Linux fast lane publishes structured timing; the optimized full Linux lane remains visible and required at the integration boundary and on main; macOS runs named portability consumers on main, scheduled, manual, and explicit portability-sensitive triggers instead of duplicating the full gate on every unrelated PR; every invoked macOS check remains direct and blocking; workflow-contract tests cover triggers, commands, artifacts, and failure semantics; before/after p50 and p95 are retained.

## Notes

2026-08-26 baseline: latest 24 successful workflows p50 346s/p95 430s; PR run 32926510669 is Linux 378s and macOS 436s. Fresh terminal PR 41 run 32934785896 is Linux validate 5m10s and macOS portability 10m01s, so macOS determined the tail but Linux independently exceeded the one-minute target by 5.2x. Implement stable packing-required aggregator. Immediate required lane excludes only checked-in exhaustive_exact nodes and monolithic controls while retaining all assurance on integration/main/schedule/manual. Steady state: 1 core + 6 exact + 4 control + 4 validator jobs, each <=45s work; prove exact union/no duplicates; accept after ten fixed-SHA runs at <=60s p50 and <=75s p95.
