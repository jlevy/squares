---
type: is
id: is-01m298ppyd1stv2dqe2g5b40b9
title: check_revision6.py cannot finish, so nothing it checks is checked
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-11T22:16:41.665Z
updated_at: 2026-09-11T22:16:41.665Z
---
`check_revision6.py` holds the desaturation rule, the snap, the blind mode and continuous play. It does not finish.

Measured today, unmodified, against the all-pairs page: **57 minutes without completing** under load, and **still running past 30 minutes on an idle machine**. Against the 25-pair spike page it ran 43 minutes without completing. The cost is its blind sweep, which runs a physics simulation for every pair.

The consequence is not that a gate is slow. It is that **nothing it checks is checked**, and has not been for as long as it has been this slow. Phase 6D could produce no before/after comparison for it for exactly this reason -- there was no 'before' to capture.

Two things to work out, in order:

1. **Where the time goes.** 323 pairs x a physics run is the obvious answer, but the gate `check_workbench.py` also builds trajectories and finishes in 90 seconds with a declared per-trajectory budget (TRAJECTORY_MS_CEILING = 400 ms). Either the sweep is doing something the gate is not, or it is doing the same thing 300 times over.
2. **What it should cost.** A sweep over a sample -- every tenth n, or the pairs the record calls hard -- may hold the same property for a fraction of the time. If the full sweep is genuinely worth an hour, it belongs in the deep tier with its cost declared, not in a file anyone is expected to run by hand.

Blocks Phase 6C (think-tmqs): a checker that cannot finish cannot join packing-validate at any tier.
