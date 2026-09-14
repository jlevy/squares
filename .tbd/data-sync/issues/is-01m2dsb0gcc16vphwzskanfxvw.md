---
type: is
id: is-01m2dsb0gcc16vphwzskanfxvw
title: "PR157-MATH-05: Bound grid-route expansion work before materialization"
kind: bug
status: closed
priority: 2
version: 4
assignee: root
delegate: root
labels: []
dependencies: []
parent_id: is-01m2csyyq4nzfqppqj639avs51
created_at: 2026-09-13T16:24:21.766Z
updated_at: 2026-09-14T02:25:14.965Z
closed_at: 2026-09-14T02:25:14.962Z
close_reason: "MATH-05 fix cadbf7e1 is an ancestor of PR #157 head 382944dd, recorded in the #157 body as fixed and independently accepted, and Packing run 34791046990 passed on that exact head; duplicate think-7bfa already closed."
resolution: null
duplicate_of: null
---
PR157 review finding PR157-MATH-05 (Medium, resource). Published: https://github.com/jlevy/squares/pull/157#issuecomment-5654506997 . packing/src/sqpack/fractional/threshold.py: _headroom (l.397-411) runs absolute_expansion_sum(A,k) before weighting; rectangle_terms (l.473) materializes token_sites before its zero-weight skip; _headroom bounds int64 mass, not emitted subsets (A=30,k=15 passes with 6.1e8 subsets; A=40,k=20 with 6.2e11). Fix: skip zero weights before expansion; documented per-atom token cap and emitted-term cap preflighted from compact records; no unbounded coefficient iteration; controls for sentinels, zero-weight success, cap boundary, one-past refusal, existing int64-max direct control. Source e0a1a65e. Address with address-pr-review; retain the finding ID in disposition.

## Notes

Duplicate discovered: think-7bfa (under the parallel address-review tree think-gwxh, created 08:10Z) reports the same grid-route hazard, found while fixing MATH-01, with timings on this Mac. _headroom/absolute_expansion_sum is super-linear in A: A=1000 0.02s, A=2000 0.15s, A=4000 0.95s, A=10000 k=2 did not finish in 110s. This bead is canonical because it carries the published finding (issuecomment-5654506997). Close think-7bfa as its duplicate once this fix lands. Also: the unbounded term count predates PR157 for unweighted atoms (A = listed points), so the cap covers both.
