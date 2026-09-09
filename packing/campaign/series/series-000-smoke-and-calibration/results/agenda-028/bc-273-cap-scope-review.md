# BC-273: Independent Cap and Scope Review

**Accepted within this audit: the cap localization and inequalities (9)–(12) of the
[analytical adversary](bc-273-analytic-adversary.md), conditional on its preceding proof
that $\delta>0$.** Their treatment of legal touching is sound.
If the separate whole-argument audit accepts the ten-square contradiction, it also
excludes the design’s entire $T_+$, including every admitted square-10 angle.
This report does not independently accept the preceding protrusion lemma or the
subsequent complete SAT reduction.

This is the session-092 phase-5 independent correctness audit assigned to the cap and
scope questions. The reviewer did not author either target attempt.
The reviewed premises are the [frozen protocol](bc-273-analytic-release-protocol.md) and
[release design](bc-273-release-domain-design.md), with their original labels, contact
sides, parameter bounds, containment and legal equality conventions.
The protocol explicitly permits an independently audited proof using exact necessary
inequalities. The cap argument uses this route; it does not claim a closed
forbidden-polygon cover.

## Connected Open Cap and Its Boundaries

Let $H=y_8+h$, $\delta=H-(L-1)>0$ and $X=x_8+(c-s)/2$. Here $h=(c+s)/2$, $e=(c,s)$ and
$f=(-s,c)$ are exactly the design’s actual-angle basis for squares 6 through 9. On the
whole closed interval $1/3\le t\le2/5$, one has $c>s>0$. In particular, the numerator of
$c-s$ is $1-2t-t^2\ge1/25>0$; its denominator is positive.
No endpoint or angle-coincidence case is removed to obtain the cap geometry.

For precision, interpret the report’s “open portion” as

$$
K=\operatorname{int}(S_8)\cap\{(x,y):L-1<y<L\}.
$$

Containment gives $H\le L$ and puts every interior point of square 8 strictly inside the
container. The strict protrusion $\delta>0$ makes $K$ nonempty.
It is open and convex, hence connected.
At these heights, squares 3 and 4 occupy the full interval $[0,2]$, and square 2
occupies $[z,z+1]$.

The fact that touching is legal creates no extra open corridor along $x=1$, the shared
edge of squares 3 and 4, or along their outer vertical boundaries.
If a point of $K$ were on such a line, its open neighborhood in $K$ would enter the
interior of an adjacent obstacle.
Thus every point of $K$ lies in one of the two open free strips $2<x<z$ or $z+1<x<L$.
Connectedness puts the entire cap in one of them.
This also handles the degenerate cases $z=2$ or $z+1=L$: the corresponding strip is
empty, not a new seam to cover.

The source-feature identity and containment of square 9 give

$$
x_9=x_8+ac+s\le L-h,
\qquad
X\le L-ac-2s\le\frac{66}{25}<3\le z+1.
$$

Interior cap points approach the highest vertex.
If $K$ lay in the right strip, their limiting horizontal coordinate would satisfy
$X\ge z+1$, contrary to this strict bound.
Hence $K\subset\{2<x<z\}$.

Taking limits initially gives only $2\le X\le z$. To check the report’s strict version,
take any sufficiently small depth $d>0$ below the highest vertex, with
$d<\min(\delta,s)$. The horizontal interior section is

$$
X-\frac cs d<x<X+\frac sc d.
$$

It contains points on both sides of $X$. Therefore $X=2$ or $X=z$ would put interior cap
points inside an obstacle.
This proves $2<X<z$. When $H=L$, the same sections have height $L-d<L$, so the argument
does not mistake the legal top-wall contact for overlap.
The use of strict apex inequalities and weak base inequalities is justified by different
local geometries.

## Section Width, Triangular Limit and Exact Algebra

The two edges descending from the highest vertex have vectors $-e$ and $-f$. Their
respective vertical drops to the adjacent vertices are $s$ and $c$. Consequently, for
$0<d\le s<c$, the closed horizontal section has endpoints $X-cd/s$ and $X+sd/c$, and
width

$$
d\left(\frac cs+\frac sc\right)=\frac{d}{cs}.
$$

At $d=s$ the width is $1/c\ge5/4$, while the central gap has width $z-2\le L-3\le21/25$.
If $\delta>s$, this section has height strictly above $L-1$ and below $L$, so its
interior must fit inside that smaller gap, a contradiction.
If $\delta=s$, the section at $y=L-1$ itself is not treated as an overlap: sections with
$d<s$ approach width $1/c>21/25$ and already exceed the gap while remaining strictly
above $L-1$. Thus equality also fails, and $0<\delta<s<c$ follows.

