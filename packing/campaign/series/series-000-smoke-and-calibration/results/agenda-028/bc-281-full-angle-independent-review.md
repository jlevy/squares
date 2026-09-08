# BC-281: Independent Audit of the Partial Full-Angle Results

**Accept the new closed exclusions and the stated necessary conditions; the complete
BC281 determination remains inconclusive.** The [author](bc-281-full-angle-author.md)
excludes both slide signs on $[2/5,1/2]$ and the closed axis neighborhoods $[0,1/24]$
and $[23/25,1]$. The [adversary](bc-281-full-angle-adversary.md) independently proves a
weaker endpoint restriction and useful necessary cap and separating conditions on a
broader angle domain.
Every decisive implication was reconstructed below; agreement between the reports was
not used as its justification.

Together with the accepted [positive](bc-273-analytic-independent-review.md) and
[negative](bc-276-negative-slide-independent-review.md) middle-angle results, the new
exclusions retain the closed remainder

$$
\mathcal S_{\rm full}\cap
\left\{t\in[1/24,1/3]\cup[1/2,23/25]\right\}.
\tag{R}
$$

Both signed slide children, every other original parameter, and all actual-square
conditions remain. Its endpoints overlap proved regions deliberately.
Neither an exclusion of this remainder nor an actual eleven-square witness has been
established. No unrestricted bound or global representative theorem follows.

## Domain and Individual Dispositions

The [prospective protocol](bc-281-full-angle-release-protocol.md) incorporates the
[BC280 domain](bc-280-full-angle-release-domain.md) and its
[independent admission](bc-280-full-angle-domain-review.md).
The unchanged ten parameters satisfy $381/100\le L\le96/25$, $t,v\in[0,1]$,
$a,b\in[-1/4,1/4]$, $2\le z\le L-1$, and $p,w\in[1/2,7/2]^2$. The source centers, nine
flush incidences, six positive segments, 44 containment rows and 55 complete pair
clauses remain. The pair inventory is $15+24+6+10=55$ for the axis group, cross group,
block group and square10 respectively.
Each of squares 0–9 used below is an actual square of every target point; deleting
square10’s conditions for a necessary contradiction does not change the side or move a
wall square.

Use $c=(1-t^2)/(1+t^2)$, $s=2t/(1+t^2)$, $u=c+s$, $h=u/2$, $D=h+1/2$, $e=(c,s)$,
$f=(-s,c)$, $A=e\cdot p$, and $B=f\cdot p$. An axis square and a block square have
combined support $D$ on each of $x,y,e,f$. The full pair clause is the union of the
eight directed inequalities, rather than their conjunction.

| Claim | Independent disposition |
| --- | --- |
| $Lu\ge4$ for every target skeleton | Accepted, including its equality surface |
| $L\ge2+2/u$ using the six fixed axis squares | Accepted throughout the full chart, also for four independent common-angle centers with the same fixed axis-square geometry |
| Both signed endpoint exclusions $[0,1/24]$, $[23/25,1]$ | Accepted, including both physical axis lifts |
| Both signed exclusions on $[2/5,1/2]$ | Accepted through $c=s$ and every declared boundary |
| Adversary’s individual cap-depth bound on the whole chart | Accepted, with a separate axis-endpoint argument |
| Only square8 may penetrate the top strip, and $A\ge u+1/2$, when $c,s\ge1/4$ | Accepted as necessary conditions on that closed subdomain |
| Negative threshold differences at the two scalar controls | Accepted as failures of an angle-and-side-only transfer; no feasible geometry is certified |
| Complete exclusion of $\mathcal S_{\rm full}$, or an actual target packing | Neither established |

No mathematical error was found in the reports’ stated partial claims.
The stronger implications refused in the last two rows are also disclaimed by their
authors.

## The Two Core Counts and Endpoint Margins

Set $d=1/u$. Since $1\le u\le\sqrt2$, each of the ten actual squares 0–9 contains an
axis-aligned square of side $d$ at the same center.
For a block square, the maximum absolute projection of this core on either block axis is
$du/2=1/2$; the core’s open interior lies in the actual square’s open interior.
For an axis square, inclusion follows from $d\le1$. Thus disjoint actual interiors imply
disjoint core interiors.

If $L<4d$, the allowable core-center interval has length $L-d<3d$. Its three-part
coordinate partition gives nine cells of both coordinate diameters strictly below $d$.
Two of ten centers share a cell and their interiors overlap.
This proves $Lu\ge4$ without excluding legal contacts at equality.
The adversary’s endpoint bound uses $u(1/50)=u(49/51)=2599/2501$ and the checked margin

