---
type: is
id: is-01m5k6s4z0ffnjkgnvqfppdn7j
title: Keep navigation active after same-document result aliases
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: frontier-split
labels: []
dependencies: []
parent_id: is-01m5k60tb3vcvhr0ezjwphzz0s
hold: null
hold_until: null
created_at: 2026-10-23T01:42:34.207Z
updated_at: 2026-10-23T01:46:13.580Z
started_at: 2026-10-23T01:42:50.889Z
closed_at: 2026-10-23T01:46:13.578Z
close_reason: "Fixed same-document result-section aliases without skipping navigation initialization in coordinator-pushed acba0b245 on PR #737. Chromium regression reproduced the Results-menu failure before the fix (1 failed in 42.77s) and passed afterward (1 passed in 38.64s), covering Results and Learn menus after Recent Results forwards to All Results. Biome and focused Ruff passed; senior rereview accepted the fix."
resolution: null
duplicate_of: null
---
Legacy Recent Results section aliases now map to results.html#all-results in the same document; continue navigation initialization after this fragment change so Results and Learn menus remain wired. Cover legacy alias arrival followed by opening both menus in Chromium.
