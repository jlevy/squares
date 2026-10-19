# BC303 T2: From the Accepted Pose Domains to Exact Charge Tests

Date: 2026-09-13. Mathematical continuation of X-029, independently accepted under
`think-pcxo` with the implementation conditions stated below.
The source analysis and review were read-only; this retained note does not execute a
scientific target. The
[source-distinct review](../reviews/review-2026-09-13-bc303-t2-charge-bridge.md) records
the accepted deductions and required reader specifications.

The next useful bridge is a complete C charge sweep over open atom cells, together with
a cheaper sufficient test for S using only its first owner.
The proofs below remove the need to enumerate C edges and vertices as candidate minima.
No atomic charge, minimum, or scientific target was evaluated in this continuation.
T2, global availability, routing, and the n11 bound keep their existing status.

## Sources and Assumptions

The source checkout was inspected at `4f897b7b506e62d9a68670870469b844fecddf3f`. The
starting geometry and its accepted review are
[X-029](../../../packing/campaign/explorations/X-029-bc303-t2-exact-geometry-draft.md)
and the
[independent geometry review](../reviews/review-2026-09-13-bc303-t2-geometry.md).
The
[active n11 plan](../specs/archive/plan-2026-09-10-n11-daytime-strategy-and-explainer.md)
and
[selection theorem analysis](research-2026-09-12-n11-selection-routing-first-principles.md)
keep local helper tests separate from selection over actual eleven-parent packings.
The unavailable V3 planning source remains outside this analysis.

The measure is the literal
[BC293 source file used by BC303](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-293-measure-free-96-25.json):

$$
\mu=\sum_{\ell=1}^{377}w_\ell\delta_{p_\ell},\qquad
w_\ell\ge0,\qquad Ww_\ell\in\mathbb Z,\qquad W=4000000.
$$

The
[BC303 replay](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md)
supplies the imported complete coverage floor \(\mu(C)\ge800003/800000\). Thus

$$
W\mu(C)\ge4000015,\qquad
W\mu(\mathbb R^2)=45048398.
$$

These facts are imported from the retained source and review, not reverified here.
`git diff --exit-code 39714308ce2081abbd76624387d134fee4be6deb HEAD --` returned success
for the atom file, `owner_footprints.py`, `fractional/adaptive.py`,
`fractional/model.py`, `fractional/sweep.py`, and `wall-containment-contract.md`. The
[model](../../../packing/src/sqpack/fractional/model.py) defines rational atom
coordinates and weights, exact rational frames, and a required nonnegative-weight guard
at proof entry points.
A charge reader must call that guard before applying the boundary-monotonicity argument.
The existing [unconditioned sweep](../../../packing/src/sqpack/fractional/sweep.py)
already uses nonnegative closed-atom boundary monotonicity.
The new obligation here is proving that property remains sufficient after imposing the
particular C roles.

Use X-029’s closed, symmetric source equipment, all 182 eligible source charts, 181
distinct bin-0 orientations, closed core membership, and simultaneous parent
requirements. Write

$$
q=\frac{96}{25},\quad h=\frac{9977}{20000},\quad
a=\frac{3152}{3175},\quad b=\frac{2336}{3175},\quad
\delta=a-b,\quad m_1=(a,b).
$$

For an eligible non-axis ray \(r=(c,s)\), \(0<s<c\), use \(z=m_1+xr+yJr\),
\(X=h-\delta(c-s)\), and the source lower whole-angle tangent \(L\). The accepted C
domain is

$$
D=\lbrace0\le x\le X,\ 0\le y\le h,\ a+cx-sy\ge e\rbrace,\qquad
e=\frac{1+L}{2\sqrt{1+L^2}}.
$$

For either axis alias it is \(D=[0,h-\delta]\times[0,\delta)\), with parent walls
inactive. Label 15 is automatically absent on the non-axis C domains; the axis strict
upper edge is required.
These are source-specific results, not properties of arbitrary conditioned owner
domains.

