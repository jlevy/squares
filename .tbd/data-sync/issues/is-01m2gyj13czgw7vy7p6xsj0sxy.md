---
type: is
id: is-01m2gyj13czgw7vy7p6xsj0sxy
title: Keyboard shortcuts fire under Cmd, so Cmd+C hides the controls
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m2gyhqfmr0xpcjsr34na3acq
created_at: 2026-09-14T21:53:17.931Z
updated_at: 2026-09-14T22:16:21.487Z
closed_at: 2026-09-14T22:16:21.486Z
close_reason: "Fixed in c94054c4: the keydown handler ignores keys with Cmd, Ctrl or Alt held, so Cmd+C no longer enters capture mode (which hid the controls). check_workbench.py asserts Meta+c, Control+c, Meta+s, Meta+p and Alt+b leave state unchanged while bare c and Escape still work. Clicks, drags and double-clicks on the diagram were re-tested headless in Pack and Animate on the rebuilt page: controls stay visible (73 in Animate). The click report fits the same cause, a selection followed by Cmd+C. PR #160 has the same unguarded handler; carry the guard in the merge."
resolution: null
duplicate_of: null
---
Owner, 2026-09-14: "when I try to copy-paste or click on the main diagram, the controls disappear."

Reproduced headlessly on the built page: Meta+C sets `body.capture`, and `body.capture #controls { display: none }` hides every control. The window keydown handler switches on `ev.key` with no modifier check, so Cmd+C reads as `c` and toggles capture. The same applies to Cmd+A (play all), Cmd+S (snap), Cmd+P (style), Cmd+D, Cmd+B and Cmd+L. PR #160 has the same handler without a guard.

A click on a square or on empty diagram did not hide the controls in Pack mode. Re-test in Animate mode, where a click grabs a square and starts the optimiser, before closing that half.

Fix: shortcuts ignore any keydown with Meta, Ctrl or Alt held, so browser and OS shortcuts pass through. Consider also moving capture off a bare letter, since capture is a recording mode rather than a viewing toggle. Accept: Cmd+C, Cmd+A and Cmd+S leave the page state unchanged; `c` and Escape still work without modifiers.
