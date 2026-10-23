---
type: is
id: is-01m5mt15em8s41h5vb6tdknd5t
title: Canonical orientation stage for drawn packings (quadrant-weight D4 rule)
kind: feature
status: in_progress
priority: 2
version: 2
delegate: claude-orientation-coordinator-u2p5tx
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-23T16:38:14.228Z
updated_at: 2026-10-23T16:38:17.921Z
started_at: 2026-10-23T16:38:17.920Z
---
Owner request 2026-10-23: add a display-only stage to the regularization process that rotates/reflects each drawn (default) picture by one of the container's 8 symmetries so the heaviest quadrant (filled area) is upper-left and the heavier of its neighbours upper-right; deterministic tie-breaks; floating point is fine. Run it across n = 1..324, re-render the default-picture surfaces, document it in the regularization policy and process guide, PR with before/after screenshots. Workflow W7 pipeline-improvement.
