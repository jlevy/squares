# BC-280: Independent Admission of the Full-Angle Release Domain

**Accept the frozen domain as defined.** It is a complete closed physical angle chart
for this signed short-slide source-feature family.
The ten parameters, source corner binding, six retained segments, nine prescribed flush
incidences, 44 actual containment inequalities and 55 complete pair disjunctions are
consistent. The eight closed angle/sign children cover it, and exactly the two
middle-angle children inherit the accepted exclusions.
No new target theorem is established by this admission.

The reviewed artifact is the
[frozen domain design](bc-280-full-angle-release-domain.md).
I independently read the [source code](../../../../../cases/trump11/packing.py),
[original release domain](bc-273-release-domain-design.md), its
[source-corner review](bc-273-release-domain-independent-review.md), the
[signed-domain review](bc-276-negative-slide-domain-review.md), and the completed
[positive](bc-273-analytic-independent-review.md) and
[negative](bc-276-negative-slide-independent-review.md) mathematical audits.
I did not use the concurrently drafted target protocol as evidence for admission.

## Source Coordinates, Corners and Retained Features

Use $E=(1,0)$ and $F=(0,1)$. The source’s axis square at lower-left corner $(x,y)$ has
center $(x+1/2,y+1/2)$. Its six listed origins therefore give exactly the design’s
centers

$$
\begin{aligned}
C_0&=(1/2,1/2),&C_1&=(L-1/2,1/2),\\
C_2&=(z+1/2,L-1/2),&C_3&=(1/2,L-1/2),\\
C_4&=(3/2,L-1/2),&C_5&=(1/2,L-3/2).
\end{aligned}
$$

For a tilted source square with local origin $(o_x,o_y)$, the actual ordered corners are

$$
(1,1)+(o_x+d_x)e+(o_y+d_y-r_1)f,
\quad(d_x,d_y)=(0,0),(1,0),(1,1),(0,1).
$$

Their center is $(1,1)+(o_x+1/2)e+(o_y+1/2-r_1)f$. Subtracting this center gives the
successive corner offsets

$$
-(e+f)/2,\quad(e-f)/2,\quad(e+f)/2,\quad(-e+f)/2.
$$

These are exactly the design’s $V_{i,0},\ldots,V_{i,3}$ labels.
Unit orthogonal $e,f$ with determinant one make this counterclockwise order valid
throughout the chart.
The outward normals of edges $[0,1],[1,2],[2,3],[3,0]$ are respectively $-f,+e,+f,-e$. A
corner’s label is its algebraic source label, not its height order.

For the four-square component, closure of the two paths from 6 to 9 equates opposite
slides. The common-basis centers are exactly

$$
C_6=p,\quad C_7=p+ae-f,\quad C_8=p+e+bf,\quad
C_9=p+(a+1)e+(b-1)f.
$$

Square 10 has independent center $w$ and basis at $v$. The six source contact-edge
assignments check as follows:

| Pair | First/second edges | Normal displacement | Tangential displacement |
| --- | --- | --- | --- |
| 3–4 | $[1,2]/[3,0]$ | $+E$ coordinate $1$ | $F$ coordinate $0$ |
| 3–5 | $[0,1]/[2,3]$ | $F$ coordinate $-1$ | $E$ coordinate $0$ |
| 6–7 and 8–9 | $[0,1]/[2,3]$ | $f$ coordinate $-1$ | $e$ coordinate $a$ |
| 6–8 and 7–9 | $[1,2]/[3,0]$ | $e$ coordinate $1$ | $f$ coordinate $b$ |

The first two segments have length one; the other four have lengths $1-\lvert a\rvert$
or $1-\lvert b\rvert$, at least $3/4$ on the signed box.
This remains true at both axis lifts, zero slides and slide endpoints.
Squares 4 and 5 also meet at the forced point $(1,L-1)$.

The nine prescribed flush incidences are exactly 0 left/bottom, 1 bottom/right, 2 top, 3
left/top, 4 top and 5 left.
The top-row ordering gives $z\ge2$ and right containment of square 2 gives $z\le L-1$.
Additional wall or inter-square contacts remain legal.
The retained angular-equality forest has rank $6+3=9$; the full contact graph may have
higher rank. This count supplies no feasible motion or dimension theorem.

## Full Actual-Angle and Geometric Domain

For either $r=t$ or $r=v$, direct substitution gives

$$
c(r)^2+s(r)^2=1,\qquad
\det(e(r),f(r))=1,
$$

with denominator $1+r^2>0$. The actual angle $2\arctan r$ traverses the whole closed
interval $[0,\pi/2]$ when $r\in[0,1]$. Both axis lifts are retained.
The definition contains no hidden $c\ge s$ restriction and no division by $c$, $s$ or
$c-s$.

The admitted bounds are exactly

$$
381/100\le L\le96/25,\quad t,v\in[0,1],\quad a,b\in[-1/4,1/4],
$$

$$
2\le z\le L-1,\qquad p,w\in[1/2,7/2]^2.
$$

The parent changes only the upper side bound to four.
Variable $L$ remains a parameter; enlarging a container while holding the physical
arrangement fixed generally destroys these flush incidences.

