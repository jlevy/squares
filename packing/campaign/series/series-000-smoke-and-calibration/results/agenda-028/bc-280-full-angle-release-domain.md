# BC-280: Full-Angle Signed-Release Domain

Status: domain design for H-120, awaiting independent admission.
No enlarged-family exclusion or witness is claimed.
Workflow: W3 insight-iteration, existing BC-280 and think-7ylp, session-092 phase 16.
The prospective lease is September 7, 2026, 11:36:33–11:56:33 UTC; the actual first
clock was 11:39:13 UTC.

This design extends the accepted signed short-slide feature domain to the complete
physical common-angle chart $t\in[0,1]$. It retains the source wall and contact-side
pattern, all eleven squares, variable side length, and every separating-axis
alternative. The accepted exclusion remains confined to $t\in[1/3,2/5]$. The rest of the
chart is an unresolved target proposal, requiring a separate future protocol before
scientific work begins.

The starting equations and their original control are in the
[BC-273 release design](bc-273-release-domain-design.md) and
[independent domain review](bc-273-release-domain-independent-review.md).
The signed decomposition was accepted in the
[BC-276 domain review](bc-276-negative-slide-domain-review.md).
The positive and negative middle-angle exclusions were accepted separately in the
[BC-273 mathematical audit](bc-273-analytic-independent-review.md) and
[BC-276 mathematical audit](bc-276-negative-slide-independent-review.md).
Those results are reused only on their stated domains.

## Frozen Parameter Domain

For $r\in[0,1]$, define

$$
c(r)=\frac{1-r^2}{1+r^2},\qquad s(r)=\frac{2r}{1+r^2},\qquad
e(r)=(c(r),s(r)),\qquad f(r)=(-s(r),c(r)).
$$

The actual angle is $2\arctan r\in[0,\pi/2]$. Orientations are physical square
orientations modulo $\pi/2$, with both endpoint lifts retained.
The basis is orthonormal with determinant one throughout the closed chart.
Its denominators never vanish.
There is no averaged angle or restriction to $c\ge s$.

The ten parameters and their target bounds are

$$
\begin{gathered}
(L,z,p_x,p_y,a,b,t,w_x,w_y,v),\qquad p=(p_x,p_y),\quad w=(w_x,w_y),\\
381/100\le L\le96/25,\quad 0\le t,v\le1,\quad
-1/4\le a,b\le1/4,\\
2\le z\le L-1,\qquad p,w\in[1/2,7/2]^2.
\end{gathered}
$$

Squares 0–5 use the basis $E=(1,0),F=(0,1)$. Squares 6–9 share $e=e(t),f=f(t)$. Square
10 uses its independent basis $e(v),f(v)$. The centers are

$$
\begin{aligned}
C_0&=(1/2,1/2),&C_1&=(L-1/2,1/2),\\
C_2&=(z+1/2,L-1/2),&C_3&=(1/2,L-1/2),\\
C_4&=(3/2,L-1/2),&C_5&=(1/2,L-3/2),\\
C_6&=p,&C_7&=p+ae-f,\\
C_8&=p+e+bf,&C_9&=p+(a+1)e+(b-1)f,\\
C_{10}&=w.
\end{aligned}
$$

Call the domain with these bounds and **all** the geometric conditions below
$\mathcal S_{\rm full}$. Its parent control domain $\mathcal P_{\rm full}$ changes only
the upper side bound to $L\le4$; thus
$\mathcal S_{\rm full}=\mathcal P_{\rm full}\cap\{L\le96/25\}$. These symbols are local
mathematical definitions, not new experiment or hypothesis identifiers.

## Corner Labels, Walls, and Retained Segments

For every square, its declared basis $(e_i,f_i)$ fixes the counterclockwise corners

$$
\begin{aligned}
V_{i,0}&=C_i-(e_i+f_i)/2,&V_{i,1}&=C_i+(e_i-f_i)/2,\\
V_{i,2}&=C_i+(e_i+f_i)/2,&V_{i,3}&=C_i+(-e_i+f_i)/2.
\end{aligned}
$$

This is the corner order of the exact source’s rotated unit square.
The edges with outward normals $-f_i,+e_i,+f_i,-e_i$ are respectively $[0,1]$, $[1,2]$,
$[2,3]$, $[3,0]$. Labels continue algebraically through every angle seam; they are not
reassigned to whichever corner is currently highest.

