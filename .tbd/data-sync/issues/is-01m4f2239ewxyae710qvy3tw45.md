---
type: is
id: is-01m4f2239ewxyae710qvy3tw45
title: Expand the homepage Atlas in place with an Explore destination
kind: feature
status: in_progress
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels:
  - website
dependencies:
  - type: blocks
    target: is-01m4ex3gpzxxh9eqemc2r78p4e
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-09T00:47:24.965Z
updated_at: 2026-10-09T04:10:43.063Z
started_at: 2026-10-09T00:48:47.737Z
---
Keep native SVG Atlas drawings, colors, bound labels and case popovers in a compact two-row homepage preview. Reuse the dedicated Atlas SiteAtlasView layout and animation engine. Prepare all remaining drawings during page initialization so Expand immediately animates all 324 cases into triangle view without a click-time request or delay. Collapse reverses the shared animation to the compact preview. Keep Explore, shared double chevrons, themes, keyboard state and no-JavaScript destinations. Preserve the existing two-megabyte homepage ceiling.

## Notes

Local implementation now reuses SiteAtlasView via a scoped, control-free adapter. Persistent cropped native SVG links retain bound labels and colors; 36 initial cases in two rows, all324 prepared at initialization from byte-exact inert gzip source. Expand immediately invokes shared triangle/FLIP without click-time fetch; Collapse reverses with viewport settlement inside the shared mutation. Shared double chevrons and reduced motion retained. Three focused source/browser checks passed63.32s at1280/390, including node identity, zero fetch, scroll delta0, shared360ms/easing, reduced-motion0, no URL/global state writes and unclipped216x252 crops.21 shared-engine Node tests passed; refreshed dedicated controls/URL smoke passed. Ruff/Biome/TypeScript clean; homepage1,220,393bytes below2MB. Astra bounded source review has no remaining actionable findings; refreshed screenshots/theme confirmation pending. Localdraft only; publication gates tracked by think-xio5.
