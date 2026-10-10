---
type: is
id: is-01m4kwy8y1d871rvz1jdsdysvf
title: Remove recent-result stars from Atlas tiles
kind: bug
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
created_at: 2026-10-10T21:54:08.961Z
updated_at: 2026-10-10T22:01:21.711Z
started_at: 2026-10-10T21:54:22.652Z
---
Keep new-result stars on case/result records, but remove them from Atlas tile numbers and tile accessible names on homepage and Atlas. Preserve upstream PDF rendering, which already uses no per-card red stars. Audit upstream square-rendering and print changes for regressions.

## Notes

Removed the web-only Atlas star helper, recent-result tile wording, and obsolete star positioning; tiles now show counts only. Case/result stars and upstream print markers remain unchanged. Fetched origin/main and confirmed the print generator differs only in legend sizing and the shared square-rendering implementation is unchanged. Live page refresh is published; existing star-specific contracts are being migrated to the new behavior. Final-head CI remains pending.
