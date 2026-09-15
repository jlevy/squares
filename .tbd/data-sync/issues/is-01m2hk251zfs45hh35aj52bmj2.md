---
type: is
id: is-01m2hk251zfs45hh35aj52bmj2
title: "PR #171 review D18: the box and its gap-bar pointer turn locked mid-move"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb41hy7fx18dy67asht84d
created_at: 2026-09-15T03:51:37.790Z
updated_at: 2026-09-15T04:16:20.091Z
closed_at: 2026-09-15T04:16:20.090Z
close_reason: "Fixed on PR #171 in ac49b452: the box and pointer lock only at rest (dwell, from move end, or a step whose box does not change size) at the best known side of state.liveN within PACKING_VALIDITY.penetrationTolerance; stage/box-locks sweeps every step (72 of 2,271 samples failed before, on the 17 steps the review named)."
resolution: null
duplicate_of: null
---
Canonical defect D18 from the 2026-09-14 stack triage (High). Source: #171 R2.

The box and its gap-bar pointer turn green ("locked") mid-move. `drawBounds` switches `best` to n + 1's side at `moveStart`; where n + 1's best known side equals `openSide(n + 1)` the box finishes growing at 20 % of the move and sits exactly at n + 1's side for the rest, while `liveN` and the gap bar still show n. The review's sweep found a green pointer more than 1 px from the displayed n's record on 16 steps (1, 5, 11, 19, 29, 41, 55, 71, 89, 132, 156, 182, 210, 241, 273, 307) and 110 -> 111 within 1 px; under physics 5 -> 6 flickers green, black, green.

Files: `packages/workbench/src/application.js:3841-3884`, pointer `:2560-2566` @bb3f7c99; `check_animation_editor.py` exercises only 10 -> 11, where `to < open`. Feature bead: think-31ln.
