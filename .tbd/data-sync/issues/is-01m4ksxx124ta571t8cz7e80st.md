---
type: is
id: is-01m4ksxx124ta571t8cz7e80st
title: Reduce shared uppercase button and toggle label sizes
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T21:01:31.039Z
updated_at: 2026-10-11T01:13:23.117Z
started_at: 2026-10-10T21:03:18.577Z
closed_at: 2026-10-11T01:13:23.117Z
close_reason: Implemented and source-reviewed in PR462 at 53c8d37a2. Final ordinary Packing38100510883 and Pages38100510886 pass, including frontend and publication assembly. Shared Row outlines match width/alignment and paint gray behind black; web case/Atlas/table data retain ordinary ink. Later neutral-number and shared-spacing requests supersede earlier red-number/spacing intents. Final deferred/merge/deploy remain tracked separately by think-mvh7, think-21wu and think-xio5; controlled CI-performance follow-up remains think-ht59.
resolution: null
duplicate_of: null
---
Make all-caps button labels a little smaller throughout the shared design system, including action buttons, tabs and toggle controls. Adjust common size tokens rather than local overrides; preserve accessible control hit areas, arrow sizing and wrapping. Document final values and verify representative buttons and Atlas toggles.

## Notes

Shared --paper-button-label-scale:0.9 applies contextual action/tab/toggle and common Workbench button/chip label sizes. Line boxes, padding and fixed Workbench control heights preserved. Both desktop/mobile homepage browser checks verify actual 90% sizes for actions/tabs. CSS floors and Astra final review pass; identified chip cascade override fixed. Commit and exact-head CI pending.
