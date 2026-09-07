# Fractional Barriers and Scoped Negative Results

These results restrict specific relaxations, sites, nets, weights or proof transfers. They do not rule out the general packing conjecture or every additive witness. X-014 predates the current lower endpoint and quantitative radius; use its mathematical barrier and conditioning arguments at their stated scope. H-092's unintegrated transport is not included or promoted to independently inspected evidence.

## Thresholds to Read at Their Exact Scope

X-014's scalar obstruction includes the finite-net transfer: its symbolic threshold is `C = U B max_i(cos(delta_i)+sin(delta_i))`, where each `delta_i` is the angular distance to the selected net direction. For `L > C` the eleven closed cores lie strictly inside the scaled packing squares. The displayed 3.868983 is rounded; `UB` alone is the ideal-angle value, not the finite-net threshold.

The exp-064 excerpt quotes a two-end-cell ceiling `B(2+4sqrt(2)/3)` using an attaining 0/45-degree packing. Its rational net endpoint is `2 atan(207107/500000)`, not exactly pi/4. Applying that exact threshold to this finite net requires an additional angular-containment transfer, which the quoted deduction does not supply. The attaining construction is also a literature premise here, not reconstructed coordinates. Review this inference before reusing the quoted number as an exact finite-net theorem. The retained computational control failure remains a result at its recorded scope; this packet makes no new ceiling claim.

<a id="source-1"></a>

## Source 1: `packing/campaign/explorations/X-014-closing-from-both-ends.md`

Snapshot `4d305597a505`, source lines 83-430.

<a id="source-1-the-question-and-the-two-gaps-it-conflates"></a>

#### The Question, and the Two Gaps It Conflates

The owner’s question, in its own terms: if the lower bound keeps rising toward Trump’s
packing, is there a proof strategy in which the two get close enough that the rest can
be argued away — a chunking argument over the coarse configurations of the blocks, or a
perturbation argument that nothing near the record can be smaller — so that Trump’s
configuration is the only packing left in the interval, and the upper bound cannot get
any smaller?

The answer has a yes in it and a no in it, and both depend on distinguishing two gaps
that the question runs together.