$$
4-\frac{96}{25}\frac{2599}{2501}=\frac{596}{62525}>0.
$$

For the author’s stronger count, suppose $L<2+2d$. Then $L-3<2d-1\le d$. A block core
with positive interior in the top strip has its full horizontal width $d$ there,
exceeding both available top gaps.
A core with positive interior in the left strip similarly exceeds the only available
vertical gap $(1,L-2)$. Therefore all four block cores lie right of $x=1$ and below
$y=L-1$, with equality allowed.

Actual block containment gives the remaining edges of their common rectangle.
After translation, it is $[0,T]^2$, where

$$
T=L-1-h+d/2,\qquad r=1-h+d/2,\qquad 0<r\le d.
$$

Its intersection with actual square1 is precisely $[T-r,T]\times[0,r]$. The identity
$r-d=1-(u+1/u)/2\le0$ checks the asserted upper bound on $r$; positivity follows from
$u\le\sqrt2$. Every core must be wholly left of this corner obstacle or wholly above it.
Assign a core satisfying both conditions to either class, once.

Since $T-r=L-2<2d$ and $T<r+2d\le3d$, each class contains at most two cores.
Four cores would require two in each class.
Take the upper member $H$ of the left class and the left member $V$ of the above class.
The independently reconstructed bounds are

$$
\begin{aligned}
x_V-x_H&\le T-2d<d,&x_H-x_V&\le T-r-d<d,\\
y_V-y_H&\le T-2d<d,&y_H-y_V&\le T-r-d<d.
\end{aligned}
$$

These are distinct assigned cores and overlap in both coordinate directions.
The contradiction proves $L\ge2+2/u$ without the block contact equations.
The top and left arguments used nonempty open strip intersections; a core merely
touching a strip boundary was not removed.

The exact reusable scope is six axis squares at the prescribed centers $C_0,\ldots,C_5$,
with the same $381/100\le L\le96/25$ and $2\le z\le L-1$, together with four actual unit
squares at independently variable centers and one common physical orientation
$t\in[0,1]$. All ten squares must be contained and have pairwise disjoint interiors.
The proof requires neither the four block segment identities nor their contact sides or
slide bounds: none of the equations for $C_7-C_6$, $C_8-C_6$ or $C_9-C_6$, or either
slide parameter, occurs in it.
The two axis contacts remain implicit in the fixed six-square positions.
Common orientation supplies the same $d=1/u$ and actual support $h=u/2$ for all four
additional squares; the fixed wall pattern supplies the top gaps, left gap and corner
obstacle. No arbitrary wall pattern, independently varying block orientations, or global
representative is covered by this reuse statement.

The author’s two inner endpoints have $u(1/24)=u(23/25)=623/577$. Monotonicity on the
two stated neighborhoods and the stronger count give

$$
L\ge\frac{2400}{623},\qquad
\frac{2400}{623}-\frac{96}{25}=\frac{192}{15575}>0.
$$

Both margins and both endpoint substitutions check exactly.
The complementary scalar supports do not assert a reflection or relabeling of the source
geometry. The adversary’s smaller endpoint intervals lie within the author’s accepted
exclusions.

## Cap Geometry, Including the Diagonal Seam

Put $\delta_i=y_i+h-(L-1)$, $\delta=\delta_8$, and $X=X_8$. For an interior chart angle,
a top vertex has abscissa $X_i=x_i+(c-s)/2$. At depth $d_0\le\min(c,s)$ below that
vertex, the section endpoints are $X_i-cd_0/s$ and $X_i+sd_0/c$, with width $d_0/(cs)$.
The width at depth $\min(c,s)$ is $1/\max(c,s)$. These formulas hold on either side of
$c=s$ and at the seam.

A positive open cap above $L-1$ is connected and lies in one of the open gaps $(2,z)$
and $(z+1,L)$. It cannot occupy an obstacle boundary: its openness would then enter a
neighboring obstacle interior.
Both gaps have width at most $L-3\le21/25$. Sections approaching depth $\min(c,s)$ would
have width at least one, so each positive cap has depth strictly below $\min(c,s)$.
Taking limits at its base yields weak endpoint conditions and $\delta_i\le(L-3)cs$. At
either axis endpoint, a positive cap has constant width one and is impossible.
Consequently $y_i\le L-1-h+(L-3)cs$ holds on the full chart for each block square.

On the author’s interval $[2/5,1/2]$, reconstruction gives

$$
3/5\le c\le21/29<73/100,\quad
17/25<20/29\le s\le4/5,\quad
7/5\le u\le\sqrt2<71/50.
$$

