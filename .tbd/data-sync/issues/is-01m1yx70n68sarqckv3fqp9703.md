---
type: is
id: is-01m1yx70n68sarqckv3fqp9703
title: Make square rotation handles usable on touch screens
kind: bug
status: in_progress
priority: 1
version: 4
labels: []
dependencies: []
parent_id: is-01m1ywjmdsmsjnxqbhd56er89j
created_at: 2026-09-07T21:43:28.677Z
updated_at: 2026-09-07T22:04:00.708Z
---
User reports box handles depend on hover and work poorly on mobile/tap. Make both figure handles visible with touch targets and usable rotation while preserving page scrolling; verify touch and keyboard.

## Notes

Implemented visible 44 px native handles in Figures 5 and 6. Tap turns 5 degrees; drag captures touch; arrows turn 1 degree, or 10 with Shift. Canvas scrolling remains enabled and handles stay within its bounds. Real CDP touch checks passed for both certificates; independent review accepted.
