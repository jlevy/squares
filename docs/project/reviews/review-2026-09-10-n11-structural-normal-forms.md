# N=11 Structural Normal Forms

Date: 2026-09-10. BC328; bead `think-02l0`; W10 insight iteration.
Author: GPT-6 Astra, max reasoning.
Status: analytic derivation and source review; independent review PASS. No scientific
target was run, no claim identifier was allocated, and the lower bound is unchanged.

If eleven squares fit at a side `q`, there is a packing at the same side, with the same
eleven orientations, in which every physical contact component touches both the left and
bottom walls. One can choose this representative to have 22 independent active
translation constraints, each arising from a genuine wall or square contact.
The proof below yields an exhaustive alternative between one square touching both
adjacent walls and a chain of distinct squares joining those walls.
It does not require literal corner occupancy, prescribed angles, or rigidity.

The [independent review](review-2026-09-10-n11-structural-normal-forms-independent.md)
rechecked the topology, minimization, strict separating-axis choice, rank argument and
both exact fixtures from first principles.
It found no remaining theorem blocker after the source wording was narrowed from an
arbitrary cell vertex to the representative selected over a full feasible component.

The review also identifies a repair to a retained argument.
Equality of projection intervals along a selected separating axis need not be physical
contact. Choosing an arbitrary vertex of one selected-separation polytope does not
justify interpreting all active rows as contacts.
A lexicographic choice over a full feasible component, followed by strict separation
choices for disjoint pairs, supplies the missing step.

## 1. Definitions and Quantifiers

Let `C_q=[0,q]^2`. A closed unit square is

$$
Q_i=z_i+[-1/2,1/2]u_i+[-1/2,1/2]v_i,
\qquad v_i=R_{\pi/2}u_i,
$$

where `z_i=(x_i,y_i)` is its centre and `u_i` is a unit vector.
Orientation is defined modulo a quarter turn.
A **packing** requires containment in `C_q` and pairwise disjoint interiors; boundaries
may touch.

| Term | Definition used here | What does not follow merely from the definition |
| --- | --- | --- |
| **Optimal packing** | A packing at `q=s(n)`, the infimum of feasible sides | Uniqueness, isolation, a contact graph, or corner occupancy |
| **Inclusion-minimal container for a fixed configuration** | No strictly smaller, translated, axis-aligned square contains the unchanged positioned squares | Optimality after moving squares, or a connected spanning chain |
| **Insertion-saturated packing** | No further unit square can be inserted while the existing squares stay fixed | Local optimality or literal corner occupancy |
| **Boundary contact** | A square meets a specified container wall | Positive-length or flush contact; a tilted square normally touches a wall at a vertex |
| **Flush wall contact** | A positive-length edge segment lies in a wall | Any other square shares that orientation |
| **Literal corner occupant** | A square contains a container vertex | This is stronger than touching the two adjacent walls |
| **Snug square at a corner** | One square touches both adjacent walls | It contains the literal corner; a tilted snug square leaves a gap |
| **Corner-mark owner** | A selected strict core contains one of the retained near-corner marks | Its parent touches a wall, contains the literal corner, or owns both marks |
| **Physical contact graph** | Square labels are vertices; an edge means two closed squares intersect | Positive-length contact, common orientation, or rigidity |
| **Contact component** | A connected component of that graph | The component must remain rigid during all motions |
| **Perturbation** | A specified continuous motion preserving containment and non-overlap | An arbitrary local optimizer finds that motion |
| **Quench** | A numerical descent procedure with a named objective and termination rule | Global optimality or completeness |
| **Rigid** | Isolated among nearby feasible configurations after specifying motions and quotient symmetries | Rank in an artificial inequality branch alone proves rigidity |
| **Finite pose alternative** | A finite list of constraint types covering a required representative of every feasible case | A finite list of actual poses; each alternative may contain a continuum |

“Inclusion-minimal packing” is ambiguous and should be replaced by a specified notion
above. A deletion-minimal obstruction to a capacity claim is another distinct notion.

