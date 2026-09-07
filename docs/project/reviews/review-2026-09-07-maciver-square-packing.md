# MacIver’s Square-Packing Papers: Source and Method Review

Reviewed 7 September 2026 against David R. MacIver’s public repository at
[`9e2cd597047e040a63b7dcd103e79962cfc2d781`](https://github.com/DRMacIver/square-packing-research/tree/9e2cd597047e040a63b7dcd103e79962cfc2d781),
committed 10 August 2026. The user supplied this lead during the Stromquist n26 review.
The supplied URL was this project’s own site; the author’s repository and its
paper-facing pages identify the relevant work.

The source was absent from this repository’s literature and frontier records.
Its proposed numerical bound does not improve our verified bounds.
Its geometric arguments offer possible inputs to existing proof work, subject to the
separate checks below.

## The Bound and Its Evidence

MacIver’s 8 August paper,
[*An improved lower bound for packing seventeen unit squares in a square, via a deformation of Green’s scaffold with certified defect charging*](../../../packing/resources/web/maciver-square-packing-2026-09-07/maciver-2026-seventeen-unit-squares-lower-bound.pdf),
Theorem 1.1, asserts

$$
s(17) > B := \frac{40\sqrt2+19}{17}+\frac1{200}
=4.450208382054341291\ldots.
$$

Deleting a square transfers the asserted lower bound to n18. Both current
[n17](../../../packing/frontier/n-017.md) and [n18](../../../packing/frontier/n-018.md)
records carry the independently verified lower bound $459/100=4.59$. The comparison is
exact:

$$
\frac{459}{100}-B=\frac{11789-8000\sqrt2}{3400}>0,
\qquad 11789^2=138980521>128000000=2(8000)^2.
$$

The improvement between these numbers is about $0.139791617945659$ in container side.
The source belongs in the chronology and method record; it changes no operative verified
bound. Its assertion of priority since Green’s 2000 result is not adopted.

The proof combines fourteen interval–Farkas certificates with a 634,562-row
combinatorial ledger.
The public Lean file explicitly formalizes only its algebraic identities and abstract
counting identity. A successful build of that file cannot establish the packing
exclusion. The paper’s appendix and retained aggregate log report a successful
source-side replay. Those reports are not an independent replay here.
The full pinned snapshot contains none of the fourteen named certificate files, none of
the cited `scripts/s17_green_*.py` replay files, and no Makefile implementing the
paper’s commands. Its `LEAN-CHECK.md` locates the computational artifacts in an
author-local checkout.
The
[archive packet](../../../packing/resources/web/maciver-square-packing-2026-09-07/README.md)
records this specific source-availability gap.

All three papers state that their AI-assisted proofs and exposition have not yet
received adequate human review.
This review checks the claims, their interfaces, and selected arguments; it does not
certify all three papers.

## Methods Worth Retaining

### Defect charging and a co-hit graph

The n17 paper permits some squares to miss its sixteen scaffold points.
For a hypothetical packing of seventeen squares, let $E$ count squares containing no
scaffold point in their interior, $U$ count unused points, and $R$ count incidences
beyond the first in each nonempty square.
Writing $H$ for the total number of incidences gives $U=16-H$ and $R=H-(17-E)$, hence
$E=U+R+1$. This identity follows directly from disjoint interiors and was independently
re-derived in this review.

The paper then certifies losses caused by empty squares.
If $B_{\rm lost}$ is the set of lost points and $\Gamma$ contains an edge within each
multiply hit set, those sets yield a matching and
$U+R\ge |B_{\rm lost}|-\nu(\Gamma[B_{\rm lost}])$. Adding a vertex increases the
matching number by at most one, so certified subsets of the lost set give safe weaker
inequalities. This combinatorial step also checks directly.
The difficult remaining claim is complete geometric classification and valid loss
certificates, not the counting identity.

The method can inform the existing resource-and-compatibility program
([H-111](../../../packing/campaign/hypotheses/H-111-resource-anchor-case-exclusion.md)
and [H-118](../../../packing/campaign/hypotheses/H-118-capacity-versus-coupled-lp.md)).
For n26, it suggests a possible way to handle defects in a recovered Green point
configuration, under `think-0x08`. It supplies neither Green’s missing n26 coordinates
nor a transferred n26 theorem.
The n17 scaffold, classifications, and certificate clauses cannot simply be reused at
n26.

Its geometric certificates also use correlated translation regions.
For $g\ge0,\kappa>0$, evaluating the three vertices of a triangular region gives

$$
\max_{0\le y\le g,\ |z|\le y/\kappa}(ay+bz)
=g\max\{0,a+|b|/\kappa\}.
$$

This exact elimination avoids replacing the triangle by a larger coordinate box.
It is a candidate technique for
[H-119](../../../packing/campaign/hypotheses/H-119-shared-anchor-correlation.md) after a
common-anchor correlation loss is identified; the formula establishes no capture gap or
comparator limitation on its own.

### Center triangles and local capacity

[*The Center-Area Lemma*](../../../packing/resources/web/maciver-square-packing-2026-09-07/maciver-2026-center-area-lemma.pdf),
Theorem 1.1, states that three interior-disjoint unit squares whose centers form a
non-obtuse triangle have center-triangle area at least $1/2$. Three axis-parallel
squares centered at $(0,0),(1,0),(0,1)$ attain equality.
The non-obtuse hypothesis is essential: centers $(0,0),(1,\epsilon),(2,0)$ of
axis-parallel unit squares are admissible, with obtuse center triangle of area
$\epsilon$ for $0<\epsilon<1$.

The proof freezes a separating axis owned by one square for each pair, minimizes
center-triangle area within those constraints, and converts first-order optimality into
a reciprocal force diagram.
Ownership cases reduce the final step to scalar inequalities.
The source exposes full Lean theorem entrypoints for this lemma.
The two paper-facing wrappers share the reciprocal implementation; they are not two
independent proofs. The separate corner-trap route is
`CenterAreaLemma.center_area_lemma_from_axis_aligned_normalized` in
`CenterAreaLemma/Basic.lean`. The formal statements, their dependency closures, and
replay status must be distinguished from the mathematical outline.

This is a candidate for rejecting configurations of three center boxes after the boxes
force non-obtuseness and an area below $1/2$. A bound on pairwise center distance alone
cannot supply it: an equilateral triangle of side one has area $\sqrt3/4<1/2$. It is
also not a consequence of Delaunay triangulation, whose triangles may be obtuse.
Before adoption, replay the theorem and implement outward-rounded checks of the actual
box hypotheses, including equality and collinear controls.

A concrete design check uses square center boxes of coordinate radius $1/200$ around
$(0,0),(51/50,0),(51/100,9/10)$. Throughout these boxes, squared pair distances are at
least $1.0201,1.0421,1.0421$, so incircle separation cannot reject them.
The three angle dot products are at least $0.4959,0.4959,0.5217$, while doubled triangle
area is at most $0.9425<1$. Thus the center-area lemma would exclude the whole box
domain. These finite decimals are exact rational interval bounds, re-derived
independently; they specify a control for a future instrument, not an executed packing
search.

[*Counting unit squares by their centers: sharp convex bounds and exact strip laws*](../../../packing/resources/web/maciver-square-packing-2026-09-07/maciver-2026-counting-unit-squares-by-centers.pdf)
studies squares whose centers lie in a region; squares may protrude.
Its rectangle bound is $N_{\max}(a,b)\le(a+1)(b+1)$, with exact narrow-strip and
three-center thresholds supplying more local information.
Its convex extension is $N\le\operatorname{area}(K)+w_x(K)+w_y(K)+1$. The paper
distinguishes its formalized rectangle and strip results from the unformalized convex
clipping proof and local toolbox.

These are candidate capacity cuts for restricted center domains.
Applied to the entire center box $[1/2,L-1/2]^2$, the rectangle formula gives only
$n\le L^2$, the existing area bound.
Any useful gain needs smaller, correlated center regions or a sharper strip threshold.
Wall and corner formulas must retain containment and wall-distance hypotheses; a
center-region result and a contained-packing result are different statements.

For example, the paper’s very-narrow law applies to $w=1/5,h=29/10$: $w<(\sqrt2-1)/2$
and $w^2+h^2=169/20$ lies strictly between $4$ and $9$. It gives capacity
$\lfloor\sqrt{169/20}\rfloor+1=3$ where the rectangle formula gives only
$\lfloor(6/5)(39/10)\rfloor=4$. This is a specific local comparison for H-118 after the
theorem is replayed.
It does not settle H-118, whose acceptance also requires an exact surviving witness for
the declared coupled LP on the same natural target domain.

## Formal-Verification Evidence

The pinned source requests Lean 4.29.1 and pins mathlib to
`5e932f97dd25535344f80f9dd8da3aab83df0fe6`. GitHub’s run API reports
[Lean build 31393239180](https://github.com/DRMacIver/square-packing-research/actions/runs/31393239180)
successful at the pinned source commit on 10 August 2026. Individual job logs were not
obtained, and no local Lean build or axiom-dependency replay was performed.
This is external CI evidence, not an independent kernel replay.

The relevant paper-facing files are
[`CenterAreaLemmaPaper.lean`](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/PaperProofs/CenterAreaLemmaPaper.lean),
[`NmaxPaper.lean`](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/PaperProofs/NmaxPaper.lean),
and
[`S17Paper.lean`](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/PaperProofs/S17Paper.lean).
The first-party Lean source scan found no `sorry`, `sorryAx`, `axiom`, `admit`,
`native_decide`, or `unsafe` tokens.
That scan does not establish what axioms appear in every theorem’s transitive dependency
closure. The paper reports standard classical axioms in its own `#print axioms` output.
Neither the source scan nor the successful build is described here as global axiom
freedom.

## A Claimed Method Barrier That Cannot Be Used

The repository’s historical
[`reports/square-solver.md`](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/reports/square-solver.md)
claims that all scalable witness-measure methods have an n17 ceiling of 4.5. The same
paragraph describes floating-point LP calculations and says exact rational duals still
need to be supplied.
As a universal claim about weighted unavoidable measures, it conflicts with our verified
$4.59$ certificate; the independently replayed Massaccesi $4.5058$ certificate already
exceeds it.

Do not use this note to stop weighted-measure work.
A finite support LP can establish a restriction of its own support family only if the
constraint direction, complete pose domain, and exact certificate are correct.
Reopening this particular claim requires its original model and a valid dual with an
explicit explanation of the discrepancy.
The broad ceiling is not adopted as a theorem.

## Recorded Disposition

Retain the three dated source identities, original paper bytes and faithful extractions,
the exact n17/n18 comparison, and the limits of the available verification.
Link the n17 proposal as source-reported historical evidence.
Keep the operative lower-bound fields at 4.59.

The next useful adoption step, tracked as `think-sske`, is a bounded replay of the
center-area, rectangle, and very-narrow-strip theorem entrypoints, followed by a
comparison of local capacity cuts in the existing H-118 program.
Replaying the weaker n17 numerical result has lower immediate value; its missing
computational artifacts must be recovered before any such replay can be complete.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
