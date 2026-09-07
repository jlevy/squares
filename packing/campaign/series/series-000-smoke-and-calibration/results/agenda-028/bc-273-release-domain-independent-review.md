# BC-273: Independent Review of the Segment 9–10 Release Domain

The [release-domain design](bc-273-release-domain-design.md) is accepted as a closed,
explicit source-feature pilot, with the rank qualification below.
The center formulas, six retained segments, diagonal sign restriction, exact Trump
parent membership, separation from the named local radius, and strict forbidden-center
cover equivalence are correct.
The existing exact source verifier passed again in this review.

The required determination of $T_{\rm mid}$ remains open.
This review accepts neither a uniform exclusion certificate nor BC-261 instrument
readiness. It is independent of the design author and inherits session-092 phase 2, W7
`pipeline-improvement`, under BC-261 and BC-273. The coordinator owns hypothesis status,
shared records and integration.
The acceptance rule remains
[H-120](../../../../hypotheses/H-120-rank-nine-release-exclusion.md): uniform coverage
and independent replay of the declared target, or an exactly verified feasible packing
in it.

## Verdicts and Required Qualification

| Claim | Review verdict | Limit |
| --- | --- | --- |
| Ten real parameters and the source contact-side equations | Accepted | Fixed labels, origin, wall assignments and the displayed oblique side pattern |
| Six positive segments and the selected $3/4$ lower bound | Accepted | The four oblique lengths use $0\le a,b\le1/4$; the two axis lengths are one |
| $ab\ge0$ | Accepted | Necessary and sufficient for the two oblique diagonal pair conditions when $\lvert a\rvert,\lvert b\rvert<1$; not a complete packing criterion |
| Complete containment and all 55 pair disjunctions | Accepted | Weak inequalities preserve all legal touching; no chosen source SAT cell replaces them |
| Closed rational pilot and actual-angle endpoints | Accepted | The selected pilot and its stated children, with no claim to the whole released family |
| Exact Trump in $P_+$ and outside $T_{\rm mid}$ | Accepted | Bound directly to the source corners and formulas, with fresh exact source feasibility |
| Separation from the retained local radius | Accepted | The named labelled, origin-anchored chart; no use of the local theorem to prove target infeasibility |
| Uniform cover by interiors of forbidden-center polygons | Accepted as an equivalence | The cover itself has not been established |
| Target exclusion, complete sibling cover or a feasible motion | Open | No target run or motion theorem in this review |

