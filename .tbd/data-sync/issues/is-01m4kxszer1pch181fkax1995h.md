---
type: is
id: is-01m4kxszer1pch181fkax1995h
title: Give section headings more consistent breathing room
kind: bug
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
created_at: 2026-10-10T22:09:16.757Z
updated_at: 2026-10-11T01:13:23.144Z
started_at: 2026-10-10T22:09:37.989Z
closed_at: 2026-10-11T01:13:23.144Z
close_reason: Implemented and source-reviewed in PR462 at 53c8d37a2. Final ordinary Packing38100510883 and Pages38100510886 pass, including frontend and publication assembly. Shared Row outlines match width/alignment and paint gray behind black; web case/Atlas/table data retain ordinary ink. Later neutral-number and shared-spacing requests supersede earlier red-number/spacing intents. Final deferred/merge/deploy remain tracked separately by think-mvh7, think-21wu and think-xio5; controlled CI-performance follow-up remains think-ht59.
resolution: null
duplicate_of: null
---
Check homepage section heading spacing, especially Squares Project Documentation. Increase shared space above and below major section headings with more above than below; remove conflicting margins so homepage and content pages follow one design-system rule.

## Notes

Latest refinement makes every ordinary site-page H1 use the centered sans-serif caps title style and shared 3.5rem above/2rem below margins without needing site-title. Low-specificity defaults preserve dedicated compact case and popover headings. Removed competing generic subtitle-bottom rule. Live All Results vs homepage/About heading comparison pending.