Keep three quantifier patterns separate: every packing at `q` has a property;
feasibility at `q` implies that some packing at `q` has it; some global optimum has it.
The second suffices for a fixed-side exclusion if every packing with that property is
excluded. The third concerns the unknown optimal side unless the argument treats that
side as a variable or supplies a valid transfer to `q`.

## 2. Retained Structural Results

This avenue has already been pursued.
The relevant sources are:

- `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md`:
  compactness, opposite-wall spanning, fixed-angle LP vertices, chain projections, and
  transfer tolerances.
- `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-a-corner-structure.md`:
  saturation and overhang, four distinct corner blockers, corner penetration, common
  contained boxes, and corrected penetration-bin alternatives.
- `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md`,
  §3: independent replay of the four-corner mark-pair ownership premise at `q=96/25`.
- `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md`:
  sixteen classes per corner and sound residual counting/banking.
- `docs/project/reviews/review-2026-09-07-n11-hybrid-strategy.md`: fixed-side anchors,
  angle cells, outer LPs, local resources, and the scope of orientation/contact
  arguments.
- `packing/cases/n11_five_dot_cover/`: T023’s selected conditional exclusion and its
  continuation contracts.
- `packing/cases/n11_threshold_certificate/t-025-threshold-certificate-proof.md` and
  `t-026-dilation-limit-proof.md`: the certificate and exact dilation-limit argument
  proving the current unconditional lower bound
  `s(11) >= 955000*sqrt(518400042893309449)/179696714646249 =
  3.826447410572939744...` at V4/C5. The later
  [claim review](review-2026-09-10-t025-t026-verifiable-claims.md) supplies the mapped
  C5 review; it does not change this structural review’s scope.

