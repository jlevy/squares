# BC-270: A Parent Compatibility Restriction From the Other Seven Squares

**Independently accepted direct geometric result:** a finite alternating fence condition
on four central-band squares leaves room for at most four further unit squares.
The exact central four-diamond fixture satisfies the condition strictly, as therefore
does a continuous family of four-square poses.
Seven additional full squares cannot coexist with that family.
This removes the central fixture and its five-square anchored extension from an
eleven-square parent for a proved residual reason.
The [independent review](bc-270-parent-compatibility-review.md) accepts the geometry and
identifies a redundant-remainder issue, corrected explicitly below on 2026-09-07.

The condition below is a list of inequalities in the actual four poses.
It uses no preset center box, fitted orientation interval, assumed residual anchor or
residual packing-number oracle.
The other seven squares supply the contradiction through their radius-$1/2$ incircles
and four explicitly constructed regions.
The lower and upper band siblings remain open.
No surviving coupled-LP witness is supplied, so
[H118](../../../../hypotheses/H-118-capacity-versus-coupled-lp.md) and BC271 remain
blocked as a strength comparison.

This is BC270’s remaining parent-compatibility design slice in session092 phase 7. Only
hand mathematics and document checks were used; no target computation, resource search
or solver ran.

## Complete Parent and Seam Ownership

Write $q=96/25$, $b=1/2$ and $d=q-1/2=167/50$. Preserve the
[accepted three-band split](bc-270-capacity-comparison-design.md):

$$
B_0=[1/2,217/150],\quad B_1=[217/150,359/150],\quad
B_2=[359/150,167/50].
$$

Every contained unit-square center lies in $[b,d]^2$. For the counting argument, assign
a vertical seam to its lower-index band.
Eleven assigned centers put four in some band.
For each band $j$, every four-label subset $I$, and every ordering $\pi$ of its labels,
retain the closed parent $P_{j,I,\pi}$ that puts those four centers in $B_j$ and orders
them weakly by horizontal coordinate.
This is a finite overlapping cover.
Weak-order ties, band seams and additional centers in the same band remain represented.

Each parent contains all eleven actual unit squares.
Orientations use the complete closed chart $[-\pi/4,\pi/4]$ modulo quarter turns, with
both seam lifts retained.
For square $i$, let $Q_i$ be its centered unit square, with orthonormal basis $e_i,f_i$
and center $C_i$. Define

$$
H_i(n)=\tfrac12(|n\cdot e_i|+|n\cdot f_i|),\qquad
h_i=H_i((1,0))=H_i((0,1)).
$$

Impose all eleven containment conditions $h_i\le C_{i,x},C_{i,y}\le q-h_i$ and all 55
weak SAT disjunctions

$$
\bigvee_{n\in\{e_i,f_i,e_j,f_j\},\ \sigma\in\{-1,1\}}
\sigma(C_j-C_i)\cdot n\ge H_i(n)+H_j(n),\qquad i<j.
$$

No pair or direction is selected from a source packing.
The seven labels outside $I$ have no additional position or angle restriction.
The proposed closed child $D$ is $P_{1,I,\pi}$ with the fence guards below.
The same statement applies to every label choice and ordering; it is not a
label-specific packing assumption.
Distinguish the guarded four-pose set $\Gamma$, defined by the four-square containment,
six pair conditions, band/order conditions and these guards, from $D$. The fixture
belongs to $\Gamma$. The full eleven-square $D$ additionally requires seven other
squares and all their conditions, and is empty by the accepted capacity proof.

## Universal Guard Polygons

Let $\mathcal D(m)=\{(x,y):|x|+|y|\le m\}$. Every actual unit square $Q_i$ contains
$\mathcal D(m_i)$, where

$$
m_i=\frac{1}{2\max(|e_{i,x}|,|e_{i,y}|,|f_{i,x}|,|f_{i,y}|)}.
$$

Indeed each of the four diamond vertices satisfies both square coordinate inequalities;
convexity gives the entire diamond.
This is an exact orientation-dependent core, with $1/2\le m_i\le1/\sqrt2$, rather than a
substituted average angle.

Fix the closed octagon

$$
E=\{(x,y): |x|,|y|\le2/5,\quad |x|+|y|\le699/1000\}.
$$

