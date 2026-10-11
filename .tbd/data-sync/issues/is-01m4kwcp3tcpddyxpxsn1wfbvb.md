---
type: is
id: is-01m4kwcp3tcpddyxpxsn1wfbvb
title: Animate shared Atlas expansion height smoothly
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
created_at: 2026-10-10T21:44:32.629Z
updated_at: 2026-10-11T01:13:23.127Z
started_at: 2026-10-10T21:44:45.675Z
closed_at: 2026-10-11T01:13:23.127Z
close_reason: Implemented and source-reviewed in PR462 at 53c8d37a2. Final ordinary Packing38100510883 and Pages38100510886 pass, including frontend and publication assembly. Shared Row outlines match width/alignment and paint gray behind black; web case/Atlas/table data retain ordinary ink. Later neutral-number and shared-spacing requests supersede earlier red-number/spacing intents. Final deferred/merge/deploy remain tracked separately by think-mvh7, think-21wu and think-xio5; controlled CI-performance follow-up remains think-ht59.
resolution: null
duplicate_of: null
---
Animate the overall Atlas expansion and collapse using shared transition tokens on homepage and Atlas, preserving preloaded persistent tiles and immediate reduced-motion behavior.

## Notes

Implemented shared viewport height reveal using existing 360 ms Atlas duration/easing. Existing tile FLIP retained; follower transforms skipped during height animation to avoid double movement. WAAPI cleanup leaves no inline height. Six live geometry reads passed: homepage and Atlas at1280/390 have intermediate height frames; rapid mobile expand-collapse returns to727.5px with no animations; reduced-motion commits immediately. Biome, overview/probes tsc, Ruff, and25Node tests passed. Preview updated source=published=HTTP200; PDFs untouched. Review and publication pending.
