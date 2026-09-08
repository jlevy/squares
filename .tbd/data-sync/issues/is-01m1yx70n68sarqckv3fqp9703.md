---
type: is
id: is-01m1yx70n68sarqckv3fqp9703
title: Make square rotation handles usable on touch screens
kind: bug
status: closed
priority: 1
version: 5
labels: []
dependencies: []
parent_id: is-01m1ywjmdsmsjnxqbhd56er89j
created_at: 2026-09-07T21:43:28.677Z
updated_at: 2026-09-07T22:10:52.077Z
closed_at: 2026-09-07T22:10:52.069Z
close_reason: Completed in commit 330b1abd on PR117. All required CI and the paper build passed; local pre-push, browser interaction, and PDF visual checks passed. The remaining T-022 prose move is tracked separately as think-1lyz.
resolution: null
duplicate_of: null
---
User reports box handles depend on hover and work poorly on mobile/tap. Make both figure handles visible with touch targets and usable rotation while preserving page scrolling; verify touch and keyboard.

## Notes

Implemented visible 44 px native handles in Figures 5 and 6. Tap turns 5 degrees; drag captures touch; arrows turn 1 degree, or 10 with Shift. Canvas scrolling remains enabled and handles stay within its bounds. Real CDP touch checks passed for both certificates; independent review accepted.
