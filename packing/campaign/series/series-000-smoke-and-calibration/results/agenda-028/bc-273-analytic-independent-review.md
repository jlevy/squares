# BC-273: Independent Acceptance of the Analytical Release Exclusion

The [adversary’s ten-square contradiction](bc-273-analytic-adversary.md) is accepted.
It proves the entire frozen $T_{\rm mid}$ empty, with all declared equality boundaries
included. The proof uses no parameter or condition of square 10. Consequently the
already-defined $T_+$ is also empty for every $v\in[0,1]$, including both axis lifts.
This is an independently audited analytical result for the selected source-feature
pilot. It gives no unrestricted packing bound or global angle normal form.

This review is session092 phase 5, W3 `insight-iteration`, under BC273 and the
[frozen analytical protocol](bc-273-analytic-release-protocol.md).
The independent starting materials were that protocol, the
[release design](bc-273-release-domain-design.md), its
[source-corner review](bc-273-release-domain-independent-review.md), and both completed
analytical reports. The calculations below reconstruct the decisive inequalities and
geometric implications; they do not introduce another target argument.

## Individual Verdicts

| Implication | Verdict | Exact scope |
| --- | --- | --- |
| Rational angle and containment bounds in adversary (1)–(3), (14) | Accepted | The declared nonnegative slides, block angle interval and side cap |
| Below-top case forces $L\ge4900/1261>96/25$ | Accepted | Includes equality $y_8+h=L-1$ |
| The remaining open cap lies in the central top-row gap | Accepted | Uses actual interior nonoverlap with squares 2, 3 and 4 |
| $0<\delta<s$ and the two weak cap-base inequalities | Accepted | Includes touching the top wall and obstacle bottom corners |
| $B+b\le M$ and $J-M\ge2/87$ | Accepted | Uniform in every declared skeleton parameter |
| Complete reductions for pairs 0–6, 1–7 and 1–9 | Accepted | Every directed alternative is screened or implies the retained row |
| The ten-square skeleton is impossible | Accepted | A contradiction from necessary conditions of every frozen target point |
| $T_{\rm mid}=\varnothing$ and $T_+=\varnothing$ | Accepted | The second follows because the skeleton proof is independent of $v,w$ |
| Author’s conditional $27/7$ bound and four exterior compartments | Accepted | The former is conditional; the latter is a necessary restriction |
| Author’s forced rows, top-gap bound and right-compartment exclusion | Accepted | The stated scopes; these are not needed for the complete contradiction |
| Exclusion of the whole parent $P_+$ or other feature/slide/block-angle domains | Not established | The exact source remains a feasible parent control above the target side cap |
| BC261 target-instrument readiness | Not established | This analytical audit does not implement target feature inclusion or a generic complete SAT cover |

No decisive implication in the proposed skeleton proof is rejected, and no missing
premise remains for this restricted analytical determination.
The author’s explicit partial-result limits were correct for that report; they do not
invalidate the separate complete argument.

## Domain and Support Reconstruction

Put $c=(1-t^2)/(1+t^2)$, $s=2t/(1+t^2)$, $u=c+s$, $h=u/2$, and $D=h+1/2$. Use the
design’s orthonormal directions $e=(c,s)$ and $f=(-s,c)$ and write $A=e\cdot p$,
$B=f\cdot p$. The exact endpoint ranges are

$$
21/29\le c\le4/5,\qquad 3/5\le s\le20/29,\qquad
7/5\le u\le41/29,
$$

with $c>s>0$. The derivative signs of the displayed rational functions give these
bounds. In particular the coarser $c\ge18/25$, $s\le7/10$ and $7/10\le h\le71/100$ used
by the adversary are valid.

For an axis unit square and a block unit square, the combined support on each of
$x,y,e,f$ is exactly $D$. Thus a center difference $d$ is legal only if at least one of
the eight projections $\pm d_x,\pm d_y,\pm e\cdot d,\pm f\cdot d$ is at least $D$. Every
such inequality is weak.
A projection strictly below $D$ excludes that direction even at a legal contact
boundary.

The retained equations give

$$
x_9=p_x+(a+1)c+(1-b)s,\quad y_7=p_y+as-c,\quad
x_8=p_x+c-bs,\quad y_8=p_y+s+bc,
$$

and $y_9=y_7+s+bc=y_8+as-c$. Therefore containment gives

