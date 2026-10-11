---
type: is
id: is-01m4mnp7npptywfbvfh2cq0fdv
title: "PR #496 G4: --push banner does not name the unclaimed paths"
kind: bug
status: in_progress
priority: 3
version: 2
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mneswbxt0m4w1caxy0x320
hold: null
hold_until: null
created_at: 2026-10-11T05:06:39.925Z
updated_at: 2026-10-11T05:06:57.055Z
started_at: 2026-10-11T05:06:57.052Z
---
Suggestion. packing/src/sqpack/cli/validate.py:7442-7449 vs :7475-7482. Fix: one helper names the first unclaimed paths for both the --push and --since blocks and applies E1's stdout/stderr choice. PR #496, review G: https://github.com/jlevy/squares/pull/496#pullrequestreview-5481975880
