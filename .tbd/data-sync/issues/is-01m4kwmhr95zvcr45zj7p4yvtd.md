---
type: is
id: is-01m4kwmhr95zvcr45zj7p4yvtd
title: Use muted labels and primary values throughout detail sections
kind: bug
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
created_at: 2026-10-10T21:48:50.302Z
updated_at: 2026-10-11T01:13:23.132Z
started_at: 2026-10-10T21:49:08.821Z
closed_at: 2026-10-11T01:13:23.132Z
close_reason: Implemented and source-reviewed in PR462 at 53c8d37a2. Final ordinary Packing38100510883 and Pages38100510886 pass, including frontend and publication assembly. Shared Row outlines match width/alignment and paint gray behind black; web case/Atlas/table data retain ordinary ink. Later neutral-number and shared-spacing requests supersede earlier red-number/spacing intents. Final deferred/merge/deploy remain tracked separately by think-mvh7, think-21wu and think-xio5; controlled CI-performance follow-up remains think-ht59.
resolution: null
duplicate_of: null
---
Apply shared design-system detail colors consistently across standalone case records, table detail sections, and popovers: bold labels use the muted gray text token; values use the primary text token (black in light mode, readable light text in dark mode). Preserve emphasis, math and link styling. Verify the reported lower-bound section and representative result details in the live preview.

## Notes

Shared detail styles now make every dt muted gray and medium weight, with dd values in the primary theme text color. Removed conflicting case/table/popover and standalone-result overrides. Four live case 39/result T-115 light/dark checks pass. Source Biome and diff checks pass; final-head PR CI remains pending.
