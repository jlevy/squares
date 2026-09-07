# BC-282: Residual Skeleton and a Proposed Translation Fence

**The complete ten-square domain is specified; the proposed new proof route is not
target-ready.** A joint translation description retains the correlations among all four
squares in the contact block.
A specific sufficient strengthening would cover every permitted translation fiber by a
strict chain of at most six collision intervals, with distinct axis-square owners.
Uniform chain templates and a bounded accounting of their endpoint changes have not been
obtained. Finiteness alone is not an admission argument for the conditional analytical
target.

This is design-only work under existing BC-282, H-120 and `think-s6e7`, in
[session-096](../../../../agent-sessions/session-096-residual-skeleton.md).
The prospective design window is September 7, 2026, 17:20–17:40 UTC; the actual first
clock was 17:21:00 UTC. No target proof, witness search, numerical measurement, adapter
or implementation is attempted.
The other BC-282 reports were not read.

The defining source is the [BC-280 domain](bc-280-full-angle-release-domain.md),
incorporated by the [BC-281 protocol](bc-281-full-angle-release-protocol.md).
Only the implications accepted in the
[BC-281 independent audit](bc-281-full-angle-independent-review.md) are inherited.
The
[current agenda](../../../../agendas/agenda-028-hybrid-strength-and-angular-release.md)
requires a complete residual decision or an explicit admission gap, not another fitted
angular exclusion.

## Complete Indexed Domain

Let $\mathcal K^*$ be the seven-parameter necessary skeleton with

$$
(L,z,p_x,p_y,a,b,t),\qquad p=(p_x,p_y),
$$

$$
381/100\le L\le96/25,\qquad
t\in[1/24,1/3]\cup[1/2,23/25],\qquad
-1/4\le a,b\le1/4,
$$

$$
2\le z\le L-1,\qquad p\in[1/2,7/2]^2.
$$

All retained parameters have their original bounds.
Square 10’s center $w$ and angle parameter $v$ disappear because no remaining condition
uses them. If the original ten-coordinate tuple is desired, the same skeleton is the
product with the dummy box $w\in[1/2,7/2]^2$, $v\in[0,1]$; this does not restore square
10\.

Put

$$
c=\frac{1-t^2}{1+t^2},\qquad s=\frac{2t}{1+t^2},\qquad
e=(c,s),\quad f=(-s,c),\quad u=c+s,\quad h=u/2.
$$

These are actual common orientations modulo quarter turns.
On this remainder, $c,s>0$; neither $c\ge s$ nor a reflection between the two intervals
is assumed. Squares 0–5 have basis $E=(1,0),F=(0,1)$, and squares 6–9 have basis $e,f$.
Their centers are exactly

$$
\begin{aligned}
C_0&=(1/2,1/2),&C_1&=(L-1/2,1/2),\\
C_2&=(z+1/2,L-1/2),&C_3&=(1/2,L-1/2),\\
C_4&=(3/2,L-1/2),&C_5&=(1/2,L-3/2),\\
C_6&=p,&C_7&=p+ae-f,\\
C_8&=p+e+bf,&C_9&=p+(a+1)e+(b-1)f.
\end{aligned}
$$

For each declared basis $(e_i,f_i)$, keep the source counterclockwise corner order

$$
V_{i,0}=C_i-(e_i+f_i)/2,\quad V_{i,1}=C_i+(e_i-f_i)/2,
$$

$$
V_{i,2}=C_i+(e_i+f_i)/2,\quad V_{i,3}=C_i+(-e_i+f_i)/2.
$$

The nine prescribed wall incidences remain: 0 left/bottom, 1 bottom/right, 2 top, 3
left/top, 4 top, and 5 left.
The six positive segments remain 3–4 and 3–5 of length one, 6–7 and 8–9 of length
$1-|a|$, and 6–8 and 7–9 of length $1-|b|$. The block lengths are at least $3/4$. For
ordered pairs $(3,4),(3,5),(6,7),(6,8),
(7,9),(8,9)$, the contact normals are respectively $+E,-F,-f,+e,+e,-f$. Additional
contacts, including the forced 4–5 point contact, are permitted.

For all $i=0,\ldots,9$, define

$$
H_i(n)=\tfrac12(|n\cdot e_i|+|n\cdot f_i|),\qquad
h_i=H_i(E)=H_i(F).
$$

