# Multiple Owner-Footprint Domain Contract

**Status, 2026-09-09:** analytic implementation design by the existing GPT-6 Astra agent
at extra-high reasoning.
No target computation was run.
The proposed decomposition needs exact geometry controls before scientific use.

## Domain and Existing Interfaces

Reuse the rational polygons and rotations in `packing/devtools/owner_footprints.py`:
`forbidden_centre_polygon`, `container_centre_polygon`, convex hull/normalization, area,
membership, and strict SAT. Reuse the separate-piece event machinery in
`run_owner_footprint_cover.py` and `run_residual_cover_pilot.py`.

For each residual orientation, work in its rotated (u,v) frame.
Let C be the exact contained-centre polygon and let

`F_i = rot(A_i) + [-B/2,B/2]²`, for i=1,...,4,

where each A_i is its owner’s guaranteed closed core footprint.
The physical residual domain is

`int(C) \ (F_1 ∪ F_2 ∪ F_3 ∪ F_4)`.

All four collision polygons are closed, convex, and full-dimensional, even when a
footprint is a single point.
Do not convex-hull their union: that would forbid legal gaps.
Do not form all combinations of exterior half-planes: that produces up to 8⁴ overlapping
pieces for endpoint footprints.

The return object should retain C, all four footprints and collision polygons, and
positive-area convex component closures.
Its membership predicate must check `centre∈int(C)` and `centre∉F_i` for every i.
Membership in the returned closures alone is not a strict-disjointness claim.

## Exact Vertical Decomposition

1. Normalize every polygon counterclockwise; remove repeated and collinear vertices.
   Collect the u-coordinate of every vertex of C and every F_i.
2. Add the u-coordinate of every pairwise boundary-segment intersection between distinct
   polygons, including C versus every F_i. Use exact rational segment parameters and
   retain endpoint intersections.
   Parallel disjoint segments contribute nothing.
   For collinear overlaps, existing endpoint coordinates suffice: the affine boundaries
   coincide rather than exchange order.
3. Restrict cuts to C’s u-range, retain its two extremes, sort, and deduplicate exactly.
   For each consecutive pair u0<u1, use the rational midpoint u*=(u0+u1)/2.
4. A convex polygon active at u* has exactly two section endpoints, obtained from its
   nonvertical crossing edges.
   Store each endpoint’s complete affine function `v(u)=slope*u+intercept`, not only its
   midpoint value. Vertical edges cannot cross the interior of this slab because their
   u-coordinates are cuts.
   A polygon absent at u* is absent throughout the open slab.
5. Intersect every obstacle interval with the container interval.
   Select max(lower endpoints) and min(upper endpoints) by exact midpoint comparisons,
   retaining the affine identities.
   Discard empty or zero-height intersections.
6. Sort the surviving intervals by their lower midpoint values and merge overlaps AND
   touches, selecting the outer affine bounds.
   Subtract their union from the container interval.
   At most five positive-height free intervals remain.
7. For each free gap with affine boundaries l(u)<r(u), emit the closure with vertices
   `(u0,l(u0)), (u1,l(u1)), (u1,r(u1)), (u0,r(u0))`. Normalize and remove zero-area
   results. The result is a convex trapezoid, rectangle, or triangle.
   An endpoint height may vanish without invalidating a positive-area triangle.

Why midpoint decisions suffice: section edges change only at polygon vertex abscissae.
Their vertical order changes only where two boundary edges intersect.
Every such event was made a cut.
On an open slab the active edges, endpoint ordering, overlap groups, and free-gap
boundary identities are constant.
The emitted trapezoid is therefore the closure of that entire free strip, not an
approximation sampled at its midpoint.

If two active affine functions agree at the midpoint, they must agree throughout the
slab; otherwise their isolated intersection should already have been a cut.
Treat an unexpected isolated midpoint equality as a geometry assertion failure.
Coincident intervals are merged.
A zero-height apparent gap is not a physical corridor.

