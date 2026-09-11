---
type: is
id: is-01m263zys62s3y4gymq6yhdk3f
title: Lift rotation and the constant container in sqpack.render.motion
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-10T16:56:38.433Z
updated_at: 2026-09-11T01:49:05.242Z
closed_at: 2026-09-11T01:49:05.241Z
close_reason: Rows 1-5 done and committed (72ed5e4f). validate_translation_only_trajectory split into validate_motion_trajectory keeping poses-or-corners and non-decreasing time; square_keyframes appends rotate() negated for SVG's flipped y and wrapped to the short way round a quarter turn; the animation rule carries transform-box:fill-box and transform-origin:center; container_keyframes no longer refuses a changing side. Five tests in tests/test_render_motion.py, each on a case the old validator rejected.
resolution: null
duplicate_of: null
---
Phase 4. Four web surfaces exist and none share a renderer: the explainer site (packing/site/index.html) draws packings its own way; the motion lab has two of its own (devtools/render_packing_motion_lab.py and render_general_motion_lab.py); the v1 slideshow embeds 324 packings as pre-rendered SVG markup, 1,098 elements; the v2 workbench embeds the same packings as pose JSON and draws them in JavaScript at run time. Same objects, four drawings, two encodings.

Extract one function from a frame -- poses, container side, labels, palette -- to SVG, with no application state in it, and make the slideshow and workbench both call it. Two drawings of one object is the defect; a third drawing is not the fix.
