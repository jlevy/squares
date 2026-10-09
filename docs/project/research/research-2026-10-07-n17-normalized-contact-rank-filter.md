---
title: n17 Normalized Contact Rank Filter
date: 2026-10-07
status: proposed
---
# n17 Normalized Contact Rank Filter

The [global contact budget](research-2026-10-07-n17-global-contact-budget.md) supplies a
normalized representative with active rank 35 if a strict counterexample exists.
Its nineteen-contact count can be strengthened to a finite necessary-pattern test: a
35-element set must satisfy both a graph-forest condition and wall-incidence capacities.
Failure can be certified by two small, exact rank calculations.
Passing this relaxation does not realize a contact pattern or packing.

This note gives the hand derivation and a proposed finite consumer.
It is written and self-audited by the sole Astra mathematical lead; it has not received
independent mathematical review or formal verification.
No state contact graph, search outcome or target geometry was evaluated in preparing it.
The scalar checker for the preceding note verifies arithmetic premises, not the
normalization or determinant argument here.

## The Quantifier Being Filtered

Freeze seventeen square orientations.
In original coordinates, a physical packing has 34 centre variables and side variable
$L$. As established in the preceding note, a strict counterexample has another
fixed-orientation representative that is a vertex of a closed SAT branch with one
selected row per unordered pair.
The artificial side bounds $0\le L\le U$ are inactive there.
The active physical rows have rank 35.

Call such a representative a *full-rank representative*. The proposed filter rules out
full-rank representatives in specified closed cell assignments.
It does not rule out every packing in those assignments: normalization can move a
packing to another assignment.
Its results therefore belong to a separate normalized-cover record, never the ordinary
exclusion census.

The established lower bound may restrict physical sides to

$$
L\in[L_{\min},U],\qquad L_{\min}=18641771/4000000=4.66044275,\quad U=1169/250.
$$

