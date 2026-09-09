# BC-281: Author’s Partial Full-Angle Exclusion

The whole-domain determination is **inconclusive**. This report gives exact hand proofs
excluding both slide signs on $t\in[2/5,1/2]$, including the $c=s$ seam, and on the two
closed axis neighborhoods $[0,1/24]$ and $[23/25,1]$. Together with the accepted
middle-angle theorem, these leave the closed remainder

$$
\bigl([1/24,1/3]\cup[1/2,23/25]\bigr)
\times\bigl(\{a,b\ge0\}\cup\{a,b\le0\}\bigr),
$$

with every other defining parameter and geometric condition retained.
Its endpoints deliberately overlap proved regions.
No contradiction for this remainder and no actual eleven-square witness is supplied.
The new proofs below are submitted for the protocol’s fresh independent audit.

This is the BC281 author allocation in session092 phase 18, inheriting W3
`insight-iteration`, H120 and bead `think-ilpc`. The controlling revision is
`bdbfc054baefb79d67832b339c71830ba39e1ab1`. The
[frozen protocol](bc-281-full-angle-release-protocol.md), its
[independent admission](bc-281-full-angle-protocol-review.md), the
[full-angle domain](bc-280-full-angle-release-domain.md) and its
[domain admission](bc-280-full-angle-domain-review.md) define the unchanged target.
The coordinator reported passing immutable records before dispatch.

## Scope and Necessary Geometry

The target remains the entire $\mathcal S_{\rm full}$, with $381/100\le L\le96/25$,
$t,v\in[0,1]$, $a,b\in[-1/4,1/4]$, $2\le z\le L-1$ and $p,w\in[1/2,7/2]^2$. It has
eleven actual labeled unit squares, nine prescribed flush incidences, six positive
prescribed segments, 44 containment rows and all 55 complete weak SAT disjunctions.
Square 10 retains its independent center $w$ and angle $v$. Every target point projects
to the ten actual squares used below with these same parameters and conditions; the
projection does not change $L$ or move a wall square.

Put

$$
c=\frac{1-t^2}{1+t^2},\quad s=\frac{2t}{1+t^2},\quad
e=(c,s),\quad f=(-s,c),\quad u=c+s,\quad h=u/2,\quad D=h+1/2,
$$

and write $A=e\cdot p$, $B=f\cdot p$. The needed centers are exactly

$$
\begin{aligned}
C_0&=(1/2,1/2),& C_1&=(L-1/2,1/2),\\
C_2&=(z+1/2,L-1/2),& C_3&=(1/2,L-1/2),\\
C_4&=(3/2,L-1/2),& C_5&=(1/2,L-3/2),\\
C_6&=p,& C_7&=p+ae-f,\\
C_8&=p+e+bf,& C_9&=p+(1+a)e+(b-1)f.
\end{aligned}
$$

Squares 0–5 are axis aligned; 6–9 have basis $(e,f)$. For an axis square and a block
square, the sum of their actual supports on each of $x,y,e,f$ is $D$. Their full pair
condition is therefore that at least one of the eight directed projections on these four
axes is at least $D$. All thresholds are weak; a screened direction is strictly below
its threshold.

The two block diagonal clauses give

$$
(a\ge0\lor b\le0)\land(a\le0\lor b\ge0),
$$

or $ab\ge0$, throughout the slide box.
Thus the two closed sign children cover the target, including every one-zero slide face
and their intersection $a=b=0$. The
[positive middle audit](bc-273-analytic-independent-review.md) and
[negative middle audit](bc-276-negative-slide-independent-review.md) already exclude
$t\in[1/3,2/5]$ for both signs and all $v,w$. The following extension supplies its own
bounds and SAT reductions.

## A Uniform Counting Restriction and Both Axis Neighborhoods

Every feasible ten-square skeleton in the full chart must satisfy

$$
L(c+s)\ge4. \tag{1}
$$

