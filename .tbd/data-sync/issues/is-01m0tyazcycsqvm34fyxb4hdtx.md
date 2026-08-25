---
type: is
id: is-01m0tyazcycsqvm34fyxb4hdtx
title: Diagnose the n4 seed-0 HiGHS solve error
kind: bug
status: in_progress
priority: 0
version: 13
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
  - is-01m0w4xmf6zpvw01t897n8f49y
created_at: 2026-08-24T22:30:27.485Z
updated_at: 2026-08-25T09:48:37.957Z
---
After D-199 restores n=10, both PACK_JOBS=10 and PACK_JOBS=1 deep regenerations still produce n=4 at 3/4 converged. A 13.70-second four-seed slice isolates seed 0: side 2.0205018998600455, typed initial-cell solver_failure status 4 (HiGHS Solve error), 3,404 LP solves, 2,884 fixed-point evaluations, one unsettled evaluation. Capture the exact failing theta/cell and solver inputs, distinguish model pathology from numerical instability, and fix without weakening the all-row screen or committed golden. No further full-golden retry before a millisecond fixture exists.

## Notes

Session-010 phase10 implemented the authorized D-203 repair without a seed/golden run. solve_cell now retries only failed highs status4 once with highs-ipm on identical c/A/b/bounds/options and unchanged1e-10 tolerances; every call is indexed, receipted, and counted inside the existing cap4; IPM stays selected for residual repairs; nonfinite/wrong-shape success is refused. Ten focused controls cover actual fixture recovery, identical inputs, primary status1/2 no fallback, status4->IPM success, status4->status1/2 typed solver_failure, nonfinite and bad-residual refusal, attempt indices, and cap. All60 pytest tests, 8 regression groups, Ruff, BasedPyright pass. D-266 records/fixes the reviewed draft error that promoted status4->status2 disagreement to infeasibility. D-203 stays open until committed review and one seed0 end-to-end replay in phase11; no full golden or other seed yet.
