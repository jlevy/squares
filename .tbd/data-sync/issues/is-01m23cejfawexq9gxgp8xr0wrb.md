---
type: is
id: is-01m23cejfawexq9gxgp8xr0wrb
title: Seed the projection ratchet off the grid
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T15:26:42.665Z
updated_at: 2026-09-09T15:26:42.665Z
---
exp-139 measured that every failed run of the divide-and-concur ratchet failed at the first tightening and never moved: each used exactly 48 solver calls, which is eight step halvings at six attempts with no acceptance between. The cause is geometric and specific to squares -- a grid of k squares in a row needs a container of exactly k, so asking for k-epsilon makes the whole grid topology infeasible at once with no small repair available.

The schedule currently starts at the trivial grid (devtools/run_projection_ratchet.py, ratchet()). Replace that start with something that is not a strict local minimum: a random configuration solved cold at a loose side, or a jammed random packing, or the previous n's best with one square added. The floor for what counts as success stays the grid side, so a run that never beats it is still recorded as a failure.

Measured escape rates to beat, best-of-runs: n=5 1 of 4, n=10 4 of 4, n=11 2 of 4, n=17 1 of 4 for pure continuation.
