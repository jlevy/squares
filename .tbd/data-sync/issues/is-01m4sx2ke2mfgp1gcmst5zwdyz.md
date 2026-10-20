---
type: is
id: is-01m4sx2ke2mfgp1gcmst5zwdyz
title: Record regularized-views' hosted reading with the stack's views and revisit its 450 s ceiling
kind: task
status: in_progress
priority: 2
version: 5
delegate: claude-coordinator-014zkp7r
labels:
  - regularization
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-13T05:51:57.376Z
updated_at: 2026-10-20T10:13:23.857Z
started_at: 2026-10-20T10:13:23.428Z
---
Deep-gate run 38325954699 (against #559, 90 drawn views) took 445 s in 'Re-derive the regularized atlas views' against the step's 450 s ceiling; gate-budgets.yaml records 310 s from 2026-10-03 (74 fewer views). Add the new hosted reading(s) (run 38353486272 against #548 too), update development.md's readings, and decide under OR-17 whether the ceiling or the step's worker count changes before more views are admitted.

## Notes

2026-10-20 (c-lane-rv692, scratchpad/rv692): #692's deferred checkpoint 39396692368 timed out at 900 s in regularized-views (380/381). Both causes: main alone is at ~97% of the 900 s per-subprocess deadline on slow runners (it timed out once at 901 s, job 118235737861, 350/379); #692 adds ~+149 s summed (n=271 Evan Daniel view 21->116 s, new 155 view 65 s), as its drawn views carry 1,700-2,300-digit corner rationals. The all-pairs independent checker is ~90% of the work. Fix: compute each square's own-axis projections once (0.47-0.58x checker time, byte-identical results); landing as its own PR (c-lane-checker) before #692. The 450 s in gate-budgets.yaml is a reporting ceiling only.
