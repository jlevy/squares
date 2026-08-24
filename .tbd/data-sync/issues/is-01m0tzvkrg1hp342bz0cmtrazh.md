---
type: is
id: is-01m0tzvkrg1hp342bz0cmtrazh
title: "PR 24 review R11: close workflow checker and mutation blind spots"
kind: bug
status: closed
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - pr24-review
dependencies: []
parent_id: is-01m0tz8s4yps8zgqwk8cng9qnx
created_at: 2026-08-24T22:57:01.199Z
updated_at: 2026-08-24T23:24:52.659Z
closed_at: 2026-08-24T23:24:52.658Z
close_reason: "Fixed in 0775c20: extra workflow rows, volatile datelines, malformed transitions, terminal fields, status mismatches, and clock contracts are checked and mutation-controlled."
resolution: null
duplicate_of: null
---
PR #24 consistency checks accept extra W7 rows and plural/experiment freshness labels; transition mutation coverage misses later switch_reason, terminal stop_reason, final phase/session mismatch, and active clock/contract omissions. Tighten checks and add focused controls.
