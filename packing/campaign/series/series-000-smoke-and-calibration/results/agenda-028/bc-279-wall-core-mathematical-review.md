# BC-279: Independent Mathematical Admission of the Wall Core

**The generic maximal-core identity is accepted.** For a residual center $C$ whose
distance from the nearest container wall is $r\ge1/2$, the intersection of all centered
unit-square orientations compatible with those walls is exactly

$$
K(r)=\operatorname{conv}\left(B_{1/2}\cup[-a,a]^2\right),
\qquad a=\frac1{4\min(r,1/\sqrt2)}.
$$

All parent statements use $q=96/25$, $b=1/2$, $d=167/50$ and the unchanged four-pose
domain $\Gamma_0$. This review independently reconstructs both inclusions of the
proposed identity and accepts their use in the frozen
[native protocol](bc-279-wall-core-protocol.md).
The endpoint bodies, exact graph constraints, pair predicates and reflection contract
are sound. No capacity bound or seven-core witness is established by this admission.
The full-square $D_0$ determination and the separate strict H118 comparison remain
unresolved.

## The Exact Wall Information

For $C=(x,y)$ in the fixed square container, write

$$
r(C)=\min(x,y,q-x,q-y),\qquad
h(\theta)=\frac{|\cos\theta|+|\sin\theta|}{2}.
$$

A centered unit square has this same coordinate support in both coordinate directions.
Its containment is therefore exactly $h(\theta)\le r(C)$, with weak inequality.
The orientations compatible with one residual center are not identified with those
compatible with any other residual center.

For $r\ge1/2$ the allowed set is nonempty, since an axis square is admissible.
Put $t=\min(r,1/\sqrt2)$ and $a=1/(4t)$. The radius-$1/2$ disk lies in every unit
square. For any admissible square normal $e=(\cos\theta,\sin\theta)$, the support of
$[-a,a]^2$ is

$$
a(|\cos\theta|+|\sin\theta|)=2ah(\theta)\le2at=1/2.
$$

The perpendicular normal gives the same bound.
Thus both the disk and the axis square lie in every admissible square.
Convexity proves the first inclusion

$$
\operatorname{conv}(B_{1/2}\cup[-a,a]^2)
\subseteq\bigcap_{h(\theta)\le r}Q_\theta.
$$

Also $a\le r$: below saturation this is $1\le4r^2$, and above saturation
$a=1/(2\sqrt2)\le r$. Both component cores, and therefore their convex hull, remain
contained after translation by $C$. This also follows directly from inclusion in any
admissible actual square.

The axis half-side is itself maximal.
When $1/2\le r\le1/\sqrt2$, choose an orientation with $h(\theta)=r$. Its normal
projects the signed core vertex by $2ar$, so any larger axis half-side would violate the
square’s support bound.
At and above saturation, the admissible diagonal square requires $a\le1/(2\sqrt2)$. This
preliminary fact concerns axis cores; the next argument establishes maximality among all
common bodies.

## Independent Reverse Inclusion

For $1/2<t<1/\sqrt2$, choose the unique $\alpha\in(0,\pi/4)$ with
$\cos\alpha+\sin\alpha=2t$, and put $c=\cos\alpha$, $s=\sin\alpha$. The actual
wall-compatible orientations are $[-\alpha,\alpha]$ modulo quarter turns.
Their signed edge normals consequently form four closed arcs centered on the coordinate
directions.

Call the proposed hull $H$. For any normal $n$, its exact support is

$$
h_H(n)=\max\left(\|n\|/2,\ a(|n_x|+|n_y|)\right).
$$

For a unit normal in an allowed arc, $|n_x|+|n_y|\le c+s=2t$, so $h_H(n)=1/2$. Every
point of the intersection already satisfies the corresponding square support inequality.

It remains to check directions missing from those arcs.
By reflection and quarter-turn symmetry, consider a unit first-quadrant normal between
$n_1=(c,s)$ and $n_2=(s,c)$. Because $c>s>0$, these boundary normals are linearly
independent. The direction lies in their positive cone, so

