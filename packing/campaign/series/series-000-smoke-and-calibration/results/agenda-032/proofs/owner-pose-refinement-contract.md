# Owner-Pose Refinement Contract

**Status, 2026-09-09:** analytic design by the existing GPT-6 Astra agent at extra-high
reasoning. No target was run and no numerical outcome was selected.
The proposed rectangles and residual-domain formulas require implementation controls and
exact replay before becoming pipeline evidence.

## Recommendation

Use centre-and-angle classes when the sector footprint is too weak.
A concrete exhaustive one-owner partition has **256 raw classes**, each with a
guaranteed core rectangle of area **49B²/144**. This is over three times the area of the
widest-sector endpoint polygon, while remaining a four-vertex obstacle.
The mark, angle, and centre data also support a stronger residual-domain test: a
candidate residual core must be able to coexist with at least one owner pose in its
class.
This can reject cores that avoid the common footprint but intersect every possible
owner.

First run exact retained-family filters for one predetermined refinement and its
fixed-owner limit.
A new covering LP is the next step if those filters leave the question
open.
Pairwise overlap cuts alone do not strengthen an all-site fractional packing bound;
they are already implied by point capacity.

Inputs and source contracts remain q=96/25, B=9977/10000, the two bottom-left marks from
BC-303, the full reflected owner net, and the strict-core transfer in
`corner-owner-sector-footprints.md` and `owner-footprint-contract.md`.

## A Finite Exhaustive Partition

Let h=B/2. At an owner’s selected net orientation (u,v), write its centre as

`z = m + a*u + b*v`, with `a,b ∈ [-h,h]`.

This follows exactly from the selected core containing m. Partition each displacement
coordinate into the four closed intervals

`I_i = [-h+i*B/4, -h+(i+1)*B/4]`, for i=0,1,2,3.

Their boundary overlaps are harmless.
No assumption that the mark is strictly interior is needed.

For the angle classes, write A=207107/500000 and t_j=A*j/180 for the retained folded
half-tangent net.
Use four blocks j=0..45, 45..90, 90..135, 135..180, and their reflected
orientation blocks. All full-net owner directions are represented.
A reflected 90-degree axis frame may be retained as a duplicate geometric owner
orientation so the block reflection map is exact.
Its square equals the 0-degree square, with correspondingly transformed centre
coordinates. Residual directions may still use the canonical 361-orientation list.
Each folded block uses the rational reference half-tangent at the midpoint of its
endpoint half-tangents.
Its reflected block uses the reflection of that same reference frame; do not recompute
an arithmetic midpoint after transforming the half-tangents.
The reference rotation need not itself be a retained owner direction; it is only the
coordinate frame for a guaranteed rectangle.

Two marks, eight angle blocks, and sixteen displacement boxes give 2×8×16=256 raw
classes. A hypothetical packing belongs to at least one class for its bottom-left owner.
Successful residual-ten certificates may differ between classes; every class must pass
or be exactly excluded to close the partition.

Diagonal reflection maps m1 to m2, a folded block to its reflected block, and
displacement indices `(i,j)` to `(i,3−j)`: the reflected u-axis agrees with the target
u-axis, while the reflected v-axis is its negative.
With matching support and variable grouping, this gives 128 representative pairs.
Certificates must be explicitly transported; it does not justify D4 averaging within an
asymmetric class.

## Uniform Guaranteed Rectangle

Fix one class with a∈[a0,a1], b∈[b0,b1]. For any one owner orientation, intersecting all
translated B-cores gives

`[a1−h,a0+h] × [b1−h,b0+h]`

in coordinates relative to m and that orientation.
Its side is W=3B/4. Every coordinate of this rectangle has absolute value at most W.

Let u0,v0 be the block’s reference axes.
Set η=B/12. The following rotated rectangle is guaranteed inside every owner core in the
class:

`R = m + [a1−h+η,a0+h−η]*u0 + [b1−h+η,b0+h−η]*v0`.

Its side is W−2η=7B/12 and its area is 49B²/144. This is core containment, so R supplies
both an obstacle for remaining cores and bankable mass.
It is not an assertion that μ(R)≥1.

Here is the exact angular allowance.
The half-tangent distance from the reference is at most d=A/8=207107/4000000. The
angular difference is therefore at most 2 arctan d. Rotating a vector whose two
coordinates have absolute value at most W changes either coordinate by at most

`W*E`, where `E=2*d*(1+d)/(1+d²) < 1/9`.

The last inequality is exact: `17*d²+18*d−1 = −359109739367/16000000000000 < 0`. This is
equivalent to E<1/9. Thus the inward margin η=W/9 absorbs the entire coordinate change.
Every point of R remains within the un-eroded rectangle in every owner orientation of
the block, proving containment.

The derivation uses every retained owner direction in the block, even if a later
residual screen uses fewer directions.
Reflections preserve the same bound.
No approximation to a 45-degree direction is inserted.

A class near the edge of the displacement range may have R not containing m. That is
harmless: `conv(R ∪ {m})` is a larger guaranteed footprint, since every owner is convex
and contains both. If a class refines a previously certified sector class, also take the
convex hull with that class’s old endpoint footprint.
This preserves geometric nesting for matched comparisons.
Alternatively, intersect all of the class’s exact rotated rectangles to obtain its
larger exact common core region; the four-vertex R is a cheap conservative option.

## Exact Pruning and Further Refinement

For each retained owner orientation, compute the exact possible-centre polygon

`Z = centre_domain(q,B,owner_direction) ∩ (m + I_i*u + I_j*v)`.

