---
type: is
id: is-01m4ft8nnwh5gkkg6z5z10gsp6
title: Standardize explanatory web tooltips for evidence icons and levels
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-09T07:50:26.225Z
updated_at: 2026-10-09T08:22:40.320Z
started_at: 2026-10-09T07:51:04.801Z
---
Provide meaningful shared styled tooltips for case-property icons such as optimal/exact/rigid and S/V/C levels wherever shown on web pages or popovers. Reuse the existing tooltip system and shared design transitions, with keyboard and reduced-motion support. Preserve PDF graphics and scientific meanings.

## Notes

Shared rating-tooltips adapter reuses KPress placement/top-layer surface and common motion tokens for property badges, stars and S/V/C levels; dynamic case/result records and ordinary, paper, nav and Workbench shells are wired. Focus/touch/Escape, reduced motion, native no-JS titles, viewport fitting and keyboard focus-scroll are covered. Eight focused browser checks passed in 16.83s, including all 17 rung meanings, real paper footnote/code-copy coexistence and vendor table-edge negative control. CI ownership contract corrected for the four new website suites; focused contract passed 4.10s, Ruff clean. Astra source review has no remaining material findings. Final local asset publication and live smoke pending.
