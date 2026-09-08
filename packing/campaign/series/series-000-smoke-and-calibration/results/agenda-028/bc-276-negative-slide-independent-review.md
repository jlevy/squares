# BC-276: Independent Acceptance of the Negative-Slide Exclusion

The complete frozen $N$ is empty.
Both the [author’s argument](bc-276-negative-slide-author.md) and the
[adversary’s argument](bc-276-negative-slide-adversary.md) pass independent
reconstruction. Each contradicts necessary conditions of the declared ten-square
skeleton, uniformly over the closed domain, with final side margin

$$
\frac{4900}{1261}-\frac{96}{25}=\frac{1444}{31525}>0.
$$

Together with the
[accepted positive-child exclusion](bc-273-analytic-independent-review.md) and the
[reviewed identity](bc-276-negative-slide-domain-review.md) $S=T_+\cup N$, this proves
the entire declared signed short-slide parent $S$ empty.
The conclusion retains every square-10 angle, including both axis lifts, angle
coincidence and possible 9–10 recontact.
It does not cover other block-angle intervals, longer slides, different contact sides or
wall assignments, or an unrestricted packing problem.

This is the session092 phase-9 independent audit under the
[frozen protocol](bc-276-negative-slide-protocol.md).
Both reports were terminal before this audit began.
No decisive implication is rejected and no missing premise remains for the stated $N$ or
$S$ determination. Their explicitly rejected positive-slide transfers remain invalid;
neither accepted argument relies on them.

## Frozen Geometry and Exact Ranges

Write $\alpha=-a$, $\beta=-b$. The reviewed bounds are

$$
381/100\le L\le96/25,\quad 1/3\le t\le2/5,\quad 0\le v\le1,
\quad 0\le\alpha,\beta\le1/4,\quad 2\le z\le L-1,
\quad p,w\in[1/2,7/2]^2.
$$

All original center equations, containment and 55 complete weak SAT disjunctions remain
in the domain. The [source-feature definition](bc-273-release-domain-design.md) gives
$e=(c,s)$, $f=(-s,c)$, where $c=(1-t^2)/(1+t^2)$ and $s=2t/(1+t^2)$. Put $u=c+s$,
$h=u/2$, $D=h+1/2$, $A=e\cdot p$ and $B=f\cdot p$. The rational endpoint ranges are

$$
21/29\le c\le4/5,\quad 3/5\le s\le20/29,\quad
7/5\le u\le41/29,
\quad c>s>0,
$$

with $c^2+s^2=1$. The displayed derivatives in the reports have the required signs on
the whole interval. Consequently their coarse bounds $c\ge18/25$, $s\le7/10$,
$7/10\le h\le71/100$, $D\ge6/5$ and $cs\le1/2$ are valid.

The block equations independently reconstruct as

$$
\begin{aligned}
x_7&=p_x-\alpha c+s,& y_7&=p_y-\alpha s-c,\\
x_8&=p_x+c+\beta s,& y_8&=p_y+s-\beta c,\\
x_9&=p_x+(1-\alpha)c+(1+\beta)s,
&y_9&=y_8-\alpha s-c=y_7+s-\beta c.
\end{aligned}
$$

Containment gives $p_x\ge h$, $p_y\ge h+c+\alpha s$ and
$p_x\le L-h-(1-\alpha)c-(1+\beta)s$. The inequalities $s-\alpha c\ge2/5$ and
$s-\beta c\ge2/5$ remain valid at their extremal endpoints.

For every axis square and block square, the support sum is exactly $D$ on each of
$x,y,e,f$. Thus their eight directed projections have the same weak separating
threshold. A sign exclusion or a strict bound below $D$ removes a direction; a weak
inequality at $D$ remains legal.
This is the threshold used in both audits below.

## Cap Localization and the Author’s Square-6 Lemma

For square 8 put $\delta=y_8+h-(L-1)$ and $X=x_8+(c-s)/2$. If $\delta>0$, then

$$
X\le L+\alpha c-2s\le71/25<3\le z+1,
$$

using $x_9=x_8+s-\alpha c\le L-h$. The occupied top rectangles are $[0,2]\times[L-1,L]$
and $[z,z+1]\times[L-1,L]$. Its nonempty open interior cap in $L-1<y<L$ is convex.
Openness rules out points on vertical obstacle boundaries and the shared seam between
squares 3 and 4, since a neighborhood would enter an obstacle interior.
Connectedness therefore confines the cap to one free strip.
The bound on its apex excludes the right strip and puts the cap in $2<x<z$.

The two descending edges have horizontal components of opposite signs.
Interior points just below the apex occur on both sides of $X$, so $2<X<z$, including a
top-wall apex. At depth $s$ its section width is $1/c\ge5/4$, larger than the gap
$z-2\le21/25$. Hence $\delta>s$ is impossible; when $\delta=s$, shallower sections
approaching that depth already violate the same width bound.
Thus $0<\delta<s<c$, and taking section limits gives the weak base inequalities