Optional exact simplification: merge adjacent trapezoids when they have the same affine
lower and upper functions and meet at the same slab boundary.
Their union is again a trapezoid over the combined u-range.
This removes cuts caused by unrelated geometry elsewhere in the section.

## Polynomial Size Bound

Let there be r obstacles with collision-polygon edge counts k_i, plus four container
edges. Put V=4+sum(k_i). Two convex polygon boundaries have at most twice the smaller
edge count in isolated intersections; collinear overlap endpoints are already vertices.
Therefore the number S of distinct cuts is at most

`V + sum_{i<j} 2*min(k_i,k_j)`,

where that sum includes the container as a polygon of edge count four.
There are at most S−1 slabs and r+1 free gaps per slab.

For four endpoint footprints, k_i≤8: V≤36, obstacle-pair intersections contribute at
most96, and obstacle/container intersections at most32. Thus S≤164 and there are at most
**815 raw pieces**. Four triangle footprints give S≤148 and at most735 pieces.
These are conservative bounds; duplicate cuts, occluded intervals, and adjacent-piece
merging reduce them.
The construction replaces an exponential product by polynomial arrangement work.

For these small polygons, a direct exact test of every cross-polygon segment pair is
sufficient. No general polygon-Boolean library is required.
Cache the decomposition once per branch, footprint kind, and residual direction; do not
rebuild it during every LP round.

## Strict Boundaries and Event Cells

Every selected core is compact and lies strictly inside its physical unit parent.
Different parent interiors are disjoint, so every actual remaining core has positive
distance from each guaranteed owner footprint.
It also lies strictly inside the container.
Its centre therefore has an open neighbourhood in the strict domain above.

The trapezoid closures cover every actual centre, including centres on decomposition
cuts. They may additionally contain forbidden tangencies along their edges.
Dropping zero-area pieces cannot remove an actual physical centre: such a centre has a
two-dimensional feasible neighbourhood, and adjacent positive-area strips approach it.

Closed-core incidence and nonnegative atom weights justify transferring coverage from
open atom-event cells to an actual event-boundary centre.
Nearby generic placements may lose boundary atoms; they cannot gain atoms absent from
the limit core. Do not advertise coverage of every isolated artificial weak-contact
placement unless it is separately checked.

The existing `reachable_spans` interface can consume the trapezoids.
It must union each component’s reachable event-index ranges, preserving gaps.
A witness must be constructed in one actual component and checked against all four
closed collision polygons; never choose the midpoint of a min/max interval spanning
several components.

## Avoid Making Geometry the Dense Grid

The smallest code change can retain the current rule that inserts all component-vertex
coordinates into the mass event grid.
Its complexity receipt must count the resulting distinct u and v events before running.
With many decomposition vertices this may dominate the grid even when few atoms have
positive weight.

There is a safe optimization if that guard is too expensive: incidence mass changes only
at atom coordinates ±B/2. Build the mass grid from those events plus C’s coordinate
extremes, while keeping the full trapezoids for exact reachability.
Geometry vertices need not become mass events.
Every mass cell is still constant; component clipping decides whether it has an
admissible witness. This keeps each grid dimension at most about 2p+4 for p retained
sites, independently of decomposition size.

If implementing that optimization, index trapezoids by their u-ranges instead of
scanning every trapezoid for every atom slab.
The overlay of the geometry and atom partitions has only the sum of their cut counts,
and at most five free pieces over each overlay interval.
This avoids replacing a small dense grid with an unnecessarily quadratic piece scan.
It is an optimization after geometry controls, not a prerequisite for the first
small-support pilot.

## Four Inward Owners: Exact Branch Definition

Take the existing bottom-left m1/j0 footprint A. Define the other three footprints by
the same maps used in `screen_corner_dual_salvage.py`:

`(x,y)`, `(q−x,y)`, `(x,q−y)`, `(q−x,q−y)`.