The **side gap** is what the frontier record reports: `s(11) ∈ [3.81, 3.877084]`, width
`0.067084` after [`T-018` (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/frontier/RESULTS.md).
It is a property of the problem, and narrowing it is what a certificate ladder does.

The **mass gap** is a property of one certificate at one side.
A weighted fractional unavoidable-set certificate at side `L` is a finite atom measure
`μ` whose every admissible core covers mass at least `1`; its total mass `M(L)` is what
the search minimises, and the certificate proves `s(11) > L` exactly when `M(L) < 11`.
Above the side where the least achievable `M` crosses `11`, the certificate proves
nothing, but the quantity `ε(L) = M(L) − 11` still carries information: it is the slack
a packing at side `L` would have to live inside, and it is small exactly where the
certificate has just stopped working.

The perturbation half of the question is about the side gap: it asks that the last
sliver below Trump’s value be closed by a local argument at Trump’s pose.
The chunking half is about the mass gap: it asks that a certificate that no longer
proves infeasibility still constrain the packings that survive it, tightly enough that
finitely many cases remain.
The yes is that both mechanisms exist, are elementary, and are within reach of the
instruments in this repository.
The no is that neither is a shortcut past the case analysis; they change what the cases
are and what closes them, and the size of the resulting tree is not known.
Six measurements would decide it, and none has been made.

<a id="source-1-what-a-certificate-is-and-the-two-places-it-must-stop"></a>

#### What a Certificate Is, and the Two Places It Must Stop

The certificate in [`sqpack.fractional` (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/src/sqpack/fractional/certificate.py) is
the dual of a linear relaxation, and reading it that way is what makes the rest of this
report precise. Fix a side `L`, a shrink `B`, and a direction net.
The **covering program** minimises the total mass of a non-negative measure on the
container subject to every admissible `B`-square at a net direction carrying mass at
least `1`; its value is the covering value `τ*(L)`. Its dual is the **fractional packing
program**: non-negative weights on admissible placements whose depth — the weighted
number of placements containing a point — is at most `1` everywhere, with value `ν*(L)`.
Weak duality, proved in one line in the docstring of
[`ceiling.py` (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/src/sqpack/fractional/ceiling.py), gives `ν*(L) ≤ τ*(L)`. Over
`D4`-symmetric measures — equivalently over all measures with the doubled net — a
certificate exists at side `L` when `τ*(L) < 11`, up to the discretisation into finitely
many rational atoms that the search performs, and a fractional packing of value at least
`11` proves that none does.

A packing of eleven unit squares is a fractional packing of value `11` with all weights
equal to `1`: each unit square contains a `B`-square at a net direction or a `D4` image
of one (conditions `Condition 4` and `Condition 1`), the eleven cores are disjoint, and
their depth is at most `1`. So `ν*(L) ≥ 11` at every side where eleven squares fit, and
the certificate’s reach is bounded above by `s(11)` for the trivial reason.
What the method actually reaches is the smaller of two quantities, and the record now
lets both be stated.

**Where the shrink stops it.** Scaling Trump’s packing by `λ = L / U` puts eleven
squares of side `λ` in a container of side `L`. A square of side `λ` at angle `θ`
contains a `B`-square at the net direction `θ_k` about the same centre whenever
`λ ≥ B (cos δ + sin δ)` with `δ = |θ − θ_k|`, which is the containment step of
`Condition 4`. Trump’s six axis-aligned squares sit at direction `0`, a net direction,
and need `λ ≥ B`; the five tilted ones, at `40.181937°`, are `0.012100°` from the
nearest net direction, index `159` at `40.194037°`, and need
`λ ≥ B (cos δ + sin δ) = 0.997911`. So for every `L > U × 0.997911 = 3.868983` the
scaled packing contains eleven pairwise disjoint admissible `B`-squares at net
directions — a fractional packing of value `11` — and no certificate exists at that `L`,
whatever the site set and weights.
That is arithmetic on three constants recorded in
[`certificate.json`](07-standalone-381-proof.md#source-1), the
record’s tilt, and the formula of `Condition 4`, not a measurement, and it is the
argument of the ceiling theorem in
[`CERTIFICATE-REACH.md` (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/frontier/CERTIFICATE-REACH.md) with the record packing in
place of the grid: there the refuting object is the grid at `4B = 3.9908`; here it binds
`0.1218` lower.

Two readings follow.
The retained instrument can never certify the last `0.0081` below `U` at `n = 11`: the
shrink `B = 9977/10000` alone caps it at `U · B = 3.868166`, and the net’s offset from
the record’s tilt moves the cap up by less than a thousandth.
And the cap rises only with `B`, which `Condition 4` ties to the net’s largest half-gap
tangent `D` through `B (1 + D) < 1`, so halving the tax needs roughly twice the
directions. The shrink is a fixed price of the instrument, about an eighth of the
remaining side gap; the covering value decides how much of the rest is reachable.

**Where the covering value stops it, which is not known.** `T-018`’s own `next_rung`
records that two independent site sets at `3.82` stop at a restricted optimum of exactly
`11.000000` — one converged, one stood there through twenty-four rounds while its least
covered mass climbed from `0.8490` to `0.9997` — and that the rejection route does not
close either: the converged dual is `76` squares, `608` after the `D4` images, with raw
total `11`, but its exact maximum pointwise depth is `1925/1152 = 1.671007`, so the
depth-scaled family reaches only `1152/175 = 6.5829` of the eleven a ceiling needs.
So at `3.82` the record holds `6.58 ≤ ν*(3.82) ≤ τ*(3.82)`, with the restricted optimum
on both site sets sitting at exactly `11.000000` — an artefact-shaped round number that
the block-close handoff explicitly warns against reading as `τ*`. Whether the
certificate ladder is blocked at `3.82`, at `3.85`, or nowhere below `U` is the fact on
which the rest of this report turns, and it is unmeasured.

The measurement is well defined and the instrument exists.
`ν*(L)` is bounded below by any family of placements with weights whose depth is at most
`1` at every vertex of their arrangement, which is exactly what `ceiling.py` decides;
the family at `3.82` fails only because its weights came from a dual that enforced depth
at the sites, not at the arrangement’s vertices.
Adding the violating vertices as sites and re-solving is the cutting-plane loop the
column generator already runs in the other direction.
A value at or above `11` at some `L < U` proves the ladder cannot pass `L`, and the
distance from that `L` to `U` is the part of the side gap that no certificate of this
shape will ever close.
That is where the owner’s question begins in earnest, and the rest of this report
assumes the answer is that such an `L` exists somewhere in `(3.81, U)`. If it does not —
if `τ*(L) < 11` all the way to the shrink cap `3.868983` — the ladder alone proves
`s(11) ≥ L` for every rational `L` below the cap, a finer net moves the cap toward `U`
without reaching it, and the perturbation lemma of the section after next is all that is
left.

The literature the archive holds is consistent with a gap but does not decide one.
Caoduro–Sebő prove that the piercing-to-packing ratio of families of unit squares under
rotation can be as large as `3` and is never above `6`, and the 2026 counterexamples to
Wegner’s conjecture put the clique-LP integrality gap for rectangles at `5/2 − ε`; both
concern finite families given in advance rather than the covering value of a container,
so they say that a plateau below `s(11)` would be unsurprising, and no more.

<a id="source-1-the-bridge-what-a-packing-must-do-to-a-certificate-it-does-not-refute"></a>

#### The Bridge: What a Packing Must Do to a Certificate It Does Not Refute

The first lemma is the whole of the chunking half in one counting step.
It is the complementary-slackness statement for this relaxation, and its content is that
a certificate that has stopped proving infeasibility has not stopped constraining
packings.

**Lemma 1 (tight cores).** Let `μ` be a `D4`-symmetric finite atom measure on `[0, L]²`
satisfying `Condition 3`, `Condition 4` and `Condition 5` for `(B, net)`, with total
mass `M`. Let `Q₁, …, Q₁₁` be closed unit squares in `[0, L]²` with pairwise disjoint
interiors. Then there are closed `B`-squares `P_i ⊂ int Q_i`, each at a net direction or
a `D4` image of one, pairwise disjoint, with `μ(P_i) ≥ 1` for every `i`; and
consequently

- `M ≥ 11`;
- `μ(P_i) ≤ 1 + (M − 11)` for every `i`; and
- `μ([0, L]² ∖ ⋃ P_i) ≤ M − 11`.

*Proof.* `Condition 4` places a `B`-square at a net direction, or a `D4` image of one,
inside each unit square’s interior about its centre; the interiors are disjoint, so the
cores are disjoint as closed sets.
`Condition 5` with `Condition 1` gives each core mass at least `1` (a core at an image
direction covers the mass its reflected image covers).
Then `11 ≤ Σ μ(P_i) ≤ M`, and each inequality in the statement is that sum with all but
one term bounded below by `1`. ∎

Write `ε(L) = M − 11` for the mass gap.
The lemma says that any packing at side `L` sits on cores that are `ε`-tight against `μ`
and that together miss at most `ε` of `μ`’s mass.
In the language of integer programming this is reduced-cost fixing: a placement whose
mass exceeds `1 + ε` cannot appear in any integral solution, and the search may be
restricted to the `ε`-tight placements.
Two consequences follow, and the second is the one worth building.

**Corollary 1a (the boundary case is decidable).** The cores are disjoint closed sets
and the atoms outside all of them weigh at most `ε` together, so every atom heavier than
`ε` lies in exactly one core.
The atoms heavier than `ε` are therefore partitioned into eleven groups, each contained
in a `B`-square at a net direction or its image, each core weighing at most `1 + ε` in
all, and the cores’ enclosing unit squares are pairwise interior-disjoint inside the
container. If no such partition exists, no packing exists at side `L`, even though
`M ≥ 11`.

This is a finite question about one atom set, and it addresses the configuration `T-018`
records as the one neither pre-registered route can close if it holds: `τ*(3.82) = 11`
exactly. There, a certificate fails by an infinitesimal and a ceiling fails by an
infinitesimal, but the packing that would have to exist is pinned to an exact cover of
the heavy atoms by eleven cores of mass one: finitely many assignments of atoms to cells
and directions, each with a semialgebraic feasibility check in the free centres and
angles, so decidable, if not purely combinatorial.
The skeleton is not the whole atom set: the retained `3.81` certificate has `1121` atoms
with weights from `3/40000` to `917/6250`, read from the file, and of those `649` weigh
more than `1/200` and carry `9.97` of its `10.86` units of mass, `289` weigh more than
`1/100` and carry `7.02`, and `93` weigh more than `1/50` and carry `4.28`. A mass gap
of a few thousandths, which is the size the rationalisation step alone introduces,
forces every atom of the heavy skeleton into a core and leaves the light ones free.

**Corollary 1b (tightness is computable cell by cell).** Covered mass is piecewise
constant in a core’s centre and changes only on the event grid, which is what makes the
exact sweep in [`sweep.py` (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/src/sqpack/fractional/sweep.py) finite.
So the `ε`-tight placements at each net direction are a union of event cells, and the
sweep fills a grid holding every reachable cell’s mass before it takes the minimum.
A census of cells with mass at most `1 + ε`, per direction, is a readout of that grid
rather than a new computation, and it is the first thing to look at: if the tight set at
the ladder’s top is a few hundred cells clustered around a few dozen positions, the case
analysis is finite in practice and not only in principle; if it is a fat region, the
mass gap constrains nothing worth enumerating.

Lemma 1 holds for any measure that satisfies the covering condition, not only the one
the search minimised, so the measure can be chosen for the purpose: maximise the least
slack outside a neighbourhood of the record’s own eleven placements and their images,
subject to a total mass of at most `11 + ε`. That is another linear program, and it is
the form in which the case analysis would be built, because a measure that is tight
everywhere constrains nothing.

`μ` speaks about `B`-squares at net directions; a packing consists of unit squares at
arbitrary angles. Lemma 1 bridges them through `Condition 4`, and the price is that the
case analysis in Corollary 1a runs over cores rather than over squares: a group of atoms
must fit in a `B`-square, concentric with its unit square as Lemma 1 constructs it,
whose enclosing unit square, at some angle within the half-gap of the net direction, is
what must be disjoint from its neighbours.
Disjointness of the unit squares is strictly stronger than disjointness of the cores,
and it is the stronger condition the exact-cover search must use; eleven disjoint cores
alone would only say that eleven `B`-squares fit, which at `3.82` would give
`s(11) ≤ 3.8288` and is not known to be false.

<a id="source-1-branching-is-chunking-conditional-certificates"></a>

#### Branching Is Chunking: Conditional Certificates

The owner’s “major configurations of the blocks” is a branching rule.
A branch fixes something discrete about the packing — which class a square’s direction
falls in, which region its centre occupies, which contact structure the blocks form —
and what a proof needs is a lower bound valid on that branch alone.
The certificate conditions on a branch in two ways, and both are one counting step from
the unconditional argument.

**Lemma 2 (conditional certificate).** Let `b` be a set of placements of one unit square
(a box in `(x, y, θ)`), and let `I_b = ⋂_{Q ∈ b} Q` be the region every placement in the
box occupies.
Take a net that spans a full quarter turn and satisfies `Condition 4` — its
half-gaps are those of the eighth-turn net, so the same `B` serves — and let `Λ_b` be
the admissible `B`-square placements at net directions that are disjoint from `I_b`.
Suppose a finite atom measure `μ` of total mass `M < 11` gives mass at least `1` to
every member of `Λ_b` and to every `B`-square at a net direction that lies inside some
placement in `b`. Then no packing of eleven unit squares in `[0, L]²` has a square in
`b`.

*Proof.* If `Q_k ∈ b`, its core `P_k` is a `B`-square at a net direction inside a
placement in `b`, so `μ(P_k) ≥ 1`; each other square `Q_i` has a core `P_i ⊂ int Q_i` at
a net direction, disjoint from `Q_k ⊇ I_b`, so `P_i ∈ Λ_b` and `μ(P_i) ≥ 1`. The eleven
cores are pairwise disjoint, so `11 ≤ Σ μ(P_i) ≤ M < 11`. ∎

An unconditional certificate satisfies the hypotheses, so the conditional bound is never
weaker, and it is strictly stronger whenever the branch lets mass move: atoms inside
`I_b` cover every placement in `b` at once and need not cover any member of `Λ_b`, which
is disjoint from `I_b` by construction.
Putting mass exactly `1` inside `I_b` and asking the rest to weigh below `10` outside it
is one feasible point of that program, not its optimum.
The net must span a quarter turn rather than an eighth, because a box breaks the
container’s `D4` symmetry and `Condition 1` can no longer fold angles onto the shorter
arc; the interval route already decides on a doubled net, so this costs a factor of two
in directions and no new idea.

The same count boxes several squares at once.
For boxes `b₁, …, b_k` with cores `I₁, …, I_k`, require mass at least `1` on every
`B`-square at a net direction that lies inside some placement in `b_i` and is disjoint
from every `I_j` with `j ≠ i`, for each `i`, on every admissible `B`-square disjoint
from all the `I_j` for the free squares, and `M < 11`; then no packing has `Q_i ∈ b_i`
for every `i`. Each boxed square gets its own non-convex admissible set, which is what
the fifth measurement below would have to build.

**Lemma 3 (class certificate).** Partition the net directions into `D4`-closed classes
`Θ₀` and `Θ₁`, each a union of the net’s half-gap cells, the arcs bounded by the
midpoints between consecutive net angles; a square belongs to the class of the net
direction `Condition 4` assigns it, the one whose cell contains its angle.
Fix counts `n₀ + n₁ = 11`. Suppose weights `w₀, w₁ ≥ 0` and a `D4`-symmetric measure `μ`
of total mass `M` satisfy: every admissible core at a direction in `Θ₀` has mass at
least `w₀`, every admissible core at a direction in `Θ₁` has mass at least `w₁`, and
`M < n₀ w₀ + n₁ w₁`. Then no packing has exactly `n₀` squares with directions in `Θ₀`
and `n₁` in `Θ₁`.

*Proof.* Each square’s core is at the net direction of its own class, the cores are
disjoint, and each contributes at least its class weight.
∎

The cell condition is not decoration: a square at `4.9°` on the retained net lies in the
cell of the direction at `5.007°` and contains no `B`-square at the direction below it,
so a class cut at a geometric angle rather than at a cell boundary would count it
wrongly.

The constraints are linear in `(μ, w₀, w₁)` and the objective `M − n₀ w₀ − n₁ w₁` is
homogeneous, so the class certificate is one linear program per composition, decided by
the sign of its optimum under a normalisation.
It is the two-threshold form of `Condition 5`, and it prices what everyone in this
subject knows informally — a tilted square costs more room than an aligned one — as a
dual variable instead of a lemma.
Stromquist’s Theorem 3 is a class certificate with one more step: the class is
`{0°, 45°}`, the strengthened Lemmas 7 and 8 of his paper are the covering condition
restricted to that class, and his twelve points — one more than eleven, so the count
alone proves nothing — are closed by a step of Corollary 1a’s kind, a box forced to
swallow three of them at once.
Its bound, `2 + (4/3)√2 ≈ 3.885618`, sits above Trump’s value, which is what settles
Gardner’s conjecture and also what shows the shape is the right one: the class that does
not contain Trump’s packing is closed above `U` by a certificate conditioned on the
class. A proof would need every class closed that way except the one Trump’s pose lives
in, and that one handed to the next section.

One class certificate needs no shrink and no computer, and it calibrates the composition
step. A unit square tilted by `θ` contains an axis-parallel square of side
`1 / (cos θ + sin θ)` about its centre, and nine points on a grid of pitch `s/4` pierce
every axis-parallel square of side at least `s/4` inside `[0, s]²`, because an interval
of that length inside `[0, s]` contains a multiple of `s/4` other than `0` and `s`. So
at side `s` at most nine squares of any packing are tilted by less than `θ₀(s)`, where
`cos θ₀ + sin θ₀ = 4/s`: `1.85°` at `U` and `2.77°` at `3.82`. At every side below `U`,
then, at least two squares are tilted by `1.85°` or more, and the compositions `n₁ ≤ 1`
are closed by nine points for every near-axis class contained in the tilts below
`1.85°`. Trump’s packing has five such squares, so the fact is consistent rather than
sharp; its value is as the template, since a class certificate is a covering condition
restricted to a class and the classical lemmas are the special case where the covering
is by points.

The branching order this suggests is the chunking the owner described, made discrete:

1. **Composition.** Twelve class certificates, one per `n₁ = 0, …, 11` tilted squares
   for a near-axis class `Θ₀` that is a union of half-gap cells of half-width about `α`.
   Nine points close `n₁ ≤ 1` at every side below `U` for any such class inside the
   tilts below `1.85°`; the grid that proves the ceiling caps every near-axis class at
   `4B`; Stromquist’s Theorem 3 is the evidence that compositions far from Trump’s close
   above `U`; the compositions near Trump’s, with five squares tilted near `40°`, cannot
   close and are refined.
2. **Angle bins.** Within a surviving composition, the tilted class is split into bins;
   every bin that does not contain `40.18°` is a class certificate again, and the bins
   that do are refined.
3. **Position boxes.** Lemma 2, one square at a time, on the squares whose regions the
   tight-core census of Corollary 1b says are forced.
4. **Contact type.** In the boxes that survive, the fixed-angle cell of `T-2` — every
   angle and every separating axis fixed makes the side a linear program in the centres
   — bounds the side exactly, and only the cell containing Trump’s pose reaches `U`.

None of this is implemented.
The codebase inventory on which this report rests found no admissibility hook in
`sqpack.fractional`: the admissible centre domain is hard-coded as the rotated container
square in `sweep.centre_domain`, in the float mirror in `generate.py`, and in the four
half-planes `interval.DirectionSearch` propagates; each of the three assumes that domain
is convex, which a container minus `I_b` is not, and the column generator routes its
oracle through the second.
Lemma 3 needs none of that — it changes the covering program’s thresholds and objective,
adding two variables and one normalisation row, and nothing geometric — which is why the
composition step is the cheap one and the place to test whether conditioning buys
anything at all.

The symmetry bookkeeping is standard.
A minimal packing spans the container in at least one direction, or the container could
shrink, so after a translation it touches both walls of one pair of opposite sides;
labels are broken by ordering the squares, and the container’s symmetries by fixing the
spanning direction and the wall the lowest square touches.
Montanher and co-authors do this for squares in a circle by tiling the centre domain
into isosceles triangles of base below `1`, each holding at most one centre, and
iterating over tile combinations one square at a time so that infeasible small
combinations kill their supersets; at `n = 3` that was `6`, `43` and `12` subproblems
out of `7140` combinations.
The same device applies here unchanged.

<a id="source-2"></a>

## Source 2: `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-064-h-063-two-threshold-class-program.md`

Snapshot `4d305597a505`, source lines 148-end.

<a id="source-2-exp-064--a-control-that-could-not-be-reached"></a>

### exp-064 — A Control That Could Not Be Reached

`BC-198` built `X-014`’s Lemma 3 and ran its two pre-registered controls.
One passed exactly. The other refused, and the interesting part is that it could never
have done anything else.

<a id="source-2-what-was-built"></a>

#### What was built

`classcert.py` partitions the net’s half-gap cells into direction classes, carrying the
boundaries as exact tangents — the midpoint angle’s tangent is rational even where its
half-tangent is not.
`solve_class_program` adds `w0` and `w1` as LP variables under the single normalisation
row `n0·w0 + n1·w1 = 1` and separates each placement against its own class’s threshold;
`decide_class_program` decides the same object exactly on the event-cell sweep,
reporting Conditions 1, 3 and 4 unchanged, `Condition 5'` per class and `Condition 2'`
as `M < n0w0 + n1w1`.

Nothing geometric moved.
`sweep.centre_domain`, the float mirror in `generate.py` and the four half-planes
`interval.DirectionSearch` propagates are untouched, which is what kept this a threshold
change and left the non-convex domain to `BC-204`.

<a id="source-2-control-one-exactly-nine"></a>

#### Control one: exactly nine

The near-axis class at `3877/1000` returns `9.000000` in floats, converged in five
rounds, and exactly `9` from nine unit atoms with least cell mass exactly one over the
six leading cells. The lane then closed the bound from below as well — nine pairwise
disjoint axis-parallel `B`-squares fit — so the optimum is *exactly* nine, not merely at
most nine. The cell’s suspension clause, which treats an optimum above nine as an
instrument defect, does not fire.

<a id="source-2-control-two-0000403-short-and-not-by-accident"></a>

#### Control two: `0.000403` short, and not by accident

At Trump’s `3.877084` the two-end-cell class gives `11885/1024 = 11.606445` against the
eleven a refutation needs.
Six independently built site sets never go below `11.6`.

That is not a search that ran out of budget.
The figure that refuses it is exact and does not mention a site set:

`L/B = 969271/249425 = 3.886021850` exceeds `2 + (4/3)√2 = 3.885618083`.

So eleven pairwise disjoint `B`-squares of the class fit inside the container at that
side, and no measure of total mass below eleven can cover them — whatever sites are
chosen, however long the row loop runs.
The control’s ceiling is `B(2 + (4/3)√2) = 3.876681`, which sits **`0.000403` below the
side the cell asked it to reach**. The shrink costs `0.008937` of side; Stromquist’s
headroom above Trump is `0.008534`. The control was unreachable before the first command
ran.

`H-063`’s own text anticipated the shape without noticing the arithmetic: it says
Stromquist’s Theorem 3 reaches `3.885618` “by a further box step this program does not
have”, and sets the threshold at `3.877084` precisely because the program should not be
credited with reach it lacks.
What nobody computed in advance is that removing the box step also removes `0.000403`
more than the margin between the two sides.

<a id="source-2-what-conditioning-does-buy"></a>

#### What conditioning does buy

The round reports this rather than only the refusal, because “conditioning buys too
little” is the kill condition and the amount matters.

Two thresholds do separate.
On one site set at Trump’s side a single threshold gives margin `+0.082256`; two at
composition `(9, 2)` give `+0.072368`, with the LP pulling `w0 = 0.093383` above
`w1 = 0.079777` once the site set is fine enough.
And `X-014`’s own step-1 design point is reachable: composition `(11, 0)` over the
leading nineteen cells at Trump’s side, grid 79, exact `39123/4096 = 9.551514`, margin
`−5933/4096`, every condition holding, refuted.
The `11.000000` readings at grids 39 and 95 are the round-number artefact this register
now recognises at three orders, not a wall.

Nothing was retained.
`decide_certificate` decides a five-condition `Certificate` and not a two-threshold
object; registering a class theorem is `BC-208`’s gate work.

<a id="source-2-the-price-which-is-what-the-cell-existed-to-produce"></a>

#### The price, which is what the cell existed to produce

One class LP solve is `14.4 ms` mean and `22.3 ms` max at 78 orbits plus two thresholds
and 1191 rows; `49.4 ms` and `82.2 ms` at 210 orbits and 1554 rows.
A whole class program over all 181 directions with both classes active, run to
convergence, is `8.57 s` at grid 23 and `27.66 s` at grid 39. Twelve compositions at
grid 39 price at about five and a half minutes of one core.

**The LP is under two per cent of that.** Separation, not the LP, is what a composition
sweep buys — which is the number `BC-208` needs and the reason this cell was worth its
budget even though its headline control refused.

<a id="source-3"></a>

## Source 3: `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-070-h-064-n11-fractional-resume.md`

Snapshot `4d305597a505`, source lines 110-end.

<a id="source-3-exp-070--bc-232-retained-state-resume"></a>

### exp-070 — BC-232 Retained-State Resume

This round spent the first 105-minute deadline of BC-232’s retained four-CPU-hour
evidence budget, plus the runner’s terminal in-flight tail.
It raised the exact lower endpoint from approximately `9.907905595` to
`21342289572/2055263195 ≈ 10.384212408377215`; the only row-converged computational
upper endpoint remains `11.055616942909783`. The resulting provisional width is about
`0.671404535`, roughly 41.5 percent narrower than the pre-resume bracket.

That percentage is a checkpoint, not the routing decision.
The frozen rule evaluates the full four-CPU-hour evidence budget, so the remaining 135
one-core minutes may begin only after this T+2 landing.
The retained state is resumable.
Its pre-add serialization does not include iteration 13’s terminal 150 selected orbits
or summary stop string; the terminal summary and frozen family carry the authoritative
last-iteration and stop receipt.

<a id="source-4"></a>

## Source 4: `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-110-h-090-core-shrink.md`

Snapshot `4d305597a505`, source lines 71-end.

<a id="source-4-exp-110--a-corner-event-rejects-the-first-core-shrink"></a>

### exp-110 — A Corner Event Rejects the First Core Shrink

The first core shrink fails.
The [raw receipt (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/results/exp-110-h-090-core-shrink/result.json) records
$m(99769/100000)=85353/100000=0.85353$, below $M/11=434547/440000\approx0.98760681818$.
No candidate certificate was emitted, and the production retention gate and standalone
verifier had no candidate to decide.
T-022 remains the retained lower bound.

The exact source replay took 14.846608 seconds; the candidate replay, including a
separate sweep of the worst direction and direct atom summation at its witness, took
14.957827 seconds. The full invocation ran from 11:14:26.226943Z to 11:14:56.091880Z on
2026-09-06. The raw command records the actual interpreter and isolated checkout paths;
the command above uses the repository’s portable invocation.

<a id="source-4-the-obstruction-is-a-narrow-event-not-every-smaller-core"></a>

#### The Obstruction Is a Narrow Event, Not Every Smaller Core

The worst direction is axis aligned.
Put $e=1849127/1853400\approx0.9976945074$. The witness center is $(e/2,e/2)$, and a
core at this center is admissible for every positive side $b\le e$. The receipt gives
the complete sorted inclusion-event spectrum at this center.
Its last event below $e$ is $1565797464121/1570613788200$; the next event is exactly
$e$, where the covered mass increases by $917/6250$. The total mass from all preceding
events is $85353/100000$. Thus every $b<e$ has a concrete admissible placement of mass
at most $85353/100000$, which rejects normalization of these fixed weights throughout
that range. At $e$ the mass at this witness becomes exactly $4001/4000$.

The range $e\le b<9977/10000$ remains unresolved.
Its width is exactly $509/92670000$. The experiment therefore identifies a necessary
core size for this measure; it does not establish that the source side is critical or
rule out every positive shrink.

<a id="source-4-why-the-acceptance-rule-allows-mass-below-one"></a>

#### Why the Acceptance Rule Allows Mass Below One

For fixed atoms and net, let $m(b)$ be the minimum mass over all admissible side-$b$
cores in the fixed container.
If $m(b)>M/n$, replacing each weight $w_i$ with $w_i/m(b)$ makes the minimum one and the
total strictly less than $n$. Any rational dilation $q$ satisfying $qb(1+D)<1$ then
gives an ordinary certificate at side $qL$. The proposed $q=100001/100000$ satisfies the
containment inequality, and $qL=38100381/10000000$ exceeds T-022’s endpoint by more than
$1/100000$. Coverage is the failed premise.

The function $m(b)$ is nondecreasing: if $b_1<b_2$, every center admissible for the
larger core also admits the smaller core, and the smaller core is contained in the
larger one. Taking minima gives $m(b_1)\le m(b_2)$. It need not be continuous.
Even an equally spaced one-dimensional atomic measure can cover every closed interval of
the lattice spacing with positive mass while slightly shorter intervals fit between
atoms and have zero mass.
A coverage margin alone supplies no geometric perturbation radius.

<a id="source-4-exact-critical-events-for-a-further-size-search"></a>

#### Exact Critical Events for a Further Size Search

At a retained rational direction $(c,s)$, rotate centers to $(U,V)$ and atoms to
$(u_i,v_i)$. The coverage-event lines are $U=u_i\pm b/2$ and $V=v_i\pm b/2$. The
admissible-center lines are $cU-sV=b(c+s)/2$, $cU-sV=L-b(c+s)/2$, $sU+cV=b(c+s)/2$, and
$sU+cV=L-b(c+s)/2$. Each line has the form $aU+dV+f+gb=0$ with rational coefficients.

Changes in the arrangement occur only at parallel-line coincidences or vanishing
three-line determinants.
The determinant is affine in $b$, so every isolated critical value is rational.
The familiar event-order changes $b=|u_i-u_j|$ and $b=|v_i-v_j|$ are included.
Identically zero determinants represent persistent coincidences and do not supply
isolated critical values.
Between consecutive critical values, the cell incidence and its mass labels are
constant.

For a complete test immediately below a proposed side $B=p/r$, clear denominators on
every line and let $H\ge1$ bound the absolute integer coefficients.
The numerator and slope of each three-line determinant have magnitude at most $6H^3$;
the parallel-coincidence equations obey the same bound.
Every distinct critical value is at least $1/(6rH^3)$ from $B$. Consequently a replay at
$B-\min(B/2,1/(12rH^3))$ decides the immediate left-hand arrangement, including the case
where $B$ itself is critical.
This finite bound is a proof plan; this experiment implements the single-side replay and
the complete inclusion events at its witness, not that global arrangement search.

<a id="source-4-verification-and-next-slice"></a>

#### Verification and Next Slice

Five focused tests pass, including normalization of a genuine below-one minimum through
both production decision routes, refusal of wrong-$n$, duplicate-key and
stale-declaration sources, failure-witness retention, containment refusal, and a direct
atom-sum regression of the exact corner obstruction.
Ruff and BasedPyright report zero findings.
The coordinator’s document-map correction has been integrated into the isolated
checkout. The synopsis carries the new hypothesis, round and cost totals.

A separate hypothesis should test a rational side above $e$ before investing in a
complete critical-arrangement enumerator.
The rejected point and its original acceptance rule remain frozen as H-090.

<a id="source-5"></a>

## Source 5: `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-111-h-091-core-shrink.md`

Snapshot `4d305597a505`, source lines 72-end.

<a id="source-5-exp-111--an-interior-witness-closes-the-ordinary-shrink-route"></a>

### exp-111 — An Interior Witness Closes the Ordinary Shrink Route

The second fixed-atom core shrink fails.
The [frozen receipt (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/results/exp-111-h-091-core-shrink/result.json) gives
$m(997696/1000000)=96377/100000=0.96377$, below $M/11=434547/440000$ by $52441/2200000$.
No candidate certificate was emitted, so there was no candidate for the production
retention gate or standalone verifier to decide.
Neither T-018 nor T-022 changes.

H-091 was committed as `210991ad` before this point was measured.
The run used clean commit `aeb683d5`, which adds only a synopsis wording correction.
It ran from 11:31:11.672807Z to 11:31:42.257452Z on 2026-09-06. The source replay took
15.128362 seconds; the smaller-core replay, including a repeated sweep of its worst
direction and direct atom sum, took 15.403501 seconds.
The raw receipt preserves the actual interpreter, checkout, command and tool digest.

<a id="source-5-the-recovery-event"></a>

#### The Recovery Event

The worst placement uses zero-based net direction 97 and an interior center, not
exp-110’s corner center.
For this fixed center $(U,V)$ in coordinates rotated to that direction, atom $i$ enters
the closed core exactly at side $2\max(|u_i-U|,|v_i-V|)$. The receipt retains these
rational sides with their added masses and the exact center in both coordinate systems.

The first inclusion event at which this witness exceeds $M/11$ is

$$
e_{97}=\frac{1696802860582378979}{1700716629721128200}.
$$

Its mass immediately below this event is $96377/100000$. At the event, mass
$25257/200000$ enters, giving $218011/200000$. The center admits every positive core
side through

$$
a=\frac{17137540266205342633239451929256187973}
{8490057146508782661010155026357102600}>e_{97}.
$$

Thus every $0<b<e_{97}$ has an admissible core of mass at most $96377/100000$. No
normalization of these fixed weights can certify such a core side: its exact minimum
cannot exceed this witness mass, which is below $M/11$. This conclusion uses a single
placement and nonnegative weights; it does not require a sweep at any unmeasured side.

<a id="source-5-why-this-excludes-the-entire-ordinary-containment-window"></a>

#### Why This Excludes the Entire Ordinary-Containment Window

Write $B=9977/10000$ and $D=207107/90000000$ for the source core side and largest
half-gap tangent. T-022’s endpoint is $S_*=L\sqrt{1+D^2}/(B(1+D))$. For a smaller core
$b$ and dilation $q$ to improve it using ordinary containment, both $qL>S_*$ and
$qb(1+D)<1$ must hold.
Combining these strict inequalities requires

$$
b<\frac{B}{\sqrt{1+D^2}}.
$$

But the exact witness event satisfies

$$
e_{97}^2-\frac{B^2}{1+D^2}
=\frac{65196331602516217274491708275075416012593285009}
{23428864208538589123227153839724949707492304182760000}>0.
$$

Every core in the ordinary-containment improvement window is therefore below $e_{97}$
and rejected by this witness.
This is a whole-window obstruction for fixed sites, fixed net and fixed relative
weights, not just a negative result at two sampled points.
The proposed side $381002667/100000000$ does exceed T-022 algebraically; the failed
coverage premise prevents obtaining that bound.

<a id="source-5-replay-and-disposition"></a>

#### Replay and Disposition

The reusable witness-inspection mode hashes the frozen source, reconstructs every
inclusion event from its atoms, requires the entire spectrum and witness fields to match
the receipt, and computes the first mass-recovering event and the exact ordinary-window
comparison. It does not infer a global minimum from this one placement.
Run it without launching another sweep:

```bash
cd packing
uv run --frozen --all-extras --group dev python -m devtools.core_shrink \
  cases/n11_fractional_certificate/certificate.json \
  --inspect-witness campaign/series/series-000-smoke-and-calibration/results/exp-111-h-091-core-shrink/result.json
```

Seven focused tests pass, including both retained witnesses’ recovery events,
source-byte and witness-mass mutation refusals, and a small positive normalization that
passes both production routes with an original minimum below one.
Ruff and BasedPyright report zero findings.
The records tier passes all 31 selected steps in 15.15 seconds, including the experiment
schema, generated ledger, synopsis totals and mutation anchors.
This scoped checkpoint is not the full integration gate.

The two registered measurements are complete; no third experiment was run.
Refined containment on a smaller, successfully normalized source core is a distinct
route not excluded here.
It would need a new preregistration, an exact mass replay at a side above this
obstruction, and the refined-limit proof and retention checks.
Changing sites, the net or relative weights also falls outside this obstruction.
The coordinator can price those alternatives against the released research lanes without
repeating either frozen negative.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
