---
type: is
id: is-01m2phtqshxcx71hnw8j0djm2a
title: Sparse checkouts for the typecheck and geometry jobs
kind: task
status: open
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels:
  - ci
  - focus-efficiency
dependencies:
  - type: blocks
    target: is-01m2kam88w7r9959zvwcswccx3
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-17T02:06:18.416Z
updated_at: 2026-09-17T02:06:23.820Z
---
Lane V7 of think-t7zm is partial at PR #188 da2259fb: sweeps, the Pages jobs and the aggregators use sparse or blobless checkouts, but typecheck and geometry in .github/workflows/packing-validation.yml still check out the whole repository. Measure their checkout cost on hosted runs and apply the same fail-closed sparse checkout where the job's declared inputs allow, with the workflow contract tests updated.