Retain all **40** scalar containment inequalities

$$
h_i\le C_{i,x}\le L-h_i,\qquad h_i\le C_{i,y}\le L-h_i,
$$

and all **45** unordered pair clauses, separately for every $0\le i<j\le9$:

$$
\bigvee_{n\in\{e_i,f_i,e_j,f_j\},\ \sigma\in\{-1,1\}}
\left[\sigma(C_j-C_i)\cdot n\ge H_i(n)+H_j(n)\right].
$$

Each clause is a union of eight directed alternatives, with duplicate axes retained.
Equality is legal touching.
The inventory is 15 axis/axis pairs, 24 axis/block pairs and six block/block pairs.
No source-selected SAT direction, local theorem, stationarity or fixed-side substitution
enters this domain.

Deleting square 10 gives the necessary implication

$$
\pi(\mathcal R_{11})\subseteq\mathcal K^*,
$$

where $\mathcal R_{11}$ is the accepted closed eleven-square remainder and $\pi$ drops
$w,v$. Equality of these two sets is **not** asserted: an arbitrary skeleton may have no
square-10 extension.
All relations are closed, and the bounded parameter domain is compact.

The two block diagonals retain the complete conditions $(a\ge0\text{ or }b\le0)$ and
$(a\le0\text{ or }b\ge0)$, equivalently $ab\ge0$. Thus the two angle intervals crossed
with $a,b\ge0$ and $a,b\le0$ give four complete closed children.
Their slide-sign overlap is $a=b=0$; every zero-slide face and every $\pm1/4$ endpoint
remains. The four angle endpoints overlap previously excluded portions deliberately.
The original axis lifts and $c=s$ seam are already in the accepted complementary
coverage, not silently discarded.

## Inherited Lemmas and Their Limits

| Inherited implication | Exact reusable domain and restriction |
| --- | --- |
| $Lu\ge4$ | Every contained, interior-disjoint ten-square skeleton in this source geometry |
| $L\ge2+2/u$ | The six fixed axis squares plus four contained, interior-disjoint squares with one common angle; the block contact equations are unnecessary for this lemma |
| Individual cap depth $\delta_j\le(L-3)cs$, where $\delta_j=C_{j,y}+h-(L-1)$ | Each block square throughout the chart; the accepted argument treats axis endpoints separately |
| Only square 8 can have positive top cap, and $e\cdot p\ge u+1/2$ | Only the closed subdomain $c,s\ge1/4$, with the original short slides and full geometric conditions |
| Signed exclusions on $[0,1/24]$, $[2/5,1/2]$, $[23/25,1]$, plus the earlier $[1/3,2/5]$ | Accepted complementary coverage, including boundaries; no enlarged conclusion is inherited |

In particular, the old threshold comparisons do not supply the missing route.
At $L=96/25$, the audit gives $J-M=-7/325$ at $t=1/5$ and $J-K_5=-7/325$ at $t=2/3$.
Both points lie in this remainder.
They refute the angle-and-side-only positive-gap transfer, but specify no feasible
centers.
Even a complete ordering table would not repair these failures: those two scalar
controls already lie in the ordinary ordering regime.

## Exact Block Envelopes, Including Changed Extremal Labels

Write the two contact displacements as

$$
U=ae-f=(ac+s,as-c),\qquad V=e+bf=(c-bs,s+bc),
$$

and offsets $o_6=0,o_7=U,o_8=V,o_9=U+V$. Their exact coordinate envelopes are

$$
m_x=\min(0,U_x)+\min(0,V_x),\quad
M_x=\max(0,U_x)+\max(0,V_x),
$$

$$
m_y=\min(0,U_y)+\min(0,V_y),\quad
M_y=\max(0,U_y)+\max(0,V_y).
$$

Consequently block containment is exactly the closed translation rectangle

$$
T=[h-m_x,L-h-M_x]\times[h-m_y,L-h-M_y].
\tag{T}
$$

An inverted interval makes $T$ empty; a zero-width interval remains a closed fiber and
must be checked. The original $p$ box can be intersected explicitly; it is already
implied by the containment of square 6 and the side cap.

There are ten closed envelope chambers, rather than a globally fixed top square.
The table lists one valid extremal owner on each weak chamber.
At an equality, both adjacent chambers and all tied owners remain available.

