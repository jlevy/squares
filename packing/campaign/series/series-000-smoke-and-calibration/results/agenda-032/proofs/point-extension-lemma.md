# Point-Extension Lemma

**Verdict:** exact, with matching support and domain assumptions.
Review by the existing GPT-6 Astra agent at extra-high reasoning, 2026-09-09. No target
result was inspected or computed for this lemma.

Let P={m1,...,mk} be k distinct owned marks.
Let ν be a nonnegative atomic measure giving mass at least one to EVERY contained B-core
whose closed square avoids P. Apart from strict-domain boundary conventions, this must
be the point-only residual family: no additional owner-angle, footprint, or coexistence
restrictions are allowed in this premise.

Then

`μ = ν + δ_m1 + ... + δ_mk`

is a global B-core cover.
A core meeting P contains at least one added unit atom and therefore has mass at least
one. A core avoiding P already has ν-mass at least one.
Multiple marks in the same core cause no problem.
The global measure has total mass ν(K)+k. This is an exact feasible construction
requiring no LP optimality assumption.

## Boundaries and Angle Transfer

The split uses closed-core containment: a mark on a core edge or vertex receives its
unit atom. A core not containing a mark has positive distance from that point.
If the residual reader covers only strictly contained cores, an unmarked core touching
the container boundary can be approached by strictly contained unmarked cores.
Nonnegative atomic weights make the limiting closed-core mass at least that of
sufficiently close generic placements.
Thus the construction also covers contained boundary poses whenever the container centre
domain has nonempty interior, as it does here.

Apply the argument on the same retained direction family as the residual cover.
The existing B-shrink theorem then supplies the same all-angle transfer.
The added atoms address marks in selected B-cores; no assumption about marks being
strictly inside those cores is needed.

## Optimization Consequence

For independent variables on matched support S containing P, write τ0(S) for the
unrestricted optimum and τP(S) for the point-only residual effective-mass optimum.
Atoms on P may be deleted from a residual measure because its cores avoid them.
The construction proves

`τ0(S) ≤ τP(S)+k`, hence `τ0(S)−τP(S)−k ≤ 0`.

The same holds with unrestricted atom support.
If S omits a mark, the direct conclusion instead uses the augmented global support S∪P;
it does not bound the original finite-support global program.
If global variables are tied by a genuine symmetry group, averaging the constructed
GLOBAL cover restores those ties at unchanged total mass, provided the global domain and
support are invariant.
Arbitrary variable ties have no such guarantee.
A generic asymmetric residual family still needs its complete reflected directions;
symmetry averaging does not repair missing residual coverage.

Thus one point can save at most one unit, and four points at most four, in the true
matched optimum.
Point conditioning alone cannot improve the exclusion gap after charging
for the removed owners.
Occupied area or other structural constraints are where additional power can enter.
This statement does not bound the gain from a stronger residual family that avoids a
triangle or an owner core.

As a conditional corollary, a matching unrestricted all-site dual lower bound of at
least eleven would force every one-point residual optimum to be at least ten and every
four-point residual optimum to be at least seven.
That conclusion requires the same q, B, direction/core domain, and all-site capacity
scope; this note does not assert that a particular retained lower-bound artifact
satisfies those conditions.

## Numerical Sanity Check

For genuinely settled matched programs, expect `M0−Mpoint≤1+tolerance`, or at most four
for four marks. A material violation calls for checking global optimality, residual row
completeness, support inclusion, symmetry grouping, and the definition of the residual
domain.

Two arbitrary feasible primal objectives can violate that numerical inequality because
the global candidate may be suboptimal.
Such a comparison alone neither refutes the lemma nor proves an optimum gap.
A sharper constructive diagnostic is to add the unit mark atom to the verified residual
proposal and test the resulting global proposal: it has a known feasible mass of
Mpoint+1. An exact global dual lower bound greater than that verified mass would
contradict weak duality and expose a contract or implementation error.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
