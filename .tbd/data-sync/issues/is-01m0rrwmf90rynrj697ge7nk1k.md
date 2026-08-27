---
type: is
id: is-01m0rrwmf90rynrj697ge7nk1k
title: quench_bracket's budget is wall-clock, so results depend on machine load
kind: bug
status: open
priority: 2
version: 6
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T02:16:45.800Z
updated_at: 2026-08-27T10:12:54.511Z
---
quench_bracket and _free_sweep take time_budget in seconds and stop on a wall-clock deadline. Host speed, load, pool width, and contention therefore change how many LP solves and angle probes a nominally identical quench performs, making convergence a property of the machine as well as the mathematics.

D-036 already covers an incomplete free sweep returned as complete. On 2026-08-24 this broader risk became observed rather than benign: a 10-wide strict deep gate and a separately isolated one-worker deep golden step both changed the n=4 convergence total and left n=10 at a typed post-check rejection. The isolated step consumed 109 seconds and reproduced the same D-162 golden drift; no tolerance was weakened and no regenerated map was accepted.

Express the scientific budget as work (LP solves or bracket iterations), retain wall time only as an outer recorded safety deadline, and mark any deadline hit censored. Also separate load sensitivity from solver-residual nondeterminism under D-162. Acceptance requires identical retained work and outcomes across declared pool widths and a stable known-answer response at n=4 and n=10.

## Notes

Observed load dependence remains: under concurrent full gates the merged-main n=10 regression path failed, while an immediate isolated PACK_JOBS=1 replay passed; no threshold or retained map was changed. Session 027 W3 found that existing quench and local-realization paths collapse or omit the seated-wall, contact, and nonedge semantics needed by the new full-cell label. The bounded repair therefore retains only target-free FullCellExecutionPlan/v1: 15 exact tagged structural rows, complete derived work, pair_tests=0, lp_solver_attempts=0, hashless replay, and typed row/count mutations in the generator-owned control. It has no numerical matrix, target read, geometry, side, feasibility, or optimality result. Actual LP compilation remains blocked on full-cell-execution-semantics-unfrozen. BC-017 separately remains open for real n=5/n=10 counted execution and load equality; this bead remains open for stable n=4/n=10 quench outcomes and work across pool widths/load.
