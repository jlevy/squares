---
type: is
id: is-01m4mnp6h19cg6k4wphp11h83z
title: "PR #496 G2: browser floor does not claim packages/workbench JSON fixtures"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mneswbxt0m4w1caxy0x320
hold: null
hold_until: null
created_at: 2026-10-11T05:06:38.753Z
updated_at: 2026-10-11T05:06:54.438Z
started_at: 2026-10-11T05:06:54.432Z
---
Medium. packing/src/sqpack/cli/validate.py:4195-4212. node:test reads packages/workbench/tests/fixtures/*.json and design-allowlist.json; biome.json formats packages/workbench/**/*.json. Fix: claim packages/workbench/*.json; extend test_browser_floor_inputs_select_the_browser_floor with corpus.json and design-allowlist.json. PR #496, review G: https://github.com/jlevy/squares/pull/496#pullrequestreview-5481975880
