# BC-276: Independent Negative-Slide Adversary

**Candidate result for independent audit: the entire frozen $N$ is empty.** The argument
excludes its ten-square skeleton using containment, the occupied top row and the
complete SAT alternatives for pairs 5–6, 1–7 and 1–9. It uses no parameter or condition
involving square 10. This is an independently produced analytical argument, not an
accepted campaign determination.

The scope is exactly the [prospective protocol](bc-276-negative-slide-protocol.md),
[accepted domain review](bc-276-negative-slide-domain-review.md) and
[complete allocation domain](bc-275-first-checkpoint-allocation.md).
No source SAT assignment, sampled angle, numerical computation or solver is used.
The adversary did not read the author report or exchange mathematical reasoning with its
author. Interim claims were sent only to the coordinator with an explicit independence
request.

## Notation and Uniform Bounds

Put $\alpha=-a$, $\beta=-b$, so $0\le\alpha,\beta\le1/4$. Use the exact basis $e=(c,s)$,
$f=(-s,c)$ specified by $t$, and write

$$
u=c+s,\qquad h=u/2,\qquad D=h+1/2,\qquad
A=cp_x+sp_y,\qquad B=-sp_x+cp_y.
$$

On the whole closed angle interval,

$$
\frac{21}{29}\le c\le\frac45,\quad
\frac35\le s\le\frac{20}{29},\quad
\frac75\le u\le\frac{41}{29},\quad c>s>0,\quad c^2+s^2=1.
$$

For the coarse estimates below, also use $c\ge18/25$, $s\le7/10$ and $h\ge7/10$. These
follow from the displayed exact ranges.
The function $u=(1+2t-t^2)/(1+t^2)$ increases on $[1/3,2/5]$, since its derivative has
the sign of $1-2t-t^2>0$. Thus the endpoints give the stated range without fixing the
angle.

For an axis unit square and a unit square in this oblique basis, the support sum along
each candidate SAT axis $x,y,e,f$ is exactly $D$. Consequently nonoverlap means that at
least one of the four absolute center projections is at least $D$. Equality is legal
throughout this proof.

The component equations become

$$
\begin{aligned}
x_7&=p_x-\alpha c+s,&y_7&=p_y-\alpha s-c,\\
x_8&=p_x+c+\beta s,&y_8&=p_y+s-\beta c,\\
x_9&=x_7+c+\beta s,&y_9&=y_8-\alpha s-c=y_7+s-\beta c.
\end{aligned}
$$

Containment gives $p_x\ge h$, $p_y\ge h+c+\alpha s$ and $x_9\le L-h$. Since
$x_9-p_x\ge3c/4+s$, define

$$
X_6=p_x-1/2,\qquad
\xi_i=L-1/2-x_i,\qquad Y_i=y_i-1/2\quad(i=7,9).
$$

Then

$$
\frac15\le X_6,\xi_9\le\frac{4341}{2900},\qquad
\xi_7=\xi_9+c+\beta s>0,\qquad Y_7\ge\frac15,\quad Y_9\ge\frac35.
\tag{1}
$$

For the common upper bound, both $p_x$ and $L-x_9$ are at most $L-h-3c/4-s\le5791/2900$.
For $Y_9$, use $y_9\ge h+s-\beta c\ge11/10$. In particular,

$$
c\xi_9\le\frac{4341}{3625}<\frac65\le D.
\tag{2}
$$

The strict rational estimate in (2) avoids dropping a possible SAT equality by rounding
a bound to $6/5$.

Define the following rows and the protrusion depth:

$$
\begin{aligned}
k&=u+1/2,&J&=3/2+u-sL,\\
M&=cL-c-2s-1/2,&F_0&=cL-2c-s-1/2,\\
E_0&=c+1/2+s(L-1),&Q&=cL-c-1/2,\\
P&=u(L-1)-3/2,&\delta&=y_8+h-(L-1).
\end{aligned}
$$

Two exact comparisons will be used repeatedly:

$$
J-M\ge\frac{96t^2-42t+4}{25(1+t^2)}\ge\frac2{87}>0,
\qquad M-F_0=c-s>0.
\tag{3}
$$

The first bound uses $L\le96/25$. With $d=t-1/3\ge0$, its numerator is
$2/3+22d+96d^2\ge2/3$, and its denominator is at most 29. Also, put