To prove this, set $q=1/(c+s)$. Each block square contains the axis-aligned square of
side $q$ with the same center: its projection on either $e$ or $f$ has half-width
$q(c+s)/2=1/2$. Since $1\le c+s\le\sqrt2$, the same centered square also lies in each of
the six axis unit squares.
The ten cores are contained in $[0,L]^2$ and have disjoint interiors, because their
actual containing squares do.
This is a necessary projection, with no claim that a feasible core packing would
reconstruct an actual target packing.

If $L<4q$, the possible center interval $[q/2,L-q/2]$ has length $L-q<3q$. Partition
that interval into three consecutive intervals of equal length, assigning shared
endpoints consistently.
The resulting nine cells each have width and height strictly less than $q$. Two of ten
centers lie in one cell, so their cores overlap in both coordinate directions and have
intersecting interiors.
This contradiction proves (1), without discarding legal touching.

The six fixed axis squares strengthen (1) to

$$
L\ge2+\frac2{c+s}. \tag{1a}
$$

Suppose instead $L<2+2q$. Because $q\le1$, this implies $L-3<2q-1\le q$. No block core
can extend above $y=L-1$: its intersection with the top strip would have its full
horizontal width $q$, whereas each free top interval, $[2,z]$ and $[z+1,L]$, has width
at most $L-3<q$. Likewise no block core can extend left of $x=1$, because the only free
interval between the left-column obstacles is $[1,L-2]$, of height $L-3<q$. These
arguments use a nonempty interior intersection with a strip; equality at its boundary
remains allowed.

Actual block-square containment also puts their core right edges at most $L-h+q/2$ and
their core bottom edges at least $h-q/2$. Thus the four block cores lie in
$[1,L-h+q/2]\times[h-q/2,L-1]$. Translate this rectangle to the origin and put
$T=L-1-h+q/2$ and $r=1-h+q/2$. It is a square of side $T$; its intersection with the
actual unit square 1 is the corner square $[T-r,T]\times[0,r]$. Here $r>0$ and $r\le q$,
the latter because $r-q=1-(u+1/u)/2\le0$. Each core must be wholly to the left of that
corner square or wholly above it.
Assign it to one of these classes, choosing either class if both apply.

We have $T<r+2q\le3q$. Centers in the left class have horizontal range of length
$T-r-q<q$, so distinct members must be vertically separated by at least $q$. There are
at most two, since the full vertical center range has length $T-q<2q$. The above class
likewise has at most two members, horizontally separated by at least $q$. Four cores
would require two in each class.
Let $(x_H,y_H)$ be the upper center in the left class and $(x_V,y_V)$ the left center in
the above class. Their ordering and containment give $y_H\ge3q/2$, $x_V\le T-3q/2$,
$x_H\le T-r-q/2$ and $y_V\ge r+q/2$. The remaining coordinate bounds are $q/2$ and
$T-q/2$, so

$$
\begin{aligned}
x_V-x_H&\le T-2q<q,& x_H-x_V&\le T-r-q<q,\\
y_V-y_H&\le T-2q<q,& y_H-y_V&\le T-r-q<q.
\end{aligned}
$$

These two distinct cores overlap in their interiors, a contradiction.
This proves (1a) for every target skeleton, without using the block contact equations or
restricting its angle.

On $[0,1/24]$, $c+s$ increases, and on $[23/25,1]$ it decreases.
The two inner endpoints give exactly

$$
u(1/24)=u(23/25)=\frac{623}{577}.
$$

Consequently these two closed angular neighborhoods would require

$$
L\ge\frac{2400}{623}>\frac{96}{25},
\qquad
\frac{2400}{623}-\frac{96}{25}=\frac{192}{15575}>0.
\tag{2}
$$

Both physical axis lifts, both slide signs and every square-10 pose are covered.
The equality of the scalar supports at the two inner endpoints is an identity; no
reflection or relabeling of the target has been assumed.

## Fresh Bounds and Cap Geometry on $[2/5,1/2]$

For the rest of the proof assume $2/5\le t\le1/2$. The rational formulas and their
derivatives give