$$
X-c\delta/s\ge2,\qquad X+s\delta/c\le z,
\qquad \delta\le cs(z-2)\le21/50.
$$

These preserve bottom-corner touching.
The exact coordinate identities are

$$
sX-c\delta=cL-c-1/2-(B-\beta),\qquad
cX+s\delta=A+3/2-sL+s.
$$

In particular, with $M=cL-c-2s-1/2$ and $P=u(L-1)-3/2$, the positive cap implies
$B-\beta\le M$ and $A\le cz+sL-s-3/2\le P$. The $\beta$ terms cancel in the right
identity; they have the displayed negative sign in the left one.

The author’s additional lemma is also correct.
If square 6 had positive depth $\delta_6=p_y+h-(L-1)$ and apex abscissa
$X_6=p_x+(c-s)/2$, then

$$
\delta=\delta_6+s-\beta c>\delta_6>0,
\qquad X-X_6=c+\beta s>0.
$$

Its apex is left of square 8’s, so its open cap also lies in the central free strip.
Both caps are triangular.
Comparing square 6’s left base endpoint with square 8’s right base endpoint gives

$$
z-2\ge (X-X_6)+(s/c)\delta+(c/s)\delta_6
=\frac1c+\frac{\delta_6}{cs}>\frac54>\frac{21}{25},
$$

a contradiction. The cancellation of $\beta s$ in this identity is exact.
Thus $p_y\le L-1-h$. The equality $\delta_6=0$ remains included.
The bound $\delta\le21/50$ now holds in all cases: it was proved for a positive cap and
is automatic for $\delta\le0$. There is no circular use of a conditional height bound.

The cap arguments use actual interior nonoverlap with the top-row squares, so they cover
all possible SAT directions for those pairs.
They do not substitute selected source normals or a closed forbidden-polygon cover.

## The Author’s Complete SAT Reductions

Put $J=3/2+u-sL$ and $K_5=cL-2c-s-1/2$. Their exact gap obeys

$$
J-K_5=2+3c+2s-Lu
\ge2-(21/25)c-(46/25)s\ge1/25>0.
$$

For pair 5–6, write its displacement as $(X_0,-Z)$, where $X_0=p_x-1/2$ and
$Z=L-3/2-p_y$. The newly proved height bound and containment give $1/5\le X_0\le3/2$ and
$1/5\le Z\le23/25$. Both vertical directions fail, as do negative $x$ and positive $f$.
The other screened bounds are

$$
cX_0-sZ\le(4/5)(3/2)-(3/5)(1/5)=27/25<D,
$$

$$
sZ-cX_0\le(7/10)(23/25)-(18/25)(1/5)=1/2<D.
$$

Thus exactly the two retained possibilities are positive $x$ or negative $f$:
$p_x\ge h+1$ or $B\le K_5$.

For pair 1–9 use displacement $(-\xi_9,Y_9)$, with $\xi_i=L-1/2-x_i$ and $Y_i=y_i-1/2$.
The exact coarse bounds are $1/5\le\xi_9\le3/2$ and $3/5\le Y_9\le67/50$. The latter
upper bound follows from $y_9\le L-1-h+21/50-c\le46/25$. Both $e$ directions fail by

$$
c\xi_9-sY_9\le21/25<D,
\qquad sY_9-c\xi_9\le397/500<D.
$$

Positive $x$, negative $y$ and negative $f$ fail by sign.
Horizontal-left separation implies positive $f$, because

$$
s\xi_9+cY_9-D\ge c(2s-1-\beta c)\ge0
\quad\text{when }\xi_9\ge D.
$$

The last factor may be zero and has not been treated as positive.
The complete disjunction therefore gives $B-\beta\ge J$ or $Y_9\ge D$.

In the upward case $Y_9\ge D$, pair 1–7 has $Y_7\ge D-s+\beta c$ and $Y_7\le23/25$. Its
displacement is $(-\xi_7,Y_7)$ with positive magnitudes.
Positive $x$, negative $y$ and negative $f$ fail by sign.
Positive $y$ fails by the height bound, and positive $e$ is at most $sY_7\le161/250<D$.
The remaining horizontal-left alternative implies

$$
s\xi_7+cY_7\ge sD+c(D-s+\beta c)=D+\beta c^2\ge D.
$$

The remaining negative-$e$ alternative gives

$$
s\xi_7+cY_7\ge\frac{sD+Y_7}{c}
\ge D+\frac{s^2+\beta c}{c}>D.
$$

