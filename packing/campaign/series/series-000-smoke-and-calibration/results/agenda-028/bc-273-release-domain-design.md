# BC-273: A Closed Domain for Releasing Segment 9–10

Status: analytical design for H-120; no target determination or independent acceptance.
Session: session-092. Workflow entry: insight-iteration through BC-273 in
[Agenda 028](../../../../agendas/agenda-028-hybrid-strength-and-angular-release.md),
following [X-018](../../../../explorations/X-018-hybrid-strength-and-angular-release.md)
and [H-120](../../../../hypotheses/H-120-rank-nine-release-exclusion.md).

The retained source feature pattern reduces to ten real parameters, including side and
two actual angles. Its oblique four-square block has two slide parameters whose product
must be nonnegative.
A closed nonnegative-slide pilot has retained segment lengths at least $3/4$. Every
point in the target side interval $[381/100,96/25]$ is already outside the retained
local Trump interior, because a prescribed top-wall center moves by more than $3/100$.
The first proposed exclusion keeps both free angles in the same explicit rational
half-angle interval, while covering every center and separating-axis alternative.

The parameterization and elementary restrictions below are derived here.
Their independent acceptance, control replay, and the proposed exclusion remain
outstanding. This is design progress, not acceptance of H-120.

## Exact Coordinates and Feature Equations

Use the zero-based labels and fixed origin of
[the exact source](../../../../../cases/trump11/packing.py).
For $r\in[0,1]$, put

$$
c(r)=\frac{1-r^2}{1+r^2},\qquad
s(r)=\frac{2r}{1+r^2},\qquad
e(r)=(c(r),s(r)),\qquad f(r)=(-s(r),c(r)).
$$

The actual angle is $2\arctan r$, with orientations understood modulo $\pi/2$. The
endpoints $r=0,1$ represent the same physical axis orientation with different
quarter-turn lifts. There is no average-angle surrogate.
Squares 0 through 5 have the axis basis.
Squares 6 through 9 share the basis $e=e(t),f=f(t)$; square 10 has basis $e(v),f(v)$.

The variables are

$$
(L,z,p_x,p_y,a,b,t,w_x,w_y,v),\qquad p=(p_x,p_y),\quad w=(w_x,w_y).
$$

The six axis-square centers are

$$
\begin{aligned}
C_0&=(1/2,1/2),&C_1&=(L-1/2,1/2),\\
C_2&=(z+1/2,L-1/2),&C_3&=(1/2,L-1/2),\\
C_4&=(3/2,L-1/2),&C_5&=(1/2,L-3/2).
\end{aligned}
$$

These enforce precisely the nine prescribed flush incidences: square 0 left/bottom; 1
bottom/right; 2 top; 3 left/top; 4 top; 5 left.
Positive segments 3–4 and 3–5, together with these wall incidences and containment,
force the displayed relative positions.
Both segments have length one.
The forced 4–5 point contact is retained.
Nonoverlap of the top-row squares gives the useful necessary bound $2\le z\le L-1$.

For the source choice of contact sides in the oblique component, write

$$
\begin{aligned}
C_6&=p,\\
C_7&=p+a e-f,\\
C_8&=p+e+b f,\\
C_9&=p+(a+1)e+(b-1)f,\\
C_{10}&=w.
\end{aligned}
$$

Equivalently, the four retained feature equations and slide restrictions are

| Pair | Normal equation | Tangential displacement | Segment length |
| --- | --- | --- | --- |
| 6–7 | $(C_7-C_6)\cdot f=-1$ | $(C_7-C_6)\cdot e=a$ | $1-\lvert a\rvert$ |
| 6–8 | $(C_8-C_6)\cdot e=1$ | $(C_8-C_6)\cdot f=b$ | $1-\lvert b\rvert$ |
| 7–9 | $(C_9-C_7)\cdot e=1$ | $(C_9-C_7)\cdot f=b$ | $1-\lvert b\rvert$ |
| 8–9 | $(C_9-C_8)\cdot f=-1$ | $(C_9-C_8)\cdot e=a$ | $1-\lvert a\rvert$ |

Starting with four independent tangential slides, closure of the contact cycle equates
the opposite slides, giving exactly $a,b$. This fixes the source contact-side pattern;
other assignments of contact sides are sibling feature domains, not silently covered by
these equations. No equality is imposed on pair 9–10.

The retained angular equality graph has wall component $\{0,\ldots,5,*\}$ and free
components $\{6,7,8,9\}$ and $\{10\}$. Its rank is nine.
Two angular parameters remain before other geometric restrictions; rank alone gives no
feasible motion.

## All Containment and Nonoverlap Conditions

For square $i$, let $(e_i,f_i)$ denote its declared orthonormal basis and define