$$
n=\lambda n_1+\mu n_2,\qquad \lambda,\mu\ge0.
$$

For example, $\lambda=(cn_x-sn_y)/(c^2-s^2)$ and $\mu=(cn_y-sn_x)/(c^2-s^2)$ are
nonnegative on this angular interval.
The two boundary inequalities for a point $z$ in the intersection imply

$$
n\cdot z\le\frac{\lambda+\mu}{2}
=\frac{n_x+n_y}{2(c+s)}=a(n_x+n_y).
$$

Here $n_x+n_y\ge c+s$, so the last expression is precisely $h_H(n)$, including the gap
endpoints. All directions therefore obey the hull’s support inequalities.
The support-halfspace characterization of a closed convex body gives the reverse
inclusion.
Equivalently, each missing-normal support bound follows from the two available
bordering square normals; no sampled normal stands in for the arc.

At $r=1/2$, the only physical allowed orientation is axis alignment.
The intersection is the axis unit square, $a=1/2$, and the hull is that same square.
At $r=1/\sqrt2$, all orientations are admitted and the intersection is the disk.
The axis-core vertices have norm $\sqrt2a=1/2$, so the hull is also the disk.
The same body persists for every larger $r$. These endpoint arguments avoid division by
the vanishing $c^2-s^2$ at saturation.
Both endpoints and every legal wall contact are included.

Thus the identity holds throughout the complete feasible center box.
It is a statement about all actual orientations compatible with the center, not a
midpoint core, a folded-angle average or an assertion about the orientation chosen by a
particular extension.

## Pair Predicates and Exact Counts

For a unit normal let $L_n=|n_x|+|n_y|$. Each residual core has support

$$
h_{K_j}(n)=\max(1/2,a_jL_n).
$$

The cores contain the disk and hence have nonempty interiors.
For compact convex bodies with nonempty interiors, disjoint interiors are equivalent to
a weak separating hyperplane.
Central symmetry converts the two directional supports into the support sum used in the
assessment. This verifies both directions of the existential pair predicates, including
tangency.

For a residual pair, the sum of two maxima is the maximum of their four pairwise sums.
Its one common unit normal must therefore satisfy all four inequalities

$$
n\cdot(P_k-P_j)\ge
1,\quad 1/2+a_jL_n,\quad 1/2+a_kL_n,\quad(a_j+a_k)L_n.
$$

For a selected actual square and residual core, the one common normal must satisfy both
$n\cdot(P_j-C_i)\ge H_i(n)+1/2$ and $n\cdot(P_j-C_i)\ge H_i(n)+a_jL_n$.

There are exactly 21 residual pairs and 28 selected-to-residual pairs.
Their normals are independent between pairs, but shared within each pair’s conjunction.
This gives 49 unit normals, 98 normal coordinates, 49 unit-circle equations and
$21\cdot4+28\cdot2=140$ support inequalities.
Each normal ranges over the whole unit circle.
The six selected-square pairs retain their original complete eight-way weak SAT
disjunctions.

Different normals for different component inequalities of one pair would not establish
separation of the convex hulls.
Restricting a pair’s normal to finitely many source, selected-square or coordinate
directions would not define this curved-body model.
Neither change is admitted as an exact implementation of the stated predicates.

## Closed Graphs and All Boundary Cases

The graph for $r$ is exact: require $r\ge1/2$, bound it above by all four wall
distances, and require equality to at least one.
A wall tie belongs to every matching closed branch.
A merely smaller free value of $r$ can enlarge the core and invalidate necessity, so the
equality disjunction is essential.

With $a\ge0$, the two saturation branches

$$
(r^2\le1/2\ \wedge\ 4ar=1)
\quad\lor\quad
(r^2\ge1/2\ \wedge\ 8a^2=1)
$$

select the unique positive intended half-side.
They agree when $r^2=1/2$; both branches retain the seam.
There is no negative-root alternative and no free slack that may inflate $a$.