All four block coordinate-order increments remain positive for both slide signs.
For square8, right containment of square9 gives $X\le L-ac-2s\le213/80<3\le z+1$. Thus
any positive square8 cap is central, with $2<X<z$. The section argument then gives

$$
X-c\delta/s\ge2,\quad X+s\delta/c\le z,\quad
\delta\le cs(z-2)\le21/50.
$$

Only the last inequality is used when $\delta\le0$. Direct expansion of the source
centers gives

$$
sX-c\delta=cL-c-1/2-(B+b),\qquad
cX+s\delta=A+3/2-sL+s.
$$

A positive cap therefore implies $B+b\le M=cL-c-2s-1/2$ and $A\le P=u(L-1)-3/2$. With
$J=3/2+u-sL$ and $K_5=cL-2c-s-1/2$, the new interval gives the exact strict gaps

$$
J-M\ge64/725,
\qquad J-K_5\ge3/125.
\tag{G}
$$

The first weighted trigonometric expression is decreasing and attains its maximum at
$t=2/5$; the second is increasing and attains its maximum at $t=1/2$. The claimed
derivative signs follow from the displayed rational bounds, including $54/125$ as a
lower bound for the derivative of the second weighted expression.
Neither calculation assumes $c\ge s$.

The adversary’s broader cap result also checks.
On $c,s\ge1/4$, every required coordinate increment is strictly positive because the
other coordinate is strictly below one.
For neighbors with offset $e+bf$, two positive caps have same-gap span
$1/c+\delta_P/(cs)>1$ or different-gap separation $-b/s-\delta_P/(cs)<|b|/s\le1$. For
offset $ae-f$, the corresponding quantities are $1/s+\delta_Q/(cs)>1$ and
$a/c-\delta_Q/(cs)<|a|/c\le1$. The first exceeds a gap’s width; the second cannot cross
the intervening unit square2. The center ordering then prevents positive caps on
squares6,7,9. Strictly positive depths supply the strict comparisons even at $c=1/4$,
$s=1/4$ and slide endpoints.
Zero cap depth remains allowed.

## Complete SAT Screening on the New Interval

All projections below have threshold $D\ge6/5$. I reconstructed the center bounds from
containment, the coordinate order and the cap bound, rather than taking the screening
tables as assumptions.
For positive slides they give

$$
X_6,\xi_9\in[1/5,153/100],\quad
Y_6\in[3/5,69/50],\quad Y_7\in[1/5,19/20],\quad
Y_9\ge22/25,\quad\xi_7\ge1/5.
$$

Here $X_6=p_x-1/2$, $Y_i=y_i-1/2$, and $\xi_i=L-1/2-x_i$. For negative slides, write
$a=-\alpha$, $b=-\beta$. The author’s two-cap argument forces $p_y\le L-1-h$: otherwise
squares6 and8 would have central caps with span $1/c+\delta_6/(cs)>5/4$. With
$X_0=p_x-1/2$ and $Z=L-3/2-p_y$, the resulting bounds are

$$
X_0,\xi_9\in[1/5,151/100],\quad Z,Y_7\in[1/5,26/25],\quad
Y_9\in[279/400,73/50],\quad\xi_7\ge1/5.
$$

Write $H_7$ for the horizontal-left condition $x_7\le L-1-h$.

| Sign and pair | Strictly screened directions | Complete surviving alternatives |
| --- | --- | --- |
| Positive, 0–6 | $-x,-y,-e$ by sign; $+f\le4357/5000$ and $-f\le108/125$ | $+x,+y,+e$; each implies $A\ge k=u+1/2$ |
| Positive, 1–7 | $+x,-y,-f$ by sign; $+y\le19/20$, $+e\le19/25$; $-e$ contradicts $c(L-2)\le1679/1250<42/25\le1+s$ | Horizontal-left $H_7$ or $B\ge J$ |
| Positive, 1–9 | $+x,-y,-f$ by sign; $-e\le11169/10000$; $+e$ has the negative residual checked below | Horizontal-left, vertical-above, or $B+b\ge J$ |
| Negative, 5–6 | $-x,+y,+f$ by sign; $-y\le26/25$, $+e\le9663/10000$, $-e\le89/125$ | $p_x\ge h+1$ or $B\le K_5$ |
| Negative, 1–9 | $+x,-y,-f$ by sign; $-e\le157/250$, $+e\le131/125$ | Vertical-above or $B-\beta\ge J$, after horizontal-left implies the latter |
| Negative, 1–7 when $Y_9\ge D$ | $+x,-y,-f$ by sign; $+y\le26/25$, $+e\le104/125$ | Horizontal-left, $-e$, or $+f$; all imply $B\ge J$ |

