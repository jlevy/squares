---
type: is
id: is-01m4ft3dwbdg30fkjzrvg9mjnq
title: Use subtle shared scrollbars across website surfaces
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
created_at: 2026-10-09T07:47:34.409Z
updated_at: 2026-10-09T07:58:27.061Z
started_at: 2026-10-09T07:48:09.776Z
---
Use thin scrollbars with transparent tracks across web pages, popovers and horizontally scrolling diagrams, with thumb contrast appropriate to light and dark themes. Keep scrolling and existing controls functional; verify the local draft.

## Notes

Implemented once in shared paper-type.css: thin standard scrollbars, 6px WebKit fallback, transparent tracks/corners, and muted-theme thumbs at55% strength; forced-color mode keeps platform colors. Root reusable measure_site_scrollbars tool verifies html/page/popover/formula computed styles in light/dark: all thin, all tracks transparent, thumb colors change with theme. Ruff/Biome/probe types and diff checks passed. Shared preview stylesheet references refreshed across470 HTML files; final bounded design review pending.
