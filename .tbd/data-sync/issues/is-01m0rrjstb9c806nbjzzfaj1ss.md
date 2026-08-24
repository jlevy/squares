---
type: is
id: is-01m0rrjstb9c806nbjzzfaj1ss
title: solve_to_fixed_point decides convergence by exact float equality of the cell tuple
kind: bug
status: in_progress
priority: 2
version: 5
labels: []
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T02:11:23.594Z
updated_at: 2026-08-24T15:25:57.133Z
closed_at: 2026-08-24T15:12:21.943Z
close_reason: "D-132 fixed: fixed-cell iteration returns typed settlement evidence for fixed point, cycle, infeasible or worse transition, and cap; both quench paths refuse outer convergence after unsettled evidence. Focused regression, historical gate, Ruff, BasedPyright, schema, and replay checks pass. The newly exposed golden drift is separately open as D-162 / think-wbra."
resolution: null
duplicate_of: null
---
The loop stops when 'nxt == cell', a tuple comparison over (i, j, ax, ay, h, sign) floats. Two consequences:

1. Convergence is all-or-nothing on bit patterns. A cell that oscillates between two representations one ulp apart never converges and burns all 12 iterations, then returns the incumbent with the caller unable to distinguish 'settled' from 'gave up' except through the solves/changes counters.
2. max_iters=12 is a magic cap with no recorded justification, and hitting it is reported the same way as converging.

Related and now fixed on the review branch: choose_cell computed h separately per candidate axis, and h is mathematically identical on all four. Sampling 20,000 random pairs, the four axes disagreed on h in 9.7% of them, by up to 4.4e-16 -- noise that entered the argmax over gap = |d| - h and could pick a different separating axis than the geometry does. With one shared h it cancels exactly and argmax|d| decides.

Suggested work: make the fixed-point test compare the discrete part of the cell (i, j, axis index, sign) rather than the floats, and return an explicit converged flag.

## Notes

Reopened after D-165 recurrence. The D-132 implementation typed fixed-point exits only after an initial cell solve succeeded. An initial solve returning None still becomes a dummy 1e3 objective in angle probes, so the outer quench can later report convergence without acknowledging that failure. A typed CellSolveResult prototype proved the bypass: once initial post-check rejection is propagated, D-016 and D-029 controls stop early; one bounded tightened-constraint retry restores both side values, but n=10 remains explicitly nonconverged on a free-sweep cell cycle. Prototype is recoverable in stash@{0}; do not merge until policy and controls are scientifically green.
