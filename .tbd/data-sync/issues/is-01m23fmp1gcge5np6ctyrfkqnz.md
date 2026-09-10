---
type: is
id: is-01m23fmp1gcge5np6ctyrfkqnz
title: Generate LP sites by structure, not by arrangement vertex
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T16:22:28.656Z
updated_at: 2026-09-09T16:22:28.656Z
---
Generate LP sites from the structure of the obstruction rather than from arrangement
vertices. Vertex-by-vertex separation costs about 825 s a round, moves the value by
nothing, and the obstruction does not stay where it was cut.

Measured 2026-09-09 across agenda-033 lanes A3 and A4
(packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-a3-threshold-loop-at-383-100.md
addendum S2/S4, and .../lane-a4-separating-the-plateau-dual-at-153-40.md findings P5, P8,
P9).

The evidence, in the order it was found:

- A3 ran three site rounds at `153/40` with the depth-witness oracle. The value stayed at
  exactly eleven throughout. One round of 300 site columns cost about 825 s of warm LP and
  pushed the excess into a sliver `0.0006` wide, where the right edges of wall squares at
  `0.26` through `2.90` degrees interleave. S4's reading was that sites must be placed by
  the sliver's structure rather than one vertex at a time.
- A4 then showed the sliver is not even the right target. The `1/25`-integral dual A3
  produced is one vertex of a WIDE optimal face. A cold re-solve of the identical column
  set lands on a different vertex (64 rows and 512 placements, against the warm solve's 35
  rows and 280), and the two duals are not separated by the same atoms: the 19 small atoms
  cut both, but all five K6 giants are satisfied by the cold dual by margins of `9.5` to
  `17.4`.
- Worse, adding cuts moves the excess rather than shrinking it. Exact maximum depth of the
  LP's own dual is `1.096307560` at `(1.300943, 1.847007)` before the atom columns, and
  `1.114546762` at `(1.294501, 1.843441)` after -- 0.018 DEEPER and 0.0035 FURTHER from
  any sampled site, at `0.007740` from the nearest of 17,389 sites. Both witnesses are led
  by the 29-degree-class tilted pair near `(1.389, 1.328)` and its mirrors: an INTERIOR
  meeting of the tilted pair, not the mid-wall sliver S4 was aiming at.

So the loop is chasing one vertex of a face that has many, and the excess migrates between
rounds. A site oracle that samples the current dual's depth witness is structurally a
treadmill.

What to build instead -- sites indexed by the structure that produces the depth, not by
the arrangement:

1. Enumerate the interacting families directly: the near-axis wall squares whose right
   edges interleave (the `0.26`-`2.90` degree band A3 named) and the tilted pair classes
   near 29 degrees that A4's two witnesses are led by. Place sites on the exact crossing
   loci of those families -- edge-edge and edge-corner incidences in exact rationals --
   rather than on whatever vertex the current dual happens to be deepest at.
2. Add all D4 images of a structural locus at once. The obstruction is D4-symmetric and
   the LP symmetrises its dual anyway; sampling one image at a time is part of why a round
   buys so little.
3. Price a round honestly before running it. A3's 300-column round is 825 s; the
   measurement worth having is value moved per second of warm LP, against the `0.018` the
   `383/100` plateau would need and the `0` that three rounds have bought so far.
4. Carry a control that the structural site set contains the vertex the depth oracle would
   have picked, so the new generator is a superset rather than a different guess.

The reason this is priority 1: A4 established that the atom language is not what pins
`153/40` -- twenty-four violated atom orbits, every one exact, all priced at their true
budgets, and the LP moved by `2.2e-13` with all twenty-four carrying primal weight exactly
zero. If the atoms are not the limit then the sites are, and the site generator is the
only part of the loop nobody has changed.
