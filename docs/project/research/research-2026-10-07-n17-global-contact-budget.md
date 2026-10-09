---
title: n17 Global Wall and Contact Budget
date: 2026-10-07
status: hand-derived
---
# n17 Global Wall and Contact Budget

Every packing of unit squares in a square of side at most $U=1169/250$ has at most four
squares touching any one container wall.
There are therefore at most sixteen active wall constraints.
If a strictly smaller packing than the accepted candidate exists, the fixed-orientation
normalization below supplies another such packing with at least nineteen distinct
contacting square pairs.

The wall bound applies to every packing in this container range.
The nineteen-contact conclusion is an existence statement about a normalized
representative, not every placement of seventeen squares.
It strengthens the earlier
[fourteen-contact corollary](research-2026-10-07-n17-full-square-partner-coupling.md)
without changing the global side bound or excluding an existing cell assignment.

This is a sole-Astra hand derivation and self-audit.
It has not received independent mathematical review or formal verification.
No packing geometry, solver or target experiment was evaluated to obtain it.
The finite arithmetic checker proposed below would verify only its explicitly identified
algebraic premises.

## Four Squares per Wall

Consider any packing of closed unit squares with disjoint interiors in $[0,L]^2$, where
$L\le U$. Each unit square contains an open disk of radius $1/2$ centred at its centre.
Distinct square centres are therefore at least one unit apart.

A square touching the left wall has centre coordinate

$$
x=\frac{|\cos\theta|+|\sin\theta|}{2}
\in[1/2,\sqrt2/2]\subset[1/2,3/4).
$$

The same support formula bounds its distance from any other wall it touches.
For two left-wall squares, $|\Delta x|<1/4$. Their centre separation gives

$$
|\Delta y|^2\ge1-|\Delta x|^2>15/16>(15/16)^2,
$$

so $|\Delta y|>15/16$. Every square centre lies between $1/2$ and $L-1/2$ in the
tangential coordinate, because its support in that direction is at least $1/2$. Five
left-wall squares, sorted by their tangential centre coordinate, would thus span more
than

$$
4\cdot\frac{15}{16}=\frac{15}{4},
$$

whereas the available span is at most

$$
L-1\le\frac{919}{250}<\frac{15}{4}.
$$

This is a contradiction.
The argument applies separately to all four walls.
Count one wall constraint for each square/wall incidence; a square touching two walls
contributes once to each.
The total number of active containment rows is at most $4\cdot4=16$.

This proof allows arbitrary orientations and contacts at corners.
It uses no nondegeneracy, contact-graph assumption, cell assignment or local guard.

## A Normalized Representative with Nineteen Contacts

Let $S^\ast$ be the accepted candidate side and suppose a physical packing exists with
side $L_0<S^\ast$. The accepted cap relation gives $S^\ast<V<U$; the normalization
actually needs only $L_0<U$. Freeze the seventeen orientations of that packing.
The variable vector consists of 34 centre coordinates and the container side $L$.

For each unordered pair, nonoverlap is a disjunction of finitely many signed
separating-axis inequalities.
With the orientations fixed, each row is linear in the centres.
The available normals are the two body axes of either square, with both signs.
The square supports on those fixed normals are constants.
Selecting one valid row for each of the 136 unordered pairs, together with the 68
containment rows, gives a closed polyhedron.
The union of these finitely many choices is exactly the fixed-orientation packing set.

For completeness, the separating-axis statement follows from the difference polygon of
the two centred squares.
Its edge normals come from the two squares’ edge normals.
Disjoint interiors mean the relative centre is outside that polygon’s interior, so one
facet inequality is weakly separating.
If the closed squares are disjoint, the relative centre lies outside the closed
difference polygon and a facet inequality is strictly separating.
If the squares touch, any valid separating row has equality at the touching placement.

Restrict the side to the artificial interval $0\le L\le U$. Containment makes all
centres bounded, so the finite union is compact and nonempty.
Minimize $L$ over the entire union.
On the complete minimizing set, minimize the 34 centre coordinates lexicographically in
a fixed order. Nested compact minimizer sets give one unique final vector $p$.

Only after this global lexicographic choice, select a SAT branch containing $p$ as
follows. For every pair whose closed squares are disjoint, select an ordinary weak SAT
row that has positive slack at $p$. The row remains a closed weak inequality throughout
the branch; no strict constraint is introduced.
For every touching pair, select a valid touching row.
Use exactly one row per unordered pair.