$$
p_x\ge7/10,\quad
p_x\le96/25-7/10-18/25-(3/4)(3/5)=197/100,
$$

$$
p_y\ge7/10+18/25-(1/4)(7/10)=249/200,
\quad x_9\ge187/100,\quad y_9\ge h+s\ge13/10.
$$

Writing $X_6=p_x-1/2$, $Y_6=p_y-1/2$ and $\xi_i=L-1/2-x_i$, $Y_i=y_i-1/2$ for $i=7,9$,
this independently reproduces $1/5\le X_6,\xi_9\le147/100$ and $Y_9\ge4/5$. No lower
side endpoint, positive slide, or nonzero angle difference is needed in these
deductions.

## The Two Cap Cases

If $y_8+h\le L-1$, substitution gives $p_y\le77/50$ and $y_9\le319/200$. For pair 0–6,
the negative coordinate and negative $e$ directions fail by sign; the positive $y$
projection is at most $26/25<D$. Both $f$ projections are strictly below $D$, since
their absolute value is at most $\max(1029/1000,104/125)<6/5$. The positive $x$
alternative implies the positive $e$ alternative through the exact identity bound

$$
cX_6+sY_6-D\ge s(2c-1-as)>0
\quad\text{when }X_6\ge D.
$$

Here $2c-1-as\ge53/200$. Thus pair 0–6 forces $A\ge k:=u+1/2$.

For pair 1–9, the displacement is $(-\xi_9,Y_9)$. The positive $x$, negative $y$ and
negative $f$ directions fail by sign.
Positive $y$ is at most $219/200<D$, and both $e$ projections have absolute value at
most $\max(147/125,1533/2000)<6/5$. Horizontal-left separation implies positive $f$
separation because

$$
s\xi_9+cY_9-D\ge c(2s-1)>0
\quad\text{when }\xi_9\ge D,
$$

using $Y_9\ge h+s-1/2$. Its only other surviving alternative is positive $f$ itself.
Consequently $B+b\ge J:=3/2+u-sL$.

The identity $sA+c(B+b)=p_y+bc$ now contradicts $p_y+bc\le L-1-s-h$: it gives

$$
L\ge2+\frac{2u}{1+cs}
=2+\frac{4u}{1+u^2}
\ge\frac{4900}{1261}.
$$

The last function decreases for $u>1$. Substitution of $u=41/29$ gives the displayed
fraction, and $4900/1261-96/25=1444/31525>0$. This proves $\delta:=y_8+h-(L-1)>0$; the
equality case was part of the rejected branch.

The top vertex of square 8 has horizontal coordinate $X=x_8+(c-s)/2$. Its containment
through $x_9=x_8+ac+s$ gives

$$
X\le L-ac-2s\le66/25<3\le z+1.
$$

Consider the open set $K=\operatorname{int}(Q_8+C_8)\cap\{L-1<y<L\}$. It is nonempty and
convex, even when the top vertex touches $y=L$. The occupied top rectangles are
$[0,2]\times[L-1,L]$ and $[z,z+1]\times[L-1,L]$. Interior nonoverlap confines $K$ to the
union of the free strips $(2,z)\times(L-1,L)$ and $(z+1,L)\times(L-1,L)$. An open cap
point cannot remain on a shared vertical obstacle boundary: its neighborhood would enter
an obstacle interior.
Connectedness puts the cap in one strip.
The bound on $X$ excludes the right strip, including its closure.

Both descending edges from the top vertex have nonzero horizontal components of opposite
signs. Nearby interior cap points consequently occur on both sides of $X$, which proves
$2<X<z$. This is a geometric use of the complete nonoverlap conditions for pairs 2–8,
3–8 and 4–8. It does not select or omit any of their eight SAT alternatives.

At depth $d\le s$ below the top vertex, the section endpoints are $X-cd/s$ and $X+sd/c$,
with width $d/(cs)$. At $d=s$ that width is $1/c\ge5/4$, whereas $z-2\le L-3\le21/25$.
Therefore $\delta>s$ is impossible.
If $\delta=s$, sections with $d<s$ approaching $s$ already exceed the gap; equality is
also impossible. Hence $0<\delta<s<c$, and limits of the contained cap sections give the
weak inequalities

$$
X-c\delta/s\ge2,\qquad X+s\delta/c\le z,
\qquad \delta\le cs(z-2)\le21/50.
$$

