---
type: is
id: is-01m1tx0qnedarbs6vtv362gg9j
title: "Deep gate: emission-precision negative controls fail during collection"
kind: bug
status: closed
priority: 2
version: 4
labels: []
dependencies: []
created_at: 2026-09-06T08:23:05.133Z
updated_at: 2026-09-06T08:36:25.696Z
closed_at: 2026-09-06T08:36:25.696Z
close_reason: Fixed in stacked PR 96 commit 8e0fba99. All required CI checks passed in run 34022006920; all45 selected pre-push steps and31 record steps passed locally, including558 reachable tests. Previously failing bounds audit and all affected negative controls now pass.
resolution: null
duplicate_of: null
---
Full local negative-control run reports collection errors instead of expected evidence for both emission precision field-refinement and renderer-context mutations. Diagnose snapshot test imports and preserve real mutant detection.

## Notes

Fixed in follow-up PR 96 commit 8e0fba99: Cairo imports deferred to PNG/PDF export. Both unchanged emission controls pass with DYLD unset; subprocess regression renders SVG with cairosvg blocked. Raster and PDF generation validated with Cairo configured.
