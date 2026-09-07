# Alternative Routes Toward an Exact Resolution

Historical contributed strategy, excerpted with its mathematical corrections. Ideas and rankings are proposals. Later local-radius, scalar-refinement and density results are in files 08-12. The purpose is to expose alternatives and their quantifiers, including routes outside the current allocation; no claim of feasibility or novelty is implied.

<a id="source-1"></a>

## Source 1: `docs/project/reviews/review-2026-09-05-strategy-gpt-56-pro-gemini-grok.md`

Snapshot `4d305597a505`, source lines 98-469.

<a id="source-1-revised-judgment"></a>

#### Revised judgment

The feedback materially improves the strategy.
Its most important contribution is not any individual technique; it is the insistence
that we distinguish **three different proof systems**:

1. a one-body fractional covering certificate, which is what proves \(3.81\);
2. conditional versions of that certificate, valid only after a genuine case split;
3. configuration-level or integral arguments that encode compatibility among several
   squares.

Several tempting ideas become invalid when an inequality from level 3 is inserted
casually into level 1. The feedback is right to reject those shortcuts.

I would nevertheless qualify two parts of the corrected map:

* Conflict graphs, clique cuts, odd-cycle cuts, and higher-order relaxations are **not
  dead**. They simply do not belong as replacement rows in the current atom-covering LP.
  They belong in a separate stable-set or configuration relaxation.
* Segment-supported measures are mathematically sound, but they are not as close to a
  drop-in extension of the current exact sweep as the feedback suggests.
  They require a new piecewise-linear intersection-length verifier.

The resulting research program is clearer than either my earlier answer or the feedback
alone:

$$
\boxed{
\text{measure the fractional wall}
\;\longrightarrow\;
\text{improve the witness/resource language}
\;\longrightarrow\;
\text{extract and classify survivors}
\;\longrightarrow\;
\text{capture all survivors near Trump}
\;\longrightarrow\;
\text{close with quantitative rigidity}
}
$$

The attachment appears to contain Grok’s corrected synthesis rather than Gemini’s
complete original analysis, so I am evaluating Gemini’s proposals through the corrected
descriptions given there.

* * *

<a id="source-1-1-the-corrections-i-accept"></a>

#### 1. The corrections I accept

<a id="source-1-the-conflict-sum-row-idea-is-invalid-in-the-present-proof"></a>

##### The conflict “sum-row” idea is invalid in the present proof

The existing theorem selects one inner witness \(P_j\) inside each packed square and
relies on

$$
\operatorname{mass}(P_j)\ge1
$$

**for every selected witness individually**. Only then can it sum over the eleven
disjoint witnesses and obtain

$$
11\le \sum_j\operatorname{mass}(P_j)\le\mu(C)<11.
$$

A constraint such as

$$
\operatorname{mass}(Q_1)+\operatorname{mass}(Q_2)\ge1
$$

does not ensure that the member actually selected by a hypothetical packing has mass
one. The feedback correctly retracts that proposal.
The original proof makes the individual-mass requirement and the final count explicit.

I would therefore retract any implication in my previous answer that pairwise-conflict
information could simply be added as weaker rows to the current covering LP.

But the **configuration-graph idea survives** in a different form, discussed below.

<a id="source-1-independent-per-angle-measures-do-not-share-one-cheap-global-budget"></a>

##### Independent per-angle measures do not share one cheap global budget

The feedback is also correct that a separate measure for every angle bin is not an
unconditional certificate.
All eleven squares might have the same angle, so each angle-specific measure would have
to be capable of covering an entire eleven-square instance on its own.
Summing the norms of hundreds of such measures is not useful.

Angle-dependent resources become valid after one has fixed or bounded the number of
squares in each angle class.
That is a **conditional composition theorem**, not a universal one-body theorem.

A particularly clean conditioned formulation uses one measure \(\mu\) and
class-dependent thresholds \(a_c\):

$$
\mu(P)\ge a_c
\quad\text{for every witness }P\text{ in class }c.
$$

For a branch with composition \((n_c)\), it is impossible whenever

$$
\mu(C)<\sum_c n_ca_c.
$$

That is the form I would prioritize over maintaining many completely separate measures.

<a id="source-1-translating-the-shrunken-square-cannot-increase-its-maximum-size"></a>

##### Translating the shrunken square cannot increase its maximum size

