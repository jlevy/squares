---
type: is
id: is-01m0vpakbh6fy8p18cxsmtydgd
title: Bound packing validation steps and reap timed-out process groups
kind: bug
status: in_progress
priority: 1
version: 13
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
  - is-01m0wkr0es931jvxpg735s7vq5
  - is-01m0wmfncxtt2ffk5b9pdtf504
  - is-01m0wmn0zw88qedq2hjv6asdxs
created_at: 2026-08-25T05:29:40.976Z
updated_at: 2026-08-25T14:30:32.217Z
---
packing-validate launches proof, solver, Cargo, and checker subprocesses without per-step deadlines or process-group cleanup; _run_selected waits for every future. A hung step can consume an entire unattended handoff despite mutation controls now being bounded. Add configurable per-step/default deadlines suitable for deep mathematics, group termination/reaping, timed-out diagnostics and focused failure tests. This is a follow-up robustness blocker for unattended use, not for the next supervised exact slice.

## Notes

Session-014 completed the first production policy slice: every subprocess launched through the captured or quiet command seam now has a finite configurable 600-second POSIX default, smaller explicit caps win, and coordinator interruption terminates registered process groups while late registration fails closed. Focused evidence: 21 validation CLI tests, Ruff, and BasedPyright pass; D-314 through D-317 record the defects found before checkpoint. Keep this bead in progress: pure-Python worker hangs, aggregate duration across multi-command steps, detached daemons, and Windows process trees remain outside the policy. Resume only as a separately declared bounded pipeline slice; do not present the strict gate as a complete watchdog.
