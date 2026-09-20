---
type: is
id: is-01m2y1zgej76sjb7yb548x5d6e
title: Regenerate stale n18 composite atlas exports after T-030
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-20T00:03:12.977Z
updated_at: 2026-09-20T01:51:15.450Z
closed_at: 2026-09-20T01:51:15.450Z
close_reason: Repaired at the cumulative tip in PR 202 (https://github.com/jlevy/squares/pull/202). Final code 8dbc1068 passed matching fast 35480879196 and dispatched deferred 35480905141 on clean merge 8ac5a340, identical Git tree, covering all 80 validation steps. Fresh exact and interval replays retain all four n=18 certificates. Original PR 199-201 heads are unchanged and are not independently merge-ready; this closure applies to the corrected tip. The separate scheduling follow-up think-1i1x remains open.
resolution: null
duplicate_of: null
---
The full PR 201 checkpoint 35476507563 failed test_known_best_composite_contains_every_case_and_square: source and composite JSON say 4.679 but retained 1-100 and 1-324 SVGs still say 4.67. Regenerate owned atlas exports and validate before publishing the correctness layer.
