---
type: is
id: is-01m0vpakbh6fy8p18cxsmtydgd
title: Bound packing validation steps and reap timed-out process groups
kind: bug
status: in_progress
priority: 1
version: 9
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
child_order_hints:
  - is-01m0wbykkdfa1p55rkc66byp9k
  - is-01m0wbykxb2qt4bcjyf2eq3k8r
  - is-01m0wbym69h0rtff9hh1b13a4g
  - is-01m0wkpjps57ptqvd15dfnk8ps
created_at: 2026-08-25T05:29:40.976Z
updated_at: 2026-08-25T14:03:02.232Z
---
packing-validate launches proof, solver, Cargo, and checker subprocesses without per-step deadlines or process-group cleanup; _run_selected waits for every future. A hung step can consume an entire unattended handoff despite mutation controls now being bounded. Add configurable per-step/default deadlines suitable for deep mathematics, group termination/reaping, timed-out diagnostics and focused failure tests. This is a follow-up robustness blocker for unattended use, not for the next supervised exact slice.

## Notes

Session-014 phase 1 began 06:57:09 PT with a 07:27:09 hard deadline. Add a declared finite default for every production validation subprocess at the existing command seam, plus one ordinary-action timeout control and docs. Stop implementation at 20 minutes; do not replace ThreadPoolExecutor, run strict/deep validation, or claim pure-Python worker/Windows tree bounds.
