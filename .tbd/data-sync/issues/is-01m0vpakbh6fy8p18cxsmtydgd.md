---
type: is
id: is-01m0vpakbh6fy8p18cxsmtydgd
title: Bound packing validation steps and reap timed-out process groups
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-25T05:29:40.976Z
updated_at: 2026-08-25T11:39:48.388Z
---
packing-validate launches proof, solver, Cargo, and checker subprocesses without per-step deadlines or process-group cleanup; _run_selected waits for every future. A hung step can consume an entire unattended handoff despite mutation controls now being bounded. Add configurable per-step/default deadlines suitable for deep mathematics, group termination/reaping, timed-out diagnostics and focused failure tests. This is a follow-up robustness blocker for unattended use, not for the next supervised exact slice.

## Notes

Session-011 phase 5 opens frozen order 11 at 04:38:34 PT. Scope is exactly one reusable cross-platform subprocess timeout/process-group termination primitive plus one focused tests/test_validation_cli.py failure test. Do not retrofit every deep step or change existing criteria/durations. Stop implementation at 20 minutes, on platform uncertainty or inability to prove child cleanup; then preserve the smallest blocker and rotate to order 12.
