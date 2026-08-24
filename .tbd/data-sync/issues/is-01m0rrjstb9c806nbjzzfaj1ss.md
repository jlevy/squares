---
type: is
id: is-01m0rrjstb9c806nbjzzfaj1ss
title: solve_to_fixed_point decides convergence by exact float equality of the cell tuple
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T02:11:23.594Z
updated_at: 2026-08-24T07:25:37.581Z
---
The loop stops when 'nxt == cell', a tuple comparison over (i, j, ax, ay, h, sign) floats. Two consequences:

1. Convergence is all-or-nothing on bit patterns. A cell that oscillates between two representations one ulp apart never converges and burns all 12 iterations, then returns the incumbent with the caller unable to distinguish 'settled' from 'gave up' except through the solves/changes counters.
2. max_iters=12 is a magic cap with no recorded justification, and hitting it is reported the same way as converging.

Related and now fixed on the review branch: choose_cell computed h separately per candidate axis, and h is mathematically identical on all four. Sampling 20,000 random pairs, the four axes disagreed on h in 9.7% of them, by up to 4.4e-16 -- noise that entered the argmax over gap = |d| - h and could pick a different separating axis than the geometry does. With one shared h it cancels exactly and argmax|d| decides.

Suggested work: make the fixed-point test compare the discrete part of the cell (i, j, axis index, sign) rather than the floats, and return an explicit converged flag.

## Notes

2026-08-24 post-merge PR #18 address-pr-review sweep: assigned this previously unnumbered review finding R9 and logged it as D-132. Disposition is deferred. The demonstrated defect is the untyped termination contract: settled, rejected/worse, and max-iteration outcomes return the same tuple and can feed outer convergence. The exact-float-equality subclaim is narrowed because fixed theta deterministically regenerates identical numeric axis fields for the same discrete choices; no separate mismatch was reproduced.
