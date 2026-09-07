# BC-273: Analytical Attempt on the Frozen Middle-Angle Domain

Status: terminal author result; partial exclusion awaiting independent mathematical
audit. The whole-domain determination is unresolved.
Session-092 phase 4, W3 `insight-iteration`, under the
[frozen protocol](bc-273-analytic-release-protocol.md).
The coordinator recorded the phase start at `2026-09-07T07:44:12Z` and the target
delegation wave at `2026-09-07T07:49:50Z`; the author’s first clock read was
`2026-09-07T07:50:25Z`. The author deadline is `2026-09-07T08:11:12Z`.

The question remains the entire unchanged $T_{\rm mid}$ from the
[accepted design](bc-273-release-domain-design.md) and
[independent review](bc-273-release-domain-independent-review.md).
All eleven containment conditions, all 55 complete SAT disjunctions, variable side,
angle equality and touching remain required.
No local-ball exclusion is used.

## Coordinates and Exact Uniform Bounds

Write $c=c(t)$, $s=s(t)$, $k=c+s$, $h=k/2$ and $K=(1+k)/2$ for the four-square block.
Its shared-coordinate center is

$$
E=c p_x+s p_y,\qquad F=-s p_x+c p_y.
$$

The block centers in these coordinates are $(E,F)$, $(E+a,F-1)$, $(E+1,F+b)$ and
$(E+1+a,F+b-1)$, for labels 6, 7, 8 and 9 respectively.
The frozen angle interval gives

$$
\frac{21}{29}\le c\le\frac45,\quad
\frac35\le s\le\frac{20}{29},\quad
\frac75\le k\le\frac{41}{29},\quad
\frac1{29}\le c-s\le\frac15.
$$

These follow from monotonicity of the rational sine and cosine formulas on
$1/3\le t\le2/5$. In particular $c>s>0$. Since $0\le a,b\le1/4$, the increments $ae-f$
and $e+bf$ have coordinate signs $(+,-)$ and $(+,+)$. Thus block containment gives the
exact necessary translation bounds

$$
\begin{aligned}
h&\le p_x\le L-h-(a+1)c-(1-b)s,\\
h+c-as&\le p_y\le L-h-s-bc.
\end{aligned}
$$

For one axis square and one block square, every candidate SAT axis has the same combined
support half-width $K$: coordinate axes and block axes both give $(1+c+s)/2$. This makes
all eight directed alternatives explicit without selecting a source cell.

## A Conditional Lower Bound That Does Not Yet Cover the Target

Suppose pair 4–8 separates below/right along $f$, and pair 1–9 separates above/left
along $f$. Their exact inequalities are

$$
F+b\le c(L-1)-2s-\tfrac12,\qquad
F+b\ge c-s(L-1)+\tfrac32.
$$

Combining them yields

$$
L\ge 2+\frac{2+s}{c+s}.
$$

As a function of the actual angle $\theta$, the derivative of $(2+s)/(c+s)$ is
$(1-2(c-s))/(c+s)^2>0$ on the admitted interval.
At its lower endpoint, $(c,s)=(4/5,3/5)$, so

$$
L\ge\frac{27}{7}>\frac{96}{25};\qquad
\frac{27}{7}-\frac{96}{25}=\frac3{175}.
$$

This excludes the conjunction of those two directed alternatives, including their
equality boundaries, uniformly in every remaining parameter.
It does not justify assuming the alternatives.
Other SAT directions are legal in the frozen definition, and the full target is
unresolved until they are covered.

## A Uniform Four-Way Restriction on Square 10

Let $X=cw_x+sw_y$ and $Y=-sw_x+cw_y$ denote its center in the block basis.
Its actual angle differs from the block angle by at most

$$
|\phi-\theta|\le 2\arctan(1/17),
$$

because the tangent half-difference at the two interval endpoints is
$(2/5-1/3)/(1+(2/5)(1/3))=1/17$. Consequently

$$
\cos(\phi-\theta)+|\sin(\phi-\theta)|\le\frac{161}{145}.
$$

The tilted square 10 therefore contains a square aligned with the block basis, centered
at $(X,Y)$, of side $\lambda=145/161$. Nonoverlap with an actual block square implies
nonoverlap with this contained square.
Thus its center cannot lie in the interior of any block-centered axis square of radius

$$
R=\frac{1+\lambda}{2}=\frac{153}{161}>r=\frac{19}{20}.
$$

The strict inequality follows from $3060>3059$. Using the smaller rational radius $r$
preserves a strict margin rather than treating touching as overlap.