Every numerical projection bound in the table is strictly below $6/5$. The remaining
positive 1–9 projection has residual at most

$$
F_L=s(L-2)-1-2cs+cs^2(L-3)+s^2/4.
$$

Its coefficient of $L$ is positive.
At $L=96/25$, its derivative with respect to the actual angle is

$$
\frac{46}{25}c-2c^2+2s^2
+\frac{21}{25}s(3c^2-1)+\frac12sc>0.
$$

The first three terms are at least $963/1000$ and the remaining terms are nonnegative.
The endpoint value at $(c,s)=(3/5,4/5)$ is exactly $-17/3125$. Thus this direction is
screened strictly on the entire interval.
Replacing $L$ by its bound in this scalar inequality does not replace variable-side
geometry by a fixed-side packing.

The surviving alternatives also check, including their equality cases:

- **Positive 0–6:** horizontal separation gives $A-k\ge s(2c-1-as)\ge0$. Vertical
  separation requires a positive cap; $X>2$ then gives $A>k+c(1-2c+s+bs)\ge k$. Direct
  $+e$ is exactly $A\ge k$.
- **Positive 1–9:** horizontal-left gives positive $f$ with excess $c(2s-1+bc)>0$.
  Vertical-above combined with $H_7$ gives projection at least $D+bs^2$. Combined with
  the other 1–7 alternative, it gives $B+b\ge J$ directly.
  Thus the full clauses force $B+b\ge J$.
- **Negative 1–9:** horizontal-left gives positive $f$ with excess $c(2s-1-\beta c)>0$,
  using $2s-1-\beta c\ge71/400$.
- **Negative 1–7 in the upward case:** $Y_7\ge D-s+\beta c$. Horizontal-left gives $f$
  projection at least $D+\beta c^2$. The $-e$ alternative gives at least
  $D+(s^2+\beta c)/c>D$. The identity $D(1+s-c)-s=s^2$ verifies the latter conversion.
  All alternatives therefore give $B\ge J$.

For positive slides, a positive cap contradicts $B+b\ge J>M$. At nonpositive cap depth,
the identity $sA+c(B+b)=p_y+bc\le L-1-h-s$ yields

$$
L(1+cs)\ge(1+u)^2,
\qquad
L\ge2+\frac{4u}{1+u^2}
\ge2+\frac{4\sqrt2}{3}>\frac{96}{25}.
\tag{C}
$$

The function $u/(1+u^2)$ decreases for $u\ge1$; the last strict comparison follows from
$\sqrt2>69/50$.

For negative slides, the screened clauses first give $B\ge J$. Gap (G) removes
$B\le K_5$, forcing $p_x\ge h+1$. If the cap is positive, $A\le P$ and $cA=p_x+sB$ give
exactly the first inequality in (C). If it is nonpositive, $Y_9\le26/25<D$ forces
$B-\beta\ge J$; containment gives $A\ge k+s(2c-1)+\alpha s^2\ge k$. Then
$sA+c(B-\beta)=p_y-\beta c\le L-1-h-s$ again gives (C). Both signed children are
excluded, including $\delta=0$ and every zero slide.

## The Adversary’s Broader Separating Condition

On the closed domain $c,s\ge1/4$, the full 0–6 clause reduces to $A\ge k$,
$R:p_x\ge1+h$, or $V:p_y\ge1+h$. The two $f$ directions imply the corresponding
coordinate separation because $c,s\le1$; the negative coordinate and negative $e$
directions fail by sign.

For $R$ and $c\ge5/8$, containment gives $A-k\ge s(2c-1-as)\ge0$. For $c\le5/8$,
$s\ge3/4$ and the complete 1–7 alternatives are $H_7$, $V_7:y_7\ge1+h$, $B\ge J$, or
$A+a\le Q=cL-c-1/2$. The positive $e$ direction implies $V_7$; the wrong coordinate
signs and negative $f$ fail.
Their independent dispositions are:

| Additional alternative under $R$ | Verified implication |
| --- | --- |
| $H_7$ | $L\ge2+3c/4+2s\ge4$; the squared comparison for $s\ge1-3c/8$ has difference $c(48-73c)/64\ge0$ |
| $A+a\le Q$ | Requires $c(L-2)\ge1+2cs+ac^2$; the opposite strict gap is at least $1-17c/50-c^2/4\ge883/1280$ |
| $B\ge J$ | $1+h+sJ-ck=s[2-s(L-2)]>0$, hence $A>k$ |
| $V_7$ | $A-k\ge s(2c-as)>0$ |

