---
type: is
id: is-01m229amjwvykvfz1jhnjxdap9
title: Add restart, a best-known start, and a re-randomising random to the workbench
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-09T05:12:53.595Z
updated_at: 2026-09-09T05:12:53.595Z
---
In packing/atlas/known-best/video/spikes/v2-transitions/. Restart beside play and pause, defined as returning to the beginning of whatever play would play: in Pack the initial arrangement with settings kept, in Animate the first step of the range. Distinct from the existing reset, which restores parameters to defaults. Add a best-known start that loads the record's own packing for the current n; its purpose is diagnostic rather than a common start, so report drift from the loaded record. Change random to re-randomise on every press with the seed shown and typeable; it is currently seeded from n and so gives the same scatter every time, which is right for reproducibility and wrong for exploring.
