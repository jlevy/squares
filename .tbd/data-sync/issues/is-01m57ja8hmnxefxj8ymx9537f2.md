---
type: is
id: is-01m57ja8hmnxefxj8ymx9537f2
title: "PR #665 A3: reconcile adoption regression fixtures"
kind: bug
status: in_progress
priority: 2
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m57j9xsga57szgfah5ex2bcd
hold: null
hold_until: null
created_at: 2026-10-18T13:13:16.083Z
updated_at: 2026-10-18T14:48:15.932Z
started_at: 2026-10-18T13:13:25.542Z
---
Medium; review A https://github.com/jlevy/squares/pull/665#pullrequestreview-5562201404. tests/test_house_adoption.py:80,93,162 and poster, announcement, recent-result, grid-slack, frontier-draft and chunk-taxonomy fixtures retain displaced house assumptions. Use retained old records for old-packing behavior; update current-record expectations and replay closed-form writer in required order.

## Notes

Fixed in391fdc594 with retained old records for historical behavior, current adopted-house expectations and closed-form replay. Tiny strict rational improvements display beyond40 places. bf93722b1 also updates source-stratified chunk fixture to1779/27 and declares the synthetic tie test as a ceiling consumer. Focused batches131+21 pass; final record/pin quartet4 pass at2890be7fa. Closed linked harness child think-lrrt / b88568f9a preserves60s subprocess timeout, isolates9 pool items and guarantees sibling cleanup;69 module tests pass, including2 real-child negative controls. Exact earlier broad-run probe stall remains unproved. Full rerun/hosted shards remain pending.
