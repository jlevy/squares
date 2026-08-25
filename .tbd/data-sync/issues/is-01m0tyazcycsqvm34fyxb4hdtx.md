---
type: is
id: is-01m0tyazcycsqvm34fyxb4hdtx
title: Diagnose the n4 seed-0 HiGHS solve error
kind: bug
status: in_progress
priority: 0
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - correctness
  - solver-boundary
dependencies: []
parent_id: is-01m0twy8zcmaz9q79aph5qx8kd
created_at: 2026-08-24T22:30:27.485Z
updated_at: 2026-08-25T09:08:31.487Z
---
After D-199 restores n=10, both PACK_JOBS=10 and PACK_JOBS=1 deep regenerations still produce n=4 at 3/4 converged. A 13.70-second four-seed slice isolates seed 0: side 2.0205018998600455, typed initial-cell solver_failure status 4 (HiGHS Solve error), 3,404 LP solves, 2,884 fixed-point evaluations, one unsettled evaluation. Capture the exact failing theta/cell and solver inputs, distinguish model pathology from numerical instability, and fix without weakening the all-row screen or committed golden. No further full-golden retry before a millisecond fixture exists.

## Notes

Session-010 phase 8 begins 2026-08-25 02:10 PDT with a 30m budget. First deliverable only: intercept n=4 seed-0's first HiGHS status-4 LP call and retain theta, separating cell, LP arrays/options/status as a millisecond replay fixture. No full-golden retry, tolerance change, or committed-map update. Implementation stops at 02:30; phase deadline 02:40.
