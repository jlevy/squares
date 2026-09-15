---
type: is
id: is-01m2hh8eqnpbkh6w7x3pk1vgw4
title: "PR #160 review D14: a square dragged past the walls runs away from the cursor"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T03:20:07.156Z
updated_at: 2026-09-15T03:32:50.598Z
closed_at: 2026-09-15T03:32:50.597Z
close_reason: "Fixed on PR #160 in 2edbf3ba: the view is taken when a square is picked up and held until release; a real-mouse drag 150 px past the wall stays within 3 px of the cursor (123.9 px before) in check_animate_view."
resolution: null
duplicate_of: null
---
Canonical defect D14 from the 2026-09-14 stack triage (High). Source: #125 F6.

Dragging a square past the walls ran it away from the cursor: `renderOptimizeScene` re-fit the view to hold the held square on every frame, and `worldPoint` mapped each pointermove through the new screen matrix, pushing the square further out. Reproduced with a real mouse: a 65 px move took the square from world x 4.5 to 29.0; ten one-pixel jiggles to 124.2. Probes dragged in world coordinates, so none saw it.

Files: `packages/workbench/src/application.js` (`renderOptimizeScene` ~:3501-3514, `worldPoint` ~:5747, drag ~:3113-3124 @bb3f7c99); a real-mouse probe. The new Pack panel is not affected (`pack-scene.ts:16`).
