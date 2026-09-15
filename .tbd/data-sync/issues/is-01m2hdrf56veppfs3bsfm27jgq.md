---
type: is
id: is-01m2hdrf56veppfs3bsfm27jgq
title: Animate a resizing container's outline in trajectory SVGs
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-15T02:18:57.573Z
updated_at: 2026-09-15T02:18:57.573Z
---
Follow-up from PR #125 review D22 (think-mpjj, fixed in a6b53082).

A trajectory SVG whose container side changes (every atlas ascent step, exported on #160 by packages/workbench/tools/workbench_tools/animation_render.py) draws one container outline at the final frame's side and never animates it; the control `container_change_renders_one_outline_at_the_final_side` in packing/devtools/check_svg_rendering.py now pins that. The panel is also sized from the final side only, so a larger earlier container would draw past it.

Animating the outline needs the motion CSS grammar in packing/src/sqpack/render/svg.py `_validate_motion_css` widened (it admits only translate, rotate, saturate and transform-origin:center). Options measured by the delegate: allow `scale(k)` after translate with a constant stroke (vector-effect or counter-animated stroke-width); allow a fill-box corner origin plus scale; scale a wrapping group so box and squares move together; or two clipped L-shaped outline pieces moved by translate (fragile). `container_keyframes` (opacity only) and `append_container_motion` (never called) are dead until then. A renderer safety-policy change: needs an owner call.