The cap is therefore triangular.
Passing to the limit $d\uparrow\delta$ in its interior sections gives exactly the weak
inequalities

$$
X-\frac cs\delta\ge2,
\qquad
X+\frac sc\delta\le z.
$$

They allow a base endpoint to equal $2$ or $z$ at $y=L-1$. Such a bottom-corner contact
is legal and has not been discarded.
Subtracting the endpoints gives $\delta/(cs)\le z-2$. Since $cs\le1/2$ and
$z-2\le21/25$, this yields $\delta\le cs(z-2)\le21/50$. Every divisor here is strictly
positive throughout the declared closed angle interval.

I independently expanded the change of coordinates.
With $A=cp_x+sp_y$ and $B=-sp_x+cp_y$,

$$
X=p_x+\frac{3c-s}{2}-bs,
\qquad
\delta=p_y+s+bc+\frac{c+s}{2}-L+1.
$$

Using $c^2+s^2=1$ gives the exact identities

$$
sX-c\delta=cL-c-\frac12-(B+b),
\qquad
cX+s\delta=A+\frac32-sL+s.
$$

Multiplying the left base inequality by $s>0$ therefore proves, equivalently,

$$
B+b\le cL-c-2s-\frac12=M.
$$

Multiplying the right base inequality by $c>0$ likewise gives $A\le cz+sL-s-3/2$, as
reported. These are exact equivalences with the individual base inequalities, not
approximate or fixed-angle substitutions.

No missing boundary premise was found in (9)–(12). The explicit definition of $K$ and
the neighborhood argument at the shared top-square seam above make the report’s
compressed localization step fully explicit; they do not add a geometric restriction.

## What Omitting Square 10 Proves

The frozen question is $T_{\rm mid}=\varnothing$. The design’s larger $T_+$ has the same
side, four-square angle, slides, top-row position and retained feature equations, but
permits every $v\in[0,1]$. Deleting square 10 from any hypothetical point of $T_+$
leaves a ten-square skeleton satisfying every necessary condition used in the
adversary’s two branches: the displayed bounds, retained component equations,
containment, occupied top-row rectangles and nonoverlap of pairs 0–6, 1–7 and 1–9. The
proof has no premise involving $w$, $v$, square-10 containment or a separation from
square 10.

Therefore, if the complete ten-square contradiction is independently accepted,
$T_+=\varnothing$ follows directly by projection.
In particular, $v=0$, $v=1$, $v=t$, and every square-9–10 recontact are covered without
a limiting-angle argument or an eleventh-square cavity enumeration.
No converse projection or extension of an arbitrary skeleton to eleven squares is
required. Merely proving the middle-angle child empty by a square-10-dependent argument
would not have justified this inference; the absence of every square-10 premise in this
particular contradiction does.

This conditional corollary preserves $381/100\le L\le96/25$, $1/3\le t\le2/5$,
$0\le a,b\le1/4$, and the fixed labelled contact-side and wall pattern.
It does not cover other four-square angles, negative or larger slides, shorter or
vanished retained segments, different contact sides or wall patterns, or the
unrestricted rank-nine family.
It supplies no global packing bound by itself and does not change the prospective
question or its independent acceptance requirement.

The remaining audit obligation is the whole argument: the protrusion proof, its exact
range bounds, the complete surviving SAT reductions and the final strict contradiction.
The separate whole-argument reader owns that determination.
This focused review finds no cap or square-10-scope obstruction to accepting it.

## Timing and Checks

The prospective phase-5 lease was 08:12:35–08:22:35 UTC on 2026-09-07. This review’s
first recorded clock read was 08:13:07 UTC. Mathematical review and document readback
ended at 08:19:24 UTC, 6 minutes 17 seconds after that start.
The checks were independent symbolic reconstruction of the connected-cap argument, the
wall and base equalities, the case $\delta=s$, the exact cross-section endpoints and
width, both affine-coordinate identities, and the projection of $T_+$ to the proof’s
necessary ten-square conditions.
The frozen protocol, design and adversary report were read directly.
No numerical search, solver, target script, sampled target measurement or scientific
target command ran. Only this review file was written; no shared registry, Git state,
identifier or dependency was changed.
Installed Flowmark 0.4.0 formatted this file and passed its check with the incremental
cache disabled. Formatting is a document check, not mathematical evidence.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