The nine prescribed flush wall incidences are 0 left/bottom, 1 bottom/right, 2 top, 3
left/top, 4 top, and 5 left.
For these axis squares, left, bottom, right, and top use corner edges $[3,0]$, $[0,1]$,
$[1,2]$, and $[2,3]$, respectively.
The incidence counts are bottom 2, right 1, top 3, left 3. Additional wall contacts are
allowed. The top-row ordering and containment require $2\le z\le L-1$.

The six retained positive segments are explicit:

| Pair | Center displacement | First / second contact edges | Length |
| --- | --- | --- | --- |
| 3–4 | $E$ | $[1,2]$ / $[3,0]$ | $1$ |
| 3–5 | $-F$ | $[0,1]$ / $[2,3]$ | $1$ |
| 6–7 | $ae-f$ | $[0,1]$ / $[2,3]$ | $1-\lvert a\rvert$ |
| 6–8 | $e+bf$ | $[1,2]$ / $[3,0]$ | $1-\lvert b\rvert$ |
| 7–9 | $e+bf$ | $[1,2]$ / $[3,0]$ | $1-\lvert b\rvert$ |
| 8–9 | $ae-f$ | $[0,1]$ / $[2,3]$ | $1-\lvert a\rvert$ |

All four block segments have length at least $3/4$, including at both axis lifts and all
slide endpoints. Contact-cycle closure identifies opposite tangential slides because
$e,f$ are linearly independent.
The forced 4–5 point contact at $(1,L-1)$ also remains.
Pair 9–10 has no prescribed contact or positive separation margin.

The retained angular-equality graph has the wall component $\{0,\ldots,5,*\}$ and
components $\{6,7,8,9\}$ and $\{10\}$, hence retained rank nine.
Coincident orientations do not themselves add graph edges; new segment contacts may add
edges.
Neither this graph rank nor the ten-parameter description proves a feasible motion
or a positive-dimensional feasible family.

## Complete Actual-Square Conditions

Write

$$
H_i(n)=\frac{|n\cdot e_i|+|n\cdot f_i|}{2},\qquad
h_i=H_i((1,0))=H_i((0,1)).
$$

All eleven squares satisfy their actual containment conditions

$$
h_i\le C_{i,x}\le L-h_i,\qquad h_i\le C_{i,y}\le L-h_i.
$$

These are 44 scalar wall inequalities.
For every one of the 55 unordered pairs $i<j$, independently impose all eight directed
SAT alternatives as one disjunction:

$$
\bigvee_{n\in\{e_i,f_i,e_j,f_j\},\ \sigma\in\{-1,1\}}
\left[\sigma(C_j-C_i)\cdot n\ge H_i(n)+H_j(n)\right].
$$

The condition is exact for closed squares with disjoint interiors.
Equality permits edge or point touching.
Duplicate axes at equal angles or endpoint lifts remain valid alternatives.
No source-selected SAT direction is fixed in this definition.
The pair inventory is 15 within 0–5, 24 between 0–5 and 6–9, six within 6–9, and ten
incident to square 10: $15+24+6+10=55$. Both block diagonals and all square-10 pairs
remain, even if a future contradiction uses fewer premises.

For all chart angles, $1/2\le h_i\le1/\sqrt2$. Therefore target containment bounds every
center in $[1/2,167/50]^2$; parent containment bounds every center in $[1/2,7/2]^2$. The
displayed bounds on $p,w$ do not omit a contained center.
The parameter set is bounded and closed: all maps are continuous and each SAT condition
is a finite union of closed sets.
Its geometric image is compact.
Resolving the finitely many absolute-value signs and multiplying positive denominators
also gives a semialgebraic description.

At fixed $t,v$, each selected SAT system is affine in the other eight parameters.
This observation supplies neither a uniform angular certificate nor a complete cover.
Variable $L$ stays quantified; enlarging the box to a fixed side generally breaks the
prescribed flush incidences.

## Complete Closed Angle and Sign Cover

The two diagonal pairs give an angle-independent sign restriction.
Their common-basis displacements are

$$
C_9-C_6=(1+a)e+(b-1)f,\qquad
C_8-C_7=(1-a)e+(1+b)f.
$$

On $|a|,|b|\le1/4$, their full SAT conditions reduce exactly to