$$
\Lambda=2+\frac{2u}{1+cs}
=2+\frac{4u}{1+u^2}
\ge\frac{4900}{1261}>\frac{96}{25}.
\tag{4}
$$

The middle expression decreases for $u>1$, so the lower bound follows at $u=41/29$. Its
strict excess over $96/25$ is $1444/31525$.

## Complete SAT Reductions Under a Height Bound

For this section only, suppose $\delta\le21/50$. This assumption will hold in both cases
considered below. It gives

$$
p_y\le\frac{54}{25},\qquad
\frac3{20}\le Z:=L-3/2-p_y\le\frac{23}{25},\qquad
Y_7\le\frac{47}{50},\qquad Y_9\le\frac{67}{50}.
\tag{5}
$$

For $p_y$, use $p_y=L-1-h+\delta-s+\beta c$. The lower bound on $Z$ uses $L\ge381/100$;
its upper bound uses $p_y\ge h+c$. For $Y_7$, subtract $\alpha s+c+1/2$ from the bound
on $p_y$. For $Y_9$, use $y_9=L-1-h+\delta-\alpha s-c$.

**Pair 5–6.** Its center difference is $(X_6,-Z)$, with both displayed quantities
positive. The $y$ alternatives fail because $Z\le23/25<D$. The negative $e$ alternative
fails because $sZ-cX_6\le sZ\le161/250<D$. The $f$ projection is negative, and the $x$
projection is positive.
Thus its complete disjunction leaves only

$$
R:\ p_x\ge h+1,
\qquad
E_5:\ A\ge E_0,
\qquad
F_5:\ B\le F_0.
\tag{6}
$$

These are respectively the positive $x$, positive $e$ and negative $f$ alternatives,
obtained from the exact square-5 center $(1/2,L-3/2)$.

**Pair 1–9.** Its center difference is $(-\xi_9,Y_9)$ with both magnitudes positive.
Both $e$ alternatives fail: the absolute $e$ projection is at most
$\max(c\xi_9,sY_9)<D$, by (2) and $sY_9\le469/500$. The $f$ projection is positive.
If the leftward $x$ alternative holds, then

$$
s\xi_9+cY_9
\ge sD+c(h+s-\beta c-1/2)
=D+c(2s-1-\beta c)\ge D,
\tag{7}
$$

because $2s-1-\beta c\ge6/5-1-1/5=0$. Thus that alternative also implies positive $f$
separation. All its surviving alternatives imply either

$$
B-\beta\ge J
\qquad\text{or}\qquad
V:\ y_9\ge h+1.
\tag{8}
$$

The second alternative is exactly upward $y$ separation.
Neither it nor the equality case in (7) has been discarded.

**Pair 1–7.** Its center difference is $(-\xi_7,Y_7)$. The $y$ alternatives fail by
$Y_7\le47/50<D$, and positive $e$ separation fails since $-c\xi_7+sY_7\le329/500<D$. The
$f$ projection is positive.
Its complete disjunction therefore leaves only

$$
H_7:\ x_7\le L-1-h,
\qquad
E_7:\ A-\alpha\le Q,
\qquad
F_7:\ B\ge J.
\tag{9}
$$

These are leftward $x$, negative $e$ and positive $f$ separation, respectively.

## Square 8 Must Protrude

Suppose first that $\delta\le0$. The conditional bounds and reductions above apply.
The stronger bound $y_9\le L-1-h-c\le71/50$ gives $Y_9\le23/25<D$, so pair 1–9 cannot
use $V$. Equation (8) forces $B-\beta\ge J$.

In (6), $F_5$ is consequently impossible, since $B\ge J+\beta>F_0$ by (3). Alternative
$E_5$ implies $A\ge k$ because $E_0-k=s(L-2)>0$. Alternative $R$ also implies $A\ge k$:
containment of square 7 gives

$$
A\ge c(h+1)+s(h+c+\alpha s)
=k+s(2c-1)+\alpha s^2\ge k.
$$

Finally,

$$
sA+c(B-\beta)=p_y-\beta c\le L-1-s-h.
$$

