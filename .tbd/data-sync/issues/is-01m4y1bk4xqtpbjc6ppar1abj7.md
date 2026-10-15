---
type: is
id: is-01m4y1bk4xqtpbjc6ppar1abj7
title: Keep ordinary pre-push validation in the reachable quick lane with explicit slow opt-in
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
child_order_hints:
  - is-01m4zkv7xaws31vqay1f35rs0t
hold: null
hold_until: null
created_at: 2026-10-14T20:23:44.013Z
updated_at: 2026-10-15T11:06:05.609Z
started_at: 2026-10-14T20:24:38.989Z
---
Measured News pre-push selected608of791files, included slow behavior and ran serially700.49s before interruption at13%. Make default reachable validation use the existing QUICK_TESTS predicate for all selection kinds; preserve conservative path selection and normal/pool lane ownership. Add explicit deliberate slow coverage CLI and meaningful option/selection/control tests, document its required role at deep checkpoints. All fast checks stay automatic in CI; no timing ceilings or scientific obligations weakened. Follow Astra next-default-loop-slice report and active CI iteration plan.

## Notes

Implemented and committed on separate codex/quick-push-selection at 934c68019b523a54bef8e121591a1f4a52bb01af, currently based on main d33. Default execution uses the unchanged shared QUICK_TESTS predicate for all conservative file-selection kinds; explicit reachable-slow opt-in, lane/marker/exclusion receipts, empty-phase refusals and pool complement remain. Runner/progress 164 passed, selected CLI 44 passed; Ruff/format/type checks clean. Independent senior, correctness and security reviews clear across the nine-file slice. Delivery awaits News PR617 v0.7.5, then current-main integration, maintained site v0.7.6 cut for the public development guide, canonical quick push and hosted CI. This fixes iteration selection, not the unresolved PR599 strict hosted timing gate; full checkpoint obligations remain.