The four open forbidden boxes of radius $R$ cover the closed rectangle

$$
[E+a-r,E+1+r]\times[F+b-1-r,F+r].
$$

For a direct proof, the boxes at 6 and 7 cover $[E+a-r,E+r]\times[F-1-r,F+r]$; their
vertical intervals overlap because $2r>1$. The boxes at 8 and 9 cover
$[E+1+a-r,E+1+r]\times[F+b-1-r,F+b+r]$. Their horizontal ranges overlap because
$2r>1+a$, and their common vertical range contains the displayed rectangle’s vertical
interval. The strict radius gap $R>r$ puts the closed rectangle inside the union of the
open forbidden boxes, including all rectangle endpoints.

Every feasible target packing must therefore satisfy at least one of the four strict
alternatives

$$
\boxed{
X<E+a-r\quad\lor\quad X>E+1+r\quad\lor\quad
Y<F+b-1-r\quad\lor\quad Y>F+r.}
$$

This is a necessary consequence of the four square-10 pair conditions, not a replacement
for the other six or for containment.
Each strict alternative can be enlarged to its weak-inequality closure when constructing
a future closed exclusion cover.
The enlargement preserves coverage and includes extra boundary controls; none of those
added boundary points is being asserted feasible.
The result covers the complete two-angle interval, including $v=t$, and makes no
assumption about 9–10 recontact or a positive release gap.

## Forced Separations in Every Feasible Skeleton

These deductions retain the original SAT disjunctions and prove which alternatives
survive. They do not impose source directions as extra premises.

### Pair 0–6 must use its positive block projection

Both components of $p-(1/2,1/2)$ are positive.
Its complete SAT condition therefore implies at least one of

$$
E\ge k+1/2,\qquad p_x\ge1+h,\qquad p_y\ge1+h.
$$

A positive or negative $f$ separation implies the corresponding vertical or horizontal
coordinate separation: its positive term is smaller than that coordinate difference.
The negative $e$ alternative is impossible.
If $p_x\ge1+h$, block containment gives

$$
E-(k+1/2)\ge s(2c-1-as)>0,
$$

since $2c-1-as\ge8/29$.

If $p_y\ge1+h$, compare square 6 with axis square 5. Their displacement has positive
horizontal component and vertical component in $[-16/25,1/5]$. Both vertical directions,
the negative horizontal direction, negative $e$ and positive $f$ have projection
strictly below $K$. For the last two, upper bounds are $(20/29)(16/25)<K$ and
$(4/5)(1/5)<K$. The remaining alternatives are positive horizontal, positive $e$, and
negative $f$. Positive horizontal was handled above.
Positive $e$ gives $E\ge k+1/2+s(L-2)>k+1/2$. Negative $f$ gives $F\le c(L-2)-s-1/2$,
whence

$$
E-(k+1/2)\ge\frac{c[1-c(L-3)]}{s}>0.
$$

The last sign follows from $c(L-3)\le84/125<1$. Thus every feasible skeleton obeys
$E\ge k+1/2$.

### Pairs 4–8 and 1–9 each have only two relevant alternatives

Write $(u,d)=(C_{8,x}-3/2,C_{8,y}-L+1/2)$. Block containment gives

$$
-36/145\le u\le26/25,\qquad d\le1/2-h<0.
$$

Both horizontal directions, positive vertical, positive $e$ and positive $f$ have
projection below $K\ge6/5$. For positive $e$ use $cu+sd\le(4/5)(26/25)$; for positive
$f$ use $-su+cd\le(20/29)(36/145)$. For the negative $e$ alternative, substitution of
the lower translation bounds gives

$$
e\cdot(C_8-C_4)+K
\ge2+2cs-as^2-c-(L-1)s\ge2/25>0.
$$

The final estimate uses $2cs\ge24/25$, $as^2\le3/25$, $c\le4/5$ and
$(L-1)s\le284/145<49/25$. Consequently pair 4–8 requires

$$
F+b\le c(L-1)-2s-1/2
\quad\text{or}\quad C_{8,y}\le L-1-h.
$$

For pair 1–9 the displacement has negative horizontal and positive vertical components.
Its $e$ alternatives imply horizontal-left or vertical-above separation; negative $f$ is
impossible. Horizontal-left separation itself implies positive $f$: using
$C_{9,y}\ge h+s$, its $f$ projection exceeds $K$ by at least $c(2s-1)>0$. Hence pair 1–9
requires

$$
F+b\ge c-s(L-1)+3/2
\quad\text{or}\quad C_{9,y}\ge1+h.
$$