Combining this with $A\ge k$ and $B-\beta\ge J$ yields $(1+cs)L\ge2+2u+2cs$, or
$L\ge\Lambda$. Equation (4) contradicts the side cap.
Hence

$$
\delta>0.
\tag{10}
$$

## The Open Cap and Its Weak Base Rows

Let $(X,y_8+h)$ be square 8’s highest vertex, where $X=x_8+(c-s)/2$. Since
$x_9=x_8-\alpha c+s\le L-h$,

$$
X\le L+\alpha c-2s\le\frac{71}{25}<3\le z+1.
\tag{11}
$$

The interior of square 8 above $y=L-1$ is a nonempty open convex cap.
Containment puts its interior below $y=L$ and inside $0<x<L$. Squares 3 and 4 occupy
$[0,2]\times[L-1,L]$, while square 2 occupies $[z,z+1]\times[L-1,L]$. An interior cap
point on an obstacle boundary or the shared seam $x=1$ would have an open neighborhood
penetrating an obstacle.
Connectedness therefore puts the cap in one of $2<x<z$ and $z+1<x<L$. Interior points
approach its highest vertex, so (11) excludes the right strip.
The cap lies entirely in $2<x<z$.

The highest vertex has descending edges $-e$ and $-f$. At a small positive depth below
it, interior points occur on both sides of $X$. Thus $2<X<z$, including when the highest
vertex is on the container’s top wall.
Empty-gap endpoints $z=2$ or $z+1=L$ create no additional open component.

At depth $s$ below the highest vertex, the horizontal section has width $1/c\ge5/4$,
larger than the gap $z-2\le L-3\le21/25$. If $\delta>s$, that section lies within the
top strip. If $\delta=s$, sections at depths just less than $s$ already exceed the gap
while lying strictly above its lower boundary.
Therefore $0<\delta<s<c$. The cap is triangular, and its limiting section at $y=L-1$ has
endpoints $X-c\delta/s$ and $X+s\delta/c$. Consequently

$$
X-\frac cs\delta\ge2,\qquad
X+\frac sc\delta\le z,\qquad
\delta\le cs(z-2)\le\frac{21}{50}.
\tag{12}
$$

These are weak base inequalities: bottom-corner touching at $y=L-1$ is legal.
No closed forbidden polygon is counted as an interior cover.
All denominators are positive.

Substitution of the center equations gives the exact rows

$$
B-\beta\le M,
\qquad
A\le cz+sL-s-3/2\le P.
\tag{13}
$$

For example, $sX-c\delta=cL-c-1/2-(B-\beta)$ and $cX+s\delta=A+3/2-sL+s$. This also
verifies both sign changes introduced by the negative slides.
The height assumption used in (5)–(9) is now proved in the remaining case.

By (3), (8) and (13), pair 1–9 must use $V$. Equivalently,

$$
p_y\ge h+1+c-s+\alpha s+\beta c.
\tag{14}
$$

Alternative $E_5$ in (6) is impossible because $E_0-P=2-c(L-2)>0$. Indeed
$c(L-2)\le184/125<2$. It remains to exclude $F_5$ and $R$ against the three complete
alternatives (9).

## Case $F_5$: $B\le F_0$

Alternative $F_7$ contradicts $J>F_0$ immediately.

Under $H_7$, the identity $x_9=x_7+c+\beta s$ gives $\xi_9\ge D-c-\beta s$. Together
with $V$, this implies

$$
s\xi_9+cY_9\ge s(D-c-\beta s)+cD=D-\beta s^2.
$$

Since $s\xi_9+cY_9=B-\beta-1+sL-h$, the last inequality gives
$B\ge J+\beta c^2\ge J>F_0$, another contradiction.
This is a geometric lower bound; it does not incorrectly promote $D-\beta s^2$ to a
separating threshold $D$.

Under $E_7$, the identity $p_y=sA+cB$ gives

$$
p_y\le s(Q+\alpha)+cF_0=cu(L-2)-h+\alpha s.
$$

Comparing with (14) cancels $\alpha s$ and requires

$$
cu(L-2)\ge1+2c+\beta c.
$$

This is impossible: the left side is at most $(4/5)(3/2)2=12/5$, while the right side is
at least $1+36/25=61/25>12/5$. Here $u\le41/29<3/2$ and $L-2\le46/25<2$ justify the
coarser upper bound.
All three alternatives have failed.