The symmetrization argument in the feedback is convincing: because the containing unit
square is invariant under quarter-turns about its center and is convex, averaging the
four quarter-turned translations of an inscribed \(B\)-square produces a concentric
\(B\)-square of the same size.
Translation therefore cannot improve the largest geometrically guaranteed \(B\).

This modifies, but does not eliminate, my earlier “movable witness” suggestion:

* **Invalid goal:** use a shifted witness merely to make \(B\) larger.
* **Valid goal:** use a shifted or differently shaped witness because it happens to
  capture more certificate mass.

The existential statement

$$
\forall S\ \exists W\subset\operatorname{int}S
\quad\text{such that}\quad \mu(W)\ge1
$$

is still sound and potentially powerful.
Its benefit is measure-theoretic, not an improvement in the maximum inscribed-square
side.

<a id="source-1-full-d_4-symmetry-costs-no-mass-in-the-ideal-problem"></a>

##### Full \(D_4\) symmetry costs no mass in the ideal problem

The proof formally needs only reflection in the diagonal, and the claim document says
so.
But the test family is invariant under quarter-turns, so averaging a feasible measure
over the quarter-turn group preserves feasibility and total mass.
Combining that with diagonal reflection gives a fully \(D_4\)-symmetric optimum.

Thus the feedback is right: removing symmetry is not a theorem-level improvement.
It may change behavior on an incomplete, frozen candidate grid, but that would diagnose
the discretization—not reveal a superior continuous certificate.

Keep \(D_4\) in the final optimization and verifier.

* * *

<a id="source-1-2-one-important-qualification-conflict-cuts-are-still-valuable"></a>

#### 2. One important qualification: conflict cuts are still valuable

The feedback correctly says that pairwise overlap is already represented in the
fractional packing LP. If two exact placements overlap, they share a point \(y\), and
the depth constraint at \(y\) implies

$$
x_p+x_q\le1.
$$

So merely adding edge inequalities to that LP adds nothing.

However, this does **not** mean the point-depth relaxation already describes the convex
hull of actual packings.

For example:

* An odd cycle of mutually conflicting placements has all edge inequalities, but the
  integral inequality

  $$
  \sum_i x_i\le \left\lfloor\frac{k}{2}\right\rfloor
  $$

  is stronger.

* Several pairwise-overlapping rotated squares can form a clique without all sharing one
  common point. Pairwise edge constraints are present, but the clique inequality

  $$
  \sum_i x_i\le1
  $$

  need not be represented by any single point-depth constraint.

* More general rank, web, or semidefinite stable-set inequalities can strengthen the
  fractional relaxation.

There is one subtle correction to the feedback itself: for **fixed exact placements**,
three placements that are pairwise compatible are jointly compatible, because
containment is already fixed and non-overlap is a pairwise property.
Genuine “pairwise feasible but jointly infeasible” hyperedges arise only when vertices
represent **pose cells or placement classes**, so that different pairwise
compatibilities may require inconsistent representatives.

The correct conclusion is therefore:

> Pairwise-conflict information is not a new atom-covering row.
> It is the beginning of a separate integral stable-set or cell-configuration proof.

That is precisely where the conflict-graph part of my previous proposal should live.

* * *

<a id="source-1-3-the-right-mathematical-map"></a>

#### 3. The right mathematical map

Let \(\mathcal W(L)\) be the current family of admissible witnesses: \(B\)-squares at
the chosen net directions inside the side-\(L\) container.

The present one-body covering value is

$$
\tau_1(L)=
\inf_{\mu\ge0}
\left\{
\mu(C_L):
\mu(W)\ge1\ \text{for every }W\in\mathcal W(L)
\right\}.
$$

Its fractional packing dual is

$$
\nu_1(L)=
\sup_{x\ge0}
\left\{
\sum_{W}x_W:
\sum_{W\ni y}x_W\le1\ \text{for every point }y
\right\}.
$$

At minimum, weak duality gives

$$
\nu_1(L)\le\tau_1(L).
$$

The \(3.81\) theorem proves

$$
\tau_1(3.81)<11.
$$

The attachment correctly emphasizes that the method can stop before the true packing
threshold because its fractional packing number can reach eleven while no integral
eleven-square packing exists.

This gives a useful hierarchy:

| Layer | Mathematical object | What a success proves |
| --- | --- | --- |
| 1 | One measure covering every individual witness | A direct lower bound \(s(11)>L\) |
| 1.5 | One-body measures conditioned on angle, position, wall, or role branches | Elimination of a specified class of packings |
| 2 | Integral configuration LP, conflict graph, stable-set cuts, or low-level SDP | Elimination using interactions among several candidate placements |
| 3 | Typed contact/stationarity equations plus interval and algebraic verification | Exhaustion of the final continuous configurations |
| Local endpoint | Quantitative rigidity around Trump | Nothing in the final neighborhood beats \(U\) |

The strategy should advance through these layers deliberately rather than mix their
inequalities.

* * *

<a id="source-1-4-revised-program-a-determine-how-much-life-remains-in-the-current-theorem"></a>

#### 4. Revised Program A: determine how much life remains in the current theorem

This should come first because every later investment depends on the answer.

<a id="source-1-a1-compute-the-true-diagnostic-curve-not-isolated-rungs"></a>

##### A1. Compute the true diagnostic curve, not isolated rungs

For fixed \(B\) and direction net, measure

$$
c(L)=\tau_1(L)
$$

at closely spaced values immediately above \(3.81\), warm-starting from the retained
certificate. The feedback recommends steps of \(0.001\)–\(0.002\), margin sweeps, and
continued column generation rather than jumping directly to \(3.82\). That is sound.

The important output at each \(L\) is not merely a floating objective.
Record:

* the best rigorously verified covering mass;
* the best rigorously verified fractional-packing value;
* the duality gap between them;
* the number and geometry of positive atom orbits;
* the active least-covered placement cells;
* whether site and placement generation have genuinely priced out.

A restricted site set returning exactly \(11.000000\) is not evidence that \(c(L)=11\).

<a id="source-1-a2-make-the-dual-ceiling-mandatory"></a>

##### A2. Make the dual ceiling mandatory

For every serious attempted rung, construct the opposite certificate:

* finitely many rational witness placements;
* nonnegative rational weights;
* exact maximum pointwise depth at most one;
* total weight as large as possible.

If that total reaches eleven, then **no measure of the current \((L,B,\text{net})\) form
can prove the desired bound**. This is the cleanest possible stopping criterion and
should be stored alongside every failed covering attempt.
The feedback correctly elevates this to a first-class proof artifact.

The existing \(6.58\)-type scaled result at \(3.82\) is not such a ceiling.
It only says one proposed dual family was poor after exact depth normalization.

The right algorithm is a double-oracle process:

1. solve the restricted covering LP;
2. find an exactly least-covered placement and add it;
3. solve the restricted fractional-packing LP;
4. find an exactly maximum-depth point and add it;
5. generate new atom sites or placements from the relevant arrangement vertices;
6. repeat until one side certifies \(<11\), the other certifies \(\ge11\), or a
   rigorously bounded gap remains.

<a id="source-1-a3-use-margin-restrictions-only-as-generators"></a>

##### A3. Use margin restrictions only as generators

The Massaccesi-style inset or margin sweep is a good search heuristic.
Restricting atoms to an inset can only make the restricted optimum worse, so:

* a successful restricted certificate is still valid;
* a failed restricted search says nothing about the unrestricted problem.

Use the best margin as a **seed geometry**, then release the restriction and let
unrestricted column generation add wall-near sites.
That agrees with the feedback’s recommendation.

<a id="source-1-a4-improve-seeding-but-do-not-overfit-trump"></a>

##### A4. Improve seeding, but do not overfit Trump

Trump-scaled centers are reasonable candidate sites, but I would use a richer
Trump-induced seed:

* the scaled centers;
* intersections of boundaries of the eleven associated witness-placement regions;
* images of exact wall and contact lines;
* small clouds around active dual arrangement vertices;
* several unrelated lattice and randomized seeds.

Optimal hitting atoms are more likely to lie where several coverage constraints become
simultaneously active than exactly at packed-square centers.

Trump-based seeding is useful, but every run should have non-Trump controls to avoid
merely discovering a dual tailored to the known basin.

<a id="source-1-a5-replace-coarse-rounding-with-exact-basis-recovery"></a>

##### A5. Replace coarse rounding with exact basis recovery

The current cover slack is small enough that rationalization can destroy an otherwise
real improvement. The feedback is right to make rationalization a research item.

At a fixed finite set of atom sites and placement constraints, the LP incidence matrix
is rational—usually binary.
Rather than independently rounding every floating weight:

1. use the floating solver to identify a candidate basic active set;
2. solve that basis exactly over \(\mathbb Q\);
3. check all inactive inequalities exactly;
4. pivot or enlarge the basis if exact feasibility fails.

