---
title: Full-Square Partner Coupling for the n17 Witness
date: 2026-10-07
status: prospective-proof-contract
---
# Full-Square Partner Coupling for the n17 Witness

This is a proposed fallback to the
[complete partner-core test](research-2026-10-07-n17-complete-partner-coupling.md).
It tests the full squares directly on each accepted partner row’s product domain.
Its purpose is to distinguish loss from a common interior core from loss already present
in the independent centre-and-angle domains.
It does not change the first test’s criterion, authorize another target, or assert a
result.

The derivation is the sole Astra agent’s hand proof.
It has not received an independent mathematical review or an end-to-end machine proof.
A future exact checker would verify the finite polynomial and margin obligations below;
the geometric composition would remain an explicit mathematical premise.

## Premises and Complete Domains

Keep the accepted original parent, root, numeric container, owner map and exp288 witness
from the preceding contract.
Exp284’s unaccepted child remains excluded.
Use all 992 foreign closed rows, every residual piece, all seams and the same
independently clipped necessary wall domains.
For each row, let $P_k$ be the convex hull of those clipped pieces.
Retain the complete seventeen-owner endpoint calibration and the actual-piece membership
control for the fixed witness.

The fixed owner-0 chart is $a=53/128$, with

$$
c_0=\frac{13575}{19193},\qquad
s_0=\frac{13568}{19193},\qquad
u_0=(c_0,s_0),\quad v_0=(-s_0,c_0).
$$

Its centre is the exact accepted $x_*$. For a partner centre $y\in P_k$, write
$d=y-x_*=(d_x,d_y)$. All these centres and $x_*$ lie in $[0,U]^2$, where $U=1169/250$.
This bound is checked from the clipped domains and the accepted fixed pose; it is used
in the regional lift.

For the partner chart $t\in[0,1]$, put $\theta(t)=2\arctan t$. The two unit squares have
overlapping interiors exactly when each of the four separating-axis projection
inequalities is strict:

$$
|n\cdot d|<H(t),\qquad
n\in\{u_0,v_0,u(t),v(t)\},
$$

where

$$
H(t)=\frac{1+\cos(\theta(t)-\theta(a))+
|\sin(\theta(t)-\theta(a))|}{2}.
$$

The cosine is nonnegative on this chart range.
Equality in a separating-axis inequality can permit boundary contact, so equality must
not certify an interior collision.

## Eight Exact Quadratics

Split every closed row at $a$, retaining both closed subintervals when the split is
interior. On a subinterval below $a$ use $\sigma=-1$; above $a$ use $\sigma=1$. At the
shared endpoint both formulas agree.
Define

$$
A_\sigma(t)=2(1+t^2)H(t)=A_0+A_1t+A_2t^2,
$$

with

$$
A_0=1+c_0-\sigma s_0,\qquad
A_1=2s_0+2\sigma c_0,\qquad
A_2=1-c_0+\sigma s_0.
$$

For each vertex $y$ of $P_k$ and each sign $\eta\in\{-1,1\}$, check the following
polynomials are strictly positive throughout the closed subinterval:

| Axis | Coefficients of $Q(t)=q_0+q_1t+q_2t^2$ |
| --- | --- |
| Fixed $n=u_0$ or $v_0$, with $z=n\cdot d$ | $(A_0-2\eta z,\ A_1,\ A_2-2\eta z)$ |
| Partner $u(t)$ | $(A_0-2\eta d_x,\ A_1-4\eta d_y,\ A_2+2\eta d_x)$ |
| Partner $v(t)$ | $(A_0-2\eta d_y,\ A_1+4\eta d_x,\ A_2+2\eta d_y)$ |

Each polynomial is exactly $2(1+t^2)(H(t)-\eta n\cdot d)$. No interval division or
sampled angle is needed.
Its minimum is attained at an endpoint or, when $q_2>0$, at the stationary point
$-q_1/(2q_2)$ if that point lies inside the interval.
Retain the exact minimum and its rational minimizer.
Use the least minimizer to resolve a tie deterministically.

For every fixed $t$, each polynomial is affine in $y$. Checking every vertex therefore
checks all of $P_k$. Checking every closed angular subinterval covers the row, including
its seams. Let $M_j$ be the least checked value over all eight signed axes, all vertices
and all live rows of partner $j$.

If $M_j>0$, the fixed owner square overlaps every represented pose of that partner.
One such partner suffices to exclude the fixed witness.
A positive result uses **all rows of that same partner**. A row-specific collision
cannot be combined with a different row-specific partner choice to bypass this universal
quantifier.

For a complete negative result, retain an exact nonpositive minimum for each partner.
Its row, vertex, angular minimizer, axis and sign are a witness that this product-domain
implication fails.
The vertex may fail the exact wall condition at that particular angle:
the row domain only used a necessary wall box.
This is evidence about the represented relaxation, not a physical two-square pose or a
seventeen-square packing.

The frozen secondary diagnostic checks the retained nonpositive witness against the
exact numeric wall box at its own minimizing angle.
It records the four signed wall margins and their joint nonnegativity without changing
$M_j$, the selected partner or the primary verdict.
A wall failure identifies one source of centre-angle over-cover.
A wall pass still proves no joint packing.

## A Positive Margin Gives a Closed Region

Suppose a complete partner has $M=M_j>0$. Since $0\le t\le1$, all its normalized
separating-axis gaps at the fixed owner pose are at least $M/4$. Set

$$
L=4U+4=\frac{2838}{125},\qquad
h=\min\left\{\frac1{128},\frac{M}{8L}\right\}>0.
$$

Consider every owner centre $x'\in x_*+[-h,h]^2$ and every owner chart $a'\in[a-h,a+h]$.
Its physical angle changes by at most $2h$, because $\theta'(a)=2/(1+a^2)\le2$.

The support threshold $(1+|\cos\Delta|+|\sin\Delta|)/2$ changes by at most the physical
angular change, hence by at most $2h$. For an owner axis, changing its direction changes
its projection of the old displacement by at most $2h\,\|y-x_*\|_1\le4Uh$. Moving the
centre changes any unit-axis projection by at most $2h$. Thus any owner-axis gap
decreases by at most $(4U+4)h$. For a partner axis, the direction stays fixed; the gap
decreases by at most $4h\le Lh$.

Every gap in the whole closed box is therefore at least

$$
\frac{M}{4}-Lh\ge\frac{M}{8}>0.
$$

The same partner overlaps the owner square for every point of this position and angle
box and every represented partner pose.
Intersecting the box with the accepted parent preserves that exclusion.
The accepted exp288 pose lies inside the box and satisfies the reduced point model, so
the comparison has a retained nonempty control.

This argument proves a declared box with positive coordinate widths.
It does not claim every parameter point in that box is a physically contained square;
the relevant excluded domain is its intersection with the accepted parent and the exact
container constraints.
In particular, the matched square touches a wall.
No open ball of feasible packing poses is being assumed.

