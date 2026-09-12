---
type: is
id: is-01m2ay2nyw6emx0zphn4pj685e
title: Meter and publish BC329 runner-stack resource usage separately
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: root accounting lane
labels:
  - n11
  - usage
dependencies:
  - type: blocks
    target: is-01m2axbxf0xz00ezc32q4mesn2
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T13:49:28.411Z
updated_at: 2026-09-12T13:49:38.134Z
---
Treat the BC329 runner, calibration, and scientific continuation as a separate stacked-PR cost interval from PR148 and PR149. At each publication boundary, retain the native task-tree or agent rollups that are actually available, command wall times, validation shape, agent/model/effort assignments, and scientific target cost. Never infer missing token counts or mix earlier PR sessions into this layer. Update the runner PR's What This Branch Cost section and the relevant session/close report; finish with the record validators green.

## Notes

Initial PR body separates this 13-file runner layer from PR148/149 and records focused, edit, manifest, pre-push, agent-review, and zero scientific-target costs. Native token/task-tree rollup remains to be captured at a stable publication boundary; no missing figure will be inferred.
