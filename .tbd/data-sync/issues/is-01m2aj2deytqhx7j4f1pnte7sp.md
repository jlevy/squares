---
type: is
id: is-01m2aj2deytqhx7j4f1pnte7sp
title: Bound BC329 interval and dilation replay memory and checkpoint progress
kind: bug
status: in_progress
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2aj2ewckram8ww4458w74hr
  - type: blocks
    target: is-01m2aj7q4y8raaw35s0jq3ty2y
  - type: blocks
    target: is-01m2anzgc2aqn6vzx29ps3rpn2
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T10:19:36.798Z
updated_at: 2026-09-12T11:27:55.777Z
---
The WIP reflected-interval executor submits a closure carrying dense ThresholdAtomData per direction, and the mandatory dilation replay serializes the full certificate per direction while exposing no progress/deadline/log callback. Measure the complete positive path, remove or bound repeated dense serialization, stream or otherwise cap retained outcomes, and make every landed dilation/interval direction atomically checkpointable under the shared scientific deadline. A timeout must leave reconstructable partial evidence and cannot silently lose completed directions. Prove bounds with adversarial controls and retain peak-memory/timing measurements before target registration.

## Notes

Interval and dilation threshold schedulers now cap submissions at 2W, publish completion-order progress, return deterministic net-order results, drain landed batches, and terminate workers on incomplete exits. Integrated target-free suite passes 117 tests with 3 platform skips. Fixed-core dilation progress/deadline retention and measured RSS calibration remain.
