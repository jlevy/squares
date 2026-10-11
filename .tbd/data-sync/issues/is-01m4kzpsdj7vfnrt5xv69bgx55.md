---
type: is
id: is-01m4kzpsdj7vfnrt5xv69bgx55
title: Align Row-view packings bottom left within a darker reference square
kind: task
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
created_at: 2026-10-10T22:42:29.418Z
updated_at: 2026-10-11T01:13:23.214Z
started_at: 2026-10-10T22:43:17.919Z
closed_at: 2026-10-11T01:13:23.214Z
close_reason: Implemented and source-reviewed in PR462 at 53c8d37a2. Final ordinary Packing38100510883 and Pages38100510886 pass, including frontend and publication assembly. Shared Row outlines match width/alignment and paint gray behind black; web case/Atlas/table data retain ordinary ink. Later neutral-number and shared-spacing requests supersede earlier red-number/spacing intents. Final deferred/merge/deploy remain tracked separately by think-mvh7, think-21wu and think-xio5; controlled CI-performance follow-up remains think-ht59.
resolution: null
duplicate_of: null
---
For Row-scaled Atlas visuals, darken the gray reference square and align each packing at its bottom-left, leaving excess reference area only above and right. Preserve upstream tile geometry, square shapes and independent Fixed/Global scales.
