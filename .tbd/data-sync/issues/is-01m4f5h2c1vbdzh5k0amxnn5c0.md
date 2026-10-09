---
type: is
id: is-01m4f5h2c1vbdzh5k0amxnn5c0
title: Make the embedded SVG Atlas honor live light and dark themes
kind: bug
status: in_progress
priority: 1
version: 3
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
created_at: 2026-10-09T01:48:01.280Z
updated_at: 2026-10-09T01:48:13.814Z
started_at: 2026-10-09T01:48:13.448Z
---
The native homepage SVG Atlas retains a white poster background and fixed ink in dark mode. Use shared theme tokens for its background, labels and outlines while preserving packing geometry and hue semantics. Cover live light/dark/automatic theme changes in the initial two-row preview and full expanded graphic, cached collapse/re-expansion, and desktop/mobile. Keep exported poster SVG/PDF source artifacts unchanged.
