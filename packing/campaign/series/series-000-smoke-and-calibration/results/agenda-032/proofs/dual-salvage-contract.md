# Exact Fractional-Family Screen for Corner Residual Covers

Prepared 2026-09-09 for the prospective n11 corner-owner sprint.
This is a mathematical and instrument contract.
No obstacle filtering, survivor-mass measurement, or scientific target run was performed
for this note.

**Recommendation:** run this screen before optimizing weights for the coarse footprint
classes. A surviving family of weight at least ten rules out a one-owner residual-ten
cover on every site set; weight at least seven does the same for a four-owner
residual-seven cover.
Translation and deletion preserve the existing exact depth bound, so no LP or new
arrangement-depth search is needed for each class.
The screen does not refute stronger constraints on the unknown owners or on joint
compatibility.

## Retained Source and Verification

[Exp-070](../../../../../../campaign/series/series-000-smoke-and-calibration/experiments/exp-070-h-064-n11-fractional-resume.md)
retains the
[BC-232 family](../../../../../../campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-family.json):
768 closed squares of side `B = 9977/10000` in `[0,191/50]^2`, with exact weights
summing to

```text
W0 = 21342289572/2055263195 = 10.384212408377... .
```

The family’s embedded receipt and its
[summary](../../../../../../campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-summary.json)
report exact maximum depth one over 2,677,732 arrangement vertices, with 128 exact tie
decisions. `proved: false` records only failure of `K3 total weight at least n`, because
the source target was eleven.
It is not a depth failure.
The exact reader is
[verify_ceiling](../../../../../../src/sqpack/fractional/ceiling.py), which checks
admissibility, containment, arrangement depth, and total weight separately.

The inspected source and reader files were clean at checkout
`f917b498e332c2019f39fe366f00ba2d48422c23`. The source family has Git blob
`8a0bf1a264a1361649bc0acd0f70907ba8125f2f`; the ceiling reader has blob
`f026bd04186787096fb57128517e319e7ee1ae00`. Bind a future run to its actual commit and
source blob, and preserve the source receipt.
A fresh replay can validate the source once before processing all classes.
Each filtered class can then inherit depth by the deletion lemma instead of repeating
millions of arrangement checks.

## Exact Transport and Filtering

Embed the family centrally at `q = 96/25` by adding `(1/100,1/100)` to every centre.
Keep every side, angle, and weight unchanged.
This is scale **one**, unlike the separate unit-square transport by `10000/9977`. The
existing
[transport_ceiling_family](../../../../../../devtools/transport_ceiling_family.py)
implements the required exact transformation with `factor=1, side=96/25`.

Let `U` be the union of the declared rational convex footprint polygons for one branch.
Reconstruct each translated square from the source and retain it only when:

1. Its side is exactly the residual program’s `B`, its actual orientation is in that
   program’s checked direction family, and it is contained in the target container.
2. It is strictly disjoint from every closed footprint polygon: `P intersect T = empty`.

For convex polygons, decide the second condition by exact separating-axis tests on both
square-axis normals and all footprint-edge normals.
Retain a square only when one projection interval is strictly before the other, giving a
positive rational gap.
Equality is touching and is discarded.
This conservative convention proves admissibility for both the strict residual family
and any larger family that also admits touching.

The source’s 181-angle metadata is folded, while some actual placements have reflected
angles. Its receipt therefore says `symmetric_only: true`. That limits the old
admissibility shortcut, not the all-point depth check.
A general corner branch can have asymmetric weights.
Require literal membership, modulo the square’s quarter-turn identity, in the branch’s
full checked direction family; never reflect an individual survivor into a new pose
using symmetry that the branch does not possess.
If the numerical screen checks fewer directions, either discard missing-angle members or
state that the obstruction concerns the full-direction program.
An all-point obstruction to the full program can still justify stopping a cheaper
exploratory LP that could never certify that program.

