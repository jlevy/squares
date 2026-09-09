# BC-276: Negative-Slide Author’s Analytical Exclusion

**Proposed result for independent audit: the complete frozen domain $N$ is empty.** The
contradiction already occurs among the ten-square skeleton’s necessary conditions.
It uses the left-wall square 5 to replace the positive pilot’s sign-dependent SAT
implications. Both possible positions of square 8 relative to the top unit strip force

$$
L\ge\frac{4900}{1261}>\frac{96}{25}.
$$

This is the author’s candidate proof, not an independently accepted campaign verdict.
Its scope is the entire [BC276 protocol](bc-276-negative-slide-protocol.md), with the
exact parameterization and closed boundaries accepted in the
[domain review](bc-276-negative-slide-domain-review.md).
Containment of all eleven squares, all 55 complete pair disjunctions, both square-10
axis lifts, equal angles, zero slides and recontacts remain in the target.
Using a subset of its necessary conditions for a contradiction does not delete the other
defining conditions.

The author worked independently of the concurrent adversary and did not read that report
or receive its reasoning.
The workflow is session092 phase 8, W3 `insight-iteration`, BC276 under H120. The frozen
protocol and domain review were committed at `4ac71438` and the coordinator reported all
31 record checks passed before dispatch.
No numerical search, solver or target script was used.
The calculations are hand derivations; one failed exact hand proposal is retained below.

## Coordinates and Exact Bounds

Write $\alpha=-a$ and $\beta=-b$, so $0\le\alpha,\beta\le1/4$. Use the
[source-feature equations](bc-273-release-domain-design.md), with

$$
c=\frac{1-t^2}{1+t^2},\quad s=\frac{2t}{1+t^2},\quad
e=(c,s),\quad f=(-s,c),\quad
u=c+s,\quad h=u/2,\quad D=h+1/2,
$$

and put $A=e\cdot p$, $B=f\cdot p$. The common support sum of an axis unit square and a
block unit square is exactly $D$ on each of the four candidate SAT axes $x,y,e,f$. Every
pair considered below therefore requires at least one of its eight directed center
projections to be at least $D$, with equality legal.

The unchanged angle interval gives

$$
\frac{21}{29}\le c\le\frac45,\qquad
\frac35\le s\le\frac{20}{29},\qquad
\frac75\le u\le\frac{41}{29},\qquad c>s>0.
\tag{1}
$$

These follow by differentiating the rational functions on $1/3\le t\le2/5$;
$u'(t)=2(1-2t-t^2)/(1+t^2)^2>0$ there.
For the SAT screening we use the weaker bounds

$$
\frac{18}{25}\le c\le\frac45,\qquad
\frac35\le s\le\frac7{10},\qquad
\frac7{10}\le h\le\frac{71}{100},\qquad D\ge\frac65,
\quad c^2+s^2=1,\quad cs\le\frac12.
\tag{2}
$$

In ordinary coordinates the block centers are

$$
\begin{aligned}
C_6&=(p_x,p_y),\\
C_7&=(p_x-\alpha c+s,\ p_y-\alpha s-c),\\
C_8&=(p_x+c+\beta s,\ p_y+s-\beta c),\\
C_9&=(p_x+(1-\alpha)c+(1+\beta)s,
       \ p_y+(1-\alpha)s-(1+\beta)c).
\end{aligned}
\tag{3}
$$

Containment of squares 6, 7 and 9 gives

$$
p_x\ge h,\qquad
p_x\le L-h-(1-\alpha)c-(1+\beta)s,\qquad
p_y\ge h+c+\alpha s.
\tag{4}
$$

The short negative slides satisfy

$$
s-\beta c\ge\frac25>0,\qquad s-\alpha c\ge\frac25>0.
\tag{5}
$$

Thus square 8 is above square 6 and square 9 is to the right of square 8. No division by
a slide or an angle difference occurs.

## The Top Cap and the Position of Square 6

The top-row obstacles are exactly

$$
[0,2]\times[L-1,L]
\quad\text{from squares 3 and 4},\qquad
[z,z+1]\times[L-1,L]
\quad\text{from square 2}.
$$

Define the top penetration and apex abscissa of square 8 by

$$
\delta_8=y_8+h-(L-1),\qquad X_8=x_8+(c-s)/2.
$$

Suppose first that $\delta_8>0$. Since $x_9=x_8+s-\alpha c\le L-h$, we have

$$
X_8\le L-2s+\alpha c
\le\frac{71}{25}<3\le z+1.
\tag{6}
$$