This is a necessary physical restriction, not a replacement of the normalization LP’s
artificial lower bound zero.
The consumer must bind the accepted lower-bound premise; an unverified numerical lower
bound would not suffice.
The accepted bound and its T-093 replay status are recorded in the
[n17 bracket](../n17-optimality-explainer.md#the-bracket).

### Component Obstructions

Let $G$ be the graph of active chosen pair rows at a full-rank representative.
Translating one connected component leaves all its pair equalities unchanged.
If that component has no contact with either vertical wall, its horizontal translation
is a nonzero null direction of every active row.
The analogous statement holds for horizontal walls.
Every component must therefore have at least one vertical-wall and one horizontal-wall
incidence.

At least one component must touch opposite walls.
Otherwise each component touches at most one of left/right and at most one of
bottom/top. Set $dL=1$ and translate each component horizontally by zero if it touches
the left wall or one if it touches the right wall; choose the vertical translation
analogously for bottom/top.
All active pair and wall rows remain equalities, contradicting rank 35. The preceding
translation argument handles any component missing an axis of wall contact.

If there are $k$ components, these facts require at least $2k+1$ wall incidences: every
component needs two wall directions, and an opposite-wall component needs a third
distinct wall. Since there are at most sixteen wall incidences, $k\le7$. Together with
the preceding note, the selected contact graph has at least nineteen edges and cycle
rank at least three.

These conditions also give inexpensive necessary tests on a graph of *possible*
contacts. Adding edges can merge components or add cycles but cannot remove a cycle.
Every component of the possible graph must permit both wall directions, some possible
component must permit opposite walls, its component count cannot exceed seven, and its
cycle rank cannot be below three.
A high degree in the possible graph is not a reason to reject it: the physical contact
graph may use a proper subset.

## A Forest Witness for Every Rank-35 Basis

Choose 35 independent active physical rows at a full-rank representative.
Each selected pair row has centre coefficients

$$
a_e(x_i-x_j)+b_e(y_i-y_j)
$$

and no $L$ coefficient.
Its normal is a body axis of one of the two squares, but no independence between the
different normals is assumed.
A left or bottom wall row uses one centre coordinate; a right or top wall row uses that
coordinate and $-L$. Supports are constants because orientations are fixed.

Expand the nonzero determinant of these 35 rows by multilinearity in the rows.
For each pair row, choose its x-incidence or y-incidence term.
For each right/top wall row, choose its coordinate term or side-column term.
Left/bottom wall rows have only their coordinate term.
At least one expanded determinant is nonzero.
Zero normal components merely make some terms zero and cause no completeness problem.

A nonzero term uses exactly seventeen x rows, seventeen y rows and one side-column row.
On either coordinate axis, pair rows are weighted graph incidences and wall rows are
weighted single-vertex pins.
Add one ground vertex for that axis.
The resulting reduced incidence matrix is nonsingular exactly when its seventeen edges
form a spanning tree on the seventeen square vertices and ground.
This follows directly: a cycle gives a row dependence, and an unpinned connected
component gives a constant-column null direction; a rooted tree can be eliminated one
leaf at a time.

Thus the nonzero determinant term supplies two wall-rooted forests, one for each
coordinate, and one additional right/top wall row assigned to the side column.
Removing the ground vertices leaves forests with exactly one wall pin in each tree.
Each physical pair or wall row is used at most once.
At most four selected wall rows touch each wall.

This is a necessary witness, not a generic-rank sufficiency theorem.
Different determinant terms can cancel; body-axis coefficients share orientation
variables; and the right-hand sides may be infeasible.
The relaxation below deliberately does not resolve these additional constraints.

## The Two Exact Rank Functions

For a state with seventeen occupied cells, assign its cells a fixed index order.
Construct the following finite ground set $E$ from conservative possible contacts and
wall incidences:

- A possible unordered pair $\{i,j\}$ has two clones: the edge $x_i x_j$ in an x layer
  and the edge $y_i y_j$ in a y layer.
- A possible left/right wall incidence at $i$ has an edge from $x_i$ to x-ground; a
  possible bottom/top incidence has an edge from $y_i$ to y-ground.
- A possible right/top wall incidence has one further clone: an edge between two new
  side-layer vertices.
  All these side clones are parallel.

The three graph layers are disjoint.
They have 38 vertices in total and maximum forest rank $17+17+1=35$. Include all
vertices, including isolated ones, in rank calculations.
The graph rank is

$$
r_G(A)=38-\operatorname{components}(A),\qquad A\subseteq E.
$$

The second independence system permits at most one clone for each physical pair and each
physical wall incidence, and at most four selected wall incidences of each wall type.
These are nested or disjoint capacity sets, so they form a laminar matroid.
Its rank on any set $B$ has the explicit formula

$$
r_C(B)=
\#\{\text{physical pairs with a clone in }B\}
+\sum_{w\in\{\mathrm L,\mathrm R,\mathrm B,\mathrm T\}}
\min\bigl(4,\#\{\text{distinct incidences at }w\text{ with a clone in }B\}\bigr).
$$

The determinant witness is a 35-element subset independent in both systems.
The graph construction allows a pair’s x/y coefficient to be nonzero even when its
actual axis would make that coefficient zero.
This only enlarges the relaxation.

### Rejection Certificate

An exact rejection certificate is simply a subset $A\subseteq E$ satisfying

$$
r_G(A)+r_C(E\setminus A)<35.
$$

For any set $J$ independent in both systems,

$$
|J|=|J\cap A|+|J\setminus A|
\le r_G(A)+r_C(E\setminus A).
$$

The certificate therefore contradicts the necessary 35-element witness.
Its soundness does not depend on the correctness of the search algorithm, a
floating-point rank, a sampled orientation or a genericity assumption.

A survival certificate is a 35-element subset independently checked to be a forest and
to obey every capacity.
It proves only that this finite relaxation survives.
A search that returns neither kind of certificate is unresolved or incomplete; it is not
a geometric verdict.

### A Bounded Search Proposal

Ordinary unweighted matroid intersection is a suitable proposal mechanism.
Start from the empty common independent set.
In the exchange graph, sources are outside elements that can be added to the graphic
system; sinks can be added to the capacity system.
Use arcs from an inside element to an outside element for graphic exchanges, and from an
outside element to an inside element for capacity exchanges.
Choose a shortest augmenting path with a fixed lexicographic tie order.
Check both independence conditions again after each proposed augmentation.

Stop at size 35 and emit its survival certificate.
If no augmenting path exists, let $R$ be the source-reachable elements and propose
$A=E\setminus R$. The checker must recompute the displayed rank bound; failure to obtain
a bound below 35 gives unresolved, regardless of what the search calls its result.
This separates the small rejection argument from the more complicated producer.

There are at most $2\binom{17}{2}+68+34=374$ clones and at most 35 augmentations per
state. Exact graph connectivity and integer capacity counts suffice.
The optional eight/five/three physical-degree bounds are not included: constraining
degrees of the possible graph would be unsound, and adding selected-edge degree
conditions would change this tractable relaxation.

## Conservative Geometric Intake

Use the original closed occupancy cells in the accepted outer frame, not the much
smaller conditional pose domains from experiments 293–301. A complete assignment
consumer must bind the original cell catalogue, its scale and D4 actions, the closed
assignment-cover theorem, and the accepted ordinary exclusions used to form its residue.
Each occupied cell is one graph vertex; no endpoint label permutation is needed.

Reconstruct rational cells with `check_n17_capacity_one_cover.build_cover` on
`UNIQUE_24`, then check its exact `d4_permutations`. Do not use
`select_n17_sub_patterns.cover_geometry` polygons for these inequalities: that adapter
converts the cell coordinates to floating point.
Names and masks do not replace the exact geometric join.

Let $B_i$ be an exact rational axis-aligned bounding box containing cell $i$. A possible
pair is retained whenever the squared minimum distance between $B_i$ and $B_j$ is at
most two. For each axis, the interval distance is the maximum of zero and the two
directed endpoint gaps; sum their squares.
Every physical contact is retained because two touching unit-square centres are at
distance at most $\sqrt2$. Equality is retained.

Embed a physical packing of side $L$ into the outer frame by translation $\delta(1,1)$,
where $\delta=(U-L)/2$. Then

$$
0\le\delta\le\delta_{\max}=(U-L_{\min})/2.
$$

A left-wall contact has embedded x coordinate in $[1/2,3/4+\delta_{\max}]$; a right-wall
contact lies in $[U-3/4-\delta_{\max},U-1/2]$. Use the corresponding y intervals for
bottom/top. Retain a possible wall incidence exactly when the cell’s coordinate interval
meets this closed necessary interval.
The support upper bound $3/4$ is conservative; no orientation or variable-side equality
is inferred from meeting the interval.

These boxes may add impossible pairs or walls.
They must never remove a real contact.
The matrix proof remains in original variable-side coordinates; the embedded cells are
used only to construct a conservative incidence roster.
Replacing the physical moving walls with fixed $U$-wall equalities would invalidate the
argument.

### D4 and Normalized-Cover Accounting

A D4 action on a variable-side packing is an invertible affine change of its 35
variables. It maps physical pair/wall equalities to physical pair/wall equalities and
preserves their rank.
Therefore absence of any full-rank representative in a named assignment transports to
its exact D4 orbit, even though global lexicographic minimality itself need not be
D4-invariant.

The current ordinary residue is 36,768 assignments in 4,683 D4 orbits after sixty
admissions.
A separate normalized cover can combine those ordinary impossibility receipts
with these rank obstructions.
It must explicitly cover every remaining normalized assignment before concluding global
nonexistence. Eliminating some normalized assignments alone neither changes the ordinary
census nor proves a new side bound.

This particular coarse filter uses $[L_{\min},U]$, which includes the known packing at
$S^\ast$. That packing also has a full-rank normalized representative somewhere in the
complete original cover.
Consequently a sound application of this filter alone cannot eliminate every orbit.
A complete optimality proof still needs a separate strict-smaller-side or terminal
argument for surviving representatives; their membership in the old endpoint-family
state is not supplied by normalization.

An arbitrary known feasible endpoint placement need not itself have rank 35. Its
original state is consequently not an automatic survival control for this filter.
A sound endpoint calibration checks that its actual represented contacts and moving-wall
incidences are retained; a stronger survival control requires a separately established
full-rank endpoint-family member in the controlled assignment.
Do not invent that premise or normalize the endpoint inside its old state without proof.

## First Discriminator and Stop Rule

The proposed first target is the complete set of **95 distance-two D4 orbits** in the
accepted current partition.
Freeze their exact named representatives, closed-cell/D4 identity and partition receipt
before any graph construction.
This is a complete selected stratum, not a representative sample of all 4,683 orbits.
Normalization is not claimed to preserve distance from the endpoint assignment.

The primary criterion is at least one independently checked rank-obstruction certificate
among all 95 accounted orbits.
Report how many have obstruction certificates, how many have 35-element survival
certificates and how many are incomplete or unresolved.
A complete target verdict requires all 95 outcomes checked; a stopped run can retain
valid individual certificates without claiming the complete-stratum criterion was
evaluated. No ordinary admission or lower-bound improvement follows from a positive
result.

If all 95 survive, stop this coarse box/contact-rank filter.
Do not respond by enumerating all contact graphs or by relabelling survival as evidence
of a packing. A useful next filter would need a specified new ingredient, such as exact
orientation compatibility or a finite moving-wall feasibility bound, with a new
criterion and completeness proof.

Proposed resource allocation is 120 seconds construction and 60 seconds fresh checking,
one worker, with sampled 4 GiB current RSS per live process and owned-group cleanup.
These are allocations, not runtime predictions.
Freeze at most 374 clones, 38 graph vertices and 35 augmentations per state, one million
exchange tests per state and 64 million over the selected roster, 4,096-bit rational
geometry, a 10 MiB descriptor and 64 MiB output.
Every exchange or geometry budget stop must be explicit.
No packing solver or existing parent-geometry replay is required.

The fresh checker reconstructs every possible-incidence roster from the frozen original
cells, checks each named state and D4 join, and checks only the finite rank or survival
certificate. It does not rerun the search.
Synthetic controls should include a valid two-rooted-forest witness, a subset-rank
obstruction, parallel side clones, the four-wall capacity boundary, duplicate
physical-row clones, disconnected unpinned components, closed box-distance/wall-interval
equality, a D4-transformed complete roster, and altered certificate or input identities.

This offers a bounded global discriminator during the present block.
Its potential gain is a smaller *normalized* cover; the moving-side geometry, full-rank
existence theorem and eventual complete cover remain explicit proof interfaces.

## Actual First Discriminator

Exp303 completed the frozen 95-orbit test with zero rank obstructions and zero
unresolved cases.
Every orbit has a retained 35-clone common-independent-set witness, and
the fresh checker independently verified both finite rank conditions.
Construction and fresh receipts have identical mathematical payloads; the supervised
pair completed normally in 19.484 seconds.

This is a complete miss of the selected coarse relaxation.
Stop this unchanged filter and do not fund a contact atlas from these witnesses.
The result does not realize the selected contacts, supply feasible packings, refute the
normalized-representative lemma or prove that a stronger orientation- and
displacement-aware rank test cannot work.
No ordinary assignment or normalized assignment in this selected roster was excluded.
The current ordinary census and global side bracket remain unchanged.

The retained evidence is in
`packing/campaign/series/series-000-smoke-and-calibration/results/exp-303-normalized-contact-rank-filter/`.
The exact consumer’s finite validation does not independently verify the hand-derived
normalization and determinant arguments above.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
