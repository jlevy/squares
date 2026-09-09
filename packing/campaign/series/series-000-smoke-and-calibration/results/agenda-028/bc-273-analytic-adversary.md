# BC-273 — Independent Analytical Adversary

**Candidate result for independent audit: the entire frozen $T_{\rm mid}$ is empty.**
The argument below excludes its ten-square skeleton already.
It checks the relevant complete SAT alternatives, including legal equality, rather than
selecting the source’s separations.
Its decisive inequality has rational margin at least $2/87$. This is a proposed
analytical proof, not an independently accepted campaign verdict.

The scope is exactly the
[frozen analytical protocol](bc-273-analytic-release-protocol.md), its ten parameters,
and the [accepted source-feature design](bc-273-release-domain-design.md).
All 55 pair disjunctions, containment, retained segments, walls, variable side and
recontacts remain in the target.
Using a subset of these conditions for a contradiction does not remove any defining
condition.
The argument does not use the parameters of square 10, so no assumption on its
cavity, orientation or contact with square 9 enters.

The adversary worked independently of the author.
No numerical search, solver, one-off target script, target sample or coordinate fitting
computation was used.
Exact arithmetic below is a hand derivation.
The coordinator received interim claims for the later audit, with an explicit request
not to forward them to the author during the independent attempt.

## Notation and Bounds

Use $c=c(t)$, $s=s(t)$, $e=(c,s)$ and $f=(-s,c)$ from the design, and put

$$
u=c+s,\qquad h=u/2,\qquad D=h+1/2,\qquad
A=e\cdot p,\quad B=f\cdot p.
$$

Here $D$ is the support sum between an axis unit square and a square of the oblique
component along **each** of their four candidate SAT directions $x,y,e,f$. Thus their
exact nonoverlap condition is that at least one of the four absolute projections of
their center difference is at least $D$.

Throughout the unchanged target,

$$
L\le96/25,\quad 1/3\le t\le2/5,\quad 0\le a,b\le1/4,\quad
2\le z\le L-1,
$$

and the following rational bounds hold:

$$
\frac{18}{25}\le c\le\frac45,\quad
\frac35\le s\le\frac7{10},\quad
\frac7{10}\le h\le\frac{71}{100},\quad c>s>0,\quad c^2+s^2=1.
$$

The exact endpoint ranges are $21/29\le c\le4/5$ and $3/5\le s\le20/29$. Also
$7/5\le u\le41/29$: the derivative of $(1+2t-t^2)/(1+t^2)$ has the sign of $1-2t-t^2$,
positive on the declared interval.
The coarser bounds above keep the SAT screening arithmetic short.

Write $x_i,y_i$ for the center coordinates.
The retained equations give

$$
\begin{aligned}
x_7&=p_x+ac+s,&y_7&=p_y+as-c,\\
x_8&=p_x+c-bs,&y_8&=p_y+s+bc,\\
x_9&=x_7+c-bs=x_8+ac+s,&y_9&=y_7+s+bc=y_8+as-c.
\end{aligned}
$$

Containment and the nonnegative slide bounds imply

$$
\frac7{10}\le p_x\le\frac{197}{100},\qquad
p_y\ge\frac{249}{200},\qquad
x_9\ge\frac{187}{100},\qquad y_9\ge\frac{13}{10}.
\tag{1}
$$

For example, $x_9\ge p_x+c+3s/4$ and $x_9\le L-h$ give the upper bound on $p_x$;
$y_7\ge h$ gives $p_y\ge h+c-as$. Define center differences from the bottom corner
squares by

$$
X_6=p_x-1/2,\quad Y_6=p_y-1/2,\qquad
\xi_i=L-1/2-x_i,\quad Y_i=y_i-1/2\quad(i=7,9).
$$

In particular,

$$
\frac15\le X_6\le\frac{147}{100},\quad Y_6>0,\qquad
\frac15\le\xi_9\le\frac{147}{100},\quad Y_9\ge\frac45.
\tag{2}
$$

The center difference for pair 0–6 is $(X_6,Y_6)$; for pair 1–9 it is $(-\xi_9,Y_9)$.
Since all displayed coordinates are positive, the signs of their $x,y$ projections and
of their $e$ or $f$ projection, where used below, are fixed by these formulas.
No division by $a$, $b$, or an angle difference occurs.

## Square 8 Must Enter the Top Unit Strip

First suppose, for contradiction, that $y_8+h\le L-1$. Then

$$
p_y\le77/50,\qquad y_9\le319/200.
\tag{3}
$$

These follow from $p_y=y_8-s-bc$ and $y_9=y_8+as-c$ using the bounds above.

For pair 0–6, the $y$ alternative fails because $Y_6\le26/25<D$. The two $f$
alternatives fail because

$$
|{-sX_6+cY_6}|
\le\max(sX_6,cY_6)
\le\max(1029/1000,104/125)<6/5\le D.
$$

The negative $e$ alternative is impossible because $X_6,Y_6>0$. If the remaining $x$
alternative holds, then $X_6\ge D$ and $Y_6\ge h+c-as-1/2$, whence

