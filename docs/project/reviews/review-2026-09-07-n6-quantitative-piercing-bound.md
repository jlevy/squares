# An Explicit Five-Point Piercing Obstruction Near Side Three

**Date:** 2026-09-07. **Status:** independently reviewed analytic derivation; not a
registered campaign theorem.
**Scope:** five unweighted points piercing individual squares.
This does not exclude fractional measures or conditional arguments involving several
packed squares, and it changes no packing bound.

Stromquist’s email prompted the
[five-point argument](review-2026-09-07-n6-pure-dots-obstruction.md).
Its boundary-strip case split shows that five points cannot pierce every open unit
square in a container of side $L\ge L_0=(12+2\sqrt2)/5$, including equality.
The rational proposition implemented by the control proves that every set of at most
five points in `[0,3]^2` misses a closed square of side at least `101/100`. The
constants are fixed algebraic choices; no parameter sweep was used, and no optimality is
claimed.

## What the Published Piercing Result Establishes

[Bašić–Slivková, *On optimal piercing of a square*](../../../packing/resources/papers/basic-slivkova-2018-optimal-piercing-square.pdf)
defines $\mathcal U_L$ using open unit squares in a container of side $L$. Theorem 1 and
Corollary 4 give $\pi(\mathcal U_3)=9$: the nine disjoint open unit cells already
require nine piercing points.
Theorem 7 gives an upper bound for noninteger container sides.
Its displayed formula on preprint p. 14 yields

$$
\pi(\mathcal U_L)\le7
\quad\text{for}\quad
2\sqrt2-1+\frac{\sqrt3}{2}\le L<3.
$$

