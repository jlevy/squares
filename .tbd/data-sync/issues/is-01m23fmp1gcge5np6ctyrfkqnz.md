---
type: is
id: is-01m23fmp1gcge5np6ctyrfkqnz
title: Generate LP sites by structure, not by arrangement vertex
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-09T16:22:28.656Z
updated_at: 2026-09-10T04:08:49.191Z
closed_at: 2026-09-10T04:08:49.191Z
close_reason: |
  Run and answered on 2026-09-10, retained as agenda-034 lane A6. The instrument works, and
  the answer it returns is that the premise behind this bead was inverted.

  The instrument. A structural site generator: depth is piecewise constant on the cells of
  the arrangement of a family's placement edge lines, so the scan levels are the midpoints of
  consecutive distinct placement-corner ordinates -- one line strictly inside every slab --
  and the same in x, and every maximal run of the exact depth profile above one contributes
  its MIDPOINT, a point interior to a deep cell rather than a vertex on its boundary, so it
  stays a separating site when the dual moves within the optimal face. It runs over all seven
  retained duals of the 153/40 optimal face at once. 37,368 raw candidates, 37,055 distinct,
  all 37,055 exactly above depth one, 17,885 D4 orbits, in 14.6 s -- against the vertex
  oracle's 60,000 vertices screened, 300 kept, 204 s a round. Selection is spatial (round
  robin over coarse 0.02 cells), not by depth.

  It is better than the oracle and it does not matter. Adding 1,400 structural orbits (10,848
  sites, none of them a point the oracle had ever sampled over four rounds) takes the LP from
  17,389 sites in 2,250 orbits to 28,237 in 3,650, and the cold solve returns 11.000000000 in
  404.9 s against the control's 10.999999999999945.

  THE SITE SIDE IS CLOSED, and there is a certificate. Maximising total weight over the
  280-placement support of the 1/25-integral family, weights tied over its 35 D4 orbits,
  subject to depth at most one at all 139,521 structural sites and all 2,566 atom orbits,
  returns exactly 11. The optimum is a D4-symmetric family of 64 admissible placements, total
  exactly 11, exact maximum depth exactly 1 over all 14,344 arrangement vertices, charging
  every one of the 2,566 atom orbits at ratio exactly 1. The plateau reader holds K0 through
  K3 rather than refusing it, an independent exact atom check finds none violated, and
  verify_ceiling proves it separately. A depth-one family is dual-feasible for EVERY site
  set, so on this atom set the rows-complete LP at 153/40 is at least eleven for every site
  set whatsoever. That measurement cost 18 s of LP and 80 s of plateau reader.

  So the lever is the atom set. Lane A4's 24 atoms entered at primal weight zero because an
  atom separated from a DUAL VERTEX need not cut the optimal PRIMAL family, and an atom that
  does not cut the primal optimum cannot move the objective. Separated from the certificate
  instead, six atoms -- two two-of-three and four three-of-five, budget 1 each -- take the
  blocking support from exactly 11 to 10.4210526, bracketed exactly between a feasible
  325657893/31250000 and a dual bound 2605263163/250000000 with A^T u >= cost in Fractions.

  Three readings worth carrying. Stop adding sites at 153/40. The deep region is three
  structures, not two: wall-column seam 46.7 per cent, interior 30.1 per cent, NEITHER 22.0
  per cent, wall band 1.0, diagonal 0.2 -- and the "sliver 0.0006 wide" is one cell of a
  full-height column with 1,123 distinct deep abscissae over a width of 0.0196 and ordinates
  spanning [0.0663, 3.7631]. And the finest deep cells are about 3e-4 wide with typical ones
  near 5e-3, so a net meeting every deep cell needs of order 1e6 sites against the 1e4 the LP
  can carry.

  Left open, and tracked separately: the joint support-and-atom iteration this points to, and
  round two of the LP (4,000 orbits, 8,815 columns, 63.6 M nonzeros) which was still in
  simplex at 71 minutes when the lane closed. Round two is OPEN, not a result, and nothing
  depends on it.
resolution: null
duplicate_of: null
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
