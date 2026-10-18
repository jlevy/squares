---
type: is
id: is-01m57ja8zb6hss8cjvqfnp0ama
title: "PR #665 A4: reduce expanded T-174 result payload"
kind: bug
status: in_progress
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m57j9xsga57szgfah5ex2bcd
hold: null
hold_until: null
created_at: 2026-10-18T13:13:16.522Z
updated_at: 2026-10-18T13:38:36.474Z
started_at: 2026-10-18T13:13:25.548Z
---
Medium; review A https://github.com/jlevy/squares/pull/665#pullrequestreview-5562201404. packing/frontier/results.yaml:21986 expands t-174.html to 335153 bytes vs 300000 budget. Reduce repeated renderer payload with behavior preserved, measure overview.

## Notes

Implemented in 391fdc594046d6090379de55ff552243f42ca6d5: native repeated count labels retain every regularization sentence; T-174 full page falls from 335153 to 249465 bytes against unchanged 300000-byte budget. The retained page-size regression passes. Full overview/Pages gate and repair-head CI pending.
