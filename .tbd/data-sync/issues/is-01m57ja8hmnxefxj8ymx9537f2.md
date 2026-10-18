---
type: is
id: is-01m57ja8hmnxefxj8ymx9537f2
title: "PR #665 A3: reconcile adoption regression fixtures"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m57j9xsga57szgfah5ex2bcd
hold: null
hold_until: null
created_at: 2026-10-18T13:13:16.083Z
updated_at: 2026-10-18T13:13:25.542Z
started_at: 2026-10-18T13:13:25.542Z
---
Medium; review A https://github.com/jlevy/squares/pull/665#pullrequestreview-5562201404. tests/test_house_adoption.py:80,93,162 and poster, announcement, recent-result, grid-slack, frontier-draft and chunk-taxonomy fixtures retain displaced house assumptions. Use retained old records for old-packing behavior; update current-record expectations and replay closed-form writer in required order.