For $V$, the accepted broader cap lemma gives $p_y\le L-1-h$. The 5–6 displacement is
$(X,-Z)$ with $X,Z\ge0$. Downward separation would require $L\ge3+u\ge4$; negative $e$
implies this refused direction.
Positive $f$ and the wrong coordinate signs fail.
The remaining alternatives are $R$, $A\ge E_0=c+1/2+s(L-1)$, or $B\le K_5$. They imply
$A\ge k$, respectively through the proved $R$ case, $E_0-k=s(L-2)>0$, and

$$
1+h-cK_5-sk=c[1-c(L-3)]>0.
$$

This proves the claimed broad necessary row without dropping a SAT alternative.
It does not produce a contradiction on that broader domain.

## Controls and Exact Remaining Coverage

At $L=96/25$, the adversary’s two scalar checks reconstruct as

$$
\begin{array}{c|c|c}
t&(c,s)&\text{threshold difference}\\
1/5&(12/13,5/13)&J-M=-7/325\\
2/3&(5/13,12/13)&J-K_5=-7/325.
\end{array}
$$

Both angles satisfy $c,s\ge1/4$ and lie outside the accepted middle interval.
These values refute positivity from those angle bounds and the side cap alone.
They specify no other target parameters, feasible skeleton or packing, and cannot refute
an implication using additional geometric premises.

The axis endpoint offsets reconstruct to $(0,0),(a,-1),(1,b),(1+a,b-1)$ at $t=0$, and
$(0,0),(1,a),(-b,1),(1-b,1+a)$ at $t=1$. Both endpoints are excluded by the core count;
they are component controls, not target witnesses.
The two opposite-sign slide controls have common-basis displacements $(7/8,7/8)$ and
$(7/8,-7/8)$, giving interior overlap.
At $a=b=0$, the diagonal unit-coordinate displacements retain legal point touching.
The exact Trump control remains outside the target since $U>387/100>96/25$; its retained
source replay was not rerun.

| Original closed interval, for both signs | Accepted coverage after this audit | Interior still unresolved |
| --- | --- | --- |
| $[0,1/3]$ | $[0,1/24]$ and the middle endpoint $1/3$ | $(1/24,1/3)$ |
| $[1/3,2/5]$ | Entire interval, by the retained BC273/276 audits | None |
| $[2/5,\sqrt2-1]$ | Entire interval, by the new signed proofs | None |
| $[\sqrt2-1,1]$ | $[\sqrt2-1,1/2]$ and $[23/25,1]$ | $(1/2,23/25)$ |

The closed remainder (R) preserves every seam by overlap.
The accepted necessary counts and cap conditions may be carried with their domains; they
do not erase the unresolved rows of this table.
No actual angle reflection identifies its two remaining portions.
The missing determination is still a contradiction for every surviving point under all
original conditions, or one exact actual eleven-square witness with all 44 containment
rows and 55 complete pair conditions checked.

No proof divides by $a$, $b$, $c-s$ or an angle difference.
The interior cap proofs divide only by positive $c,s,cs$; the core count handles both
axes separately.
The $c=s$ seam, side and $z$ endpoints, slide endpoints and zero slides,
$v=t$, both independent square10 axis lifts, physical coincidences, containment/SAT
equalities and all recontacts remain included.
These are independently audited analytical lemmas, without a machine proof replay,
full-angle exclusion, unrestricted bound, finite-motion theorem, H118 comparison or H120
uniform-LP adapter acceptance.

## Work Receipt

The session092 phase19 audit lease is **13:10–13:30 UTC on 2026-09-07**, including
writing and checks.
The first actual clock was **13:10:26 UTC**. Both target reports were
terminal before this audit began.
The same reviewer’s earlier closing-scope assessment read neither target report,
discussed neither target argument, and derived no full-angle target lemma; it therefore
did not coauthor the evidence reviewed here.

This audit used exact hand reconstruction of the source equations, core classes, cap
sections, discarded alternatives, threshold arithmetic and closed cover.
No numerical target, scientific script, solver, construction search, source replay,
identifier, dependency, Git mutation or shared-record edit was performed.
Only this assigned review was written; the coordinator owns its adoption and record
integration. Mathematical reconstruction and the complete report readback froze at
**13:23:21 UTC**, 775 seconds after the first actual clock.
The common-document and prose passes were applied.
At **13:23:58 UTC**, all seven linked native source files were checked against the
report’s link inventory and existed; the exact footer occurred once and the
trailing-whitespace scan had no matches.
Installed Flowmark’s no-cache formatting check passed on this assigned file.
Those checks took place 812 seconds after the first clock, within the unchanged lease.
The receipt receives the same scoped formatting check before terminal delivery.
No mathematical continuation or background command follows the freeze.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
