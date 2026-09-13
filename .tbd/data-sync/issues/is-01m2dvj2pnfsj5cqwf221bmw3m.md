---
type: is
id: is-01m2dvj2pnfsj5cqwf221bmw3m
title: A throwing Pack step stops playback visibly instead of leaving the page marked playing
kind: bug
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p88qyq83eek30pja3np54
created_at: 2026-09-13T17:03:10.548Z
updated_at: 2026-09-13T17:03:10.548Z
---
Review 2026-09-13: with the shared kernel, API misuse that yields a NaN pose or pinned position (e.g. grab(i, 'x') then a drag) throws inside tick(), which stops the animation loop while state.playing stays true, so the page looks like it is playing. grab() sets state.optimizing before createPackRun validates the scene poses. With infinite poses advancePackRun stops after one base step and optimizeStep discards the nonfinite termination reason. The old optimizer hung the tab on the same input, so this is already better; make it explicit: validate before arming, pause and surface the reason. Also remove the now-unused wallForce in application.js.