$$
H_i(n)=\tfrac12\bigl(|n\cdot e_i|+|n\cdot f_i|\bigr),\qquad
h_i=H_i((1,0))=H_i((0,1)).
$$

Impose, for all eleven squares,

$$
h_i\le C_{i,x}\le L-h_i,\qquad
h_i\le C_{i,y}\le L-h_i.
$$

Impose, separately for every one of the 55 unordered pairs $i<j$,

$$
\bigvee_{n\in\{e_i,f_i,e_j,f_j\},\ \sigma\in\{-1,1\}}
\left[\sigma(C_j-C_i)\cdot n\ge H_i(n)+H_j(n)\right].
$$

This is the complete separating-axis condition for closed squares with disjoint
interiors. All alternatives include equality.
A selected source SAT label is not a substitute for this disjunction.
Retained contacts may make some clauses redundant, but the defining domain keeps all 55
conditions, including both oblique diagonals and all ten pairs incident to square 10.

Every denominator $1+t^2$ or $1+v^2$ is positive.
After resolving finitely many absolute value signs, multiplication by positive
denominators gives polynomial equalities and weak inequalities over rational
coefficients. At fixed $t,v$, each SAT selection is linear in the remaining eight
variables.
Uniform angle coverage still needs a proof; a finite collection of fixed-angle
LP answers does not provide it.

## Two Exact Restrictions Before a Target Run

**The diagonal pairs force $ab\ge0$.** Assume $|a|,|b|<1$. The common-basis displacement
of pair 6–9 is $(a+1,b-1)$, so its nonoverlap condition is

$$
a\ge0\quad\text{or}\quad b\le0.
$$

For pair 7–8 the displacement is $(1-a,1+b)$, giving

$$
a\le0\quad\text{or}\quad b\ge0.
$$

Together these are equivalent to $ab\ge0$. Thus a closed box with $a\ge\eta>0$ and
$b\le-\eta$, or the reversed signs, is excluded by one diagonal pair for any rational
$\eta>0$. This elementary feature restriction leaves the shared boundaries $a=0$ and
$b=0$ covered. It is a reduction of the next domain, not the proposed H-120 target
determination.

**The target is outside the local interior without subtracting a ball.** The source root
$u\in(36/100,37/100)$ gives

$$
U(u)=\frac{6u+4}{1+2u-u^2},\qquad
U'(u)=\frac{6u^2+8u-2}{(1+2u-u^2)^2}>0
$$

throughout that interval.
Therefore

$$
U>U(36/100)=\frac{1925}{497}>\frac{387}{100}.
$$

For every $L\le96/25$, the retained center $C_{3,y}=L-1/2$ differs from its source value
by

$$
|C_{3,y}-C^*_{3,y}|=U-L>\frac3{100}>
\rho_{\rm row}=\frac{808514697}{200000000000}.
$$

This binds to the labelled, origin-anchored, center-and-radian sup norm in the
[local theorem](../../../../../cases/trump11/isolation-theorem.md).
The side is not treated as a thirty-fourth norm coordinate.
The center coordinate alone proves separation, independent of the angular lifts.
Consequently the target does not intersect that local interior or its radius boundary.
The local lemma is not used to exclude any target point.
There is no inference about other labelings, reflected wall patterns, or an unproved
global capture by local charts.

## Frozen Compact Pilot and Parent Control

Define the parent $P_+$ using all preceding equations, all containment and SAT
conditions, and the rational bounds

$$
\frac{381}{100}\le L\le4,\qquad
\frac13\le t\le\frac25,\qquad 0\le v\le1,\qquad
0\le a,b\le\frac14,\qquad 2\le z\le L-1.
$$

Require $p,w\in[1/2,7/2]^2$; all other centers are explicitly defined above and obey the
same bound by containment.
Define the target $T_+=P_+\cap\{L\le96/25\}$. All its centers additionally belong to
$[1/2,167/50]^2$. The four retained oblique segments have length at least $3/4$; the two
axis segments have length one.
These bounds are a selected source-feature pilot, not necessary bounds for the whole
rank-nine family.

The parameter box is bounded and every defining relation is closed.
The SAT disjunction is finite.
Thus the parameter domain and its continuous geometric image are compact, including all
equality boundaries.
All eleven-square conditions remain in $T_+$ even when a later proof uses only a subset
to obtain a contradiction.

Trump is an exact feasible control in $P_+$. To bind it, take $t=v=u$, $L=U$, $a=u_1$,
$b=v_1$, $z=x_0$, and

$$
p=(1,1)+\tfrac12e+(\tfrac12-r_1)f,\qquad
w=p+(a+2)e-v_2f,
$$

