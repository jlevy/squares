---
type: is
id: is-01m0tyazcycsqvm34fyxb4hdtx
title: Diagnose the n4 seed-0 HiGHS solve error
kind: bug
status: open
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - correctness
  - solver-boundary
dependencies:
  - type: blocks
    target: is-01m0vcb6qqhf20a5mex14zss2b
parent_id: is-01m0twy8zcmaz9q79aph5qx8kd
created_at: 2026-08-24T22:30:27.485Z
updated_at: 2026-08-25T02:35:15.053Z
---
After D-199 restores n=10, both PACK_JOBS=10 and PACK_JOBS=1 deep regenerations still produce n=4 at 3/4 converged. A 13.70-second four-seed slice isolates seed 0: side 2.0205018998600455, typed initial-cell solver_failure status 4 (HiGHS Solve error), 3,404 LP solves, 2,884 fixed-point evaluations, one unsettled evaluation. Capture the exact failing theta/cell and solver inputs, distinguish model pathology from numerical instability, and fix without weakening the all-row screen or committed golden. No further full-golden retry before a millisecond fixture exists.