$$
\frac35\le c\le\frac{21}{29}<\frac{73}{100},\qquad
\frac{17}{25}<\frac{20}{29}\le s\le\frac45,
\qquad \frac75\le u\le\sqrt2<\frac{71}{50}.
\tag{3}
$$

For the lower bound on $u$, its rational formula gives $u\ge7/5$ exactly when
$6t^2-5t+1\le0$, which holds on $[1/3,1/2]$. In particular $7/10\le h<71/100$ and
$D\ge6/5$. Both $c$ and $s$ are positive, but their ordering is unrestricted.

The four block displacements have the coordinate order

$$
s+ac>0,\quad c-as>0,\quad c-bs>0,\quad s+bc>0.
$$

For example, $s+ac,s+bc\ge17/25-73/400=199/400>0$, and $c-as,c-bs\ge3/5-1/5=2/5>0$.
Containment therefore gives

$$
p_x\ge h,\quad
p_x\le L-h-(1+a)c-(1-b)s,\quad
p_y\ge h+c-as.
\tag{4}
$$

Define the height and abscissa of square 8’s top cap by

$$
\delta=y_8+h-(L-1),\qquad X=x_8+(c-s)/2,\qquad G=z-2.
$$

If $\delta>0$, the open interior of square 8 above $y=L-1$ is nonempty and connected.
The occupied top rectangles are $[0,2]\times[L-1,L]$ and $[z,z+1]\times[L-1,L]$. Actual
interior nonoverlap confines the open cap to one of the two free strips $2<x<z$ or
$z+1<x<L$. An open cap cannot lie on a vertical obstacle boundary or the seam between
squares 3 and 4, since a neighborhood would enter an obstacle interior.

Since $x_9=x_8+ac+s\le L-h$,

$$
X\le L-ac-2s\le\frac{213}{80}<3\le z+1.
$$

This excludes the right strip.
Interior points sufficiently near the top vertex occur on both sides of its abscissa, so
$2<X<z$. The argument still holds when that vertex touches $y=L$.

Let $m=\min(c,s)$ and $M_0=\max(c,s)$. At depth $d\le m$ below the top vertex, the
section endpoints are $X-cd/s$ and $X+sd/c$, with width $d/(cs)$. At depth $m$ the width
is $1/M_0\ge5/4$, whereas $G\le L-3\le21/25$. If $\delta\ge m$, sections strictly inside
the cap and approaching depth $m$ already violate this width bound.
Thus $0<\delta<m$, on either side of $c=s$ and at equality.
Limits of the contained open sections give the weak base inequalities

$$
X-c\delta/s\ge2,\qquad X+s\delta/c\le z,\qquad
\delta\le csG\le\frac{21}{50}.
\tag{5}
$$

The last bound also holds when $\delta\le0$, since $G\ge0$. The two base inequalities
are used only for a positive cap.
They permit contact with the bottom corners of the top-row squares.

Direct substitution gives

$$
sX-c\delta=cL-c-1/2-(B+b),\qquad
cX+s\delta=A+3/2-sL+s.
$$

Hence a positive cap implies

$$
B+b\le M:=cL-c-2s-1/2,\qquad
A\le cz+sL-s-3/2\le P:=u(L-1)-3/2.
\tag{6}
$$

Use the further abbreviations

$$
k=u+1/2,\qquad J=3/2+u-sL,\qquad K_5=cL-2c-s-1/2.
$$

Two strict gaps on the new interval will be needed:

$$
J-M\ge\frac{64}{725}>0,\qquad J-K_5\ge\frac3{125}>0.
\tag{7}
$$

For the first, $J-M\ge2-(46/25)c-(21/25)s$. Writing $c=\cos\theta$, $s=\sin\theta$, the
subtracted expression decreases on this interval because its derivative is
$-(46/25)s+(21/25)c<0$ by (3). Its maximum is at $t=2/5$, giving $64/725$. For the
second, $J-K_5\ge2-(21/25)c-(46/25)s$. The subtracted expression increases, since its
derivative is at least $(46/25)(3/5)-(21/25)(4/5)=54/125>0$. Its maximum is at $t=1/2$,
where the gap is $3/125$.

