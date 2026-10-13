---
type: is
id: is-01m4t2geederxhbmhn6zbqebd4
title: Register n=290's exact side below its rounded ceiling
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@vm
labels:
  - regularization
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-13T07:26:53.900Z
updated_at: 2026-10-13T18:08:05.272Z
started_at: 2026-10-13T17:08:43.423Z
---
A grid-slack view of n=290 (runs of 13 October 2026, 0.5 and 5 degrees) is exactly verified on both routes at the decimal witness's side 70142135623730950488016887242097/4000000000000000000000000000000, 2.4e-15 below the verified upper bound 876776695296637/50000000000000 (Evan Daniel's ceiling rounded up at 14 decimals) and 4.8e-33 above Kingbird's 14 + (5/2)sqrt(2). Policy row 3 / question 3: register it as a result, as T-154 did for 59 counts, then draw it. Not a new packing: the same construction certified at a tighter rational side.

## Notes

Registered as T-155 on claude/upbeat-ptolemy-1lxxx8-register290 (head 1bf791a75, pushed 2026-10-13; no PR yet): register_regularized_bounds gains a second batch (--batch grid-slack); receipts and view under packing/cases/regularized_bounds/grid-slack-2026-10-13/; n-290 verified_upper_bound exact form moved to s_W. Drawing: no change, nothing drawn. Close when the branch merges.
