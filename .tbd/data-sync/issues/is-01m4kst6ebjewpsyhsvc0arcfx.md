---
type: is
id: is-01m4kst6ebjewpsyhsvc0arcfx
title: Share homepage H1 spacing across website pages
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
created_at: 2026-10-10T20:59:29.610Z
updated_at: 2026-10-10T21:17:19.322Z
started_at: 2026-10-10T21:00:16.183Z
---
Increase margin above H1 section headings on About and other website pages to match homepage. Move spacing to shared design-system rule, preserve paper/print heading hierarchy and first-title behavior. Verify matching computed spacing on homepage/About and representative other page; document shared token.

## Notes

Shared screen-only --site-title-space-above:2.5rem applied to h1.site-title, homepage override removed. Both desktop/mobile homepage checks passed computed H1 margin equivalence across homepage/About; source CSS floor and final Astra review pass. Print rules retained. Commit and exact-head CI pending.
