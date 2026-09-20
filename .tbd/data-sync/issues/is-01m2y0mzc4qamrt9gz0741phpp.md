---
type: is
id: is-01m2y0mzc4qamrt9gz0741phpp
title: "PR199 review R1: repair n18 doubled-net assertion on the bottom of the stack"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-19T23:39:59.233Z
updated_at: 2026-09-20T01:51:15.257Z
closed_at: 2026-09-20T01:51:15.253Z
close_reason: Repaired at the cumulative tip in PR 202 (https://github.com/jlevy/squares/pull/202). Final code 8dbc1068 passed matching fast 35480879196 and dispatched deferred 35480905141 on clean merge 8ac5a340, identical Git tree, covering all 80 validation steps. Fresh exact and interval replays retain all four n=18 certificates. Original PR 199-201 heads are unchanged and are not independently merge-ready; this closure applies to the corrected tip. The separate scheduling follow-up think-1i1x remains open.
resolution: null
duplicate_of: null
---
At c877006b packing/tests/test_fractional_interval.py:405 expects 361 directions; certificate direction_steps=181 gives 182 half-tangents and 363 doubled directions. PR200 inherits the failure; only PR201 dd2b4d7a fixes it. Move the fix to PR199, restack, correct the 181/361 evidence narration, and obtain fresh full checkpoints before merging each layer.
