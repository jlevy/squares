# Generic Owner-Footprint Cover: Sprint Contract

**Status, 2026-09-09:** mathematical design, read-only source inspection, no scientific
target run. This contract extends the reviewed sector lemma; the endpoint-square
enlargement below is an analytic derivation, not an exact-reader or pipeline result.

Source contracts:
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md`;
`packing/src/sqpack/fractional/{model,generate,colgen,sweep}.py`;
`packing/devtools/run_residual_cover_pilot.py`. The existing pilot’s four-flush-corner
domain and symmetry assumptions do not describe a generic owner footprint.

## Mathematical Inputs and Direction Family

Use q=96/25, B=9977/10000, h=B/2, and the existing corner-pair core-ownership premise.
The bottom-left marks are m1=(3152/3175,2336/3175), m2=(2336/3175,3152/3175). A class
specifies one mark and one of eight closed signed-axis sectors.
Every actual owner has at least one class; overlapping boundary classes are allowed.

Without branch symmetry, cover square orientations modulo 90 degrees.
From every retained direction u=(c,s), append its reflected orientation u'=(s,c), with
v'=(-c,s). Canonicalize the 90-degree axis square to the 0-degree square and deduplicate
exact orientations. The current 181-point folded net gives 361 distinct square
orientations: its rational last direction slightly overshoots 45 degrees, so it and its
reflection are distinct.
Do not merge them by float tolerance.
All retained representatives can have c,s nonnegative, so the existing exact
`centre_domain` formula using h(c+s) remains valid.
A direction representation with negative coordinates would instead need h(|c|+|s|).

The owner-footprint construction always uses this FULL retained family.
A cheap residual LP may use a symmetric subset, but deriving its owner footprint from
that subset would omit possible owner orientations and be unsound.

## Exact Footprints, Including a Cheap Enlargement

The existing triangle is T_j(m)=conv(m,m+r_(j+1),m+r_(j+2)), with the eight rational
rays and indices from the retained lemma.
Its area is h²/4. It is contained in the selected core, not merely in its unit parent.

For a larger footprint, form the exact signed unit rays G={u,v,-u,-v} from the full
family. For each closed sector j, select its angularly first and last rays a,b. Rational
signs and cross products determine bin membership and ordering; do not use inverse
trigonometry. Both sector boundary memberships are retained.
Define J(x,y)=(-y,x) and the anchored square

Q_r(m)=conv(m, m+h r, m+h(r+Jr), m+h Jr).

Those vertices are counterclockwise.
Output P_j(m)=Q_a(m) intersect Q_b(m), using exact rational clipping, removing repeated
and collinear vertices, and retaining counterclockwise ordering.
This is generally a quadrilateral, and contains T_j(m).

An equivalent explicit counterclockwise vertex list is
`(m, m+h*b, m+h*((c/(1+s))*a+J(a)), m+h*J(a))`, where `c=a·b` and `s=det(a,b)`. The
denominator is positive.
This avoids clipping in production and gives an independent exact control against the
two-square intersection.

Endpoint proof: let the endpoint angles be α≤β, with β−α≤π/4. A point in both squares
lies in the common angular wedge [β,α+π/2]. There, its projection onto an intermediate
ray e_φ is maximized at φ=β; its projection onto J e_φ is maximized at φ=α. Nonnegative
projection constraints likewise reduce to endpoints.
Hence Q_a intersect Q_b equals the intersection of ALL anchored squares between them.
It is uniformly inside every selected owner core in the class.
No extra cases are introduced.

An exact area control is h²(a·b)/(1+det(a,b)), equivalently h²(1−det(a,b))/(a·b). At
ideal width π/4 this is (sqrt(2)−1)h², about 65.7% larger than the triangle.
Use the actual rational endpoints in the artifact, not ideal irrational endpoints.
Coincident endpoints give the whole h-square.

## Generic Residual Centre Domain

Let A be the chosen point, triangle, or enlarged convex footprint.
At a residual orientation (u,v), rotate each footprint vertex p to (u·p,v·p). Let
S=[-h,h]² and F=rot(A)+S. Build F as the exact convex hull of all vertex sums with the
four vertices of S. Its interior consists exactly of centres whose core interior
overlaps a positive-area footprint; for a point footprint it consists of centres
containing the point in their core interior.
Closed F represents any intersection, including touching, in every case.

For each counterclockwise edge p→p+d of F, form the exterior closed half-plane

(-d_y) U + d_x V ≤ (-d_y) p_U + d_x p_V.

Clip the exact container centre polygon C to each exterior half-plane separately.
Their union is C minus int(F), so it admits touching.
A triangle has at most seven Minkowski edges and therefore at most seven convex pieces;
an enlarged quadrilateral has at most eight.
A point gives four. Duplicate or empty pieces can be removed.
Do not use the fixed-corner pilot’s six-piece formula.

Keep separate vertical spans for different components in each event slab.
A single minimum/maximum span can bridge a forbidden gap.
Merge only overlapping reachable event-index intervals.
All nonzero site weights and their event boundaries must be retained for exact replay.

Boundary contract: actual remaining cores avoid the CLOSED owner footprint with positive
clearance, since their closed cores lie strictly inside pairwise disjoint-interior unit
parents. They also lie strictly inside the container.
Thus their centres lie in int(C) outside closed F. Every actual centre has an open
feasible neighbourhood.
The existing event method may safely cover that strict residual family by positive-area
exterior pieces; closed-core incidence and nonnegative weights make event-boundary mass
at least adjacent-cell mass.
This does NOT, by itself, verify every isolated touching centre in the enlarged weak
domain. If a reader advertises that stronger closed-domain claim, it must separately
handle zero-area pieces and isolated boundary contacts; the current pilot’s
`reachable_spans` skips them.

Independent geometry controls should compare the polygon union with direct
separating-axis tests on exact rational poses, including axis orientations, reflected
orientations, tangencies, and event cells meeting multiple pieces.
These are instrument controls, not target evidence.

## LP Variables, Symmetry, and Matched Scores

Use nonnegative weights.
Safest expressive choice: independent variables for every site in the same fixed
D4-closed support S for every arm.
`SiteSet` groups variables by its `orbits`; its convenience constructors impose D4 ties.
The existing numeric routines can represent singleton groups, but metadata must identify
them as independent variables rather than genuine symmetry orbits.

Imposing equal weights on D4 orbits remains a valid restricted search even for an
asymmetric branch, provided ALL required directions and residual rows are checked.
It can lose useful measures.
Averaging an asymmetric branch’s solution over D4 is not justified.
Whichever grouping is chosen must match across comparison arms.

For strict avoidance of A, sites in closed A cover no admissible residual core.
With independent variables they can be removed or assigned zero weight.
This makes residual total mass the effective banked mass; it avoids free-cost variables
arising from the equivalent objective μ(K)−μ(A). If generic banking is retained, the
coefficient for a site in A is zero and outside A is one; tied-orbit coefficients count
sites outside A. For tied variables, either use those banked coefficients or remove
inside-footprint entries from each column while preserving its remaining coupling; do
not silently delete the whole orbit.
Never replace the actual μ(A) by one.

Suggested matched arms on identical support, direction subset, variable grouping, and
settled row-generation tolerances:

- unrestricted, optimum M0;
- one owned point m, optimum effective mass Mm;
- its triangle T, optimum effective mass MT;
- its enlarged footprint P, optimum effective mass MP.

The incremental footprint scores Mm−MT and MT−MP separate geometry from bare point
ownership. The exclusion-gap improvement is G_A=M0−M_A−1, because the threshold changes
from eleven to ten. Positive G_A improves the gap by that amount; it is NOT a packing
exclusion unless M_A<10 with complete exact coverage and full direction transfer.
A triangle need not save one unit, so G_A may be negative.
Nested-domain monotonicity gives MP≤MT≤Mm≤M0 at true settled optima on the same
admissible variable family.
Violations beyond numerical tolerance indicate unfinished solves or a mismatch, not
scientific evidence.

## Exhaustiveness, Equivalence, and Pruning

There are sixteen raw classes for the fixed bottom-left corner.
Its diagonal reflection sends (m1,j) to (m2,7−j mod8). With reflected full directions
and a reflection-invariant support/grouping, eight representative solves can cover all
sixteen by explicitly transforming certificates.
A single passing class remains only a conditional exclusion.
Moving the chosen corner by global D4 does not authorize independently transforming
corners of a four-owner branch.

Cheap pose-emptiness pruning does not appear useful here: each mark can itself be the
centre of a contained B-core at every orientation, since its nearest-wall distance
2336/3175 exceeds h sqrt(2). At centre equality, either signed ray can be chosen, so all
sectors are represented.
Cross-corner footprint intersections also cannot prune these classes: every anchored
h-square lies in a radius-h sqrt(2) disk about its mark, while the replay’s cross-corner
mark distances exceed B sqrt(2), the sum of those radii.
This does not establish that four owners, or eleven parents, can coexist.

## First Discriminator and Dependency Map

First branch: (bottom-left m1,j=0), an inward footprint with simple axis/diagonal
triangle vertices. First LP screen: modest fixed support, such as the 21×21 inset grid
augmented by the mark orbit, and the reflected subset generated from folded indices
{0,45,90,135,180}; after square-orientation deduplication this is nine orientations.
The engineer should use the existing complexity estimator before committing a run
budget. Derive P0 from the full net regardless of this subset.

The parallel dual-salvage lane can first filter its retained exact depth-one family
against this same footprint.
That may expose an obstruction more cheaply than finding a new cover.
It needs the footprint’s exact counterclockwise vertices and the same B-core convention.

Dependencies: full direction normalization → exact endpoint footprints →
Minkowski-domain controls → support/grouping and matched score receipts → single-branch
dual filter and LP screen in parallel → exact replay of any promising proposal → full
directions → all eight representatives/sixteen classes.
Only then consider 16^4 four-corner branches; their required residual threshold is
seven.

A float failure, deadline, unresolved separation, or M_A≥10 merely fails to supply a
certificate.
An exact feasible dual of mass at least ten against the fixed support proves
that support/grouping cannot attain a strict mass-below-ten cover, even if its rows use
only a direction subset.
It does not exclude richer support, independent weights when ties were imposed, other
owner classes, or physical packings.
A full-support obstruction needs its separate all-site capacity proof.
No screen over nine directions is an all-angle positive certificate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
