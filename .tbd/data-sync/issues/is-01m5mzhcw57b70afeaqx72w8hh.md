---
type: is
id: is-01m5mzhcw57b70afeaqx72w8hh
title: Register Evan Daniel's solved view of T-238 at 303 (row 3, 2.17e-11 below)
kind: task
status: open
priority: 2
version: 1
labels:
  - regularization
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T18:14:28.997Z
updated_at: 2026-10-23T18:14:28.997Z
---
The regularization runs of the T-238 adoption at 303 (PR #757, think-tqb5; receipts in packing/cases/regularized_drawings/think-tqb5-2026-10-23/) found a register candidate: Evan Daniel's driver (devtools.regularize_evand run, pin 675a5ea) solved T-238's witness to a certified KKT local minimum at the rational side 17.909762327453569781414351410156, 2.17e-11 below T-238's exact side 223872029093440709529093216833/12500000000000000000000000000, a view of the same packing (one to one, 37 squares moved). By the regularization policy's row 3 it is a smaller packing: register it as a result through the import runbook (stage 3 then 4), as T-155 registered Daniel's exact re-solves (devtools.register_regularized_bounds, a regularizations item naming T-238 as 'of', the packing credited to Amund Kristiansen and the re-solve to Evan Daniel's regularizer run by the project), and adopt it at 303 once validated. Needs a T-NNN id from the coordinator; the lane that adopted T-238 held only T-238. The view is not retained; re-run with: python -m devtools.regularize_evand run --run-dir RUNS/adopt-...-n303-evand --n 303 --workers 2 (about 4 CPU-minutes). Expected significance S1, as T-155's padding re-solves are.
