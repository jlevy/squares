---
type: is
id: is-01m28rzfz3nnrjrqw0zdg5xvxm
title: Keep every intermediate frame a valid packing, so the pointer can show progress
kind: feature
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T17:41:52.226Z
updated_at: 2026-09-11T17:41:52.226Z
---
The owner's target for the animation: every intermediate frame should be a VALID packing, so the pointer can honestly show the search's progress. Because the final phase is forced onto the exact known packing we always end on the green record; what should vary in between, and be worth watching, is how close the annealing gets -- and that is only meaningful if each frame is a packing rather than an overlapping arrangement.

Today it is not. The page now measures the summed overlap every frame (overlapOf, in unit sides), and the numbers are decisive:

  retained records     0 to 1.3e-5      (the float precision of the poses; exactly 0 at perfect squares)
  the same steps mid-move   1.1 at n = 11, 2.1 at n = 26, 12.4 at n = 110

So the physics currently resolves overlaps over the course of the move rather than maintaining non-overlap throughout. That is why the pointer is hidden mid-move (7517864b) rather than showing a side that is not a claim.

What it would take: a projection to non-overlap after each integration step, so the drawn state is always feasible. The project already has the mechanism on the Python side -- project_pairs in devtools/divide_and_concur.py is exactly this, the inequality projection of the divide-and-concur method, and run_projection_ratchet drives it. The workbench's simulate() would gain the same step.

Two things to decide with a measurement rather than in the abstract:

1. Cost. The projection is another sweep over the neighbour pairs per step, and the simulation runs 168 steps a move at up to 324 bodies. The gate holds a trajectory to 400 ms; today it builds in 43 ms at n = 324, so there is room, but the projection is iterative and its iteration count is the question.

2. Whether a feasible path exists at all for a step with no slack. 164 of 323 steps gain no container side, and at the perfect squares there is no free area whatever -- side^2 - n is exactly 0 at n = 100 and n = 324. A square cannot be inserted into a full grid without something moving through something, unless the container opens first. The container breath (PHYS.open) exists for this and may need to be larger, or the insertion may need to come from outside the box.

Once it holds, the pointer can be shown throughout and the grade_motion instrument gains a real measure of how the annealing is doing frame by frame, which is the owner's stated reason for wanting it.
