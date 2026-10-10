---
type: is
id: is-01m4ksqas22jt3c2p05c8tfg63
title: Center visible Atlas rows and animate expansion on both pages
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T20:57:55.731Z
updated_at: 2026-10-10T21:03:57.873Z
started_at: 2026-10-10T20:58:07.605Z
---
Center homepage and dedicated Atlas canvases based on visible rows. Use the same shared controls, legend, overview and initial100-square preview on both pages, expanding to324 with complete Grid/Triangle row cutoffs. Prepare hidden diagrams before reveal so artwork does not arrive incrementally; preserve first-paint responsiveness, shared FLIP animation, mobile panning, case links/popovers and reduced motion. Supersedes earlier36-square homepage staging. Verify representative desktop/mobile transitions, then update PR462 and local preview.
