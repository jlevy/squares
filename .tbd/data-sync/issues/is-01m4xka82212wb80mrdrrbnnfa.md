---
type: is
id: is-01m4xka82212wb80mrdrrbnnfa
title: Let homepage and Atlas atlas viewport use the full screen width
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
hold: null
hold_until: null
created_at: 2026-10-14T16:18:19.821Z
updated_at: 2026-10-14T16:20:30.072Z
started_at: 2026-10-14T16:20:30.059Z
---
User reports main Atlas viewport on homepage and atlas.html capped narrower than wide screens. Remove the artificial width cap for this viewport; preserve a small edge gutter, existing horizontal scrolling, all atlas views/sizes and Regularized/Original switching. Implement in a separate reviewable delivery from PR599 CI repair, apply site version/changelog policy and verify wide and narrow viewport behavior.
