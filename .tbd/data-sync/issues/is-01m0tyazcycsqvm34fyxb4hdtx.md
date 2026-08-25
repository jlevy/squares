---
type: is
id: is-01m0tyazcycsqvm34fyxb4hdtx
title: Diagnose the n4 seed-0 HiGHS solve error
kind: bug
status: in_progress
priority: 0
version: 10
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
updated_at: 2026-08-25T09:26:58.567Z
---
After D-199 restores n=10, both PACK_JOBS=10 and PACK_JOBS=1 deep regenerations still produce n=4 at 3/4 converged. A 13.70-second four-seed slice isolates seed 0: side 2.0205018998600455, typed initial-cell solver_failure status 4 (HiGHS Solve error), 3,404 LP solves, 2,884 fixed-point evaluations, one unsettled evaluation. Capture the exact failing theta/cell and solver inputs, distinguish model pathology from numerical instability, and fix without weakening the all-row screen or committed golden. No further full-golden retry before a millisecond fixture exists.

## Notes

Session-010 phase 8 completed its bounded W7 deliverable. Seed 0 reproduces in 2.77s and fails only at fixed-point evaluation 2,884 / LP call 3,404. The retained tests/fixtures/n4_seed0_highs_status4.yaml binds the same-call theta, incoming centres, six-row cell, exact f64 objective/A_ub/b_ub/bounds/options, versions, and status-4 receipt. tests/test_research_contracts.py independently rebuilds all LP inputs, exact-compares them, rejects a cross-wired cell mutation, and directly replays in about 0.33s; current platform returns status 4, while a portable successful result is accepted only if finite and every original-row residual is <=1e-10. Ruff, BasedPyright, and focused pytest pass. D-260 through D-263 record the capture, self-defining receipt, static-gate, and status-patch errors caught before commit. D-203 and this bead remain open: phase 9 W2 must independently diagnose the exact LP and decide whether one further W7 repair is earned. No full golden, tolerance change, or map update occurred.
