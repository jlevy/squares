---
type: is
id: is-01m4pcpb29v0db74jb4pg37yk6
title: Speed up arrangement_gap with a spatial index (72 of 553 s at n = 292)
kind: task
status: open
priority: 3
version: 1
labels:
  - regularization
dependencies: []
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
created_at: 2026-10-11T21:07:55.081Z
updated_at: 2026-10-11T21:07:55.081Z
---
devtools.check_half_angle_area.arrangement_gap matches every square to its nearest centre under each of the box's eight symmetries by an exact all-pairs scan; at n = 292 it took 72 s of the driver's 553 s. A grid bucket on float centres to propose candidates, with the exact distance only for those, keeps the result and cuts the cost; the full 1..324 run calls it once per changed view.