| Angle and slide child | Additional weak signs | Left / right / bottom / top center |
| --- | --- | --- |
| Low angle, nonnegative slides | None | $6,9,7,8$ |
| Low angle, nonpositive slides | $U_x\ge0,V_y\ge0$ | $6,9,7,8$ |
| Low angle, nonpositive slides | $U_x\le0,V_y\ge0$ | $7,8,7,8$ |
| Low angle, nonpositive slides | $U_x\ge0,V_y\le0$ | $6,9,9,6$ |
| Low angle, nonpositive slides | $U_x\le0,V_y\le0$ | $7,8,9,6$ |
| High angle, nonpositive slides | None | $6,9,7,8$ |
| High angle, nonnegative slides | $V_x\ge0,U_y\le0$ | $6,9,7,8$ |
| High angle, nonnegative slides | $V_x\le0,U_y\le0$ | $8,7,7,8$ |
| High angle, nonnegative slides | $V_x\ge0,U_y\ge0$ | $6,9,6,9$ |
| High angle, nonnegative slides | $V_x\le0,U_y\ge0$ | $8,7,6,9$ |

Here low and high mean the two entire closed remainder intervals.
On the low interval $c\ge4/5,s\le3/5$; on the high interval $s\ge4/5,c\le3/5$. These
bounds and $|a|,|b|\le1/4$ fix the other increment signs in the table.
The formulas, not any numerical approximation to a crossing angle, define the chambers.
For the actual block corners, the corresponding coordinate extrema use corner 3 on the
left, 1 on the right, 0 at the bottom and 2 at the top.
No division by a slide, increment, or $c-s$ is used.

## Finite Alternative Obligations

The following is a complete grouped inventory, not a claim that its symbolic ordering
cases have already been solved.

| Group | Indexed inventory | Required alternatives or boundary obligation |
| --- | --- | --- |
| Axis/axis | All $0\le i<j\le5$: 15 pairs | All eight original alternatives, even where directions coincide; these depend only on $L,z$ |
| Retained block sides | $(6,7),(6,8),(7,9),(8,9)$ | Four complete pair clauses and their exact positive contact segments |
| Block diagonals | $(6,9),(7,8)$ | Both complete clauses; retain the exact sign split and its zero-slide boundaries |
| Axis/block | Each $i\in\{0,1,2,3,4,5\}$ with each $j\in\{6,7,8,9\}$: 24 pairs | Eight alternatives $\pm x,\pm y,\pm e,\pm f$, each with threshold $D=(1+c+s)/2$ |
| Translation bounds | Four block extrema, using (T) | Ten envelope chambers; empty, singleton and positive-width fibers |
| Collision interval endpoints | 24 pair slices | Three lower and three upper candidate endpoints, vertical entry/exit, every active-facet tie |
| Proposed fence | At most six intervals per fiber | Strict coverage of both closed endpoints and every link; distinct axis owners; all parameter and height seams |

The first four rows account for all $15+4+2+24=45$ pair clauses.
In the cross group, converting the eight-way clause to the complement of an open
collision set is exact; it does not choose a surviving source alternative.

## Proposed New Implication: A Six-Source Translation Fence

This route keeps the **joint translations of the complete contact block** instead of
transferring the failed individual $J-M$ or $J-K_5$ bounds.

Fix structural parameters $(L,z,a,b,t)$ in their full declared domains.
Retain the 15 axis clauses and six internal block clauses.
Let $Y$ be a height in (T), put $d_y=Y+o_{j,y}-C_{i,y}$, and set $D=(1+c+s)/2$. The
actual interiors of axis square $i$ and block square $j$ overlap precisely when all
eight signed projections are strictly below $D$. Thus their forbidden horizontal
translation interval is empty when $|d_y|\ge D$, and otherwise is

$$
I_{ij}(Y)=(\lambda_{ij}(Y),\rho_{ij}(Y)),
$$

$$
\lambda_{ij}=C_{i,x}-o_{j,x}
+\max\left(-D,\frac{-D-sd_y}{c},\frac{cd_y-D}{s}\right),
$$

$$
\rho_{ij}=C_{i,x}-o_{j,x}
+\min\left(D,\frac{D-sd_y}{c},\frac{cd_y+D}{s}\right).
\tag{I}
$$

