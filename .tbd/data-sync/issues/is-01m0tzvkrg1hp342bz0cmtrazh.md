---
type: is
id: is-01m0tzvkrg1hp342bz0cmtrazh
title: "PR 24 review R11: close workflow checker and mutation blind spots"
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - pr24-review
dependencies: []
parent_id: is-01m0tz8s4yps8zgqwk8cng9qnx
created_at: 2026-08-24T22:57:01.199Z
updated_at: 2026-08-24T22:58:09.144Z
---
PR #24 consistency checks accept extra W7 rows and plural/experiment freshness labels; transition mutation coverage misses later switch_reason, terminal stop_reason, final phase/session mismatch, and active clock/contract omissions. Tighten checks and add focused controls.
