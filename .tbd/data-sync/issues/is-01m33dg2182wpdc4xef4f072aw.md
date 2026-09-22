---
type: is
id: is-01m33dg2182wpdc4xef4f072aw
title: Slide the arriving scarlet square in from off the stage's upper right
kind: feature
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T02:00:41.767Z
updated_at: 2026-09-22T02:31:40.508Z
closed_at: 2026-09-22T02:31:40.504Z
close_reason: The owner tried the slide-in (first from off the upper right, then rising from below) and decided against it (2026-09-21). It was never committed; the working-tree changes were discarded, and the branch is back to 512bbf456 plus a real-time playback check.
resolution: canceled
duplicate_of: null
---
The owner (2026-09-21): instead of fading in where it lands, the new scarlet square should slide in from off the upper right of the screen to its place. Both renderers draw the arrival (illustrationFrame's arriving square and renderPhysicsScene's newNode), so the slide is one shared function; the start point is off the stage's upper-right corner, in scene coordinates at each frame's view, and the packing's SVG must not clip the square on its way in. Keep the landing, the scarlet hold and the crossing to its own color as they are, and move check_animation_editor's arrival assertions and the transition contract to the new behavior.
