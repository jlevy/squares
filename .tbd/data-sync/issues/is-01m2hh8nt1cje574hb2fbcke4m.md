---
type: is
id: is-01m2hh8nt1cje574hb2fbcke4m
title: "PR #160 review D83: three small page defects: double loop, sticky dragging, step buttons stuck on gaps"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T03:20:14.400Z
updated_at: 2026-09-15T03:32:53.469Z
closed_at: 2026-09-15T03:32:53.468Z
close_reason: "Fixed on PR #160 in 3f8c49b7: tick asks for a frame only while playing and only once; body.dragging clears before the early return; adjacentSupportedStep moves Prev/Next across gaps (Node test); check_animate_view counts tick requests per frame and presses Home mid-drag."
resolution: null
duplicate_of: null
---
Canonical defect D83 from the 2026-09-14 stack triage (Low). Source: #125 F33.

Three small page defects: a pause inside `tick` still re-requested a frame, so play-before-next-frame ran two loops; `body.dragging` stuck if a key replaced the run mid-drag; Prev and Next could not cross gaps on the 25-pair page.

Files: `packages/workbench/src/application.js` (~:4513-4535, ~:5841-5851, ~:5583), `packages/workbench/src/core/navigation.ts` (:32-47) @bb3f7c99.
