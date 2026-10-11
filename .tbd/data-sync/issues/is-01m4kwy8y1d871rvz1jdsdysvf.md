---
type: is
id: is-01m4kwy8y1d871rvz1jdsdysvf
title: Remove recent-result stars from Atlas tiles
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
created_at: 2026-10-10T21:54:08.961Z
updated_at: 2026-10-11T01:13:23.138Z
started_at: 2026-10-10T21:54:22.652Z
closed_at: 2026-10-11T01:13:23.138Z
close_reason: Implemented and source-reviewed in PR462 at 53c8d37a2. Final ordinary Packing38100510883 and Pages38100510886 pass, including frontend and publication assembly. Shared Row outlines match width/alignment and paint gray behind black; web case/Atlas/table data retain ordinary ink. Later neutral-number and shared-spacing requests supersede earlier red-number/spacing intents. Final deferred/merge/deploy remain tracked separately by think-mvh7, think-21wu and think-xio5; controlled CI-performance follow-up remains think-ht59.
resolution: null
duplicate_of: null
---
Keep new-result stars on case/result records, but remove them from Atlas tile numbers and tile accessible names on homepage and Atlas. Preserve upstream PDF rendering, which already uses no per-card red stars. Audit upstream square-rendering and print changes for regressions.

## Notes

Removed the web-only Atlas star helper, recent-result tile wording, and obsolete star positioning; tiles now show counts only. Live home and Atlas checks confirm all 324 persistent nodes have no tile stars or recency names; case 39 stars remain. Case/result stars and upstream print markers are preserved. Fetched origin/main; print changes are legend-only and square-rendering implementation is unchanged. Four focused source contracts passed in 25.04 seconds. Final-head PR CI remains pending.
