---
type: is
id: is-01m0vpakbh6fy8p18cxsmtydgd
title: Bound packing validation steps and reap timed-out process groups
kind: bug
status: open
priority: 1
version: 7
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
child_order_hints:
  - is-01m0wbykkdfa1p55rkc66byp9k
  - is-01m0wbykxb2qt4bcjyf2eq3k8r
  - is-01m0wbym69h0rtff9hh1b13a4g
created_at: 2026-08-25T05:29:40.976Z
updated_at: 2026-08-25T11:57:20.396Z
---
packing-validate launches proof, solver, Cargo, and checker subprocesses without per-step deadlines or process-group cleanup; _run_selected waits for every future. A hung step can consume an entire unattended handoff despite mutation controls now being bounded. Add configurable per-step/default deadlines suitable for deep mathematics, group termination/reaping, timed-out diagnostics and focused failure tests. This is a follow-up robustness blocker for unattended use, not for the next supervised exact slice.

## Notes

Session-011 order 11 retained the narrow primitive only. Explicit timeout_seconds calls now have tested Linux/macOS POSIX process-group TERM/grace/KILL cleanup, bounded direct-child reaping, captured timeout output, and an adversarial output-detached descendant test. Ordinary timeout_seconds=None calls preserve their prior subprocess.run and interrupt behavior. Windows bounded-tree mode fails closed. D-239 remains outstanding because no production validation action or engine build supplies a finite timeout, ThreadPoolExecutor can still wait indefinitely, and detached daemons are outside the group contract. Wire a declared per-step/default duration policy in a separate slice; do not close this bead from the primitive alone.