## Deduction 1: C Minima Occur in Open Atom Cells

Every C chart has a strict interior anchor

$$
v=(X/2,\delta/2).
$$

Its rectangle inequalities are strict, including the axis bound.
For non-axis charts its left-wall clearance satisfies

$$
a+cX/2-s\delta/2>a-\delta/2=\frac{a+b}{2}=\frac{2744}{3175}
>\frac1{\sqrt2}\ge e,
$$

where \(2(2744/3175)^2-1=4978447/10080625>0\). Hence each domain is convex and every one
of its points is a limit of interior points: the segment toward \(v\) lies strictly
inside all the active domain inequalities after leaving its starting point.

For an atom \(p\), put

$$
U_p=(p-m_1)\cdot r,\qquad V_p=(p-m_1)\cdot Jr.
$$

It belongs to the core exactly when

$$
(x,y)\in R_p=[U_p-h,U_p+h]\times[V_p-h,V_p+h].
$$

Fix any feasible \(v_0\). Every atom absent at \(v_0\) is outside a closed rectangle,
and therefore stays absent in some neighborhood.
There are finitely many atoms, so one neighborhood works for all absent atoms.
Throughout that neighborhood, the set of present atoms can only shrink relative to the
set at \(v_0\), giving \(\mu(C_v)\le\mu(C_{v_0})\).

The neighborhood contains an open subset of \(\operatorname{int}D\). A finite union of
atom event lines cannot fill that subset.
Choose a point there off every event line.
It is feasible, belongs to an open two-dimensional atom cell, and has charge no larger
than the original point.
Consequently

$$
\boxed{\min_{v\in D}\mu(C_v)
=\min_{\text{feasible open atom cells }\sigma}\mu(\sigma).}
$$

The minimum exists because only finitely many atomic membership sets occur and each
chart is nonempty. This argument covers C rectangle edges, atom intersections, vertices,
source-endpoint parent tangencies, and the included parts of the axis domain.
It does not add the forbidden axis edge \(y=\delta\).

This supplements X-029’s complete all-strata method with a proof that lower-dimensional
C strata cannot improve its answer.
Their closed predicates remain necessary for witness validation and synthetic controls.
The lemma does not allow arbitrary conditioned boundaries to be dropped, and it has not
established interior density for jointly realizable S configurations.

## Deduction 2: A Complete C Sweep Needs Only a Feasible Prefix

Partition \([0,X]\) and \([0,h]\) at all atom event coordinates in their interiors.
For the axis substitute the upper bound \(\delta\) on the second coordinate.
Use consecutive open intervals.
On \(\sigma=(x_-,x_+)\times(y_-,y_+)\), the integer charge \(N_\sigma=W\mu(C)\) is
constant. In a non-axis chart,

$$
M_\sigma=a+cx_+-sy_-
$$

is the unattained supremum of left-wall clearance.
Thus the open cell is feasible exactly when

$$
\boxed{M_\sigma>e
\quad\Longleftrightarrow\quad
4M_\sigma^2(1+L^2)>(1+L)^2.}
$$

Squaring is sound because \(M_\sigma\ge a-h>0\). Equality is infeasible for this open
cell. An original boundary pose at equality is nevertheless covered by Deduction 1
through another feasible open cell of no greater charge.
All axis cells inside the prescribed rectangle are feasible.

For fixed \((x_-,x_+)\), the feasible y intervals form an initial segment: the displayed
clearance decreases strictly with \(y_-\). This yields a complete sweep:

1. Project all source atoms exactly and clip their closed membership rectangles to the
   sweep domain. Discard zero-width or zero-height intersections only from the open-cell
   calculation; retain every original atom for closed witness replay.
   Deduplicate the rational x and y event levels, including the domain bounds.
2. Sweep the open x strips.
   Schedule each nondegenerate clipped rectangle’s positive weight at its left x
   endpoint and negative weight at its right endpoint, over exactly the y intervals in
   its clipped range. Start with zero and process every event at the lower domain bound.
   At each later x coordinate, apply all coincident starts and ends before querying the
   immediately following open strip.
   Never query an intermediate update state.
   This includes rectangles that cover the whole domain and have no original interior
   event.