For every declared actual square, $H_i(n)=(|n\cdot e_i|+|n\cdot f_i|)/2$. Its coordinate
half-supports are equal and satisfy $1/2\le h_i\le1/\sqrt2$. Thus the four scalar
support containment rows per square are equivalent to actual corner containment.
There are 44 such rows; they are not 44 prescribed wall contacts.
Parent containment already bounds each center in $[1/2,7/2]^2$, and target containment
bounds it in $[1/2,167/50]^2$, so the boxes on $p,w$ discard no contained center.

The four actual edge axes and both signs give a complete eight-alternative SAT
disjunction for each pair.
Their weak threshold is the sum of actual supports, not an average-angle substitute.
Equality permits point or segment touching.
The pair count is $15+24+6+10=55$: the axis component, its block cross pairs, the block
pairs and all square-10 pairs.
Both block diagonals remain.
Duplicate axes at equal angles do not remove a clause or an endpoint.

The parameter bounds and all conditions are closed; SAT is a finite disjunction of
closed inequalities.
All maps are continuous and the parameter box is bounded.
The domain and its geometric image are compact.
Finite exact absolute-value branches and positive-denominator clearing give the stated
semialgebraic description.
At fixed $t,v$, selected SAT rows are affine in the other eight parameters; this
observation is not a certificate over a continuous angular interval.

## Four Quarter-Turn Lifts and Endpoint Checks

Put $U=ae-f$ and $V=e+bf$, so the four block centers are $p,p+U,p+V,p+U+V$. Direct
substitution in each row gives:

| Lift | New block edge vectors | New origin | Old labels in new slots $(6,7,8,9)$ | Corner cycle |
| --- | --- | --- | --- | --- |
| 0 | $U,V$ | $p$ | $(6,7,8,9)$ | $k$ |
| 1 | $V,-U$ | $p+U$ | $(7,9,6,8)$ | $k+1$ |
| 2 | $-U,-V$ | $p+U+V$ | $(9,8,7,6)$ | $k+2$ |
| 3 | $-V,U$ | $p+V$ | $(8,6,9,7)$ | $k+3$ |

The bases are respectively $(e,f),(f,-e),(-e,-f),(-f,e)$; the slides are
$(a,b),(b,a),(a,b),(b,a)$. For example, in lift 1, $b f-(-e)=V$ and $f+a(-e)=-U$. The
other rows follow by the displayed substitutions.
For the same physical square, changing the basis to $(f,-e)$ sends new corner 0 to old
corner 1. Iteration proves every listed corner cycle modulo four.

Each new origin is an old contained center, so its bound holds.
The source contact cycle maps to itself, with the corresponding edge-label cycles.
Physical shapes, containment and the complete pair inventory are preserved.
The axis square labels and square 10 are fixed.
The operation swaps slides or leaves them unchanged; it does not reverse their signs.

These identities preserve the physical geometry with the lifted basis.
For an interior angle, a nonzero quarter-turn lift generally leaves the chosen
real-angle interval; the table is not an unrestricted parameter symmetry of the selected
chart. Returning to that chart requires consistent basis, slot and corner conversion.
A particular labeled recontact child need not map to itself either: under lift 1, old
square 9 becomes new square 7, so an old 9–10 contact becomes a new 7–10 contact.
Neither contact is required in the defining domain.
Any later margin child singled out by $g_{9,10}$ needs its label map; it cannot inherit
invariance of that individual scalar without checking it.

At $t=0$ the block centers relative to $p$ are $(0,0),(a,-1),(1,b),(a+1,b-1)$. At $t=1$
they are $(0,0),(1,a),(-b,1),(1-b,a+1)$. These match the design.
Lift 1 maps the first representation to the second with its required simultaneous
origin, slide and label changes.
Holding $p,a,b$ fixed would not preserve the labeled centers.
Square 10’s $v=0,1$ lifts preserve its center and cycle its corners.

For $0<t<1$, both vertical basis components are positive, so corner 2 is uniquely
highest. At $t=0$, corners 2 and 3 form the highest edge; at $t=1$, corners 1 and 2 do.
The $c=s$ seam at $\tau=\sqrt2-1$ has a unique highest corner and is regular.
These facts verify labels and degeneracies; they prove no enlarged cap inequality.

## Eight Closed Children and Exactly Inherited Scope

The two common-basis diagonal displacements are $(1+a,b-1)$ and $(1-a,1+b)$. On the
strict short-slide range contained in this box, their complete SAT conditions are
exactly

$$
(a\ge0\ \lor\ b\le0)\quad\land\quad(a\le0\ \lor\ b\ge0),
$$

or $ab\ge0$. This reduction uses orthonormality, not $c>s$. The mixed controls
$(a,b)=(1/8,-1/8)$ and $(-1/8,1/8)$ fail their respective diagonal clauses; at $a=b=0$
both diagonals have legal point touching.
None is an eleven-square feasibility control.

Hence the two closed sign children cover every domain point, overlap at $a=b=0$, and
retain every one-zero boundary.
Cross them with