## Positive Slides: Complete Necessary SAT Reductions

Assume $0\le a,b\le1/4$. Put $X_6=p_x-1/2$, $Y_i=y_i-1/2$, and $\xi_i=L-1/2-x_i$ for
$i=7,9$. Equations (3)–(5), including $\delta\le21/50$ in both cap cases, give

| Quantity | Bound |
| --- | --- |
| $X_6,\xi_9$ | $[1/5,153/100]$ |
| $Y_6$ | $[3/5,69/50]$ |
| $Y_7$ | $[1/5,19/20]$ |
| $Y_9$ | $Y_9\ge22/25$ |
| $\xi_7$ | $\xi_7\ge1/5$ |

For example, $p_x\le L-h-c-3s/4\le203/100$, $p_y\ge h+c-s/4\ge11/10$ and
$p_y\le L-1-h-s+21/50\le47/25$. Also $Y_7\le L-3/2-h+21/50-3s/4-c\le19/20$, and
$y_9=y_7+s+bc\ge h+s$.

For pair 0–6, the negative $x,y,e$ alternatives fail by sign.
The positive and negative $f$ projections are bounded above respectively by

$$
\frac{73}{100}\frac{69}{50}-\frac{17}{25}\frac15
=\frac{4357}{5000}<D,
\qquad
\frac45\frac{153}{100}-\frac35\frac35
=\frac{108}{125}<D.
$$

The surviving alternatives all imply $A\ge k$. Direct positive $e$ separation is exactly
that row. Positive $x$ separation, together with square-7 bottom containment, gives

$$
A-k\ge s(2c-1-as)\ge0,
$$

because $2c-1-as\ge2(3/5)-1-(1/4)(4/5)=0$. This equality is retained.
If positive $y$ separates, then $p_y\ge1+h$. The case $\delta\le0$ would instead give
$p_y\le L-1-h-s\le73/50<1+h$, so the cap is positive.
Its $X>2$ gives $p_x>2-3c/2+s/2+bs$, and therefore

$$
A>k+c(1-2c+s+bs)\ge k,
$$

using $1-2c+s\ge1-146/100+17/25=11/50>0$. Thus the complete pair 0–6 condition forces

$$
A\ge k. \tag{8}
$$

For pair 1–7 the displacement is $(-\xi_7,Y_7)$, with positive magnitudes.
Positive $x$, negative $y$ and negative $f$ fail by sign.
Positive $y$ fails because $Y_7\le19/20<D$; positive $e$ is at most
$(4/5)(19/20)=19/25<D$. Negative $e$ would give $A+a\le cL-c-1/2$. By (8) and $a\ge0$,
this requires

$$
c(L-2)\ge1+s,
\qquad
c(L-2)\le\frac{1679}{1250}<\frac{42}{25}\le1+s,
$$

a contradiction. Exactly two possible alternatives remain:

$$
H_7:\ x_7\le L-1-h,
\qquad F_7:\ B\ge J. \tag{9}
$$

For pair 1–9, positive $x$, negative $y$ and negative $f$ fail by sign.
The negative $e$ projection is at most $(73/100)(153/100)=11169/10000<D$. The positive
$e$ direction needs a sharper uniform bound.
Containment gives $\xi_9\ge h-1/2$, and (5) gives

$$
Y_9\le L-3/2-h+cs(L-3)+s/4-c.
$$

Consequently

$$
sY_9-c\xi_9-D
\le F_L(c,s):=s(L-2)-1-2cs+cs^2(L-3)+s^2/4.
\tag{10}
$$

The coefficient of $L$ is $s+cs^2>0$, so replace $L$ by its upper bound only in this
inequality. For $F=F_{96/25}$,