3. Maintain range additions and a range minimum over the y intervals.
   Find the last feasible interval by exact monotone comparisons with the boxed formula,
   then query the minimum on that prefix.
4. Take the minimum over every x strip and every eligible source chart.
   Retain an attaining cell and source identity, or a replayable lower-bound result.

This covers all open cells by their x strip and y index; the event updates reproduce the
literal rectangle indicators; the prefix test is equivalent to parent existence;
Deduction 1 supplies completeness over the original closed-core role domain.

Computing the minimum, a threshold verdict, and one attaining cell takes \(O(m\log m)\)
exact arithmetic operations and \(O(m)\) working storage per chart with a range-add
segment tree. This excludes bit complexity, rational-witness reconstruction, and
materializing all low-charge cells.
There can be \(K=O(m^2)\) such cells; retaining them requires at least proportional
output work and storage.
The second-stage S pairing calculation needs its own complexity and coverage accounting.
A dense integer array is a simpler independent implementation.
Before pruning, each C direction has at most \((2m+1)^2\) open cells, or 570025 at
\(m=377\). The later shared C/S grid adds a cut and has at most \((2m+2)^2=571536\) open
cells. Both axis aliases must remain in the source manifest; their equal closed-domain
closed-domain geometry permits one charge calculation with two explicit dispositions.
The interior second-mark sign line is unnecessary for the threshold calculation, because
the forced predicate is already exact on D. Full labels are recomputed for each retained
witness.

A feasible low-charge cell has a constructive rational witness.
Put

$$
x_n=x_+-(x_+-x_-)/2^n,\qquad
y_n=y_-+(y_+-y_-)/2^n.
$$

For some finite \(n\ge1\), the same exact quadratic test accepts its clearance.
Let \(U\) be the source cell’s upper whole-angle tangent.
Enumerate rational half-angle tangents \(0\le t<1\) until

$$
L<\frac{2t}{1-t^2}<U,
\qquad
\frac{1+2t-t^2}{2(1+t^2)}<z_x.
$$

These are exact rational tests.
The resulting folded parent ray is \(((1-t^2)/(1+t^2),\,2t/(1+t^2))\). Transport it
using the retained source reflection and quarter turn.
Positive wall clearance and density of rational unit rays guarantee termination.
Axis aliases admit the axis parent directly.
Replay all 377 closed atomic memberships, complete labels, and the matching contained
unit parent before accepting a witness.
The reader must retain the closed chart manifest; a single lower-index owner choice
cannot replace its source-endpoint policy.

## Deduction 3: S Has a Cheap First-Owner Sufficient Test

Every actual forced-0 S configuration has a unique owner of \(m_1\). X-029 puts that
owner in one of the eligible source strips

$$
E_r=\lbrace X<x\le h,\ 0\le y\le h\rbrace.
$$

All its parent wall conditions are inactive.
It owns \(m_1\), excludes \(m_2\), and supplies label 0. The strip is convex with dense
interior, so the proof of Deduction 1 applies to its individual charge.
Its minimum is a rectangular open-cell sweep with no wall filter.

The two calculations can share one exact atom projection and event sweep per chart.
Build the arrangement on \([0,h]^2\), insert \(X\) as an event, and for the axis also
insert \(\delta\) as a y event.
C queries the intervals with \(x<X\), its appropriate y range, and its wall prefix.
The S first-owner test queries \(X<x<h\) over the whole y range.
Deduction 1 justifies omitting the respective outer edges when taking each individual
minimum.
A separate rectangular array is an equally complete reference for S; it needs no
parent-angle oracle or second-owner geometry.

The imported coverage floor gives the second actual owner at least 4000015 integer mass.
A violating S pair must therefore satisfy

