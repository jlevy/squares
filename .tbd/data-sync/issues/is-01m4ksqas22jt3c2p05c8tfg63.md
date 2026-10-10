---
type: is
id: is-01m4ksqas22jt3c2p05c8tfg63
title: Center visible Atlas rows and animate expansion on both pages
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T20:57:55.731Z
updated_at: 2026-10-10T20:58:07.606Z
started_at: 2026-10-10T20:58:07.605Z
---
Center homepage and dedicated Atlas canvases based on currently visible rows, rather than full hidden coverage. Preserve shared upstream geometry, complete Grid/Triangle row cutoffs, homepage36→100→324→36, dedicated preview/full controls, case links/popovers and mobile panning. Expansion/collapse must smoothly animate centering with shared FLIP; reduced motion settles immediately. Verify desktop/mobile stages, then commit/update PR462 and local preview.
