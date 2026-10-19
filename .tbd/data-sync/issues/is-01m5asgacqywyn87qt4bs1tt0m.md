---
type: is
id: is-01m5asgacqywyn87qt4bs1tt0m
title: "Results page headroom: 1,203,626 of 1,250,000 bytes at 217 results (~8 rows left)"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-19T19:16:37.910Z
updated_at: 2026-10-19T19:16:37.910Z
---
Measured on claude/integrate-514 (bf1beaab1, PR #514 + main f3d5da7b): results.html is 1,203,626 bytes at 217 results against the 1,250,000 ceiling in devtools/site_urls.py; at the p90 row cost (4,607 + 291 B) the room is about 8 results, so RESULTS_ROOM_THROUGH was set to 225. Registering #675/#678's upper bounds (up to ~85+79 rows) or several intakes will exceed it. Options: paginate/lazy-render the results table, compress row markup, or re-measure the page-load budgets at a larger size and re-select the ceiling under OR-17. Test name and spec still say 'through 200'.
