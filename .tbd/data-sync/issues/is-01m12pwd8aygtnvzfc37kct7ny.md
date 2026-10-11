---
type: is
id: is-01m12pwd8aygtnvzfc37kct7ny
title: "Composite: centre and enlarge the badge glyphs"
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-08-27T22:54:05.577Z
updated_at: 2026-10-06T08:28:58.176Z
closed_at: 2026-10-06T08:28:58.176Z
close_reason: "Done on main: build_known_best_atlas.py sets letters on the cap height and = / approx on the math axis by measurement (SUMMARY_MATH_GLYPH_BASELINE, SUMMARY_BADGE_FONT_SIZE)."
resolution: null
duplicate_of: null
---
The = glyph is not visually centred in its box, and = and the approx sign should both be slightly larger within the box bounds. Letters and math symbols centre on different metrics, so they need separate baselines.