These limits allow legal contacts at the bottom corners of the top squares.
In particular no closed forbidden polygon is treated as an overlap region.

The exact substitution identities are

$$
sX-c\delta=cL-c-1/2-(B+b),\qquad
cX+s\delta=A+3/2-sL+s.
$$

They give $B+b\le M:=cL-c-2s-1/2$ and the unused upper bound $A\le cz+sL-s-3/2$. The
decisive gap is

$$
J-M=2+2c+3s-Lu
\ge\frac{96t^2-42t+4}{25(1+t^2)}\ge\frac2{87}.
$$

For $d=t-1/3\ge0$, the numerator is $2/3+22d+96d^2$, and the denominator is at most
$29$. All signs and the margin hold at both angle endpoints.

## Complete SAT Reduction After Cap Localization

The cap bound gives $p_y\le49/25$, $y_7\le139/100$ and $y_9\le403/200$ by substituting
$\delta\le21/50$ into their retained formulas.
The following accounts for all eight alternatives of each remaining pair.

For pair 0–6, negative $x,y,e$ fail by sign.
Both $f$ projections have absolute value at most $\max(1029/1000,146/125)<6/5$. Positive
$x$ implies positive $e$ by the identity above.
If positive $y$ separates, $p_y\ge1+h$; the cap inequality $X>2$ gives
$p_x>2-3c/2+s/2+bs$. Therefore

$$
A>k+c(1-2c+s+bs)\ge k,
$$

since $1-2c+s+bs\ge0$. Direct positive $e$ also gives $A\ge k$. Thus its three possible
survivors all force the same row, including $a=b=0$.

For pair 1–7, the displacement is $(-\xi_7,Y_7)$, where
$\xi_7\ge h+c-bs-1/2\ge149/200>0$ and $1/5\le Y_7\le89/100$. Positive $x$, negative $y$
and negative $f$ fail by sign.
Positive $y$ and positive $e$ fail because $Y_7<D$ and $-c\xi_7+sY_7\le623/1000<D$.
Negative $e$ would give $A+a\le cL-c-1/2$, hence

$$
c(L-2)\ge1+s,
\qquad c(L-2)\le184/125<8/5\le1+s,
$$

a contradiction. Positive $f$ would require $B\ge J$, whereas $B\le M-b\le M<J$. Only
horizontal-left separation survives:

$$
x_7\le L-1-h.
$$

For pair 1–9, positive $x$, negative $y$ and negative $f$ again fail by sign.
Both $e$ projections have absolute value at most $\max(147/125,2121/2000)<6/5$, using
$Y_9\le303/200$. Horizontal-left separation implies positive $f$ by the earlier
identity. Vertical-above separation gives $Y_9\ge D$, while the newly forced horizontal
bound and $x_9=x_7+c-bs$ give $\xi_9\ge D-c+bs$. Consequently

$$
s\xi_9+cY_9\ge s(D-c+bs)+cD=D+bs^2\ge D.
$$

The equality here uses $D(u-1)=cs$ and remains valid when $b=0$. Thus vertical-above
also implies positive $f$. Direct positive $f$ is the final survivor.
Every alternative therefore gives $B+b\ge J$, contradicting $B+b\le M$ with the strict
margin $J-M\ge2/87$.

## Reconciliation With the Author’s Partial Results

The [author report](bc-273-analytic-author.md) is mathematically consistent with this
contradiction.
Its notation $E,F,K$ equals $A,B,D$ here; its two conditional $f$ rows are
exactly $M$ and $J$. Combining them yields $L\ge2+(2+s)/(c+s)\ge27/7$, with margin
$3/175$ over the target side cap.
The displayed angle derivative $(1-2(c-s))/(c+s)^2$ is positive.

The square-10 core is also valid: the largest actual angle difference has half-angle
tangent $1/17$, giving support factor at most $161/145$. A centered block-aligned square
of side $145/161$ is therefore contained in square 10. Its forbidden radius $153/161$
strictly exceeds $19/20$ by $1/3220$. The two pairs of overlapping column rectangles in
the author proof cover the stated closed rectangle inside the four open forbidden boxes.
The strict exterior disjunction is a necessary condition; taking its four weak closures
preserves coverage. It does not characterize full feasibility.

