---
type: is
id: is-01m3319g2ggyq2yrrtth7xzxkv
title: Make the colour transition duration a setting in seconds
kind: feature
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-21T22:27:23.846Z
updated_at: 2026-09-21T22:27:23.846Z
---
Owner's request: the speed at which a square's colour changes should be its own setting, in seconds, rather than following the step's clock.

Why it matters, measured on the run of static appends n = 96..100 at 30 fps: every frame-to-frame change is confined to ONE square's cell, span 97 px, and nothing spans the packing -- the geometry is completely still. What changes is a single square's colour, and it changes over about two frames, because a static append is a simple transition and plays at SIMPLE_TRANSITION_SPEED (now 3x). Two frames is not a transition; it is a cut, and on the blend through neutral it lands as a grey frame.

A colour duration declared in seconds would be independent of the step's own beat and of the speed-up, so a grid fill that plays in 0.46 s can still cross its colours over, say, 0.3 s and read as a blend rather than a flash.

The blend itself is `mix` in `packages/workbench/src/view/colour.ts`; what schedules it is `scene.presentation.resting` and the drain schedule in `application.js`. The setting belongs beside the other timing controls (THE STEP ANIMATION: dwell, move, correct, settle) rather than in THE VIEW, since it is a duration.

Needs a UI control, a public API setter and a capture command, like `hold square colours`.
