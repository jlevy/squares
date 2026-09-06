# BC-254: Exact Finite-Support Screen Design

Status: design only; the support has not been generated, no target LP has run, and
instrument readiness and measured cost remain pending.
This is the W3 first slice for BC-254 / H-099 / `think-01q4`, under
[Agenda 024’s Current Allocation](../../../../agendas/agenda-024-post-381-24h-portfolio.md#current-allocation)
and
[Agenda 026’s BC-254](../../../../agendas/agenda-026-density-stationarity-and-trump-capture.md).
The source inspected is Git commit `c14451f5378e55dd072327d6d8f55dc957fbc5c3`. The
coordinator must commission controls, review readiness, and freeze the experiment and
instrument before any target measurement.

The proposed discriminator is a rational upper certificate for a relaxation with at most
eleven orbit variables.
A certificate at most eleven rejects only
[H-099’s specified support claim](../../../../hypotheses/H-099-trump-d4-finite-support-dual.md).
A larger finite-row optimum is a candidate for further checking, not a dual lower bound.
The
[BC-242 weak-duality contract](bc-242-full-size-density-proof-contract.md#almost-everywhere-dual-and-weak-duality)
supplies the measure semantics; its historical pilot allocation does not fund this work.

## Exact Support and Orbit Variables

Use the eleven ordered corner lists returned by
[`cases.trump11.packing.build`](../../../../../cases/trump11/packing.py), without moving
or adding a square. Its field is $K=\mathbb Q(u)$, where $u$ is the unique root in
$(36/100,37/100)$ of

$$
5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1=0,
\qquad U=\frac{6u+4}{1+2u-u^2}.
$$

[`sqpack.field`](../../../../../src/sqpack/field.py) provides reduced rational
power-basis coefficients, exact equality, and signs from rational isolating intervals.
Use one field instance throughout construction.
Geometry stays in $K$; weights, neighborhood radii, LP coefficients, and LP multipliers
use `Fraction`. Floating coordinates or rounded keys are not admissible inputs to a
certificate.

Let $R(x,y)=(U-y,x)$ and $F(x,y)=(U-x,y)$, and apply the eight maps $R^kF^e$, ordered by
$(e,k)$ with $e\in\{0,1\}$ and $k\in\{0,1,2,3\}$. For each image, sort its four corner
keys, each key being the pair of reduced rational coefficient tuples.
This sorted tuple identifies the geometric square independently of the starting corner,
orientation of traversal, and local quarter-turn parametrization.
Keep the ordered corners separately for incidence calculations.

Deduplicate all 88 labelled images by that exact key.
Order the resulting support $\mathcal F$ by key, then partition it into D4 orbits, each
represented by its least key.
Record every source-square/map preimage, every distinct orbit member, and $m_O=|O|$.
These are construction bounds, not measured counts: $|\mathcal F|\leq88$, at most eleven
orbits, and $m_O\in\{1,2,4,8\}$. Recheck unit edge lengths, orthogonality, corner
closure, and containment in $[0,U]^2$.

Orbit variables are valid without assuming symmetry of an optimizer.
Given arbitrary feasible weights $w_S$ on this D4-closed support, define

$$
\bar w_S=\frac18\sum_{g\in D4}w_{g^{-1}S}.
$$

Each transformed depth is at most one outside a null set.
The union of the eight exceptional sets is null, so their average is feasible almost
everywhere. The maps permute the support and preserve total mass.
Also, $\bar w_S$ is constant on each orbit and rational whenever the original weights
are rational. Thus restricting to a weight $a_O$ per distinct orbit member loses no
full-support feasible mass, and $D=\sum_O m_Oa_O$.

For the retained control, let $n_O$ count original Trump squares belonging to $O$.
Averaging the eight complete packings gives $a_O^0=n_O/m_O$ and $\sum_Om_Oa_O^0=11$.
Equivalently, each distinct placement receives its labelled preimage count divided by
eight.
Assigning weight $1/8$ to each deduplicated placement would discard multiplicities
and is not this control.

## Necessary Rows and Positive Neighborhoods

For an ordered unit square with corner $v_0$ and orthonormal edges $e_1=v_1-v_0$,
$e_2=v_3-v_0$, use the four affine forms

$$
\ell_1(x)=(x-v_0)\cdot e_1,\quad 1-\ell_1(x),\quad
\ell_2(x)=(x-v_0)\cdot e_2,\quad 1-\ell_2(x).
$$

All four are positive exactly in the interior.
Require a row point $q$ to lie strictly inside the container and off every supporting
line of every square.
Excluding a whole supporting line is stronger than excluding the boundary segment and is
sufficient here. Reject a zero affine value exactly; a tolerance must not classify it.

The neighborhood is constructive.
First certify the signs of all square forms and the four positive container margins.
Obtain positive rational lower bounds on their absolute values with
`NumberField.enclose`, refining by the existing exact sign procedure as needed.
Let $\gamma>0$ be the minimum of these lower bounds and set $\varepsilon=\gamma/4$.
Every unit edge has coordinate absolute values at most one, so changing either
coordinate by at most $\varepsilon$ changes each square form by at most $2\varepsilon$.
Container margins satisfy that bound too.
The checker verifies $|\ell(q)|>2\varepsilon$ for every square form and positive
container margin. Consequently $q+[-\varepsilon,\varepsilon]^2$ stays inside the
container and has constant incidence, with positive area $4\varepsilon^2$.

Define the integer row

$$
A_{qO}=|\{S\in O:q\in\operatorname{int}S\}|.
$$

This counts distinct placements, not labelled images and not merely whether an orbit
covers $q$. An almost-everywhere feasible orbit weighting must satisfy
$\sum_O A_{qO}a_O\leq1$: otherwise its constant depth on the certified neighborhood
would exceed one on a set of positive area.
No assertion that these rows cover all arrangement faces is needed for an upper
certificate.

### Initial rows

Visit orbit representatives in exact key order.
For each representative, try its center first.
If a supporting-line equality prevents admission, try $q_k=c+2^{-k}(1,2)$ in increasing
order $k=4,\ldots,4+4|\mathcal F|$, taking the first admissible point.
Verify that $(1,2)$ is nonparallel to every supporting line before using this fallback;
otherwise stop with a guard failure rather than select another direction after
inspection.

The fallback is finite under that guard.
Each supporting line excludes at most one $k$, while there are at most $4|\mathcal F|$
lines and one more trial point.
Each trial remains strictly inside its source square: its change in either unit-edge
projection is at most $3/16<1/2$. It is therefore strictly inside the container as well.
Retain the successful point, its radius, its source orbit, and the skipped equality
indices.
There must be at least one admitted row with positive coefficient in every orbit
column; otherwise refuse to solve.

### Deterministic extension

If the first exact relaxation has objective above eleven, append points
$q=(Ui/2^k,Uj/2^k)$ in increasing $(k,i,j)$ order, where $k=1,2,3,4$,
$1\leq i\leq j\leq2^{k-1}$, and at least one of $i,j$ is odd.
There are 36 candidate points by construction.
They form the denominator-at-most-16 grid in a D4 chamber.
For orbit weights, the row at any transformed point is identical, so adding its other
seven images is unnecessary.

Skip exact supporting-line equalities without perturbing these extension points.
For each remaining point, construct the positive radius above.
Deduplicate identical integer rows in admission order, retaining the first point as
representative and the other point dispositions in the run receipt.
The initial and extended matrices have at most eleven and 47 rows respectively before
this deduplication. If the first optimum remains feasible for every added row, retain it
with the earlier upper multipliers extended by zeros and recheck equality of the two
objectives; a second solve is unnecessary.
This also covers an extension that adds no distinct row.
The extension ends at this fixed grid; an unresolved screen authorizes neither finer
grids nor new support.

## Exact LP Contract and Solver-Independent Certificate

The relaxation maximizes $m^Ta$ subject to $Aa\leq\mathbf1$ and $a\geq0$. The existing
[`ExactLP` and `solve`](../../../../../src/sqpack/exact_lp.py) instead take a
minimization program with free variables and rows bounded above.
Supply exactly

$$
c=-m,\qquad B=\begin{bmatrix}A\\-I\end{bmatrix},\qquad
b=\begin{bmatrix}\mathbf1\\0\end{bmatrix},
\qquad \min c^Ta\text{ subject to }Ba\leq b.
$$

Use `Fraction` scalars, `rational_sign`, and the indices of the $-I$ rows as `start`. At
$a=0$ these rows are active and independent, and every incidence row has slack one.
This meets `solve`’s feasible-vertex contract; no phase-one solve or floating basis is
required. `certify_vertex` additionally requires optimal multipliers, so it must not be
used to demand that this starting vertex is already optimal.

The incidence matrix is nonnegative.
The initial-row guard gives, for every orbit $O$, some $A_{qO}\geq1$. Thus every
feasible point satisfies $0\leq a_O\leq1/A_{qO}\leq1$, proving finite bounds on the
objective before calling the solver.
A reported unbounded program would be an instrument failure under these guards, not
evidence about H-099.

Preserve the deterministic row ordering and call `solve(..., pivot_budget=64)`. There
are at most two solves: the initial matrix, then the fixed extension only after the
initial solve and exact replay return an optimum above eleven.
Each starts at zero; an earlier optimum need not remain feasible after extension.
A pivot-budget refusal stops this screen as unresolved and does not trigger another
basis or solver.
The total limit is 128 pivots; the design does not rely on a termination
claim about the solver’s pivot-order implementation.
No coefficient, point, or bound is read from a floating solve.

The independent upper check verifies a retained nonnegative rational vector $y$ and
reports its bound $V$ when

$$
A^Ty\geq m,\qquad V=\mathbf1^Ty.
$$

For any feasible $a$, $m^Ta\leq y^TAa\leq V$. Support retirement additionally requires
$V\leq11$. This proof does not trust solver status or optimality.
To extract $y$ from a solver certificate, expand its active multipliers onto all rows.
With $z$ denoting the nonnegativity-row multipliers, the solver’s equation is
$A^Ty-z=-c=m$, which has the required inequality direction when $z\geq0$.

Replay must regenerate the support and orbit sizes from the declared source, verify unit
geometry and containment, and regenerate every used incidence row.
Use oriented edge cross products for replay incidence, separately from the producer’s
edge projections; share exact field arithmetic and the retained packing construction,
not the proposed incidence matrix.
Check the rational radii and strict margins, all dimensions and rational types,
$y\geq0$, every column inequality, and the exact sum.
Recompute $a^0$, its mass eleven, and $Aa^0\leq\mathbf1$. A bound strictly below eleven
would contradict this retained control and is an invalid packet, not a better result.

For a larger finite-row result, replay a rational primal point $a\geq0$ with
$Aa\leq\mathbf1$ and match $m^Ta=\mathbf1^Ty$ to an upper witness.
Report that common value only as the exact finite-row optimum.
A point with mass above eleven still needs BC-243’s complete almost-everywhere depth
check before any dual lower-bound claim.
Only a fully verified $D>11$ obstructs a mass-eleven area density at $U$; it neither
closes the below-$U$ density question nor establishes global packing optimality.

## Control-Only Commission and Readiness

The proposed next implementation slice is at most 30 active author minutes, followed by
a separately allocated source-distinct review of at most ten minutes.
These are estimates for a future commission, not an extension of the current design
slice. Build only the reusable support, row, LP-adapter, and independent-certificate
routines needed by the controls below.
Do not invoke the Trump support builder or solve a target LP during this commission.
Label its records as non-target controls; their smaller ceilings are not H-099 results.

| Non-target control | Required outcome |
| --- | --- |
| In $[0,2]^2$, the D4 orbit of the axis-aligned unit square centered at $(3/4,3/4)$ | Four distinct placements; the center point $(1,1)$ has row $A=(4)$ and objective coefficient $m=(4)$. $y=(1)$ certifies the exact ceiling one despite positive-area overlaps. |
| The same control with corner rotations, reversed traversal, repeated raw images, and reordered source/map input | Identical geometric support, orbit size, mass, and recomputed incidence; raw duplicates never become distinct placements. |
| The same control with row point $(1/4,1)$, an enlarged radius, or a square crossing the wall | Refuse the boundary point, an uncertified neighborhood, and failed containment respectively. |
| Matrix $A=((1,2),(2,1))$, $m=(4,4)$, with the explicit $-I$ rows and zero basis | Exact adapter optimum $8/3$ at $a=(1/3,1/3)$; independent upper witness $y=(4/3,4/3)$. Reversing the objective or inequalities must fail these expectations. |
| A missing support member, a Booleanized incidence count, a changed orbit size, a negative or weakened multiplier, a float, or a malformed rational | Refuse the mutated certificate at the relevant source, geometry, type, or column guard. |
| In the same field $K$, a non-target axis-aligned square centered at $(3/4+u/100,3/4)$ in $[0,2]^2$ and its D4 orbit | Eight distinct contained placements, all containing $(1,1)$; the row $A=(8)$ and $m=(8)$ certify ceiling one. Exercise algebraic equality and radius replay without constructing the Trump packing. |
| Deliberately uncovered LP column or a zero pivot cap on the nonoptimal toy start | Refuse the missing finite-bound guard; preserve the typed pivot-budget refusal without a success verdict. |

Proposed disjoint implementation paths are
`packing/src/sqpack/full_size_density/support_ceiling.py` (with an empty package
`__init__.py`), `packing/devtools/check_full_size_density_support_ceiling.py`, and
`packing/tests/test_full_size_density_support_ceiling.py`. Retained control and later
screen outputs belong under
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-254-support-ceiling/`.
The coordinator owns preregistration, hypothesis readiness, sessions, shared views, and
consequential acceptance.
The checker author does not accept their own result.

After commissioning, the focused command from `packing/` is
`uv run --frozen --all-extras --group dev python -m pytest -q tests/test_full_size_density_support_ceiling.py`
under Python 3.14. Record wall time, CPU time, test and refusal counts, and all missing
measurements. No dependency change, arrangement implementation, target sampling, or
broader gate is part of that control-only run.

Readiness requires passing controls, independent review of the geometric and LP
inequalities, a source-bound instrument, and a coordinator-approved command deadline.
A proposed first target allowance is one process, at most two solves and 128 pivots,
within a 60-second process wall cap.
Its viability is unmeasured; controls must inform the cost decision before the target
cap and instrument are frozen.
H-099 remains `instrument_ready: false` until that decision.
If the control-only build or review exceeds its commission, retain the gap and cost; do
not substitute an arrangement build.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
