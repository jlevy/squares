---
type: is
id: is-01m4f2239ewxyae710qvy3tw45
title: Expand the homepage Atlas in place with an Explore destination
kind: feature
status: in_progress
priority: 1
version: 5
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
updated_at: 2026-10-09T03:11:55.149Z
started_at: 2026-10-09T00:48:47.737Z
---
Keep the homepage Atlas as an embedding of the existing SVG atlas graphic, initially filtered to fewer rows rather than eight curated HTML tiles. Preserve Expand and Explore controls, full graphic expansion and collapse, accessible state and working destinations. Remove the inline explanatory selection/tile prose; show the graphic with concise navigation to the dedicated Atlas page. Latest owner steering supersedes the eight-tile preview.

## Notes

Owner refinement: all in-place expand/collapse controls use existing shared double-chevron icons, double-down when collapsed/Expand and double-up when expanded/Collapse. Homepage native SVG toggle must match dedicated Atlas expander; labels, aria-expanded, retry/collapse and cached expansion remain intact. Shared design-system and plan updated. Focused wiring/check and local refresh underway.
