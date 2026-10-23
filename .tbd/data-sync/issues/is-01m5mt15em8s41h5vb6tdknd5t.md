---
type: is
id: is-01m5mt15em8s41h5vb6tdknd5t
title: Canonical orientation stage for drawn packings (quadrant-weight D4 rule)
kind: feature
status: in_progress
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-10-23-canonical-orientation.md
delegate: claude-orientation-coordinator-u2p5tx
labels: []
dependencies: []
child_order_hints:
  - is-01m5mtmzr06r03ckzb8sh8943r
  - is-01m5mtn0k2bvk9c6ezvd9fv20h
  - is-01m5mtn1m7bgjm1mmf7aw94q12
hold: null
hold_until: null
created_at: 2026-10-23T16:38:14.228Z
updated_at: 2026-10-23T16:49:05.671Z
started_at: 2026-10-23T16:38:17.920Z
---
Owner request 2026-10-23: add a display-only stage to the regularization process that rotates/reflects each drawn (default) picture by one of the container's 8 symmetries so the heaviest quadrant (filled area) is upper-left and the heavier of its neighbours upper-right; deterministic tie-breaks; floating point is fine. Run it across n = 1..324, re-render the default-picture surfaces, document it in the regularization policy and process guide, PR with before/after screenshots. Workflow W7 pipeline-improvement.
