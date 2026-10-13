---
type: is
id: is-01m4mnfg8dk1fp4xfk8vtvxexj
title: "PR #496 E3: verify-deployment ceiling contract accepts a uselessly small ceiling"
kind: bug
status: closed
priority: 3
version: 3
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mneswbxt0m4w1caxy0x320
hold: null
hold_until: null
created_at: 2026-10-11T05:02:59.339Z
updated_at: 2026-10-12T23:38:59.853Z
started_at: 2026-10-11T05:03:46.042Z
closed_at: 2026-10-12T23:38:59.853Z
close_reason: "Fixed in PR #507 (merged 2026-10-12): test_pages_workflow pins the verify-deployment ceiling (30) and checker deadline (25) as a pair."
resolution: null
duplicate_of: null
---
Low. packing/tests/test_pages_workflow.py:819-821 accepts any ceiling in (0, 30]. Fix: pin the bounds derived for the F1 checker deadline (deadline floor from measured healthy audits; deadline plus setup margin below the job ceiling). PR #496, review E: https://github.com/jlevy/squares/pull/496#pullrequestreview-5481683586