Its eight vertices have coordinate magnitudes $2/5$ and $299/1000$. Their squared norm
is $249401/1000000<1/4$. Thus the whole closed $E$ lies strictly inside the radius-$1/2$
disk. Since every residual unit square contains that disk, a residual center in
$C_i+\mathcal D(m_i)+E$ forces interior overlap with square $i$, whatever the residual
orientation. This assertion includes the guard boundary: the guard lies inside the open
forbidden-center set.
It does not declare touching unit squares illegal.

Write the selected four centers, in horizontal order, as $(x_i,y_i)$ for slots
$i=0,1,2,3$. Define their two virtual row heights and actual row scatter by

$$
\ell=(y_0+y_2)/2,\quad u=(y_1+y_3)/2,\quad
\varepsilon=\tfrac12\max(|y_0-y_2|,|y_1-y_3|),\quad
m=\min_{i=0}^3m_i.
$$

Put

$$
k=299/1000,\quad A=m+2/5-\varepsilon,\quad R=A+k,
\quad \Delta=u-\ell,\quad \beta=999/1000.
$$

The four guard polygons $K_i$ are centered at $(x_i,\ell)$ for even $i$ and $(x_i,u)$
for odd $i$, with inequalities

$$
|X-x_i|\le A,\quad |Y-v_i|\le A,\quad
|X-x_i|+|Y-v_i|\le R,
\qquad v_i=\begin{cases}\ell&i\text{ even},\\u&i\text{ odd}.\end{cases}
$$

The octagon $\mathcal D(m_i)+E$ has axis bound $m_i+2/5$ and diagonal bound
$m_i+699/1000$. Its vertices are obtained by adding the corresponding diamond and $E$
vertices. Moving from a virtual row to the actual center costs at most $\varepsilon$ in
each relevant absolute-value inequality.
Hence

$$
K_i\subseteq C_i+\mathcal D(m_i)+E.
$$

This proves that every residual center avoids every closed $K_i$. No target pose is used
in this implication.

## Finite Fence Guards and Four Regions

Require the following weak inequalities:

$$
\begin{gathered}
b\le\ell\le u\le d,\qquad 0\le\Delta\le A-k,\\
\ell-A\le b,\qquad u+A\ge d,\\
x_0\le b+k,\qquad x_3\ge d-k,\qquad
x_{i+1}-x_i\le2k+\Delta\quad(i=0,1,2).
\tag{F}
\end{gathered}
$$

These express a fence reaching both horizontal center boundaries, with consecutive guard
intervals joined in the overlap of the two rows.
Their consequences are derived below, not assumed as a capacity condition.

Define

$$
\begin{aligned}
y_B&=\ell-R+(x_2-x_0)/2,& w_B&=2(y_B-b),\\
y_T&=u+R-(x_3-x_1)/2,& w_T&=2(d-y_T),\\
y_L&=u+R+b-x_1,& v_L&=d-y_L,\\
x_R&=x_2+R-\ell+b,& w_R&=d-x_R,\\
y_R&=u-A,& h_R&=y_R-b.
\end{aligned}
$$

The four regions are convex hulls of these explicit vertices:

| Region | Vertices |
| --- | --- |
| Bottom middle $P_B$ | $(x_0+R-\ell+b,b)$, $(x_2-R+\ell-b,b)$, $((x_0+x_2)/2,y_B)$ |
| Bottom right $P_R$ | $(x_R,b)$, $(d,b)$, $(d,y_R)$, $(x_R+h_R,y_R)$ |
| Top left $P_L$ | $(b,y_L)$, $(b,d)$, $(b+v_L,d)$ |
| Top middle $P_T$ | $((x_1+x_3)/2,y_T)$, $(x_1+R+u-d,d)$, $(x_3-R-u+d,d)$ |

As part of the definition of $D$, require all displayed vertices to lie in $[b,d]^2$,
$w_B,w_T,v_L\ge0$, and $0\le h_R\le w_R$. These are finitely many explicit weak
coordinate inequalities.
Finally require

$$
w_B\le\beta,\quad w_T\le\beta,\quad
2v_L^2\le\beta^2,\quad w_R^2+h_R^2\le\beta^2.
\tag{C}
$$

The two middle triangles have diameter their horizontal base length, respectively
$w_B,w_T$. The top-left triangle has diameter $\sqrt2v_L$. The bottom-right trapezoid
has diameter $\sqrt{w_R^2+h_R^2}$; its other vertex distances are no larger because
$0\le h_R\le w_R$. Thus every region has diameter at most $\beta<1$.