I would also optimize a proof-margin objective, not merely total mass.
For example, maximize a normalized minimum of

$$
11-\mu(C),\qquad
\min_W\mu(W)-1,\qquad
1-B(1+D).
$$

A certificate with slightly worse floating mass but ten times the exact slack can be
much more valuable.

* * *

<a id="source-2"></a>

## Source 2: `docs/project/reviews/review-2026-09-05-strategy-gpt-56-pro-gemini-grok.md`

Snapshot `4d305597a505`, source lines 470-1112.

<a id="source-2-5-revised-program-b-strengthen-the-additive-witness-theorem-itself"></a>

#### 5. Revised Program B: strengthen the additive witness theorem itself

These approaches remain in the same broad counting tradition, but enlarge either the
witness family or the class of measures.

<a id="source-2-b1-direction-dependent-b_k-and-a-nonuniform-net"></a>

##### B1. Direction-dependent \(B_k\) and a nonuniform net

This is sound and should be attempted early.

For an angular cell \(I_k\) represented by \(\theta_k\), choose \(B_k\) satisfying the
local containment condition

$$
B_k
\max_{\varphi\in I_k}
\bigl(\cos|\varphi-\theta_k|+\sin|\varphi-\theta_k|\bigr)
<1.
$$

Then require every admissible \(B_k\)-square at direction \(\theta_k\) to have mass at
least one.

This permits:

* very fine angular spacing and \(B_k\) extremely close to one near important angles;
* coarser spacing and smaller witnesses in unimportant regions;
* direct optimization of net density using dual sensitivity.

The net and \(B_k\) assignments must be closed under the relevant \(D_4\) action.
The feedback correctly identifies adaptive \(B_k\) and clustered directions as valid
improvements.

I would not cluster solely because the verifier reports one minimizing direction at
zero; the retained certificate may have many tied minima.
Use:

* active-constraint density by angle;
* reduced-cost sensitivity;
* Trump’s \(0^\circ\) and \(40.1819^\circ\) classes;
* adaptive refinement wherever the exact coverage margin is smallest.

<a id="source-2-b2-replace-the-inscribed-square-by-a-better-angle-cell-kernel"></a>

##### B2. Replace the inscribed square by a better angle-cell kernel

This is an extension I would add to both my earlier strategy and the feedback.

For each angle cell \(I_k\), choose a fixed convex witness \(K_k\) that is guaranteed to
lie inside every unit square whose orientation belongs to \(I_k\), after suitable
centering and rotation.

The largest common kernel is the intersection of the relevant rotated unit squares.
It need not be a square and may not have a simple polygonal boundary, but one can use a
certified rational polygonal inner approximation.

Then require

$$
\mu(c+R_{\theta_k}K_k)\ge1
$$

for every admissible translation \(c\).

The ordinary \(B_k\)-square is only one possible inner approximation.
A polygonal kernel can be strictly larger as a set and therefore easier to hit with a
fixed measure. For point atoms, the exact verifier generalizes from an arrangement of
center rectangles to an arrangement of reflected copies of \(K_k\).

This is probably the most promising **same-theorem geometric improvement** because it
attacks the angular shrink tax directly without invoking an invalid translated-square
argument.

<a id="source-2-b3-segment-supported-measures"></a>

##### B3. Segment-supported measures

A nonnegative measure supported on line segments is valid while the witnesses remain
strictly inside the original squares.
The selected witnesses are then disjoint as sets, so no segment mass can be counted
twice.

The potential benefits are:

* compactly representing what would otherwise require dense rows of atoms;
* reproducing classical unavoidable-line arguments;
* making the dual more regular as the numerical optimum approaches a continuum.

But it is not a simple binary “segment hit” test.
The mass of a square is the weighted length of its intersection with each segment.
As the square center moves, that length is piecewise affine or piecewise algebraic.
Exact verification therefore needs:

* a finite arrangement of all combinatorial intersection events;
* exact formulas on each cell;
* minimization of the summed piecewise functions.

I regard this as credible, but behind adaptive \(B_k\), exact basis recovery, and
angle-cell kernels.

<a id="source-2-b4-full-size-boundary-null-area-measures"></a>

##### B4. Full-size, boundary-null area measures

This remains one of the strongest high-upside ideas from my previous answer and is not
displaced by the feedback.