## Case $R$: $p_x\ge h+1$

Alternative $E_7$, together with square-7 containment, would require

$$
\begin{aligned}
Q&\ge A-\alpha
\ge c(h+1)+s(h+c+\alpha s)-\alpha\\
&=1/2+c+2cs-\alpha c^2,
\end{aligned}
$$

or $c(L-2)\ge1+2cs-\alpha c^2$. Its left side is at most $184/125$, while its right side
is at least $1+2(18/25)(3/5)-(1/4)(4/5)^2=213/125$. Thus $E_7$ fails.

Under $F_7$, $cA=p_x+sB\ge h+1+sJ$. With $A\le P$, this yields

$$
(1+cs)L\ge2+2u+2cs,
$$

again requiring $L\ge\Lambda$, contrary to (4).

It remains to consider $H_7$. Combining $x_7=p_x+s-\alpha c$ with $R$ gives

$$
\alpha c\ge2+c+2s-L.
\tag{15}
$$

Combining $R$, (14) and $A\le P$ gives

$$
\begin{aligned}
A&\ge c(h+1)+s(h+1+c-s+\alpha s+\beta c)\\
&=1/2+u+2cs-s^2+\alpha s^2+\beta cs,
\end{aligned}
$$

and hence

$$
\alpha s^2+\beta cs\le uL-2u-2-2cs+s^2.
\tag{16}
$$

Multiply (15) by $s^2$, multiply (16) by $c$, and eliminate $\alpha cs^2$. Using
$c^2+s^2=1$ gives

$$
(1+cs)L\ge2+2u+2cs+\beta c^2s.
\tag{17}
$$

Because $\beta\ge0$, (17) also requires $L\ge\Lambda$. This excludes the final
alternative. No division by either slide was used.

## Failed Transfers, Scope and Audit Obligation

The positive-slide proof cannot simply be relabeled.
For instance, $B-\beta\le M$ does not imply $B<J$: at $L=96/25$, $t=1/3$ and
$\beta=1/4$, one has $M=143/250$, $J=149/250$, and the scalar value $B=3/5$ satisfies
the former inequality and exceeds $J$. This is a counterexample to that isolated
implication, not a proposed packing.
Likewise the geometric bound $D-\beta s^2$ is generally below $D$. The two cases above
preserve that term and use a different opposing row.

The argument has excluded both $\delta\le0$ and $\delta>0$ using necessary conditions of
every point in $N$. All rejected SAT alternatives have strict bounds below $D$; every
surviving alternative is retained with weak equality.
This includes $\alpha=0$, $\beta=0$, their intersection, the angle endpoints, top-wall
touching, cap-base contacts and the complete side interval.
No ten-square or eleven-square feasible witness is claimed.

If the independent reader accepts every step, the contradiction excludes the whole
ten-square projection and therefore every square-10 center, angle $v\in[0,1]$,
equal-angle pose and allowed 9–10 recontact.
The other pair conditions cannot repair an impossible subset of necessary conditions.
Together with the separately accepted positive child, this would exclude the declared
signed short-slide parent $S$. No wider angle range, longer-slide family, changed
contact sides or global packing bound follows.

The required independent audit should check the conditional height bounds, all three SAT
reductions, cap localization with legal equality, both coordinate identities in (13),
and the elimination in (17). A failed implication leaves the determination unresolved;
the candidate result is not self-certified by this report.

## Timing and Checks

The prospective phase-8 lease began at 09:00:45 UTC on 2026-09-07, with hard delivery at
09:20:45 UTC. The adversary’s actual first clock read and start were 09:01:45 UTC. The
protocol, accepted domain review and allocation were read before target analysis.
No author report, numerical target, solver, one-off target script or scientific
measurement tool was used.
All calculations above are exact symbolic derivations.
Only this assigned report was written; no code, registry, Git state, identifier or
dependency was changed.

The mathematical derivation and full draft were complete by 09:19:22 UTC, 17 minutes 37
seconds after the actual start.
The report preserves the failed transfer and every remaining acceptance obligation.
Installed Flowmark 0.4.0 formatted it and passed the initial check with caching disabled
by 09:19:39 UTC; the final receipt receives the same scoped check before delivery.
No background command remains.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
