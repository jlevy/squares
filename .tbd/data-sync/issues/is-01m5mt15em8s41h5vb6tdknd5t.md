---
type: is
id: is-01m5mt15em8s41h5vb6tdknd5t
title: "Flip regularization: canonical pose stage for drawn packings (quadrant-weight rule)"
kind: feature
status: closed
priority: 2
version: 17
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
  - is-01m5nrtdxf5sswwytj8g47m6m4
hold: null
hold_until: null
created_at: 2026-10-23T16:38:14.228Z
updated_at: 2026-10-24T01:36:19.374Z
started_at: 2026-10-23T16:38:17.920Z
closed_at: 2026-10-23T20:48:44.136Z
close_reason: "Merged in https://github.com/jlevy/squares/pull/761 (merge 77aba4c02, 2026-10-23 20:22 UTC). Flip regularization: heaviest quadrant lower right, keeps 252/324 published poses, own record + 1.5 s check; posters (infographics v0.7.0) and site canonical; Original/As published unchanged. Deployed site: check_published_site --commit 77aba4c02 passed 5710/5710. Follow-up: think-rkg1 (registry dates)."
resolution: null
duplicate_of: null
---
Owner request 2026-10-23: add a display-only stage to the regularization process that rotates/reflects each drawn (default) picture by one of the container's 8 symmetries so the heaviest quadrant (filled area) is upper-left and the heavier of its neighbours upper-right; deterministic tie-breaks; floating point is fine. Run it across n = 1..324, re-render the default-picture surfaces, document it in the regularization policy and process guide, PR with before/after screenshots. Workflow W7 pipeline-improvement.

## Notes

Post-merge: main's integration suites showed one failure from #761 (test_site_drawing_hover pinned atlas/house/n-11.svg); fixed in https://github.com/jlevy/squares/pull/762 (e48d696b1). Other main failures (test_site_ladders, test_site_text_tokens, test_site_wide_blocks) predate #761 (same on 7cd0a94bf). Snapshot pre-release pr-761-snapshots and its tag deleted after merge, as planned; PR comment updated.
