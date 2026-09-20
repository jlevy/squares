---
type: is
id: is-01m2y0n0x69m65yn2cj85wh6gr
title: "PR199 review R2: keep threshold LP solver errors unresolved"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-19T23:40:00.804Z
updated_at: 2026-09-20T01:51:15.276Z
closed_at: 2026-09-20T01:51:15.276Z
close_reason: Repaired at the cumulative tip in PR 202 (https://github.com/jlevy/squares/pull/202). Final code 8dbc1068 passed matching fast 35480879196 and dispatched deferred 35480905141 on clean merge 8ac5a340, identical Git tree, covering all 80 validation steps. Fresh exact and interval replays retain all four n=18 certificates. Original PR 199-201 heads are unchanged and are not independently merge-ready; this closure applies to the corrected tip. The separate scheduling follow-up think-1i1x remains open.
resolution: null
duplicate_of: null
---
packing/devtools/produce_threshold_certificate.py:209-212 handles status1 but maps status4 and other unsuccessful outcomes to infeasible. Reproduced mocked HiGHS status4 on a feasible one-row matrix; resolve then emits scientific refusal. Only status2 can report solver infeasibility; preserve raw status/message, classify numerical/solver failures unresolved, and cover both initial and subsequent LP paths.
