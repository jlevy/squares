# Fixed-Four-Corner Cover Transfer Review

**Verdict:** a positive exact full-net coverage bound permits exact rescaling of the
retained atom measure into a valid conditional cover, without another LP solve.
This gives a feasible cover mass.
A packing exclusion requires that effective mass to be below seven; an improvement
between LP optima requires a matching dual lower bound.

**Status, 2026-09-09:** analytic review by the existing GPT-6 Astra agent at extra-high
reasoning. The reported experiment numbers are inputs to this review.
No target minimum was evaluated, no measure was normalized, and no numerical result was
selected here.

## The Conditional Branch

Let q=96/25, K=[0,q]², and B=9977/10000. The four physical unit squares are fixed
axis-aligned and flush in the four corners.
Write O for their closed union.
The hypothetical packing has seven other physical unit squares.

The measure must have exact nonnegative rational weights, coordinates in K, and exact D4
symmetry of the weighted measure.
Position symmetry alone is insufficient.
The obstacle union O is also D4 invariant.
The exact reader must use the specified B and the complete retained 181-direction folded
net, with a sound centre-domain cover for cores avoiding O. The existing six-piece
domain is specific to this fixed-four-unit branch.

Let m>0 be an exact rational lower bound on covered mass for every relevant net core.
It is enough to verify all reachable open event cells and justify their boundary
transfer as below. Calling m an exact minimum over the swept cells is consistent;
asserting a minimum over a larger closed contact domain needs the corresponding
completeness proof.

Then the scaled measure ν=μ/m gives every relevant net core mass at least one.
This is exact homogeneity: no optimization, new rationalization, or numerical adjustment
is needed. Scaling preserves nonnegativity, support, and D4 symmetry.
If the exact reader returns zero or cannot complete the declared coverage scope, this
normalization theorem supplies no positive cover.

## Transfer to Physical Squares at Every Angle

The retained half-tangents are t_j=(207107/500000)j/180. They start at zero and reach
beyond tan(π/8), since

`t_180²+2*t_180−1 = 309449/250000000000 > 0`.

The largest tangent of a half-gap between adjacent direction angles is

`D = max (t_(j+1)−t_j)/(1+t_j*t_(j+1)) = 207107/90000000`.

The strict shrink condition is

`B*(1+D) = 899996306539/900000000000 < 1`.

After folding a physical square’s angle by a container D4 symmetry, choose the nearest
retained direction.
If the angular discrepancy is δ, then tan|δ|≤D. A concentric B-square
at that direction has extent, in either parent-axis direction, at most
`(B/2)*(cosδ+|sinδ|) < 1/2`, because `cosδ+|sinδ| ≤ 1+D`. Thus its closed core lies
strictly inside the physical unit parent.
Undo the fold to obtain the actual selected core.

The weighted measure and O are invariant under the same container symmetry, so folding
preserves both admissibility and covered mass.
Consequently the 181 folded directions suffice here.
They would not suffice for a generic asymmetric owner footprint without its additional
reflected direction family or a proved branch stabilizer.

Each of the seven selected cores lies strictly inside its own parent and inside K. It is
disjoint from the entire CLOSED union O: if a core point lay on an obstacle boundary, an
open ball about that point inside its parent would also meet the obstacle interior,
contradicting disjoint parent interiors.
Compactness gives positive distance from O for each actual core.
Distinct selected cores are likewise disjoint compact sets.

Their centres therefore lie in the strict residual domain and have feasible open
neighbourhoods. At an atom-event boundary, sufficiently nearby generic placements can
lose boundary atoms but cannot gain atoms absent from the limit core; nonnegative
weights imply that limit mass is at least the nearby mass.
This is why open event-cell coverage is enough for actual selected cores.
Ignoring a zero-area touching component does not automatically verify every artificial
weak-contact placement, but actual strict cores do not depend on those components.

## What the Normalized Mass Proves

Let M=μ(K). The conservative feasible cover receipt is

`U = M/m`.

If U<7, seven disjoint remaining cores would carry total ν-mass at least seven inside K,
a contradiction. If U≥7, this receipt does not exclude the eleven-square branch.

A tighter effective-mass receipt is available by deleting atoms in closed O. Actual
residual cores avoid O entirely, so their mass is unchanged.
Put `M_out=μ(K\O)` and use

`U_eff = M_out/m`.

The counting contradiction requires U_eff<7. Deletion retains D4 because O is invariant.
It is valid for the strict residual family even if the restricted measure changes the
coverage of artificial touching poses in a larger weak domain.
The mask and the scope should be explicit in the receipt; do not silently substitute
this mass for the originally reported total.