$$
\frac{dF}{d\theta}
=\frac{46}{25}c-2c^2+2s^2
+\frac{21}{25}s(3c^2-1)+\frac12sc>0.
$$

Indeed, the first three terms are at least $963/1000$ by (3), and the remaining terms
are nonnegative because $3c^2-1\ge2/25$. At the upper endpoint $(c,s)=(3/5,4/5)$,

$$
F=-\frac{17}{3125}<0.
$$

Thus positive $e$ also fails throughout the interval, including its endpoints.
The full pair 1–9 condition leaves horizontal-left, vertical-above or positive $f$
separation. Horizontal-left implies positive $f$, since $y_9\ge h+s+bc$ gives

$$
s\xi_9+cY_9-D\ge c(2s-1+bc)>0
\quad\text{when }\xi_9\ge D.
$$

If vertical-above separates and $H_7$ holds, then $\xi_9=\xi_7-c+bs\ge D-c+bs$ and
$Y_9\ge D$, whence

$$
s\xi_9+cY_9\ge s(D-c+bs)+cD=D+bs^2\ge D.
$$

The identity used here is $D(u-1)=cs$. If vertical-above separates and $F_7$ holds, then
$B\ge J$ and $b\ge0$ already give $B+b\ge J$. Direct positive $f$ for pair 1–9 gives
this same row. Every alternative of both pair clauses is therefore covered, and

$$
B+b\ge J. \tag{11}
$$

If $\delta>0$, (6), (7) and (11) contradict one another.
If $\delta\le0$, the exact identity $sA+c(B+b)=p_y+bc$ and $y_8=p_y+s+bc\le L-1-h$ give

$$
s k+cJ\le L-1-h-s,
\qquad L(1+cs)\ge(1+u)^2. \tag{12}
$$

Since $cs=(u^2-1)/2$ and $1\le u\le\sqrt2$, this requires

$$
L\ge2+\frac{4u}{1+u^2}\ge2+\frac{4\sqrt2}{3}>\frac{96}{25}.
\tag{13}
$$

The middle inequality uses the decreasing function $u/(1+u^2)$ for $u\ge1$; the strict
comparison follows from $\sqrt2>69/50$. Both cap cases are impossible, including
$\delta=0$.

## Negative Slides: Complete Necessary SAT Reductions

Assume $a=-\alpha$, $b=-\beta$, with $0\le\alpha,\beta\le1/4$. First square 6 cannot
have a positive top cap.
If its depth were $\delta_6=p_y+h-(L-1)>0$ and its apex abscissa were $X_6=p_x+(c-s)/2$,
then

$$
\delta=\delta_6+s-\beta c>\delta_6>0,
\qquad X-X_6=c+\beta s>0.
$$

Square 8’s cap is central by the proved localization.
Square 6’s apex is left of square 8’s, so its cap also lies in the central strip; it
cannot be in the right strip.
Both caps are triangular by the same depth argument through $\min(c,s)$. Square 8’s
right base endpoint and square 6’s left base endpoint then give

$$
\begin{aligned}
G&\ge(X-X_6)+(s/c)\delta+(c/s)\delta_6\\
&=\frac1c+\frac{\delta_6}{cs}>\frac54>\frac{21}{25},
\end{aligned}
$$

a contradiction. Therefore

$$
p_y\le L-1-h. \tag{14}
$$

Set $X_0=p_x-1/2$, $Z=L-3/2-p_y$, and retain $\xi_i=L-1/2-x_i$, $Y_i=y_i-1/2$. Equations
(3)–(5) and (14) give

| Quantity | Bound |
| --- | --- |
| $X_0,\xi_9$ | $[1/5,151/100]$ |
| $Z$ | $[1/5,26/25]$ |
| $Y_9$ | $[279/400,73/50]$ |
| $Y_7$ | $[1/5,26/25]$ |
| $\xi_7$ | $\xi_7\ge1/5$ |

