---
type: is
id: is-01m3n5xm0vg30jrf4bnsd50b48
title: Intake wand125's point-only s(21) = 5 (point_n21_L5/, Lean overlay) and s(45) = 7 (point_n45_L7/, evand's zmx2)
kind: task
status: closed
priority: 2
version: 5
labels:
  - packing
  - wand125-update
  - low-n
  - review
dependencies: []
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-28T23:34:37.339Z
updated_at: 2026-10-12T23:39:22.984Z
closed_at: 2026-10-12T23:39:22.983Z
close_reason: "Delivered: wand125's point-only routes are registered at V3/C3, s(21) = 5 as T-055 (c03c6d4fb, 2026-10-02) and s(45) = 7 as T-054, both on main."
resolution: null
duplicate_of: null
---
Per packing/resources/web/wand125-x-update-2026-09-28/supplied-messages.txt: a point-only route to s(21) = 5 derived from evand's support (no priority claimed) with a Lean 4 reduction to minSide 21 = 5 from a single capture hypothesis; a script turns a certificate into a Lean data file. Retain point_n21_L5/ at a pinned revision, replay the capture check that discharges the hypothesis, and review exactly what the Lean part proves versus what stays computational. If its checker is method-distinct from evand's sweep it is the candidate second method for s(21) = 5 at C4. Credit: wand125, derived from evand's support.

## Notes

wand125 point_n21_L5 verify_portable.py --workers 2 running on this host (Lane 3 scratch lane3/n21-replay, logs lane3/logs/); root and sieve stages reproduced byte for byte; frontier stage slow under load. Finish with n21-compare per the wand125-point-and-mixed-2026-09-28 README.
