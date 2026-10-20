---
type: is
id: is-01m4vexycvd7ptrrst85g2nyza
title: "PR #588 B3: the two modules split the C2 rung differently, and restates combines them"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4vex5amc35y6f4zqamve8q6
hold: null
hold_until: null
created_at: 2026-10-13T20:23:13.563Z
updated_at: 2026-10-13T20:51:08.549Z
started_at: 2026-10-13T20:23:28.340Z
closed_at: 2026-10-13T20:51:08.548Z
close_reason: "fixed in d3cfe11: one partition UNREPLAYED from CONFIRMED_FROM; REPLAYED_RUNGS removed; tested at C2"
resolution: null
duplicate_of: null
---
Severity Low. PR #588 review https://github.com/jlevy/squares/pull/588#pullrequestreview-5509418328, finding B3. Where: packing/devtools/check_standing.py:111,279,391-394, packing/devtools/render_recent_results.py:151,560.