Let \(\rho(x,y)\ge0\) be an integrable density and define

$$
\mu(A)=\int_A\rho(x,y)\,dx\,dy.
$$

Because every square boundary has \(\mu\)-measure zero, no shrink is needed.
If

$$
\int_{C_L}\rho<11
$$

and every full unit square \(S\subset C_L\), at every orientation, satisfies

$$
\int_S\rho\ge1,
$$

then eleven interior-disjoint unit squares are impossible.

This removes:

* the \(B<1\) shrink tax;
* the finite-net containment loss;
* atomic boundary complications.

A practical basis might use rational piecewise-constant, bilinear, or low-degree
polynomial densities on a \(D_4\)-symmetric subdivision.
The minimum integral over a unit-square pose is a three-variable problem in
\((x,y,\theta)\), much smaller than the full eleven-square configuration problem, and
could be certified by interval branch-and-bound.

This should be tested both below \(U\) and at \(U\).

<a id="source-2-b5-existential-witness-certificates"></a>

##### B5. Existential witness certificates

The correct formulation is

$$
\forall\text{ unit-square poses }S,\qquad
\max_{\substack{W\in\mathcal L\\W\subset\operatorname{int}S}}
\mu(W)\ge1,
$$

where \(\mathcal L\) is a library of possible witnesses.

Possible witness options could differ by:

* offset;
* orientation;
* size;
* polygonal shape;
* membership in a finite menu.

This is strictly weaker than requiring **every** admissible \(B\)-square to be heavy, so
it can pass a universal-cover wall.

The difficulty is logical rather than geometric: it is a robust \(\forall S\,\exists W\)
statement. A sound implementation would require a disjunctive interval verifier or a
finite witness-selection certificate over cells in unit-square pose space.

I would pursue this after the exact ceiling demonstrates that the universal witness
formulation has genuinely stalled.

* * *

<a id="source-2-6-a-potentially-decisive-one-body-shortcut-a-sharp-equality-certificate-at-trumps-value"></a>

#### 6. A potentially decisive one-body shortcut: a sharp equality certificate at Trump’s value

Let

$$
U=3.877083590022814\ldots
$$

be Trump’s exact side.
The repository represents the configuration in an exact degree-eight number field and
gives the exact algebraic relation for \(U\).

Search for an absolutely continuous measure \(\mu\) on \(C_U\) satisfying

$$
\mu(C_U)=11
$$

and

$$
\mu(S)\ge1
\quad\text{for every unit square }S\subset C_U.
$$

Any packing of eleven unit squares in \(C_U\) would then force equality everywhere:

* every packed square has mass exactly one;
* the union of their interiors captures all of \(\mu\);
* every square belongs to the equality set of the dual inequality.

If the only compatible eleven members of that equality set are the Trump squares, up to
\(D_4\) and relabeling, then a packing in a smaller container is impossible: embedded
into \(C_U\), it would create a different equality configuration.

This is a direct optimality-and-uniqueness proof by complementary slackness.

A productive way to search for it is **inverse dual design**:

1. choose a \(D_4\)-symmetric density basis;
2. impose integral exactly one on Trump’s eleven squares;
3. impose first-derivative stationarity of those integrals under the allowable pose
   perturbations;
4. minimize total mass or maximize the global unit-square coverage margin;
5. certify the resulting semi-infinite inequalities.

This is elegant and potentially much shorter than a global contact enumeration.
But it has a sharp kill test:

> If the full-unit-square fractional packing value at \(U\) is rigorously greater than
> eleven, no one-body equality measure can work.

So a full-size primal/dual pilot at \(U\) should precede major investment.

* * *

<a id="source-2-7-revised-program-c-use-the-certificate-as-a-structural-classifier"></a>

#### 7. Revised Program C: use the certificate as a structural classifier

This is where the current result may matter more than its raw numerical endpoint.

Suppose at some \(L>3.81\) a covering measure has total mass

$$
M=11+\varepsilon
$$

and still covers every relevant witness with mass at least one.
If an eleven-square packing existed, its eleven disjoint witnesses would satisfy

$$
1\le\mu(P_i)\le1+\varepsilon
$$

and their union would omit at most \(\varepsilon\) of the total mass.

Thus every square in the hypothetical packing must lie among the **near-tight witness
placements**.

The feedback’s tight-cell census is exactly the right first diagnostic.

<a id="source-2-program-c-step-1-near-tight-cells-and-role-clusters"></a>

