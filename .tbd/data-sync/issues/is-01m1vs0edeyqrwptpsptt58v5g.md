---
type: is
id: is-01m1vs0edeyqrwptpsptt58v5g
title: "W5: measure and optimize the exhaustive checkpoint with bounded workers"
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T16:32:15.789Z
updated_at: 2026-09-06T19:18:52.300Z
---

## Notes

Two complete hosted exhaustive observations on the same base and identical55case selection are retained. Run34050662740 atfb1a987d requested1outer/2inner on4CPUs: job26m56, pytest1598.45s. Run34052836364 atbc65e779 requested1outer/4inner: job20m56, pytest1234.35s, all55setup/call/teardown identity sets audited. The6minute difference is descriptive only: serial n40 also fell236.30 to169.59s, so host/run variation prevents causal speedup attribution. Actual CPU/memory caps remain enforced; the isolated allocation restores previously allowed parallelism. Profiling/allocation first slice is implemented; bounded pytest scheduling and dependency-based reuse remain Phase3 under think-xejq. Newmainc144 changes verifier/controlinputs; latestheadeff5587f integration needsfreshfullcheckpoint beforePRreadiness.
