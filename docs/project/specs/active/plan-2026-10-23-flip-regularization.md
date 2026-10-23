# Feature: Flip Regularization

**Date:** 2026-10-23 (last updated 2026-10-23)

**Author:** Claude, for the owner (bead think-l2i6)

**Status:** In Review

## Overview

Packings arrive in whatever pose their source published, so neighbouring tiles of the
atlas are rotated or mirrored against one another and the figure reads as chaotic.
This adds one stage to the regularization process, which the owner named flip
regularization: each count’s drawn picture is turned by one of the container’s eight
symmetries into a canonical pose, chosen from where its squares lie.
The stage is drawing only; no certificate, witness or view changes.

## Goals

- One deterministic pose per count, decided in binary64 floating point from the drawn
  picture alone, so the same packing in any of its eight poses draws the same way.
- The owner’s rule, with the owner’s choice of corner: the heaviest quadrant (by filled
  area) lower right, then the heavier of its two neighbours lower left; the opposite
  quadrant follows.
- Keep the published pose wherever the rule allows, the well-known packings above all (n
  = 11), and the catalogues’ habit for the integer grids.
- A separate, fast stage: its own record and check, decided in seconds, applied by every
  surface that draws the default picture.
- Documented once, in the regularization policy, with the process guide and the atlas
  README pointing at it.

## Non-Goals

- Changing any witness, view, certificate, side, digest, evidence tier or credit.
- Reorienting the house drawing *as published* (the Original toggle and the case page’s
  *As published*), which stays in its source’s pose.
- Rewriting the one registered atlas isometry, n = 211’s mirror in
  `devtools.atlas_orientation`, which is history (see its docstring).

## Background

The owner, 23 October 2026: divide the container down the middle into four quadrants,
weigh the squares filled in each, and rotate or flip by those weights; “first rotate to
put the heaviest quadrant, and then flip if necessary”; ties broken by “some other
arbitrary way to make it deterministic”; floating point is sufficient, since this is
only for the drawing.
The first version put the heaviest quadrant upper left.
Seeing it, the owner moved it to the lower right, so that “the really well-known ones
should not change, like n = 11”, and asked that the rule match “what the conventions are
for the common ones as much as possible”, and that the stage be “completely separate
from the other regularization” and fast.

The container’s symmetry group has eight elements and the four quadrants have 24
orderings, so a full ordering by weight cannot always be had.
A rotation fixes which quadrant is lower right, and the one flip that keeps the
lower-right quadrant in place, the mirror across the upper-left to lower-right diagonal,
decides which of its two neighbours is lower left.
The upper-left quadrant is then forced: it is the one opposite the heaviest, whatever
its weight. A diagonal packing, heavy at two opposite corners, so lies along that
diagonal.

### Prior Practice

A survey of 23 October 2026 found no orientation convention stated by any packing
catalogue: Friedman’s survey, Ellsworth’s catalogue and MathWorld say only “up to
symmetry”. Two habits exist without being stated.
Integer grids fill rows from the bottom, so their empty cells sit at the top right
(Ellsworth’s renderings and this repository’s grid witnesses); this rule keeps that.
Tilted bands mostly run from lower left to upper right (53 of 65 strips Evan Daniel
read). Evan Daniel’s regularizer ranks the eight poses too (`orient_score` in
`vendor/evand-regularize/search/regularize/reg.py`), by band direction, then empty area
toward the top right, and found no single key that reproduces every source’s pose.
Outside packing, the rule is the polyomino practice (the lexicographic extreme of the
eight images) with a chess endgame tablebase’s structure (a quadrant first, then the
diagonal mirror through that corner).
The policy said until now that regularization keeps the source orientation; that stays
true of every view and witness, and this stage changes only how the default picture is
drawn.

### Choosing the Order

With the heaviest quadrant fixed lower right, the remaining order and the tie-break
decide how many published poses survive.
Measured on the 324 default pictures of 23 October 2026, as the number of counts whose
published pose the rule keeps:

| Order of the quadrants | Finer grids | Kept |
| --- | --- | --- |
| lower right, lower left, upper left, upper right | quadrant by quadrant | **252** |
| lower right, upper left, lower left, upper right | quadrant by quadrant | 252 |
| lower right, lower left, upper left, upper right | row by row from the lower right | 104 |
| lower right, lower left, upper right, upper left | either | 104 |
| lower right first, upper right second | either | 64 |
| the first version: upper left, upper right, lower left, lower right | row by row | 56 |
| the best with the heaviest quadrant lower left | quadrant by quadrant | 195 |