Compactness supplies an optimum because centres are bounded, orientations live on a
compact quotient circle, and containment/non-overlap are closed.
It imposes no corner condition.
Martin proves a broader compactness theorem; see
`packing/resources/papers/martin-2000-compactness-theorems-geometric-packings.md` and
the [primary source](https://arxiv.org/abs/math/0005054).

Lane D’s **opposite-wall spanning lemma** uses side optimality.
If no physical contact component spans either pair of opposite walls, each component has
room in at least one direction on each coordinate axis.
Distinct components have positive mutual distance.
Small independent translations fit them in a smaller square, a contradiction.
The conclusion is horizontal *or* vertical spanning; it does not force both in every
optimizer.

At `q=96/25`, the retained weighted ownership premise forces four distinct selected core
owners. It does not force four literal corner occupants or wall-contact parents.
The sixteen raw labels per corner are an overlapping cover of choices, not sixteen
feasible poses. The corrected penetration-bin method is a separate complete alternative:
near-corner cases give common occupied regions and far-corner cases give avoided
triangles. Neither family should be conflated with four fixed flush squares.

## 3. A Normal Form at the Trial Side

**Proposition S1.** Fix a feasible side `q`, a feasible labelled orientation vector, and
any connected component of its feasible translation space.
That component contains a packing `P*` such that:

1. Every physical contact component touches both the left and bottom walls.
2. There are `2n` independent active translation rows, each a genuine wall or pair
   contact.
3. Each square participates in at least two linearly independent contact normals when
   all other centres are fixed.

The representative retains `q`, all labelled orientations, and all squares.
At `n=11` the rank is 22. This is an existence reduction, not a rotational rigidity
theorem or a finite-angle theorem.
The rank statement concerns equality rows; unilateral contacts may open during a
feasible motion. A contact component may consist of one square when that square touches
both named walls; “no isolated square” would therefore be misleading if isolation
referred only to the square–square contact graph.

### Proof

For a unit vector `a`, define the support radius

$$
h_i(a)=\tfrac12\bigl(|a\cdot u_i|+|a\cdot v_i|\bigr).
$$

The separating-axis theorem gives the exact pairwise disjunction

$$
a\cdot(z_j-z_i)\ge h_i(a)+h_j(a),
\qquad a\in\{\pm u_i,\pm v_i,\pm u_j,\pm v_j\}.
$$

At fixed orientations, selecting one alternative per pair and adding four containment
rows per square gives a compact polytope in `2n` centre coordinates.
The full feasible space `F` is a finite union of those polytopes.

Every connected component `K` of `F` is a union of some of the polytopes: any connected
polytope meeting `K` lies in `K`. There are finitely many, so `K` is compact.
It is also path connected.
The intersection graph of its convex pieces is connected; straight segments through
successive intersections give a piecewise-linear path.

Over `K`, first minimize

$$f(z)=\sum_i(x_i+y_i).$$

Among its minimizers minimize `x_1`, then `y_1`, then the remaining centre coordinates
in order. Compactness makes each step attainable.
The final lexicographic minimum `P*` is unique.

Suppose a physical contact component `I` of `P*` does not touch the left wall.
It has positive left clearance and positive distance from every other physical
component. Translating precisely `I` a sufficiently small distance left preserves
containment, internal relative positions, and external separation.
The short continuous motion stays in `F`, hence in `K`, and lowers `f` by the distance
times `|I|`. This is impossible.
The same argument downward proves bottom-wall contact.

Now choose a strictly separating axis for every pair disjoint as closed sets at `P*`.
Such an axis exists: the difference of two squares is a polygon with facet normals among
the listed axes, and a point outside it strictly violates a facet inequality.
For a physically contacting pair, choose any valid separating alternative.

The resulting selected polytope `P_beta` contains `P*` and lies in `K`, since it is
connected. Therefore `P*` is its lexicographic minimum too.
Successive linear minimizations over a polytope give nested faces, ending at the
singleton `{P*}`. Thus `P*` is a vertex and its active rows have rank `2n`.

Every active wall row is a wall contact.
Every active pair row is a physical contact because disjoint pairs were assigned
strictly slack alternatives.
Select `2n` independent active rows.
Their restriction to one square’s two columns must have rank two, or the full rank would
be less than `2n`. This proves the final assertion.
∎

The adjacent-wall conclusion works directly at a trial side.
It needs neither the unknown optimum nor dilation of an optimizer into `C_q`. Applied at
`q=s(11)`, it preserves optimality; combined with opposite-wall spanning, it gives a
minimizing representative with one physical component touching three walls: left,
bottom, and at least one of right or top.

The component version also supplies a path from an initial packing to such a
representative, keeping angles fixed.
It does not make that path arbitrarily small, realizable by independent single-square
moves, or decreasing in `f` at every intermediate point.

The initial minimization is analogous to Huang–Ye–Chen’s rectangle Lemma 1. The
component and true-contact-basis steps above are stated and proved here for arbitrary
fixed square orientations.
The [rectangle paper](https://arxiv.org/html/1107.4463v1) requires edges parallel to the
container in its subsequent placement theorem.

## 4. Repair to the Retained Vertex Argument

Lane D, Lemma V, treats every active pair row as a physical contact.
For an arbitrary selected separating axis this implication is false.
Take

$$
Q_1=[0,1]\times[0,1],\qquad Q_2=[1,2]\times[2,3].
$$

Their horizontal projection intervals touch, so the horizontal separation row is an
equality. The squares are disjoint with vertical distance one.

This can occur at an entire selected-polytope vertex.
In `[0,4]^2`, place four axis squares at lower-left corners

$$Q_1:(0,0),\quad Q_2:(3,1),\quad Q_3:(1,2),\quad Q_4:(3,0).$$

Use the left and bottom wall equalities for `Q_1`, right and bottom wall equalities for
`Q_4`, the right wall for `Q_2`, and these pair rows in centre coordinates:

$$y_2-y_4=1,\qquad x_3-x_1=1,\qquad y_3-y_2=1.$$

The eight rows are independent and fix every centre.
For the remaining pairs choose strictly valid horizontal separations.
The selected cell therefore has this packing as a vertex, yet `Q_3` touches neither a
wall nor another square.
Its two active pair rows are equalities of support lines only.

This is a fixed-side four-square counterexample to the inference used for an arbitrary
vertex of a preselected separating-axis cell.
It is not an optimal four-square packing or an eleven-square counterexample.
Proposition S1 supplies a different existential conclusion: first minimize over a
connected component of the full fixed-angle feasible space, then choose a cell whose
disjoint-pair rows are strict.
It does not prove the stronger physical-contact statement for every preselected cell;
the fixture does not refute that separate existential statement either.
A source correction should preserve the useful rank reduction and replace the
unsupported contact-identification step.

No existing numerical certificate is invalidated solely by this gap.
A consumer would be affected if it had interpreted arbitrary tight support rows as
actual occupied-contact geometry.

## 5. Exact Counterexamples and Their Limits

### Adjacent walls do not imply literal corner occupancy

Let `u=(4/5,3/5)`, `v=(-3/5,4/5)`, with centre `(7/10,7/10)`. Its square vertices are

$$
(3/5,0),\quad(7/5,3/5),\quad(4/5,7/5),\quad(0,4/5).
$$

It touches both axes in `[0,7/5]^2`, but misses the origin; its minimum `x+y` is `3/5`.
Conversely, a nondegenerate square contained in a quadrant and containing its vertex
must have that point as a square vertex.
Its interior angle equals the quadrant’s angle, so its incident edges lie on the axes.
Literal corner occupancy forces both a specific placement and axis alignment.

### Not every optimizer occupies a literal corner

The squares `[0,1] x [1/2,3/2]` and `[1,2] x [1/2,3/2]` pack optimally in `[0,2]^2`,
since `s(2)=2`, but occupy no container vertex.
A short proof of the lower bound is available: if a unit square of axis-parallel width
`w` fits in a container of side `q<2`, the container centre differs from the square
centre by at most `(q-w)/2` in each coordinate.
Its coordinates in the square’s own frame therefore have absolute value at most
`w(q-w)/2<1/2`, since `w(2-w)=1-(w-1)^2<=1`. The container centre lies strictly inside
every contained unit square, so two cannot have disjoint interiors.
A downward translation gives a different optimizer with corner occupants.
This refutes the universal statement while leaving the existential one intact.
It does not settle whether some `n=11` optimizer occupies corners.

### Frozen-container minimality does not imply a spanning component

The two squares `[0,1]^2` and `[2,3]^2` make `[0,3]^2` inclusion-minimal for that fixed
configuration. They are separate physical components and neither spans opposing walls.
They can be repacked more tightly.
The side-optimality premise cannot be replaced by this weaker minimality.

### Individual stability does not seat a square on both chosen walls

Use the rational axes above and set

$$h=7/10,\qquad a=5/7,\qquad q_0=2h+a=74/35,$$

with centres `z_A=(h,h+a)` and `z_B=(h+a,h)`. The first square touches the left and top
walls; the second touches the bottom and right walls.
Their difference is `(a,-a)`, with

$$u\cdot(z_B-z_A)=1/7,\qquad v\cdot(z_B-z_A)=-1.$$

Their interiors are disjoint and they share an edge segment of length `6/7`. Neither
touches both left and bottom, and neither contains a literal corner.
Each is individually bottom-left stable: `A` cannot move left through its wall or down
through `B`; `B` cannot move down through its wall or left through `A`. This individual
stability persists in a larger container with the same lower-left origin.

At `q_0` these configurations are isolated with the angles fixed.
Centre coordinates lie in `[h,h+a]`; the maximum possible separating-axis projection of
their difference is `(4/5+3/5)a=1`. Equality requires both coordinate differences to be
extreme with the prescribed signs.
Hence the feasible fixed-angle arrangements are discrete diagonal placements.
A same-component translation argument cannot in this example put one square on the
chosen wall pair.

It is not a free-rotation optimum: `q_0>2=s(2)`. It limits the translation/stability
proof, not the existential question for free rotations at `n=11`.

### The orthogonal-rectangle escape lemma fails for tilted squares

Remove the walls from the same fixture.
Moving `A` a small positive distance `t` right changes the local difference coordinates
to

$$ (1/7-4t/5,-1+3t/5), $$

both strictly between `-1` and `1`, so the squares overlap.
Moving `B` up changes them to `(1/7+3t/5,-1+4t/5)` and also causes overlap.
Neither square can escape freely in both upward and rightward directions.

Huang–Ye–Chen’s Lemma 2 is an escape statement for axis-parallel rectangles.
This exact tilted pair refutes its direct extension.
It does not refute a different normalization proof.
See the [primary theorem and hypotheses](https://arxiv.org/html/1107.4463v1).

### Optimal packings can have continuous angle freedoms

At `n=6`, put five axis squares at lower-left corners `(2,0),(2,1),(2,2),(0,2),(1,2)`. A
sixth unit square centred at `(1,1)` fits in the vacant `[0,2]^2` at every orientation.
All six fit in `[0,3]^2`, and `s(6)=3`, so this is an optimal family with a rotational
rattler. See the retained six-square source and lane D. This rules out the claim that
every optimum has only isolated angles; it leaves the possibility of choosing a
convenient optimizer open.

## 6. Finite Alternatives and the Weight Argument

Apply S1 at a hypothetical feasible trial side and take a simple physical contact path
from a left-wall square to a bottom-wall square.
After consistent relabelling, either:

- One square touches both walls.
  Its centre is `(h(theta),h(theta))`, with `h(theta)=(|cos theta|+|sin theta|)/2`; its
  actual angle is continuous.
- A path of `k` distinct squares joins the walls, for some `2 <= k <= 11`. Consecutive
  squares physically contact.
  Angles and unfixed positions remain continuous.

This is an exhaustive finite disjunction of constraint types.
Long paths, point contacts, and feature degeneracies must remain covered.
Treating the one-square case as exhaustive would restore the unproved corner premise.

The snug-parent branch has one continuous parameter instead of the usual bottom anchor’s
horizontal position and angle.
A two-parent path supplies two wall contacts and one genuine pair contact.
Its dimension depends on the contact features and dependencies; nominal equation
counting alone is not a proof of dimension.

A full basis language is also finite.
At `n=11` a selected cell has 44 wall rows and 55 selected pair rows.
S1 supplies a 22-row true-contact basis.
The loose bounds `8^55` separation selections and choices of 22 rows among 99 establish
finiteness, not tractability.
A nonsingular basis can eliminate centres in terms of angles and `q`; all eleven angles
remain continuous.
A determinant-zero locus for one basis must be covered through another
valid representation, not discarded.

The physical KKT argument has a different role: its at-most-34 positive scalar
multiplier rows are a stress support in a variable-side physical system, not a contact
count or the 22-row fixed-side basis.
Its dilation direction is unavailable in an unchanged fixed-side or artificially
partitioned system. See
`packing/resources/papers/n11-complete-research-bundle-2026-09-07/original_review/n11_research_review.md`,
Propositions A–B, and
`packing/campaign/explorations/X-017-compatibility-and-complete-case-covers.md`.

At `q=96/25`, select corner-mark owners *after* choosing the normalized packing.
The existing owner theorem still applies, but normalization need not preserve the
initial owner labels.
Each owner’s parent has physical contact paths to left and bottom; it need not touch
either wall itself. Those joint restrictions may tighten a residual family.
Parent contact must be transferred through actual parent geometry: strict inner cores do
not touch merely because their parents touch.

The required global logic is:

$$
\mathcal F_q\ne\varnothing\Longrightarrow
\exists P\in\mathcal N_q\ \exists\sigma\in S(P),
$$

where `F_q` is the physical feasible set, `N_q` the normal-form family, and `S(P)` its
valid owner/contact labels.
It suffices to prove that every normalized packing has at least one valid label among
the excluded branches.
Excluding every raw label is sufficient but stronger than necessary.

For `k` distinct forced parents, a point-mass residual certificate can require mass at
least one on every remaining admissible core and

$$\mu(C_q)-\mu\Bigl(\bigcup_i R_i\Bigr)<11-k.$$

The banked regions `R_i` must lie in selected owner cores.
A region known only to lie in a unit parent can restrict residual geometry but cannot
automatically supply banked core mass.
Threshold atoms require their independently validated packing-budget rule.
None of these obligations disappears through normalization.

## 7. Concrete Next Obligations

This ordering is a strategic recommendation based on the current instruments and proof
gaps, not measured comparative productivity.

| Item | Required setup | Useful outcome and exact limit |
| --- | --- | --- |
| Independent S1 review and source repair | Check compactness, the component argument, strict SAT alternatives, and lexicographic faces from the equations | A publishable normal form and repaired contact inference; no new bound |
| Actual-contact adapter controls | Positive fixture: tilted pair at `74/35`; negative fixture: disjoint squares with equal projection endpoints | Separate true contact, support-line equality, positive gap, and interval uncertainty |
| One snug-parent pilot | Define the one-parameter parent family, derive a safe strict-core domain, freeze a matched baseline, then preregister | A certificate or exact obstruction for the declared conditional branch/resource family |
| One two-parent path pilot | Keep full contact, containment, feature alternatives, and a comparison dropping only contact | Measure whether genuine contact improves the residual restriction; not global coverage |
| Owner routing with contact paths | Consume BC326’s parent geometry and identify the extra relation it does not already enforce | A proved map from normalized packings to excluded valid owner choices; pairwise necessity alone is insufficient |
| Penetration-bin alternative | Use corrected lane-A Theorem B and re-establish the core banking region for the selected net | Separate near/far corner certificates; one neutral site family does not decide other resources |

BC326 can continue without a theorem that every optimizer has corner squares.
S1 is a prospective addition to its strategy, not a reinterpretation of a saved run as
having tested these contacts.
Global exclusion at `3.84` still requires complete required-branch coverage or an
adequate selection theorem.

## 8. Literature and Evidence Limits

The review checked the retained Stromquist corner/nonavoidance arguments, Martin’s
compactness theorem, project contact/ownership reports, and the physical stationarity
packet. It also inspected Huang–Ye–Chen’s
[real-parameter rectangle theorem](https://arxiv.org/abs/1107.4463) and its separate
[integral formulation](https://arxiv.org/abs/1111.3715). Both use orthogonal placement;
“rotatable” there means horizontal or vertical placement.
Their constructive placement theorem cannot be imported for freely tilted squares
through its escape lemma.

Dewar’s contact bounds distinguish homothetic and arbitrarily oriented squares and
require generic size conditions for the low contact-count conclusions.
Eleven equal sizes do not meet that condition.
The paper does not supply an orientation or contact-count normalization here.
See `packing/resources/papers/dewar-2024-contacts-oriented-squares.raw.md` and the
[primary source](https://arxiv.org/abs/2210.10422).

This was a bounded source review, not a systematic literature search.
The checked sources supply no theorem that some `n=11` free-rotation optimum occupies
all four literal corners, has a specified number of flush squares, or uses only two
exact orientations. This is not evidence that no such theorem or alternate proof exists.

## 9. Ladder of Inference

| Level | Finding | Permitted conclusion |
| --- | --- | --- |
| Definitions and retained facts | Compactness, physical non-overlap, owner forcing, current bound packets | These premises retain their exact meanings |
| Exact counterexamples | Corner-free optimizer; tilted snug square; stable tilted pair; false contact from projection equality; rotational rattler | Only the specifically quantified stronger statements or proof transfers fail |
| New analytic derivation | S1 with a complete proof and independent PASS | A fixed-side existential adjacent-wall/contact-basis normal form is available at its stated component-wise scope |
| Method implication | Normalized packings satisfy joint contact restrictions compatible with valid owner choices | A contact-conditioned residual experiment can be formulated without assuming literal corners |
| Unmeasured possibility | Snug anchors or short genuine contact paths may give useful certificates | Testable possibility, not demonstrated gain or productivity |
| Open | Global branch coverage, useful routing, literal corner existence for some `n=11` optimum, stronger bounds from these restrictions | No conclusion follows from the earlier levels alone |

The next concrete work is independent review of S1, repair of the contact inference, and
one declared contact-conditioned pilot through the experiment process.
The evidence does not establish that the broader corner, contact, orientation, or
combinatorial routes are exhausted.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
