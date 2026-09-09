# BC-279: Independent Wall-Core Predicate and Control Admission

**Accept the native protocol’s exact common-core model and the stated control outcomes,
with the deep-interior clarification below.** The accepted predicates use one freely
directed unit normal for each pair, shared by every threshold for that pair.
They describe disjoint interiors of the actual selected squares and the proposed
residual cores exactly.
They are necessary conditions for full residual squares, not an exact description of
their joint angle compatibility.

The initial inspection used the frozen working assessment.
This durable review cites the [native protocol](bc-279-wall-core-protocol.md), the
[adopted allocation](midpoint-allocation.md), the
[original domain](bc-277-boundary-band-domain-design.md), and the
[accepted BC278 controls](bc-278-boundary-band-independent-review.md).
No capacity question is attempted.
Final native-protocol reconciliation is recorded separately below; mathematical
admission of this assessment does not authorize a target.

## Independent Reconstruction of the Body and Its Support

For a residual center $P=(x,y)$, let

$$
r=\min(x,y,q-x,q-y),\qquad
\rho=\min(r,1/\sqrt2),\qquad a=1/(4\rho).
$$

Containment of an actual centered unit square is exactly
$(|\cos\theta|+|\sin\theta|)/2\le r$. Thus $r\ge1/2$ is necessary and every permitted
orientation contains both the closed incircle $B_{1/2}$ and the axis square
$S_a=[-a,a]^2$. Indeed the support of $S_a$ on either actual edge normal is
$a(|\cos\theta|+|\sin\theta|)\le2a\rho=1/2$. Convexity gives
$\operatorname{conv}(B_{1/2}\cup S_a)\subseteq Q_\theta$. Also $a\le r$, so the
translated core is itself contained in the container.

I independently obtain equality with the intersection of all wall-admissible squares.
Choose $\alpha\in[0,\pi/4]$ satisfying $\cos\alpha+\sin\alpha=2\rho$. The permitted
square normals form four closed arcs of half-width $\alpha$ about the coordinate axes.
Write $c=\cos\alpha,s=\sin\alpha$. In the first quadrant, between the bordering normals
$(c,s)$ and $(s,c)$, any normal is their nonnegative linear combination.
Their support lines at distance $1/2$ meet at $(a,a)$, because $a(c+s)=1/2$.
Consequently the inequalities for those two permitted normals imply the hull’s support
inequality throughout that gap.
On a permitted arc, $a(|n_x|+|n_y|)\le1/2$ for a unit normal, so the disk support is the
hull support. Reflection and quarter turns of this centered-body argument cover all
directions. At $\alpha=0$ the intersection is the axis square; at $\alpha=\pi/4$ every
normal is permitted and the intersection is the disk.
No singular decomposition is needed at either endpoint.

Therefore the maximal common core is exactly

$$
K(r)=\operatorname{conv}(B_{1/2}\cup S_a),\qquad
h_{K(r)}(n)=\max\left(\|n\|/2,\ a(|n_x|+|n_y|)\right).
\tag{1}
$$

The maximality is conditional on the center and container alone.
Other squares or joint orientation compatibility may supply stronger premises.
This is a generic identity, not a capacity result on the boundary-band family.

## Pair Predicates, Quantifiers and Complete Inventory

All bodies in (1) contain an open disk.
For two compact convex bodies with disjoint interiors, weak separation supplies a
nonzero normal; normalize it to unit length.
Central symmetry makes the separating inequality for centers $P_j,P_k$

$$
n\cdot(P_j-P_k)\ge h_{K_j}(n)+h_{K_k}(n).
$$

Conversely that inequality separates the interiors.
Equality therefore permits legal touching, including disk tangencies and shared
axis-square boundary segments.
It must not be replaced by a strict inequality.

For $L_n=|n_x|+|n_y|$ and the **same** unit normal, the sum of the two maxima in (1) is
the maximum of the four numbers

$$
1,\qquad 1/2+a_jL_n,\qquad 1/2+a_kL_n,\qquad(a_j+a_k)L_n.
\tag{2}
$$

Requiring the projection to exceed or equal every number in (2) is therefore exact.
For a selected actual square with support $H_i(n)=(|n\cdot e_i|+|n\cdot f_i|)/2$, the
exact cross predicate has the two thresholds

$$
H_i(n)+1/2,\qquad H_i(n)+a_jL_n,
\tag{3}
$$

again on one shared normal.
Each pair may have a different normal from every other pair.
Within one pair, different normals for the different thresholds would change
$\exists n\,\bigwedge$ into $\bigwedge\exists n$ and would not establish separation of
the convex hulls. That altered certificate must be refused as this exact model.