All resulting angle intervals lie in $[13/32,27/64]$. Analytic label 1 remains axis
aligned throughout the accepted endpoint slider family, with chart alternatives 0 and 1,
so this region is disjoint from that family.
Keep the same exact role, endpoint-retention and family-disjointness controls as the
first coupling test.

## Prospective Finite Contract

If selected after the first coupling result, register a new hypothesis and experiment.
Freeze these rules before inspecting the new polynomial signs:

1. Reconstruct the complete accepted row domains and endpoint controls with the same
   source and custody discipline.
   An all-empty owner refuses the known-endpoint control.
2. Check all sixteen partners in owner order and retain exact $M_j$ witnesses.
   Choose the least owner with $M_j>0$. Do not alter the angle, point or row domains
   after a miss.
3. Compute the exact $h$ above, check $h>0$, the angular guard and the bound
   $M/4-Lh\ge M/8$. Fresh reconstruction must reproduce the selected owner, every
   minimum and the region exactly.
4. Primary success requires that positive-width regional certificate.
   All $M_j\le0$ is a completed miss for this product-domain recipe.
   Resource stops are incomplete; failed input or endpoint controls are refusals.

Use the existing 4,096-bit normalized geometric budget and the separately declared
endpoint budgets. The proposed additional ceiling is 8,000,000 quadratic minimizations,
including all vertex/sign/axis/subinterval checks.
Use one worker, 120 seconds for construction and 120 for fresh reconstruction, with
owned-group cleanup and a sampled 4 GiB RSS guard per live process.
These are proposed bounded allocations, not measured runtime estimates.
Output is limited to 64 MiB; retain per-row minima and their witnesses rather than every
redundant polynomial evaluation.
A future instrument must expose the actual check counts and refuse to call a partial
scan complete.

Target-free controls must cover the split at $a$, both formulas at equality, all
projection signs, both body axes, constant and linear polynomials, endpoint minima,
interior stationary minima, a zero margin and a strictly positive margin.
Compare the formulas with independently constructed exact square projections at rational
synthetic angles.
Include an interior angular violation missed by endpoint-only sampling,
product-domain over-cover, degenerate centre domains, the exact regional bound and
endpoint-family disjointness.
Fresh verification remains producer-free and inherits the accepted parent rather than
replaying its geometry.

A positive result following a complete common-core **fixed-point** miss on the same
domains would identify the core approximation as a sufficient cause for that
discrepancy. A regional-only miss does not establish that diagnosis.
A second complete fixed-point miss would direct the next derivation toward centre-angle
correlation or conditional multi-owner constraints.
Neither outcome establishes dominance over the existing standing checker, which already
uses partner pose covers.

## Joint-Domain Successor After a Second Miss

The next proposed discriminator conditions all partner domains on one small owner-0
guard, then tests whether two owners acquire a common strictly owned point.
Independent escape poses for the fixed square do not answer this question: those poses
need not be mutually compatible with the other owners.
This is a different finite implication, not another unchanged propagation run.
It remains unregistered and has no target measurements.

For a possible first test, fix $h=1/512$ before inspecting its geometry and use the
closed guard

$$
G=\{x_0\in x_*+[-h,h]^2,\quad \tau_0\in[a-h,a+h]\}.
$$

This proposed allocation and width require a separate root registration.
Every physical packing under the accepted parent and $G$ is the quantified population.
The guard is disjoint from the accepted endpoint family, whose owner-0 chart is 0 or 1.
Check endpoint retention on the original parent, not on these conditional domains: the
endpoint is deliberately outside $G$.

First construct a closed positive-area polygon $Q_0$ whose points lie strictly inside
owner 0 for every pose in $G$. For each coefficient-rectangle corner on the guard angle
interval, each body axis $n$, and both signs, impose

$$
\eta n\cdot q\le\frac12-2^{-20}
   +\min_{x\in x_*+[-h,h]^2}\eta n\cdot x.
$$

Clip these sixteen planes from $[0,U]^2$. Independently check every resulting vertex
relative to all four centre-box corners with the exact closed-arc strict-ownership test.
Convexity in the centre and the candidate point extends the check to the whole polygon
and box. The matched fixed square contains $Q_0$ strictly, but that control alone says
nothing about seventeen-square feasibility.

There is an input-independent positive-area control.
Put $r=(1/2-2^{-20})/2-h=520191/2097152>0$. The box $x_*+[-r,r]^2$ satisfies every
construction plane, since coefficient absolute values are at most 1 and
$2(r+h)=1/2-2^{-20}$. The accepted contained square gives $x_{*,i}\in[1/2,U-1/2]$, so
this small box lies in $[0,U]^2$. An empty computed $Q_0$ is therefore a calibration
refusal, not a conditional contradiction.

For every foreign owner $j$ and every original row $k$, retain its strict zero-centred
core $D_{jk}$. Define the forbidden centre polygon

$$
F_{jk}=Q_0-D_{jk}.
$$

If $y\in F_{jk}$, there are $q\in Q_0$ and $d\in D_{jk}$ with $y=q-d$, hence $q=y+d$.
That point is interior to both squares.
Such a centre is impossible under $G$ for every angle in the row.

Write the exact closed facets of $F_{jk}$ as $n_r\cdot y\le b_r$. Replace each
individually wall-clipped residual piece $P$ by the closed union

$$
\bigcup_r\bigl(P\cap\{n_r\cdot y\ge b_r\}\bigr).
$$

This union contains $P\setminus F_{jk}$; it also retains the forbidden boundary.
That extra boundary is a safe over-cover.
Preserve all nonempty pieces, including points, segments and duplicates at seams.
An implementation may deduplicate identical pieces, but may not discard a disjunct
because a different one is nonempty.
Newly empty rows carry their exact subtraction witness; all rows of an owner empty is
now a valid **conditional** contradiction, unlike the unconditional endpoint-calibration
refusal in the first test.

If no owner is empty, let $P'_{jk}$ be the convex hull of all surviving pieces in row
$k$. Recover a common strictly owned polygon $K_j$ from every live row of owner $j$. For
each row’s coefficient-rectangle corner, body axis and sign, impose

