---
type: is
id: is-01m4ky4hmzta9p8qcdmm2g0nx2
title: Wrap long resource URLs within cards
kind: bug
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T22:15:03.070Z
updated_at: 2026-10-11T01:13:23.157Z
started_at: 2026-10-10T22:15:21.435Z
closed_at: 2026-10-11T01:13:23.157Z
close_reason: Implemented and source-reviewed in PR462 at 53c8d37a2. Final ordinary Packing38100510883 and Pages38100510886 pass, including frontend and publication assembly. Shared Row outlines match width/alignment and paint gray behind black; web case/Atlas/table data retain ordinary ink. Later neutral-number and shared-spacing requests supersede earlier red-number/spacing intents. Final deferred/merge/deploy remain tracked separately by think-mvh7, think-21wu and think-xio5; controlled CI-performance follow-up remains think-ht59.
resolution: null
duplicate_of: null
---
Ensure external repository URLs, including ry-xu links and arbitrary unbroken URL text, wrap within shared resource cards at all viewport widths. Apply the fix in the shared card design rather than one URL-specific override.