Use consistent world or rotated coordinates.
An empty polygon removes that orientation from the class.
If none remain, the class is impossible.
Zero-area intersections can also be removed under the strict-core-inside-container
premise: an actual centre is interior to the contained-centre polygon, and the
displacement box has positive widths.
A guaranteed footprint extending outside K also proves class impossibility.

Containment pruning is substantive here.
For example, at the axis orientation, the lowest b-bin has z_y≤m_y−B/4<h because the
chosen m1 has m_y=2336/3175<3B/4. Those poses cannot be owners.
This is a pose exclusion, not a packing exclusion or evidence from a numerical run.

Finer centre bins of width B/k replace W by B(1−1/k), with 16k² raw classes for the same
eight angle blocks. The same 1/9 allowance gives guaranteed area `(49/81)*B²*(1−1/k)²`.
Subdividing the angle blocks also lowers the exact error E; both refinements converge
toward a fixed owner.
An adaptive proof tree can refine only unresolved classes while retaining the original
exhaustive cover and documenting every child’s coverage of its parent.

Do not expand all four owners at once: 256⁴ raw combinations are over four billion.
The sprint target should remain a one-owner test with residual count ten.

## Stronger Domain: Some Owner Pose Must Coexist

The common-footprint relaxation can retain a residual core that intersects every owner
pose, with the intersections occurring in different places.
The exact existential-owner test removes this defect without representing all parents
jointly.

For a fixed residual orientation, let its centre be x. For each allowed owner
orientation o and its nonempty exact centre polygon Z_o, take signed axes

`n ∈ {±u_o, ±v_o, ±u_r, ±v_r}`.

Define the projection radii

`r_o(n)=h*(|n·u_o|+|n·v_o|)` and `r_r(n)=h*(|n·u_r|+|n·v_r|)`.

A residual core can be strictly disjoint from some owner core in this orientation and
centre polygon if and only if at least one axis satisfies

`n·x > min_{z∈Z_o}(n·z) + r_o(n) + r_r(n)`.

The minimum occurs at a vertex and is rational.
This follows by the complete square-square separating-axis criterion, followed by
minimizing over the owner centre.
Taking the union over allowed owner orientations gives the class’s existential residual
domain. Using closed contained-centre polygons for the owner is a safe enlargement if
some extreme owner poses touch the container.

Equivalently, the forbidden residual centres form the intersection of all complementary
closed half-planes, one for each orientation and signed axis.
This is convex. Build it by exact clipping and remove redundant sides, then reuse the
generic exterior-piece event-cell engine.
An exact bounded starting polygon is the Minkowski collision polygon of any one allowed
owner pose; the forbidden intersection is a subset of it.
This avoids an arbitrary bounding box.
Before redundancy removal there are at most `4+4*N` distinct normal directions for N
owner orientations: four residual axes plus four per owner orientation.
Before restricting to the residual container domain, the forbidden polygon must contain
the guaranteed common rectangle plus the residual square.
An empty result there contradicts a nonempty owner class and is a geometry error.
An empty intersection with the contained residual-centre domain merely means that this
condition excludes no contained residual centre at that orientation.

This test is necessary, not sufficient, for a packing.
A different possible owner may witness admissibility of each residual core.
The ten remaining cores must still share one actual owner and be mutually compatible;
the row relaxation forgets that common choice.

There is an important limit to the improvement.
For one fixed owner orientation and an unclipped displacement rectangle aligned with its
axes, existential coexistence is exactly avoidance of the common owner rectangle.
Projection-radius subtraction makes the two SAT conditions identical.
Additional gain comes from correlations introduced by containment clipping and from
retaining the disjunction over multiple owner orientations, rather than intersecting
their occupied regions first.

## Predetermined First Discriminator

Choose m1, the first folded angle block, and displacement bins i=j=2, so `a,b∈[0,B/4]`.
This refines the previous inward sector j=0: choose the signed rays toward the centre
along +u,+v, including zero-coordinate boundaries.
Construct

`A_ref = conv(old_sector_endpoint_footprint ∪ R)`.

The old footprint is included, so the refined residual family is nested inside the old
one. Use the same full retained owner net and the same B convention throughout.

The first exact retained-family controls are:

1. Filter against A_ref by strict closed-set separation.
2. Filter against the existential-owner criterion for the same class.
3. As a cheap limiting control, filter against a single fixed B-core centred at m1 with
   axis orientation. This pose is individually contained and owns its mark; it is not
   asserted to occur in an eleven-square packing.

Existing nonnegative family weights and their pointwise depth bound survive deletion.
A survivor mass at least ten therefore blocks a strict effective-mass-below-ten weighted
cover for that tested residual family.
A mass below ten only defeats that particular obstruction; it does not produce a cover.
The fixed-owner control tests whether an obstruction persists even after removing pose
uncertainty. If it does, refinements containing that pose need stronger premises or a
stronger method to close that leaf.

If filters leave the selected class open, run a matched
old-footprint/refined-footprint/existential-domain cover screen.
All three use residual threshold ten.
Report effective mass differences, remaining gap to ten, and exact coverage scope.
A successful refined leaf does not exclude its unrefined siblings.

## When to Change the Method

Pairwise overlap inequalities for two retained cores are already consequences of
all-site depth at an intersection point.
Adding them only repairs a finite-support relaxation that omitted that point.
Genuine packing-interaction strengthening needs inequalities not reducible to one point,
such as clique inequalities for pairwise-intersecting families lacking a common point,
or odd-cycle stable-set inequalities.

Such cuts would require a different certificate theorem and a way to cover the continuum
of poses. Their validity on one finite family is diagnostic, not a global packing proof.
This is a larger change than the owner-class refinement and should not be improvised
into the current point-measure reader.
The immediate dependency order is exact refinement geometry, retained-family filters,
one matched class screen, then selective class subdivision or a separately designed
interaction certificate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
