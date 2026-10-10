---
type: is
id: is-01m4ksxx124ta571t8cz7e80st
title: Reduce shared uppercase button and toggle label sizes
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T21:01:31.039Z
updated_at: 2026-10-10T21:04:33.031Z
started_at: 2026-10-10T21:03:18.577Z
---
Make all-caps button labels a little smaller throughout the shared design system, including action buttons, tabs and toggle controls. Adjust common size tokens rather than local overrides; preserve accessible control hit areas, arrow sizing and wrapping. Document final values and verify representative buttons and Atlas toggles.

## Notes

Implemented shared --paper-button-label-scale:0.9. Site action labels scale the existing note size; shared tabs/toggles scale navigation label size; common workbench buttons scale body size. Original action/tab line boxes, padding and workbench fixed control heights retained. CSS Biome check of four changed stylesheets passed. Final browser verification and Astra review pending.