$$
(a\ge0\ \text{or}\ b\le0)\quad\text{and}\quad
(a\le0\ \text{or}\ b\ge0),
$$

equivalently $ab\ge0$. This uses only the shared orthonormal basis, so it remains valid
at $t=0,1$ and $c=s$. It is the existing feature restriction, not an exclusion of the
enlarged domain. Keep all diagonal SAT clauses as well.

Define $\mathcal S^+_{\rm full}$ by $a,b\ge0$ and $\mathcal S^-_{\rm full}$ by
$a,b\le0$, within $\mathcal S_{\rm full}$. Then

$$
\mathcal S_{\rm full}=\mathcal S^+_{\rm full}\cup\mathcal S^-_{\rm full},\qquad
\mathcal S^+_{\rm full}\cap\mathcal S^-_{\rm full}
=\mathcal S_{\rm full}\cap\{a=b=0\}.
$$

If exactly one slide is zero, the sign of the other determines its child.
No zero-slide boundary is discarded.
Each of the four slide-boundary faces $a=\pm1/4$ and $b=\pm1/4$ retains the same
complete geometric conditions.

Let $\tau=\sqrt2-1$, the positive root of $\tau^2+2\tau-1=0$. Then $2/5<\tau<1/2$ and
$c(\tau)=s(\tau)=1/\sqrt2$. Cross each row below with both sign children, keeping every
$v\in[0,1]$:

| Common-angle interval | Status for both slide signs |
| --- | --- |
| $I_0=[0,1/3]$ | Unresolved outside its already accepted endpoint |
| $I_{\rm mid}=[1/3,2/5]$ | Excluded by the accepted BC-273 and BC-276 results |
| $I_2=[2/5,\tau]$ | Unresolved outside its already accepted endpoint |
| $I_3=[\tau,1]$ | Unresolved, including the second axis lift |

These eight closed children cover the whole proposed domain.
Six children remain unresolved.
Adjacent children overlap at $1/3$, $2/5$, and $\tau$; sign children overlap at $a=b=0$.
A future remainder may use the closed union of $I_0,I_2,I_3$ for both signs, retaining
the accepted endpoint overlaps.
Deleting the closed middle interval and then treating the remainder as closed would lose
this contract.

The accepted middle-angle theorem has unrestricted $v$ because its contradiction does
not use square 10. This does not extend its common-angle range.
The half chart $[0,\sqrt2-1]$ would omit physical common orientations with canonical
angle $\theta-\pi/2\in(-\pi/4,0)$; no symmetry reduction removes them here.

## Regular Endpoints and Quarter-Turn Relabeling

At $t=0$, $(e,f)=(E,F)$ and

$$
C_7=p+(a,-1),\quad C_8=p+(1,b),\quad C_9=p+(a+1,b-1).
$$

At $t=1$, $(e,f)=(F,-E)$ and

$$
C_7=p+(1,a),\quad C_8=p+(-b,1),\quad C_9=p+(1-b,a+1).
$$

These are regular contained-square and SAT domains.
They describe the same physical axis orientation with different basis lifts, but not the
same labeled centers when $p,a,b$ are held fixed.
The $c=s$ seam is also regular; no domain equation divides by $c-s$, $c$, or $s$.

A basis change by a quarter turn can preserve the physical four-square set with the
following simultaneous relabeling.
Here the slot tuple lists the old square labels assigned to new slots $(6,7,8,9)$;
corner subscripts are modulo four.

| Basis lift | New basis | New $p$ | New $(a,b)$ | New slot tuple | New corner $k$ is old corner |
| --- | --- | --- | --- | --- | --- |
| $0$ | $(e,f)$ | $C_6$ | $(a,b)$ | $(6,7,8,9)$ | $k$ |
| $+1$ | $(f,-e)$ | $C_7$ | $(b,a)$ | $(7,9,6,8)$ | $k+1$ |
| $+2$ | $(-e,-f)$ | $C_9$ | $(a,b)$ | $(9,8,7,6)$ | $k+2$ |
| $+3$ | $(-f,e)$ | $C_8$ | $(b,a)$ | $(8,6,9,7)$ | $k+3$ |

