# From One Excluded Branch to a Stronger Eleven-Square Bound

[T-023](../../../../../frontier/RESULTS.md) proves a conditional result at
$q=96/25=3.84$. If four distinct unit squares have selected inner cores containing the
four saved rational patches, at most five further unit squares fit in the container.
An eleven-square packing with those four owners would require seven further squares, so
that branch is impossible.
The [sprint report](sprint-report.md) shows the patches, dots, and counting argument.

The missing global step is to cover every possible packing with conditions we can
exclude. We do not yet know how many other owner classes admit these dots, how many need
different certificates, or whether completing this case analysis is affordable.

## The Stronger Target

Write $s(11)$ for the smallest container side allowing eleven unit squares with pairwise
disjoint interiors. Excluding every eleven-square packing in the closed square
$[0,3.84]^2$ would establish at least $s(11)\ge3.84$: a packing in a smaller container
would also fit in this one.
T-023 does not supply that exclusion.

A complete exclusion at a smaller side above the current bound $3.810025723614703\ldots$
would also improve the global result; $3.84$ is a strategic target.
Changing sides requires valid transport and revalidation of the marks, owner theorem,
patches, net containment, and dots.
The five-versus-seven count alone proves neither robustness to changing the container
nor coverage of other classes.

A strict statement $s(11)>3.84$ also needs the endpoint argument recorded explicitly.
The relevant compactness principle says that packings in every slightly larger closed
container have a limiting packing in the endpoint container.
Thus a *global* endpoint exclusion would imply a positive gap above it, without
quantifying that gap.
The archived
[Martin, Theorem 1](../../../../../resources/papers/martin-2000-compactness-theorems-geometric-packings.md)
provides this principle, including rotations.
It cannot turn exclusion of one owner branch into a global endpoint exclusion.

## What an Exhaustive Owner Argument Must Retain

A **parent** is a packed physical unit square.
Its **selected core** is a concentric square of side $B=9977/10000$, turned to a nearby
orientation in the retained list of 361 rational square orientations.
Here $D=207107/90000000$ bounds the tangent of the angular mismatch.
The proved inequality $B(1+D)<1$ puts that closed core strictly inside its parent.
Distinct parents therefore have disjoint closed selected cores.
This selection applies to parents at arbitrary physical angles.
[Transfer proof](proofs/five-dot-transfer-review.md)

