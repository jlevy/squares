---
type: is
id: is-01m2aj2deytqhx7j4f1pnte7sp
title: Bound BC329 interval and dilation replay memory and checkpoint progress
kind: bug
status: in_progress
priority: 1
version: 4
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
updated_at: 2026-09-12T10:32:32.910Z
---
The WIP reflected-interval executor submits a closure carrying dense ThresholdAtomData per direction, and the mandatory dilation replay serializes the full certificate per direction while exposing no progress/deadline/log callback. Measure the complete positive path, remove or bound repeated dense serialization, stream or otherwise cap retained outcomes, and make every landed dilation/interval direction atomically checkpointable under the shared scientific deadline. A timeout must leave reconstructable partial evidence and cannot silently lose completed directions. Prove bounds with adversarial controls and retain peak-memory/timing measurements before target registration.

## Notes

Sol high implemented and tested the bounded interval scheduler on the clean BC329 stack: submissions cap at 2W, progress sees landed results without input-order blocking, deterministic verdict order and early-refutation prefix are preserved, and completed successes survive a mixed error batch. Focused evidence: interval 20 passed/1 Linux-only skip on macOS; fixed-runner mocked integration 29 passed; Ruff clean; BasedPyright zero. Root review has not yet admitted this slice: current early-return cleanup uses shutdown(wait=False), so already-running pool children may outlive the reusable call. The remaining cf2z scope also includes dilation deadline/progress and measured serialization/RSS bounds.