This exclusion concerns the literal four-flush-unit branch.
It does not prove the general n=11 lower bound or normalize arbitrary packings into that
branch. Exclusion at q also excludes smaller sides within the same branch: embed the
remaining squares unchanged and move each fixed corner square outward to its
corresponding corner of K. Its intersection with the old container is a subset of its
old corner square, so this relocation creates no new overlap.

The reported rationalized residual total is 7.804903. With that total, the conservative
threshold would require `m > 7.804903/7`; a positive m by itself is far from enough.
No value of the full-net m has been assumed or evaluated in this review.
For any verified U_eff, the counting argument more generally excludes a branch with r
remaining squares whenever the integer r is strictly greater than U_eff.

## Feasible Masses Versus an Objective Gap

The reported numerical values are M0≈11.981481481481488 and Mres≈7.804878048780487,
giving M0−Mres−4≈0.1766034. The rationalized totals are 11.981511 and 7.804903. These
describe solver proposals and rounded measures.
Full-net exact minima m0,mres could convert them to verified feasible masses U0,Ures;
the minima may differ, so the original score cannot simply be relabelled an exact
full-net result.

Even if U0−Ures−4 is positive, subtracting two feasible upper bounds does not prove a
gap between the true covering optima τ0 and τres.
To prove an improvement beyond the four-owner accounting, obtain

`L0 ≤ τ0`, `τres ≤ Ures`, and `L0−Ures−4 > 0`.

L0 needs an exact feasible global covering dual with the same support and variable
grouping as the claimed comparison.
A finite set of legal global rows suffices for such a lower bound, even if those rows
use only a subset of the full directions; adding rows cannot lower the optimum.
It must satisfy every candidate-column capacity constraint.
A statement about unrestricted atom support instead requires the stronger all-site
capacity proof. The dual and primal receipts must identify which optimization problem
they bound. If Ures uses the outside-obstacle effective mass, τres must use that same
objective; do not silently compare it with an unbanked total-mass program.

There is also a useful comparison requiring no optimality claim.
From a verified unrestricted measure μ0/m0, restrict to K\O. Each fixed unit contains a
contained axis B-core, so the global cover gives μ0(O)/m0≥4. The directly constructed
residual cover has effective mass

`U0_restricted = (M0−μ0(O))/m0 ≤ U0−4`.

Comparing Ures against U0_restricted measures improvement over this particular
constructible baseline.
Using only U0−4 may under-credit that baseline if the actual mass in O exceeds four.
This remains a comparison of feasible measures, not a theorem about optimal values.

## Exp137 Consequence for the Next Lane

The sprint coordinator reports that Exp137 completed its exact fixed-weight deletion
filters with no obstruction in any one-owner or four-owner class.
The point-only survivor masses are `77421212793/8221052780 < 10` for the one-owner cases
and `13394344077/2055263195 < 7` for the four-owner cases.
These receipts were not independently re-run in this review.

This closes the proposed additional deletion filters on that same weighted family.
Every stronger footprint containing the owned mark has a smaller avoidance domain.
Every fixed owner contains its mark; likewise, a residual core that can coexist with
some owner must avoid the mark contained in every possible owner.
Such survivors are therefore subsets of the point-only survivors.
The weights are nonnegative, so their retained total cannot increase to ten or seven.
The same conclusion holds for all centre-and-angle refinement classes that retain their
known mark constraint.

An inset rectangle that omits its mark should not be tested alone to evade this
conclusion: doing so drops a known restriction.
Include the mark or the previous footprint in its convex hull, as the refinement
contract specifies.

Consequently the extra fixed-family refinement filters proposed earlier should not run.
The refinement remains useful as a stronger conditional LP domain.
A new dual attempt would need to re-optimize survivor weights under a freshly verified
pointwise capacity bound, add different legal placements, or both.
The low mass of the unchanged surviving weights does not bound the optimum of those new
programs and does not establish that a conditional cover below ten or seven exists.

## Minimum Honest Receipt

Retain the unchanged source atom artifact, exact total M, exact outside-obstacle total
if used, exact full-net minimum or certified lower bound m, worst direction, completed
direction list, nonnegativity and weighted-D4 checks, B and D, domain scope, and the
exact ratios M/m and M_out/m. Label the resulting object a verified feasible conditional
cover with its strict threshold test.
A deadline, incomplete direction pass, or positive numerical score is not a completed
exact receipt.

The source contracts are `packing/src/sqpack/fractional/certificate.py` for the
net/shrink theorem and `packing/devtools/run_residual_cover_pilot.py` for the six-piece
conditional domain and exact event reader.
The reader currently includes all component vertices and all atom events and preserves
separate component spans.
Its returned rational minimum can support this argument once the declared full-net run
and input checks complete under the fresh protocol.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
