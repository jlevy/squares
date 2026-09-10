---
type: is
id: is-01m23cey3rdtt5j3q97j3fa6ya
title: Hand the projection search's converged pose to the fixed-angle LP
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T15:26:54.583Z
updated_at: 2026-09-09T15:26:54.583Z
---
The 2026-09-09 simulation survey is explicit that the projection loop should not be asked for the final precision: Gravel and Elser's own results are quoted at 1e-9 only after refinement. exp-139 stops its container ratchet when the step falls below 1e-3, so the reported side carries about three digits of slack that belong to a different instrument.

Evidence it matters: n=5 reached 2.708203125 against the proved 2.7071067811865475. That gap is 0.04 per cent and is entirely the schedule's floor -- the arrangement is the right one. sqpack.exact_lp / the LP-in-cell quench should take the converged pose and close it.

Entry point: devtools/run_projection_ratchet.py, after ratchet() returns.
