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

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