The portion of the interior of square 8 in $L-1<y<L$ is nonempty, open and convex.
It cannot meet any boundary of a top-row obstacle within this open strip: an open
neighborhood of such a point would also meet that obstacle’s interior.
Consequently it lies in one connected free strip, either $2<x<z$ or $z+1<x<L$. Points
approaching the highest vertex have horizontal coordinate approaching $X_8$; (6)
excludes the right strip.
The entire open cap lies in the central gap, and

$$
2<X_8<z.
\tag{7}
$$

Equality at either side in (7) would make sections just below the apex enter the
adjacent obstacle’s interior.
This remains true if the apex touches the top container wall.
When $z=2$, (7) itself excludes a positive cap.

We must have $\delta_8<s$. At depth $s$ below the top vertex, the horizontal section of
the rotated square has width $1/c\ge5/4$, whereas $z-2\le L-3\le21/25$. If $\delta_8>s$,
this section lies inside the top strip.
If $\delta_8=s$, sections just above its lower boundary approach that width and already
exceed the gap. Both contradict the open-cap containment in the gap.

For $0<\delta_8<s<c$, the cap is triangular, and its limiting section at $y=L-1$ has
endpoints $X_8-c\delta_8/s$ and $X_8+s\delta_8/c$. Therefore

$$
X_8-\frac cs\delta_8\ge2,\qquad
X_8+\frac sc\delta_8\le z,
\qquad
\delta_8\le cs(z-2)\le cs(L-3)\le\frac{21}{50}.
\tag{8}
$$

These endpoint inequalities are weak, so touching a bottom corner of a top-row square
remains legal. Substitution in the right endpoint inequality gives

$$
A\le cz+sL-s-\frac32
\le u(L-1)-\frac32.
\tag{9}
$$

For clarity, that substitution uses the exact identity

$$
X_8+\frac sc\delta_8
=\frac{A+3/2-sL+s}{c};
$$

the $\beta$ terms cancel.
The coarse upper bound $\delta_8\le21/50$ also holds when $\delta_8\le0$.

**Square 6 cannot have a positive top cap.** Write $\delta_6=p_y+h-(L-1)$ and
$X_6=p_x+(c-s)/2$ for this paragraph only.
If $\delta_6>0$, then

$$
\delta_8=\delta_6+s-\beta c>\delta_6>0,
\qquad X_8-X_6=c+\beta s>0.
$$

The preceding cap argument applies to square 8. Square 6’s apex is to its left, so it
cannot belong to the right free strip either.
Its open cap must also lie in $2<x<z$. Both caps are triangular because
$0<\delta_6<\delta_8<s$. Their limiting base endpoints satisfy

$$
X_6-\frac cs\delta_6\ge2,
\qquad X_8+\frac sc\delta_8\le z.
$$

Subtracting gives the impossible inequality

$$
z-2\ge
(X_8-X_6)+\frac sc\delta_8+\frac cs\delta_6
=\frac1c+\frac{\delta_6}{cs}
>\frac54>\frac{21}{25}\ge z-2.
$$

The equality $\delta_6=0$ was not discarded.
We have proved the weak necessary condition

$$
p_y\le L-1-h.
\tag{10}
$$

## Three Complete SAT Reductions

Define

$$
J=\frac32+u-sL,
\qquad K_5=cL-2c-s-\frac12.
\tag{11}
$$

Their gap is uniformly positive on the frozen box:

$$
\begin{aligned}
J-K_5
&=2+3c+2s-L(c+s)\\
&\ge2-\frac{21}{25}c-\frac{46}{25}s\\
&\ge2-\frac{21}{25}\frac45-\frac{46}{25}\frac7{10}
=\frac1{25}>0.
\end{aligned}
\tag{12}
$$

### Pair 5–6: horizontal-right or negative $f$

Put $X=p_x-1/2$ and $Z=L-3/2-p_y$. The center difference from square 5 to square 6 is
$(X,-Z)$. Equations (2), (4) and (10) give

$$
\frac15\le X\le\frac32,
\qquad \frac15\le Z\le\frac{23}{25}.
\tag{13}
$$

For the upper bound on $X$, use $p_x\le L-h-(3/4)c-s$; for the upper bound on $Z$, use
$p_y\ge h+c$. Both coordinates are positive.
The vertical alternatives fail since $Z<D$. The two $e$ projections satisfy

$$
cX-sZ\le\frac{27}{25}<D,
\qquad sZ-cX\le\frac12<D.
$$

The negative $x$ and positive $f$ alternatives fail by sign.
Thus every legal SAT alternative for pair 5–6 implies at least one of

$$
p_x\ge h+1
\quad\text{or}\quad
B\le K_5.
\tag{14}
$$

The second is exactly negative-$f$ separation: $sX+cZ\ge D$ is equivalent to $B\le K_5$.

### Pair 1–9: positive $f$ or upward separation