### The surviving skeleton has square 9 above square 1

The two vertical alternatives cannot occur together.
They would give

$$
16/29\le c-as=C_{8,y}-C_{9,y}\le L-2-k\le11/25,
$$

which is impossible.
If pair 4–8 uses its vertical alternative and pair 1–9 its $f$ alternative, substitute
$E\ge k+1/2$ and the latter $F+b$ bound into $C_{8,y}=s(E+1)+c(F+b)\le L-1-h$. The
result is

$$
L\ge2+\frac{2k}{1+cs}\ge\frac{58}{15}>\frac{96}{25}.
$$

Here $k\ge7/5$ and $cs\le1/2$ suffice for the second bound.
Thus the vertical 4–8 alternative is excluded.
The conditional $27/7$ bound then excludes the $f$ alternative of 1–9. Every feasible
target skeleton must obey

$$
\boxed{E\ge k+1/2,\quad F+b\le c(L-1)-2s-1/2,\quad C_{9,y}\ge1+h.}
$$

### Square 2 forces a top-row gap

For pair 2–8, the horizontal displacement is at most $1/25$, and its vertical
displacement is negative and at least $3/2+7/10+16/29-96/25>-11/10$. Thus neither
vertical direction, positive horizontal, positive $e$ nor negative $f$ can separate.
For negative $f$ use the upper bound $(20/29)(1/25)+(4/5)(11/10)<6/5$. Positive $f$, if
it separates, implies negative $e$: both displacement components must then be negative,
and $-e\cdot d-f\cdot d=-(c-s)d_x-kd_y>0$. The remaining horizontal-left possibility is
$C_{8,x}\le z-h$. Combining this with the forced 4–8 $f$ bound shows that its $e$
projection exceeds the desired upper bound by at most $s[s(z-2)-1]/c<0$, since
$s(z-2)<1$. Therefore every surviving skeleton satisfies

$$
E+1\le cz+s(L-1)-1/2.
$$

Together with the forced 4–8 row this gives $C_{8,y}\le L-1-h+cs(z-2)$. Since
$C_{8,y}=C_{9,y}+c-as\ge1+h+c-as$,

$$
\boxed{cs(z-2)\ge2+2c+(1-a)s-L
\ge2+2c+\tfrac34s-L.}
$$

The function $2c+3s/4$ decreases on the admitted angle interval.
At $t=2/5$ it is $57/29$. Hence $z-2\ge182/725>1/4$. If $s\le13/20$, monotonicity and
$c(\arcsin(13/20))=\sqrt{231}/20>759/1000$ strengthen this to $z-2>331/1000$.

## Exclusion of the Right Exterior Compartment

The entire closed branch $X\ge E+1+r$ is impossible.
The proof uses the contained square of side $\lambda=145/161$ and the original axis
square 2. Their combined support half-widths are $A=(1+\lambda k)/2$ on coordinate axes
and $J=(k+\lambda)/2$ on block axes.
Actual containment of square 10 gives $7/10\le w_x,w_y\le L-7/10$. The branch and the
forced 0–6 row imply

$$
X\ge k+49/20\ge77/20.
$$

Seven of the eight core-versus-square-2 SAT alternatives are impossible:

| Alternative | Exact exclusion bound |
| --- | --- |
| Right in the horizontal coordinate | $w_x\ge z+1+\lambda h>363/100$, but $w_x\le157/50$ |
| Above in the vertical coordinate | $w_y\ge L+\lambda h$, contradicting containment |
| Left in the horizontal coordinate | $X\le Lk-c-(7/10)s-\lambda ch<96/25<77/20$; use $k<283/200$, $c\ge18/25$, $s\ge3/5$, $h\ge7/10$, $\lambda>9/10$ |
| Below in the vertical coordinate | $X-k\le(L-1)k-(7/10)c-s-(9/20)sk\le1219/500<49/20$ |
| Positive $e$ | $X-e\cdot C_2\le c(L-16/5)-s/5\le49/125<J$ |
| Negative $e$ | $X\le cz+s(L-1)-\lambda/2\le k(L-1)-\lambda/2<17843/5000<77/20$ |
| Positive $f$ | $Y\ge cL-sz+\lambda/2$ implies $X\le Lk-c-[(7/10)+c\lambda/2]/s<33/10<77/20$ |