with $r_1,u_1,v_1,v_2,x_0$ exactly as defined in `packing.py`. The source root interval
implies the coarse rational bounds $3/4<c(u)<4/5$, $3/5<s(u)<7/10$, $19/5<U<4$, and
$1/5<r_1<2/5$. Consequently $-1/6<a<1/5$ and $1/20<b<1/5$. Source feasibility and the
diagonal restriction then give $a\ge0$. This proves the selected slide bounds and the
positive segment margins from the source formulas and their retained validity control.
The source also belongs to the 9–10 recontact and coincident-angle seams.
It lies outside $T_+$ because $U>96/25$. The existing exact witness verifier has not
been re-executed in this design slice.

Enlarging a hypothetical smaller packing to side $96/25$ generally breaks these flush
incidences. The variable $L$ remains quantified in every target and leaf.

## Closed Sibling Scopes

The following boundaries remain explicit even when they are covered by overlap.
No strict feature condition is silently promoted to a closed cover.

| Boundary or remainder | Closed treatment and status |
| --- | --- |
| A retained segment shortens | The pilot uses lengths at least $3/4$. For the same side pattern, a larger positive-feature parent is covered by the pilot-margin portion and closed short-feature portions $0\le1-\lvert a\rvert\le3/4$ or $0\le1-\lvert b\rvert\le3/4$, with the other slide in $[-1,1]$. These portions are open obligations; they are not all covered by the pilot’s angle/sign restrictions. |
| A retained segment reaches zero | Explicit siblings $\lvert a\rvert=1$ or $\lvert b\rvert=1$. A general zero-length contact no longer forces equal component angles, so its physical sibling must also allow the orientations freed by the vanished graph edge. Merely setting $\lvert a\rvert=1$ in this common-angle chart covers only its own closure. |
| Other retained contact sides | Enumerate their side-normal and tangential choices with the same six retained pair identities. The source-feature equations above make no coverage claim for them. |
| Negative slides | For $\lvert a\rvert,\lvert b\rvert<1$, the other possible sign branch is $a,b\le0$. Together the two closed sign branches retain every zero-slide point; their intersection is $a=b=0$. The negative branch is an open exclusion obligation. |
| Slide or angle ranges beyond the pilot | For this side pattern, use closed overlapping intervals outside $[0,1/4]$ for each nonnegative slide, and $t\in[0,1/3]$ or $[2/5,1]$. The pilot does not establish their exclusion. |
| Pair 9–10 recontacts | Define $g=\max_n(\lvert(C_{10}-C_9)\cdot n\rvert-H_9(n)-H_{10}(n))$ over the four SAT axes. All $g\ge0$ are retained. The seam $g=0$ includes point and segment contacts. If separation margins are useful later, $g\ge\eta$ and $0\le g\le\eta$ give closed overlapping children for rational $\eta>0$. |
| Coincident component angles | $v=t$ is included. In a full quarter-turn chart the pairs $(t,v)=(0,1),(1,0)$ are additional physical-coincidence seams. For this pilot $t\in[1/3,2/5]$, so only $v=t$ occurs. No transfer to a completed one-angle theorem is assumed. |
| Axis orientations | Square 10 at $v=0$ or $v=1$ is included. The four-square component’s axis cases belong to the wider-chart siblings $t=0,1$. Angles are actual orientations modulo quarter turns. |
| Local-chart boundary | The displayed top-wall inequality separates all of $T_+$ from the retained local radius boundary. For an extension reaching that boundary, use distance $\ge\rho$ with boundary overlap, or a stated positive separation margin; do not remove a closed ball. |
| Newly formed contacts elsewhere | All equalities in every containment and SAT condition remain allowed. No assumption fixes the other source contact identities. |

The complete cover of all retained graph patterns is not constructed here.
In particular, a zero-length sibling can have angular rank below nine.
Neither this pilot nor its source-feature closure covers every six-axis/four-plus-one
packing.

## Next Exact Proof Obligation

The first proposed target is the closed middle-angle child

$$
T_{\rm mid}=T_+\cap\{1/3\le v\le2/5\}.
$$

Both actual oblique angles range over $[2\arctan(1/3),2\arctan(2/5)]$. This retains
angle coincidence and 9–10 recontact.
Its centers have the full bounds above; no center box is fitted to Trump samples.
The other two square-10 angle children are $v\in[0,1/3]$ and $v\in[2/5,1]$, sharing the
endpoint seams.

**Required determination:** prove $T_{\rm mid}=\varnothing$, or exhibit and exactly
verify one packing in it.
This scope must be prospectively registered and independently accepted before a target
run. The design does not predict that the target is empty with evidential confidence.