##### Program C, Step 1: Near-tight cells and role clusters

For several values of \(\varepsilon\), enumerate exactly the pose cells satisfying

$$
\mu(P)\le1+\varepsilon.
$$

Then cluster them by:

* angle;
* center region;
* wall proximity;
* which heavy atoms they contain;
* similarity to one of Trump’s eleven roles.

The hoped-for structure is not merely “few cells.”
It is something like:

* six clusters corresponding to near-axis roles;
* five clusters corresponding to the tilted block;
* an exact-cover constraint forcing one selection from each;
* only one compatible assignment pattern.

That would convert the fractional certificate into a global capture mechanism.

<a id="source-2-program-c-step-2-exact-cover-and-hall-type-forcing"></a>

##### Program C, Step 2: Exact-cover and Hall-type forcing

If certain atoms have weight greater than \(\varepsilon\), every such atom must lie in
one of the eleven selected witnesses, because at most \(\varepsilon\) total mass may
remain uncovered.

This creates a finite incidence problem:

* heavy atoms on one side;
* near-tight witness cells on the other;
* a witness cell covers a known subset of atoms.

Use exact-cover, matching, and Hall-type deficiencies to force roles or eliminate
branches. This is substantially stronger and more structured than enumerating arbitrary
center tiles.

<a id="source-2-program-c-step-3-angle-composition-certificates"></a>

##### Program C, Step 3: Angle-composition certificates

Partition orientations into \(D_4\)-closed bins and solve class-threshold programs for
each possible composition.

The first coarse objective should be to prove that every survivor near \(U\) has a
composition close to:

$$
6\text{ near-axis squares}
\quad+\quad
5\text{ squares near }40.18^\circ.
$$

Stromquist’s \(0^\circ/45^\circ\) theorem should be treated as an already closed branch,
not re-proved expensively.
The feedback is right on this point.

Useful intermediate theorems include:

* at least two squares lie outside a narrow near-axis class;
* at least four or five lie in a specified tilted range;
* all packings with at most two tilted squares require side \(>U\);
* all two-orientation-class packings require side at least \(U\).

These would be real structural results even before the full problem is closed.

<a id="source-2-program-c-step-4-boundary-support-signatures-not-just-wall-contact-counts"></a>

##### Program C, Step 4: Boundary-support signatures, not just wall-contact counts

The feedback proposes splitting by how many squares touch each wall.
That is useful but probably too coarse.

I would instead branch on the **support signature**:

* which square supplies the left, right, top, and bottom supports;
* whether each support is at an edge or corner;
* the angle bin of each supporting square;
* which contact chains transmit force between opposite walls.

At a side-minimizing packing, all four outer directions must be supported.
Once the identities and angle bins are fixed, much of the center geometry becomes a
linear or interval-linear system.

Projection chains are especially valuable.
For a fixed contact/separating-axis branch, a dual LP often produces a wall-to-wall
inequality whose coefficients can be interpreted as a weighted chain of widths.
These may be the human-readable geometric inequalities hidden inside the numerical
solver.

<a id="source-2-program-c-step-5-boxed-conditional-certificates"></a>

##### Program C, Step 5: Boxed conditional certificates

Once a square is known to occupy a pose box \(b\), exploit the region common to every
square in that box. The other ten squares must avoid that guaranteed occupied region.
A measure optimized only over the remaining admissible witness placements may be
substantially cheaper.

This is mathematically natural but technically expensive:

* the admissible center region becomes nonconvex;
* the broken global symmetry requires the full quarter-turn direction range;
* multiple boxed squares create unions of excluded regions;
* the exact verifier and both optimization oracles must understand the same branch
  definition.

The feedback correctly places this after cheaper class and census tests rather than as
the immediate next implementation.

Calibration on a known hand-proved branch, such as one from \(n=13\), remains important.

* * *

<a id="source-2-8-revised-program-d-configuration-level-integrality"></a>

#### 8. Revised Program D: configuration-level integrality

Once the one-body relaxation reaches eleven, the natural next object is not a more
elaborate sum-row. It is the integral packing problem on a reduced set of candidate
poses.

<a id="source-2-d1-a-certified-pose-cell-conflict-graph"></a>

##### D1. A certified pose-cell conflict graph

After the near-tight census, partition the surviving pose space into small certified
cells.

Create a graph in which an edge means:

$$
\text{every placement in cell }A
\text{ overlaps every placement in cell }B.
$$

