# Independent Review of the N=11 Structural Normal Form

Date: 2026-09-10. Delegated W10 review of BC328, bead `think-02l0`. Reviewer: GPT-6
Astra, max reasoning.

**Final verdict: PASS for S1, both principal exact fixtures, and the revised source
quantifiers.** Proposition S1 is proved at its stated scope.
The original inference identifying every active pair row as physical contact fails; the
coordinator’s revised sources now distinguish it from the replacement theorem.
Its connected-component, lexicographic-minimum, strict-separation, and rank arguments
are valid. The two principal exact fixtures also check out.
The necessary correction concerns the relationship to retained Lemma V: S1 changes the
quantifier from a preselected separating-axis cell to a connected component of the full
feasible translation space.
It does not prove the retained contact conclusion inside every preselected cell.
The source repair must say this explicitly.

This review used first-principles reasoning and exact arithmetic written below.
It did not edit repository files, run scientific targets, inspect all certificate
consumers, or establish a new bound for eleven squares.
The reviewed candidate is the
[retained structural review](review-2026-09-10-n11-structural-normal-forms.md).
The affected retained statements are
[Lane D, Lemma V](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md#14-lemma-v-the-corrected-lp-vertex-statement-and-the-rank-question)
and
[X-021, fixed-angle representatives](../../../packing/campaign/explorations/X-021-what-can-be-proved-about-eleven-squares.md).

## 1. S1’s Quantifiers and Topology Are Valid

**Status: proved.** Let `n ≥ 1`, fix the finite side `q` and every labelled square’s
orientation, and assume the feasible translation space `F` is nonempty.
At these fixed orientations, containment is a finite set of linear inequalities.
For each pair, the separating-axis alternatives form a finite disjunction of linear
inequalities.
Thus `F` is a finite union of nonempty compact convex polytopes, with empty
selections omitted.
Boundedness follows from containment; there is no need to assume that
these polytopes have full dimension.

A connected polytope that meets a connected component `K` of `F` is contained in `K`:
its union with `K` is connected.
Consequently `K` is a union of some of the finitely many polytopes and is compact.
Its pieces have connected intersection graph.
Otherwise two disjoint finite unions of compact pieces would separate `K`. Joining
points by straight segments inside successive intersecting pieces proves that `K` is
path connected.

There is no hidden assumption that arbitrary closed sets are path connected when
connected. The finite polyhedral decomposition supplies that implication here.
The conclusion applies to each fixed-angle connected component, including a component
consisting of one configuration.

**Exact clarification:** Introduce `n ≥ 1` and “nonempty connected component”
explicitly. For the path corollary, retain the qualifications already present: the path
can be piecewise linear in the centre coordinates, can move several squares together,
and need not decrease the objective at every point.

## 2. Minimizing the Coordinate Sum Anchors Every Physical Component

**Status: proved.** Let

$$
f(z)=\sum_{i=1}^{n}(x_i+y_i)
$$

and minimize it over `K`. Suppose a physical contact component `I` of a minimizer has no
contact with the left wall.
Its union has strictly positive left clearance because it is compact.
Its distance from the union of the other squares is strictly positive when there are
other components: the finitely many relevant closed squares are disjoint as sets.

Choose a positive translation distance smaller than the left clearance and that mutual
distance. Translating all squares of `I` rigidly to the left preserves their internal
geometry, keeps them inside the container, and preserves external separation throughout
the translation. The motion stays in `F`, hence in the original `K`. It decreases `f` by
the translation distance times `|I|`, a contradiction.
When `I` is the only physical component, the mutual-distance restriction is unnecessary.
The same proof works vertically downward.

This proves contact with the two **named** walls, left and bottom, for **every physical
contact component of the chosen representative**. It does not require relabelling,
rotating the container, side optimality, or rigidity.
The contact components concerned are those of the final packing; the motion to that
packing need not preserve the initial contact graph.

**Exact clarification:** State this last distinction if component labels are later
attached to owners or other records.
The theorem does not transport the original packing’s components as named objects.

## 3. The Lexicographic and Strict-Axis Steps Give a Physical Contact Basis

**Status: proved.** Among the minimizers of `f` over `K`, successively minimizing
`x_1,y_1,…,x_n,y_n` is legitimate.
At each stage there is a nonempty compact set of minimizers.
The final set is a singleton because all centre coordinates have been fixed.
Call its point `P*`.

For a pair disjoint as closed sets at `P*`, a strict separating alternative exists among
the listed square axes.
To see this directly, write the centred squares as `S_i,S_j`. They intersect exactly
when `z_j-z_i` belongs to the Minkowski difference `S_i-S_j`. This polygon is full
dimensional, and its facet normals are among `±u_i,±v_i,±u_j,±v_j`. A point outside it
strictly violates one of its facet inequalities.
This gives a listed axis `a` with

$$
a\cdot(z_j-z_i)>h_i(a)+h_j(a).
$$

For a physically contacting pair, choose any valid separating alternative.
If `p` is an actual common point, then

$$
a\cdot z_j-h_j(a)\le a\cdot p\le a\cdot z_i+h_i(a).
$$

Together with the selected separation inequality, these relations force equality.
The selected normal therefore supports the two squares along a line through an actual
common point. It is a physical contact normal, even at a point contact or a degenerate
feature choice.

Let `P_beta` be the selected polytope.
It contains `P*` and, being connected, lies in `K`. Each stage of the lexicographic
minimization on `K` is also minimal among the corresponding points of `P_beta`.
Equivalently, successive linear minimizations on `P_beta` give nested faces ending at
`{P*}`. Hence `P*` is a vertex.

The ambient rank conclusion also holds for a lower-dimensional polytope.
If its active rows at `P*` had rank below `2n`, a nonzero vector annihilating them would
permit small motions in both signs; every inactive row has positive slack.
One sign would lower the first lexicographic objective whose directional derivative is
nonzero. Such an objective exists because the list includes all centre coordinates.
This contradicts minimality.
The active rows therefore have rank `2n`.

Every active wall row at `P*` is a wall contact.
Every selected pair row belonging to a disjoint pair is strictly slack at `P*`, so every
active pair row is a physical contact.
Selecting `2n` independent active rows proves S1(2).

**Exact clarification:** All contact identifications are at `P*`. Strict choices made
there do not make arbitrary vertices elsewhere in `P_beta` physical-contact vertices.
No substantive gap remains in S1’s proof.

## 4. The Per-Square Rank Inference Is Correct and Has a Limited Meaning

**Status: proved.** Let `A` be the `2n × 2n` matrix of an independent active basis.
For each square `i`, its two-column block `A_i` has rank two.
Otherwise some nonzero translation of that square alone would lie in the kernel of `A`,
contradicting nonsingularity.
The nonzero rows of `A_i` are the incident wall or pair-contact normals, with the
relevant signs. Thus every square has at least two linearly independent contact normals
when the other centres are fixed.

The conclusion concerns active equality rows.
The original feasible constraints are unilateral, and the active contacts can open.
Even one square seated against the left and bottom walls has two independent wall
normals and can move up and right when there is room.
Neither translational isolation in the physical feasible space nor rotational rigidity
follows from the rank statement.

**Exact fix to retained summaries:** Replace “no isolated square” by “each square has at
least two linearly independent wall or pair-contact normals.”
The physical graph in the candidate has only square vertices and square-square edges.
S1 allows a singleton component seated against both walls, so “no isolated square” is
false as a general consequence if it refers to that graph.
For example, at `q=3`, put one axis square at `(0,0)` and the other five at lower-left
corners `(2,0),(2,1),(2,2),(0,2),(1,2)`. The first square has no pair contacts; both
components meet the left and bottom walls.
The retained six-square theorem makes this an optimum as well.
This all-`n` example does not decide whether an eleven-square optimum has a singleton
physical component.

## 5. Lemma V Must Be Replaced With Different Cell Quantifiers

**Status: false proof inference; corrected replacement proved.** Lane D starts by fixing
a minimizer’s angles **and a SAT selection valid at that minimizer**. Part (a),
existence of a vertex with active rank 22 in that selected cell, is correct.
Part (b), at least two active rows incident to each square, is also correct.
The proof’s next assertion, that an active pair row is necessarily a physical pair
contact, is false. Finding 6 supplies a complete exact counterexample to that assertion.

The counterexample is at four squares and a nonoptimal side.
It does not disprove the full retained existential statement at an eleven-square
optimum. Conversely, S1 does not prove that original statement with its selected cell
held fixed. The minimization is over a full physical feasible component, and the strict
SAT selection is made only after the representative is chosen.
That new cell need not equal the original cell.

**Exact replacement for Lemma V:**

> Fix a feasible side, all labelled orientations, and a nonempty connected component of
> the full feasible translation space.
> There is a representative in that component and a SAT selection valid there such that
> the selected active rows have rank `2n` and all active rows are physical wall or pair
> contacts. Every physical contact component of this representative meets both the left
> and bottom walls. Every square has two linearly independent incident contact normals.
> At an optimal side the representative remains optimal.

A separate sentence can preserve the original algebraic fact: “For each preselected
nonempty SAT cell, a vertex with `2n` independent active translation rows exists;
physical contact identification does not follow for all those rows.”

The candidate’s sentence “Proposition S1 repairs that conclusion by strengthening the
choice of representative” should become: “Proposition S1 supplies a replacement
existential contact theorem over each full feasible component; it does not retain the
original quantifier over preselected SAT cells.”
X-021’s “in every fixed-angle cell” needs the same correction wherever it is coupled to
physical-contact conclusions.

## 6. Exact Check of the Artificial-Vertex Counterexample

**Status: correct.** In `[0,4]^2`, the lower-left coordinates

$$
Q_1:(0,0),\quad Q_2:(3,1),\quad Q_3:(1,2),\quad Q_4:(3,0)
$$

give centres

$$
z_1=(1/2,1/2),\quad z_2=(7/2,3/2),\quad
z_3=(3/2,5/2),\quad z_4=(7/2,1/2).
$$

Choose the six pair inequalities as follows:

| Pair | Selected inequality | Slack at the fixture | Physical contact |
| --- | --- | --- | --- |
| `1,2` | `x_2-x_1 ≥ 1` | `2` | None |
| `1,3` | `x_3-x_1 ≥ 1` | `0` | None |
| `1,4` | `x_4-x_1 ≥ 1` | `2` | None |
| `2,3` | `y_3-y_2 ≥ 1` | `0` | None |
| `2,4` | `y_2-y_4 ≥ 1` | `0` | Segment `[3,4] × {1}` |
| `3,4` | `x_4-x_3 ≥ 1` | `1` | None |

Together with containment, this defines a valid selected cell.
Its eight active rows can be solved in triangular order:

$$
x_1=1/2,\ y_1=1/2,\ x_4=7/2,\ y_4=1/2,\ x_2=7/2,
\quad y_2-y_4=1,\ x_3-x_1=1,\ y_3-y_2=1.
$$

They uniquely determine all eight centre coordinates and have determinant of absolute
value one after row and column ordering.
The fixture is a vertex.

Nevertheless, `Q_3=[1,2]×[2,3]` has positive wall clearance, and its Euclidean distances
from `Q_1,Q_2,Q_4` are respectively `1,1,√2`. Both pair rows incident to `Q_3` are tight
support-projection equalities without physical contact.
The two-square example `Q_1=[0,1]^2`, `Q_2=[1,2]×[2,3]` is the same failure in its
smallest displayed form: the horizontal gap is zero while the actual distance is one.

The fixture proves failure of the contact-identification inference at an entire cell
vertex. It proves neither failure of rank 22 nor a counterexample to an eleven-square
existence theorem.

It does not even refute the weaker existence of a vertex with no contact-free square
inside this particular four-square cell.
Keeping the other three squares fixed and moving `Q_3` to lower-left corner `(2,2)`
gives another vertex in the same selected cell.
The active basis replaces `x_3-x_1=1` with `x_4-x_3=1`, and `Q_3` now touches `Q_2` at
`(3,2)`. Its selected row against `Q_4` remains a false contact.
Thus this example must not be described as a disproof of the full per-cell existential
conclusion.

## 7. Exact Check of the Tilted Pair and Its Escape Obstruction

**Status: correct.** Put

$$
u=(4/5,3/5),\quad v=(-3/5,4/5),\quad h=7/10,\quad a=5/7,
\quad q_0=2h+a=74/35,
$$

and take two unit squares of these same orientations at

$$
z_A=(49/70,99/70),\qquad z_B=(99/70,49/70).
$$

Their axis-aligned bounding boxes are

$$
[0,7/5]\times[5/7,74/35],\qquad
[5/7,74/35]\times[0,7/5].
$$

Thus `A` meets left and top, while `B` meets bottom and right.
Their relative coordinates in the orthonormal frame are

$$
u\cdot(z_B-z_A)=1/7,\qquad v\cdot(z_B-z_A)=-1.
$$

For identically oriented unit squares, interior overlap occurs exactly when both
relative coordinates have absolute value below one.
Here the second coordinate is exactly `−1`, so the interiors are disjoint.
In `A`’s frame, the common segment has `v` coordinate `−1/2` and `u` coordinate in
`[-5/14,1/2]`. Its endpoints in the original frame are

$$
(5/7,4/5),\qquad(7/5,46/35),
$$

whose difference is `(24/35,18/35)`. Its length is `30/35=6/7`. Neither square meets
both left and bottom or contains any container corner.

Moving `A` right by `t`, or `B` left by `t`, gives relative coordinates

$$
(1/7-4t/5,-1+3t/5).
$$

Moving `A` down by `t`, or `B` up by `t`, gives

$$
(1/7+3t/5,-1+4t/5).
$$

For every `0<t<10/7`, both entries in either pair have absolute value below one.
These moves create interior overlap.
The wall constraints additionally forbid `A` moving left and `B` moving down.
Individual bottom-left stability is therefore proved, and remains true after increasing
the container side while keeping the same origin and positions.

At `q_0`, every centre coordinate lies in `[h,h+a]`. If `d` is the relative centre
vector, then `|d_x|,|d_y|≤a`, giving

$$
|u\cdot d|\le(7/5)a=1,\qquad |v\cdot d|\le(7/5)a=1.
$$

Nonoverlap requires equality in at least one.
Equality requires both coordinate differences to attain their extreme magnitudes with
the corresponding signs.
Hence `d` is one of `(a,a),(a,-a),(-a,a),(-a,-a)`, and in each case the two centres are
forced to the appropriate opposite corners of their allowed centre box.
The whole labelled fixed-angle feasible space consists of exactly four points.
The chosen component is a singleton and has no square touching both left and bottom.

This verifies a limitation on same-component normalization.
Another isolated diagonal arrangement, with centres `(h,h)` and `(h+a,h+a)`, does have a
square on the chosen wall pair.
The fixture therefore does not disprove a full-space existential snug-square statement,
even at these fixed orientations.
It is also not a free-rotation optimum, since `74/35>2=s(2)`.

Removing the walls leaves `A` blocked to the right and `B` blocked upward.
Neither can move freely in both directions.
This refutes extension of the orthogonal-rectangle escape lemma to freely tilted
squares. The source’s definitions require unobstructed straight translation along each
named direction; its orientation choices are horizontal or vertical.
The candidate’s use of the fixture matches that precise statement.
[Huang–Ye–Chen, definitions 5–6 and Lemma 2](https://arxiv.org/html/1107.4463v1).

## 8. The Other Displayed Counterexamples Respect Their Quantifiers

**Status: correct at the stated scope.** The single tilted square with centre
`(7/10,7/10)` has the four displayed vertices and support extrema `0` and `7/5` on both
axes.
The minimum of `x+y` over it is `3/5`, so it misses the origin despite touching the
two walls. Conversely, a square in a quadrant that contains the quadrant’s vertex must
have that point as one of its own vertices: the linear functional `x+y` has its unique
minimum there.
Its right-angle tangent cone must coincide with the quadrant, forcing axis
alignment. The candidate correctly distinguishes literal occupancy from snugness.

The corner-free two-square optimizer is valid.
For completeness, if a contained unit square has coordinate width `w=|cos θ|+|sin θ|`
and `q<2`, the vector from its centre to the container centre has coordinate magnitudes
at most `(q-w)/2`. Each component in the square’s own orthonormal frame therefore has
magnitude at most

$$
\frac{w(q-w)}2<\frac{w(2-w)}2
=\frac{1-(w-1)^2}{2}\le\frac12.
$$

Thus the container centre is strictly inside every contained unit square, precluding two
squares with disjoint interiors.
The displayed side-two packing is optimal and has no literal corner occupants.
It refutes an “every optimizer” assertion without refuting a “some optimizer” assertion.

The frozen squares `[0,1]^2` and `[2,3]^2` need a containing axis-aligned square of side
at least three because both coordinate spans equal three.
Neither physical component spans opposing walls.
This correctly separates fixed-configuration container minimality from optimality after
repacking.

For the six-square rotational family, the moving square centred at `(1,1)` always lies
in `[1-√2/2,1+√2/2]^2`, strictly inside the vacant `[0,2]^2`. Its angle can vary
continuously without meeting any of the other five squares.
Optimality here uses the retained theorem `s(6)=3`, stated in the
[six-square memorandum](../../../packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-i-six-unit-squares.md).
This review checked the geometry and that retained premise; it did not re-prove the
six-square lower bound.

## 9. Strongest Surviving Statement and N=11 Consequences

For every `n≥1`, every feasible finite side `q`, every labelled fixed orientation
vector, and every nonempty connected component of its full feasible translation space,
there exists a representative `P*` in that component satisfying all of S1:

1. Every physical contact component meets both the left and bottom walls.
2. For a suitable separating-axis selection made at `P*`, the active translation rows
   have rank `2n`, and every active row represents a physical wall or pair contact.
3. Every square has at least two linearly independent incident contact normals.
4. Every starting point in the component can be joined to `P*` by a continuous,
   piecewise-linear feasible path with all orientations and the side fixed.

At `n=11`, this gives a 22-row independent physical-contact basis at the trial side
itself. In each physical component a simple path joins a left-wall square to a
bottom-wall square. Selecting such a path gives either a single square touching both
walls or a path of `2,…,11` distinct squares.
These are finite constraint types with real angle and position variables.
To make the alternatives disjoint, select the one-square case whenever a square touching
both walls exists; exclusivity is otherwise unnecessary for a covering argument.

A selected cell has 44 wall rows and 55 pair rows, so `8^55` axis selections and
`binom(99,22)` candidate bases are valid loose finiteness bounds.
An invertible basis eliminates the centres in terms of the angles and `q`. The angle
variables remain real and must satisfy every residual condition; no freedom of motion in
each angle is implied.
Singular choices require another valid basis, as the candidate says.

At a global optimum, Lane D’s opposite-wall spanning lemma combines with S1 to give a
physical component meeting left and bottom and at least one of right or top.
The adjacent-wall and contact-basis reductions themselves need no dilation or contact
tolerance. Accordingly, the retained blanket wording that every structural lemma at a
trial side requires the dilation tolerance should be narrowed to properties imported
only from an unknown optimum.
Opposite-wall spanning still needs its optimality premise or a separate valid transfer
argument.

The theorem supplies no literal corner occupant, forced flush edge, prescribed finite
angle set, short-path bound beyond eleven, or global exclusion at `96/25`. Owner labels
must be chosen for the normalized packing.
Actual parent contacts do not become contacts between strict inner cores.
A proposed case cover must still cover a valid representative and a valid label for
every hypothetical feasible packing.
Nothing checked here establishes that such a cover has been excluded, or that all
existing numerical consumers are unaffected by the retained proof gap.

## 10. Final Wording Check Against the Coordinator’s Revised Files

The revised Lane D and X-021 correctly separate the algebraic per-cell theorem from the
physical-contact theorem on full feasible components, and they now allow singleton
physical components.
The following exact corrections were identified during the final wording check; the
coordinator applied them before this review was closed:

1. **Durable structural review, §4:** Replace “This is a fixed-side four-square
   counterexample to the inference used in the proof and to its claim for an arbitrary
   preselected separating-axis cell” with “This is a fixed-side four-square
   counterexample to the assertion that every tight pair row at an arbitrary selected
   cell vertex is a physical contact.”
   The next sentence should preserve the limitation: “It does not disprove the retained
   existential claim for every preselected cell at an eleven-square optimum.”
   Finding 6 gives a vertex without a contact-free square in the same example cell and
   shows why this distinction matters.
2. **Lane D, V+ proof summary:** Replace “first lexicographically minimizes the centre
   coordinates” with “first minimizes `f=Σ_i(x_i+y_i)` over the component and then
   breaks ties lexicographically in all centre coordinates.”
   Then a translation of any physical component does lower the first objective, as the
   next sentence claims.
   Pure lexicographic minimization could also be used in a different proof, but a
   translation of a component excluding square 1 need not lower the first coordinate.
3. **Lane D, §3 item 1:** Replace the blanket statement that all of §1.2–1.4 needs
   dilation with “Opposite-wall spanning and properties known only at the unknown
   optimal side require a valid transfer to the trial side; Lemma T supplies the stated
   tolerance for dilation.
   Proposition V+ is proved directly at every feasible trial side and requires no
   contact tolerance.”
4. **X-021, Robust transfer:** Replace “Every structural lemma handed to a certificate
   must be stated with that tolerance” with “A structural fact imported by this dilation
   must include its resulting tolerance.
   The component normal form is proved directly at the trial side and retains exact
   contacts.”

The corrected durable review, Lane D proof summary, and X-021 transfer paragraph were
re-read. The audited theorem and source-repair claims pass, with no remaining theorem
blocker. The retained review now records this PASS, while global exclusion and any
certificate-consumer audit remain outside its scope.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