Indeed, set $b=\lfloor(2/\sqrt3)(L+1-2\sqrt2)\rfloor$. On this interval,
$\lfloor L\rfloor=2$, $b=1$, and the fractional part of $L$ exceeds one half.
The applicable branch of Theorem 7 is $\lfloor L\rfloor(b+2)+\lfloor(b+2)/2\rfloor$,
giving $2(1+2)+\lfloor3/2\rfloor=7$. The left endpoint is included: the expression
defining $b$ is exactly one there.
At the right endpoint $L=3$, the integer part and the fractional-part branch change.
Thus the integer-side value nine cannot imply left continuity at side three.
The paper gives no quantified lower bound of six below three.
The
[author’s preprint](https://people.dmi.uns.ac.rs/~bojan.basic/papers/square_pak%20new.pdf)
and [published article](https://doi.org/10.1016/j.dam.2018.03.048) identify the primary
source.

[Friedman, §5](https://erich-friedman.github.io/papers/squares/squares.html) gives a
seven-point unavoidable set for closed unit squares in `[0,3]^2`, and uses five *almost*
unavoidable points inside a helper proof for seven packed squares.
Neither statement rules out all five-point unavoidable sets.
[Nagamochi’s §3](../../../packing/resources/papers/nagamochi-2005-packing-unit-squares-in-a-rectangle.pdf)
generalizes the resource count to points, line segments, and area; it does not give this
five-point threshold.
This is a bounded source check, not a claim that the following derivation is absent from
all literature.

## Uniform Empty-Square Proposition

**Proposition.** For every set $P\subset[0,3]^2$ with $|P|\le5$, there is a closed
square $Q\subset[0,3]^2$ such that $Q\cap P=\varnothing$ and its side is at least
$a=101/100$.

Extend $P$ to five distinct points if necessary.
If a closed axis-aligned square of side $a$ misses $P$, the proposition is proved.
Otherwise assume every such square contained in `[0,3]^2` meets $P$.

The four corner squares of side $a$ are pairwise disjoint because $2a<3$. Choose one
point in each and name them in cyclic order: $A$ at the bottom left, $B$ at the bottom
right, $C$ at the top right, and $D$ at the top left.
Call the remaining point $R$.

Define the two intervals

$$
I_-=[3-2a,a]=[49/50,101/100],\qquad
I_+=[3-a,2a]=[199/100,101/50].
$$

Consider closed intervals `[t,t+a]` along a boundary strip, with `0 <= t <= 3-a`. If all
eligible projected sites lie in `[0,a]` or `[3-a,3]`, let $u$ be the largest coordinate
in the first group and $v$ the smallest in the second.
Hitting every such interval requires $v-u\le a$; otherwise a closed interval of length
$a$ lies strictly between $u$ and $v$. Since $u\le a$ and $v\ge3-a$, it follows that
$u\in I_-$ and $v\in I_+$. When a group has one point, this bounds that point.

Up to a global symmetry, $R$ has three possible locations.
Closed corner cells include their boundaries; edge-middle coordinates are strictly
between $a$ and $3-a$ along the edge; the central cell is `(a,3-a)^2`.

1. **Central cell.** Every boundary strip contains only its two selected corner sites.
   Applying the interval fact on all four sides gives $A\in I_-^2$,
   $B\in I_+\times I_-$, $C\in I_+^2$, and $D\in I_-\times I_+$.
2. **Bottom edge-middle cell.** The left and right strips put $A.y,B.y\in I_-$ and
   $D.y,C.y\in I_+$. The top strip gives $D.x\in I_-$ and $C.x\in I_+$. Thus the two top
   points lie in the indicated inner rectangles, and all three other points have
   `y <= a`.
3. **Bottom-left corner cell.** The right strip gives $B.y\in I_-$ and $C.y\in I_+$; the
   top strip gives $D.x\in I_-$ and $C.x\in I_+$. The bottom strip has two left-group
   sites and only $B$ in the right group, so $B.x\in I_+$. The left strip similarly
   forces $D.y\in I_+$. Again the top points lie in their inner rectangles, and all
   other points have `y <= a`.

Take four closed diamonds of radius $r=143/200$ in the $\ell_1$ distance, centered at

$$
(3/2,3/4),\quad (3/4,3/2),\quad (3/2,9/4),\quad (9/4,3/2).
$$

Each is a square rotated 45°. Its side $\ell=r\sqrt2$ exceeds $a$, since

$$
\ell^2-a^2=2(143/200)^2-(101/100)^2=47/20000>0.
$$

Each diamond lies strictly inside `[0,3]^2`, with minimum wall clearance $7/200$. Every
pair of centers has $\ell_1$ distance at least $3/2$, exceeding $2r$ by at least
$7/100$; the four closed diamonds are pairwise disjoint.

The top diamond’s center has $\ell_1$ distance at least

$$
(3/2-a)+(9/4-2a)=15/4-3a=18/25
$$

from each of $I_-\times I_+$ and $I_+^2$. This exceeds $r$ by $1/200$, so the top
diamond avoids $C$ and $D$. Its lowest height is $9/4-r=307/200>a$, so in the
edge-middle and corner cases it also avoids the other three points.

In the central case, the same calculation and rotations show that each diamond avoids
all four corner-site rectangles.
The nonadjacent rectangles are farther away.
Since the four diamonds are pairwise disjoint, $R$ belongs to at most one of them.
At least three diamonds therefore avoid all of $P$. This proves the proposition.

## Rational Control for Unit-Square Piercing

**Corollary.** For every $L\ge300/101$ and every set of at most five points in
`[0,L]^2`, some closed unit square contained in `[0,L]^2` avoids all those points.
Consequently $\pi(\mathcal U_L)\ge6$ for the open-unit-square family as well.

First take $L=300/101$. Scale the points and container by $101/100$ to obtain a set in
`[0,3]^2`. Apply the proposition and scale its avoiding square back; its side is at
least one. If necessary, take a closed unit square inside it.
For a larger container, apply this argument to the points in a corner subcontainer of
side `300/101`; points outside that subcontainer cannot belong to its avoiding square.

## Sharper Open-Unit Endpoint

**Theorem.** Put

$$
L_0=\frac{12+2\sqrt2}{5}.
$$

For every $L\ge L_0$ and every set $P\subset[0,L]^2$ with $|P|\le5$, there is an open
unit square contained in `[0,L]^2` that misses $P$. Hence $\pi(\mathcal U_L)\ge6$. For
every $L>L_0$, a closed unit square avoiding $P$ also exists.

It suffices first to prove the open-square assertion at $L=L_0$. Pad $P$ to five
distinct points if needed.
If a closed axis-aligned unit square misses $P$, its interior proves the assertion.
Otherwise every such square meets $P$. The four corner unit squares are pairwise
disjoint since $L_0>2$. Select their sites $A,B,C,D$ in cyclic order as before, with
remaining site $R$.

The boundary-strip argument from the rational proposition now uses intervals of length
one in a container of length $L_0$. It gives

$$
J_-=[L_0-2,1],\qquad J_+=[L_0-1,2].
$$

The two extreme projected sites must satisfy $v-u\le1$, with $u\le1$ and $v\ge L_0-1$.
Thus $u\in J_-$ and $v\in J_+$. The same three cases for $R$ have the following
consequences:

1. If $R\in(1,L_0-1)^2$, the four selected sites lie respectively in $J_-^2$,
   $J_+\times J_-$, $J_+^2$, and $J_-\times J_+$.
2. If $R\in(1,L_0-1)\times[0,1]$, the top sites satisfy $C\in J_+^2$ and
   $D\in J_-\times J_+$, and all three other sites have `y <= 1`.
3. If $R\in[0,1]^2$, the same conclusion holds: the top and right strips bound
   $C.x,C.y,D.x$, and the left strip’s unique top site forces $D.y\in J_+$.

Global symmetries cover every edge-middle and corner location, including boundaries.
Take four **open** diamonds of $\ell_1$ radius $\rho=1/\sqrt2$, centered at

$$
(L_0/2,L_0/4),\quad(L_0/4,L_0/2),\quad
(L_0/2,3L_0/4),\quad(3L_0/4,L_0/2).
$$

Each is a unit square rotated 45°. Their closures fit strictly inside the container,
since their minimum wall clearance is

$$
\frac{L_0}{4}-\rho=\frac{3-2\sqrt2}{5}>0.
$$

Every pair of centers has $\ell_1$ distance at least $L_0/2$, and

$$
\frac{L_0}{2}-2\rho=\frac{6-4\sqrt2}{5}>0.
$$

Thus even the four closures are pairwise disjoint.
The top center has distance at least

$$
\left(\frac{L_0}{2}-1\right)
+\left(\frac{3L_0}{4}-2\right)
=\frac{5L_0}{4}-3=\rho
$$

from each top rectangle $J_-\times J_+$ and $J_+^2$. Both coordinate differences are
positive. The two bottom rectangles have distance at least $5L_0/4-2=\rho+1$. Therefore
the top open diamond avoids all four rectangles, including their boundaries.
Its lowest height is

$$
\frac{3L_0}{4}-\rho=\frac{9-\sqrt2}{5}>1.
$$

In the edge-middle and corner cases, it also avoids the other three sites and proves the
assertion. In the central case, rotation gives the same rectangle avoidance for all four
diamonds. Since they are pairwise disjoint, $R$ can belong to at most one, leaving at
least three open unit squares avoiding $P$.

This proves the theorem at $L_0$, including equality.
For $L>L_0$, scale $P$ into `[0,L_0]^2`, apply the result, and scale its avoiding open
square back. Its side is $L/L_0>1$, so it contains a closed unit square avoiding $P$. At
$L=L_0$, the corner-rectangle distance can equal $\rho$; the endpoint proof uses the
open-square convention at precisely that step.

The endpoint also follows from the rational proof’s parameter inequality.
An enlarged diamond of side at least $a$ has radius at least $a/\sqrt2$, while its
distance from the adjacent inner rectangles is $15/4-3a$. The closed-diamond argument
requires

$$
\frac a{\sqrt2}\le r<\frac{15}{4}-3a,
\qquad\text{hence}\qquad
1<a<\frac{15}{12+2\sqrt2}.
$$

The open formulation permits equality at $a=15/(12+2\sqrt2)=3/L_0$. The fixed rational
control has the positive clearances displayed above and does not depend on this boundary
equality.

## Combined Piercing Interval

The published upper-bound interval includes $[L_0,3)$, because

$$
2\sqrt2-1+\frac{\sqrt3}{2}<2\sqrt2<L_0<3.
$$

Combining Theorem 7 of Bašić–Slivková with the analytic theorem above gives

$$
6\le\pi(\mathcal U_L)\le7
\qquad\text{for}\qquad
\frac{12+2\sqrt2}{5}\le L<3.
$$

The lower bound is the derivation in this review; the upper bound is published.
The result concerns piercing individual placements.
Avoiding squares constructed for different point sets need not coexist, so the argument
proves no additional packing theorem.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