An **owner** is a parent whose selected core contains a prescribed **mark**, a point
near a container corner.
The
[corner-pair theorem](../agenda-030/bc-303-first-wave-selection.md#3-replay-of-the-corner-pair-theorem-lane-c)
gives four distinct owners in every hypothetical eleven-square packing at $q$. Each
contains at least one of two marks for its corner.
It does not fix their centres, put them flush against the walls, or identify them with
four literal corner squares.

An **owner class** chooses a mark and restricts the core’s position and orientation
relative to it. For the present classes, choose perpendicular signed core axes with
nonnegative projections of the mark-to-centre displacement, ordered counterclockwise.
Put the first axis in one of eight closed angular sectors.
An axis need not point directly at the centre.
Two marks and eight sectors give sixteen classes per corner, or $16^4=65{,}536$ raw
combinations. Closed boundaries overlap safely; a core owning both marks still counts as
one owner. The [sector proof](../agenda-031/proofs/corner-owner-sector-footprints.md)
establishes that these classes cover all possibilities.
A **footprint** is a fixed closed patch contained in every owner core in its class.

What must be exhaustive is coverage of possible packings, not the number of LP solves.
A proof can discard an impossible class, identify an equivalent one, or cover many
classes with one certificate.
It must explain why every remaining possibility is included.
Four compatible example owners show that their local conditions are realisable; they do
not show that seven additional squares can accompany them.

## Routes and Their Missing Steps

The priorities follow
[Agenda 032’s disposition](../../../../agendas/agenda-032-conditional-owner-sprint.md).

| Priority and route | What remains to prove | Cheap discriminator |
| --- | --- | --- |
| 1. Independently check T-023 | An independent implementation must confirm the same frozen five-dot result. | Replay this certificate with the independently controlled instrument. |
| 2. Reuse the certificate | Exact symmetries or occupied-region containment must connect another class to the certified one. | Compute whole-branch symmetry images and exact union-containment decisions. |
| 3. Try a small dot portfolio | Other classes need five or six piercing dots, or nonnegative weighted covers of mass below seven. | Screen a declared set of distinct classes with existing patterns; retain uncovered-core witnesses. |
| 4. Refine difficult classes | Smaller position-and-angle classes must remain exhaustive and give stronger residual restrictions. | Split one unresolved class and compare its new legal domains and cover results. |
| 5. Add structural premises | Compatibility, penetration, or contact lemmas must apply to every packing assigned to the new cases. | Test the exact premise on one unresolved class before building a larger case tree. |
| Reserve: global pricing | New sites must improve a relevant covering program and ultimately yield a complete certificate. | Run the retained paired-support mechanism test within its declared scope. |

**Certificate reuse** should precede new optimization.
Reflecting or rotating the container transports its patches and dots together.
Independently rotating individual owners does not.
If a new guaranteed occupied union $A'$ contains the certified union $A$, every core
avoiding $A'$ also avoids $A$, so the existing dots still cover it.
The required relation is exact set containment; greater area is insufficient.
Their class coverage is unmeasured.

**Different dot patterns** need not reproduce the same five points.
Six unit-weight dots would still exclude seven disjoint residual cores.
More generally, a **weighted cover** assigns nonnegative weights to points so that every
admissible residual core receives at least one unit.
Its available total must be below seven.
Weights inside the guaranteed occupied union can be removed, since actual residual cores
avoid it. If the exact minimum is $m>0$, normalize by $m$ and compare the resulting
available mass with seven.
Four owner patches do not automatically contribute four units of weight.
[Covering condition](../agenda-031/proofs/corner-owner-sector-footprints.md#exhaustive-branches-and-sound-banking)

Each candidate still needs complete centre coverage at the required net orientations.
Generic classes require the full 361-direction family unless a symmetry of both the
domain and weighted measure justifies a reduction.
Open event-cell coverage extends to actual boundary placements because weights are
nonnegative and the selected cores have strict clearance.
The physical-angle conclusion comes from core selection, not from sampling many angles.
[Exact exp144 receipt](exp-144-four-owner-endpoint-full-net-replay.json)

## When Footprints Are Too Weak

A footprint forgets some restrictions on its owner’s pose.
Smaller centre-and-angle intervals can enlarge this common region.
A stronger alternative asks whether a proposed residual core can coexist with at least
one legal owner pose in that class.
A core that intersects every possible owner can be removed even if it avoids the common
footprint. The [pose-refinement contract](proofs/owner-pose-refinement-contract.md)
derives such options; their target gains remain unmeasured.
Refine unresolved cases first.

**Compatibility pruning** removes a class whose required owners cannot coexist.
For example, two guaranteed closed core footprints intersecting even at one point
contradict the selected cores’ strict separation.
An empty legal-owner pose domain also removes a class.
Conversely, disjoint footprints do not prove compatible owners, and compatible owners do
not prove an eleven-square packing.

Other structural information could reduce the case tree.
The retained [corner and wall analysis](../agenda-030/lane-a-corner-structure.md) gives
a penetration-depth case cover and parent regions that follow from its hypotheses.
A region inside a parent obstructs other cores, but needs a core-containment proof
before it is credited as owner-core mass.
These occupants must not automatically be identified with the corner-mark owners.

Contact arguments need particular care.
A **contact** is a boundary meeting between squares or with the container.
The retained
[structural review](../../../../explorations/X-021-what-can-be-proved-about-eleven-squares.md)
distinguishes facts about a side-minimal packing from facts about an arbitrary packing
at $q$. Moving a minimizer into a larger container can turn contacts into near-contacts.
There is no established permission to freeze arbitrary contacts, force all four walls to
be touched, or remove rotations until a convenient pattern remains.
A contact-based route needs its own exhaustive reduction and any required tolerance in
the transferred conditions.

## What the Negative Results Leave Open

Exp137/138 and the
[independent exp141 audit](../../experiments/exp-141-independent-dual-salvage-audit.md)
show that deleting poses from one retained fractional family does not produce the
desired cover obstruction.
A **fractional family** assigns weights to possible cores with total weight through any
point at most one; its total lower-bounds required cover mass.
The point-only filters already fall below ten or seven.
Stronger obstacles containing those marks only delete more nonnegative weight.
Further unchanged-weight filters of that family therefore cannot recover those
thresholds. New placements or newly optimized weights remain possible.

A failed dot pattern, unfinished LP, or large optimum on restricted sites does not
decide the branch.
A decisive stopping test is an exact feasible fractional residual-core
family of mass at least seven, with depth at most one everywhere.
It would rule out every nonnegative point cover of mass below seven for that relaxed
branch. It would not construct seven coexisting unit parents.
The current deletion screens do not reach that threshold.

Keep [H-135 global pricing](../../../../hypotheses/H-135-paired-full-support-pricing.md)
as a separate reserve.
It asks whether full retained positive dual support exposes a site missed by a 32-row
truncation. Its unit-square transport is a mechanism test, not the present side-$B$
certificate. A successful witness still needs optimization and complete verification.
A global cover below eleven could replace the owner split; a mixed proof could instead
use different verified methods for different cases.
Neither outcome is established.

The next milestone is an independently confirmed certificate plus a measured extension
to more classes. There is presently no evidence that full case exhaustion is feasible.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
