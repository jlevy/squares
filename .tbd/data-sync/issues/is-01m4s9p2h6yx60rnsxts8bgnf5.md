---
type: is
id: is-01m4s9p2h6yx60rnsxts8bgnf5
title: "Regularize 270 and 305 again on #553's witnesses"
kind: task
status: closed
priority: 2
version: 5
delegate: user-eb-reg-leftovers
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m4mdbq6bhkv71fxeeckawsbt
hold: null
hold_until: null
created_at: 2026-10-13T00:13:03.909Z
updated_at: 2026-10-16T09:57:49.021Z
started_at: 2026-10-16T05:22:37.035Z
closed_at: 2026-10-16T09:57:49.021Z
close_reason: "Verified 2026-10-16 by lane D (user-eb-reg-leftovers): 301 is drawn from Evan Daniel's view at U (0/0/0 light/uneven/near-axis, 8 classes), better than the 1-degree grid view (14 classes, 4.6e-12 above U); at 270 and 305 neither strong generator improves on the drawn views (runs evand-regularize-leftovers-1016, grid-slack leftovers 0.5/1/5 deg). No record names these beads."
resolution: null
duplicate_of: null
---
#553 (T-151, T-152) re-housed 270 and 305 after #559's runs on #518's witnesses, so the views #559 drew there (Evan Daniel's at 270, grid-slack /1 at 305) lapsed and the axis tool's views of #553's witnesses are drawn. Run devtools.regularize_evand and devtools.regularize_grid_slack on the new witnesses at both counts and admit by the grid lane's rule (better on some drawing-census measure, worse on none). Stack 498, follows #559.

## Notes

2026-10-16 ~08:05Z user-eb-reg-leftovers (lane D): VERIFIED, the ask is met. Both generators have now run on #553's witnesses at 270 and 305. Grid-slack: the views drawn since 13 October (270: grid-slack-deg05-1013; 305: grid-slack-deg5-1013-b), admitted under the improvement rule (state regularized). Evan Daniel's regularizer, run tonight (evand-regularize-leftovers-1016, both counts on the current witnesses): 270 row 4 held, its solved view 1.69e-19 above U (it would draw one class fewer and 754 stage sides against 752, but a drawn view must be at most U); 305 row 7 refuse (house/stage sides 824/842 to 820/838). Grid-slack re-run at 0.5/1/5 degrees: 270 ties the drawn view at 0.5 and 1, worse on light/uneven at 5; 305 row 7 at 0.5 and 1, ties at 5. regularize_select: nothing improves on the drawn views, so nothing is admitted. No record names think-zjmt; the README paragraph citing this lands with this lane's PR. Coordinator: please close (I have not); note think-zjmt blocks think-ux1v.
