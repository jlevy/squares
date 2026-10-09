---
type: is
id: is-01m4f2239ewxyae710qvy3tw45
title: Expand the homepage Atlas in place with an Explore destination
kind: feature
status: in_progress
priority: 1
version: 7
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
updated_at: 2026-10-09T03:54:38.538Z
started_at: 2026-10-09T00:48:47.737Z
---
Keep native SVG Atlas drawings, colors, bound labels and case popovers in a compact two-row homepage preview. Reuse the dedicated Atlas SiteAtlasView layout and animation engine. Prepare all remaining drawings during page initialization so Expand immediately animates all 324 cases into triangle view without a click-time request or delay. Collapse reverses the shared animation to the compact preview. Keep Explore, shared double chevrons, themes, keyboard state and no-JavaScript destinations. Preserve the existing two-megabyte homepage ceiling.

## Notes

Implemented shared double-chevron convention: homepage Expand uses double-down, expanded Collapse uses double-up; loading/failure and cached expansion preserve correct state. Dedicated Atlas already follows same convention. Two bounded toggle browser cases passed; shared mask paints correctly. Updated design-system specification. Latest combined core draft rebuilt and served at127.0.0.1:8766.