For the first upper bound use $p_x\le L-h-3c/4-s\le201/100$ and $x_9\ge h+3c/4+s$. For
$Z$, use $p_y\ge h+c+\alpha s$ and (14). For $Y_9$, use
$y_9=y_7+s-\beta c\ge h+s-\beta c$ and $y_9=L-1-h+\delta-\alpha s-c$. The latter also
explains why the cap bound is unconditional here.

For pair 5–6, the displacement is $(X_0,-Z)$. Negative $x$, positive $y$ and positive
$f$ fail by sign.
Negative $y$ fails because $Z\le26/25<D$. The positive and negative $e$
projections are at most

$$
\frac{73}{100}\frac{151}{100}-\frac{17}{25}\frac15
=\frac{9663}{10000}<D,
\qquad
\frac45\frac{26}{25}-\frac35\frac15
=\frac{89}{125}<D.
$$

The remaining alternatives are exactly

$$
p_x\ge h+1\quad\text{or}\quad B\le K_5. \tag{15}
$$

For pair 1–9, positive $x$, negative $y$ and negative $f$ fail by sign.
The negative and positive $e$ projections are at most

$$
\frac{73}{100}\frac{151}{100}-\frac{17}{25}\frac{279}{400}
=\frac{157}{250}<D,
\qquad
\frac45\frac{73}{50}-\frac35\frac15
=\frac{131}{125}<D.
$$

Horizontal-left separation implies positive $f$ because

$$
s\xi_9+cY_9-D\ge c(2s-1-\beta c)>0
\quad\text{when }\xi_9\ge D,
$$

using $2s-1-\beta c\ge71/400>0$. Thus the full pair 1–9 condition gives

$$
B-\beta\ge J\quad\text{or}\quad Y_9\ge D. \tag{16}
$$

In the upward case $Y_9\ge D$, pair 1–7 has $Y_7\ge D-s+\beta c$. Its positive $x$,
negative $y$ and negative $f$ alternatives fail by sign.
Positive $y$ fails because $Y_7\le26/25<D$; positive $e$ is at most
$(4/5)(26/25)=104/125<D$. The remaining horizontal-left alternative gives

$$
s\xi_7+cY_7\ge sD+c(D-s+\beta c)=D+\beta c^2\ge D.
$$

The remaining negative-$e$ alternative gives

$$
s\xi_7+cY_7\ge\frac{sD+Y_7}{c}
\ge D+\frac{s^2+\beta c}{c}>D,
$$

where $D(1+s-c)-s=s^2$. Both therefore imply positive $f$, the final direct alternative.
All three give $B\ge J$. The other case in (16) gives $B\ge J+\beta\ge J$ as well.
Combining with (7) and (15) proves, uniformly,

$$
B\ge J,\qquad p_x\ge h+1. \tag{17}
$$

If $\delta>0$, (6) gives $A\le P$, whereas $cA=p_x+sB\ge h+1+sJ$. Thus $cP\ge h+1+sJ$.
Expansion yields precisely $L(1+cs)\ge(1+u)^2$, contradicting (13).

If $\delta\le0$, then $Y_9\le L-3/2-h-c\le26/25<D$. Equation (16) therefore forces
$B-\beta\ge J$. Together with $p_x\ge h+1$ and $p_y\ge h+c+\alpha s$,

$$
A\ge c(h+1)+s(h+c+\alpha s)
=k+s(2c-1)+\alpha s^2\ge k.
$$

Finally, $sA+c(B-\beta)=p_y-\beta c\le L-1-h-s$ follows from the below-top condition for
square 8. It gives (12) and the same contradiction (13). The negative child is empty on
the entire new interval.

## Controls, Coverage and Unresolved Implication

The partial proofs use only necessary conditions of actual target squares.
The core argument is a proved projection for exclusion, and its feasible points have
never been treated as target witnesses.
The cap arguments use open interiors and limits to weak base inequalities.
Every SAT alternative of each pair used in the contradiction has been screened or shown
to imply a retained row.
Unused containment rows and pair clauses remain in the target definition.
Neither argument restricts square 10 or divides by $a,b,c-s$ or an angle difference.
The central proof divides only by positive $c,s,cs,1+cs$; the core proof covers both
axis endpoints without those divisions.

