---
type: is
id: is-01m4ft8nnwh5gkkg6z5z10gsp6
title: Standardize explanatory web tooltips for evidence icons and levels
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-09T07:50:26.225Z
updated_at: 2026-10-09T08:30:51.652Z
started_at: 2026-10-09T07:51:04.801Z
closed_at: 2026-10-09T08:30:51.651Z
close_reason: null
resolution: null
duplicate_of: null
---
Provide meaningful shared styled tooltips for case-property icons such as optimal/exact/rigid and S/V/C levels wherever shown on web pages or popovers. Reuse the existing tooltip system and shared design transitions, with keyboard and reduced-motion support. Preserve PDF graphics and scientific meanings.

## Notes

Implemented shared KPress-based tooltips for property badges, stars and all S/V/C levels across ordinary/nav/paper/Workbench shells and fetched popovers. Uses common motion/style tokens, accessible focus/touch/Escape, native no-JS title fallback, reduced-motion support, viewport fitting and focused-scroll repositioning. Eight retained browser checks passed in16.83s; all17 rung meanings, vendor table-edge negative control and real paper footnote/code-copy runtime coexistence covered. CI ownership contract corrected for four new site suites and passed4.10s; Ruff, BasedPyright, Workbench tsc, Biome and diff checks clean. Published immutable assets to486 existing HTML files without pruning, preserved325 case files/118 result files, rebuilt actual Workbench app. Live smoke passed actual Workbench, ResultsV3, fetchedcase291 and paperfootnote preview with zero page errors. Published paper has no code blocks; retained fixture covers code-copy. Astra source review and Workbench/Results screenshots clear. Durable rating-tooltip-live-report.json and four screenshots saved in current visualization directory.
