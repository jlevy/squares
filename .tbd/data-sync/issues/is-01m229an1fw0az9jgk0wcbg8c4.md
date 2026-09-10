---
type: is
id: is-01m229an1fw0az9jgk0wcbg8c4
title: Benchmark the workbench simulator from the command line, without a browser
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-09T05:12:54.062Z
updated_at: 2026-09-09T05:12:54.062Z
---
A browser reading conflates algorithm cost, paint cost and machine load. Measured context so nobody chases a phantom: the page is not slow. Headless it holds 120 frames per second at both n=17 and n=272, worst frame 10 ms, 358 DOM nodes, 10.7 MB heap, every API call under 2 ms; apparent sluggishness coincided with a five-minute load average of 116 caused by another session. Build a benchmark that runs the simulator's step function under Node with no DOM, the way packing/tests/test_motion_lab.py runs the motion lab's model with the nodejs-wheel-binaries dependency. Report steps per second and pair tests per second at n = 5, 17, 100, 272 for the physics and bodies solvers, fixed step count and seed. Write the table into the prototype's NOTES.md so a future regression can be attributed rather than argued about.
