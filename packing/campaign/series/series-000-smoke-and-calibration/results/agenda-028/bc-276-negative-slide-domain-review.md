# BC-276: Negative-Slide Domain Preflight

The complete closed domain $N$ in the
[BC275 allocation](bc-275-first-checkpoint-allocation.md) is accepted for a prospective
analytical determination.
Its stated signed short-slide parent satisfies exactly $S=T_+\cup N$. No established
label, angle-lift or container symmetry transfers the whole negative branch to the
[accepted positive pilot](bc-273-analytic-independent-review.md).
The candidate therefore has unresolved scope beyond the already excluded zero-slide
intersection. This review makes no exclusion claim or feasible construction for $N$.

The review is session092 phase 7, BC276, W3 domain preflight under H120. It checks the
allocation against the [feature equations](bc-273-release-domain-design.md), their
[independent source-corner and diagonal review](bc-273-release-domain-independent-review.md),
and the accepted analytical exclusion.
It does not extend BC273’s completed target attempt.

## Complete Domain and Closed Boundaries

The accepted candidate keeps the same labels, origin and displayed center formulas, with
bounds

$$
381/100\le L\le96/25,\quad 1/3\le t\le2/5,\quad 0\le v\le1,
\quad -1/4\le a,b\le0,\quad 2\le z\le L-1,
\quad p,w\in[1/2,7/2]^2.
$$

The axis centers remain

$$
\begin{aligned}
C_0&=(1/2,1/2),&C_1&=(L-1/2,1/2),\\
C_2&=(z+1/2,L-1/2),&C_3&=(1/2,L-1/2),\\
C_4&=(3/2,L-1/2),&C_5&=(1/2,L-3/2),
\end{aligned}
$$

and the free centers remain

$$
C_6=p,\quad C_7=p+ae-f,\quad C_8=p+e+bf,\quad
C_9=p+(a+1)e+(b-1)f,\quad C_{10}=w.
$$

Here $e(r)=((1-r^2)/(1+r^2),2r/(1+r^2))$ and $f(r)$ is its counterclockwise quarter
turn. Squares 6–9 use $r=t$ and square 10 uses $r=v$. These are exact unit bases with
actual angle $2\arctan r$; all denominators are positive.
The interval $v\in[0,1]$ includes both representations of the axis orientation.
The block interval contains no axis orientation, by design.
The equal-angle case $v=t$ is included.

Every square has all four support containment inequalities.
Every one of the 55 unordered pairs has its complete four-axis, two-direction SAT
disjunction, with threshold $H_i(n)+H_j(n)$ and a weak inequality.
In particular this retains the two block diagonals, all ten pairs incident to square 10,
and possible recontacts.
No positive 9–10 gap is imposed.
The common center box is redundant: containment and the unit-square support bound
$h_i\ge1/2$ already put every target center in $[1/2,167/50]^2$.

The retained component identities do not require positive slides.
The four oblique segment lengths remain $1-\lvert a\rvert$ or $1-\lvert b\rvert$, at
least $3/4$ on this negative box.
The two axis segments have length one, and all nine specified wall incidences are
unchanged. These are statements about the retained graph; additional contacts may raise
its full angular equality rank.

The box is bounded.
The centers, supports and pair projections are continuous; the finite
SAT disjunctions are closed.
Thus the complete parameter set and its geometric image are compact.
Side, slide and angle endpoints, $z=2$, $z=L-1$, containment equalities, zero slides and
legal touching remain included.
Some of these boundary conditions may later be shown infeasible, but none is deleted in
the definition.

## Exact Signed-Parent Identity

Let $S$ have the same equations, containment and all 55 pair conditions, replacing only
the slide bounds by $a,b\in[-1/4,1/4]$. In the common block basis, the diagonal
displacements are $(1+a,b-1)$ for 6–9 and $(1-a,1+b)$ for 7–8. The complete common-angle
SAT conditions therefore reduce to

$$
(a\ge0\ \lor\ b\le0)\quad\land\quad
(a\le0\ \lor\ b\ge0),
$$

equivalently $ab\ge0$. The strict bounds $\lvert a\rvert,\lvert b\rvert<1$ needed for
this reduction hold on all of $S$. No directed alternative or equality is lost by
reducing the duplicate common-basis axes.

Every point of $S$ consequently has either $a,b\ge0$ or $a,b\le0$, and belongs to $T_+$
or $N$, respectively.
Conversely each child satisfies every condition of $S$. This proves $S=T_+\cup N$
exactly. When one slide is zero, the sign of the other places the point in its
appropriate closed child.
The two sets of defining conditions intersect at $a=b=0$; their feasible intersection is
empty by the already accepted $T_+$ exclusion.
The entire zero-slide boundary must nevertheless remain in the prospective definition of
$N$.

The identity is specific to the common-angle, short-slide chart with its fixed contact
sides and wall assignments.
It does not cover longer slides, other block angles or physical degenerations in which a
vanished contact frees an orientation.

## Symmetry and Redundancy Check

There is no nonidentity symmetry of the square container preserving the declared wall
inventory, even if its square labels are permuted.
The nine prescribed incidences have wall counts

$$
\text{bottom}:2,\qquad \text{right}:1,\qquad
\text{top}:3,\qquad \text{left}:3.
$$

An inventory-preserving dihedral symmetry must fix the uniquely counted bottom and right
walls individually. They are adjacent, so only the identity does so.
This uses the prescribed inventory, not an assertion that no extra contacts can occur.
A transfer relying on additional forced wall incidences would need a new geometric
premise.