The inventory is complete: seven residual centers give 21 residual pairs and four
selected squares give 28 cross pairs.
Equations (2)–(3) require 49 pair normals, 98 normal coordinates, 49 equalities
$n_x^2+n_y^2=1$, and $21\cdot4+28\cdot2=140$ support inequalities.
The original six selected pairs keep all eight actual-square SAT alternatives.
Thus no pair is omitted from the original six-plus-28-plus-21 partition.

The quantifiers are finite in number, but each normal ranges over the entire real unit
circle. They are not a finite catalogue of normal directions.
Restricting the residual or cross normals to coordinate axes or selected-square edge
axes changes the model.
For a generic control, take two deep-interior disk cores in a container of side four,
centered at $(1,1)$ and $(9/5,8/5)$. Their displacement $(4/5,3/5)$ is unit length, so
the cores touch legally with that unit normal.
Neither coordinate-axis projection reaches one.
This is a predicate control, not a four-pose or capacity witness.

Every contained full-square extension supplies these core predicates by inclusion.
Every accepted core configuration also supplies the original disk predicates.
The admitted implication is therefore

$$
\kappa_\square(G)\le\kappa_{\rm wall}(G)\le
\kappa_{\rm disk}(G)\le\kappa_{\rm oct}(G).
$$

No reverse implication or capacity value is accepted here.

## Exact Graphs and Boundary Cases

The proposed minimum graph is exact: $r\ge1/2$, four inequalities $r\le x,y,q-x,q-y$,
and the disjunction equating $r$ to at least one of those four quantities.
Their conjunction forces the actual minimum.
Every wall tie remains in all applicable branches.
One-sided bounds alone would permit a false clearance and a false core.

With $a\ge0$, the two closed branches

$$
(r^2\le1/2\ \wedge\ 4ar=1)
\quad\lor\quad
(r^2\ge1/2\ \wedge\ 8a^2=1)
$$

give exactly (1). Positivity of $r$ excludes negative-clearance artifacts, and
nonnegativity of $a$ selects the positive saturated root.
At $r^2=1/2$ both branches agree.
At $r=1/2$ they give $a=1/2$ and the full axis square.
No seam may be removed by a strict branch selector.

The graph $v\ge0,v^2=z^2$ is exactly $v=|z|$. The two positive-part branches with $w=0$
when $v\le a$ and $w=v-a$ when $v\ge a$ are likewise exact and agree at the seam.
Absolute values in both selected support and (2)–(3) must use these exact values.
Free upper slacks, inflated positive parts, a free $a$, or a midpoint-only clearance do
not implement the admitted model.

The selected angles remain independent.
The unit-circle chart $c_i^2+s_i^2=1$, $c_i\ge0$, $-c_i\le s_i\le c_i$ preserves the two
$45$-degree lifts. The selected supports, minimum core value and row scatter retain the
original exact min/max/absolute-value definitions; their ties are included.
These closed, bounded graphs and finite unit-normal quantifiers give a semialgebraic
model. They do not make it an LP or a rational-only certificate format.

For $r\ge1/\sqrt2$, $a=1/(2\sqrt2)$ and $aL_n\le1/2$ on every unit normal.
Thus $K(r)$ **equals** the disk.
The extra box thresholds become redundant; all residual disk separations and all 28
selected-square/disk cross conditions remain required.
Any claim of redundancy in this regime must mean the extra box thresholds only.
Omitting those cross pairs would be a substantive error.

## Exact Positive and Negative Controls

The two axis squares centered at $(1/2,1/2)$ and $(3/2,1/2)$ in a container of side at
least two have $r=1/2,a=1/2$. With displacement normal $(1,0)$, all four thresholds in
(2) are one and the projection is one.
The weak predicate accepts this legal touch.

At $r=3/5$, $a=5/12$, put

$$
c=(6+\sqrt{14})/10,\qquad s=(6-\sqrt{14})/10.
$$

Then $c^2+s^2=(72+28)/100=1$, $c+s=6/5$, and the actual wall support is exactly $3/5$.
The vertex $(a,a)$ satisfies $c a+s a=1/2$. Any larger halfside crosses that permitted
square edge, so it must be refused.
This is saturation of the actual containment inequality, distinct from the core’s
$r=1/\sqrt2$ saturation branch.