Here the identity $D(1+s-c)-s=s^2$ checks exactly.
Thus both imply positive $f$, which is also the final direct alternative.
Every pair 1–7 choice in this upward case gives $B\ge J$.

Combining the two possibilities for pair 1–9 proves $B\ge J$ throughout $N$. Since
$J>K_5$, pair 5–6 must then give $p_x\ge h+1$. Every direction of all three pair
disjunctions has been accounted for.

## Both Final Side Inequalities

If $\delta>0$, the right cap row gives $A\le P$, while $cA=p_x+sB\ge h+1+sJ$.
Substitution yields

$$
L(1+cs)\ge(1+u)^2=2+2u+2cs.
$$

If $\delta\le0$, then $y_9\le L-1-h-c\le71/50$, so the upward pair 1–9 alternative is
impossible and $B-\beta\ge J$. From $p_x\ge h+1$ and square-7 containment,

$$
A\ge c(h+1)+s(h+c+\alpha s)
=u+1/2+s(2c-1)+\alpha s^2\ge u+1/2.
$$

The below-top condition and exact identity give $p_y-\beta c=sA+c(B-\beta)\le L-1-h-s$.
Substitution again gives the same side inequality.
This case includes $\delta=0$.

Since $cs=(u^2-1)/2$, each case requires

$$
L\ge2+\frac{2u}{1+cs}
=2+\frac{4u}{1+u^2}\ge\frac{4900}{1261}.
$$

The function $u/(1+u^2)$ decreases on the actual range $u>1$, so its minimum is at
$41/29$. The exact margin over $96/25$ is $1444/31525$. This completes an accepted
contradiction for the whole frozen $N$ using the author’s route.

## Independent Check of the Adversary’s Route

The adversary’s proof also passes on its own premises.
Under its temporary assumption $\delta\le21/50$, its exact sharper common bound is

$$
X_0,\xi_9\le4341/2900,
\qquad c\xi_9\le4341/3625<6/5.
$$

The first fraction comes from $L-h-3c/4-s\le5791/2900$, followed by subtracting $1/2$.
The strict second comparison has margin $9/3625$. Its conditional estimates
$p_y\le54/25$, $3/20\le Z\le23/25$, $Y_7\le47/50$, and $Y_9\le67/50$ are valid; the
lower $Z$ bound uses the declared lower side endpoint $381/100$.

With $F_0=K_5$, $E_0=c+1/2+s(L-1)$ and $Q=cL-c-1/2$, its complete screening leaves three
possibilities for pair 5–6: $R:p_x\ge h+1$, $E_5:A\ge E_0$ and $F_5:B\le F_0$. Pair 1–9
leaves $B-\beta\ge J$ or $V:Y_9\ge D$. Pair 1–7 leaves $H_7:x_7\le L-1-h$,
$E_7:A-\alpha\le Q$ and $F_7:B\ge J$. The discarded signs and projections use the same
threshold $D$; its stated bounds $161/250$, $469/500$, $47/50$ and $329/500$ are all
strictly below that threshold.
Retaining the extra positive-$e$ possibility for pair 5–6 is a valid larger case list.

In the below-top case, $V$ fails, $F_5$ conflicts with $B-\beta\ge J$, and each of
$R,E_5$ implies $A\ge u+1/2$. The same side contradiction follows.
In the positive-cap case, cap localization independently proves the assumed height bound
and gives $B-\beta\le M$ and $A\le P$. The checked gaps $J-M\ge2/87$ and $M-F_0=c-s>0$
force $V$, hence

$$
p_y\ge h+1+c-s+\alpha s+\beta c.
$$

Also $E_0-P=2-c(L-2)>0$ excludes $E_5$. The six remaining combinations check as follows:

- $F_5,F_7$ contradict $J>F_0$ directly.
- $F_5,H_7$ gives the geometric projection bound $D-\beta s^2$, which correctly
  translates to $B\ge J+\beta c^2>F_0$. It is never promoted to a separating threshold.
- $F_5,E_7$ gives $p_y\le cu(L-2)-h+\alpha s$. Comparison with the lower height cancels
  $\alpha s$ and requires $cu(L-2)\ge1+2c+\beta c$. Its left side is at most $12/5$,
  whereas its right side is at least $61/25$.
- $R,E_7$ requires $c(L-2)\ge1+2cs-\alpha c^2$. The left side is at most $184/125$ and
  the right side at least $213/125$.
- $R,F_7$ gives the already checked inequality $cP\ge h+1+sJ$ and the final side
  contradiction.
- $R,H_7$ gives the two inequalities used in the adversary’s final elimination below.

For that last case the independently reconstructed inequalities are

$$
\alpha c\ge2+c+2s-L,
\qquad
\alpha s^2+\beta cs\le uL-2u-2-2cs+s^2.
$$

