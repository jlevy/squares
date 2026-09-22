---
type: is
id: is-01m34zwwd9afe3tnppn4e8s9kr
title: Playback pauses for one frame at the end of each moving step and at the move's join to its tightening
kind: bug
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels: []
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-22T16:41:30.792Z
updated_at: 2026-09-22T20:14:47.042Z
---
Measured on the 2026-09-21 cuts (commit 17dcb3f92) with squares-workbench-check-cadence --verify, which re-draws each flagged frame from the page. In playback, the path the video records, the page holds still for one frame where a fresh draw of the same instants keeps moving:

- The last frame of a moving step, t = 3.017 s of 3.028: into 5, 10, 17, 52, 56, 72, 90 and others. The squares reach their place a frame early and hold (a fresh draw moves 1,100 to 4,500 pixels there).
- Mid-move at t = 2.417 s, 19 frames before blocksEnd, the same instant in every moving step that shows it (into 20, 130): the join between the physics move and its tightening phase (physicalPresentationProgress's knee at move / (move + correct)). A duplicate trajectory state at that join would stop playback for a frame.

41 of 33,626 frames in the full ascent and 16 of 9,579 in 1..100: one sixtieth of a second each, but a visible hitch in otherwise smooth motion. Separately, 39 frames of the full ascent draw differently walked to than jumped to, by sub-pixel edge positions across the whole packing, so the page's drawing of an instant depends on how it got there; that is the likely common cause. The capture itself is faithful: no kept frame is the page one frame early, and fidelity against the page's frames is 48 to 51 dB PSNR. Find the history dependence, fix it at its source, and add a check_animate_view section that plays a moving step in real time and requires no held frame inside motion.

## Notes

Updated 2026-09-22, lane on claude/workbench-full-ascent-video. The dominant shape is named and
measured, and it is not a held frame: it is the container box blinking out for one frame.

Measured on a fresh n = 2..24 cut at 60 fps with citations, from the page the 2026-09-22 delivery
was cut from (sha256 d99c3919...), /Volumes/spud-ext1/squares-video/tmp/cadence-lane/before-n2-24.mp4:
21 repeated frames inside motion, clock exact. `--verify` says 17 of the 21 are the page's own --
a fresh draw of both instants holds there too -- and 0 of the other 4 are the capture one frame
early, so the capture is faithful and every finding is the page.

WHAT THE FRAMES SHOW. Cropping the box's corner out of the kept PNGs across a finding (frames
87..95, step into 3) shows the packing's green container outline present, VANISHING for exactly
one frame, and present again, with the arriving square's fade starting two frames later. The
change either side of the "repeat" is 13,578 px at a peak of 121 grey levels spread over the
box's own frame -- a stroke going out and coming back, not anything moving.

THE CAUSE, in `packages/workbench/src/application.js` `drawBounds` (the `else if` branch, the
line `ink = easeInOut(ramp(t, sc.containerStart, sc.containerEnd))`). Through the dwell the box is
drawn at `Math.min(from, open)` with `ink = 1`; from `moveStart` it is drawn at `open` with `ink`
eased from ZERO, so the outline darkens into the grey trace. That is right when the box took a
larger side and wrong when it did not: on a step that does not resize the box -- every grid fill,
where `Math.min(from, open) === open` -- the outline is already at `open` at full ink, there is
nothing to darken into, and the ease blinks it out. At the 4x grid-fill speed-up the whole ease is
under two frames, so what a viewer sees is a one-frame flicker of the frame around the packing.
The cadence check then reports the frame AFTER the recovery, which sits in the arrival delay with
nothing scheduled, and calls it a repeat inside motion.

PROPOSED FIX (one line, not applied -- this lane does not own `drawBounds`):
    ink = Math.min(from, open) === open ? 1 : easeInOut(ramp(t, sc.containerStart, sc.containerEnd));

MEASURED EFFECT. The same n = 2..24 cut from a copy of the built page carrying exactly that line
(attic, not committed): 21 repeated frames -> 9, still frames 962 -> 993, clock unchanged.

WHAT REMAINS, from `--detail --frames` on the patched cut:
- 2 (frames 305, 731) and 1 (frame 1506) are frames the MEASURING SIZE calls repeats: a full-size
  diff moves 4,460 / 2,184 / 2,604 px there, which 480x270 area-averaging puts under the threshold.
  `--verify` agrees -- a fresh draw moves. Frame 1506 is this bead's mid-move knee (18 frames before
  blocksEnd, `physicalPresentationProgress`'s knee and `applySnapLanding`'s anchor in
  `packages/workbench/src/simulation/trajectory.ts`): motion falls from ~56,000 px/frame to 2,604
  for one frame and climbs back. Real, and a velocity discontinuity rather than a held frame.
- 2 (frames 1129, 1150, steps into 14 and 15) are the join between the arriving square finishing
  its fade at `arrived` and the facts column starting its handover at `TEXT_HANDOVER.outStart` of
  the roll. On the 4x-sped static beat that gap is about two frames with nothing scheduled in it.
- 3 (frames 160, 586, 1214) are the dwell's view-opening ease (`holdInView` under
  `seen = smootherstep(ramp(t, 0, sc.moveStart))`) reaching its zero-slope end, then the box taking
  `open` at `moveStart`.
- 1 (frame 25, the step into 2) is the `ink` ease's own zero-slope START on a step that really does
  resize the box, so the guard above does not reach it.

TOOL. `packages/workbench/tools/workbench_tools/cadence.py` now places a finding at the instant the
capture seeked to, on the beat the cut was priced at. It used to read the page in whatever state it
opens in, which is not the state a capture cuts from: the page prices the step into 2 at 2.692 s
where the cut plays it in 1.383 s, so every instant a finding was named against was wrong -- the
findings above were reported as "-1 frames from moveStart" when they sit at `arrive`. `--detail
--frames` also now prints what changed either side of a finding, with the peak and the stage box,
which is how the blink was named.

AT FILM LENGTH. The same n = 2..100 cut the 2026-09-22 delivery is, re-made from the patched
copy of the same page, 9203 frames and the same clock:

  delivered  73 repeated frames inside motion, 4441 still frames
  patched    29 repeated frames inside motion, 4560 still frames

So the box blink is 44 of the 73, and the film is still not smooth. The 29 that remain, placed
by `--detail` on the beat the cut played:

  12  prefix steps, one or two frames after `arrived`: the gap between the arriving square
      finishing its fade and the facts column starting its handover at TEXT_HANDOVER.outStart
      of the roll. This is the shape reported as "the end of a move" -- frame 44 of the
      delivered cut is one of them, and it is 1 frame before `arrived`, not 8 after moveStart.
   8  matched steps, the last frame of the step: a fresh draw moves 2,184 to 4,460 px there,
      which 480x270 area-averaging puts under the repeat threshold. Not a held frame.
   5  matched steps, two to ten frames after `arrive`.
   3  matched steps, at `moveStart`: the dwell's view-opening ease (`holdInView` under
      `seen`) reaching its zero-slope end, then the box's stroke cut to zero ink at moveStart.
   1  the mid-move knee, 18 frames before blocksEnd.

Files (transient, on the external disk):
  /Volumes/spud-ext1/squares-video/tmp/cadence-lane/before-n2-24.mp4
  /Volumes/spud-ext1/squares-video/tmp/cadence-lane/after-box-ink-n2-24.mp4
  /Volumes/spud-ext1/squares-video/tmp/cadence-lane/after-box-ink-n2-100.mp4