For the accepted BC278 author control, the
[original table](bc-278-boundary-band-author.md#seven-exact-disk-centers) gives
$P_2=(279/100,167/50)$ and $P_4=(167/50,5/2)$. Both have nearest-wall distance $1/2$, so
both new cores are full axis squares.
Their absolute displacement is $(11/20,21/25)$. For every unit normal,

$$
n\cdot(P_4-P_2)\le(11/20)|n_x|+(21/25)|n_y|
<|n_x|+|n_y|=h_{K_2}(n)+h_{K_4}(n).
$$

The strict inequality holds because a unit normal has a nonzero coordinate.
Hence no oblique normal can rescue this pair.
The wall-core model rejects this exact seven-disk configuration, although the audited
disk squared distance is $10081/10000>1$. This proves a strict configuration-set
refinement only.
It does not prove a smaller capacity or reject every seven-center choice
at that selected four-pose configuration.

For the accepted BC278 octagon control, the audited offending pair has selected-square
coordinates

$$
\alpha=59/120-9\sqrt3/100,\qquad
\beta=9/100+59\sqrt3/120,
$$

with $0<\alpha<1/2$ and $1/2<\beta<1$. Its point-to-square distance is $\beta-1/2<1/2$,
so the residual incircle overlaps the selected square interior.
Since that disk lies in every wall core, (3) refuses the same pair.
Passing the 28 weaker guard-octagon avoidance tests cannot bypass the actual
selected-square cross predicate.
This refusal concerns those fixed centers, not all configurations at that four-pose
fixture.

Joint reflection $(x,y)\mapsto(x,q-y)$ preserves the clearance minimum, $a$, the disk
and axis box. Reflecting each pair normal with its displacement preserves all support
inequalities, and negating selected angles preserves their actual supports.
The upper branch therefore has the same controls.
Angle lifts, wall ties, saturation equality, band and weak-order seams, every label
subset and every original failure sibling remain covered.
Reflection transfers closed branches, not the counting convention that assigns a band
seam to its lower index.

## Protocol Reconciliation and Disposition

The [native protocol](bc-279-wall-core-protocol.md) appeared during this review and was
read in full. Its equations (1)–(10) match the admitted model.
In particular, its $m_i=1/(2c_i)$ agrees with the original maximum-coordinate formula
because the complete selected chart forces $c_i\ge|s_i|$ and $c_i>0$. It retains the
original eight guards: two row conditions, one bottom attachment, two endpoint
conditions and three consecutive gap conditions.
The lower-band endpoints, actual selected containment, six complete selected SAT
clauses, exact row scatter, label subsets and weak orders are unchanged.
Its exact seven-core witness contract requires all 49 normals or exact constructions of
them, graph values, and every support inequality; an approximate drawing cannot satisfy
that contract.

One correction was requested before native freeze and independently read back at
11:23:08 UTC. The earlier reflection sentence applied “the linear part” of
$(X,Y)\mapsto(X,q-Y)$ to both centers and normals.
The corrected paragraph explicitly applies the affine map to selected and residual
centers and its linear part to displacements, normals and basis vectors.
The basis sign is absorbed into square corner signs.
This closes the wording defect and preserves $r$, supports and upper-band membership.
The correction changes no predicate in (1)–(10) and no target domain.

The final native protocol records its freeze at 11:23:05 UTC. I reread that frozen file
in full, completing reconciliation at 11:24:48 UTC. The reflection correction, retained
deep-interior disk conditions and explicit distinction between residual common cores and
old guard octagons are all present.
The final frozen native model is admitted; no predicate or control correction remains
open in this review.

No target begins by implication or by expiration of the lease.

Accept the exact body, support, finite real normal quantifiers, graph semantics and
control outcomes above.
Refuse certificates that omit pairs, choose independent normals within one pair,
discretize normal directions without a separate sound completeness argument, lose
equality cases, or use favorable free graph variables.
The first target obligation would be a separately authorized whole-domain determination;
it is not part of admission.
A seven-core witness would refute only this surrogate’s uniform bound, and an exclusion
would transfer to full squares only on the unchanged admitted parent.
Neither would establish H118 separation without its matching coupled-LP comparison.

## Work Receipt

The prospective phase-15 lease began at `2026-09-07T11:12:25Z`; this review’s absolute
cap is `2026-09-07T11:27:25Z`. The actual first clock read was `2026-09-07T11:15:44Z`.
The body and predicate identities and the listed controls were reconstructed by hand.
No capacity target, numerical run, solver, target script, implementation, shared record,
identifier, dependency or Git change was undertaken.
Only this assigned report was written.
The mathematical review and final frozen-protocol reconciliation ended at
`2026-09-07T11:24:48Z`, 544 seconds after the actual first clock read.
The common-document and prose passes were applied.
Full report readback, native source-link existence, the single required footer and a
trailing-whitespace scan passed.
Installed Flowmark 0.4.0 formatted this file with caching disabled; the final scoped
format check follows this receipt before handoff and before the absolute cap.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
