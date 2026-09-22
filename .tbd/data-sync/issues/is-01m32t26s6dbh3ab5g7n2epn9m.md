---
type: is
id: is-01m32t26s6dbh3ab5g7n2epn9m
title: Move the n headline above the gap bar and head the bar KNOWN BOUNDS
kind: feature
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-21T20:21:04.933Z
updated_at: 2026-09-21T20:21:36.876Z
---
Owner's request, restructuring the stage's right column:

- `n = 100` moves from below the packing box to the upper right, above the gap bar.
- A small heading, styled like PROVEN (`.section-head`, uppercase, quiet, tracked), sits above the number bar and all its labels, reading KNOWN BOUNDS.

The column then reads top to bottom: `n = ...`, KNOWN BOUNDS, the bar with its ticks and sqrt labels, PROVEN with the bound and badges, OPEN, and the explanatory text think-kgx1 puts at the bottom.

This supersedes part of think-emuj: with the headline gone from under the box, the box can grow into the space it vacated, and the `n` size question becomes a question about the new position rather than the old one.

Everything in the right column below the bar shifts down by the headline's and the heading's height, so `.head-proved`, `.side`, `.badges` and `.head-open` all need re-measuring -- they are absolutely positioned at fixed tops in `packages/workbench/assets/workbench.css`.

The headline's rolling numerals are positioned by `layoutHeadline`, which measures once the faces land and sets `--stage-numeral-left`; moving the headline means that measurement has to follow it, and `displayedCount` drives which n it shows mid-transition, so the roll must keep working in the new position.

Do this together with think-sc44 (wider column) and think-emuj (bigger box): all three move the same middle gap, and each is only measurable against the others. Verify in a captured frame at 1920x1080.