Of the two orders that keep 252, the first is the owner’s two steps, a rotation then the
flip that decides the heavier neighbour, and is the rule.
It keeps n = 5, 10, 11, 19, 26, 27, 28, 37, 38, 52, 53, 55, 66 and 85 and every integer
grid, and turns 72 counts, mostly larger tilted packings whose sources publish them in
no common pose, and among the small ones 17, 18, 29, 39 and 41.

## Design

### The Rule

Read a picture’s quadrant weights in the order lower right, lower left, upper left,
upper right.
Of the eight poses, keep those whose weights are lexicographically greatest.
That is exactly “rotate the heaviest quadrant to the lower right, then flip if the upper
right is heavier than the lower left”.

1. **Weights.** A cell’s weight is the area of the squares inside it over the cell’s
   area, each square clipped to the cell as a convex polygon in binary64.
2. **Comparison.** Two weights within $10^{-9}$ are equal.
   The poses are filtered position by position: keep those within $10^{-9}$ of the
   greatest weight at that position.
3. **Ties: the same comparison inside each quadrant.** Where poses still tie, compare
   their 4×4 grids, taken quadrant by quadrant in the same order and inside each
   quadrant in the same order again, then 8×8 and 16×16 likewise.
4. **Ties beyond 16×16.** Compare the poses’ squares, each as its centre and its tilt
   (the angle modulo 90 degrees, in $(-45, 45]$), sorted from the bottom row and the
   right, and keep the pose whose list is least.
   The tilt is in the key because two mirror images can share every centre and differ
   only in the sign of their tilts.
5. **Symmetric packings.** Poses still tied must draw the same picture, the packing
   having that symmetry: the stage checks it square for square and fails loudly if not.
   Keep the first in the fixed order (no rotation and no flip first), so a symmetric
   packing keeps its published pose.

### Components

- `packing/devtools/flip_regularization.py`: the eight poses, the rule, the record’s
  `--update` and `--check`, and `poses()` for the renderers.
  It reads each count’s default picture from its retained rendering under
  `atlas/known-best/rendering/` or `regularized/rendering/`, whose coordinates carry
  about 28 digits, so no exact frame is built and all 324 counts are decided in a few
  seconds.
- `packing/atlas/known-best/flip-regularization.json` and its schema: the record.
- `devtools.build_known_best_atlas`: `frame_from_witness(..., pose=)` maps the exact
  corners before the frame’s scalars are built, which costs nothing measurable;
  `tile_frame` passes each card’s recorded pose.
- `devtools.render_frontier_page`: `packing_svg(pose=)` maps the drawing’s coordinates
  for the site; `default_svg` draws the default picture in its canonical pose.
- `devtools.default_drawings` is unchanged: which picture is drawn is its decision, and
  the pose is decided on that picture afterwards.

### API Changes

`flip-regularization.json`, one row per count: `{n, drawn, rendering, rotate, flip,
decided_by, quadrants}`. `rotate` is 0, 90, 180 or 270 degrees counter-clockwise about
the container’s centre, then `flip` says whether to mirror across the upper-left to
lower-right diagonal; each of the eight symmetries is exactly one such pair.
`quadrants` are the turned picture’s weights in the rule’s order.
The site’s `atlas/regularized/n-N.svg` becomes every count’s Regularized-mode picture in
its canonical pose (324 addresses, from 95); `atlas/house/n-N.svg` stays the house
drawing as published.

## Implementation Plan

### Phase 1: Flip Regularization

- [x] The rule module and its tests, including invariance under all eight poses.
- [x] The map in every default-picture renderer, and the site’s addresses.
- [x] The owner’s corner and a separate, fast stage with its own record and check.
- [x] Policy section, process-guide step, atlas README.
- [ ] Regenerate the composites under a new infographics edition; before and after
  figures.

## Testing Strategy

Unit tests of the weights, the eight maps, the lexicographic choice, each tie level, the
tolerance edge and invariance under the eight poses; the published pose kept at n = 11
and the grids’ empty cells at the top right; a records-tier check that the record is
what the rule decides; the existing drift checks of every regenerated artifact; a visual
check of the composites and the site.

## Rollout Plan

One pull request, with before and after figures in its description.

## Open Questions

- None open. Scope (default pictures turned, *as published* left alone) is the owner’s
  decision of 23 October 2026.

## References

- [Regularization policy, section 13](../../policies/regularization-policy.md#13-flip-regularization)
- [Regularization process](../../guides/regularization-process.md)
- [Atlas README, the default picture](../../../../packing/atlas/known-best/README.md#the-default-picture)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