$$
[0,1/3],\quad[1/3,2/5],\quad[2/5,\sqrt2-1],\quad[\sqrt2-1,1].
$$

These four intervals cover $[0,1]$, with their common endpoints in both adjacent
children. The algebraic separator is uniquely specified by $\tau^2+2\tau-1=0$, $\tau>0$,
and satisfies $2/5<\tau<1/2$. No numerical endpoint approximation is needed.

The positive middle child is exactly the accepted $T_+$; the negative middle child is
exactly the accepted $N$. All other parameters and all 55 clauses match their audited
domains. Their ten-square contradictions are independent of $v,w$, which licenses all
$v\in[0,1]$ on these two children only.
The other six closed children retain unresolved scope.
Their shared endpoints at $1/3$ and $2/5$ may cite the middle theorem; their remaining
points cannot. The seam at $\tau$ receives no inherited exclusion.

Keep the closed union of the other three angle intervals for each sign as a future
remainder, with overlap.
Literal subtraction of the closed middle interval produces a different, nonclosed
remainder. Every side, $z$, slide and angle endpoint, every containment/SAT equality,
$v=t$, the physical coincidence pairs $(0,1),(1,0)$, and possible 9–10 recontact stay in
the definition.

A proper basis lift preserves the physical orientation modulo a quarter turn.
It does not send $\theta$ to $\pi/2-\theta$. A physical reflection would also move
positions and walls.
The prescribed wall inventory has counts bottom 2, right 1, top 3 and left 3; an
inventory-preserving container symmetry must fix the uniquely counted adjacent bottom
and right walls and is the identity.
Additional contacts can give special coincidences but establish no uniform reflection
transfer. In particular the final angle interval cannot be discarded through a
reflected-half-chart assumption.

## Exact Trump Parent Binding and Local Separation

The current source uses the descending polynomial coefficients
$(5,-10,-2,14,12,-6,2,2,-1)$ and isolating interval $u\in(36/100,37/100)$. Its formulas
for $U,r_1,u_1,v_1,v_2,x_0$ match the design literally.
The averaged source corners give

$$
t=v=u,\quad L=U,\quad z=x_0,\quad a=u_1,\quad b=v_1,
$$

$$
p=(1,1)+\tfrac12e+(\tfrac12-r_1)f,\qquad
w=p+(a+2)e-v_2f.
$$

In particular $b$ is $+v_1$ and the $v_2f$ sign is negative.
The source’s local origins $(0,0),(u_1,-1),(1,v_1),(u_1+1,v_1-1),(u_1+2,-v_2)$ reproduce
all five center formulas in their original labels and corner order.

The retained independent source review includes an exact 55-pair feasibility replay and
proves $0<a<1/5$, $1/20<b<1/5$ and $387/100<U<4$. These imply the parent slide and side
bounds; actual source containment gives $2\le x_0\le U-1$ and the remaining center
bounds. The root interval is inside $[1/3,2/5]$. Thus this is a feasible
$\mathcal P_{\rm full}$ control with the actual coincident angle and source 9–10
segment. It fails the target side cap, because $U>387/100>96/25$. It is not a
$\mathcal S_{\rm full}$ witness.
I did not rerun the existing verifier in this admission.

The labeled coordinate $C_{3,y}=L-1/2$ differs from its source value by
$U-L>3/100>808514697/200000000000$. This exceeds the retained local radius in its
fixed-origin, center-and-radian sup norm, independently of $t,v$. Side is not treated as
an extra norm coordinate.
The new target therefore lies outside both the named local interior and its radius
boundary; the local theorem itself excludes none of the new angle children.

## Admission Limits and Receipt

No defining correction is required.
Accept the source-feature chart, label maps, complete weak geometric conditions, closed
eight-child cover and exact scope of the two inherited exclusions.
Refuse a half-chart substitution, fixed-side normalization, source-selected SAT branch,
deleted touching seam, a full-graph rank-nine assertion or promotion of the parent
source to a target witness.
A feasible ten-square skeleton would not refute the eleven-square target.

Even a future whole-domain result would leave other wall patterns, unproved label
transfers, other contact sides, long slides, vanished segments with freed orientations,
and other angular component graphs outside its scope.
No global representative, feasible motion, unrestricted bound, H120 instrument readiness
or H118 comparator separation is admitted here.
A scientific attempt still needs its separately frozen, recorded and validated
prospective protocol.

The phase-17 review lease began at `2026-09-07T12:14:00Z`, with an absolute stop at
`2026-09-07T12:29:00Z`. The actual first clock read was `2026-09-07T12:14:20Z`. This was
a domain and source audit only.
No enlarged target proof, numerical target, solver, script, source edit, dependency,
identifier, shared record or Git change occurred.
Only this assigned review was written.
The complete mathematical readback froze at `2026-09-07T12:23:28Z`, 548 seconds after
the actual first clock.
All seven native source-link targets exist, the required footer appears once, and the
trailing-whitespace scan found no matches.
The common-document and prose passes were applied.
Installed Flowmark 0.4.0 formatted this assigned review with caching disabled; a final
scoped no-cache format check follows this receipt before handoff, within the absolute
cap. No target reasoning follows this admission freeze.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