The vector $p$ is a vertex of this selected branch polyhedron.
Otherwise it lies strictly between two distinct points of that polyhedron.
Both endpoints are physical fixed-orientation packings.
Their side coordinates cannot be smaller than the global minimum and average to that
minimum, so both sides equal it.
At the first centre coordinate where the endpoints differ, one is smaller than $p$,
contradicting the global lexicographic choice.
This argument uses the entire SAT union before branch selection; it does not assume a
particular branch’s minimizer is globally normalized.

The two artificial side bounds are inactive.
Area gives $L^2\ge17$, so $L>0$; minimality gives $L\le L_0<U$. In particular, the lower
bound is zero, not the standing numerical lower bound, which could be active in an
unrelated LP. At a vertex in 35 variables, the active row normals span rank 35. Those
active rows are therefore physical containment rows or chosen pair rows.

There are at most sixteen active containment rows by the wall lemma.
At least $35-16=19$ chosen pair rows must be active.
They represent nineteen distinct unordered pairs because the branch contains one row per
pair. Every active chosen pair is a physical contact: a closed-disjoint pair was
deliberately assigned a strictly separating row and hence cannot be active.

Thus any strict counterexample has a fixed-orientation normalized strict counterexample
with at least nineteen distinct contacting pairs.
More precisely, if that representative has $W$ active wall rows, it has at least $35-W$
active chosen pair rows, where $W\le16$.

The graph of these active chosen pairs has seventeen vertices, at least nineteen edges
and, say, $k\ge1$ connected components, including isolated vertices.
Its cycle-space dimension is $|E|-17+k\ge k+2\ge3$. Thus this normalized representative
has at least three independent contact cycles.
This is a graph-theoretic corollary of the existence argument, not a cycle requirement
on every arbitrary packing or every graph of possible contacts.

Normalization must precede the closed-cell assignment and any local guard.
It can move centres across cell boundaries and alter which endpoint-family parameters
describe them. It is not an operation licensed inside one existing census state or one
accepted regional proof.
A future normalized-representative cover must retain this order of quantifiers.

### Variable Side in the Fixed Outer Frame

The physical contacts above are with the walls of side $L$, not the outer walls of side
$U$ or the accepted numeric cap $V$. A future consumer can retain the original outer
frame by embedding each normalized centre as

$$
\widetilde c_i=c_i+\frac{U-L}{2}(1,1).
$$

If $h_i$ is that square’s support in either coordinate direction, the left and bottom
containment rows become

$$
\widetilde c_{i,a}-h_i\ge\frac{U-L}{2},
$$

and the right and top rows become

$$
U-\widetilde c_{i,a}-h_i\ge\frac{U-L}{2},\qquad a\in\{x,y\}.
$$

This is an invertible affine change in the 35 variables, so it preserves active rank,
pair differences and the wall-incidence bound.
It does not replace the physical walls by $U$-wall equalities.
A contact-pattern consumer must retain $L$ or a proved side interval and these
moving-wall rows; testing only contact with the fixed $U$ or $V$ walls could omit the
required normalized representative.

## Optional Contact-Degree Bounds

The following bounds also apply without fixed orientations or a local guard.
They are additional hand lemmas, not inputs needed for the nineteen-contact result.

### Interior Squares: At Most Eight Neighbours

Let two neighbours touch a given square, and let their centre distances from its centre
be $r,s$. Nonoverlap gives $r,s\ge1$. A contact point is within $\sqrt2/2$ of each
square centre, so $r,s\le\sqrt2$. The two neighbour centres are also at distance at
least one. For their smaller angular separation $\gamma$, the cosine rule yields

$$
\cos\gamma\le\frac{r^2+s^2-1}{2rs}\le\frac34.
$$

The second inequality follows by maximizing $r^2+s^2-1-(3/2)rs$ separately in each
variable on $[1,\sqrt2]$. It is convex in each variable, so a maximum occurs at a
corner. The corner values are $-1/2$, $0$, and $2-(3/2)\sqrt2<0$.

Write $\beta=\arccos(3/4)$. Then $\beta>2\pi/9$: if $x=\cos(2\pi/9)>1/2$, the
triple-angle identity gives $4x^3-3x+1/2=0$, while this strictly increasing polynomial
on $(1/2,1]$ has value $-1/16$ at $3/4$. Each consecutive angular gap between neighbours
is at least $\beta$, so nine neighbours would require more than $2\pi$. There are at
most eight.