Write $\xi_i=L-1/2-x_i$ and $Y_i=y_i-1/2$ for $i=7,9$. The center difference from square
1 to square 9 is $(-\xi_9,Y_9)$. Containment and (2)–(5), (8) give

$$
\frac15\le\xi_9\le\frac32,
\qquad \frac35\le Y_9\le\frac{67}{50}.
\tag{15}
$$

Here $y_9=y_7+s-\beta c\ge h+s-\beta c\ge11/10$ gives the lower bound on $Y_9$. The
upper bound follows from $y_9=y_8-\alpha s-c\le L-1-h+21/50-c\le46/25$. The upper bound
on $\xi_9$ uses $x_9\ge h+(3/4)c+s$.

Both $e$ directions are strictly below their support threshold:

$$
c\xi_9-sY_9\le\frac{21}{25}<D,
\qquad sY_9-c\xi_9\le\frac{397}{500}<D.
$$

The positive $x$, negative $y$ and negative $f$ directions fail by sign.
If the horizontal-left alternative holds, $\xi_9\ge D$, then

$$
\begin{aligned}
s\xi_9+cY_9-D
&\ge sD+c(h+s-\beta c-1/2)-D\\
&=c(2s-1-\beta c)\ge0.
\end{aligned}
\tag{16}
$$

The last inequality uses $2s-1\ge1/5$ and $\beta c\le1/5$. It includes the exact
equality at their shared extremal values.
Thus horizontal-left separation also implies positive-$f$ separation.
Every legal alternative consequently gives

$$
B-\beta\ge J
\quad\text{or}\quad
Y_9\ge D.
\tag{17}
$$

The first is the exact positive-$f$ row for pair 1–9, since its block $f$ coordinate is
$B-1-\beta$.

### Pair 1–7 when square 9 separates upward

Assume the second alternative in (17), namely $Y_9\ge D$. Then

$$
Y_7=Y_9-s+\beta c\ge D-s+\beta c.
\tag{18}
$$

We also have $\xi_7>0$, $Y_7>0$ by containment, and

$$
y_7=y_8-(1+\alpha)s-(1-\beta)c
\le L-1-h+\frac{21}{50}-s-\frac34c
\le\frac{71}{50}.
$$

Hence $Y_7\le23/25<D$ and $sY_7\le161/250<D$. For the displacement $(-\xi_7,Y_7)$,
positive $x$, negative $y$ and negative $f$ fail by sign, and positive $y$ and positive
$e$ fail by the displayed strict bounds.
The remaining possibilities are horizontal-left, negative $e$, and positive $f$.

If horizontal-left separation holds, $\xi_7\ge D$, then (18) gives

$$
s\xi_7+cY_7
\ge sD+c(D-s+\beta c)
=D+\beta c^2\ge D.
\tag{19}
$$

If negative-$e$ separation holds, $c\xi_7-sY_7\ge D$, then

$$
\begin{aligned}
s\xi_7+cY_7
&\ge\frac{sD+Y_7}{c}\\
&\ge\frac{D(1+s)-s+\beta c}{c}
=D+\frac{s^2+\beta c}{c}>D.
\end{aligned}
\tag{20}
$$

The identity in the last line is $D(1+s-c)-s=s^2$, using $c^2+s^2=1$. Thus both
remaining alternatives imply the positive-$f$ alternative itself.
Because square 7 has block $f$ coordinate $B-1$, every legal pair 1–7 gives

$$
B\ge J
\quad\text{whenever }Y_9\ge D.
\tag{21}
$$

Equations (17) and (21), together with $\beta\ge0$, now prove $B\ge J$ throughout the
whole target.
Equations (12) and (14) exclude the $B\le K_5$ alternative for pair 5–6. We
have obtained the two uniform necessary conditions

$$
B\ge J,
\qquad p_x\ge h+1.
\tag{22}
$$

## Both Positions of Square 8 Are Impossible

### A positive top cap

If $\delta_8>0$, use $p_x=cA-sB$ with (22):

$$
cA=p_x+sB\ge h+1+sJ.
$$

Combine this with the right-cap inequality (9):

$$
c\left(u(L-1)-\frac32\right)\ge h+1+sJ.
$$

Substituting $J=3/2+u-sL$ and collecting terms yields

$$
L(1+cs)\ge(1+u)^2,
\quad\text{or}\quad
L\ge2+\frac{2u}{1+cs}.
\tag{23}
$$

### Square 8 wholly below the top strip

If $\delta_8\le0$, then

$$
y_9=y_8-\alpha s-c
\le L-1-h-c\le\frac{71}{50},
$$