The design’s sentence “The angular equality graph … Its rank is nine” must mean the
**retained equality graph**. Its wall component has seven vertices, its four-square
component has four, and square 10 is a singleton.
A spanning forest therefore has $6+3=9$ edges.
An allowed 9–10 recontact segment joins the last two components and raises this angular
equality rank to ten.
The full graph is allowed to gain contacts; its rank is not fixed at nine throughout the
domain. Coincident component angles do not by themselves add a graph edge.
This is the qualification already required by
[BC-260](bc-260-direct-hybrid-contracts.md#direct-release-and-local-scope-binding).
The coordinator should make “retained” explicit in that design sentence before its rank
wording is reused. No equation or pilot bound needs to change for this correction.

## Reconstruction From Source Corners

The independent starting point was
[`packing.py`](../../../../../cases/trump11/packing.py), rather than the design’s center
equations. In the source, an axis square with lower-left corner $(x,y)$ has center
$(x+1/2,y+1/2)$. A tilted source square with local origin $(o_x,o_y)$ has corners

$$
(1,1)+(o_x+d_x)e+(o_y+d_y-r_1)f,
\qquad(d_x,d_y)\in\{0,1\}^2,
$$

so averaging its corners gives

$$
C(o_x,o_y)=(1,1)+(o_x+1/2)e+(o_y+1/2-r_1)f.
$$

The source edge differences are $e$ and $f$, with $e\cdot f=0$ and unit norms.
Thus the normal and tangential directions used below are the directions of the source
corners themselves.

The six axis centers reconstruct as

$$
\begin{aligned}
C_0&=(1/2,1/2),& C_1&=(L-1/2,1/2),\\
C_2&=(z+1/2,L-1/2),& C_3&=(1/2,L-1/2),\\
C_4&=(3/2,L-1/2),& C_5&=(1/2,L-3/2).
\end{aligned}
$$

The nine required flush incidences force the axis orientation modulo quarter turns and
the fixed coordinates shown.
Squares 3 and 4 have the same top-wall height.
A positive contact segment requires their horizontal centers to differ by one;
containment rules out placing 4 to the left of 3. Squares 3 and 5 have the same
left-wall abscissa, and containment rules out placing 5 above 3. Their center
differences are consequently $(1,0)$ and $(0,-1)$, respectively.
Square 4 and square 5 meet at the forced point $(1,L-1)$. The top-row nonoverlap
conditions force $z\ge2$, and right containment of square 2 gives $z\le L-1$.

For the oblique component, first allow distinct slides on all four retained edges:

$$
\begin{aligned}
C_7-C_6&=a_1e-f,& C_8-C_6&=e+b_1f,\\
C_9-C_7&=e+b_2f,& C_9-C_8&=a_2e-f.
\end{aligned}
$$

The two paths from 6 to 9 give $(a_1-a_2)e+(b_2-b_1)f=0$. Independence of $e,f$ forces
$a_1=a_2=a$ and $b_1=b_2=b$. Writing $p=C_6$ gives exactly

$$
C_6=p,\quad C_7=p+ae-f,\quad C_8=p+e+bf,\quad
C_9=p+(a+1)e+(b-1)f.
$$

All six normal and tangential checks are therefore:

| Pair | Normal coordinate | Tangential coordinate | Segment length |
| --- | --- | --- | --- |
| 3–4 | $(C_4-C_3)\cdot(1,0)=1$ | $(C_4-C_3)\cdot(0,1)=0$ | $1$ |
| 3–5 | $(C_5-C_3)\cdot(0,1)=-1$ | $(C_5-C_3)\cdot(1,0)=0$ | $1$ |
| 6–7 | $(C_7-C_6)\cdot f=-1$ | $(C_7-C_6)\cdot e=a$ | $1-\lvert a\rvert$ |
| 6–8 | $(C_8-C_6)\cdot e=1$ | $(C_8-C_6)\cdot f=b$ | $1-\lvert b\rvert$ |
| 7–9 | $(C_9-C_7)\cdot e=1$ | $(C_9-C_7)\cdot f=b$ | $1-\lvert b\rvert$ |
| 8–9 | $(C_9-C_8)\cdot f=-1$ | $(C_9-C_8)\cdot e=a$ | $1-\lvert a\rvert$ |

Square 10 has its own center $w$ and actual angle.
The remaining coordinates are $(L,z,p_x,p_y,a,b,t,w_x,w_y,v)$, ten real parameters.
This is a parameter count, not a claim that the feasible set is ten-dimensional or
supports a finite motion.

For the diagonals, the common-basis displacements are $(1+a,b-1)$ and $(1-a,1+b)$. Under
$|a|,|b|<1$, their SAT conditions reduce to

$$
(a\ge0\ \lor\ b\le0)\quad\land\quad(a\le0\ \lor\ b\ge0),
$$

equivalently $ab\ge0$. At $(a,b)=(1/8,-1/8)$ the 7–8 displacement is $(7/8,7/8)$, so
those interiors overlap.
At $(-1/8,1/8)$ the 6–9 displacement is $(7/8,-7/8)$, again an overlap.
At $a=b=0$, the four centers form a unit grid block and both diagonals touch at a point.
These are exact component checks by substitution, not asserted eleven-square feasible
examples or software controls claimed to have run.

## Exact Source Membership and Seams

Write $u$ for the isolated source root, $U$ for its container side and $c=c(u)$,
$s=s(u)$. Averaging the five source tilted squares gives the design’s binding

$$
\begin{gathered}
t=v=u,\quad L=U,\quad z=x_0,\quad a=u_1,\quad b=v_1,\\
p=(1,1)+\tfrac12e+(\tfrac12-r_1)f,\qquad
w=p+(a+2)e-v_2f.
\end{gathered}
$$

In particular the sign in front of $v_2f$ is negative, and $b$ is the source’s $v_1$,
not its negative. No fitted numerical center enters the binding.

The design’s coarse rational source bounds are valid.
Its inference $a\ge0$ from source feasibility, $b>0$ and the diagonal lemma is also
valid. A direct independent source bound strengthens this to $a>0$: monotonicity of
$c(u),s(u),U(u)$ on $u\in(36/100,37/100)$ and exact endpoint comparison give

$$
\frac{759}{1000}<c<\frac{771}{1000},\qquad
\frac{637}{1000}<s<\frac{651}{1000},\qquad
\frac{387}{100}<U<\frac{97}{25}.
$$

For the last upper bound, $U(37/100)=62200/16031<97/25$, with positive denominator.
These bounds imply $8/25<r_1<17/50$. Hence

$$
(1+r_1)c>\frac{33}{25}\frac{759}{1000}
=\frac{25047}{25000}>1,
$$

and the source formula $a=((1+r_1)c-1)/s$ yields $a>0$. Combining this with the design’s
valid coarse upper bounds gives

$$
0<a<\frac15<\frac14,\qquad
\frac1{20}<b<\frac15<\frac14.
$$

Thus all four source oblique retained segments have length greater than $4/5$, and the
closed pilot’s weaker $3/4$ margin is satisfied.
The source root belongs to $[1/3,2/5]$, and the fresh exact containment/nonoverlap check
supplies the remaining geometric conditions.
In particular source feasibility implies $2\le x_0\le U-1$. Every contained unit-square
center has both coordinates in $[1/2,U-1/2]$, so $p,w$ obey the parent box
$[1/2,7/2]^2$.

The 9–10 seam can also be checked from the source formulas.
Its displacement is

$$
C_{10}-C_9=e+(1-b-v_2)f.
$$

The same rational bounds and $0<a<1/5$ give

$$
0<\frac{2870}{651}-\frac{17}{50}-\frac{16}{5}\frac{771}{637}
<v_2<\frac{2880}{637}-\frac8{25}-3\frac{759}{651}<\frac45.
$$

Consequently $0<1-b-v_2<19/20$. The normal gap is exactly zero and the tangential
overlap is positive: the source has a 9–10 segment, not merely a coincident angle.
This agrees with the retained
[exact contact inventory](../exp-013-h-026-trump-tangent.json), which lists both source
axis owners for pair 9–10. It explains why treating the full equality graph as rank nine
would fail even at the positive parent control.

The verifier replay used the project interpreter, Python 3.14.7, and the existing entry
point from `packing/`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  /Users/levy/wrk/github/squares/packing/.venv/bin/python3 \
  -m cases.trump11.verify_exact
```

It exited zero and reported `VALID: 11 squares, 55 pairs tested`, 20 boundary corner
coordinates, 14 zero-gap pairs and 41 strictly separated pairs.
The exact published side-polynomial identity was true.
The verifier reported `0.154 s` and zero interval refinements.
This is a known-source feasibility replay; it does not execute a new release-domain
reader or any H-120 target.

## Closed Domain, Actual Angles and Local Separation

For $r\in[0,1]$, the declared rational basis is orthonormal and has actual angle
$2\arctan r$. Its denominator $1+r^2$ is strictly positive.
At $r=1$, $e=(0,1)$ and $f=(-1,0)$, which gives the same physical square orientation as
$r=0$ after a quarter turn and a corner-label change.
The two endpoint representations are included.
Equal-angle cases $v=t$ remain included.
Neither endpoint identification nor equality licenses deleting a SAT alternative without
an exact equivalence.

For any declared square, projection onto an axis $n$ has center $C_i\cdot n$ and
half-width $H_i(n)$. For coordinate axes the half-widths agree and are
$h_i=(|\cos\theta_i|+|\sin\theta_i|)/2\ge1/2$. Therefore the stated four center
containment bounds are exactly equivalent to corner containment.
For each unordered pair, the eight directed alternatives are the complete four-axis SAT
disjunction. Equality permits boundary contact.
All 55 pairs are present, including 45 skeleton pairs and the ten square-10 pairs.

At fixed $t,v$, the center substitutions and every selected support/SAT row are affine
in the other eight parameters.
Continuous angle boxes require uniform coefficient and error control; fixed-angle LP
infeasibility alone has no such implication.
Positive denominators and finite absolute-value sign cases give the claimed rational
polynomial description without changing inequality direction.

The reviewed parent bounds are

$$
\frac{381}{100}\le L\le4,\quad
\frac13\le t\le\frac25,\quad 0\le v\le1,\quad
0\le a,b\le\frac14,\quad 2\le z\le L-1,\quad
p,w\in[1/2,7/2]^2.
$$

The target $T_+$ adds $L\le96/25$, and its first child $T_{\rm mid}$ adds
$1/3\le v\le2/5$. These are the bounds accepted here.
The pilot bounds on $L,t,v,a,b,z,p,w$ are closed and bounded.
The finite SAT disjunction defines a closed set, as do all feature and containment
equations. The parameter domain is compact, and its continuous geometric image is
compact. Retained segment lengths are at least $3/4$ throughout this domain, including
slide endpoints. For $L\le96/25$, containment gives the claimed center box
$[1/2,167/50]^2$. For $L\le4$, the parent center box is $[1/2,7/2]^2$. These extra boxes
are necessary consequences of containment, so their inclusion loses no admitted center.

The local separation uses the exact square-3 coordinate from the source and the
[retained local chart](../../../../../cases/trump11/isolation-theorem.md#exact-witness-and-chart).
The source side function satisfies

$$
U'(u)=\frac{6u^2+8u-2}{(1+2u-u^2)^2}>0
\quad\text{on }[36/100,37/100].
$$

Thus every target point obeys

$$
\|q-q_*\|_\infty\ge|C_{3,y}-C^*_{3,y}|=U-L
>\frac{1925}{497}-\frac{96}{25}
=\frac{413}{12425}>\frac3{100}
>\frac{808514697}{200000000000}.
$$

The compared coordinate is $C_{3,y}=L-1/2$ versus $U-1/2$ in the same labelled,
origin-anchored center/radian sup norm.
Side is not a thirty-fourth norm coordinate.
This separation exceeds the retained radius and therefore excludes intersection with
either its open interior or its boundary.
It requires no angle-lift estimate because the center coordinate already separates the
sets. It is new scope relative to that named local ball, not new exclusion geometry.
Other relabellings and symmetry charts have not been compared.
Since $U>96/25$, source parent membership fails the target side cap alone; all other
$T_{\rm mid}$ restrictions hold at the source.

## Forbidden-Center Equivalence

Fix an admitted ten-square skeleton $S$ and an allowed square-10 angle $v$. Its
contained center region is exactly $B_v=[h_{10},L-h_{10}]^2$. The redundant parent or
target center box imposes no further restriction on $B_v$.

Let $Q_i$ and $Q_{10}(v)$ be the closed, centered unit squares.
Their interiors are nonempty, and central symmetry gives $-Q_{10}=Q_{10}$. Their
forbidden-center polygon is

$$
F_i=C_i+Q_i+Q_{10}(v).
$$

For convex bodies with nonempty interiors,
$\operatorname{int}(A+B)=\operatorname{int}A+\operatorname{int}B$: the right-hand side
is an open convex set whose closure is the compact sum $A+B$, and an open convex set is
the interior of its closure.
It follows that

$$
\begin{aligned}
w\in\operatorname{int}F_i
&\iff w-C_i\in\operatorname{int}Q_i+\operatorname{int}Q_{10}\\
&\iff (C_i+\operatorname{int}Q_i)\cap
(w+\operatorname{int}Q_{10})\ne\varnothing.
\end{aligned}
$$

The last equivalence follows by taking an intersection point in one direction, and using
$-\operatorname{int}Q_{10}=\operatorname{int}Q_{10}$ in the other.
Therefore a legal eleventh square exists exactly when

$$
B_v\setminus\bigcup_{i=0}^9\operatorname{int}F_i\ne\varnothing.
$$

Uniform strict coverage for every admitted skeleton and every allowed $v$ is exactly
equivalent to $T_{\rm mid}=\varnothing$. The skeleton has seven parameters; adding the
eleventh square’s angle and two center coordinates restores ten.
Covering $B_v$ by the closed $F_i$ would be insufficient: a center on obstacle
boundaries can describe a legal touching packing.
For example, two axis unit squares whose centers differ by $(1,0)$ meet along an edge,
while that displacement lies on the boundary of their Minkowski sum.
The design’s interior convention is correct.

## Remainders and the Next Bounded Task

The pilot does not construct a complete cover of the retained feature family.
The following remain explicit:

- The negative-slide branch $a,b\le0$, longer slide ranges, and the positive segments
  shorter than the selected $3/4$ margin remain open.
  The two closed sign branches retain their zero-slide seams.
- At $|a|=1$ or $|b|=1$, the common-angle formulas cover their own closure.
  A physical degeneration sibling must also cover any orientations freed when positive
  contact edges disappear; it can have a lower retained rank.
- Other contact-side assignments, different wall patterns, labels or joint symmetries
  have not been enumerated or reduced to this chart.
- Component angles outside $t\in[1/3,2/5]$ remain open.
  Within $T_+$, the square-10 children $v\in[0,1/3]$ and $v\in[2/5,1]$ remain open
  alongside $T_{\rm mid}$; adjoining children share their endpoint seams.
- Square 10’s axis cases $v=0,1$, coincident-angle cases, 9–10 point or segment
  recontact, and new contacts elsewhere remain allowed where their child includes them.
  The pilot imposes no positive 9–10 separation gap and no fixed full graph rank.
- The local-radius comparison covers the named chart only.
  Extensions toward that radius must retain its boundary or prove a positive separation
  margin. Bounds on $L$ outside the declared target interval have no target verdict here.
- All six-axis/four-plus-one packings, a minimizing representative theorem, KKT
  conclusions and finite motion remain outside this pilot’s accepted scope.

The smallest missing mathematical premise is still the uniform cavity cover, or an
equivalent complete SAT exclusion, over the declared target.
No containment reduction, rank count or diagonal restriction here supplies that premise.

The next bounded W7 task is BC-261’s independent reconstruction of one controlled
uniform leaf supporting the actual consumer requirements: these center equalities,
variable $L$, and two nonzero angle intervals.
It must bind its physical descriptor, outer rows and any certificate to the same domain.
The same reader must accept the exact source parent/seam control and refuse a reversed
cycle normal, a missing declared pair alternative, a changed wall dependence or a
closed-polygon substitution.
A complete small control cover is still required before instrument readiness.
The design’s numerical source-cell scan does not substitute for those controls.

The coordinator can now prospectively freeze this accepted pilot definition while
retaining H-120 as open.
A scientific target is appropriate only after the required reader, implication and
controls are accepted and its target/replay cost is declared.
If an existing BC-261 leaf cannot express the retained equalities or variable side, that
concrete interface gap is the next implementation obligation.

## Work Receipt

The first clock read was `2026-09-07T06:55:42Z`. Direct inspection covered the design,
source construction and verifier, retained source contact inventory, local theorem
chart, H-120 and BC-260. The contact reconstruction, interval bounds and cover
equivalence above are analytic review calculations.
They were not obtained from one-off numerical code.
Only the existing known-source verifier was executed; no scientific target, mutable
instrument target, registry, dependency or Git mutation was performed.
The verifier’s initial login shell printed a failed attempt to create an unrelated fnm
shell-state symlink; the interpreter and verifier themselves exited zero.
Subsequent shell calls disabled login startup.

The review writes only this assigned Markdown report.
Shared bead and session updates remain with the coordinator; `tbd prime` supplied
read-only project orientation.
The document received the Practical Prose common-guidelines and de-slop passes.
Flowmark 0.4.0 initially parsed literal absolute-value bars in Markdown tables as column
separators: it truncated the four review segment cells to `$1-` and the diagonal-lemma
verdict scope to `when $`. Those five cells were restored with `\lvert` and `\rvert`. At
`2026-09-07T07:07:54Z`, the design still retained its source text in the segment,
short/zero-feature, negative-slide, recontact and positive-margin table cells.
Those table occurrences need the same spelling before formatting; this document
correction does not change the accepted mathematics.
The coordinator was notified.
The terminal review checkpoint was `2026-09-07T07:09:42Z`, exactly 14 minutes after the
first clock read.
Flowmark 0.4.0 passed its full auto-format check with `--no-cache`; the
whitespace scan found no trailing blanks; all six linked files existed; the footer count
was one; and a reread confirmed every table formula survived formatting.
No background command remains.
The next task is the bounded BC-261 control-reader work described above; H-120’s target
determination remains open.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
