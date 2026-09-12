---
type: is
id: is-01m2aj2deytqhx7j4f1pnte7sp
title: Bound BC329 interval and dilation replay memory and checkpoint progress
kind: bug
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2aj2ewckram8ww4458w74hr
  - type: blocks
    target: is-01m2aj7q4y8raaw35s0jq3ty2y
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T10:19:36.798Z
updated_at: 2026-09-12T10:39:35.285Z
---
The WIP reflected-interval executor submits a closure carrying dense ThresholdAtomData per direction, and the mandatory dilation replay serializes the full certificate per direction while exposing no progress/deadline/log callback. Measure the complete positive path, remove or bound repeated dense serialization, stream or otherwise cap retained outcomes, and make every landed dilation/interval direction atomically checkpointable under the shared scientific deadline. A timeout must leave reconstructable partial evidence and cannot silently lose completed directions. Prove bounds with adversarial controls and retain peak-memory/timing measurements before target registration.

## Notes

The bounded interval scheduler now caps in-flight submissions at 2W, delivers progress in callback completion order, drains every already-landed success before re-raising a worker or progress error, preserves deterministic net-order output and the earliest refutation under reverse landing order, cancels queued work and requests Python 3.14 worker termination on non-complete exit. Focused local evidence: 23 passed, 2 platform skips; Ruff and BasedPyright clean; diff-check clean. The claim is only an in-flight submission bound, not an RSS bound. A Linux-only real failure-path exit control is included but skipped on macOS. Remaining scope: dilation replay progress/deadline and positive-path RSS/serialization calibration.
