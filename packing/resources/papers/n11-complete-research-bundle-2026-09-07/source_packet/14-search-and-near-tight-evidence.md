# Search, Near-Tight Cells and What Failures Establish

Tutorial mechanisms are combined with exact census and seed-release outcomes. Numerical failure is not a global exclusion, and the census's small percentage does not imply a small compatibility problem. Current implementation status is reconciled in file 02.

## Qualifications to the Frozen Tutorial

A feasible exact fixed-angle LP solution remains in its selected separation cell. Its canonical greatest-gap label may change when read back. Repeating until labels stabilize computes an algorithm-conditioned local result; it does not establish a unique, globally minimized function of angles. Starting-cell dependence and multiple fixed points remain possible.

Jacobian nullity describes infinitesimal motions. Identifying it with the dimension of nonlinear feasible families requires regularity and suitable constant-rank assumptions. Singular inequalities can have nonzero infinitesimal nullity at an isolated feasible point.

<a id="source-1"></a>

## Source 1: `TUTORIAL.md`

Snapshot `4d305597a505`, source lines 381-571.

<a id="source-1-3-cells-basins-and-two-traps"></a>

#### 3. Cells, Basins, and Two Traps

Both traps below arose in retained experiments and changed the project’s definitions.

<a id="source-1-the-quench-map"></a>

##### The quench map

Borrowed from Stillinger and Weber’s *inherent structure* decomposition: the **quench
map** sends a configuration to the pose that a deterministic refinement returns.
A **basin**, or **point-basin** where the distinction matters, is the preimage of one
returned pose. The atlas ultimately wants a coarser, mathematically stable relation on
connected terminal components; the current point keys do not yet provide it.

A quench map is a general notion; this project uses one particular algorithm, and the
specifics matter for what follows.
It has two nested loops, not one.

