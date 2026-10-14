---
type: is
id: is-01m4sx2ke2mfgp1gcmst5zwdyz
title: Record regularized-views' hosted reading with the stack's views and revisit its 450 s ceiling
kind: task
status: open
priority: 2
version: 2
labels:
  - regularization
dependencies: []
created_at: 2026-10-13T05:51:57.376Z
updated_at: 2026-10-14T02:57:18.692Z
---
Deep-gate run 38325954699 (against #559, 90 drawn views) took 445 s in 'Re-derive the regularized atlas views' against the step's 450 s ceiling; gate-budgets.yaml records 310 s from 2026-10-03 (74 fewer views). Add the new hosted reading(s) (run 38353486272 against #548 too), update development.md's readings, and decide under OR-17 whether the ceiling or the step's worker count changes before more views are admitted.

## Notes

Hosted readings, 14 Oct 2026 (packing-validate --only "regularized atlas views re-derive exactly" --jobs 1 --inner-jobs 4, the deep gate's regularized-views job):
- run 38325954699, #559 before the identity re-measure: 443.2 s step wall (summed per-view 735 s).
- run 38502424243, dispatched against #580's merge tree (e5bd0f98c, the whole group #511-#580): 647.1 s step wall (summed per-view 979 s), passed. Every view is about 1.33-1.37x slower, the 234 "unchanged" ones included (mean 0.70 s vs 0.51 s), so this is the runner class, not the stack's code; the cheaper identity search does not move this step (n = 132: 3.9 s vs 2.8 s).
Two readings now: geometric mean of the step walls ~535 s, above the 450 s ceiling in gate-budgets.yaml (deep-gate and post-merge entries, both enforcement: reporting). Revisit: either raise the ceiling on these two readings with their spread, or split the step across two workers.