For the below-coordinate row, the expression is increasing in $L$ and decreasing in the
actual block angle. At $L=96/25$ its angle derivative is at most
$47/250-(9/20)(24/25)<0$, because $c^2-s^2\ge0$ and $2cs\ge24/25$. Its maximum is
therefore at $(c,s)=(4/5,3/5)$, where it is $1219/500$. For the positive-$f$ row,
$z\le L-1$ was used; the final strict bound follows from $Lk<27168/5000$, $c\ge18/25$
and $[(7/10)+c\lambda/2]/s>73/50$.

The remaining SAT direction is necessarily negative $f$:

$$
Y\le c(L-1)-s(z+1)-\lambda/2.
$$

Combining it with $X\ge E+1+r$, $E\ge k+1/2$ and $w_x=cX-sY\le L-7/10$ gives

$$
L(1+cs)\ge\frac{17}{10}+2cs+s^2z+\frac{49}{20}c+\frac\lambda2s.
$$

The right side minus $(96/25)(1+cs)$ is at least

$$
-\frac{153}{50}+s^2z+\frac{49}{20}c+\frac9{20}s,
$$

using $cs\le1/2$ and $\lambda>9/10$. For any constant $z_0\ge9/4$, the function
$z_0s^2+(49/20)\sqrt{1-s^2}+(9/20)s$ increases over the admitted sine interval: its
derivative is $s(2z_0-49/(20c))+9/20>0$, using $c\ge18/25$.

If $s\ge13/20$, use $z>9/4$, $c(13/20)>759/1000$ and that monotonicity.
The displayed difference is greater than

$$
-\frac{153}{50}+\frac94\frac{169}{400}
+\frac{49}{20}\frac{759}{1000}+\frac9{20}\frac{13}{20}
=\frac{1707}{40000}>0.
$$

If $s\le13/20$, use the stronger $z>2331/1000$ and the minimum at $(c,s)=(4/5,3/5)$. The
difference exceeds

$$
-\frac{153}{50}+\frac{2331}{1000}\frac9{25}
+\frac{49}{20}\frac45+\frac9{20}\frac35
=\frac{229}{25000}>0.
$$

Both cases contradict $L\le96/25$. This excludes the closed right compartment, uniformly
in all ten original parameters and in the equal-angle seam.

## Remaining Cases and Failed Implications

The whole target remains unresolved.
The left, lower and upper exterior compartments from the four-way necessary restriction
have not been excluded:

$$
X\le E+a-r,\qquad Y\le F+b-1-r,\qquad Y\ge F+r.
$$

Their union, with all frozen containment and SAT conditions, is an explicit closed
remainder containing every possible target packing after the right-compartment result.
No point in that remainder is asserted feasible.
No claim removes angle equality, 9–10 recontact, the zero-slide seams or a legal
touching placement.

The two source $f$ directions could not be assumed from the declared features: square 9
has a vertical-above alternative in its SAT disjunction.
No feasible whole-target counterexample to that unproved implication was constructed.
The alternative was retained, and the proof derives its required top-row gap.
The square-10 inner core supplies a necessary exterior cover; it is not an equivalence
to full feasibility and cannot certify a counterexample.
The right-compartment exclusion does not establish a cover of the entire contained
center box by forbidden interiors.

The next bounded mathematical task is to decide the three displayed closed exterior
compartments against the forced rows and the complete original geometry.
In particular, the lower compartment must keep the bottom gap between axis squares 0 and
1; assuming that square 10 lies to the right of the four-square block would leave that
case out. A separately priced affine-feature certificate could encode these forced rows,
the compartment disjunction and two angle intervals, after its own controls are
accepted. This note authorizes no such computation or continuation.

No numerical search, solver or target script was used.
Every numerical constant above is an exact rational bound or an explicitly displayed
symbolic endpoint calculation.

## Terminal Receipt

The mathematical attempt stopped at the verification checkpoint `2026-09-07T08:09:22Z`,
18 minutes 57 seconds after the author’s first clock read and 1 minute 50 seconds before
the assigned deadline.
The first intermediate proof note was written at `2026-09-07T07:59:36Z`; the coordinator
received the later forced-row and right-compartment findings before terminalization.
The author did not inspect or coordinate reasoning with the independent adversary.

Only this assigned report was written.
No target scripts, numerical searches, solver invocations, Git mutations, registry
edits, IDs or dependencies were created.
The report received the Practical Prose common-guidelines and de-slop passes.
Installed Flowmark 0.4.0 formatting and its full auto-format check passed with caching
disabled; the scoped whitespace check passed.
These are document checks, not an independent replay of the mathematics.
The entire $T_{\rm mid}$ question remains open pending both the three residual
compartments and the independent audit of these partial claims.
No background command remains.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