For example, put $U=ae-f$ and $V=e+bf$. Under the $+1$ row, the new two block
displacements are $V$ and $-U$ from old $C_7$, proving that row directly; iteration
gives the others. Corner cycling follows by substituting the new basis into the four
displayed corner formulas.
The six axis labels and square 10 stay fixed.
All physical shapes, walls, and pair conditions are preserved, with block labels
permuted. The four retained block segments map to the same four-pair cycle.
The new $p$ is an old contained center, so its bound is preserved.
Slides are swapped or unchanged; this operation does not reverse their signs.

At the chart endpoints, the $+1$ row maps a $t=0$ representation to a $t=1$
representation; the inverse row reverses that change.
Both representations remain in the cover.
For an interior angle, a quarter-turn basis lift generally leaves the selected
real-angle interval before reducing modulo $\pi/2$. It does not map $\theta$ to
$\pi/2-\theta$. Square 10’s endpoint lifts likewise differ only by corner cycling at the
same center $w$.

A physical reflection that changes the angle in that latter way also changes positions
and walls. The prescribed wall inventory has unique counts at bottom and right, so an
inventory-preserving symmetry of the container must fix those two walls and is the
identity. Thus no general wall-preserving reflection and label permutation has been
established to erase the upper-angle remainder.
Rotating or reflecting only the block changes its cross-pair and containment conditions.
Additional contacts might permit special coincidences; they supply no uniform reduction
of this domain.

## Touching, Recontact, and Proof Boundaries

All wall equalities and all SAT equalities remain legal.
The angle-coincidence seams are $v=t$ and the endpoint pairs $(t,v)=(0,1),(1,0)$.
Neither coincident angles nor recontact are removed.
In particular, with the four actual pair axes,

$$
g_{9,10}=\max_n\bigl(|(C_{10}-C_9)\cdot n|-H_9(n)-H_{10}(n)\bigr)
$$

satisfies $g_{9,10}\ge0$ throughout the domain.
Its zero set includes point and segment contacts.
The source’s 9–10 contact is permitted.
Any future separation split must cover both $g\ge\eta$ and $0\le g\le\eta$, with
overlap, or retain the unsplit condition.
New contacts on other pairs are equally permitted.

The old analytical proofs cannot simply be evaluated outside their admitted middle-angle
interval. In particular:

| Old proof ingredient | Missing implication on the full chart |
| --- | --- |
| Coarse bounds such as $c\ge18/25$, $s\ge3/5$, and $c+s\ge6/5$ | They are not global chart bounds. Any use must be proved on its new closed subdomain. |
| $c>s$ and a triangular cap parametrized through depth $s$ | The ordering changes at $\tau$. At axis endpoints the highest corner becomes an edge; divisions by $cs$ are invalid there. Cap localization and section formulas require separate justified cases. |
| Forced alternatives on pairs such as 0–6, 1–7, 1–9, or 5–6 | Every discarded SAT alternative needs a fresh bound outside $I_{\rm mid}$. The domain itself discards none. |
| Top-gap localization and the terminal side contradiction | Their earlier coarse bounds and cap identities must remain valid before the old terminal constant can be reused. A displayed constant alone supplies no transfer. |
| Independence from square 10 | It yields all $v$ only where the earlier ten-square contradiction was proved. It establishes no whole-chart skeleton exclusion. |

For $0<t<1$, the highest corner of a block square is $V_{i,2}$; at $t=0$ the highest
edge is $[2,3]$, and at $t=1$ it is $[1,2]$. These degeneracies are kept in the domain
and in the corner binding.
No new cap or enlarged-family exclusion is attempted here.

## Exact Parent and Refusal Controls

The existing [Trump source](../../../../../cases/trump11/packing.py) supplies an exact
parent control. Let $u\in(36/100,37/100)$ be its isolated root, with polynomial
coefficients $(5,-10,-2,14,12,-6,2,2,-1)$ in descending order.
Using the source’s exact quantities, the binding is

$$
\begin{gathered}
t=v=u,\quad L=U=\frac{6u+4}{1+2u-u^2},\quad
a=u_1,\quad b=v_1,\quad z=x_0,\\
p=(1,1)+\tfrac12e+(\tfrac12-r_1)f,\qquad
w=p+(a+2)e-v_2f.
\end{gathered}
$$

The source defines

$$
\begin{gathered}
r_1=1-(U-3)c,\qquad u_1=((1+r_1)c-1)/s,\qquad v_1=c-s,\\
v_2=(U-1)/s-r_1-(3+u_1)c/s,\qquad
x_0=1+2/c-(U-2)s/c,
\end{gathered}
$$