**The inner loop makes the side a function of the angles.** Given a pose, the cell is
*read off it*: for each pair, take the candidate axis of greatest separation, together
with the sign saying which square is low.
That cell defines the linear program of [§2](16-mathematical-background-and-literature.md#source-2-2-the-configuration-space), which is
solved in the `2n + 1` centre-and-side variables.
But the solution may lie in a *different* cell from the one it was solved in, so its
value is an upper bound that depends on where the caller started.
That path dependence would make `s(θ)` ill-defined and leave any angle search optimising
a moving target. So the loop re-reads the cell from the solution and re-solves until the
cell it reads back is the cell it was given—a **cell fixed point**. It can also stop
unsettled, with a typed reason, and an unsettled result is exploratory data rather than
a converged endpoint.

**The outer loop moves the angles.** It works one angle class at a time, minimising each
by golden-section bracketing inside a window that narrows only when a whole sweep fails
to improve.
No derivative is used—deliberately, for the reason [§4](14-search-and-near-tight-evidence.md#source-1-4-the-corner) gives.
A final optional pass brackets each of the `n` angles individually, to test whether a
class-converged pose is genuinely stationary or an artifact of the tolerance that
decided which angles count as one class.
The sweeps stop when none improves, or a tolerance, sweep cap, or wall-clock budget is
reached.

So: **read the cell, solve to a cell fixed point, bracket the angle classes, repeat.**

The knobs are real—a class-merge tolerance, a window schedule, budgets—and that is
exactly why a basin defined by this map inherits them.
It is also why the free-angle pass exists.
Note too that changing the refiner changes the map, and therefore changes what “basin”
refers to: swapping angle descent for class bracketing, which [§4](14-search-and-near-tight-evidence.md#source-1-4-the-corner) does,
is a different quench and a different decomposition.

Two derived words carry the project’s central diagnostic:

- **Polish:** refinement *within* the basin you are already in.
  This is what the quench does, and all it does.
- **Exploration:** reaching a *different* basin.
  Nothing in the toolkit does this reliably at `n = 11`.

A gap therefore decomposes into a **polish failure** (right region, weak refinement) or
an **exploration failure** (wrong region, and refinement cannot help).
Which one a number represents **cannot be read off the number**; you establish it by
running the refiner and seeing whether the gap moves.

<a id="source-1-trap-1a-fixed-angle-cell-solve-is-not-a-basin"></a>

##### Trap 1—a fixed-angle cell solve is not a basin

A cell fixes only the discrete separating axes and orders.
The **fixed-angle LP subproblem** fixes both a cell and an angle vector; a basin does
neither, because the quench may change angles and cross cells.
A configuration can therefore sit at exactly its fixed-angle cell optimum and still be
far from its quench endpoint, with all the remaining gap in the angles and none in the
centres.

**A fixed-angle solve that stops improving has exhausted only the variables it may move;
it has not converged to a local optimum of the full problem.** Watching it flatten and
concluding “wrong basin” is exactly what the *right* basin looks like when the residual
is angular.

An agent built a fixed-angle probe, called it “the quench”, and **retracted a correct
finding** when it stalled ([D-029 (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/defects.md)). On one `n = 10` start: the annealer
output and the fixed-angle solve agree to every digit at `+5.6440e-04`, and the full
quench with its angle half reaches `+4.4409e-16`.

The renderer guide retains the
[shared-scale Göbel source-return diagnostic (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/atlas/rendering/README.md#n--10-numerical-comparison):
the start is close but not settled, while the full quench returns to the proved-side
geometry.

<a id="source-1-trap-2a-point-basin-need-not-be-a-terminal-component"></a>

##### Trap 2—a point-basin need not be a terminal component

A deterministic quench still returns an individual pose.
The problem is that its local optimum can lie on a connected terminal family, so
point-preimages split the component-level object the programme actually wants to count.

At `n = 3` the exact side-2 optimum contains a connected **sliding family**: centres
`(1/2,1/2)`, `(3/2,1/2)`, and `(t, 3/2)` for `t ∈ [1/2, 3/2]`. One connected optimal
component, infinitely many distinct coordinate keys.
The quench lands wherever in the flat region it happened to enter, and every symptom
mimics a real discovery—distinct coordinates, distinct keys, two rows in the store—while
the side agrees exactly and, along the family’s open stratum, so does the contact
certificate (the wall endpoints carry a different one).

The object that survives this trap has been computed exactly, and the figure below is
its map. `F₃(2)` is the space of *all* packings of three unit squares in the side-2
container—and since `s(3) = 2` is proved, that is the complete optimum space, not a
sample of it. With the squares labelled, the space is two disjoint circles, each a cycle
through twelve discrete states, cross-checked against the published hard-squares
computation of the same space.
Forgetting the labels—quotienting by the symmetric group `S₃`—merges the two circles
into one: relabelling was separating configurations the mathematics does not
distinguish. Quotienting also by the container’s eight symmetries `D₄` folds that circle
to the closed interval `λ ∈ [0, 1/2]`, where `λ = min(t − 1/2, 3/2 − t)` is the slider
parameter above with the reflection `t ↔ 2 − t` divided out.
Three strata remain: the corner pose at `λ = 0`, the generic slide, and the centred pose
at `λ = 1/2`.

[The exact quotient map of optimal configurations for three unit squares. (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/atlas/n-003-optimal-moduli.svg)

*Each quotient stage kills one wrong identity—relabellings and container symmetries are
not new basins—and the interval kills the rest: four exact sample poses with four
distinct geometric keys, two contact signatures, and three strata are one connected
component.*

That is why this object is a permanent known-answer control rather than an illustration.
A frozen component-assignment policy is accepted only if it recovers this interval, and
the `n = 4` quotient point, exactly while rejecting every shortcut:
[exp-032 (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-032-h-021-terminal-component-controls.md)
proposed geometric keys, contact signatures, finite samples, labelled states, and
floating-point matches as component identities, and all seven such mutations were
refused. Passing that gate is what admitted the bounded `n = 5` connectivity work below,
and this map is the only exact ground truth behind open question 1 in
[§8 (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/TUTORIAL.md#8-what-is-known-and-what-is-not).

The same phenomenon appears at `n = 5`. After one symmetry action and relabelling, two
retained poses with different coordinate keys lie on one exact continuous family in a
fixed-angle cell.
An apparent escape direction is ruled out, but the remaining directions
and global connectivity are still open.
The constrained-optimality language needed for the sharper statement is introduced in
[§5](16-mathematical-background-and-literature.md#source-3-contact-graphs-stationary-branches-and-rattlers).

The project’s term for this is a **terminal family**, and its definition is deliberately
strict: local dimension is the nullity of the appropriate independent active-constraint
Jacobian, after quotienting symmetries and accounting for inequalities and stratum
changes. **Raw contact counts cannot supply that rank**—contacts may be dependent, one
contact description may encode several scalar conditions, and angles and cells may
change along a motion.
Subtracting contacts from variables is not a rigidity calculation, and the project has a
logged defect for having done it.

<a id="source-1-the-generalized-lesson-learned-twice"></a>

##### The generalized lesson, learned twice

- **First version.** Whatever defines a basin must be independent of the *search’s* own
  knobs. A quench that merged nearby angles would make “basin” depend on a merge
  tolerance.
- **Second version.** It must also be independent of the *representation’s* knobs, and
  must not presume a structure—discreteness—that the mathematics does not supply.

Both have the same cause as Trap 1: the representation fixes more than the mathematics
does. The first lesson was documented; the same argument implied the second, but it was
not documented.

<a id="source-1-4-the-corner"></a>

#### 4. The Corner

`φ(a)` is not smooth at its minimum.
Refined finite differences give one-sided rise rates of about `0.1747` to the left and
`0.384` to the right per radian, stable over five decades.
In the conventional signed derivative, these are about `−0.1747` and `+0.384`. Two
independent LP formulations agree: `0.1747`/`0.3839` at a ratio of `2.1973`, and
`0.1747`/`0.3841` at a ratio of `2.198`. **The derivative does not vanish at the
optimum; it jumps.**

**Why.** Where the LP’s optimal *basis* is locally constant, `φ` is smooth and its
derivative reads off that basis.
A corner occurs where the optimal basis switches as the angle crosses `a*`. Because a
basis is only a subset of the active rows, a basis switch alone does not show that the
full active-contact set changed.

**What it bought.** Replacing smooth descent with a **bracketing search over merged
angle classes**—a method that tolerates non-smoothness—and changing nothing else took
`n = 5` from descent’s `3.2e-08` to `2.2e-15`, and `n = 10` from `4.5e-03` to `1.3e-15`.
Measured from the annealer output both quenches start from, that is `3.4e-08` and
`5.3e-03` respectively.
All four figures are medians over the five tested seeds; the worst `n = 5` seed stays at
`6.2e-08`.

**What it did not buy.** Nothing at `n = 11`, where the same substitution moves the
annealer’s `8.8e-02` only to `6.3e-02`. And it is *not* a theorem that derivative-free
methods must fail: Powell and Nelder–Mead did worse than descent on the tested starts,
in this implementation, which is method-selection evidence and not an impossibility
result. The kink also lives on a one-dimensional slice, so it is **not** by itself a
rigidity proof for the full packing.

The synopsis presents this measurement-to-method chain as a full worked example.

<a id="source-2"></a>

## Source 2: `TUTORIAL.md`

Snapshot `4d305597a505`, source lines 907-1028.

<a id="source-2-7-how-the-search-is-approached-and-why"></a>

#### 7. How the Search Is Approached, and Why

There are two layers: the catalogue of everything anyone has ever used, and the strategy
this project actually adopted.

<a id="source-2-the-catalogue"></a>

##### The catalogue

Twenty search strategies in four families, each cited by the hypotheses that use them,
so the ledger can report which whole families remain untried:

- **Constructive:** grids, hand geometric insight, `45°` tilted families, diagonal
  strips, strip-plus-L augmentation, rational-slope tilts, composition and
  self-similarity, parametric families, asymptotic border constructions.
  *Every record before 2000 came from here.*
- **Stochastic search:** simulated annealing (the current workhorse), billiard and
  inflation, basin hopping, nonlinear programming, SAT/CP, branch and bound over contact
  classes, evolutionary methods.
- **Exact refinement:** fixing a typed contact structure and solving the polynomial
  system, rigidity-guided enumeration, interval-verified local optima.
- **Workflow:** the human-computer loop against a public record table, which is how the
  tables actually advance.

A parallel catalogue of thirty proof strategies in six families covers the lower-bound
side.

<a id="source-2-the-strategy-why-pointing-should-beat-scaling"></a>

##### The strategy: why pointing should beat scaling

> **A validated map of terminal components is the intended deliverable, and records are
> corollaries.**

The reasoning: annealing-class methods sample basins roughly in proportion to their
**volume at the sampling temperature**, so they find the funnel whose *entropy* wins,
not the funnel whose *optimum* wins.
The canonical precedent is the 38-atom Lennard-Jones cluster, whose global minimum sits
at the bottom of a narrow funnel beside a broad one that captures almost every unbiased
run.

If that transfers, scaling the same proposer merely multiplies samples against a small
fixed probability, and the response is to point search rather than enlarge it.

**That reasoning is a precedent, not a measurement.** It enters as a reason to expect a
direction to be productive, never as a fact about this landscape.
Contact counts do not establish rigidity; rigidity does not establish rare attraction;
another author’s basin counts are a property of *their* proposer, not of the problem.
The premise is registered as a hypothesis with a kill criterion—if record basins turn
out to be hit at rates comparable to the modal basin, the cartography program stands
down and the campaign reverts to throughput.

<a id="source-2-steering-keep-the-loss-change-what-you-keep"></a>

##### Steering: keep the loss, change what you keep

The obvious response to “the objective does not reward what we want found” is to reshape
the objective. Two things are wrong with it.

Reshaping the objective creates two problems.
First, a naive contact reward favours grid-like arrangements, the opposite of the
intended direction. Note the shape of the trap, because it recurs: the grid is
high-contact *and common*; the record is high-contact *and rare*. **Any single scalar
they share cannot separate them.**

**A reshaped loss can change the minimizers** unless equivalence is proved.
Lexicographic tie-breaking, potential shaping, or an auxiliary term that vanishes on
exactly the same minimizers may preserve the target, but that preservation becomes a
separate proof obligation rather than an intuition.

The alternative keeps the objective and changes *what is retained*: a quality-diversity
archive keyed by structural descriptors.
In exploration mode, a taboo on canonical keys can avoid spending proposal budget on a
named endpoint. In measurement mode, repeated hits are essential data for
proposer-conditioned frequency and uncertainty, so they must be counted rather than
suppressed. The intelligence and the risk concentrate in descriptor design: descriptors
must come from verified canonical data rather than raw floats, must be axes of
*mechanism*, and must be combined so as to separate the grid funnel from oblique
structure.

<a id="source-2-relaxation-ladders-turn-rare-event-search-into-path-following"></a>

##### Relaxation ladders: turn rare-event search into path-following

Embed the hard instance in a one-parameter family whose far end is easy, then track
solutions along the parameter instead of searching for them cold.

| Ladder | Parameter | Easy end | What to watch |
| --- | --- | --- | --- |
| container inflation | slack `δ` in side `s* + δ` | large `δ`: hypothesized broader accessibility | basin splits and merges; the first observed or certified `δ` at which a named target is reachable |
| superdisk | exponent `p` in `|x|^(2p) + |y|^(2p) <= 1` | `p = 1`: circles, orientation-free; `p -> infinity`: the square limit | where orientation symmetry breaks |
| boundary layer | frozen grid bulk | the pure grid | whether a sheared band re-synchronizes |

Container inflation is the primary one, and it can pay three ways from one computation:
a method that may *walk into* regions direct sampling never hits, the barrier scale a
map wants anyway, and a scalar hardness measurement.
That scalar becomes well posed only after naming the proposer, target component or
event, success threshold, and whether the quantity is an observed branch-entry scale or
a certified clearance barrier.
Boundary-layer reduction is strictly a *reduction*, not a relaxation: the slice may
exclude the true optimum, and that risk is stated rather than hidden.

<a id="source-2-calibration-must-match-mechanism-not-just-difficulty"></a>

##### Calibration must match mechanism, not just difficulty

The proved cases used as positive controls, `n = 5` and `n = 10`, are both `45°`
mechanisms (the other proved small cases are plain grids).
They validate **machinery**, not **strategy**—an engine can take them to machine
precision and remain structurally blind to the irrational oblique tilt that `n = 11`
demands and that no proved case exercises.

So record-*finding* needs its own targets, chosen by mechanism: the nearest case whose
record uses genuinely oblique structure, the target at small inflation (which gives a
graded progress metric along a tracked branch, without assuming continuity across
bifurcations), and basin-entry tests that separate “search cannot find the region” from
“the refiner cannot hold it”—two failures with identical symptoms and different fixes.

The result that most sharpened this: the annealer, pointed at `n = 17`, reported `5.0`—
the trivial grid—on every one of five binary64 screening seeds
([exp-011 (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-011-h-020-n17.md)),
against Bidwell’s 1998 record of `4.6755`. Because that miss is at a second, independent
cell whose record needs oblique structure, the failure is not specific to `n = 11`;
whether it covers every oblique target is an inference the registry states as such, not
a theorem.

<a id="source-2-near-misses-are-the-data"></a>

##### Near-misses are the data

A serious campaign produces thousands of non-record endpoints.
They are not waste—they are the map, the training set for descriptors, the sample for
structure-versus-rarity laws, and the denominator for any coverage claim.

<a id="source-3"></a>

## Source 3: `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-063-h-065-n11-near-tight-cell-census.md`

Snapshot `4d305597a505`, source lines 123-end.

<a id="source-3-exp-063--four-per-cent-and-still-a-search"></a>

### exp-063 — Four Per Cent, and Still a Search

`X-014` asked for this census as its third measurement and named the reading it wanted:
a tight set at `epsilon = 1/20` of a few hundred cells clustered around a few dozen
positions makes Corollary 1a’s exact cover a *check*; a fat one makes it a *search*.

The answer is a search, and the interesting part is that `H-065` is accepted anyway.

<a id="source-3-the-numbers"></a>

#### The numbers

Over 567,130,649 reachable cells in 181 directions:

| `epsilon` | tight cells | of reachable | of domain by area | components | largest blob |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0` | 0 | 0.0000% | 0.000% | 0 | 0 |
| `1/100` | 4,320,132 | 0.7618% | 1.519% | 10,908 | 16,447 |
| `1/20` | 23,112,904 | **4.0754%** | 7.596% | 22,132 | 30,779 |
| `1/10` | 50,583,976 | 8.9193% | 14.877% | 22,780 | 38,915 |

`H-065` registered acceptance below `0.20` and its kill line at `0.50`. `0.040754` is a
fifth of the first and an eighth of the second, so the hypothesis is accepted on its own
threshold and the mass gap is not swamped.

`epsilon = 0` is empty in every direction.
No reachable cell carries mass exactly one, so `Condition 5` holds with a uniform margin
of `1/4000` and `epsilon` here is genuinely a band above a floor rather than a
neighbourhood of a boundary the certificate touches.

<a id="source-3-why-the-reading-is-still-search"></a>

#### Why the reading is still “search”

The threshold `H-065` registered answers one question — is the tight set most of the
domain? — and four per cent answers it *no*. The cell asked a different one, and the
count is the smallest part of the answer.

**It has positive area.** Not a finite list of positions but `7.596` per cent of the
centre domain, up to `19.77` per cent in a single direction, and still `1.519` per cent
at the tenth of that margin.
A positive-measure active set is a continuum of near-active covering constraints, not a
set of them to enumerate.

**It is not localised anywhere.** The tight set’s bounding box equals the centre
domain’s own bounding box, exactly, in all 181 directions, at every non-empty margin —
including `epsilon = 1/100`, where it is a hundredth of the domain by area and still
reaches both extremes of both rotated coordinates.
Nor is it a boundary skin: the deepest tight cell in the directions probed sits at
normalised depth `0.41` to `0.43`, where `0.5` is the centre.

**Its parts are regions.** 22,132 components at `epsilon = 1/20`, median about 554 cells
each.
The component counts per direction — 24 to 348, median 136 — are the only statistic
anywhere near “a few dozen”, and they count blobs rather than positions.

So Corollary 1a’s exact-cover step has a positive-measure region to search per
direction, which is what `BC-207` needed to know and could not start without.

<a id="source-3-what-this-is-not-evidence-of"></a>

#### What this is not evidence of

It is what an integrality gap looks like from the inside, and it is not evidence of one.
The census measures the *LP solution’s* near-active set; the integer optimum is a
different object and nothing here bounds it.
The reading is consistent with a gap and would also be consistent with none.

<a id="source-3-the-instrument"></a>

#### The instrument

`OR-1` is why this cell exists at all, and the first attempt at it is why the rule is
worth restating: that attempt left a half-built script, no test and no census, and the
script reached a commit anyway.
What is retained now is `devtools/census_tight_cells.py` with
`tests/test_census_tight_cells.py` behind it, reading through the `MassGrid` /
`scaled_mass_grid` seam so the census and the retention decision read the same `int64`
array rather than two implementations of the same fill.
Every count, component, box and minimum is exact integer or `Fraction` arithmetic; the
only floats in the record are two fields named `approx_*`, and no verdict rests on them.

The test’s synthetic is a side-four container with nine atoms on the integer lattice,
chosen so each event cell holds exactly one atom and the whole census — counts,
components, largest blob and all four boxes — can be written out by hand before the tool
runs. Its second anchor is direction 0 of the retained rung, checked against
`reduce_to_cells` rather than against the span reduction the census expands, so the two
paths have to agree.
A third test pins the margin’s meaning into the emitted record: the bookkeeping point
that `epsilon` is a census margin and not the mass gap `M − n`, which at `381/100` is
negative, is now a field a later reader cannot invert.

<a id="source-4"></a>

## Source 4: `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-071-h-070-n11-inset-seed-release.md`

Snapshot `4d305597a505`, source lines 87-end.

<a id="source-4-exp-071--margin-biased-seed-with-support-released"></a>

### exp-071 — Margin-Biased Seed With Support Released

The screens chose the inset-`1/2` proposal.
The matched unrestricted arms then converged after eight rounds to byte-identical
candidates of exact mass `11142893/1000000`. H-070 is therefore rejected: the seed
neither helped nor hurt under this test.
Both candidates remain above eleven, so the round also opened no exact lower-bound
route.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
