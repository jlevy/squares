---
type: is
id: is-01m34zwwd9afe3tnppn4e8s9kr
title: Playback pauses for one frame at the end of each moving step and at the move's join to its tightening
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels: []
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-22T16:41:30.792Z
updated_at: 2026-09-22T16:41:30.792Z
---
Measured on the 2026-09-21 cuts (commit 17dcb3f92) with squares-workbench-check-cadence --verify, which re-draws each flagged frame from the page. In playback, the path the video records, the page holds still for one frame where a fresh draw of the same instants keeps moving:

- The last frame of a moving step, t = 3.017 s of 3.028: into 5, 10, 17, 52, 56, 72, 90 and others. The squares reach their place a frame early and hold (a fresh draw moves 1,100 to 4,500 pixels there).
- Mid-move at t = 2.417 s, 19 frames before blocksEnd, the same instant in every moving step that shows it (into 20, 130): the join between the physics move and its tightening phase (physicalPresentationProgress's knee at move / (move + correct)). A duplicate trajectory state at that join would stop playback for a frame.

41 of 33,626 frames in the full ascent and 16 of 9,579 in 1..100: one sixtieth of a second each, but a visible hitch in otherwise smooth motion. Separately, 39 frames of the full ascent draw differently walked to than jumped to, by sub-pixel edge positions across the whole packing, so the page's drawing of an instant depends on how it got there; that is the likely common cause. The capture itself is faithful: no kept frame is the page one frame early, and fidelity against the page's frames is 48 to 51 dB PSNR. Find the history dependence, fix it at its source, and add a check_animate_view section that plays a moving step in real time and requires no held frame inside motion.
