---
type: is
id: is-01m32ypsxmkf33wwk99djtqd52
title: Never animate the container line growing; darken the grey in place instead
kind: feature
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-21T21:42:14.194Z
updated_at: 2026-09-21T21:55:12.689Z
closed_at: 2026-09-21T21:55:12.688Z
close_reason: The box takes the larger side at once and darkens in place; only shrinking is animated.
resolution: null
duplicate_of: null
---
Owner's request for the full animation. The container must get larger from one n to the next, and today it does that by animating the drawn box outward -- a line growing from within. The owner wants growth never animated, so the box only ever reads as shrinking:

- Keep the shrinking animation of the green box, and the shrinking of the outer box.
- Never animate the line growing.
- Where the box has to become larger, the LIGHT GREY outer box darkens in place rather than the green growing out to meet it.

The story it should tell, in order: the green shrinks; the light grey is what is left behind, the previous extent; once the optimisation is active the light grey darkens in place; then it shrinks and becomes dark green again.

The three elements are in `packages/workbench/assets/template.html`: `#container` (the drawn container), `#bound-trace` (the light grey trace of where the box just was) and `#bound-box` (grey where it is, turning green when it locks at the best known side). Their colours are `--scene-frame`, `--scene-trace` and `--scene-frame-locked`.

What to work out before changing anything: which of the three is animated on a step today, whether the trace is already sitting at the larger side when the step begins (if it is, the change is mostly a colour schedule rather than a geometry one), and how this interacts with `setGrowth`, whose 'start small and grow' control is a separate feature that deliberately does animate growth.

Verify on a step where the side jumps, and in a captured frame rather than only in the browser.