All guards depend continuously on the actual poses and use only weak inequalities.
Together with the compact complete parent, they define a closed compact $D$. There is no
requirement that the actual row heights coincide, that the angles equal $\pi/4$, or that
any selected square touch another square or a wall.

## Proof That the Fence Covers Every Residual Center

At height $Y$ within a guard row of height $v$, its horizontal section has radius

$$
r_v(Y)=\min(A,R-|Y-v|),\qquad |Y-v|\le A.
$$

The first guard gives $A\ge k>0$. On the overlap $u-A\le Y\le\ell+A$, both row radii are
defined. Each is a concave piecewise affine function.
At either overlap endpoint their sum is $2k+\Delta$: the condition $\Delta\le A-k$
ensures that the uncapped radius there is at most $A$. Concavity therefore gives
$r_\ell(Y)+r_u(Y)\ge2k+\Delta$ throughout the overlap.

Consecutive horizontal guard intervals overlap by (F). The first interval reaches $X=b$
and the last reaches $X=d$, because each active radius is at least $R-A=k$. Consequently
the four guards cover the whole horizontal center interval throughout that vertical
overlap.

Below it, $b\le Y\le u-A\le\ell$, only the low row is needed.
Its radius is exactly $R-\ell+Y$: at the largest such height,
$R-\ell+u-A=k+\Delta\le A$, and at $Y=b$ the row is active by $\ell-A\le b$. The
interval from slot 0 reaches the left boundary.
Any center avoiding the low-row intervals must therefore satisfy either

$$
x_0+R-\ell+Y\le X\le x_2-R+\ell-Y
$$

or

$$
X\ge x_2+R-\ell+Y.
$$

The first region is contained in $P_B$. The second, with $Y\le u-A$, is contained in
$P_R$. These weak enlargements retain every possible boundary point.

Above the overlap, $\ell+A\le Y\le d$, the high-row radius is exactly $R+u-Y$ by the
same inequalities. Its last interval reaches the right boundary.
A center avoiding both high-row intervals lies to their left or between them, giving
respectively $P_L$ and $P_T$. Therefore

$$
[b,d]^2\setminus\bigcup_{i=0}^3K_i
\subseteq P_B\cup P_R\cup P_L\cup P_T.
$$

Every residual unit-square center belongs to this union, and two residual centers in one
region would have distance at most $\beta<1$. Their radius-$1/2$ incircle interiors
would overlap, contradicting unit-square interior disjointness.
Assign a center on a region seam to its lowest-index containing region.
At most four residual squares fit.
In particular, the other seven squares of every eleven-square parent rule out $D$. This
is a concrete complement-capacity proof $\kappa(G)\le4$, not the unproved assertion
$\kappa(G)\le6$.

## The Original Fixture and a Continuous Family

For the central fixture, take the exact accepted values

$$
x_i=18/25+4i/5,\quad y_0=y_2=8/5,\quad y_1=y_3=23/10,
\quad \theta_i=\pi/4.
$$

Writing $h=1/\sqrt2$, one has $m=h$, $\varepsilon=0$, $\ell=8/5$, $u=23/10$, $A=h+2/5$,
$R=h+699/1000$ and $\Delta=7/10$. The exact comparisons $7071^2<50000000<7072^2$ give
$7071/10000<h<7072/10000$. The nontrivial fence inequalities include

$$
\ell-A=6/5-h<1/2,\qquad u+A=27/10+h>d,
\qquad \Delta<A-k=h+101/1000,
$$

$$
x_0=18/25<b+k=799/1000,\quad
x_3=78/25>d-k=3041/1000,\quad
x_{i+1}-x_i=4/5<2k+\Delta=1298/1000.
$$

The region sizes simplify to

$$
w_B=1201/500-2h<9878/10000<\beta,
\quad w_T=1141/500-2h<8678/10000<\beta,
$$

$$
v_L=1361/1000-h<2/3,
\quad w_R=1421/1000-h<143/200,
\quad h_R=7/5-h<139/200.
$$

Thus $2v_L^2<8/9<\beta^2$ and

$$
w_R^2+h_R^2<\frac{143^2+139^2}{200^2}
=\frac{3977}{4000}<\beta^2.
$$

Here $0<h_R<w_R$ with $w_R-h_R=21/1000$. The specialized vertices make every remaining
coordinate bound explicit:

| Region | Fixture vertices |
| --- | --- |
| $P_B$ | $(h+319/1000,b)$, $(2721/1000-h,b)$, $(38/25,1701/1000-h)$ |
| $P_R$ | $(1919/1000+h,b)$, $(d,b)$, $(d,19/10-h)$, $(3319/1000,19/10-h)$ |
| $P_L$ | $(b,1979/1000+h)$, $(b,d)$, $(1861/1000-h,d)$ |
| $P_T$ | $(58/25,2199/1000+h)$, $(1179/1000+h,d)$, $(3461/1000-h,d)$ |

All vertices belong to the center box by the displayed exact $h$ enclosure.
Coordinates not identically on a specified box edge have strict clearance from that
edge.

The original four-square containment, all six pair separations, band membership,
horizontal order and every substantive fence/diameter guard have strict margins.
Continuity therefore gives a relative open family of actual four-square poses satisfying
the same guards, including perturbations away from the angle seam and away from equal
row heights.
The closed family is defined by (F), (C) and the explicit vertex conditions,
not by an unspecified neighborhood.
The criterion was developed from the fixture obstruction; the fixture is an exact
membership control for the four-pose set $\Gamma$, not for the impossible eleven-square
$D$. The domain of the criterion is not restricted to the displayed coordinates.

The anchored five-square fixture cannot extend by six further squares either: the anchor
already occupies one of the four residual places.
Its successful one-square extension was never evidence for a seven-square extension.
The lower-band fixture fails the top-reaching guard $u+A\ge d$, and its upper-band
reflection is not covered by this central-band child.
Their parent branches remain explicit open obligations.

## Closed Siblings, Comparison Status and Next Obligation

Retain every $P_{0,I,\pi}$ and $P_{2,I,\pi}$. For the central parents use the following
explicit list, rather than creating a failure child from every displayed coordinate
bound. Put

$$
c_B=(x_0+x_2)/2,\quad H_B=y_B-b=w_B/2,\qquad
c_T=(x_1+x_3)/2,\quad H_T=d-y_T=w_T/2.
$$

The list $\mathcal G$ consists of exactly these 24 scalar expressions, each required to
be nonnegative:

| Group | Expressions in $\mathcal G$ | Count |
| --- | --- | --- |
| Fence | $\Delta$; $A-k-\Delta$; $b-\ell+A$; $u+A-d$; $b+k-x_0$; $x_3-d+k$; $2k+\Delta-x_{i+1}+x_i$ for $i=0,1,2$ | 9 |
| Bottom middle vertices | $H_B$; $c_B-H_B-b$; $d-c_B-H_B$ | 3 |
| Top middle vertices | $H_T$; $c_T-H_T-b$; $d-c_T-H_T$ | 3 |
| Top left vertices | $v_L$; $d-b-v_L$ | 2 |
| Bottom right vertices | $h_R$; $w_R-h_R$; $d-b-w_R$ | 3 |
| Diameters | $\beta-2H_B$; $\beta-2H_T$; $\beta^2-2v_L^2$; $\beta^2-w_R^2-h_R^2$ | 4 |

This conjunction is equivalent to the original guards on the central parent; no
necessary geometric condition is removed.
The parent already puts $\ell,u,c_B,c_T$ in $[b,d]$, and $\ell\le u$ is the same
condition as $\Delta\ge0$. Thus the first row is equivalent to (F), with its duplicate
and parent-implied bounds removed.

For $P_B$, the three expressions require a nonnegative height and both base endpoints
inside the horizontal center interval.
Adding the two endpoint inequalities gives $2H_B\le d-b$, so its apex ordinate $b+H_B$
also lies in $[b,d]$. Its apex abscissa $c_B$ is already in that interval.
The same argument for $H_T$ checks every $P_T$ vertex, with apex ordinate $d-H_T$.
Conversely the original vertex and nonnegative-size guards imply all six expressions.
For $P_L$, every variable vertex coordinate is inside the box exactly when
$0\le v_L\le d-b$. For $P_R$, the three expressions give $0\le h_R\le w_R\le d-b$; these
bounds put every displayed vertex in the box and are implied by the original vertex and
size requirements. The last row is precisely (C).

Coordinates written identically as $b$ or $d$ contribute only identities such as
$b-b=0$, $d-d=0$, and the positive constant $d-b$. They have no failure child.
Duplicate conditions and bounds already implied by the parent or by the listed vertex
inequalities also have no separate failure child.
Each of the 24 retained expressions has strict positive value at the four-pose fixture,
by the exact margins above.
Hence none introduces the identically tight sibling found in the original
representation.

Keep $D$ and, for each $g\in\mathcal G$, keep the closed sibling

