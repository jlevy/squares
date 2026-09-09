# BC-281: Independent Full-Angle Adversarial Analysis

**Inconclusive on the complete target.** This independent hand analysis gives an exact
necessary condition excluding neighborhoods of both axis lifts, a cap lemma across the
closed region $c,s\ge1/4$, and a forced separating inequality on that region.
It gives neither a contradiction for all six remainder children nor an eleven-square
witness. The statements below await the protocol’s fresh independent target audit.

This is delegated W3 insight-iteration work in session092 phase 18, under BC281, H120
and the coordinator’s existing bead.
The immutable admission revision supplied at dispatch was
`bdbfc054baefb79d67832b339c71830ba39e1ab1`. The
[native protocol](bc-281-full-angle-release-protocol.md), its
[independent admission](bc-281-full-angle-protocol-review.md), the
[complete domain](bc-280-full-angle-release-domain.md), and its
[domain review](bc-280-full-angle-domain-review.md) define the unchanged question.

All ten parameters, eleven actual squares, 44 containment rows, 55 complete pair
disjunctions, nine flush incidences and six positive segments remain in the target.
The retained bounds are $381/100\le L\le96/25$, $t,v\in[0,1]$ and $a,b\in[-1/4,1/4]$,
with the admitted bounds on $z,p,w$. Square 10 remains independent.
The [positive middle audit](bc-273-analytic-independent-review.md) and
[negative middle audit](bc-276-negative-slide-independent-review.md) are inherited only
on $t\in[1/3,2/5]$, for both signs and every admitted square-10 pose.

Write $c=c(t)$, $s=s(t)$, $u=c+s$, $h=u/2$ and $D=(1+u)/2$. Put $A=e\cdot p$,
$B=f\cdot p$, and $k=u+1/2$. The basis and center formulas are exactly those in the
admitted domain. An axis square and a block square have combined support $D$ on each of
$x,y,e,f$.

## A Necessary Condition at Both Axis Lifts

Every feasible target point satisfies

$$
L(c+s)\ge4. \tag{1}
$$

To prove this, put $d=1/u$. Each block square contains the axis-aligned square of side
$d$ at the same center: a vector with coordinate magnitudes at most $d/2$ has each
block-basis projection at most $ud/2=1/2$. Its open interior lies in the actual square’s
open interior. The six axis squares also contain these cores because $d\le1$. Thus the
ten actual squares 0–9 would contain ten axis-aligned cores of side $d$, with disjoint
interiors, in the same container.

If $L<4d$, the core centers lie in $[d/2,L-d/2]^2$, whose coordinate range has length
$L-d<3d$. Partition each coordinate range into three intervals of diameter less than
$d$, assigning shared endpoints to one interval.
Among ten centers, two must occupy the same one of the nine Cartesian cells.
Both coordinate differences are strictly less than $d$, so their core interiors overlap.
This contradicts actual-square nonoverlap and proves (1). No core feasibility is
promoted to actual-square feasibility.

Two closed consequences, for both slide signs and all $v,w$, are

$$
t\in[0,1/50]\quad\text{or}\quad t\in[49/51,1]
\quad\Longrightarrow\quad\mathcal S_{\rm full}\text{ has no such point}. \tag{2}
$$

On the first interval, $u(t)$ increases and $u(t)\le u(1/50)=2599/2501$. For the second,
the scalar substitution $q=(1-t)/(1+t)$ lies in $[0,1/50]$ and satisfies $u(t)=u(q)$.
This identity compares supports only; it does not reflect or relabel a packing.
The exact strict margin is

$$
4-\frac{96}{25}\frac{2599}{2501}
=\frac{596}{62525}>0.
$$

Both axis endpoints are included.
Equation (1) retains its equality surface; the pigeonhole argument does not exclude
$Lu=4$.

## Top Caps Without a Half-Chart Assumption

For a block square with center $(x_i,y_i)$, write

$$
\delta_i=y_i+h-(L-1),\qquad X_i=x_i+(c-s)/2.
$$

For $c,s>0$, a positive cap in $L-1<y<L$ has its apex abscissa $X_i$. Its open interior
is nonempty and convex, even when the top vertex touches the container.
Nonoverlap with squares 2, 3 and 4 confines this cap to one of the two open horizontal
gaps $(2,z)$ and $(z+1,L)$. Openness excludes points on obstacle boundaries, and
connectedness prevents a cap from occupying both gaps.
Each gap has width at most $q=L-3\le21/25<1$.

At depth $m=\min(c,s)$ below the apex, the horizontal section has width
$1/\max(c,s)\ge1$. If $\delta_i\ge m$, sections approaching that depth from above
already exceed the available gap width.
Therefore

$$
0<\delta_i<\min(c,s),\qquad
I_i=\left[X_i-\frac c s\delta_i,\ X_i+\frac s c\delta_i\right]
\subseteq\text{the closure of its gap},
\qquad \delta_i\le qcs. \tag{3}
$$

