---
type: is
id: is-01m0y081bfavkgmmjsq9qx6aeq
title: Tier packing CI into fast Linux and selected macOS lanes
kind: feature
status: in_progress
priority: 0
version: 7
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
updated_at: 2026-08-26T07:26:37.442Z
---
Shorten the required packing pull-request signal while retaining complete assurance at declared integration boundaries. Acceptance: a required Linux fast lane publishes structured timing; the optimized full Linux lane remains visible and required at the integration boundary and on main; macOS runs named portability consumers on main, scheduled, manual, and explicit portability-sensitive triggers instead of duplicating the full gate on every unrelated PR; every invoked macOS check remains direct and blocking; workflow-contract tests cover triggers, commands, artifacts, and failure semantics; before/after p50 and p95 are retained.

## Notes

Spike think-b784 landed in PR 41 commit ccc1bb5. Hosted run 32941767003: 46s end-to-end, validate 37s, required step 24s, aggregator 2s, macOS skipped. Versus prior validate 5m10s and macOS tail 10m01s: 88.1% and 92.3% reductions. First sample meets <=60s; remaining fixed-surface p50/p95 sample stays open here.
