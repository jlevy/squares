---
type: is
id: is-01m0y081bfavkgmmjsq9qx6aeq
title: Tier packing CI into fast Linux and selected macOS lanes
kind: feature
status: open
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
labels:
  - packing
  - focus-efficiency
  - performance
dependencies:
  - type: blocks
    target: is-01m0y083cqkdjbbzfjxc5j7wpd
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-26T03:01:31.629Z
updated_at: 2026-08-26T03:01:55.347Z
---
Shorten the required packing pull-request signal while retaining complete assurance at declared integration boundaries. Acceptance: a required Linux fast lane publishes structured timing; the optimized full Linux lane remains visible and required at the integration boundary and on main; macOS runs named portability consumers on main, scheduled, manual, and explicit portability-sensitive triggers instead of duplicating the full gate on every unrelated PR; every invoked macOS check remains direct and blocking; workflow-contract tests cover triggers, commands, artifacts, and failure semantics; before/after p50 and p95 are retained.
