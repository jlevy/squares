---
type: is
id: is-01m5mt15em8s41h5vb6tdknd5t
title: "Flip regularization: canonical pose stage for drawn packings (quadrant-weight rule)"
kind: feature
status: in_progress
priority: 2
version: 13
spec_path: docs/project/specs/active/plan-2026-10-23-flip-regularization.md
delegate: claude-orientation-coordinator-u2p5tx
labels: []
dependencies: []
child_order_hints:
  - is-01m5mtmzr06r03ckzb8sh8943r
  - is-01m5mtn0k2bvk9c6ezvd9fv20h
  - is-01m5mtn1m7bgjm1mmf7aw94q12
  - is-01m5mzk6r2extagk7j1b2vveve
  - is-01m5mzk7gtthm3xbdy8b1hggbn
  - is-01m5n2rhapespk8a2y6yjtnq4s
hold: null
hold_until: null
created_at: 2026-10-23T16:38:14.228Z
updated_at: 2026-10-23T19:50:28.153Z
started_at: 2026-10-23T16:38:17.920Z
---
Owner request 2026-10-23: add a display-only stage to the regularization process that rotates/reflects each drawn (default) picture by one of the container's 8 symmetries so the heaviest quadrant (filled area) is upper-left and the heavier of its neighbours upper-right; deterministic tie-breaks; floating point is fine. Run it across n = 1..324, re-render the default-picture surfaces, document it in the regularization policy and process guide, PR with before/after screenshots. Workflow W7 pipeline-improvement.

## Notes

PR https://github.com/jlevy/squares/pull/761 (draft, S2) opened at eee8416d9. Local: records and edit tiers pass; 1196/1197 affected tests + the fixed one; papers byte-identical; infographics v0.7.0 cut. Waiting on hosted CI before ready-for-review; owner reviews the turned counts. Follow-up: think-rkg1 (registry dates).
