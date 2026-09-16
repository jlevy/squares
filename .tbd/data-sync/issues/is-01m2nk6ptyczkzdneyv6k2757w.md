---
type: is
id: is-01m2nk6ptyczkzdneyv6k2757w
title: Expose the new-square-to-container-resize delay as an Animate timing control
kind: feature
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
delegate: codex@spud10
labels:
  - workbench
  - animation
dependencies: []
parent_id: is-01m2m2zmky0p8gw5m4zctfnfex
hold: null
hold_until: null
created_at: 2026-09-16T17:11:04.797Z
updated_at: 2026-09-16T17:11:12.840Z
started_at: 2026-09-16T17:11:12.838Z
---
Animate currently hard-codes the staging between the new square appearing and the container trace/growth sequence through BOUND_CLEAR, BOUND_GROW, BOUND_FADE and BOX_FIRST. Add one user-facing timing parameter for the lead/gap between the arriving red square and container resize, defaulting longer than the current effective gap, with a clear unit/direction and bounded range. It must flow through the public API, shared motion settings, timeline/cache key, tween and physical presentation where applicable, the headless kinetics configuration and deterministic browser/CLI tests. Changing it follows the pause-and-restart continuity policy. Do not overload annealing or solver stiffness with presentation timing.
