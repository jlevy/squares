---
type: is
id: is-01m5mt15em8s41h5vb6tdknd5t
title: "Flip regularization: canonical pose stage for drawn packings (quadrant-weight rule)"
kind: feature
status: in_progress
priority: 2
version: 12
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
updated_at: 2026-10-23T19:10:48.662Z
started_at: 2026-10-23T16:38:17.920Z
---
Owner request 2026-10-23: add a display-only stage to the regularization process that rotates/reflects each drawn (default) picture by one of the container's 8 symmetries so the heaviest quadrant (filled area) is upper-left and the heavier of its neighbours upper-right; deterministic tie-breaks; floating point is fine. Run it across n = 1..324, re-render the default-picture surfaces, document it in the regularization policy and process guide, PR with before/after screenshots. Workflow W7 pipeline-improvement.

## Notes

2026-10-23 evening: owner moved the heaviest quadrant to the lower right (keeps n=11; measured 252/324 published poses kept vs 56) and asked for a separate fast stage. Docs rewritten (6a73014a2). Lane D (think-1ub3): separate stage from retained SVGs, own record + check, default_drawings back to main. Lane E (think-6kps): posters map exact corners pre-scalar; site reads the new record. Fable review of the first version: nothing blocking; findings routed. Still to do: integrate D/E, regenerate record, re-pin, cut infographics v0.7.0, paper no-change re-verify, screenshots, Fable round 2, PR.
