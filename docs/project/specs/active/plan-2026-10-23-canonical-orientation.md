# Feature: Canonical Orientation of Drawn Packings

**Date:** 2026-10-23 (last updated 2026-10-23)

**Author:** Claude, for the owner (bead think-l2i6)

**Status:** In Review

## Overview

Packings arrive in whatever pose their source published, so neighbouring tiles of the
atlas are rotated or mirrored against one another and the figure reads as chaotic.
This adds one stage to the regularization process: each count’s drawn picture is turned
by one of the container’s eight symmetries into a canonical pose, chosen from where its
squares lie. The stage is drawing only; no certificate, witness or view changes.

## Goals

- One deterministic pose per count, decided in binary64 floating point from the drawn
  picture alone, so the same packing in any of its eight poses draws the same way.
- The owner’s rule: the heaviest quadrant (by filled area) upper left, then the heavier
  of its two neighbours upper right; the opposite quadrant follows.
- Applied to every surface that draws the default picture (both composites, the homepage
  and atlas tiles, the frontier-survey thumbnail, the case page’s head drawing),
  recorded per count in `default-drawings.json`, and checked in the records tier.
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
weigh the squares filled in each, and rotate or flip so that the heaviest is upper left,
the second upper right, the third lower left and the fourth lower right; “first rotate
to put the heaviest quadrant, and then flip if necessary”; ties broken by “some other
arbitrary way to make it deterministic”; floating point is sufficient, since this is
only for the drawing.

The container’s symmetry group has eight elements and the four quadrants have 24
orderings, so the full ordering cannot always be had.
A rotation fixes which quadrant is upper left, and the one flip that keeps the
upper-left quadrant in place, the mirror across the upper-left to lower-right diagonal,
decides which of its two neighbours is upper right.
The lower-right quadrant is then forced: it is the one opposite the heaviest, whatever
its weight. A diagonal packing, heavy at two opposite corners, so lies along the
upper-left to lower-right diagonal.

### Prior Practice

A survey of 23 October 2026 found no orientation convention stated by any packing
catalogue: Friedman’s survey, Ellsworth’s catalogue and MathWorld say only “up to
symmetry”. Two habits exist without being stated.
Integer grids fill rows from the bottom left, so their empty cells sit at the top right
(Ellsworth’s renderings and this repository’s grid witnesses); this rule moves them to
the bottom right, which is the owner’s rule as stated.
Tilted bands mostly run from lower left to upper right (53 of 65 strips Evan Daniel
read), which the rule keeps.
Evan Daniel’s regularizer ranks the eight poses too (`orient_score` in
`vendor/evand-regularize/search/regularize/reg.py`), by band direction, then empty area
toward the top right, and found no single key that reproduces the sources’ poses.
Outside packing, the rule is the polyomino practice (the lexicographic extreme of the
eight images) with a chess endgame tablebase’s structure (a quadrant first, then the
diagonal mirror through that corner).
The policy said until now that regularization keeps the source orientation; that stays
true of every view and witness, and this stage changes only how the default picture is
drawn.

## Design

### The Rule

Read a picture’s quadrant weights in reading order, upper left, upper right, lower left,
lower right.
Of the eight poses, keep those whose weights are lexicographically greatest.
That is exactly “rotate the heaviest quadrant to the upper left, then flip if the lower
left is heavier than the upper right”.

1. **Weights.** A cell’s weight is the area of the squares inside it over the cell’s
   area, each square clipped to the cell as a convex polygon in binary64.
2. **Comparison.** Two weights within $10^{-9}$ are equal.
   The poses are filtered position by position: keep those within $10^{-9}$ of the
   greatest weight at that position.
3. **Ties: the same comparison on finer grids.** Where poses still tie, compare their
   4×4 grids of cells in reading order, then 8×8, then 16×16.
4. **Ties beyond 16×16.** Compare the poses’ squares, each as its centre and its tilt
   (the angle modulo 90 degrees, in $(-45, 45]$), sorted top row first and left to right
   within a row, and keep the pose whose list is least (the highest square first, then
   the leftmost). The tilt is in the key because two mirror images can share every centre
   and differ only in the sign of their tilts.
   No count needs this today.
5. **Symmetric packings.** Poses still tied must draw the same picture, the packing
   having that symmetry: the stage checks it square for square and fails loudly if not.
   Keep the first in the fixed order (no rotation and no flip first), so a symmetric
   packing keeps its published pose where it can.

Measured on the 324 default pictures of 23 October 2026: the quadrants alone decide 252
counts, the 4×4 grid 51, 8×8 18 and 16×16 3 (n = 254, 287, 322); 93 of the 165 quadrant
ties are the packing’s own symmetry.
The rule turns 268 pictures, 132 of them by the top-to-bottom mirror; 56 keep their
pose. Deciding all 324 takes about 14 CPU-seconds, nearly all of it reading witnesses.

### Components

- `packing/devtools/canonical_orientation.py`: the eight operations, the rule, and the
  map applied to exact corners.
- `devtools.build_known_best_atlas.frame_from_witness`: takes an operation and maps the
  exact corners before the frame is built, so colours, contacts and walls are computed
  on the oriented picture.
- `devtools.default_drawings`: decides each count’s orientation on its drawn picture and
  records it in `states[].orientation`; `--check` decides it again.
- Every renderer of the default picture reads the recorded operation.

### API Changes

`default-drawings.json` gains `states[].orientation`:
`{rotate, flip, decided_by, quadrants}`. The pose is stated as the owner’s two steps:
`rotate` is 0, 90, 180 or 270 degrees counter-clockwise about the container’s centre,
then `flip` says whether to mirror across the upper-left to lower-right diagonal.
Each of the eight symmetries is exactly one such pair, and the eight are enumerated in
that order, rotations without a flip first.
`quadrants` are the oriented picture’s four weights.

## Implementation Plan

### Phase 1: Orientation Stage

- [ ] The rule module and its unit tests, including all eight poses of an asymmetric
  packing deciding the same picture.
- [ ] The record field, schema and check.
- [ ] The map in `frame_from_witness` and every default-picture renderer.
- [ ] Regenerate the composites, site and records; before and after figures.
- [ ] Policy section, process-guide step, atlas README and changelog.

## Testing Strategy

Unit tests of the weights, the eight maps, the lexicographic choice, each tie level and
invariance under the eight poses; a records-tier check that the recorded orientation is
what the rule decides; the existing drift checks of every regenerated artifact; a visual
check of the composites.

## Rollout Plan

One pull request, with before and after figures in its description.

## Open Questions

- None open. Scope (default pictures oriented, *as published* left alone) is this plan’s
  reading of the owner’s request and is called out in the pull request.

## References

- [Regularization policy](../../policies/regularization-policy.md)
- [Regularization process](../../guides/regularization-process.md)
- [Atlas README, the default picture](../../../../packing/atlas/known-best/README.md#the-default-picture)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