Normalize vertex orientation after reflections.
These are local corner classes; do not apply the same global sector angle to all four
corners without transforming the geometry.

A certificate remains sound as a conditional implication even if a proposed class
combination is physically impossible.
Such a success might only be vacuous, so it would not show that the cover method handles
a realizable owner arrangement.
For this particular branch, the four-owner part is analytically compatible: take four
axis-aligned UNIT parents centred at the reflected m1 marks.
With a=3152/3175 and b=2336/3175, the nearest-wall distances exceed1/2, while

`q−2a = 5888/3175 > 1`, `q−2b = 7520/3175 > 1`.

The parents are contained and pairwise separated.
Their selected B-cores are mark-centred; choosing the allowed positive signed axes at
zero displacement gives local j0, and reflection gives the other three classes.
This is only a four-owner compatibility witness.
It does not place the remaining seven unit squares.

The footprint union is invariant under horizontal and vertical reflection and their
half-turn. It is generally not invariant under diagonal reflection: that exchanges m1
with m2 and changes sector labels.
The generic implementation should retain the full361 orientation family.
For this symmetric pilot, an explicitly D2-symmetric weighted measure permits the181
folded directions because a horizontal reflection supplies the missing reflected
orientations. Enforce that actual symmetry in variables or verify it exactly; singleton
weights do not acquire it automatically.
Solving a folded-net problem with unrestricted singleton weights and averaging afterward
is not a valid shortcut.

## Counting, Pilot Scope, and Engineering Priority

BC-303 supplies four distinct owners, so seven selected cores remain.
A nonnegative measure covering every strict residual core with mass at least one
excludes the branch if its mass outside the closed footprint union is below seven.
Equivalently use `μ(K)−μ(union A_i)<7`. No guaranteed footprint is assumed to carry mass
one, and the literal fixed-unit-obstacle automatic four-unit saving does not transfer to
these smaller footprints.

Remove sites in the union once, rather than summing independent per-footprint masks.
General intersecting guaranteed owner footprints would make a branch impossible;
alternatively union mass avoids double credit.
For these particular sector footprints, the existing cross-corner mark-distance margin
already makes their guaranteed regions disjoint, but the engine need not depend on that
shortcut.

The first pilot should compare the four point, triangle, and endpoint unions on
identical candidate support, variable grouping, and direction scope, with the same
residual threshold seven.
One passing combination remains a conditional exclusion; all65,536 raw mark/sector
combinations are not covered by it.
No further fixed-weight deletion screen of Exp137’s same family is useful, by the
already-recorded point-only monotonicity result.

Compared with the256-class centre refinement, this route requires a new geometry
decomposition but directly uses all four proved owners and the residual-seven count.
It reuses the current LP and exact event interfaces and needs only one predetermined
branch for a discriminatory pilot.
Centre refinement is easier to implement as a new one-obstacle polygon, but multiplies
the case family and retains a residual-ten target.
The four-obstacle engine is therefore a reasonable next instrument; fund one bounded
conditional pilot, not an exhaustive branch campaign yet.

Required small controls are zero/one/duplicate obstacles, disjoint and overlapping
collision polygons, containment of one collision polygon in another, shared edges and
tangent vertices, an obstacle crossing C, a closing triangular gap, and rational sample
points on both sides of every new event.
Compare membership with direct strict SAT for all four footprints.
For a single obstacle, compare the new decomposition with the existing exact
exterior-half-plane union.
An additional independent exact control is area conservation: sum the trapezoid areas
and compare with `area(C)−area(C∩union F_i)`. For four convex obstacles, compute the
latter by inclusion-exclusion over the fifteen nonempty subsets, using the existing
convex-intersection routine.
Slab interiors are disjoint, so no trapezoid area should be counted twice.
This catches missing or filled positive-area gaps without using the decomposition to
verify itself. These are implementation controls, not numerical target evidence.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
