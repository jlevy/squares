---
type: is
id: is-01m2aj2deytqhx7j4f1pnte7sp
title: Bound BC329 interval and dilation replay memory and checkpoint progress
kind: bug
status: in_progress
priority: 1
version: 8
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
updated_at: 2026-09-12T16:12:02.851Z
---
The WIP reflected-interval executor submits a closure carrying dense ThresholdAtomData per direction, and the mandatory dilation replay serializes the full certificate per direction while exposing no progress/deadline/log callback. Measure the complete positive path, remove or bound repeated dense serialization, stream or otherwise cap retained outcomes, and make every landed dilation/interval direction atomically checkpointable under the shared scientific deadline. A timeout must leave reconstructable partial evidence and cannot silently lose completed directions. Prove bounds with adversarial controls and retain peak-memory/timing measurements before target registration.

## Notes

The interval and dilation schedulers are integrated and independently reviewed: submissions are capped at 2W, progress is published in completion order, final results are deterministic in net order, landed batches are drained, and incomplete exits terminate workers. The remaining acceptance evidence is the three fresh 14,404-row full-shape non-scientific profiles owned by think-vy5i, followed by source-distinct admission; no BC329 target has run.