The proposed absolute-value graph $v\ge0,v^2=z^2$ fixes $v=|z|$. The two closed
positive-part branches likewise fix $(v-a)_+$ and agree at $v=a$. Such graph variables
cannot be replaced by arbitrary upper bounds in lower-distance tests.
The selected basis graph $c_i^2+s_i^2=1$, $c_i\ge0$, $-c_i\le s_i\le c_i$ covers the
full original selected chart and both diagonal endpoint lifts.
The existing selected support, minimum and scatter expressions retain their exact graphs
and all eight guards.

These observations give a bounded closed semialgebraic model with rational polynomial
predicates at rational $q$. They do not give an executable certificate reader or a
finite list of sufficient separating directions.
An instrument would need its own controls and review before use; this admission is
mathematical.

## Necessity, Maximality and What a Negative Could Settle

For each actual residual square, independently of the other residual orientations,
$K(r_j)$ lies in that square.
An actual extension therefore maps into the core model, preserving all 28 cross and 21
mutual nonoverlap conditions.
Since each core contains its disk, a core configuration maps into the accepted disk
relaxation. The established disk-to-octagon implication is unchanged.
Consequently

$$
\kappa_\square(G)\le\kappa_{\rm wall}(G)
\le\kappa_{\rm disk}(G)\le\kappa_{\rm oct}(G).
$$

The core depends only on the individual center and its wall-compatible orientations.
Any body valid inside every one of those actual squares is a subset of their
intersection, regardless of whether the proposed smaller body is an axis square,
polygon, union or asymmetric set.
Any convex hull of sound smaller cores also lies in this same maximal convex body.

A seven-maximal-core witness would therefore also satisfy the true nonoverlap conditions
for every smaller-body model obtained solely by those substitutions.
It would refute the uniform bound of six for this entire specified class.
It would not settle models that restrict allowed angles using the selected obstacles,
common orientation choices, other residual squares or joint geometric information.
It would not yield seven actual residual squares.

A uniform wall-core bound of six over the whole unchanged $\Gamma_0$ would suffice to
exclude the full-square child.
A model witness would refute only that sufficient model bound.
No strict inequality between the numerical capacities follows merely because one known
disk configuration is rejected by the wall-core model.
A matching coupled-LP survival witness and nonlinear-guard representation remain
separately necessary for any strict H118 comparison.

## Generic and Retained Controls

The touching-axis control is accepted: at centers $(1/2,1/2)$ and $(3/2,1/2)$ in a
container of side at least two, both $r$ values are $1/2$. The cores are unit axis
squares. Normal $(1,0)$ gives $L_n=1$ and equality in every component inequality.
The contact is legal.

At saturation each core equals its disk.
The axis support obeys $aL_n\le1/2$ on every unit normal, so the additional component
inequalities become redundant in residual pairs when both centers are saturated, and in
the corresponding selected-square/core condition.

For the sharpness control $r=3/5$, the proposed $c=(6+\sqrt{14})/10$ and
$s=(6-\sqrt{14})/10$ satisfy $c^2+s^2=1$ and $c+s=6/5$. Thus $h=3/5$ and $a=5/12$ gives
$a(c+s)=1/2$. Increasing the half-side violates this admissible square’s edge
inequality. This checks a genuine wall-compatible endpoint orientation.

The accepted BC278 author centers $P_2,P_4$ each have $r=1/2$, so their cores are axis
unit squares. For their displacement $d$ and any unit normal,

$$
n\cdot d\le(21/25)(|n_x|+|n_y|)<|n_x|+|n_y|,
$$

using $|d_x|=11/20$ and $|d_y|=21/25$. The required axis-core support sum is $L_n$.
Every possible normal therefore fails; the known disk configuration is correctly
rejected even though the model permits the full unit circle.
This is a retained control, not a new seven-core determination.

The accepted adversary configuration still fails the necessary disk-to-selected-square
condition. Enlarging that disk to its wall core cannot repair the strict overlap.
The original four-diamond fixture remains selected-pose membership evidence only.
None of these controls establishes a capacity at that fixture or elsewhere.

## Joint Reflection and Parent Scope

