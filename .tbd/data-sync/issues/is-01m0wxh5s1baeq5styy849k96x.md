---
type: is
id: is-01m0wxh5s1baeq5styy849k96x
title: Fix incomplete Kingbird evidence replay commands
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - packing
  - docs
  - assurance
dependencies: []
parent_id: is-01m0wqx97nb22qwx8v47hrpfqk
created_at: 2026-08-25T16:54:50.912Z
updated_at: 2026-08-25T17:02:09.434Z
closed_at: 2026-08-25T17:02:09.433Z
close_reason: Added explicit retained-SVG arguments to both durable Kingbird evidence replays and the plan example, updated the behavioral fixture, added a semantic source-input guard, and passed the focused checks plus the full 32-surface gate.
resolution: null
duplicate_of: null
---
The durable frontier evidence records and assurance-plan example invoke cases.kingbird29.verify_svg without its required retained SVG positional argument. The internal full gate passes because it supplies the path directly, so the reader-facing replay command is stale. Add the explicit source path, update the behavioral fixture, and add a focused guard that durable replay commands remain runnable without hard-coding volatile inventory counts.