An equivalent geometric obligation isolates the genuinely new difficulty.
Let $S$ be any ten-square skeleton consisting of squares 0 through 9 that obeys the
target parameters, its containment conditions, and all 45 skeleton pair conditions.
For each $v\in[1/3,2/5]$, let

$$
B_v=[h_{10},L-h_{10}]^2,\qquad
F_i=C_i+Q_i+Q_{10}(v),\quad i=0,\ldots,9,
$$

where each $Q$ is the corresponding closed unit square centered at the origin and $+$
denotes Minkowski sum.
Central symmetry makes $F_i$ the closed forbidden-center polygon for an additional
square at angle $v$; its interior corresponds to overlap of square interiors.
The necessary and sufficient exclusion is the uniform strict cover

$$
\boxed{\quad B_v\subseteq\bigcup_{i=0}^{9}\operatorname{int}F_i
\quad\text{for every admissible }S,v.\quad}
$$

This is a one-additional-square cavity problem over a seven-parameter skeleton, followed
by its one angle and two center parameters.
At fixed two angles it has the linear leaves described above.
A proof can use the complete SAT disjunction or the equivalent polygon cover, but must
preserve obstacle boundaries: covering $B_v$ by closed $F_i$ alone can forbid a legal
touching packing and is insufficient.

The smallest missing mathematical premise is this uniform cavity cover.
The diagonal sign lemma and graph rank do not establish it.
For a uniform-LP implementation, the smallest missing instrument premise is BC-261
acceptance of a leaf that handles the retained equality substitution, variable side,
complete SAT alternatives and both continuous angle intervals.
A direct analytic cover would instead require independent acceptance of its own
implication. The existing fixed-source-cell numerical scan is not either premise.

Before the target, the same domain reader must pass these controls:

| Control | Required behavior |
| --- | --- |
| Exact Trump at $U$ | Accept the displayed $P_+$ membership and 9–10/coincident-angle seam; reject membership in $T_{\rm mid}$ solely on the side bound. |
| Contact-cycle reconstruction | Rebuild the four centers and every declared normal/tangent projection independently from their corners; detect a reversed retained normal or a changed cycle sign. |
| Positive margin | Verify lengths at least $3/4$ throughout the selected slide box, including its endpoints; refuse a claim extending that margin to $\lvert a\rvert=1$ or $\lvert b\rvert=1$. |
| Mixed slide signs | With $a=1/8,b=-1/8$, detect the 7–8 overlap; with $a=-1/8,b=1/8$, detect the 6–9 overlap. These are component controls, not asserted eleven-square feasible packings. |
| Slide seams | At $a=b=0$, accept the four-square $2\times2$ contact block, including both diagonal point contacts. This is a component feasibility control. |
| Axis and angle coincidence | Preserve the geometrically equivalent $v=0,1$ representations and $v=t$ seam without dropping SAT alternatives or dividing by an angle difference. |
| Polygon-cover equality | Reject a proof that substitutes closed forbidden polygons for their interiors and thereby counts touching as overlap. |
| Omission mutation | Removing one pair alternative, a containment row, or the variable-side wall dependence must fail the declared-domain inventory comparison. |

The independent reader must verify both the geometric implication and every leaf, with
zero unresolved cases.
A failed proposer, point grid, infeasible fixed source cell or unreplayed certificate
leaves the determination open.
No target run was launched in this slice; target/replay cost remains to be measured from
accepted controls.

## Evidence and Handoff

The source formulas, retained local chart, X-018, H-120, Agenda 028 and the
[strategy review](../../../../../../docs/project/reviews/review-2026-09-07-n11-hybrid-strategy.md)
were read directly. The exact reduction, diagonal restriction and rational local
separation are analytic derivations in this note.
Source feasibility is retained evidence from the exact source packet, not a fresh
verifier result.

Only this design note was written.
No registry, experiment ID, Git state, dependency, target computation or external
application was changed.
The next owner should review the analytic implications and source-control binding, then
price the uniform cavity cover target.
H-120, the negative-slide and wider-angle families, degeneracies and all global
structural conclusions remain open.

Work began at `2026-09-07T06:40:08Z`; the first complete draft existed by
`2026-09-07T06:49:00Z`, an elapsed 8 minutes 52 seconds.
The document received the Practical Prose common-guidelines and de-slop passes.
Installed Flowmark 0.4.0 was used only on this file.
Its initial formatting invocation reported that the default cache could not be persisted
outside the workspace; the final invocation disables that cache.
No scientific run or mathematical measurement was hidden in scratch code.
Final verification reached `2026-09-07T06:50:39Z`, 10 minutes 31 seconds after startup:
Flowmark’s full auto-format check passed with caching disabled, the scoped whitespace
check passed, and all six linked source files existed.
No background command remained.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
