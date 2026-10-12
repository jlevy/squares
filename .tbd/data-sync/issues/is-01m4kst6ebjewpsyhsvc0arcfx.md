---
type: is
id: is-01m4kst6ebjewpsyhsvc0arcfx
title: Share homepage H1 spacing across website pages
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T20:59:29.610Z
updated_at: 2026-10-11T01:13:23.107Z
started_at: 2026-10-10T21:00:16.183Z
closed_at: 2026-10-11T01:13:23.107Z
close_reason: Implemented and source-reviewed in PR462 at 53c8d37a2. Final ordinary Packing38100510883 and Pages38100510886 pass, including frontend and publication assembly. Shared Row outlines match width/alignment and paint gray behind black; web case/Atlas/table data retain ordinary ink. Later neutral-number and shared-spacing requests supersede earlier red-number/spacing intents. Final deferred/merge/deploy remain tracked separately by think-mvh7, think-21wu and think-xio5; controlled CI-performance follow-up remains think-ht59.
resolution: null
duplicate_of: null
---
Increase margin above H1 section headings on About and other website pages to match homepage. Move spacing to shared design-system rule, preserve paper/print heading hierarchy and first-title behavior. Verify matching computed spacing on homepage/About and representative other page; document shared token.

## Notes

Shared screen-only --site-title-space-above:2.5rem applied to h1.site-title, homepage override removed. Both desktop/mobile homepage checks passed computed H1 margin equivalence across homepage/About; source CSS floor and final Astra review pass. Print rules retained. Commit and exact-head CI pending.
