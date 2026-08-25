---
type: is
id: is-01m0vpakbh6fy8p18cxsmtydgd
title: Bound packing validation steps and reap timed-out process groups
kind: bug
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels: []
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-25T05:29:40.976Z
updated_at: 2026-08-25T05:37:41.153Z
---
packing-validate launches proof, solver, Cargo, and checker subprocesses without per-step deadlines or process-group cleanup; _run_selected waits for every future. A hung step can consume an entire unattended handoff despite mutation controls now being bounded. Add configurable per-step/default deadlines suitable for deep mathematics, group termination/reaping, timed-out diagnostics and focused failure tests. This is a follow-up robustness blocker for unattended use, not for the next supervised exact slice.