$$
cX_6+sY_6\ge D+s(2c-1-as)\ge D.
\tag{4}
$$

Indeed $2c-1-as\ge53/200>0$. Therefore **every** surviving alternative for pair 0–6
implies separation along $e$, or

$$
A\ge k:=u+1/2.
\tag{5}
$$

For pair 1–9, the $y$ alternative fails because $Y_9\le219/200<D$. Both $e$ alternatives
fail since

$$
|{-c\xi_9+sY_9}|
\le\max(c\xi_9,sY_9)
\le\max(147/125,1533/2000)<6/5\le D.
$$

The $f$ projection is positive.
If separation is along $x$, then $\xi_9\ge D$; the bound $Y_9\ge h+s-1/2$ gives

$$
s\xi_9+cY_9\ge D+c(2s-1)\ge D.
\tag{6}
$$

Consequently every surviving alternative implies separation along $f$, namely

$$
B+b\ge J:=3/2+u-sL.
\tag{7}
$$

On the other hand, the assumed top bound gives $p_y+bc\le L-1-s-h$. Combining (5) and
(7), and using $sA+c(B+b)=p_y+bc$, yields

$$
L\ge2+\frac{2(c+s)}{1+cs}
=2+\frac{4u}{1+u^2}
\ge\frac{4900}{1261}>\frac{96}{25}.
$$

The last rational inequality has margin $1444/31525$. The middle expression decreases
for $u>1$, so its minimum on $[7/5,41/29]$ occurs at $41/29$. This contradicts the
frozen side bound. We have proved

$$
\delta:=y_8+h-(L-1)>0.
\tag{8}
$$

This step rules out the tempting shortcut of treating square 8 as wholly below the top
row. Any surviving skeleton would have to use the gap between top squares.

## The Top Cap Must Fit Between Squares 4 and 2

The highest vertex of square 8 is

$$
(X,y_8+h),\qquad X=x_8+(c-s)/2.
$$

Because $x_9=x_8+ac+s\le L-h$,

$$
X\le L-ac-2s\le66/25<3\le z+1.
\tag{9}
$$

Squares 3 and 4 occupy $[0,2]\times[L-1,L]$, and square 2 occupies
$[z,z+1]\times[L-1,L]$. The open portion of square 8 above $y=L-1$ is nonempty and
convex. Nonoverlap confines it to one connected free strip: either $2<x<z$ or $z+1<x<L$.
Points arbitrarily close to its highest vertex have horizontal coordinates arbitrarily
close to $X$, so (9) rules out the right strip.
Its entire open cap lies in $2<x<z$, and

$$
2<X<z.
\tag{10}
$$

Equality in (10) would put nearby interior cap points on both sides of a vertical
obstacle boundary, producing overlap.
This argument remains valid when the highest vertex touches the container’s top wall.

Necessarily $\delta<s$. At vertical distance $s$ below its highest vertex, the
horizontal section of this square has width $1/c\ge5/4$, whereas the central gap has
width $z-2\le L-3\le21/25$. If $\delta>s$, that section is inside the top strip; if
$\delta=s$, sections just above the lower strip boundary approach that width and already
exceed the gap. Both possibilities contradict nonoverlap.

Since $0<\delta<s<c$, the cap is triangular.
Its limiting section at $y=L-1$ has endpoints $X-c\delta/s$ and $X+s\delta/c$. Therefore

$$
X-\frac cs\delta\ge2,\qquad
X+\frac sc\delta\le z,\qquad
\delta\le cs(z-2)\le\frac{21}{50}.
\tag{11}
$$

The weak endpoint inequalities preserve legal contacts with the bottom corners of the
top-row squares. They do not count boundary contact as interior overlap.
The first inequality, with the definitions of $X$ and $\delta$ substituted, is

$$
B+b\le M:=cL-c-2s-1/2.
\tag{12}
$$

The second also gives $A\le cz+sL-s-3/2$, although that inequality is not needed below.
There is a strict incompatibility between (12) and (7) on the entire target:

$$
\begin{aligned}
J-M
&=2+2c+3s-L(c+s)\\
&\ge\frac{96t^2-42t+4}{25(1+t^2)}
\ge\frac{2}{87}>0.
\end{aligned}
\tag{13}
$$

For the final estimate put $d=t-1/3\ge0$. The numerator is $2/3+22d+96d^2\ge2/3$, while
$25(1+t^2)\le29$. The remaining work is to force (7) without the now-disproved below-top
assumption.

## Complete SAT Reduction in the Surviving Cap Case

Equations (1), (2) and (11) imply

$$
p_y\le49/25,\qquad y_7\le139/100,\qquad y_9\le403/200.
\tag{14}
$$

For the first bound use $p_y=L-1-h+\delta-s-bc$. For the second use
$y_7=L-1-h+\delta-(1-a)s-(1+b)c$; for the third use $y_9=L-1-h+\delta+as-c$.

**Pair 0–6 still forces (5).** Both $f$ alternatives fail because