$$
N_1+N_2\le8524199
\quad\Longrightarrow\quad
N_1\le4524184\quad\text{and}\quad N_2\le4524184.
$$

In particular,

$$
\boxed{\min_{r,v\in E_r}W\mu(C_v)\ge4524185
\quad\Longrightarrow\quad
W\bigl(\mu(C_1)+\mu(C_2)\bigr)\ge8524200.}
$$

This proves the required strict S inequality if its premise is established.
It does not require finding the second owner or solving two parent angles.
A low-charge first-owner strip cell only shows that this sufficient relaxation failed;
it does not reject S or T2.

If the strip test fails, retain the low-charge cells for a second stage.
Every actual low-charge first-owner pose lies in the closure of at least one such open
cell, by the same neighborhood argument and finiteness of the arrangement.
For the joint test, use the union of those closures intersected with the original strict
strip as a necessary superdomain.
Recompute boundary charges exactly; an open cell’s charge is not automatically its
boundary’s charge. For fixed selected rays, actual strict cores obey at least one strict
separating-axis inequality

$$
|(z_2-z_1)\cdot n|
>h\bigl(1+|r_1\cdot r_2|+|\det(r_1,r_2)|\bigr),
\qquad n\in\lbrace r_1,Jr_1,r_2,Jr_2\rbrace.
$$

These rational linear branches give a complete necessary relaxation after retaining the
second owner’s exact mark exclusion, absence of label 15, and individual parent
projection.
Excluding every low-charge pair in that relaxation would prove S. A surviving
pair needs simultaneous physical-parent replay.
Do not infer that the general S boundary strata are dispensable merely because the
individual strip is full dimensional.

## The Next Experiment and Its Frozen Criteria

The source-distinct review under `think-pcxo` accepted the three deductions with the
event-sweep, complexity, and rational-parent conditions stated here.
The next implementation is the maintained source-bound reader contemplated under
`think-5zkv` and `think-d6ls`.

Before a scientific run, authenticate all source atom rows and their integer weights,
the complete source manifest, the source-cell policy, and the executing reader revision.
Independent controls must cover an atom on each closed edge and vertex, the forbidden
axis edge, coincident events, rational equality in the generic wall oracle, missing
aliases, a wrong atom row, and wrong-checkout implementation identity.
Compare the open-cell method with the all-strata reference on synthetic conditioned
domains, including a lower-dimensional domain where interior density fails and the
shortcut must be refused.

Freeze these outcomes before reading target charges:

| Test | Positive determination | Negative or unresolved determination |
| --- | --- | --- |
| C | Every feasible open cell has integer mass at least 4524200 | A source-bound, geometrically replayed witness at or below 4524199 rejects C and hence opposite/combined T2; an incomplete enumeration is unresolved |
| S first-owner sufficient test | Every strip cell has integer mass at least 4524185; the imported floor then proves S | A lower cell rejects only this sufficient test and advances to the actual S pairing problem |
| Disclosed S geometry control from X-029 | No positive universal claim follows from its charge alone | It rejects S only if exact total mass is at most 8524199 and both simultaneous parents and complete labels replay |
| Combined T2 | Both C and S are proved strictly above their thresholds | Either exact actual-role witness rejects opposite/combined T2; opposite rejection alone leaves adjacent-only T2 open |

The existing rational C control at \((6/5,9/10)\) and X-029’s simultaneous rational S
control are bounded, disclosed witness checks once the source-bound reader is admitted.
No charge is attached to either here, and no threshold outcome is predicted.
The new sweep construction guarantees that a C rejection can be represented by a
rational core centre and rational physical parent; it does not establish that such a
low-charge cell exists.

No accepted mathematical claim needs withdrawal.
X-029’s all-strata proposal remains sound; the C perturbation proof offers a smaller
complete implementation.
The S first-owner inequality is a new sufficient route with a clearly weaker negative
outcome than the actual S test.
Global local availability, selection into the admitted tuple family, and any stronger
n11 bound remain separate proof obligations.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