## Weak-Duality Certificate

Write the translated source family as `(P_i, lambda_i)`. Exact source verification gives

```text
sum_i lambda_i * 1[P_i contains z] <= 1   for every point z.
```

For any retained index set `I`, deleting nonnegative summands preserves this inequality.
Because each survivor avoids `U`, its depth is zero on `U`. Every nonnegative measure
covering all admissible residual cores with mass at least one consequently satisfies

```text
W_I = sum_(i in I) lambda_i
    <= sum_(i in I) lambda_i * mu(P_i)
    <= mu(K \ U).
```

Thus `W_I >= 10` obstructs a strict residual-ten certificate and `W_I >= 7` obstructs a
strict residual-seven certificate, on **all atom sites and all nonnegative weights**,
including asymmetric weights when literal direction membership was checked.
The same argument bounds a banking objective `mu(K) - mu(U)`; use the union’s mass, not
duplicate credits for overlapping footprints.

The obstruction applies to the declared family of cores avoiding the footprints.
A survivor need not extend to a compatible unit-square parent or coexist with any actual
corner owner. Those stronger constraints can delete its row and invalidate this
particular obstruction.
A surviving mass below the threshold gives an inconclusive lower bound, not evidence
that a covering certificate exists.
Changing weights, moving squares independently, or adding family members requires new
depth verification; none belongs to this deletion-only screen.

## Strict Residual Domains and Boundary Components

A guaranteed footprint contained in a selected owner core is inside that owner’s
unit-square interior.
Other packed squares avoid the footprint; their strict inner cores have positive
distance from it. No uniform distance over all packings is needed.

At a fixed direction, strict separation from finitely many compact polygons is an open
condition on the centre.
SAT writes it as a finite union of intersections of strict linear inequalities.
A nonempty such branch has positive area.
Intersecting with the full-dimensional container centre square still creates no isolated
line or point: every feasible boundary point has nearby feasible points in the container
interior. Therefore a checker for this **strict** residual family may discard zero-area
closures. It must not silently treat contact-only components of weak SAT branches as
members of the strict family.
Covering the remaining positive-area closures is safe, and nonnegative atom weights
preserve the usual boundary-mass argument.

## Smallest Reusable Instrument

Add one source-bound reader accepting the retained family, exact translation, target `B`
and direction list, rational convex obstacle polygons, and threshold.
Reuse `CeilingCertificate.from_record`, `Placement.corners`, and the existing transport
function. It needs a generic exact polygon SAT predicate, fixed-weight summation, and an
output receipt; it needs no optimizer or event-cell separator.

Retain the source identities and depth receipt, transformed parameters, exact obstacle
vertices and class IDs, unique survivor source indices, literal angle checks, a positive
separating-axis gap for every survivor/obstacle pair, exact total, threshold, and scoped
verdict. The replay reconstructs survivor coordinates and weights from the source; it
refuses duplicates or altered weights.
Keep all source poses immutable.
An empty survivor set is a valid zero lower bound, even though `CeilingCertificate`
itself requires a nonempty family.

For sixteen classes at one corner, the source requires 12,288 square/polygon membership
decisions before SAT short circuits.
Four-corner combinations can reuse one survivor bit mask per individual footprint,
intersect four masks, and memoize equal resulting masks.
Scale weights once to a common integer denominator for the mask sums.
This removes repeated geometry from the potential 65,536 joint branches.
The work is much smaller than a separate multiround covering LP and exact event sweep
for each branch; the runtime and number of obstructed classes remain unmeasured.

Controls should recover `W0` with no obstacles, give zero survivors when the obstacle is
the whole container, retain a known positive-gap square, discard exact tangency and
strict overlap, and reject a duplicate source index or modified weight.
A missing reflected direction must cause deletion or refusal, never a symmetry shortcut.
Replaying translation and deletion must preserve the derived depth bound without
claiming that the subset’s maximum remains exactly one.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