$$
|{-sX_6+cY_6}|
\le\max(1029/1000,146/125)<6/5\le D.
$$

The $x$ alternative implies the $e$ alternative by (4). If the $y$ alternative holds,
then $p_y\ge h+1$. Equation (10) gives $p_x>2-3c/2+s/2+bs$, so

$$
A>k+c(1-2c+s+bs)\ge k,
$$

using $c\le4/5$, $s\ge3/5$, and $b\ge0$. The direct positive $e$ alternative gives (5)
immediately; its negative alternative is impossible.
Thus all SAT alternatives have been accounted for.

**Pair 1–7 must separate horizontally.** Here

$$
\xi_7\ge h+c-bs-1/2\ge149/200>0,\qquad
1/5\le Y_7\le89/100<D.
$$

The $y$ alternatives fail.
The positive $e$ projection is at most $sY_7\le623/1000<D$. The negative $e$ alternative
would require

$$
A+a\le cL-c-1/2.
$$

Together with (5) and $a\ge0$, this requires $c(L-2)\ge1+s$, impossible because
$c(L-2)\le184/125<8/5\le1+s$. The $f$ projection is positive; its separation alternative
would require $B\ge J$. But (12), $b\ge0$, and (13) give $B\le M<J$. Only the leftward
$x$ alternative survives, proving

$$
x_7\le L-1-h.
\tag{15}
$$

**Pair 1–9 now forces (7).** Its center difference is $(-\xi_9,Y_9)$ with both
$\xi_9,Y_9>0$. Its two $e$ alternatives fail since

$$
|{-c\xi_9+sY_9}|
\le\max(147/125,2121/2000)<6/5\le D,
$$

where $Y_9\le303/200$ follows from (14). The leftward $x$ alternative implies separation
along $f$ by (6). If separation is instead upward along $y$, then $Y_9\ge D$. The
retained relation $x_9=x_7+c-bs$ and (15) give $\xi_9\ge D-c+bs$. Hence

$$
s\xi_9+cY_9
\ge s(D-c+bs)+cD
=D+bs^2\ge D.
$$

Thus the upward $y$ alternative also implies separation along $f$. Its direct positive
$f$ alternative already supplies this condition; the negative alternative is impossible.
Every legal SAT choice for pair 1–9 therefore implies (7). Equations (7), (12), and (13)
contradict one another.

Both cases for square 8, $y_8+h\le L-1$ and $y_8+h>L-1$, have been excluded.
The proof uses only the stated box bounds, retained component equations, containment,
the occupied top-row rectangles and complete SAT conditions on pairs 0–6, 1–7, and 1–9.
These are all necessary conditions of every frozen $T_{\rm mid}$ configuration.
Neither the omitted pairs nor square 10 can repair their contradiction.

## Failed Construction and Audit Obligation

A hand-proposed ten-square skeleton was

$$
L=96/25,\quad t=1/3,\quad a=b=1/4,\quad
p=(31/20,31/20),\quad z=5/2.
$$

Its oblique centers are

$$
C_6=(31/20,31/20),\quad C_7=(47/20,9/10),\quad
C_8=(11/5,47/20),\quad C_9=(3,17/10).
$$

It satisfies the retained feature equations and containment, and its square-8 cap fits
between the top-row squares.
It is **not feasible**: relative to square 1, square 7 has displacement $(-99/100,2/5)$,
with absolute $x,y,e,f$ projections

$$
99/100,\quad2/5,\quad69/125,\quad457/500,
$$

all strictly below $D=6/5$. No separating alternative exists for that pair.
No eleventh-square pose was proposed after this failure.
The failure motivated the explicit pair 1–7 reduction above, rather than an assumption
that it could be ignored when studying the square-10 cavity.

The independent auditor must check the two cap cases, the open-cap localization and its
equality limits, the full SAT reductions, and every exact range and algebraic identity.
In particular, the proof must not replace the triangular cap’s weak base inequalities
with a closed-forbidden-polygon coverage claim.
If the audit accepts the argument, it settles this frozen restricted target without a
square-10 cavity enumeration.
If a step fails, retain that exact missing implication; an unreviewed proof is not an
accepted exclusion. This result does not supply a global angle normal form, a complete
cover of other slide/contact/angle domains, or a new unrestricted packing bound.

## Timing and Checks

The phase lease began at 07:49:50 UTC on 2026-09-07. The adversary’s first recorded
clock read was 07:50:43 UTC, and the hard delivery deadline is 08:09:50 UTC. The
proposed protrusion lemma was sent to the coordinator at approximately 07:55 UTC; the
complete contradiction was reported at approximately 08:02 UTC. Only this report was
written. No target command, registry mutation, Git mutation, dependency change or new
identifier was used.

Mathematical work and the final document review ended by 08:08:55 UTC, 18 minutes 12
seconds after the first recorded clock read and 19 minutes 5 seconds after the phase
lease began. Installed Flowmark 0.4.0 formatted this file and passed its check with the
incremental cache disabled.
Mathematical acceptance belongs to the separate independent audit; formatting and link
checks are not mathematical validation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
