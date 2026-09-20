---
type: is
id: is-01m2y0x39qkdcxs03a94pjt7qx
title: "Stack review follow-ups: threshold multiplicities, pinned receipt, interpreter contract"
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-19T23:44:25.398Z
updated_at: 2026-09-20T01:51:15.430Z
closed_at: 2026-09-20T01:51:15.430Z
close_reason: Repaired at the cumulative tip in PR 202 (https://github.com/jlevy/squares/pull/202). Final code 8dbc1068 passed matching fast 35480879196 and dispatched deferred 35480905141 on clean merge 8ac5a340, identical Git tree, covering all 80 validation steps. Fresh exact and interval replays retain all four n=18 certificates. Original PR 199-201 heads are unchanged and are not independently merge-ready; this closure applies to the corrected tip. The separate scheduling follow-up think-1i1x remains open.
resolution: null
duplicate_of: null
---
Nonblocking follow-ups from PR199-201 review: threshold_separation.atom_columns ignores multiplicities; current callers use ordinary2of3, so guard that precondition or implement tokens before broader use. PR201 T029 receipt still points at live certificate.json now T030; pin certificate-1871-400.json. test_covering_queue rejects a valid project python3 executable by basename; test version/identity. Do not widen scientific scope or promote a new result.
