---
type: is
id: is-01m4y1bk4xqtpbjc6ppar1abj7
title: Keep ordinary pre-push validation in the reachable quick lane with explicit slow opt-in
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T20:23:44.013Z
updated_at: 2026-10-14T20:24:38.992Z
started_at: 2026-10-14T20:24:38.989Z
---
Measured News pre-push selected608of791files, included slow behavior and ran serially700.49s before interruption at13%. Make default reachable validation use the existing QUICK_TESTS predicate for all selection kinds; preserve conservative path selection and normal/pool lane ownership. Add explicit deliberate slow coverage CLI and meaningful option/selection/control tests, document its required role at deep checkpoints. All fast checks stay automatic in CI; no timing ceilings or scientific obligations weakened. Follow Astra next-default-loop-slice report and active CI iteration plan.
