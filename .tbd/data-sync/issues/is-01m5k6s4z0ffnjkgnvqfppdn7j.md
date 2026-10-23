---
type: is
id: is-01m5k6s4z0ffnjkgnvqfppdn7j
title: Keep navigation active after same-document result aliases
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: frontier-split
labels: []
dependencies: []
parent_id: is-01m5k60tb3vcvhr0ezjwphzz0s
hold: null
hold_until: null
created_at: 2026-10-23T01:42:34.207Z
updated_at: 2026-10-23T01:42:50.907Z
started_at: 2026-10-23T01:42:50.889Z
---
Legacy Recent Results section aliases now map to results.html#all-results in the same document; continue navigation initialization after this fragment change so Results and Learn menus remain wired. Cover legacy alias arrival followed by opening both menus in Chromium.