Under $(X,Y)\mapsto(X,q-Y)$, the four wall distances are permuted, so each exact $r$ and
$a$ is unchanged. Both disk and axis square, and hence their convex hull, are invariant
under the linear reflection.
Reflect all selected poses and every residual center, negate the selected angles, and
send every pair normal to $(n_x,-n_y)$. Unit length, $L_n$, actual selected supports and
all displacement products are preserved.

Wall-minimum ties remain closed, saturation branches are unchanged, and selected angle
endpoint lifts exchange.
The existing lower-to-upper guard mapping is evaluated in inward depth.
As before, reflection transfers closed branches, not the auxiliary lower-index band
counting rule. No reflected seam is removed because its counting owner differs.
All label subsets, weak horizontal orders, eight failure siblings and the accepted
central remainder remain in the parent cover.

The model ranges over the entire unchanged four-pose $\Gamma_0$ and all seven
independent residual centers.
It imposes no source wall contact, fitted center box or desired capacity.
No full-square child is pruned by admission alone.

## Native Protocol Reconciliation

The native author announced freeze at 11:23:05 UTC. I then read the complete
[final protocol](bc-279-wall-core-protocol.md); the first completed read was recorded at
11:24:18 UTC. The identity, exact center/core graph, 49 shared-within-pair normals, 140
inequalities, all seven independent residual centers and the full unchanged $\Gamma_0$
match this independent reconstruction.
No mathematical discrepancy remains.

Its simplified selected radius $m_i=1/(2c_i)$ is exactly the original twice-maximum
reciprocal because its selected chart enforces $c_i\ge|s_i|$ and $c_i>0$. Its residual
normal in (6) is directed from $P_j$ to $P_k$; the opposite naming in the initial
assessment describes the same predicate because the complete unit circle includes both
signs. The native text correctly retains all disk cross conditions at saturation and
distinguishes the affine center reflection from its linear action on displacements and
normals.

The accepted mathematical target is precisely emptiness of its seven-core set
$\mathcal M_7$, equivalently a uniform wall-core capacity of six over the unchanged
selected family. The positive and negative acceptance rules preserve the distinction
between the model and full squares.
A negative requires exact selected poses, all seven centers, their determined graph
values and all 49 unit-normal certificates or exact constructions generating them.
Partial coverage, a looser-core witness, a failed construction or timeout does not
determine this model.

The future price matches the coordinator’s scope: a 30-minute author and concurrent
25-minute adversary, followed by a fresh 20-minute audit after both freeze.
This is 75 worker-minutes and a 50-minute mathematical critical path, excluding
admission and integration.
All target and audit work ends by 12:40 UTC; full windows require dispatch by 11:50 UTC,
and later dispatch must prospectively shorten them.
This mathematical admission launches nothing.
The other required admission, committed native protocol, passing record checks and
recorded actual leases must precede target dispatch.

## Work Receipt

The prospective phase-15 window began at 11:12:25 UTC on 2026-09-07. This review’s
unchanged hard endpoint is 11:32:25 UTC. The actual first clock read was 11:15:28 UTC.
The independent reconstruction first used the terminal generic assessment at
`attic/agenda-028-overnight/midpoint-wall-model-assessment.md` as working provenance,
then reconciled every admitted implication against the frozen native protocol.
The native protocol is the self-contained acceptance source; the attic draft is not a
publication dependency.
The unchanged accepted domain and model distinctions were retained.
I coauthored neither the identity nor a target argument.
No new capacity proof, seven-center construction, numerical target, solver, identifier
allocation, dependency change, Git mutation or shared-record edit occurred.
Only this assigned native review was written.

The complete reconstruction and native reconciliation, followed by the readback and
document checks, finished at 11:27:02 UTC, 11 minutes 34 seconds after the first clock
read. The common-document and prose passes were applied.
Installed Flowmark 0.4.0 formatted this file and passed its scoped no-cache check; the
native source link exists, the whitespace scan found no trailing blanks, and the
required footer appears once.
A final scoped formatting check follows this receipt.
All work is scheduled to end before the unchanged 11:32:25 UTC hard endpoint; no target
capacity work follows this admission.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
