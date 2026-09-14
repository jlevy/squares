---
type: is
id: is-01m2gyj13czgw7vy7p6xsj0sxy
title: Keyboard shortcuts fire under Cmd, so Cmd+C hides the controls
kind: bug
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2gyhqfmr0xpcjsr34na3acq
created_at: 2026-09-14T21:53:17.931Z
updated_at: 2026-09-14T21:53:57.199Z
---
Owner, 2026-09-14: "when I try to copy-paste or click on the main diagram, the controls disappear."

Reproduced headlessly on the built page: Meta+C sets `body.capture`, and `body.capture #controls { display: none }` hides every control. The window keydown handler switches on `ev.key` with no modifier check, so Cmd+C reads as `c` and toggles capture. The same applies to Cmd+A (play all), Cmd+S (snap), Cmd+P (style), Cmd+D, Cmd+B and Cmd+L. PR #160 has the same handler without a guard.

A click on a square or on empty diagram did not hide the controls in Pack mode. Re-test in Animate mode, where a click grabs a square and starts the optimiser, before closing that half.

Fix: shortcuts ignore any keydown with Meta, Ctrl or Alt held, so browser and OS shortcuts pass through. Consider also moving capture off a bare letter, since capture is a recording mode rather than a viewing toggle. Accept: Cmd+C, Cmd+A and Cmd+S leave the page state unchanged; `c` and Escape still work without modifiers.