Internal relabeling of the block also supplies no sign reversal.
Write its two edge vectors as $U=ae-f$ and $V=e+bf$. For the four proper quarter-turn
basis lifts, the corner relabelings preserving the displayed directed contact-side
pattern give slide pairs $(a,b)$ or $(b,a)$. For example, in the basis $(e',f')=(f,-e)$,
take new origin at old square 7; then $V=be'-f'$ and $-U=e'+af'$, so the new slides are
$(b,a)$. The opposite lift negates both edge vectors and preserves $(a,b)$. These
operations preserve the negative sign branch.

Moreover, the physical block orientation has a unique representative in the accepted
interval $[2\arctan(1/3),2\arctan(2/5)]$. Choosing another quarter-turn lift cannot
change the physical configuration into one with different slides while keeping this same
prescribed basis. A global reflection, even if the wall obstruction were ignored, would
change the normalized half-angle to

$$
t'=(1-t)/(1+t)\in[3/7,1/2],
$$

which is disjoint from $[1/3,2/5]$. A reflection of only the oblique block can alter its
slide signs, but moves its centers relative to the six axis squares and square 10. There
is no accepted implication preserving those containment and pair conditions.
It cannot be used as a packing symmetry.

The retained graph distinguishes the four-square block from square 10 and the wall
component, so an inventory-preserving label permutation cannot exchange those
components. No broader, configuration-dependent transfer has been established here.
Such a redundancy claim would require an explicit map into accepted scope and a proof
that all walls, features, angle ranges, containment conditions and pair disjunctions are
preserved. The existing accepted contracts provide no such map.

## Controls and Future Acceptance

The controls have the following exact scopes:

- At $a=b=0$, the component forms a unit grid block and its diagonals touch at points.
  This is a valid unit-geometry and weak-touching control.
  It is not a feasible eleven-square target packing; that complete seam is already
  excluded by $T_+$.
- At $(a,b)=(1/8,-1/8)$, pair 7–8 has common-basis displacement $(7/8,7/8)$; at
  $(-1/8,1/8)$, pair 6–9 has displacement $(7/8,-7/8)$. These are exact mixed-sign
  component refusals, not tested or asserted eleven-square examples.
- The independently verified Trump source has $L=U>96/25$ and strictly positive slides.
  It is outside $N$ by both the target side cap and slide signs.
  It remains a positive parent/source-construction control, including its
  coincident-angle and 9–10 recontact, and cannot be presented as a positive candidate
  witness.

The positive proof’s inequalities $B\le M-b\le M$, $D+bs^2\ge D$ and its $a\ge0$ cap and
containment bounds cannot be transferred as written.
The previously checked expression $J-M\ge2/87$ remains an exact angle-and-side
inequality, but its opposing geometric rows have not been derived for $N$. This
preflight does not attempt to derive them.

The prospective criterion is accepted: either exclude the whole closed $N$ through
independently audited necessary conditions, or provide an exactly verified eleven-square
packing in $N$. A complete ten-square contradiction would suffice; a feasible ten-square
skeleton would only defeat that route.
Partial exclusions, failed constructions and time expiration leave the stated
determination unresolved.

The proposed 25-minute author, concurrent 20-minute adversary and subsequent 20-minute
independent audit total at most 65 worker-minutes and a 45-minute mathematical critical
path. These are future caps.
No target is admitted by this review before the coordinator commits its prospective
protocol, passes record validation, and records actual dispatch deadlines.
No numerical proposer, solver or BC261 adapter is part of that allocation.

## Comparison With the Prospective Protocol

The [BC276 protocol](bc-276-negative-slide-protocol.md) matches the reviewed allocation:
the same complete $N$, signed-parent identity, controls, independent acceptance rule,
native W3 ownership and absence of a new scientific ID. No mathematical scope mismatch
was found. It correctly requires the protocol commit, this scope acceptance and record
validation before target dispatch.

Its common endpoint is 09:50:00 UTC on September 7, with the independent audit starting
by 09:30:00. Both author and adversary reports must therefore be terminal by 09:30. A
full author window requires dispatch by 09:05, and a full adversary window requires
dispatch by 09:10. A later dispatch must shorten the corresponding worker’s cap,
including the adversary’s, to preserve the full audit.
The coordinator should record those individual deadlines before dispatch; no scope
change is required.

## Receipt and Disposition

The phase lease is `2026-09-07T08:38:00Z` through `2026-09-07T08:48:00Z`; the first
clock read after dispatch was `2026-09-07T08:40:25Z`. This was a review of domain
equations, existing implications, controls and proposed symmetries.
No $N$ exclusion, packing witness, numerical work or target run was attempted.

Only this assigned report was written.
No source or author document, registry, Git state, ID or dependency was changed.
The disposition is domain acceptance, with the full determination of $N$ unresolved and
no established whole-domain symmetry transfer.
Any exclusion would complete only the declared signed short-slide parent $S$, not global
square-packing coverage.

The coordinator may now commit and validate the reviewed, separately timed analytical
protocol. The document received the common-guidelines and de-slop passes and installed
Flowmark 0.4.0 with caching disabled.
The full reread and initial formatting check passed; the displayed equations and control
scopes survived formatting.
A final scoped check follows the protocol comparison and receipt before delivery.

The domain and protocol review and document checks completed at `2026-09-07T08:46:20Z`,
5 minutes 55 seconds after the first clock read and 1 minute 40 seconds before the hard
deadline. All five linked files exist, Flowmark’s full auto-format check passed, no
trailing whitespace was found, and the required footer appears once.
No background command remains.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