Multiplying the first by $s^2$ and the second by $c$ bounds the same $\alpha cs^2$ from
below and above. Rearrangement gives

$$
L(cu+s^2)\ge
2cu+2c+2c^2s+2s^2+2s^3+\beta c^2s
=2+2u+2cs+\beta c^2s.
$$

Here $cu+s^2=1+cs$. The last term is nonnegative, so this is again the same impossible
side bound. No slide was divided out, and $\alpha=0$ or $\beta=0$ creates no missing
case. This validates the adversary’s equation (17), including its sign.

The two reports therefore agree without needing to combine unfinished arguments.
The author uses an additional geometric height lemma to obtain a smaller SAT case list;
the adversary resolves the larger list by explicit alternatives.
Both lists cover all necessary choices on their respective established premises.

## Failed Transfers, Closed Coverage and Unused Premises

The rejected implications are correctly scoped.
At the adversary’s displayed scalar values, $M=143/250$, $J=149/250$, $\beta=1/4$ and
$B=3/5$, the inequality $B-\beta\le M$ holds while $B>J$. This refutes only that
isolated transfer, not a packing claim.
The bound $D-\beta s^2$ need not reach $D$; both accepted proofs retain the deficit or
use a different pair row.

The author’s failed hand proposal is also correctly rejected.
Its pair 5–6 has absolute projections $9/10,6/25,72/125,183/250$, each below $D=6/5$.
One overlapping pair is sufficient to refuse the proposed skeleton.
Neither report asserts a feasible ten-square or eleven-square witness.

The cap cases exhaust $\delta\le0$ and $\delta>0$, with the shared equality retained in
the first. The proof includes both slide endpoints, their zero intersection, both
block-angle endpoints, all variable sides in the interval, $z=2$ and $z=L-1$, top-wall
touching, weak cap-base contacts and newly formed contacts.
Every denominator used is positive, including $c$, $s$, $1+cs$, $1+t^2$ and $1+u^2$;
there is no division by a slide or an angle difference.
The local theorem, numerical coordinates and source SAT labels are not used.

The actual necessary subset uses the prescribed centers of axis squares 1–5, the
retained block equations for 6–9, their needed containment, the top-row obstacle
nonoverlap, and the three complete SAT conditions audited above.
Conditions involving squares 0 and 10 are not used in the contradiction.
This records the proof’s dependencies within the frozen domain.
It does not announce an unrestricted nine-square impossibility, delete wall assignments,
or enlarge any parameter range.
A differently defined theorem requires its own explicit domain and implication review.

In particular, every full $N$ configuration would project into this inconsistent
necessary subset. Unused pairs cannot restore its feasibility.
Thus $N=\varnothing$ for every admitted $v,w$, including all square-10 orientations
modulo quarter turns, equal angles and 9–10 recontact.
All original 55 disjunctions remain in the definition; checking unused disjunctions is
unnecessary for this contradiction.

For the signed parent $S$, the two block diagonals give

$$
(a\ge0\lor b\le0)\land(a\le0\lor b\ge0),
$$

equivalently $ab\ge0$ on $[-1/4,1/4]^2$. Therefore every $S$ point belongs to the closed
positive or negative child, with each one-zero boundary included and their intersection
at $a=b=0$. The previously accepted $T_+=\varnothing$ and the present $N=\varnothing$
prove exactly $S=\varnothing$.

The fixed source-feature chart and selected block-angle and short-slide ranges remain
essential scope restrictions.
Other block angles, longer or degenerating segments, different wall/contact patterns, a
global representative theorem, an unrestricted packing bound and H118’s
resource-versus-LP comparison remain outside this acceptance.
BC261 instrument readiness does not follow from this mathematical audit.

## Work Receipt

The prospective phase-9 lease was `2026-09-07T09:21:54Z` through `2026-09-07T09:41:54Z`.
The first clock read after dispatch was `2026-09-07T09:23:30Z`. Both terminal reports
were read, followed by the frozen protocol, the domain review, original feature
equations and prior positive acceptance.
The audit reconstructed the cap geometry, exact coarse bounds, all decisive SAT choices
and algebraic identities by hand.
No target computation, numerical solver, target script or new witness search ran.

Only this assigned review was written.
No author report, shared record, Git state, identifier or dependency was changed.
The document received the common-guidelines and de-slop passes and installed Flowmark
0.4.0 with caching disabled.

The mathematical audit, full formatted reread and initial document checks completed at
`2026-09-07T09:32:20Z`, 8 minutes 50 seconds after the first clock read and 9 minutes 34
seconds before the hard deadline.
Flowmark’s full auto-format check passed; all six linked files existed; no trailing
whitespace was found; the required footer appeared once; and the equations survived
formatting. A final scoped formatting check follows this receipt before delivery.
No background command remains.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
