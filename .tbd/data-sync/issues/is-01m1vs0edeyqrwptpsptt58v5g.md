---
type: is
id: is-01m1vs0edeyqrwptpsptt58v5g
title: "W5: measure and optimize the exhaustive checkpoint with bounded workers"
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T16:32:15.789Z
updated_at: 2026-09-06T17:03:45.321Z
---

## Notes

Exhaustive pytest now reports every duration, and shared worker cap has regression coverage. Whole-checkpoint profile pending after interleaved component measurements. Cap enforcement can increase certificate latency before outer scheduling; no whole-checkpoint speedup claimed. Bounded xdist and n40 duplicate removal remain separate follow-ups requiring same-selection and aggregate coverage decisions.