An interval with $\lambda\ge\rho$ is empty.
These formulas divide only by the strictly positive $c,s$ of the closed remainder.
They are actual-square collision intervals, not cores, sampled angles, or relaxed LP
rows.

This gives an **exact translation/fiber equivalence**, separate from the proposed chain
bound below. For any fixed structural tuple satisfying the axis and internal clauses, a
point $p=(X,Y)$ completes the ten-square skeleton if and only if $p\in T$ and
$X\notin\bigcup_{i=0}^{5}\bigcup_{j=6}^{9}I_{ij}(Y)$. Containment is equivalent to (T),
while each omitted open interval is exactly the corresponding complete cross-pair SAT
clause. These account for every remaining condition.
Therefore skeleton emptiness is equivalent to covering every nonempty closed fiber, for
every such structural tuple, by the full union of 24 open intervals.
This representation is independently auditable progress even if the target allocation is
declined.

An unrestricted finite interval cover can be expressed as a strict overlapping chain
using at most 24 distinct intervals, with repeated axis-source labels allowed: start
with an interval containing the left endpoint and extend the rightmost covered point
until the right endpoint is included.
If extension failed, that point would be uncovered.
This is a completeness contract for the full interval union, not a tractability bound or
a proof that it covers any target fiber.

**Proposed sufficient strengthening, unproved:** for every such structural tuple with
nonempty (T), and every height $Y$ in its closed vertical interval, there exist
$1\le k\le6$ pairs $(i_r,j_r)$ with pairwise distinct axis indices $i_r$, whose nonempty
intervals satisfy, writing the closed horizontal fiber as $[l,r]$,

$$
\lambda_{i_1j_1}<l<\rho_{i_1j_1},\qquad
\rho_{i_qj_q}\le\rho_{i_{q+1}j_{q+1}},\quad
\lambda_{i_{q+1}j_{q+1}}<\rho_{i_qj_q}\quad(1\le q<k),
$$

$$
r<\rho_{i_kj_k}.
\tag{F}
$$

If (F) is proved uniformly, its open intervals cover the entire closed fiber.
Every permissible $p$ then overlaps at least one axis square, so
$\mathcal K^*=\varnothing$. This would complete the original source-family exclusion
together with the inherited complementary intervals.

The distinct-source, six-link requirement is a **specific sufficient strengthening**,
not an equivalent rewriting of skeleton emptiness.
The complete union of 24 forbidden intervals might cover a fiber only through a longer
chain or repeated axis owners.
Failure of (F) alone therefore neither proves nor refutes skeleton feasibility.
An exact point outside **all 24** open intervals, together with the other declared
conditions, does give an exact ten-square witness.
That branch has equal scientific value for deciding whether this skeleton can finish the
eleven-square argument.

## Tractability Gap and Reuse Boundary

There are 24 cross intervals, but only **12 row/block slice types**: four block offsets
against three axis heights, $1/2$, $L-1/2$ and $L-3/2$. The bottom row has axis indices
0 and 1; the top row has 3,4,2; the shoulder row has 5. Within each row, the formulas
differ by known horizontal translations.
This supplies a concrete way to group the geometry, with ten closed envelope chambers.

Each of those 12 types nevertheless has three competing lower and three competing upper
endpoint formulas. Vertical births, deaths and ties must also be covered.
Merely allowing every chain is not a small plan: there are
$\sum_{k=1}^{6}(6!/(6-k)!)4^k$ raw ordered distinct-source choices before endpoint-order
and height changes. No enumeration of those choices, no unexplained $8^{24}$ SAT search,
and no generic elimination engine is commissioned.

The missing admission evidence is a small, explicitly listed set of uniform chain
templates with bounded active-facet and height transitions, or another equally concrete
hand argument deciding the full domain.
Neither is supplied here.
The envelope table and exact interval representation alone do not show that thirty
minutes of target proof attention can resolve the remaining cases.
**Recommend admitting the domain and recording this changed candidate, while declining
the conditional target allocation at this checkpoint.** An independent admission must
assess the missing tractability premise rather than treating finite formulas as
readiness.

