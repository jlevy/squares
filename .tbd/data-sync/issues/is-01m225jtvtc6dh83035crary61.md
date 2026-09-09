---
type: is
id: is-01m225jtvtc6dh83035crary61
title: Move the solver choice into the strategy group, and make timing and phasing Animate-only
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
created_at: 2026-09-09T04:07:27.865Z
updated_at: 2026-09-09T04:09:45.064Z
---
In flight in the v2-transitions prototype as of 2026-09-08.

Regroup the controls along the three axes a mode is a choice on (X-025: Scope, Strategy, Presentation), so the panel says which axis each control belongs to instead of listing everything at one level.

1. The solver choice joins the strategy group. Which solver runs -- the interpolated tween, or the physics -- is a strategy choice exactly as the force law, the relationship graph, growth and the annealing level are, and it currently sits apart from them.

2. The tween is unavailable in Pack. The tween interpolates between two given endpoints, so it needs a step from n to n+1 and has nothing to do in a single-n mode. Offering it in Pack advertises a solver that cannot run. Disable it there, and say why rather than leaving a control that reads as broken -- revision 12 recorded exactly that complaint about the Sweep standardising box, which 'is disabled in Pack rather than explained'.

3. Timing and phasing become Animate-only. Move duration, settle duration, dwell and the motion phase (simultaneous, rotate-first, slide-first) are presentation choices for a rendered range. In Pack there is no schedule to phase and the speed control is the only timing that means anything.

Prototype: packing/atlas/known-best/video/spikes/v2-transitions/. Notes: NOTES.md, revisions 9 and 12.
