---
type: is
id: is-01m2nk6ptyczkzdneyv6k2757w
title: Expose the new-square-to-container-resize delay as an Animate timing control
kind: feature
status: closed
priority: 1
version: 4
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
updated_at: 2026-09-16T20:40:08.775Z
started_at: 2026-09-16T17:11:12.838Z
closed_at: 2026-09-16T20:40:08.775Z
close_reason: "Completed and merged in PR #189 at merge commit 035d84c6. Exact-head hosted Packing and Pages aggregates passed; the deterministic headless kinetics CLI, shared browser/CLI settings, and bounded square-to-container delay are on main."
resolution: null
duplicate_of: null
---
Animate currently hard-codes the staging between the new square appearing and the container trace/growth sequence through BOUND_CLEAR, BOUND_GROW, BOUND_FADE and BOX_FIRST. Add one user-facing timing parameter for the lead/gap between the arriving red square and container resize, defaulting longer than the current effective gap, with a clear unit/direction and bounded range. It must flow through the public API, shared motion settings, timeline/cache key, tween and physical presentation where applicable, the headless kinetics configuration and deterministic browser/CLI tests. Changing it follows the pause-and-restart continuity policy. Do not overload annealing or solver stiffness with presentation timing.

## Notes

Implemented at engine commit 9cca493c: bounded square-first container delay flows through shared settings, public API, timeline, tween and physical presentation, CLI and browser probes. Resize duration stays continuous at adjacent and late delay settings; setting changes pause and restart. Local package and Chromium contracts pass. Close only after the PR merges green.
