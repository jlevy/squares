---
type: is
id: is-01m225jsnny9dz3vjf9jadxy27
title: Show Pack at rest with all n squares, and put restart beside play
kind: task
status: in_progress
priority: 2
version: 3
spec_path: packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m225ps2ejkzyjc45g0xj6kyh
parent_id: is-01m225hw89vjsga1wnegrwnq5a
created_at: 2026-09-09T04:07:26.644Z
updated_at: 2026-09-09T04:09:45.058Z
---
In flight in the v2-transitions prototype as of 2026-09-08.

Two changes to what Pack shows and how it is driven.

1. Pack draws all n squares at rest. Pack is the single-n mode: a person picks an n, sets a strategy and watches or intervenes in one settle. It inherited its stage from the transitions animation, so it opens on a step from n-1 to n with a step header above it, which is Animate's picture and not Pack's. Pack should open on the n squares of the chosen n, at rest, in the starting arrangement the current settings ask for, with the step header gone. Revision 13 already made the starting size redraw the arrangement, so the machinery for staging a resting frame exists.

2. Restart sits beside play. The transport currently makes restarting a run an indirect act; a run that has drifted somewhere uninteresting should be restartable without hunting for the control that does it. Revision 13 recorded that the Optimize button reading 'Restart optimize' is the only sign that the size slider has changed what kind of thing the stage is showing, which is a weak signal; an explicit restart beside play is part of the fix.

Prototype: packing/atlas/known-best/video/spikes/v2-transitions/. Notes: NOTES.md, revisions 9, 12 and 13. Do not commit the prototype from this bead's branch without the coordinator.
