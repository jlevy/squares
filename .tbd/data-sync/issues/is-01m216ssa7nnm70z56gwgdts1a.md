---
type: is
id: is-01m216ssa7nnm70z56gwgdts1a
title: sqsearch pair-test budget binds only at restart granularity
kind: bug
status: open
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m20zyy839t6mbvpqy8ay2hsn
created_at: 2026-09-08T19:09:29.787Z
updated_at: 2026-09-09T00:20:12.725Z
---
sqsearch tests --budget-pair-tests only in run_chain's outer loop, so a chain stops after the FIRST anneal that carries it past the cap. An arm whose anneals are ten times longer therefore overshoots by up to one whole anneal, and two arms compared "at equal budget" are not.

Measured in exp-135 / exp-138, delivered pair tests as a multiple of declared, per cell:
- A-control and C-pressure: 1.001 to 1.015 (clean).
- B-perturb: 1.001 to 1.040 on the cells that decide the verdict, up to 1.27 at n = 52.
- A-slow (--steps 4000000): 1.024 to 1.31.
- B-perturb-slow: 1.31 at n = 17, 2.13 at n = 37, 3.92 at n = 50, 4.24 at n = 52; 1.74x overall.

The n = 37 and n = 50 results for the both-factors arm are consequently NOT equal-budget comparisons and exp-138 reports them as observations rather than comparisons.

Fix: test the pair-test budget inside the anneal step loop, not between restarts, and stop the anneal when it trips. Keep the move budget where it is.

Regression: extend the existing selftest check "pair-test budget binds and the move budget does not have to" so it also asserts the delivered count is within a small factor of the declared one at a large --steps, which the current check would pass with any overshoot.

This is the same class of error as exp-001's "the declared budget did not bind": a budget that is nominally equal and actually is not. File it in defects.yaml with that detector once the fix lands.