The interval $I_i$ is the limiting section at $y=L-1$. Its weak endpoints preserve
bottom-corner touching.
At an axis endpoint, a positive cap would have constant horizontal width one, so no
positive cap is possible there.
Consequently the bound $y_i\le L-1-h+qcs$ holds on the entire chart, including its
endpoints, for each block square individually.
This cap-depth bound does not determine which square penetrates.

Now impose the exact closed subdomain

$$
c\ge1/4,\qquad s\ge1/4. \tag{4}
$$

In this subdomain, $ae-f$ has positive horizontal and negative vertical components, and
$e+bf$ has both components positive.
The short-slide bounds and $c^2+s^2=1$ make these signs strict even on the boundary of
(4). Thus square 8 has the highest center, square 7 the lowest, and squares 6 and 9 are
intermediate.

Two retained block neighbors cannot both have positive top caps.
First take an ordered pair $P,Q=P+e+bf$, with cap depths $\delta_P,\delta_Q>0$. Their
apex and depth differences are

$$
X_Q-X_P=c-bs>0,\qquad \delta_Q-\delta_P=s+bc>0.
$$

If their caps lie in the same gap, the span from $I_P$'s left endpoint to $I_Q$'s right
endpoint is

$$
(c-bs)+\frac c s\delta_P+\frac s c\delta_Q
=\frac1c+\frac{\delta_P}{cs}>1,
$$

which exceeds the gap width.
If they lie in different gaps, their horizontal order puts $P$ in the central gap and
$Q$ in the right gap.
The intervening square 2 requires a base-interval separation at least one.
The actual separation is

$$
(c-bs)-\frac c s\delta_Q-\frac s c\delta_P
=-\frac b s-\frac{\delta_P}{cs}<\frac{|b|}{s}\le1,
$$

again impossible. Both comparisons are strict because the cap depths are positive.

For the other neighbor direction $Q=P+ae-f$, the higher square is $P$, and
$X_Q-X_P=ac+s>0$, $\delta_P-\delta_Q=c-as>0$. The same two comparisons are respectively

$$
\frac1s+\frac{\delta_Q}{cs}>1,
\qquad
\frac a c-\frac{\delta_Q}{cs}<\frac{|a|}{c}\le1.
$$

They exclude both caps in one gap and caps in different gaps.
Every positive cap of square 6 or 9 would force a positive cap of its higher neighbor 8;
a positive cap of square 7 would force one of square 6. Hence (4) implies

$$
y_6+h\le L-1,\qquad y_7+h\le L-1,\qquad y_9+h\le L-1. \tag{5}
$$

Only square 8 may have a positive top cap.
The proof includes $c=s$, both slide signs, zero slides and all cap equalities.
It uses no complementary-angle reflection and no selected SAT branch for a top-row pair.

## A Forced Inequality Across the Same Closed Region

On (4), every feasible target point satisfies

$$
A\ge k=c+s+1/2. \tag{6}
$$

Containment gives $p_x\ge h$ and $p_y\ge h+c-as$, with $c-as>0$. For pair 0–6, the
center displacement has nonnegative coordinate components.
Negative $x,y,e$ directions fail; positive $f$ separation implies positive vertical
separation, and negative $f$ separation implies positive horizontal separation.
Its full disjunction therefore gives at least one of

$$
A\ge k,\qquad R:p_x\ge1+h,\qquad V:p_y\ge1+h. \tag{7}
$$

First suppose $R$. If $c\ge5/8$, square-7 containment directly gives

$$
A-k\ge s(2c-1-as)\ge0.
$$

For $c\le5/8$, we have $s\ge3/4$. Pair 1–7 has displacement $(-\xi,Y_7)$ with both
$\xi,Y_7\ge0$. Its positive $e$ alternative implies vertical separation; negative $f$
and the wrong coordinate signs fail.
The complete disjunction reduces to

$$
\begin{aligned}
H_7:&\quad x_7\le L-1-h,\qquad
V_7:\quad y_7\ge1+h,\\
F_7:&\quad B\ge J:=3/2+u-sL,\qquad
E_7:\quad A+a\le Q:=cL-c-1/2.
\end{aligned} \tag{8}
$$

Every possibility can be checked:

- $R,H_7$ requires $L\ge2+(1+a)c+2s\ge2+3c/4+2s\ge4$. For the last inequality,
  $s\ge1-3c/8$ follows by squaring: the difference of the squares is $c(48-73c)/64\ge0$
  on $0\le c\le5/8$.
- $R,E_7$ and square-7 containment require $c(L-2)\ge1+2cs+ac^2$. The right side minus
  the left is at least $1-17c/50-c^2/4\ge883/1280>0$, using $s\ge3/4$ and $L-2\le46/25$.
- $R,F_7$ gives $cA=p_x+sB\ge1+h+sJ$, and $1+h+sJ-ck=s[2-s(L-2)]>0$. Thus $A>k$.
- $R,V_7$ gives $A-k\ge s(2c-as)>0$.

The first two are impossible; the last two imply (6). This proves $R\Rightarrow A\ge k$
without discarding any alternative of pair 1–7.

