---
type: is
id: is-01m85bk7fexs4he29m1qhwwy17
title: Retain exact grid-slack refusal rows and the phase reached at timeout
kind: task
status: closed
priority: 2
version: 3
delegate: astra-grid-diagnostics-1123
labels:
  - regularization
  - validation
dependencies: []
parent_id: is-01m859v2drzgkxas4z184he310
hold: null
hold_until: null
created_at: 2026-11-23T23:24:26.476Z
updated_at: 2026-11-24T00:51:15.506Z
started_at: 2026-11-23T23:24:29.012Z
closed_at: 2026-11-24T00:51:15.505Z
close_reason: "Merged in #1107 after exact-head Astra review and green required checks. Bounded phase and failed-row diagnostics verified on 131, 232, 259 and 305."
resolution: null
duplicate_of: null
---
Keep a bounded, rigorously signed sample of selected separation-row violations and useful phase evidence on incomplete grid-slack runs. Preserve the ordinary solver and publication behavior. Exercise real and forced timeout cases.