so $Y_9\le23/25<D$. The upward alternative in (17) is impossible; the complete pair 1–9
reduction therefore forces the stronger row $B-\beta\ge J$. The bound $p_x\ge h+1$ in
(22), together with (4), gives

$$
\begin{aligned}
A&\ge c(h+1)+s(h+c+\alpha s)\\
&=u+\frac12+s(2c-1)+\alpha s^2
\ge u+\frac12.
\end{aligned}
\tag{24}
$$

Square 8’s below-top condition is $p_y-\beta c\le L-1-h-s$. The exact identity
$p_y-\beta c=sA+c(B-\beta)$ now gives

$$
L-1-h-s
\ge s\left(u+\frac12\right)+cJ.
$$

After substitution, this is again precisely (23). The equality case $\delta_8=0$ belongs
to this second case.

Finally, $cs=(u^2-1)/2$, so

$$
2+\frac{2u}{1+cs}
=2+\frac{4u}{1+u^2}
\ge2+\frac{4(41/29)}{1+(41/29)^2}
=\frac{4900}{1261}.
\tag{25}
$$

The function $u/(1+u^2)$ decreases for $u>1$, and (1) places $u$ in $[7/5,41/29]$. The
contradiction has exact rational margin

$$
\frac{4900}{1261}-\frac{96}{25}
=\frac{1444}{31525}>0.
$$

Both cases are excluded, so the proposed conclusion is $N=\varnothing$.

## Failed Transfer, Coverage and Audit Obligations

An initial hand proposal used

$$
L=96/25,\quad t=1/3,\quad a=0,\quad b=-1/4,\quad
p=(7/5,21/10),\quad z=L-1.
$$

It gives $C_7=(2,13/10)$, $C_8=(47/20,5/2)$ and $C_9=(59/20,17/10)$. It is not a
feasible skeleton. Relative to square 5, square 6 has displacement $(9/10,-6/25)$, with
absolute $x,y,e,f$ projections

$$
9/10,\quad 6/25,\quad72/125,\quad183/250,
$$

all strictly below $D=6/5$. Thus that pair overlaps, without needing to check the
proposal’s remaining pair conditions.
No square-10 pose or eleven-square witness was asserted.
This failure directed attention to the full pair 5–6 disjunction.

The positive pilot’s implication from upward pair 1–9 separation to its positive-$f$
separation cannot be transferred directly.
Combining that upward separation with horizontal-left pair 1–7 separation gives only
$s\xi_9+cY_9\ge D-\beta s^2$. For negative slides this does not reach $D$. The argument
here instead derives positive-$f$ separation for **pair 1–7**, giving $B\ge J$, and
compares it with square 5’s negative-$f$ row.
This records the failed premise rather than treating the positive proof as a control
inside $N$.

The proof uses only containment, the retained block equations, the top-row rectangles
and complete SAT conditions on pairs 5–6, 1–9 and 1–7. Its cap geometry additionally
uses the necessary nonoverlap of squares 6 and 8 with the top-row obstacles.
Square 0 and square 10 are not needed in the contradiction.
No omitted pair could restore feasibility to this inconsistent subset of the defining
conditions.

An independent reader must check the open-cap localization, the two-cap width identity,
the support thresholds, every screened directed alternative in (14), (17) and (21), the
weak equality in (16), and the two separate derivations of (23). All slide endpoints
remain present; there is no division by $\alpha$, $\beta$, their product, or a square-10
angle. The conclusion is independent of $v,w$, but it is restricted to the frozen block
angle, slide box, contact sides and wall assignments.

If this proof is accepted, the already accepted positive-child exclusion and the
reviewed identity $S=T_+\cup N$ close the signed short-slide parent $S$. Other block
angles, longer slides, changed wall/contact assignments and any global representative
theorem remain outside the conclusion.
There is no claim of an unrestricted packing-bound improvement or an H118
resource-versus-LP separation.

## Timing and Document Checks

The prospective author lease was `2026-09-07T09:00:45Z` through `2026-09-07T09:25:45Z`;
the first clock read after dispatch was `2026-09-07T09:01:11Z`. The full candidate
contradiction was reported privately to the coordinator at approximately
`2026-09-07T09:10:00Z`, with an explicit request to preserve the independence of the
concurrent adversary.
Only this assigned report was written.
No registry, Git state, identifier, dependency or other worker’s file was changed.

The author’s mathematical work and final document review completed at
`2026-09-07T09:17:26Z`, before the hard deadline.
The full proof received the common-documentation and de-slop passes.
Installed Flowmark 0.4.0 formatted this assigned file with caching disabled and passed
its full auto-format check.
All three linked files exist, the required footer appears once, and no trailing
whitespace was found.
The displayed equations were reread after formatting.
No background command remains.
These document checks do not substitute for the independent mathematical audit.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