Now suppose $V$. Equation (5) puts the pair 5–6 displacement in the form $(X,-Z)$, where
$X,Z\ge0$. Its vertical-down alternative would require $L\ge3+2h=3+u\ge4$ and is
impossible. Negative $e$ separation implies that already excluded vertical-down
alternative; positive $f$ and the wrong coordinate signs fail.
The remaining complete possibilities are

$$
R,\qquad A\ge E_0:=c+1/2+s(L-1),\qquad
B\le K_5:=cL-2c-s-1/2.
$$

The first was proved; $E_0-k=s(L-2)>0$ handles the second.
For the third,

$$
s(A-k)\ge1+h-cK_5-sk=c[1-c(L-3)]>0.
$$

Thus $V$ also implies (6), completing the reduction of (7). This proof uses the actual
complete clauses for pairs 0–6, 1–7 and 5–6, containment, and the top-cap result.
The geometric definition retains all other pair clauses.
Neither slide was divided out.

## Exact Controls Against Completing the Proof by Transfer

Equations (3)–(6) do not supply the remaining inequalities of the accepted middle proof.
Two exact scalar controls show why previously positive threshold differences cannot be
reused on the full chart.
Put

$$
M=cL-c-2s-1/2,\qquad
J=3/2+u-sL,\qquad K_5=cL-2c-s-1/2.
$$

At $L=96/25$, $t=1/5$ gives $(c,s)=(12/13,5/13)$ and

$$
J-M=2-\frac{46}{25}c-\frac{21}{25}s=-\frac7{325}<0.
$$

At the same side, $t=2/3$ gives $(c,s)=(5/13,12/13)$ and

$$
J-K_5=2-\frac{21}{25}c-\frac{46}{25}s=-\frac7{325}<0.
$$

Both control angles lie in (4). They refute positivity as a consequence of that angle
range and the side cap alone.
They supply no values for the other parameters and therefore do not refute an
implication using additional geometric premises.
They are scalar controls, not feasible skeletons or witnesses.
No contradiction with the accepted middle proofs follows, because neither control angle
is in their interval.

The admitted opposite-sign diagonal controls remain valid in the full chart: the two
displayed $7/8$-by-$7/8$ common-coordinate displacements give interior overlap, whereas
$a=b=0$ permits the component’s diagonal point touching.
The exact Trump parent control remains outside the target by $U>387/100>96/25$; its
retained replay was not rerun.
No parent control is promoted to a target witness.

## Coverage and Remaining Implication

The eight closed angle/sign children remain the target’s complete cover.
The two middle children inherit their accepted exclusions.
Equation (2) adds closed excluded portions of the two lowest-angle and two highest-angle
children.
Equations (3)–(6) are necessary conditions on their stated domains; they do not
exclude those domains.
The condition (4) is an additional lemma domain, not a replacement target or a fitted
angle box.

A sufficient completion still needs an actual contradiction across every surviving point
of all six closed remainder children, or an exact eleven-square witness with all 44
containment rows and one valid actual-axis separator for each of 55 pairs.
This report supplies no such witness and no feasible ten-square skeleton.
In particular, the unproved step is a complete implication from the remaining actual SAT
clauses to a contradiction after (1), (3), (5) and (6), including angles outside (4).
Square 10’s ten incident clauses have not been eliminated or replaced by a surrogate
feasibility test.

The new exclusions and necessary conditions retain variable $L$, both side endpoints,
all $z$ endpoints, zero slides, slide endpoints, $c=s$, containment and SAT equality,
$v=t$, both independent axis lifts, the physical coincidences $(t,v)=(0,1),(1,0)$, and
recontacts. The cap arguments use open interiors and weak limiting sections, so legal
touching survives. No new reflection, quarter-turn transfer of a labeled margin child,
fixed-side substitution, or deleted branch is asserted.

## Work Receipt

The parent assigned the prospective phase-18 adversary start at `2026-09-07T12:36:00Z`
and the absolute stop at `2026-09-07T13:01:00Z`, including writing, formatting and
checks. The actual first clock was `2026-09-07T12:39:21Z`. This report inherits that
fixed stop; initialization did not extend it.

The reasoning used the admitted domain, protocol, reviews, and accepted BC273/276
mathematical reports.
The concurrent BC281 author report was not read, and no reasoning was exchanged with its
author or the reserved target auditor.
Interim findings went only to the coordinator.
All derivations and scalar controls were exact hand analysis.
No numerical target, solver, target sample, scientific script, engine build, resource
search or source-control replay ran.
No shared record, identifier, dependency or Git state was changed.
Only this assigned report was written; no scratch file was needed.

The mathematical freeze was `2026-09-07T12:57:01Z`, 1,060 seconds after the actual first
clock. The complete report received a hand readback, common-document and de-slop passes.
Scoped document checks completed at `2026-09-07T12:57:36Z`, 1,095 seconds after the
actual first clock and before the absolute stop.
All six native link targets exist, the exact required footer appears once, and the
trailing-whitespace scan found no matches.
Installed Flowmark formatted only this assigned file with caching disabled, and its
scoped auto-format check passed.
The equations and the inconclusive verdict survived formatting.
One final scoped formatting check follows this receipt before terminal delivery.
No background command remains.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
