---
type: is
id: is-01m21pvfmt41mpzpwgqc569tst
title: Keep list bullets square in Elements of the project and other contexts
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T23:50:02.649Z
updated_at: 2026-09-08T23:58:58.979Z
---
Owner reports bullets under Elements of the project appear rectangular while others are square. Compare actual rendered marker width/height, layout and optical placement across serif/sans, screen/print and narrow views. Reuse the typography inspector; fix shared marker behavior upstream in KPress when applicable and verify no flex shrinking or line-height distortion. Preserve the already requested slight downward optical adjustment.

## Notes

Compared current reviewed page: all 29 visible unordered markers have equal computed width and height in desktop1280, narrow390, and print. Elements parent and three nested items are3.65625x3.65625CSSpx screen,3.25x3.25print. Existing check_print_layout marker geometry/preview tools retained measurements. No CSS shape defect found; fractional-position rasterization remains an unconfirmed optical hypothesis, not a reason to add a pixel-snapping runtime. Keep open for a matched1x/2x visual check. Crops under /private/tmp/squares-elements-marker-review.