$$
\eta n\cdot q\le\frac12-2^{-20}
   +\min_{y\in P'_{jk}}\eta n\cdot y.
$$

Start from $[0,U]^2$, and intersect across all rows of that owner.
Every vertex of a nonempty $K_j$ must also pass a fresh exact closed-arc
strict-ownership check relative to every vertex of every $P'_{jk}$. Linear dependence on
the centre and candidate point then proves that the entire convex $K_j$ is inside every
represented square of owner $j$. Empty $K_j$ means this construction found no common
polygon; it does not mean the owner has no physical pose.
Points and segments are valid nonempty owned sets after the strict check.

Set $K_0=Q_0$. An exact nonempty intersection $K_i\cap K_j$ for distinct owners proves
that every physical packing under the guard has an interior collision.
Boundary contact between these **owned sets** is enough: all their points have already
been proved interior to the respective physical squares.
The implication therefore differs from treating touching physical square boundaries as a
collision.

The primary success of this proposed single round would be either a complete owner cover
becoming empty or an exact shared strictly owned point.
A complete nonclosed result is a miss for the frozen construction, with guard
feasibility unresolved.
Retain the per-owner row/piece counts and recovered owned sets as secondary diagnostics.
Neither numerical shrinkage nor loss of the matched single-square pose in another
owner’s domain is an exclusion criterion.

The first implementation should reuse the accepted original parent and the existing
exact clipping, difference facets and closed-arc checks.
It should not use exp284, introduce a child producer, change the guard after a miss, or
replay a long unchanged sixteen-owner round.
A source-only review must freeze the subtraction-growth, vertex-pair, rational-bit and
wall ceilings before any target.
If those ceilings are reached, the result is incomplete.
The one-round derivation is finite but its actual cost and effectiveness are unmeasured.

A complete miss also supplies a monotonic stopping rule for this same construction.
Let $G_1=B_1\times J_1\subseteq G_2=B_2\times J_2$ as full product guards, with the same
parent, strict margin and foreign row cores.
The coefficient rectangles and centre domains enlarge with the guard, so
$Q_0(G_2)\subseteq Q_0(G_1)$. Thus each forbidden difference shrinks.
The declared closed outside-facet union is exactly $P\setminus\operatorname{int}F$, so
every retained conditional centre domain enlarges.
Its convex hull enlarges as well.
The recovered common owned sets consequently satisfy $K_j(G_2)\subseteq K_j(G_1)$,
including owner 0. If $G_1$ leaves every owner nonempty and every owned-set pair
disjoint, $G_2$ cannot create an empty owner or a shared owned point.
Do not spend another target widening that same one-round recipe after a complete miss.
This argument requires inclusion of the full construction product guards, not merely
inclusion of their physically feasible subsets.
It does not apply to resource stops, sharper ownership constructions, further coupled
rounds or another proof method.
This is a prospective hand lemma with the same assurance limits as the other geometric
compositions in this document.

The coordinator approved the following source-only resource contract before any guarded
target.
Use the same five byte-bound input roles and the amended original input limits of
1,024 pieces per row and 1,048,576 construction vertices.
Use one worker, 180 seconds for construction and 180 for fresh reconstruction, with a
360-second combined ceiling, owned-group cleanup and a sampled 4 GiB RSS guard per live
process. The normalized geometry limit stays 4,096 bits; endpoint inputs and arithmetic
retain their separate 16,384/32,768-bit limits.

| Guarded construction resource | Ceiling |
| --- | --- |
| Conditional pieces per row; global retained pieces | 8,192; 131,072 |
| Cumulative generated conditional clip-output vertices | 2,097,152 |
| Aggregate conditional row domain | 1,024 vertices |
| $Q_0$ and each strict row core | 32 vertices |
| Forbidden difference | 64 facets; 131,072 total raw vertex-pair products |
| Recovered $K_j$; pair-intersection output | 2,048; 4,096 vertices |
| Outside-fast-path support products | 16,000,000 |
| Recovery support products | 16,000,000, counted separately |
| Fresh strict-ownership verification | 2,000,000 vertex pairs; 8,000,000 quadratic minima |
| Output | 64 MiB |

The generated conditional clip-output counter includes owner-0 restricted-angle
necessary-wall clips, the subsequent owner-0 centre-box clips and foreign
outside-subtraction clips.
It excludes unconditional original-row wall preflight and the halfplane intermediates
used to construct $Q_0$ and recover $K_j$; those retain their separately declared input,
polygon, support-work and external wall ceilings.
This distinction fixes the pretarget resource scope and does not change any geometric
predicate.

A recovered $K_j$ has at most $64\cdot16+4=1028$ construction halfplanes; two recovered
polygons therefore have at most 2,056 intersection vertices.
These combinatorial bounds motivated the representation ceilings without inspecting a
target. They do not bound the total arithmetic work below its separate ceilings.

An exact fast path may retain $P$ once if one forbidden facet has
$\min_{y\in P}n\cdot y\ge b$: that outside-facet disjunct already equals $P$. Exact
duplicate output polygons may share storage if every original piece and facet retains
its alias. Neither shortcut may lose a disjunct or remove the forbidden boundary from
this declared closed-complement construction.
An empty recovered $K_j$ may stop its later clipping by monotonicity, with an explicit
empty-prefix reason and complete accounting of the conditional row cover.
It never licenses an empty-owner verdict.

## Exp292: Complete Full-Square Miss

Construction and fresh reconstruction both returned `criterion_missed` on the complete
original parent. They checked all 1,056 rows, including 992 foreign rows, with 34,128
exact quadratic minima and all seventeen endpoint controls.
Every partner minimum is negative; no partner or regional lift was selected.
The retained certificate and replay are under
`packing/campaign/series/series-000-smoke-and-calibration/results/exp-292-full-square-partner-coupling/`.
The
[phase record](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-292-full-square-partner-coupling/phase-execution.json)
records 52.263675 seconds for construction and 53.990876 seconds for fresh checking.
The supervisor recorded 106.652810 seconds overall, normal exit and successful cleanup.

Fifteen of the sixteen retained negative witnesses pass the exact numeric walls at their
minimizing angles. Owner 4 is the exception: its row-49 witness at $t=49/64$ has
bottom-wall margin $-75040/10713553$. This secondary failure identifies one centre-angle
over-cover witness; it does not establish that repairing it would make that partner’s
complete minimum positive.

For the fifteen wall-valid witnesses, merely subdividing the old angular rows and
recomputing their necessary wall boxes cannot remove the obstruction.
A vertex of the finite row hull belongs to an original clipped piece.
Its angle belongs to at least one closed child row, and exact containment at that angle
implies containment in the child’s necessary wall box.
The same signed separating-axis witness therefore survives.
This stopping argument assumes the original residual pieces and constraints are kept;
stronger cross-owner constraints can change the domains.

The outcome rules out common-core erosion as the sole explanation for failure of the
universal single-partner test on these domains.
The independent escape poses need not coexist.
The next selected mathematical question is guard-conditioned multi-owner ownership, with
the original parent and endpoint premises retained.

## Point-First Guard Discriminator

The monotonic guard argument also permits the degenerate product guard
$G_0=\{x_*\}\times\{a\}$. It gives

$$
Q_0(G_h)\subseteq Q_0(G_0),\qquad
P'_{jk}(G_0)\subseteq P'_{jk}(G_h),\qquad
K_j(G_h)\subseteq K_j(G_0)
$$

for every centred positive-width guard $G_h$ in the same construction.
Consequently, a complete point-guard miss rules out both conditional closure mechanisms
for all those larger guards.
Point closure alone proves only a point exclusion; the primary regional criterion still
requires the declared $h=1/512$ context.

The prospective paired implementation reconstructs the original rows and endpoint
controls once, evaluates $h=0$, and starts $h=1/512$ only after point closure.
Fresh reconstruction follows the same deterministic branch.
The proposed allocation remains 180 seconds per invocation and 360 seconds combined.
Support, generated-clip, Minkowski and strict-verification work counters are cumulative
across both contexts.
The 131,072 retained-piece ceiling is per context; row and polygon ceilings are per
object, and the combined output remains limited to 64 MiB. A resource stop in either
context is incomplete.
A complete point miss records the regional context as unstarted with the monotonic
reason. These are prospective semantics requiring source review and registration before
use.

## Prospective Full-Square Collision Envelopes

A further conditional-pruning alternative can retain the full squares without computing
a global minimum for each candidate centre.
On a closed subarc $[l,r]$, write a signed SAT polynomial as $Q(y,t)$, affine in the
partner centre $y$. For a proposed owner half-width $h$, define

$$
P(y,t)=Q(y,t)-2(1+t^2)Lh.
$$

The preceding regional bound shows that $P(y,t)>0$ for all eight signed axes implies
interior collision throughout that owner guard.
Put $d=r-l$. The three quadratic Bernstein coefficients on this subarc are

$$
b_0(y)=P(y,l),\qquad
b_1(y)=P(y,l)+\frac d2\,\partial_tP(y,l),\qquad
b_2(y)=P(y,r).
$$

Indeed, for $0\le u\le1$,

$$
P(y,l+du)=b_0(y)(1-u)^2+2b_1(y)u(1-u)+b_2(y)u^2.
$$

Each coefficient is affine in $y$. Requiring every coefficient to be at least a
predeclared rational $\kappa>0$ therefore gives exact linear centre constraints and
ensures a strict collision on the whole closed arc.
At $l=r$ the formula remains valid without division.
Retain both subarcs when a row crosses $a$ and require every signed axis on both.

Intersecting these constraints with $[0,U]^2$ yields a convex forbidden-centre set.
An original residual piece whose every vertex satisfies all constraints can be removed
whole, including a degenerate piece.
This first variant introduces no subtraction pieces.
A stronger variant could combine this set with the existing forbidden core difference,
but would need a separate growth and coverage contract.
No containment or performance dominance over that existing construction is asserted.

This is an unselected hand derivation.
The margin, resource ceilings, controls and acceptance rule must be frozen before
evaluating actual coefficients or removals.
Its immediate purpose would be to test whether full-square collision implications
strengthen conditional pruning; it supplies no present exclusion or global proof.

## Prospective Closed Separation Branches

The same polynomial identity gives a complete branch cover when merging alternative
escape directions loses useful information.
Fix one partner. In any physical packing under the owner guard, that pair has disjoint
interiors. The robust collision argument therefore implies $P(y,t)\le0$ for at least one
signed axis. On a closed subarc containing the actual angle, the Bernstein identity
implies $b_i(y)\le0$ for at least one $i\in\{0,1,2\}$.

Group by the eight signed axes and three coefficient indices.
These 24 branches form a closed cover of every possible noncolliding pose of the chosen
partner. Each branch retains every original row, both subarcs where required, and every
centre piece clipped by that branch’s coefficient halfplane.
The coefficients depend on the row and subarc; the common branch index does not replace
them by one global plane.
Boundary equality and angular seams remain in the cover.

Within a branch, recover a common owned set for the restricted partner and test it
against the other owners’ already checked common owned sets.
This shallow variant changes one partner’s domain and avoids reconditioning every
foreign piece in every branch.
Excluding the guard requires all 24 branches to close, by exact empty-cover or
shared-interior-point evidence.
A closure in one branch excludes only that branch.
Further propagation would be a separately declared construction.

The existing SAT witnesses give a useful limitation.
An exact-wall-valid pairwise escape cannot lie in $Q_0-D$, because that membership would
force an interior collision.
It survives the point-conditioned cover and belongs to at least one of the 24 branches.
The recovered owned set in that branch cannot meet $Q_0$. Thus if every other fixed
owned set is empty, this shallow branch test against $Q_0$ alone cannot close all
branches for that partner.
The actual recovered sets should decide whether this route contains new information
before allocating a target.

## Prospective Conditional Hitting-Point Certificate

A finite point cover can preserve alternatives without requiring one common owned point
for each square. Fix sixteen distinct rational points $Z$, initially proposed as

$$
Z=\left\{\left(o+\frac{kV}{5},\ o+\frac{lV}{5}\right):
k,l\in\{1,2,3,4\}\right\}.
$$

For every owner and every surviving closed row under a declared guard, prove coverage of
its centre domain by

$$
\bigcup_{z\in Z}(z-D_{jk}),
$$

where $D_{jk}$ is the checked strict body core for that row.
Membership $y=z-d$ gives $z=y+d$ strictly inside the physical square.
Every square consequently contains at least one point of $Z$. Interior-disjoint squares
cannot share such a point, so seventeen squares cannot all satisfy this condition with
only sixteen points.
The selected point may vary with the square’s pose; an empty common-owned intersection
does not by itself prevent this certificate.

Coverage must include every closed row and piece, including points, segments and seams.
Using an aggregate row hull is a permitted stronger sufficient obligation, but its
uncovered points may arise solely from that over-cover.
Retain the exact choice of domain in the contract.
All points, core margins and coverage rules must be frozen before inspecting a new
target. The accepted endpoint forbids this collective certificate on the unconditioned
parent and supplies a required negative control.

More generally, suppose owner $j$ is guaranteed to contain a point from a specified
subset $Z_j$. A set of owners $A$ is impossible whenever $|\bigcup_{j\in A}Z_j|<|A|$.
This is the finite Hall obstruction; it includes the two-owners/one-shared-point
argument as a special case.
Any proposed $Z_j$ still needs its complete geometric coverage proof.

A fully accepted point-conditioned receipt could supply explicit inherited domains for a
cheap first coverage discriminator.
With the point set and row cores fixed, a checked uncovered point persists when the
centred guard is enlarged, because the conditional domains enlarge.
This blocks only that sufficient row-core coverage recipe; it does not refute actual
containment by the rotating square or a sharper construction.
Conversely, point coverage proves only a point exclusion.
A regional claim requires the region’s own checked conditional domains;
point-conditioned domains cannot be transported to positive width.

This is a concrete conditional-capacity option within
[X-048’s R2/R3 portfolio](../../../packing/campaign/explorations/X-048-n17-optimality-after-n11.md),
not a new assertion that the broader route was absent.
Neither this option nor the 24-branch cover is selected or measured here.
Their next use requires a bounded resource contract, controls and preregistration
informed by the actual paired-guard outcome.

## Accepted Paired-Guard Result: exp293

The
[retained outcome](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-293-guard-conditioned-ownership/mechanical-summary.json)
records a completed `criterion_missed`, with matching fresh reconstruction.
All 1,056 original rows and 992 foreign conditional rows were checked.
Every foreign conditional row remains nonempty.
The original seventeen endpoint enclosures are retained, and the tested guard is
disjoint from that endpoint family.

The recovered owned sets have the following vertex counts:

| Owners | Vertices |
| --- | --- |
| 0 | 4 |
| 1, 2 | 21 each |
| 3 | 13 |
| 4 | 29 |
| 6 | 60 |
| 20 | 34 |
| 5, 7, 8, 9, 11, 12, 13, 14, 18, 21 | 0 each |

No pair of these owned sets intersects.
Construction took 75.141 seconds and fresh reconstruction 76.260 seconds; the outer run
took 151.778 seconds and completed normally.
The regional context was unstarted under the point-miss stopping rule.
The nesting lemma therefore blocks larger centered guards for this same one-round
owned-set construction; it does not report a separately measured regional miss.
No packing, global capture or census exclusion follows.

## Selected Two-Child Centre Test

The next discriminator tests whether one empty owned intersection results from merging
two spatial alternatives.
It uses exp293’s accepted point-conditioned row hulls and owned sets as explicit
premises. It does not use exp284’s unaccepted child.
The rule below is frozen before evaluating the selector or either child on the actual
geometry.

For each of the ten foreign owners with empty accepted owned set, form the bounding box
of the union of its nonempty conditional row hulls.
For each coordinate axis, split at the exact midpoint of that bounding-box interval.
Intersect every closed row hull with each of the two closed halfplanes.
Equality belongs to both children, and angular intervals and their seams are preserved.
Compute each child’s aggregate bounding box and its squared diagonal; give an empty
child score zero. Select the pair minimizing the larger child score, with ties resolved
by owner number and then $x$ before $y$. This selector uses geometry alone, without
testing closure. Keep the selected owner, axis and cut value fixed in both phases below.

Every physical packing in the parent guard belongs to at least one child.
If all rows of the selected owner are empty in a child, that child is excluded.
Otherwise reconstruct its common owned set with the preceding sixteen corner
inequalities, the same $2^{-20}$ strict margin, and fresh exact closed-arc checks
against every surviving child-row vertex.
All other owners retain the checked owned sets of that guard context.
A nonempty exact intersection between the child’s owned set and any other owner’s owned
set excludes the child.
Points, segments and touching owned hulls count because their points are strictly inside
the physical squares.
Choose the least other owner supplying such an intersection.
An empty recovered owned set gives no exclusion.
Both children must close.

The selector has a simple geometric motivation: if a child confines the centre to a
rectangle with side lengths $w,h$ and $w^2+h^2<1$, its midpoint is strictly inside every
represented unit square, regardless of angle.
Every such square contains its open radius-$1/2$ inscribed disk, and the greatest
distance from that midpoint to a centre in the rectangle is $\sqrt{w^2+h^2}/2<1/2$. This
exact squared test is a diagnostic; it does not replace the instrument’s declared
strict-margin ownership check.

### Point First, Then the Same Split on a Region

First reconstruct both point children from the accepted exp293 hulls.
If either child remains open, record a complete miss and skip the regional phase.
For the fixed split, the earlier nesting argument still applies: larger guards enlarge
each halfplane-restricted centre domain and shrink every recovered owned set.
The same child proof cannot become successful merely by enlarging the guard.
This stopping rule does not license changing the selected owner or cut for the region.

If both point children close, the point exclusion is a secondary result.
Freshly reconstruct the original parent domains, endpoint control and conditional
context at half-width $1/512$, then apply the identical selected split.
Do not transport the point-conditioned domains to positive width.
The unchanged pre-split regional context must remain nonclosed by the accepted exp293
point-miss nesting lemma; an unexpected closure there is a calibration refusal.
The primary success requires both regional children to close.
A completed regional miss retains only the point result.
A resource stop remains incomplete, with any unfinished candidates distinguished from a
freshly verified result.

### Premises, Controls and Bounds

The new descriptor binds three path-and-byte roles: the small exp293 descriptor, its
accepted certificate and its fresh receipt.
Require matching semantic payloads, fresh verification, the completed point miss, the
full row roster, endpoint controls and canonical parent identities.
The exp293 descriptor retains the preceding five-role input chain.
Each new phase may read accepted exp293 geometry as a premise; it must not claim to
replay that geometry or the original parent.
The fresh checker independently repeats the selector and all new child arithmetic.
Any regional phase additionally reconstructs its own conditional geometry from the
original parent through the existing bounded helpers.

Use one worker, 180 seconds for construction and 180 for fresh reconstruction, with the
existing 360-second outer termination and 370-second kill limits.
The memory guard samples current RSS with a 4 GiB ceiling per live owned process.
The descriptor is limited to 10 MiB; each accepted exp293 receipt and the combined new
output are limited to 64 MiB. Original geometry and endpoint input limits remain
unchanged.

For the new selector and children, count at most 2,097,152 generated clip vertices
cumulatively, 1,024 vertices per child row domain, 2,048 per recovered owned set and
4,096 per intersection.
Bound recovery support products by sixteen million, strict vertex pairs by two million
and their quadratic checks by eight million, and intersection vertex pairs by two
million.
The original conditional reconstruction retains its separately named frozen work
counters.
Geometry remains limited to 4,096-bit rational inputs and results; these bounds
do not claim to cap unreduced internal integer products.

Controls must cover closed split seams and singleton rows, an empty child, one closed
child without overall success, both children closing, deterministic selector ties,
strict ownership and touching owned hulls, the fixed-cut nesting rule, inherited premise
tampering, known-endpoint retention in the original parent, incomplete-output scope and
independent two-process reconstruction.
The new branch composition and nesting argument remain sole-Astra hand derivations, with
no independent mathematical review or end-to-end formal proof claimed.

## Actual Two-Child Result and Selected Collective Row Test

The completed exp-295 construction and fresh reconstruction agree on a miss of the
frozen two-child criterion; see its
[mechanical summary](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-295-two-center-children/mechanical-summary.json).
The deterministic selector chose owner 18, the $x$ coordinate and cut $471/250$. Both
closed children retain all 64 rows, with no empty row.
Their recovered strictly owned hulls have 56 and 105 vertices, respectively, but neither
intersects another owner’s inherited hull.
The worst squared centre-box diagonal is $167129/250000<1$. This explains why both
children recover nonempty ownership; it supplies no contradiction.
The fixed-split nesting argument correctly leaves the regional branch unstarted.
Construction took 11.804 seconds, fresh reconstruction 11.635 seconds and the supervised
pair 23.770 seconds.
This is a completed finite-recipe miss, not a feasible seventeen-square packing.

The selected next discriminator is one **simultaneous whole-row collective coverage
pass** on the accepted exp-293 point context.
It uses all seven nonempty inherited owned hulls, including owner 0, rather than
choosing another centre split.
Exp-295 supplies the route-selection prerequisite; neither of its child geometries is an
input to this pass. The experiment remains prospective until separately registered,
frozen and executed.

For every foreign owner $j$ and closed chart row $k$, let $P_{jk}$ be the accepted
conditional centre hull, and freshly construct the same strict zero-centred square core
$D_{jk}$ over its complete angle interval, with margin $2^{-20}$. For every other owner
$i$ with nonempty inherited $K_i$, form

$$
F_{ijk}=K_i-D_{jk}.
$$

If $y\in F_{ijk}$, some point of $K_i$ lies in $y+D_{jk}$. Both sets lie strictly inside
their physical squares, so this is a collision even when $y$ lies on the boundary of the
closed Minkowski difference.
The proof also applies to point or segment owned hulls; the constructor must preserve
these cases. Therefore

$$
P_{jk}\subseteq\bigcup_{i\ne j}F_{ijk}
$$

certifies that the entire closed row has no physical realization under the point guard.
Union is over different owners.
Every row uses the original accepted owned hulls: no result from an earlier row is fed
back during this pass.

First inspect the vertices of $P_{jk}$ in lexicographic order.
A vertex outside every closed $F_{ijk}$ is an exact witness that this sufficient
coverage test fails, so it can skip the full union calculation.
If every vertex is covered, a full exact union-coverage check is still required: covered
vertices do not rule out holes.
Use the retained sweep for positive-area domains and the exact degenerate routine for
segments and points.
Clipping each forbidden region to the target domain preserves the coverage question.
All 992 foreign rows, closed seams and typed references remain accounted for.
An uncovered row retains its entire previous hull; this pass introduces no fragments.

The primary criterion is a strict decrease, for at least one owner, in the exact length
of the union of its surviving closed angle intervals.
Record both interval unions and their rational length difference.
Shared endpoints remain in whichever surviving adjacent rows contain them.
Emptying one owner’s complete row cover is a secondary point-guard contradiction.
This deliberately narrower test supplies a conditional necessary-domain restriction; it
does not claim a nonzero regional exclusion, capture, a census admission or global
optimality. No lost angular length is a completed miss of this recipe.
Fresh independent reconstruction must agree on the entire new finite payload before any
deletion is accepted.

The frozen planning ceiling is 60 seconds for construction and 60 seconds for fresh
reconstruction, with outer termination at 120 seconds and forced cleanup at 130 seconds.
Use one worker and the existing sampled 4 GiB current-RSS limit per live process.
Inherited geometry admits at most 1,048,576 vertices, 1,024 vertices per row hull and
2,048 per owned hull, with 4,096-bit rational geometry.
Fresh row cores admit 32 vertices; forbidden and clipped hulls admit 4,096 each.
Cache exact interval/owned-hull pairs and charge at most 1,048,576 raw Minkowski vertex
products across cache misses, 2,097,152 generated clipped vertices and 16,000,000
point/facet products.
Before a full sweep, require at most 8,192 boundary edges in that row and charge its
prospective $E(E-1)/2$ edge pairs against a cumulative 8,000,000 ceiling.
The output limit is 64 MiB. These controls do not bound unreduced internal homogeneous
integer products separately; the cooperative deadline and owned-process supervisor
remain necessary.
No new ownership recovery, sequential feedback, second pass or regional
branch belongs to this first test.

Required controls include coverage by a union when no single region suffices, a hole
despite covered target vertices, exact point/segment/touch cases, the outside-vertex
shortcut, self-owner exclusion, closed-seam union lengths, immutable inherited owned
hulls, missing-row and premise tampering, resource refusals and fresh-process parity.
The collision composition is a sole-Astra hand argument with finite computational
verification planned, not independent mathematical review or formal proof.

### Actual Collective Restriction and Prospective Regional Lift

Exp-296 meets its frozen primary criterion; its
[mechanical summary](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-296-collective-row-coverage/mechanical-summary.json)
records independent fresh reconstruction with an identical finite payload.
All 992 foreign closed rows are accounted for.
Owner 18, which is label 11, loses rows 19–23 and 33–52: twenty-five complete rows.
Its surviving half-angle-parameter domain is

$$
[0,19/64]\ \cup\ [3/8,33/64]\ \cup\ [53/64,1],
$$

with exact lost parameter length $25/64$. This is not a measurement of physical angle in
radians or a uniform-angle fraction.
Surviving adjacent rows retain the shared endpoints.
Every other owner’s interval union is unchanged, and no complete owner cover becomes
empty. The result proves a necessary-domain restriction under the fixed owner-0 pose; it
proves neither that point guard impossible nor a regional, parent or census exclusion.
The original seventeen-square endpoint-retention and family-disjointness premises remain
inherited and unchanged.
Construction took 13.699 seconds, fresh reconstruction 14.177 seconds and the supervised
pair 28.142 seconds.
There were 38 full sweeps and 954 exact outside-vertex shortcuts.

The next narrow proof block should attempt an explicit regional lift of these same
twenty-five row exclusions before unrestricted contact-atlas enumeration.
There is a useful existence argument, but it supplies no numerical radius.
For each excluded row, take the set of full physical packings satisfying the original
bounded parent and numerical container, with that square’s angle in the original closed
row chart interval and its centre in the original residual-piece union.
This physical set uses the original row conditions, not the point-conditioned hull.
Containment, closed row membership and square nonoverlap are closed conditions; the
centre and angle domains are compact.
The set and its projection onto owner 0’s centre/angle coordinates are therefore
compact. At the fixed pose $p^\ast$, necessary conditioning places every such physical
realization inside the checked point-conditioned domain.
The accepted row exclusion therefore says $p^\ast$ is outside the original physical
set’s projection. Its distance from a nonempty compact projection is strictly positive;
an empty projection imposes no radius restriction.
Taking the minimum over the finite twenty-five rows gives some positive neighborhood in
which all their physical realizations remain impossible.
This hand argument concerns row exclusions, not exclusion of every remaining packing.

A finite consumer must supply the missing quantitative join.
For a prospectively declared $G_h$, reconstruct all 992 conditional foreign domains and
their common owned sets from the original accepted parent, then verify coverage of the
same twenty-five owner-18 rows using those regional sets.
The point-conditioned domains and owned sets cannot simply be transported.
Their strict body-interior margins alone do not bound how the conditional domains change
with the owner-0 pose; an alternative analytic consumer would need explicit
domain-sensitivity and support-error bounds as well as the ownership margins.
Retain the original full-root seventeen-square endpoint control and independently check
that the declared regional guard is disjoint from the endpoint family.

A reasonable next allocation is a 1–2 hour source/review block followed by one
registered fixed-radius construction and fresh verification, reusing the existing
regional context builder.
The previously declared $h=1/512$ is a concrete candidate, not a guaranteed radius.
Primary success would require a declared positive-width region and all twenty-five
specific row exclusions, with complete regional conditioning and fresh agreement.
A complete miss rejects that fixed-radius recipe; it does not contradict the compactness
argument. Do not choose a smaller radius from observed coverage margins without a new
prospective contract.
No regional calculation, new ownership recovery or further propagation was performed in
exp-296.

## Prospective Global Contact Normalization

This hand lemma gives a precise existence statement for X-048’s structural-normal-form
route. It is a sole-Astra derivation, without independent mathematical review or an
end-to-end formal proof.
No contact-system enumeration or performance improvement has been established.

Suppose seventeen independently rotated unit squares have disjoint interiors in a
container of side $L_0\le S^\ast<V$. Fix those orientations and the square labels, but
allow every centre and the side to vary.
There exists a packing with the same orientations and side $\ell\le L_0$ such that:

1. Its 34 centre coordinates and side satisfy at least 35 linearly independent active
   wall-containment or physical pair-contact equations.
2. Every connected component of its physical contact graph touches at least one
   horizontal and one vertical wall of its actual container.
3. Some component touches an opposite-wall pair and a wall in the other direction.
   A $D_4$ transformation can place that component against the left, right and bottom
   walls.

The conclusion concerns an existing normalized representative.
It does not assert these properties of every feasible packing.
In particular, a hypothetical packing below $S^\ast$ would have such a representative
also below $S^\ast$.

### Compact Union and Lexicographic Choice

For a fixed unit-square orientation, let $h_i(n)$ denote its support function about its
centre. Wall containment consists of the linear inequalities

$$
h_i(e_x)\le x_i\le L-h_i(e_x),\qquad
h_i(e_y)\le y_i\le L-h_i(e_y).
$$

For each of the 136 pairs, nonoverlap is the union of its eight signed owner-axis
separation inequalities

$$
n\mathbin{\cdot}(c_j-c_i)\ge h_i(n)+h_j(n).
$$

The square separating-axis theorem makes the finite union over all such choices exactly
the fixed-orientation packing set.
Equality is retained, so boundary contacts are allowed.
Intersect it with $1\le L\le V$. The resulting set is nonempty and compact: it is a
finite union of closed polyhedra, and containment bounds all centre coordinates.

First minimize $L$ over this entire union, obtaining $\ell$. Then successively minimize
all 34 centre coordinates in a fixed labelled order on the remaining compact minimum
sets. This produces a unique lexicographic point $p$ for the chosen orientations and
order. Since $\ell\le L_0<V$, the upper artificial side bound is inactive.
Area gives $\ell^2\ge17$, so the lower bound $L\ge1$ is inactive as well.

### Choose the Branch After the Global Minimum

At $p$, choose a strictly separating signed square axis for each pair whose closed
squares are disjoint.
Such an axis exists by the separating-axis theorem.
For each touching pair, choose a zero-gap separating axis.
Nonoverlap supplies a nonnegative gap, and their common point prevents a strictly
positive gap on any separating axis.

These choices define one polytope $P$ containing $p$ and contained in the full feasible
union. The point $p$ remains its unique lexicographic optimum.
It is a vertex: if it were the midpoint of two distinct points of $P$, minimization of
$L$ would force both endpoints to have side $\ell$; successive coordinate minimizations
would then force every centre coordinate to agree, a contradiction.

At a vertex in 35 variables, the active row normals span all 35 dimensions.
Otherwise a nonzero vector annihilating every active row would permit sufficiently small
movements in both directions, preserving the finitely many strict inactive inequalities
and contradicting the vertex property.
The artificial side bounds are inactive.
Every active pair row now belongs to a physically touching pair, because all
closed-disjoint pairs were assigned strict rows.
Every active wall row is a physical wall contact.
This proves the first conclusion.
The count is of independent scalar equations, not necessarily 35 distinct pair contacts.

Choosing an arbitrary feasible SAT branch before minimizing would prove only a vertex
with independent support equations.
Some of those equations could align projections of physically disjoint squares.
The global lexicographic choice followed by the strict-axis selection is what permits
the stronger physical-contact conclusion.

### Wall Components

Join two squares in the physical contact graph when their closed bodies intersect.
Consider a connected component with no horizontal-wall contact.
Translating all its centres vertically, with $L$ fixed, annihilates every active row:
internal pair differences are unchanged, no active pair joins another component, and any
active wall row of this component has a horizontal normal.
This contradicts the full active-row rank.
The analogous horizontal translation rules out a component with no vertical-wall
contact. Every component therefore touches a wall in each coordinate direction.

Suppose no component touches opposite walls.
Each then touches exactly one vertical and one horizontal wall.
Set $dL=1$; translate a component horizontally by zero if it touches the left wall and
by one if it touches the right wall.
Translate it vertically by zero if it touches the bottom wall and by one if it touches
the top wall. Internal contact differences and every active wall equation are preserved.
This again gives a nonzero vector annihilating all active rows, a contradiction.
Hence some component spans opposite walls, and the preceding argument supplies its third
wall. Rotation and reflection give the stated $D_4$ normalization.

The normalized representative also has at least fourteen distinct contacting square
pairs. No square can touch opposite walls: its coordinate width is at most $\sqrt2$,
whereas $L\ge\sqrt{17}$. For a square touching the left and bottom walls, its centre is
$(h,h)$, where $1/2\le h\le\sqrt2/2$. The point $(1/2,1/2)$ has squared distance
$2(h-1/2)^2<1/4$ from that centre and therefore lies strictly in the square’s
radius-$1/2$ inscribed disk.
Two squares cannot both touch these two walls without overlapping interiors.
The same argument applies at each corner.
At most four squares consequently touch two walls; each remaining square touches at most
one. There are at most $17+4=21$ active wall rows.
The rank-35 system therefore needs at least fourteen active pair rows.
Because its SAT branch selects only one row per unordered pair, these represent fourteen
distinct physical contacts.
This lower bound concerns the normalized representative, not every feasible packing.

### What a Future Consumer Must Still Prove

Apply this normalization globally **before** assigning the representative to cover
cells. Preserving a chosen cell, centre halfplane or fixed witness guard during the
minimization could supply artificial active rows and invalidate the physical-contact
count. The normalized representative may occupy a different state.
This lemma consequently does not certify that an original state is infeasible.

The wall equations concern the actual side $L$. If the representative is centered inside
the larger fixed cap $V$ or the outer $U$ frame, retain that variable-side centering
relation. Contact with the actual container must not be replaced by contact with the
cap’s walls.

A future finite proof must cover every allowed contact system, its independent angle
domains, degeneracies and closed boundary cases, and join the resulting representatives
to its global cover or terminal theorem.
No such enumeration is supplied here.
Do not assume the full touching graph is planar: corner contacts can add both diagonals
at four-square junctions, and larger square grids have nonplanar touching graphs.
A planar-subgraph reduction would require a separate proof.
The lemma provides no uniqueness theorem, present state exclusion, angular restriction
or estimate of the cost of completing n17 optimality.

### Prospective Seventeen-Parameter Algebraic Charts

The rank statement has an exact algebraic consequence.
Independently rotate each square’s choice of body axes by a multiple of a quarter turn,
so its unchanged physical orientation has a half-angle parameter $t_i\in[0,1]$. Write

$$
d_i=1+t_i^2,\qquad C_i=1-t_i^2,\qquad S_i=2t_i,
\qquad u_i=(C_i,S_i)/d_i.
$$

Cover this parameter cube by the finitely many closed ordering chambers
$t_{\pi(1)}\le\cdots\le t_{\pi(17)}$. On each chamber the sign of
$\sin(\theta_j-\theta_i)$ is fixed; ties belong to both adjacent chambers and cause no
gap. Since both angles lie in $[0,\pi/2]$, their difference has nonnegative cosine.
Thus the support threshold for a signed axis of either square is

$$
H_{ij}=\frac{1+\cos(\theta_j-\theta_i)
                  +|\sin(\theta_j-\theta_i)|}{2},
$$

with every absolute value resolved by the chamber’s order.
Multiplication by the strictly positive $2d_i d_j$ makes a pair-contact equation a
polynomial linear equation in the centres.
Multiplication by $2d_i$ does the same for a wall equation, since the wall support is
$(C_i+S_i)/(2d_i)$. The resulting row coefficients and right-hand sides have total
degree at most four in the angle parameters.

For a normalized representative, choose 35 independent active rows supplied by the
lemma. With $z=(x_1,y_1,\ldots,x_{17},y_{17},L)$, these give

$$
A(t)z=b(t),\qquad \Delta(t)=\det A(t)\ne0.
$$

Cramer’s rule expresses every centre coordinate and the side as a rational function
$z_m=N_m(t)/\Delta(t)$ of the seventeen angle parameters.
Splitting into $\Delta>0$ and $\Delta<0$ permits every remaining containment or signed
SAT inequality to be checked by polynomial inequalities after clearing positive
denominators. Retain the complete pairwise SAT disjunctions, all chamber boundaries and
the target side inequality; active equations alone do not certify a packing.

There are finitely many choices of ordered chamber, signed contact/wall rows and nonzero
minor. Every hypothetical packing below $S^\ast$ has a normalized representative in at
least one of these charts.
Conversely, a chart solution satisfying all original containment and nonoverlap
conditions is a packing.
Consequently a global emptiness proof for this finite union would suffice for the
strict-smaller-side problem.
Rank-deficient choices of 35 rows may be discarded, but a zero determinant for one
choice does not discard a physical configuration: another nonzero minor must cover its
normalized representative.

This reduces 52 continuous centre, angle and side variables to seventeen angle
parameters per chart.
It does not bound the number or difficulty of the discrete charts.
No determinant, contact system or angle chamber has been enumerated or tested here; no
completeness implementation, branch reduction or speedup follows from the dimension
count alone. The derivation remains a prospective sole-Astra hand result under the
assurance stated above.

### Practical Next Block for the Normalization Route

The follow-up is tracked as `think-nvkf`. First allocate 30–60 minutes to independent
mathematical review of the existence proof: global lexicographic choice before branch
selection, strict separating axes for closed-disjoint bodies, inactive artificial side
bounds, and the actual-container wall equations are the critical interfaces.
Small exact examples can test a future row generator; they cannot establish this
existence theorem.

The discrete completeness obstacle is substantial.
A complete atlas must cover signed contact choices, wall incidences, angle-order
chambers, a nonzero minor for every normalized representative, and all remaining
nonoverlap disjunctions.
The fourteen-contact lower bound does not identify those contacts, and a determinant
vanishing in one chart requires alternate charts.
Unrestricted contact-graph or minor enumeration has no justified completion estimate.

A smaller consumer can test whether the normalization has useful force on the current
cell cover before investing in that enumeration.
For each named assignment, construct an overestimate of its possible contact graph from
the closed cell bounding boxes.
A contacting pair’s centre distance lies in $[1,\sqrt2]$: the radius-$1/2$ inscribed
disks have disjoint interiors, and a shared boundary point lies within distance
$\sqrt2/2$ of each centre.
Hence an edge can be absent whenever the boxes cannot realize a squared distance in
$[1,2]$.

Wall tags must retain the actual-side centering relation.
For an accepted lower bound $L_{\min}$ and $L\le V$, a left-wall centre in the outer $U$
frame lies in the interval

$$
\left[\frac{U-V}{2}+\frac12,
      \frac{U-L_{\min}}2+\frac57\right],
$$

because the square support is at most $\sqrt2/2<5/7$. Reflect this interval for
right-wall tags and use the same construction vertically.
Intersect these closed intervals with the cell boxes to obtain conservative possible
wall incidences.

Every component of the possible-contact graph must have at least one horizontal and one
vertical wall tag; some component must have an opposite-wall pair and a third wall.
There must be at least fourteen possible edges.
If $E$ counts possible edges and $W$ possible wall incidences, also require
$E+\min(21,W)\ge35$. These are necessary graph and row-count conditions, not a proof of
realizable contacts or full matrix rank.

After the proof review, allocate a separate 1–2 hour implementation block to this narrow
checker, with exact synthetic normalized-packing controls and a prospective measurement
ceiling of 120 seconds on a declared complete candidate roster.
The current 4,683-orbit roster is a possible workload only after its closed assignment,
label and variable-side frame joins are explicit.
Record how many normalized-representative candidates each necessary condition rejects.
If all survive, stop this coarse graph filter and identify a stronger condition before
funding enumeration.
Any rejection concerns normalized representatives; it does not enter the ordinary
$U$-exclusion ledger.
A known packing that has not itself been normalized is not automatically a valid
positive control for every normal-form condition.

These durations are proposed work allocations, not forecasts of acceptance or optimality
completion. Obtaining and independently checking the four reported upstream
full-certificate packages remains ahead of unrestricted atlas enumeration in the
immediate global-proof queue.
The normalization route earns a larger block only through an independently reviewed
theorem interface and a measured reduction or an explicit new completeness argument.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