where $c=c(u),s=s(u)$. These source-only formulas are not imposed on the enlarged domain
and are not evaluated at its axis endpoints.
The accepted source review establishes its feasibility, the selected slide bounds
$0\le a<1/5$ and $1/20<b<1/5$, and $387/100<U<4$. Its exact containment supplies the
remaining parent coordinate bounds.
Thus it lies in $\mathcal P_{\rm full}$, including the coincident-angle and recontact
seams, but lies outside $\mathcal S_{\rm full}$ because $U>96/25$. No target witness
follows. No source verifier is rerun in this design slice.

The original target-side separation from the retained local Trump interior also remains
valid: $C_{3,y}=L-1/2$ differs from its source value by
$U-L>3/100>808514697/200000000000$, independently of both angle lifts.
The last number is the accepted radius in the labelled, fixed-origin, center-and-radian
sup norm; the single center coordinate supplies the separation.
The accepted local theorem does not exclude these new angle cases and is not used as a
global capture argument.

The proposed admission controls are finite formula and scope checks:

- Bind the exact parent control with its original corner order and reject its promotion
  to a target witness by the side inequality alone.
- Check both endpoint formulas, the four basis-lift rows and their corner cycles, and
  the regular $c=s$ seam.
  Reject replacing the full chart by a half chart or reflecting the block without
  transforming every wall and pair condition.
- At any common basis, $(a,b)=(1/8,-1/8)$ makes pair 7–8 have coordinates $(7/8,7/8)$
  and overlap; $(-1/8,1/8)$ makes pair 6–9 have coordinates $(7/8,-7/8)$ and overlap.
  At $a=b=0$ the four-square grid has legal diagonal point touching.
  These are block controls, not eleven-square packings.
- Check all eight closed angle/sign children, their overlaps, both independent angle
  endpoints, recontact, and every slide endpoint.
  Reject omitted seams or a strict inequality substituted for legal touching.
- Count 44 containment rows and all 55 complete SAT disjunctions, preserving the
  independent square-10 pose and variable side.
  A fixed-angle LP, a selected source SAT branch, or a ten-square feasible configuration
  cannot satisfy the proposed eleven-square target contract.

## Admission Price and Remaining Coverage

The next allocation is **one independent domain admission capped at 15 minutes**, plus
coordinator record integration.
It must check the equations, labels, both quarter-turn lifts, the complete closed cover,
and the exact scope of the inherited theorem.
A missing alternative, corner binding, endpoint, or preservation premise blocks
admission until corrected.
This document authorizes no target proof, numerical search, or enlarged-domain theorem
attempt.

After admission, any scientific allocation needs its own prospective protocol,
acceptance and negative-control rules, author/adversary/audit time limits, committed
record, and dispatch.
A sufficient positive result would exclude all of $\mathcal S_{\rm full}$, or its stated
closed remainder together with the accepted middle theorem.
A sufficient negative result would be a rigorously verified eleven-square packing in
that exact domain. A contradiction from a necessary subset suffices only when proved
uniformly on the stated domain.
Partial bounds, uncovered angular cases, or smaller-model feasibility remain unresolved
evidence.

Even complete success would cover this source wall pattern, six retained pair
identities, chosen contact sides, and signed short slides.
Other wall patterns, label assignments outside proved symmetries, contact-side choices,
longer slides, vanishing retained segments with freed orientations, and other angular
component patterns remain outside it.
No global representative or finite-motion premise is proved; no KKT result, full H-120
readiness, or strict comparison with H-118 follows.

## Work Receipt

Actual first clock: 2026-09-07 11:39:13 UTC. Substantive design and self-review ended at
11:51:47 UTC. The document freeze clock was 2026-09-07 11:52:30 UTC, 797 seconds after
the actual start, before the 11:56:33 UTC hard stop.
The complete document was reread; all six native link targets exist; the required footer
occurs once. Source formulas, corner order, quarter-turn substitutions, closed-cover
inventory, and inherited theorem scope were checked by hand.
Installed Flowmark 0.4.0 formatting and its check passed on this assigned file; the
final receipt receives the same formatting check before terminal delivery.
Work was confined to domain design and source comparison.
The active BC-279 target reports were not read or discussed.
No target proof, numerical computation, solver, source edit, dependency change, Git
mutation, or shared-record change was performed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
