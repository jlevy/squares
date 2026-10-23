---
type: is
id: is-01m5mt15em8s41h5vb6tdknd5t
title: "Flip regularization: canonical pose stage for drawn packings (quadrant-weight rule)"
kind: feature
status: in_progress
priority: 2
version: 8
spec_path: docs/project/specs/active/plan-2026-10-23-flip-regularization.md
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
updated_at: 2026-10-23T17:05:24.533Z
started_at: 2026-10-23T16:38:17.920Z
---
Owner request 2026-10-23: add a display-only stage to the regularization process that rotates/reflects each drawn (default) picture by one of the container's 8 symmetries so the heaviest quadrant (filled area) is upper-left and the heavier of its neighbours upper-right; deterministic tie-breaks; floating point is fine. Run it across n = 1..324, re-render the default-picture surfaces, document it in the regularization policy and process guide, PR with before/after screenshots. Workflow W7 pipeline-improvement.

## Notes

2026-10-23: design settled and measured (quadrants decide 252/324, grid-4 51, grid-8 18, grid-16 3; 268 poses non-identity). Docs committed in 820112576 (policy section 13, process guide step 5, atlas README, synopsis, plan). Lane A (think-dwl4) implementing devtools.canonical_orientation; lanes B (think-5j9y, record) and C (think-z7uv, renderers) follow. Validation pending.