The nearby [closed polygon cover tool](../../../../../devtools/closed_polygon_cover.py)
is not an admitted consumer of (F). Its fixed-source closed-polygon endpoint chains
count tangencies as covered, use one exact number field, and have declared
polygon/vertex limits.
Here the forbidden intervals are **open**, and their endpoints vary with five structural
parameters.
Converting a strict gap to a closed polygon cover could erase legal touching.
The retained H124 axis `no_chain` outcome supplies neither these uniform templates nor a
refutation of this model.
No implementation or replay is proposed by this design.

## Controls and Distinct Decision Rules

- Reconstruct all ten indexed squares, four closed angle/sign children, 40 containment
  rows and 45 complete pair clauses.
  Refuse a selected SAT branch, fixed-side substitution, or a changed slide interval.
- Check all ten envelope chambers directly from $U,V$. At an increment equal to zero,
  retain both weak chambers and both extremal owners.
  Do not assume square 8 is highest outside the accepted $c,s\ge1/4$ subdomain.
- Retain the old mixed-sign overlap controls and the $a=b=0$ diagonal touching control.
  Retain the two negative scalar threshold differences; they must not be presented as
  geometric witnesses.
- Check the exact source Trump ten-square subconfiguration in its parent with $L\le4$.
  Its side $U>387/100>96/25$ refuses target membership.
  No source replay is rerun here, and the local theorem provides no new target
  exclusion.
- Preserve a feasible fiber endpoint: two axis unit squares in side two, centered at
  $(1/2,1/2)$ and $(3/2,1/2)$, touch legally.
  For the second center’s horizontal coordinate the forbidden interval is $(-1/2,3/2)$;
  its endpoint $3/2$ is feasible.
  This separate component control refuses closing the forbidden interval.
  It is not a member of the residual target’s angle chart.
- The same issue occurs at a link: $(0,1)$ and $(1,2)$ do not cover the point 1.
  Equality of adjacent endpoints cannot satisfy the strict link in (F). A singleton
  containment fiber also needs strict inclusion in some forbidden interval before it can
  be excluded.

**Complete exclusion:** an independent audit verifies a contradiction for all
$\mathcal K^*$, through (F) or another separately admitted complete argument.
The inherited complementary exclusions then finish this restricted source family, for
every original square-10 pose.
This is not a global representative, finite-motion theorem, unrestricted bound, or H120
adapter result.

**Exact ten-square witness:** give exact $(L,z,p_x,p_y,a,b,t)$ with unambiguous
algebraic roots where needed; reconstruct and check all 40 containment rows, 45 actual
SAT clauses, contact identities and parameter bounds.
This proves $\mathcal K^*\ne\varnothing$ and shows that these ten-square conditions
alone cannot exclude the eleven-square remainder.
It gives no eleven-square upper bound and does not assert an extension.

**Actual eleven-square witness:** additionally supply $w,v$, the four containment rows
of square 10 and its ten complete pair clauses.
Only the resulting 44/55 actual-square certificate can establish an eleven-square
packing; bound promotion still uses the existing verified-bound contract.

A failed six-source chain, a scalar control, a partial angular exclusion, or an
uncertified translation gap is inconclusive.
No smaller target is substituted after failure.

## Conditional Price and Receipt

Independent design admission is capped at **10 minutes** after this file freezes.
If a later design actually supplies the missing bounded templates or a different
admitted complete discriminator, a separately committed prospective protocol may price
**30 minutes for an author**, **25 minutes for an independent concurrent adversary**,
and **20 minutes for a fresh auditor** after both terminalize: at most 75 worker-minutes
and 50 minutes of mathematical critical path.
Writing and checks count within those caps.
Both complete exclusion and exact ten-square feasibility must be accepted exits.
No portion of that target price is spent or authorized by this design.

Actual first clock: **2026-09-07 17:21:00 UTC**. Mathematical freeze: **17:37:35 UTC**,
after 16 minutes 35 seconds.
Complete readback, six native link-target existence checks, the required footer check,
and the first installed Flowmark 0.4.0 format/check pass finished at **17:38:02 UTC**.
The final post-receipt format/check and terminal clock are reported to the coordinator
before the **17:40 UTC** hard stop.
Work was confined to exact domain transformation, obligation design and its readiness
limit. No missing chain inequality was attempted as a target proof.
No other BC-282 report was read; no numerical run, optimizer, adapter, code, shared
registry, Git, identifier or dependency change was made.
Only this assigned document was written.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