### Wall Squares: At Most Five; Corner Squares: At Most Three

Set $a=(\sqrt2-1)/2$ and $\alpha=\arcsin a$. For a square touching a container wall, its
centre is at most $\sqrt2/2$ from the wall, while every neighbour centre is at least
$1/2$ from it. Every neighbour direction is consequently confined to an arc of length at
most $\pi+2\alpha$. Six neighbours would require five consecutive gaps of at least
$\beta$.

The strict inequality $\pi+2\alpha<5\beta$ can be checked exactly.
Since $\cos(\beta/2)=\sqrt{7/8}$, the five-angle identity gives

$$
\cos(5\beta/2)=-\sqrt{14}/16,
\qquad
\sin((5\beta-\pi)/2)=\sqrt{14}/16>a.
$$

Here $(5\beta-\pi)/2$ lies in $(0,\pi/2)$, and the last comparison is equivalent to
$89^2<2\cdot64^2$. Thus at most five neighbours are possible.

For a square touching two adjacent walls, the permitted direction arc has length at most
$\pi/2+2\alpha$. We have $a<1/4<\sin(\pi/12)$, hence $\alpha<\pi/12$. The second
inequality follows from $\sin(\pi/12)=(\sqrt6-\sqrt2)/4>1/4$. Therefore the arc length
is less than $2\pi/3$, whereas three neighbour gaps exceed $3\beta>2\pi/3$. At most
three neighbours are possible.

In the seventeen-square regime, a square cannot touch two opposite walls: its width is
at most $\sqrt2$, but area forces $L\ge\sqrt{17}$. Thus every square touching two walls
falls under the adjacent-wall case.
If $b_1,b_2$ count squares touching exactly one or two walls, the entire physical
contact graph satisfies

$$
2|E|\le8(17-b_1-b_2)+5b_1+3b_2
=136-3b_1-5b_2.
$$

This is an upper bound on actual contact degrees and edges.
A graph of merely possible contacts may have larger degrees; deleting that graph because
it exceeds these numbers would be unsound.
The bounds constrain a selected realizable contact pattern.

## A Small Exact Premise Checker

A prospective retained checker can establish the rational wall-budget packet without
reading packing data or solving an LP. Freeze $U=1169/250$, the strip bound $a=1/4$, the
tangential separation threshold $d=15/16$, wall capacity four and $n=17$. Check exactly

$$
2<(3/2)^2,\qquad 1-a^2>d^2,\qquad U-1<4d,
\qquad 2n+1-4\cdot4=19.
$$

Record which hand implications use them: support range, centre separation, sorted
wall-centre capacity, and the rank-count subtraction.
Require the exact frozen constants rather than accepting an arbitrary altered region
under the same schema.
Synthetic controls should refuse wrong inequalities, a claimed capacity of three,
changed constants and altered fresh payloads.
An optional star packet can verify the listed rational/radical comparisons and
polynomial identities separately.

The checker must not claim to verify the area argument, compactness, finite SAT union,
global lexicographic vertex argument or rank-35 existence theorem merely because the
scalar inequalities pass.
Those remain explicit hand-proof dependencies pending independent review or
formalization.
There is no sampled-matrix rank substitute for the existence argument, and
no packing-specific contact realization is asserted.

## Strategic Use and Stop Rule

The concrete global progress is the stronger necessary contact budget.
It does not eliminate any of the 4,683 current residual orbits or reduce the side
bracket. The local 22-row and 25-row regional implications remain the source-ready
computational lead; they are conditional restrictions whose global cover is still
missing.

Reserve one bounded 30–60 minute proof-interface effort for independent review of this
wall/rank composition and, if selected, the small arithmetic consumer.
A later contact search must first supply a complete normalized-representative cover,
exact orientation and wall/contact feasibility conditions, and nonzero-minor obligations
before using a chosen basis.
Nineteen contacts do not identify their graph or solve the orientations.
Possible-edge counting alone can be too weak to prune any residue.

Do not fund an unrestricted contact atlas because the contact count improved.
A separately registered finite necessary-condition test must declare its complete roster
and a strict pruning criterion; if every represented alternative survives, stop that
filter. The present lemma justifies stronger necessary conditions, not a forecast that
two or three more hours will complete the global proof.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
