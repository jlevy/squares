---
type: is
id: is-01m0tyazcycsqvm34fyxb4hdtx
title: Diagnose the n4 seed-0 HiGHS solve error
kind: bug
status: in_progress
priority: 0
version: 11
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - correctness
  - solver-boundary
dependencies: []
parent_id: is-01m0twy8zcmaz9q79aph5qx8kd
child_order_hints:
  - is-01m0w39mwjkzcb2adpv4e8ge3r
  - is-01m0w3n5fzn66s52pzeknm8bae
  - is-01m0w3n5g2t4spg1dsnwc0pphw
  - is-01m0w3twq7h1f7bm2gc5s0eq45
created_at: 2026-08-24T22:30:27.485Z
updated_at: 2026-08-25T09:40:44.291Z
---
After D-199 restores n=10, both PACK_JOBS=10 and PACK_JOBS=1 deep regenerations still produce n=4 at 3/4 converged. A 13.70-second four-seed slice isolates seed 0: side 2.0205018998600455, typed initial-cell solver_failure status 4 (HiGHS Solve error), 3,404 LP solves, 2,884 fixed-point evaluations, one unsettled evaluation. Capture the exact failing theta/cell and solver inputs, distinguish model pathology from numerical instability, and fix without weakening the all-row screen or committed golden. No further full-golden retry before a millisecond fixture exists.

## Notes

Session-010 phase 9 completed independent W2 diagnosis. Exact binary64 primal/dual certificates prove the retained 22x9 LP feasible and optimal at 2.00103283426408967985 with zero gap; A rank9, cond2 3.23, active-basis cond2 6.92. The optimum has a thin ~1.09e-9 by 8.98e-11 face and 27 near-active optimal bases. Strict highs/highs-ds reproduced status4 in 13/13 calls after presolve reduced 22x9 to4x3 and postsolve exposed two violations totaling2.08982e-9. Default and presolve-off simplex are rejected by original-row residuals1.09e-9 and3.30e-8. Strict highs-ipm solves the identical LP/tolerances at the certified objective with residual0 or2.22e-16. Phase10 authorizes exactly one W7 repair: status4-only IPM retry, unchanged inputs/tolerances/screen, both attempts explicit and counted inside the existing four-call cap, deterministic success/failure/bad-residual controls. No seed or golden before this focused repair is green. D-203 and think-nr5w remain open.