An actual packing requires eleven cells with no such robust-conflict edge, after
accounting for multiplicities and subdivisions.

The graph should be a conservative outer approximation:

* a proven conflict gives an edge;
* uncertainty gives no edge and triggers subdivision;
* absence of an edge never claims actual compatibility.

Then compute or certify that the graph has no independent set of size eleven.

<a id="source-2-d2-integral-cuts-that-really-add-information"></a>

##### D2. Integral cuts that really add information

On this graph or on a selected finite family of exact placements, add:

* clique inequalities, including cliques lacking a common point;
* odd-cycle and odd-hole inequalities;
* rank inequalities;
* symmetry and angle-composition equations;
* wall-support constraints;
* exact-cover constraints from heavy atoms;
* no-good cuts for cell combinations shown infeasible by an interval subsolver.

These are valid because they act on the **selection variables**, not on the atom masses.

A low-level Sherali–Adams or Lasserre/SDP relaxation becomes plausible only after the
candidate pose set has been reduced dramatically.
Starting with an SDP over the entire continuous 34-dimensional problem would be far less
credible.

<a id="source-2-d3-cell-hyperedges"></a>

##### D3. Cell hyperedges

For exact placements, pairwise compatibility is sufficient.
For cells, however, one can have:

* each pair of cells admitting some compatible representatives;
* no single triple of representatives being jointly compatible.

Such a triple can be stored as a certified hyperedge or no-good clause.
The distinction between exact placements and existential cells is important.

* * *

<a id="source-2-9-revised-program-e-typed-stationary-contact-analysis"></a>

#### 9. Revised Program E: typed stationary contact analysis

This remains the most credible final global engine.

The feedback is right that one should not enumerate all unlabeled planar graphs.
The meaningful objects are typed incidences:

* square–wall edge or corner support;
* edge–edge contact;
* corner–edge contact;
* the active separating axis and order;
* equal- or unequal-orientation relations;
* the support of a nonnegative equilibrium stress.

<a id="source-2-e1-enumerate-stationary-backbones-not-all-contact-graphs"></a>

##### E1. Enumerate stationary backbones, not all contact graphs

A better packing, if one exists, has a side-minimizing representative.
Such a representative must satisfy a Fritz–John or KKT-type stationarity condition on at
least one nonsmooth branch.

So enumerate only typed incidence structures capable of carrying a nonnegative stress
balancing the container-side objective.

This should prune far more aggressively than enumerating arbitrary touching graphs.

Rattlers and zero-multiplier contacts must be allowed.
The correct object is the load-bearing backbone together with any remaining feasible
squares, not an assumption that all eleven squares form one rigid contact graph.

<a id="source-2-e2-eliminate-centers-with-linear-programming"></a>

##### E2. Eliminate centers with linear programming

For fixed angles and fixed separating-axis choices, the containment and non-overlap
constraints are linear in:

* the 22 center coordinates;
* the container side \(L\).

Therefore branch primarily on:

* angle intervals;
* active support features;
* separating-axis choices.

At each node, solve the center problem as an LP. Its dual supplies:

* a rigorous lower bound on \(L\);
* a Farkas certificate of infeasibility;
* a stress-like explanation of the obstruction.

Do not subdivide the 22 center coordinates unless the LP structure genuinely leaves
ambiguity.

<a id="source-2-e3-use-a-lazy-satlpinterval-architecture"></a>

##### E3. Use a lazy SAT/LP/interval architecture

There are too many possible separating-axis choices to enumerate eagerly.

Use a solver architecture analogous to SAT modulo theories:

1. the discrete layer proposes only the contact and separation choices currently needed;
2. the LP/interval layer checks them;
3. an infeasible branch returns a compact conflict clause;
4. transitivity, wall ordering, and impossible cycles propagate further choices;
5. large-gap pairs remain unbranched.

Every closed node should carry a small checkable certificate: LP dual, exact conflict,
interval exclusion, or local rigidity reference.

<a id="source-2-e4-exactify-only-the-final-rigid-leaves"></a>

##### E4. Exactify only the final rigid leaves

At a surviving rigid branch, use

$$
t_i=\tan(\theta_i/2)
$$

to rationalize sine and cosine.
The stationary and contact equations become polynomial after denominators are cleared.

Then:

* solve numerically to locate all roots;
* certify root completeness with interval Newton or Krawczyk methods;
* reject roots violating inactive inequalities;
* derive minimal polynomials or resultants for surviving side values;
* compare them exactly with Trump’s \(U\), using root isolation and Sturm methods.

The exact algebraic value of Trump’s construction is extremely useful here, but only
**after** the branch list is finite.
Its degree-eight polynomial does not by itself create a numerical exclusion zone around
\(U\).

* * *

<a id="source-2-10-quantitative-trump-rigidity-remains-the-indispensable-endpoint"></a>

#### 10. Quantitative Trump rigidity remains the indispensable endpoint

The repository already has a strong qualitative local result: all 128
derivative-distinct fixed-side branches have zero linearized cone, with full rank and
strictly positive exact stresses; a finite-branch argument upgrades this to local
isolation and strict local side optimality in the anchored chart.
What it lacks is an explicit neighborhood radius.

The next local theorem should produce an explicit \(\rho>0\) such that every feasible
pose within distance \(\rho\) of the Trump orbit has side at least \(U\), with equality
only at Trump.

There are two practical ways to obtain it.

<a id="source-2-analytic-stress-modulus"></a>

###### Analytic stress modulus

For each branch, compute:

* a minimum first-order violation margin on the unit sphere;
* exact or interval Hessian bounds;
* the least inactive-constraint gap;
* Lipschitz bounds for inactive contacts;
* the effect of varying the side coordinate.

Combine these into a certified radius and local objective-growth bound.

<a id="source-2-direct-interval-neighborhood"></a>

###### Direct interval neighborhood

Build a box around Trump in the full pose–side chart and use:

* the known branch inventory;
* interval enclosures of every active inequality;
* interval Newton/Krawczyk tests for stationary systems;
* exact stress signs;
* subdivision only where branch switching remains possible.

This may produce a better practical radius than a pessimistic closed-form Taylor
estimate.

A radius of \(10^{-2}\) in a normalized pose chart would be enormously useful.
A radius below \(10^{-7}\) might be mathematically valid but too small for the global
classification to reach.
So the numerical size of \(\rho\) is a major strategic gate.

* * *

<a id="source-2-11-the-exact-closing-from-both-ends-theorem"></a>

#### 11. The exact “closing from both ends” theorem

The final proof should have this shape.

Let \(\mathcal T\) be the finite orbit of Trump’s packing under container symmetries and
relabeling.

<a id="source-2-global-capture"></a>

##### Global capture

Prove that every side-minimizing packing with

$$
3.81\le L\le U
$$

lies within distance \(\rho\) of \(\mathcal T\).

The proof tree may use:

* one-body certificates at coarse nodes;
* class and composition certificates;
* near-tight exact-cover forcing;
* boxed conditional certificates;
* conflict-graph and stable-set cuts;
* LP and interval contact branches;
* smaller-\(n\) exact packing bounds as subproblem cuts.

<a id="source-2-local-closure"></a>

##### Local closure

Prove that every feasible pose within distance \(\rho\) of \(\mathcal T\) has

$$
L\ge U.
$$

Together they prove

$$
s(11)=U.
$$

A crucial refinement to the phrase “residue covering” is that the complement of a Trump
neighborhood is a property of an eleven-square configuration.
It cannot ordinarily be covered by one unconditional measure on individual square poses.
It must be decomposed into finitely many cases—angle deviations, role mismatches,
position boxes, support signatures—or handled by a configuration-level dual.

Thus the final method is a proof tree, not a single miraculous measure.

* * *

<a id="source-2-12-maintain-a-parallel-falsification-lane"></a>

#### 12. Maintain a parallel falsification lane

A rigorous proof program should continue trying to disprove Trump optimality.

The same machinery can search rather than only exclude:

* complementarity MINLP over restricted angle profiles;
* stationary typed-contact systems;
* smooth overlap penalties with homotopy;
* random and adversarial seeds far from Trump;
* three- and four-orientation-class packings;
* symmetry-broken boundary-support signatures.

Any numerical packing below \(U\) should immediately be:

1. robustified;
2. interval-verified;
3. exactified if rigid;
4. used as a new target for the global proof architecture.

Especially valuable intermediate searches are:

* six axis-aligned plus five common-tilt squares, arbitrary contacts;
* arbitrary \(6+5\) two-orientation-class packings;
* arbitrary two-orientation-class packings;
* packings with the same support signature but a different contact graph.

These are simultaneously counterexample searches and tractable restricted optimality
theorems.

* * *

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