$$
P_{1,I,\pi}\cap\{g\le0\}.
$$

Their union covers the parent: outside $D$, the equivalent conjunction has a strictly
negative member. Equality belongs to both success and failure children, preserving weak
touching and all seams.
Let $\mathcal U$ be the relative open subset of the four-pose parent where every
$g\in\mathcal G$ is strictly positive.
It contains the fixture and the continuous family established above.
No retained failure child admits an assignment whose selected four poses lie in
$\mathcal U$. This is an actual removal of that four-pose family from the remainder
representation; the capacity proof establishes that no eleven-square completion is lost.
It is not a claim that the four-pose fixture was itself a point of $D$ or of the full
parent.

Ordering permutations and the original band-seam ownership are unchanged.
No success guard is asserted for an arbitrary four-square group; the full eleven-square
parent supplies the necessity of remaining outside their conjunction.

The independently accepted proof supplies new parent-cover evidence and a useful
explicit compatibility restriction for BC262. It does not establish the H118 strength
comparison. Both resource and geometric arms must use this same full domain, actual
angles, every applicable ordering/projection deduction and the identical SAT branching
policy. A surviving exact point of the strongest declared coupled outer LP is still
missing. At exact fixed angles, a fully selected physical SAT system is an exact
translation LP. This report’s additional minimum, absolute-value and quadratic guard
conditions would also need a declared exact or outer representation in any matching
comparator; dropping them from only the geometric arm would change the question.
No such matrix or witness is frozen here.
Survival of a matching outer relaxation, or its exclusion by the same geometric
deductions, remains unestablished.

Keep BC271 blocked until such a comparator and exact surviving witness are independently
accepted on a complete specified domain.
Do not run a capacity search merely to rediscover the proved four-region exclusion.
If the matching geometric comparator also excludes the domain, any resource advantage is
a separately measured proof-cost question.

The independent review accepted the universal octagon inclusion, virtual-row shrink,
section cover, equality cases, four diameters and fixture margins.
The coordinator’s next correctness check is the equivalent 24-guard representation and
corrected remainder above.
After that check, return the restriction to BC262’s parent-cover owner and separately
price the missing same-domain LP-survival question.
No computation or new target is admitted by this report.

## Work Receipt

The phase-7 lease was recorded for 08:38:00–09:08:00 UTC on 2026-09-07. This worker’s
first recorded clock read was 08:40:38 UTC. Work consisted of reading the accepted
fixtures and H118, checking the existing parent/anchor contracts, and deriving the
finite residual-center fence and its exact fixture control by hand.
Only this report was written.
No target command, numerical search, resource search, solver, Git or registry mutation,
identifier allocation or dependency change occurred.
The mathematical derivation and final scope readback ended at 09:02:59 UTC, 22 minutes
21 seconds after the first recorded clock read and 24 minutes 59 seconds after the phase
lease began. The document received the common-document and prose-editing passes.
Installed Flowmark 0.4.0 formatted this file and passed its check with the cache
disabled; both linked source files exist, the whitespace check passed, and the required
footer appears once.
A final scoped formatting check follows this receipt.
Independent mathematical acceptance belongs to the separately reserved review.

## Correction Receipt: 2026-09-07

The
[independent review’s historical finding](bc-270-parent-compatibility-review.md#complete-parent-cover-and-its-limits)
is preserved: the original instruction to generate a closed failure child from every
vertex bound included identities such as $Y-b=0$, so some children were the entire
parent. That cover was sound but did not establish useful pruning of the fixture’s
relative open family.
The correction replaces only that representation with the explicit equivalent 24-guard
list and its closed failure children.
It also distinguishes four-pose membership in $\Gamma$ from the empty eleven-square $D$.
The accepted capacity theorem, guard geometry, weak boundaries and parent scope are
unchanged.

The additional correctness lease is 09:24:17–09:32:17 UTC. The first recorded clock read
after dispatch was 09:24:41 UTC. Only this report was edited; no new target, numerical
work, solver, shared record, Git state, identifier or dependency was touched.
The correction, equivalence proof and readback completed at 09:28:45 UTC, 4 minutes 4
seconds after the first clock read and 4 minutes 28 seconds after the lease began.
Installed Flowmark 0.4.0 formatted the assigned file and passed its check with caching
disabled. All three distinct linked files exist, the historical review section is
present, the whitespace check passed, and the footer appears once.
A final scoped formatting check follows this receipt.
The coordinator independently reviews this representation correction.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
