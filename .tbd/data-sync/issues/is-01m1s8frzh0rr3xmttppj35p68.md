---
type: is
id: is-01m1s8frzh0rr3xmttppj35p68
title: "Atlas badges: derive glyph centring and size the star to the badge box"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T17:05:03.473Z
updated_at: 2026-09-05T17:10:13.698Z
closed_at: 2026-09-05T17:10:13.698Z
close_reason: "Done in 6021f6dc: _badge_baseline derives a letter's baseline from the cap height, so R sits level with O; only O had been tabulated and every other letter fell through to the math-symbol baseline meant for = and ~. The star is scaled to 92% of the badge box so it carries the weight of the lettered badges beside it."
resolution: null
duplicate_of: null
---
Owner 2026-09-05: the star read smaller than the lettered badges beside it, and R sat high because only O was tabulated and every other letter fell through to the math-symbol baseline meant for = and ~. Derive the baseline from the cap height for letters, keep the measured math baseline for symbols, and scale the star to the badge box.