The author’s separate general proof of $A\ge u+1/2$ correctly reduces the extra vertical
possibility through pair 5–6. Its pair 4–8 screening leaves only downward vertical or
negative $f$ separation; the former conflicts with the two complete possibilities
retained for pair 1–9. This yields $B+b\le M$ and $y_9\ge1+h$. The top-pair 2–8
reduction correctly implies

$$
A+1\le cz+s(L-1)-1/2,\qquad
cs(z-2)\ge2+2c+(1-a)s-L.
$$

The claimed consequences $z-2\ge182/725>1/4$ and, when $s\le13/20$, $z-2>331/1000$
follow from the stated monotonicity and $\sqrt{231}/20>759/1000$.

I also checked the author’s seven excluded core-versus-square-2 directions and the
remaining negative-$f$ inequality.
Their right-compartment contradiction is valid.
The below-coordinate expression decreases in angle as claimed and has endpoint value
$1219/500<49/20$. The last two sine ranges give the positive rational differences
$1707/40000$ and $229/25000$. These checks validate that partial result within its
stated scope; they are not premises of the accepted skeleton proof.

The apparent difference between the reports is resolved by pair 1–7. The author leaves
the possibility that square 9 separates vertically above square 1. The adversary first
forces square 7 to the left of square 1, then proves that this vertical alternative for
square 9 also implies the incompatible $f$ row.
No source separation was assumed in either accepted deduction.
The author’s three unexcluded compartments consequently require no further work for the
frozen target once this skeleton contradiction is accepted.

The adversary’s displayed hand-proposed skeleton is correctly rejected as infeasible:
pair 1–7 has absolute projections $99/100,2/5,69/125,457/500$, all below $D=6/5$. Its
retained equations, containment and top-cap placement do not establish nonoverlap.

## Exact Scope and Remaining Obligations

The contradiction uses containment of the four-square block, the retained center
equations, the occupied top rectangles, the complete pair conditions identified above,
$L\le96/25$, $1/3\le t\le2/5$, $0\le a,b\le1/4$ and $2\le z\le L-1$. These are necessary
for every frozen ten-square skeleton.
The lower side endpoint and the redundant $p$ box were not strengthened.
No coordinate was fitted, no pose was reflected, and no equality seam was deleted.

Every $T_+$ point, for any $v\in[0,1]$ and any admitted $w$, would project to precisely
such a skeleton. Hence $T_+=\varnothing$ follows directly, covering its two other
square-10 angle children and their shared endpoints as well as $T_{\rm mid}$. The
conclusion includes $v=t$, $v=0,1$, possible 9–10 recontact, new contacts and all closed
slide, center, side and top-gap boundaries.
It does not require checking any square-10 SAT direction: an additional square cannot
make an impossible skeleton feasible.
The universal cavity-cover statement is satisfied because there are no admissible
skeletons.

The source at $L=U>96/25$ remains a feasible control in $P_+$. The named local ball was
not used in this proof.
Other block-angle intervals, negative or longer slides, short/zero retained segments,
other contact-side or wall assignments and other labels remain outside this exclusion.
No full family cover, finite motion, minimizing representative theorem or unrestricted
lower bound follows.

The next action is the coordinator’s scoped publication and record disposition of this
analytical result. The independent-reader and target feature-inclusion obligations of a
future BC261 implementation remain separate.
This review authorizes no new target attempt or instrument run.

## Work Receipt

The phase lease was recorded as `2026-09-07T08:11:12Z` through `2026-09-07T08:31:12Z`.
The first audit clock read was `2026-09-07T08:11:59Z`. Both analytical reports were
already terminal. I read both and reconstructed their displayed decisive bounds and SAT
implications by exact hand calculation, against the frozen protocol and accepted domain.
No numerical target, solver, target script or source-control replay was executed.

Only this assigned review was written.
No author report, Git state, registry, identifier or dependency was changed.
The document received the Practical Prose common-guidelines and de-slop passes and
installed Flowmark 0.4.0 with caching disabled.
The mathematical audit, full reread and initial document checks were complete at
`2026-09-07T08:22:30Z`, 10 minutes 31 seconds after the first clock read and 8 minutes
42 seconds before the hard deadline.
Flowmark’s full auto-format check passed; all five linked source files existed; the
whitespace scan found no trailing blanks; the required footer appeared once; and the
reread confirmed the equations and verdict table survived formatting.
The receipt is followed by a final scoped formatting check before delivery.
No background command remains.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