The finite controls were checked at their stated scope:

- The admitted exact Trump source is retained as the parent control.
  Its isolated source side satisfies $U>387/100>96/25$, so it is refused as a target
  witness. The existing exact source replay was not rerun.
- At $t=0$ the block offsets are $(0,0),(a,-1),(1,b),(1+a,b-1)$. At $t=1$ they are
  $(0,0),(1,a),(-b,1),(1-b,1+a)$. Both are regular and both are excluded by (2); holding
  the parameters fixed has not been asserted to preserve the labeled geometry between
  them.
- At $c=s$, the cap proof uses $\min(c,s)$ and has no singularity.
  The corner formulas and highest-corner labels remain those of the domain.
  No reflected-half-chart transfer is used.
- At $(a,b)=(1/8,-1/8)$ the 7–8 displacement has common coordinates $(7/8,7/8)$ and
  overlaps; at $(-1/8,1/8)$ the 6–9 displacement is $(7/8,-7/8)$ and overlaps.
  At $a=b=0$ the block’s diagonal point contacts remain legal component controls.
- The pair inventory stays $15+24+6+10=55$, with 44 containment rows, all eleven actual
  squares, nine flush incidences and six positive segments.
  No witness is asserted and no source-selected SAT branch defines the target.

The original eight closed children now have this author-level disposition:

| Original interval, for each sign | Covered by this report and accepted prior results | Still unresolved in this report |
| --- | --- | --- |
| $[0,1/3]$ | $[0,1/24]$ and the accepted endpoint $1/3$ | $(1/24,1/3)$ |
| $[1/3,2/5]$ | The accepted BC273/276 theorem | None |
| $[2/5,\tau]$ | The new central proof, including $\tau=\sqrt2-1$ | None |
| $[\tau,1]$ | $[\tau,1/2]$ and $[23/25,1]$ | $(1/2,23/25)$ |

All statements quantify over both side endpoints, both $z$ endpoints, every slide
boundary and zero slide, all weak containment and SAT equalities, every $v,w$, $v=t$,
physical angle coincidences $(0,1),(1,0)$ and every recontact.
No margin split has been made.
The two closed remainder intervals displayed at the start preserve overlap with the
proved intervals and cover every remaining possibility.

The missing implication is an exclusion or an actual eleven-square witness on that
remainder under the unchanged full conditions.
No forced cap position or SAT row has been proved there by this report.
The high-angle and low-angle portions have not been identified through a reflection.
The report supplies no unrestricted packing bound, global capture, finite-motion
theorem, H120 uniform-LP readiness or H118 comparison result.

## Work Receipt

The prospective author window began at `2026-09-07T12:36:00Z` and ends at the absolute
hard stop `2026-09-07T13:06:00Z`. The first actual clock read was
`2026-09-07T12:38:54Z`. The work used exact hand analysis only.
No target computation, numerical solver, scientific script, engine, resource search,
dependency change, Git mutation or shared-record edit was performed.
Only this assigned author report was written.
The independent adversary’s report was not read, and target reasoning was not exchanged
with the adversary or reserved auditor.
The complete mathematical readback froze at `2026-09-07T13:02:35Z`, 1421 seconds after
the first actual clock and 205 seconds before the hard stop.
The report received the common-document and de-slop passes.
Installed Flowmark 0.4.0 formatted this assigned file with caching disabled; its scoped
auto-format check passed at the freeze clock.
The trailing-whitespace scan found no matches, and the required footer occurred exactly
once. All six native link targets were checked again with shell initialization disabled
at `2026-09-07T13:02:52Z`, 1438 seconds after the actual start, and existed.
An earlier link check had passed but printed unrelated shell-startup warnings; the clean
repeat produced none.
The receipt receives a final scoped formatting check before terminal handoff.
No mathematical continuation or background command follows this freeze.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
