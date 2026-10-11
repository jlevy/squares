---
type: is
id: is-01m4m00vmzadev17bhq1kk4zv1
title: Use shared small choosers for Atlas layout size and scale
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
created_at: 2026-10-10T22:47:59.390Z
updated_at: 2026-10-11T01:13:23.230Z
started_at: 2026-10-10T22:48:09.807Z
closed_at: 2026-10-11T01:13:23.230Z
close_reason: Implemented and source-reviewed in PR462 at 53c8d37a2. Final ordinary Packing38100510883 and Pages38100510886 pass, including frontend and publication assembly. Shared Row outlines match width/alignment and paint gray behind black; web case/Atlas/table data retain ordinary ink. Later neutral-number and shared-spacing requests supersede earlier red-number/spacing intents. Final deferred/merge/deploy remain tracked separately by think-mvh7, think-21wu and think-xio5; controlled CI-performance follow-up remains think-ht59.
resolution: null
duplicate_of: null
---
Reduce chooser text and button padding above the Atlas to the compact scale of Results widgets. Define and document a shared small chooser design-system variant and apply identically on homepage and Atlas.

## Notes

Shared site-chooser-small variant now uses Results control font size, 1.35 leading, 0.15rem by 0.65rem padding, and medium weight on all Atlas layout/size/scale strips. Shared action rows now own flex wrapping and 0.7rem gap, replacing the homepage-only Atlas spacing and fixing the touching Recent Results buttons. Preview/browser proof pending.
