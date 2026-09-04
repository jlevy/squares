---
title: "X-014 — closing from both ends: what a narrow gap buys at n = 11, and what it cannot"
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-014
  title: "Closing from both ends: what a narrow gap buys at n = 11, and what it cannot"
  date: '2026-09-04'
  author: Claude (agent), at the owner's request, on the branch stacked on PR #78
  campaign: packing.squares
  brief: >-
    The owner asked, after the fractional certificate moved s(11) to 3.81 against Trump's
    3.877084, whether a creative proof strategy exists in which the lower bound and the
    record packing get close enough that the residual gap can be argued away by other
    means: a chunking argument over the coarse configurations of the blocks, or a
    perturbation argument that nothing near the record can be smaller, so that the
    record is the only packing left in the interval. This report separates the two
    gaps that question conflates (side and mass), states the three lemmas that turn
    certificate slack into case analysis (tight cores, conditional certificates,
    class certificates), says what the retained first-order rigidity at Trump's pose
    already gives and what a quantified radius would add, assembles the proof shape
    those pieces would form, prices it against the only computer-assisted precedents,
    and proposes six measurements, each with the outcome that would kill the idea.
    It adjudicates nothing and promotes nothing.
  sources:
  - packing/frontier/n-011.md
  - packing/frontier/n-012.md
  - packing/frontier/n-013.md
  - packing/frontier/results.yaml
  - packing/frontier/CERTIFICATE-REACH.md
  - packing/frontier/proof-strategies.yaml
  - packing/campaign/explorations/X-003-stratified-chunk-enumeration.md
  - packing/campaign/explorations/X-007-the-n5-optimum-flexes-once-and-that-once-is-shut.md
  - packing/campaign/explorations/X-012-one-chart-four-hundred-inequalities-and-an-order-2m-contradiction.md
  - packing/campaign/explorations/X-013-where-the-certificate-should-go-next.md
  - packing/campaign/hypotheses/H-016-stock-annealer-reaches-standing-best.md
  - packing/campaign/hypotheses/H-022-trump-local-geometry.md
  - packing/campaign/hypotheses/H-034-fractional-piercing-ceiling.md
  - packing/campaign/hypotheses/H-039-s12-proof-frontier.md
  - packing/campaign/hypotheses/H-060-n5-local-rigidity.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-013-h-026-trump-tangent.md
  - packing/campaign/agendas/agenda-019-efficiency-first-retarget-and-deep-strategy.md
  - packing/campaign/ideas.md
  - packing/src/sqpack/fractional/certificate.py
  - packing/src/sqpack/fractional/ceiling.py
  - packing/src/sqpack/fractional/sweep.py
  - packing/src/sqpack/fractional/interval.py
  - packing/cases/trump11/packing.py
  - packing/cases/trump11/tangent_cones.py
  - packing/cases/n11_fractional_certificate/certificate.json
  - packing/resources/papers/stromquist-2003-packing-10-or-11-unit-squares.md
  - packing/resources/papers/bentz-2010-optimal-packings-13-and-46.md
  - packing/resources/papers/bentz-2016-optimal-packings-22-and-33.md
  - packing/resources/papers/caoduro-sebo-packing-hitting-colouring-squares.md
  - packing/resources/papers/trump-2023-packing-11-unit-squares.raw.md
  - packing/resources/web/montanher-2018-rigorous-packing-unit-squares-circle.md
  - packing/resources/web/markot-2021-improved-interval-methods-circle-packing.md
  - docs/project/research/research-2026-08-22-packing-11-unit-squares.md
  proposes: []
---
# X-014 — Closing From Both Ends: What a Narrow Gap Buys at `n = 11`, and What It Cannot

**Date:** 2026-09-04

**Status:** W3 insight-iteration exploration at the owner’s request, written on the
branch stacked on [PR #78](https://github.com/jlevy/squares/pull/78). It adjudicates
nothing and promotes nothing: no bound is proposed for adoption, no hypothesis is
registered, and no agenda cell is amended.
The three lemmas below are elementary and are proved in place; everything else is
labelled as a proposal, an estimate, or a measurement still to be made.

**Owns:** the separation of the side gap from the mass gap, the three lemmas that turn
certificate slack into case analysis, the reading of what
[exp-013](../series/series-000-smoke-and-calibration/experiments/exp-013-h-026-trump-tangent.md)
already supplies toward a quantified isolation radius, the assembled proof shape, and
the six measurements with their kill conditions.
The certificates, the ceiling theorem, the reach table and the rigidity certificates are
owned by the records this report cites.

## The Question, and the Two Gaps It Conflates

The owner’s question, in its own terms: if the lower bound keeps rising toward Trump’s
packing, is there a proof strategy in which the two get close enough that the rest can
be argued away — a chunking argument over the coarse configurations of the blocks, or a
perturbation argument that nothing near the record can be smaller — so that Trump’s
configuration is the only packing left in the interval, and the upper bound cannot get
any smaller?

The answer has a yes in it and a no in it, and both depend on distinguishing two gaps
that the question runs together.

The **side gap** is what the frontier record reports: `s(11) ∈ [3.81, 3.877084]`, width
`0.067084` after [`T-018`](../../frontier/RESULTS.md).
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

## What a Certificate Is, and the Two Places It Must Stop

The certificate in [`sqpack.fractional`](../../src/sqpack/fractional/certificate.py) is
the dual of a linear relaxation, and reading it that way is what makes the rest of this
report precise. Fix a side `L`, a shrink `B`, and a direction net.
The **covering program** minimises the total mass of a non-negative measure on the
container subject to every admissible `B`-square at a net direction carrying mass at
least `1`; its value is the covering value `τ*(L)`. Its dual is the **fractional packing
program**: non-negative weights on admissible placements whose depth — the weighted
number of placements containing a point — is at most `1` everywhere, with value `ν*(L)`.
Weak duality, proved in one line in the docstring of
[`ceiling.py`](../../src/sqpack/fractional/ceiling.py), gives `ν*(L) ≤ τ*(L)`. A
certificate exists at side `L` if and only if `τ*(L) < 11`, and a fractional packing of
value at least `11` proves that none does.

A packing of eleven unit squares is a fractional packing of value `11` with all weights
equal to `1`: each unit square contains a `B`-square at a net direction or a `D4` image
of one (conditions `C3` and `C0`), the eleven cores are disjoint, and their depth is at
most `1`. So `ν*(L) ≥ 11` at every side where eleven squares fit, and the certificate’s
reach is bounded above by `s(11)` for the trivial reason.
What the method actually reaches is the smaller of two quantities, and the record now
lets both be stated.

**Where the shrink stops it.** Scaling Trump’s packing by `λ = L / U` puts eleven
squares of side `λ` in a container of side `L`. A square of side `λ` at angle `θ`
contains a `B`-square at the net direction `θ_k` about the same centre whenever
`λ ≥ B (cos δ + sin δ)` with `δ = |θ − θ_k|`, which is the containment step of `C3`.
Trump’s six axis-aligned squares sit at direction `0`, a net direction, and need
`λ ≥ B`; the five tilted ones, at `40.181937°`, are `0.012100°` from the nearest net
direction, index `159` at `40.194037°`, and need `λ ≥ B (cos δ + sin δ) = 0.997911`. So
for every `L > U × 0.997911 = 3.868983` the scaled packing contains eleven pairwise
disjoint admissible `B`-squares at net directions — a fractional packing of value `11` —
and no certificate exists at that `L`, whatever the site set and weights.
That is arithmetic on three constants recorded in
[`certificate.json`](../../cases/n11_fractional_certificate/certificate.json), the
record’s tilt, and the formula of `C3`, not a measurement, and it is the argument of the
ceiling theorem in [`CERTIFICATE-REACH.md`](../../frontier/CERTIFICATE-REACH.md) with
the record packing in place of the grid: there the refuting object is the grid at
`4B = 3.9908`; here it binds `0.1218` lower.

Two readings follow.
The retained instrument can never certify the last `0.0081` below `U` at `n = 11`: the
shrink `B = 9977/10000` alone caps it at `U · B = 3.868166`, and the net’s offset from
the record’s tilt moves the cap up by less than a thousandth.
And the cap rises only with `B`, which `C3` ties to the net’s largest half-gap tangent
`D` through `B (1 + D) < 1`, so halving the tax needs roughly twice the directions.
The shrink is a fixed price of the instrument, about an eighth of the remaining side
gap; the covering value decides how much of the rest is reachable.

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
`s(11) ≥ 3.868983` in finitely many rungs, a finer net moves the cap toward `U` without
reaching it, and the perturbation lemma of the section after next is all that is left.

The literature the archive holds is consistent with a gap but does not decide one.
Caoduro–Sebő prove that the piercing-to-packing ratio of families of unit squares under
rotation can be as large as `3` and is never above `6`, and the 2026 counterexamples to
Wegner’s conjecture put the clique-LP integrality gap for rectangles at `5/2 − ε`; both
concern finite families given in advance rather than the covering value of a container,
so they say that a plateau below `s(11)` would be unsurprising, and no more.

## The Bridge: What a Packing Must Do to a Certificate It Does Not Refute

The first lemma is the whole of the chunking half in one counting step.
It is the complementary-slackness statement for this relaxation, and its content is that
a certificate that has stopped proving infeasibility has not stopped constraining
packings.

**Lemma 1 (tight cores).** Let `μ` be a `D4`-symmetric finite atom measure on `[0, L]²`
satisfying `C2`, `C3` and `C4` for `(B, net)`, with total mass `M`. Let `Q₁, …, Q₁₁` be
closed unit squares in `[0, L]²` with pairwise disjoint interiors.
Then there are closed `B`-squares `P_i ⊂ int Q_i`, each at a net direction or a `D4`
image of one, pairwise disjoint, with `μ(P_i) ≥ 1` for every `i`; and consequently

- `M ≥ 11`;
- `μ(P_i) ≤ 1 + (M − 11)` for every `i`; and
- `μ([0, L]² ∖ ⋃ P_i) ≤ M − 11`.

*Proof.* `C3` places a `B`-square at a net direction, or a `D4` image of one, inside
each unit square’s interior about its centre; the interiors are disjoint, so the cores
are disjoint as closed sets.
`C4` with `C0` gives each core mass at least `1` (a core at an image direction covers
the mass its reflected image covers).
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

This is a finite combinatorial question about one atom set, and it addresses the
configuration `T-018` records as the one neither pre-registered route can close:
`τ*(3.82) = 11` exactly.
There, a certificate fails by an infinitesimal and a ceiling fails by an infinitesimal,
but the packing that would have to exist is pinned to an exact cover of the heavy atoms
by eleven cores of mass one, and exact cover is decidable.
The skeleton is not the whole atom set: the retained `3.81` certificate has `1121` atoms
with weights from `3/40000` to `917/6250`, read from the file, and of those `649` weigh
more than `1/200` and carry `9.97` of its `10.86` units of mass, `289` weigh more than
`1/100` and carry `7.02`, and `93` weigh more than `1/50` and carry `4.28`. A mass gap
of a few thousandths, which is the size the rationalisation step alone introduces,
forces every atom of the heavy skeleton into a core and leaves the light ones free.

**Corollary 1b (tightness is computable cell by cell).** Covered mass is piecewise
constant in a core’s centre and changes only on the event grid, which is what makes the
exact sweep in [`sweep.py`](../../src/sqpack/fractional/sweep.py) finite.
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
arbitrary angles. Lemma 1 bridges them through `C3`, and the price is that the case
analysis in Corollary 1a runs over cores rather than over squares: a group of atoms must
fit in a `B`-square whose enclosing unit square, at any angle within the half-gap of the
net direction, is what must be disjoint from its neighbours.
Disjointness of the unit squares is strictly stronger than disjointness of the cores,
and it is the stronger condition the exact-cover search must use; eleven disjoint cores
alone would only say that eleven `B`-squares fit, which at `3.82` would give
`s(11) ≤ 3.8288` and is not known to be false.

## Branching Is Chunking: Conditional Certificates

The owner’s “major configurations of the blocks” is a branching rule.
A branch fixes something discrete about the packing — which class a square’s direction
falls in, which region its centre occupies, which contact structure the blocks form —
and what a proof needs is a lower bound valid on that branch alone.
The certificate conditions on a branch in two ways, and both are one counting step from
the unconditional argument.

**Lemma 2 (conditional certificate).** Let `b` be a set of placements of one unit square
(a box in `(x, y, θ)`), and let `I_b = ⋂_{Q ∈ b} Q` be the region every placement in the
box occupies. Take a net that spans a full quarter turn, and let `Λ_b` be the admissible
`B`-square placements at net directions that are disjoint from `I_b`. Suppose a finite
atom measure `μ` of total mass `M < 11` gives mass at least `1` to every member of `Λ_b`
and to every `B`-square at a net direction that lies inside some placement in `b`. Then
no packing of eleven unit squares in `[0, L]²` has a square in `b`.

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
container’s `D4` symmetry and `C0` can no longer fold angles onto the shorter arc; the
interval route already decides on a doubled net, so this costs a factor of two in
directions and no new idea.

**Lemma 3 (class certificate).** Partition the directions into `D4`-closed classes `Θ₀`
and `Θ₁` and fix counts `n₀ + n₁ = 11`. Suppose weights `w₀, w₁ ≥ 0` and a
`D4`-symmetric measure `μ` of total mass `M` satisfy: every admissible core at a
direction in `Θ₀` has mass at least `w₀`, every admissible core at a direction in `Θ₁`
has mass at least `w₁`, and `M < n₀ w₀ + n₁ w₁`. Then no packing has exactly `n₀`
squares with directions in `Θ₀` and `n₁` in `Θ₁`.

*Proof.* The cores are disjoint and each contributes at least its class weight.
∎

The constraints are linear in `(μ, w₀, w₁)` and the objective `M − n₀ w₀ − n₁ w₁` is
homogeneous, so the class certificate is one linear program per composition, decided by
the sign of its optimum under a normalisation.
It is the two-threshold form of `C4`, and it prices what everyone in this subject knows
informally — a tilted square costs more room than an aligned one — as a dual variable
instead of a lemma. Stromquist’s Theorem 3 is exactly a class certificate: the class is
`{0°, 45°}`, both weights are `1`, and the strengthened Lemmas 7 and 8 of his paper are
the covering condition restricted to that class.
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
at side `s` at most nine squares of any packing are within `θ₀(s)` of axis-parallel,
where `cos θ₀ + sin θ₀ = 4/s`: `1.85°` at `U` and `2.77°` at `3.82`. At every side below
`U`, then, at least two squares are tilted by more than `1.85°`, and the compositions
`n₁ ≤ 1` for a near-axis class of half-width `1.85°` are closed by nine points.
Trump’s packing has five such squares, so the fact is consistent rather than sharp; its
value is as the template, since a class certificate is a covering condition restricted
to a class and the classical lemmas are the special case where the covering is by
points.

The branching order this suggests is the chunking the owner described, made discrete:

1. **Composition.** Twelve class certificates, one per `n₁ = 0, …, 11` tilted squares
   for a near-axis class `Θ₀` of half-width `α`. Nine points close `n₁ ≤ 1` at every
   side below `U` for half-width `1.85°`; the grid that proves the ceiling caps every
   near-axis class at `4B`; Stromquist’s Theorem 3 is the evidence that compositions far
   from Trump’s close above `U`; the compositions near Trump’s, with five squares tilted
   near `40°`, cannot close and are refined.
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
half-planes `interval.DirectionSearch` propagates, and each of the three assumes that
domain is convex, which a container minus `I_b` is not.
Lemma 3 needs none of that — it changes the right-hand sides and the objective of the
covering program and nothing geometric — which is why the composition step is the cheap
one and the place to test whether conditioning buys anything at all.

The symmetry bookkeeping is standard.
A minimal packing has a square touching each container wall, or the container could
shrink; labels are broken by ordering the squares, and the container’s eight symmetries
by fixing which wall the lowest square touches.
Montanher and co-authors do this for squares in a circle by tiling the centre domain
into isosceles triangles of base below `1`, each holding at most one centre, and
iterating over tile combinations one square at a time so that infeasible small
combinations kill their supersets; at `n = 3` that was `6`, `43` and `12` subproblems
out of `7140` combinations.
The same device applies here unchanged.

## The Perturbation Half: What Exp-013 Gives, and the One Number It Lacks

The perturbation half of the owner’s question is that one cannot move Trump’s squares a
little and get a smaller container.
The record already proves that qualitatively, and it is worth being exact about what is
proved, because the quantified version is the easy case rather than the hard one.

[exp-013](../series/series-000-smoke-and-calibration/experiments/exp-013-h-026-trump-tangent.md)
works at Trump’s exact pose over `Q(u)`: 33 pose variables, 11 square–wall incidences
contributing 20 tied-corner rows, 14 pair contacts contributing 24 raw separating
features, `512` raw feature selections reducing to `128` derivative-distinct `42 × 33`
matrices, every one of exact rank `33` with a strictly positive stress `λ` and
`Aᵀλ = 0`. So every branchwise linearised cone at fixed side is `{0}`. The finite-branch
subsequence argument in that record then gives local isolation at fixed side and,
because a nearby packing in a smaller container would also fit Trump’s, strict local
minimality of the side in the anchored pose–side chart.
What it does not give is a radius, and
[`H-022`](../hypotheses/H-022-trump-local-geometry.md) carries that as an open leg.

A branch-and-bound needs the radius, and needs it with the side free.
The statement it consumes is: *there is `ρ₀ > 0` such that no pose within `ρ₀` of
Trump’s, in the sup norm of the anchored chart, is a packing at any side below `U`, and
the only one at side `U` is Trump’s.* That is the box around Trump’s pose that the tree
may stop refining. The first-order certificates give it, and the derivation is short
enough to state:

- **Modulus.** For branch `b` with matrix `A_b`, put
  `κ_b = min { max_j (−(A_b v)_j) : ‖v‖_∞ = 1 }`. Because the cone is `{0}`, every unit
  `v` violates some row strictly, and compactness makes `κ_b > 0`. It is `66` small
  linear programs per branch (one per face of the unit cube), `128` branches, floats
  proposing and exact arithmetic confirming, which is the pattern
  [`tangent_cones.py`](../../cases/trump11/tangent_cones.py) already uses.
- **Curvature.** Every active constraint is a corner coordinate against a wall or a
  corner of one square against an edge of another; each is a polynomial in the centres
  and in `cos θ_i, sin θ_i`, so the sum of the absolute second derivatives of any one of
  them, in the chart’s coordinates, is bounded on any box by a constant `K` computable
  by hand.

Then for a pose `z* + v` at side `U + σ` with `σ ≤ 0` in branch `b`, every active row
reads `a_j · v + σ e_j + R_j(v) ≥ 0`, where `e_j` is `1` on the two far walls and `0`
elsewhere and `|R_j(v)| ≤ (K/2) ‖v‖²`. Since `σ e_j ≤ 0`, every row has
`a_j · v ≥ −(K/2) ‖v‖²`, while the modulus supplies a row with `a_j · v ≤ −κ_b ‖v‖`; so
`v = 0` or `‖v‖ ≥ 2 κ_b / K`, and at `v = 0` a far-wall row reads `σ ≥ 0`. Hence in the
open ball of radius `ρ₀ = min_b 2 κ_b / K` the only packing at side at most `U` is
Trump’s pose at side exactly `U`. The finitely many `D4` images and relabellings of the
pose are excluded by shrinking `ρ₀` below half the distance to the nearest of them, and
the selection of a branch is sound for the reason exp-013 gives: a feature with a
strictly negative gap at the pose cannot separate a pair nearby, so a nearby packing is
separated by features active at the pose, which is one of the `512` raw selections.
Inside the ball the side grows linearly, `σ ≥ κ_b ‖v‖ − (K/2) ‖v‖²` along every feasible
direction, which is what `T-3`’s kink already showed on one slice, with one-sided slopes
`0.175` and `0.384` at the record tilt.

The stress adds a coarser statement that reaches farther.
Summing the rows of branch `b` against `λ_b` kills the linear terms, because
`λ_bᵀ A_b = 0`, and leaves `σ Λ_b + Σ_j λ_j R_j(v) ≥ 0`, where `Λ_b` is the stress
carried by the far-wall rows; so `σ ≥ −C_b ‖v‖²` with `C_b = ‖λ_b‖₁ K / (2 Λ_b)`. A
packing at side `U − η` therefore sits at distance at least `(η / C)^{1/2}` from the
pose, with `C = max_b C_b`, on the whole ball where the branch enumeration and the
curvature bound hold.
So the box the tree may discard around Trump’s pose at target side `U − η` has radius
`max(ρ₀, (η / C)^{1/2})`: never smaller than `ρ₀`, and widening as the square root of
the distance below `U`, which is the direction a ladder of rungs wants.

The `n = 5` case shows why the first-order certificates are the easy route.
There the first-order cone was a line — the middle square rotates — and closing it took
the order-`2m` Puiseux argument of
[X-012](X-012-one-chart-four-hundred-inequalities-and-an-order-2m-contradiction.md),
because a flex has no modulus.
Trump’s pose has no flex in any branch, so the modulus exists and the argument above is
the classical one for a nonsmooth strict local minimum.

Two cautions. The numbers `κ_b` could be small — the stresses exp-013 retained are
proposed by a floating linear program with nine free weights and completed exactly, and
nothing in the record says how well conditioned the `42 × 33` systems are — and `ρ₀`
scales with `κ_b / K`, so a modulus of `10⁻³` against a curvature of a few units puts
the local box at a few times `10⁻⁴` in the chart; `C_b` depends on which stress is used,
and the ratio `‖λ_b‖₁ / Λ_b` can be minimised over the branch’s stress cone by another
linear program, which the retained stresses were not chosen for.
That is the number that decides whether the local lemma meets the certificate half way
or leaves a band between them; it is a computation of an afternoon, and it is the second
measurement proposed below.
And Trump’s own 2023 note says, in the record’s raw transcription, that the packing
“cannot be improved by computer programs as long as the same geometrical arrangement of
the unit squares is used” — the exact scope of every local result here, including a
quantified one. A radius does not touch a different arrangement.

## Assembling a Proof, and Where It Would Be Expensive

Put together, the pieces form one proof shape, the one the computer-assisted packing
optimality proofs in the archive share: a tree over discrete choices, a bound on each
node, and a local lemma at the leaves that contain the optimum.
What is specific here is which tool works at which scale.

| Scale | Tool | Status here |
| --- | --- | --- |
| Coarse: composition, angle bins, forced regions | Class certificates (Lemma 3), conditional certificates (Lemma 2), tight-core census (Corollary 1b) | Unconditional certificates retained; Lemma 3 is a right-hand-side change; Lemma 2 needs the domain generalised in four files |
| Intermediate: boxes near Trump’s pose larger than `ρ₀` | Fixed-angle cell LP (`T-2`) over angle boxes, with interval propagation on the 34-variable system | The cell LP exists exactly; the interval propagation exists only in Montanher’s `n = 3` code, not here |
| Fine: the box of radius `max(ρ₀, (η / C)^{1/2})` at target side `U − η` | Quantified modulus and stress lemmas above | First-order certificates and stresses retained; `ρ₀` and `C` not computed |

The narrow gap enters in a way the question did not anticipate: it is produced, not
assumed. Run the tree at side `L₁` slightly above the ladder’s top and it proves
`s(11) ≥ L₁`; at `L₂ > L₁` it proves more and costs more, because the `ε`-tight sets
fatten and the near-Trump band widens while the discard radius `(η / C)^{1/2}` shrinks
toward its floor `ρ₀`; the last rung, at `U − η` for small `η`, is where the modulus
lemma carries the whole local weight, and it is the one that reaches `U` exactly and
proves uniqueness on the way — every packing at side `U` lies in the box, and in the box
the pose is isolated.
Each rung is a publishable bound, exactly as each certificate rung is now.

Where it would be expensive is the intermediate scale, and that is where the estimate is
least certain.

- **The band between the tools.** At side `U − η`, a box at pose-distance just above the
  discard radius `(η / C)^{1/2}` contains configurations whose side the stress bound
  allows to come within `η` of the target; the covering program sees such a box as
  nearly feasible, and whether its conditional value crosses `11` there is exactly the
  question no run has asked.
  If the certificate half reaches down to `10⁻¹` and the local lemmas reach up to
  `10⁻³`, the band between them is two orders of magnitude of pose scale in a
  34-dimensional chart, and the cell LP with interval propagation is what would have to
  fill it. If the two meet, the middle tier is empty and the proof is the coarse tree
  plus one lemma.
- **Other near-optimal arrangements.** Every local minimum of the side within the band
  the certificate cannot see needs its own box and its own local lemma.
  The search record is weak evidence that there are none close to `U`: the stock
  annealer returns `3.9144` on every seed
  ([H-016](../hypotheses/H-016-stock-annealer-reaches-standing-best.md)), Gensane and
  Ryckelynck report re-finding Trump’s packing “several times” from random starts, and
  the 2026 SCIP run from scratch lands on `3.87709`. A search that finds nothing
  certifies nothing, and this is the second-largest unknown in the cost.
- **Rotational degrees of freedom.** Markót’s interval method proves circle packings
  optimal at `n = 31, 32, 33` in `26`, `61` and `13` CPU hours on a laptop, with
  tile-pattern filtering over about `10¹²` tile combinations; the only rigorous result
  for rotating unit squares in any container is Montanher and co-authors' `n = 3`, and
  the `n = 11` report in this repository correctly calibrates against it: “do not target
  `s(11)` with a rigorous solver.”
  The one thing that changes that calibration is that the covering program is a bound
  the interval solvers lack: it prunes coarse boxes by a global counting argument rather
  than by local propagation, and the ratio band `[0.98171, 0.98270]` of
  [X-013](X-013-where-the-certificate-should-go-next.md) says it reaches `98%` of the
  record unconditionally.
  How much of the remaining `2%` conditioning buys is the measurement, not the argument.

## `n = 12` Is a Different Proof

The owner’s question was asked about Trump’s packing, and the answer changes shape at
the next case, which is worth recording because the record already calls `n = 12` the
more tractable target.

The conjectured optimum is the grid at `4`, and the retained witness is not rigid: the
translation-escape screen in [`n-012.md`](../../frontier/n-012.md) slides one square a
full unit with the packing still valid, and twelve squares in a `4 × 4` frame with four
empty cells form a positive-dimensional family, not a pose.
So there is no modulus lemma at `n = 12`; the perturbation half of the argument has
nothing to attach to.
What replaces it is the classical box method — Nagamochi’s and Bentz’s resource
starvation at sides just below an integer, which proved `s(13) = 4` with two placements
of the corner-restricted boxes and four critical regions — and that method works with
squares of side exactly `1` and directions quantified continuously, which is precisely
what the shrink gives up.
The ceiling theorem says the retained instrument stops at `4B = 3.9908`, and with
`B (1 + D) ≈ 1` for this net the whole loss is `B` itself: a finer net raises the
ceiling only as fast as it raises `B`, and it never reaches `4`.

The chunking half, by contrast, is stronger at `n = 12` than at `n = 11`. At side below
`4` no arrangement of axis-parallel squares holds more than nine, so at least one square
is tilted, and the composition step of Lemma 3 is the natural first cut: the `n₁ = 0`
class is capped at `4B` by the same grid and is where a class ladder would be expected
to reach highest, and every other composition is a certificate conditioned on how many
squares tilt. The last sliver is where `BC-193` of
[agenda-019](../agendas/agenda-019-efficiency-first-retarget-and-deep-strategy.md) asks
what a method that escapes the ceiling would look like, and Lemma 1 suggests the answer:
drop the shrink, put `B = 1`, and decide `C4` over the continuum of directions by an
interval branch and bound in the three parameters of one placement — the decision
problem the `n = 11` report already lists as “well inside the reach of interval
branch-and-bound.” With `B = 1` the refuting grid needs side exactly `4`, the ceiling
becomes the grid bound itself, and the only obstruction left is whether the covering
value at `4 − δ` sits below `12`, which is the `n = 12` instance of the first
measurement below.

The natural first test at `n = 12` is to mechanise one of Bentz’s own cases: box the two
corner-restricted squares of his non-adjacent configuration at a side just below `4`,
take their forced points as cores, and ask the conditional program to close the case —
the sixth measurement below.

## Verdict

Worth pursuing, as a measurement program before it is a proof program.
The two mechanisms the owner named are real: the mass gap turns into a finite case
analysis by Lemma 1, and the sliver below Trump’s value turns into a computable box by
the modulus lemma. Neither is speculative and neither is expensive on its own.
What is unknown is the size of the tree between them, and that size is set by three
numbers nobody has measured: where the covering value crosses `11`, how large the
tight-core set is there, and how large `ρ₀` is at Trump’s pose.
Two of the three are an afternoon’s computation each.

| # | Measurement | Instrument | Kills the idea if |
| --- | --- | --- | --- |
| 1 | `ν*(L)` at `L ∈ {3.82, 3.85, 3.87}`: a fractional packing with depth at most `1` at every arrangement vertex, by cutting planes on the `3.82` dual | `sqpack.fractional.ceiling` as the depth oracle; the column generator’s site loop in reverse | Nothing kills it; either outcome sets the ladder’s top and the tree’s working side |
| 2 | `κ_b` and `Λ_b / ‖λ_b‖₁` for all `128` branches, a curvature bound `K`, and the resulting `ρ₀` and `C` | `cases.trump11.tangent_cones` for the matrices; `66` linear programs per branch; exact confirmation | `ρ₀` below `10⁻⁶` in the chart: the local box is too small for any tree to reach |
| 3 | Census of event cells with mass at most `1 + ε`, `ε ∈ {0, 0.01, 0.05, 0.1}`, per direction, on the retained `381/100` certificate and on the `3.82` atom set once regenerated | A per-cell readout of the mass grid `sweep.minimum_covered_mass` already fills | The tight set at `ε = 0.05` covers most of the centre domain: the mass gap constrains nothing enumerable |
| 4 | Twelve class certificates at side `U`, one per composition `n₁`, near-axis half-width `α = 5°` | Lemma 3 as a right-hand-side change to the covering program; no geometry changes | The `n₁ = 0` class fails to certify above `U`: conditioning on direction buys too little |
| 5 | The handshake: one conditional certificate at side `U − 0.01` with all eleven squares boxed at radius `0.05` about Trump’s pose | Lemma 2 after the domain generalisation; time one node first with a coarse net, since a tree of nodes that cost hours each is not a plan | The conditional value stays at or above `11`: the certificate cannot reach down to where the modulus lemma reaches up, and the middle tier is not empty |
| 6 | The `n = 12` analogue: Bentz’s non-adjacent corner-restricted configuration at side `399/100`, with the two corner-restricted squares boxed and their forced points as cores, as a conditional certificate | Lemma 2 after the domain generalisation | The boxed case still returns mass at or above `12`: conditioning cannot close even a case the classical method closes by hand |

The order is the order of cost, and the first three need no new soundness surface: the
first is the ceiling instrument run to convergence, the second is exact linear algebra
on retained matrices, the third is a readout the sweep already computes.
The fourth, fifth and sixth are the first that touch the certificate’s conditions, and
they should go through the same retention gate as every certificate does — frozen bytes,
two routes, agreement on the value — before anything is claimed from them.

## If This Argument Is Wrong

The strongest case against it is that the covering value has no plateau at all: that
`τ*(L) < 11` up to the shrink cap `3.869`, so that the ladder never needs help and
Lemmas 1 through 3 are never needed for the bound.
That would be good news for the bound and would leave the modulus lemma as the only part
of this report worth building.
The first measurement decides it.

The second-strongest is that the tree’s middle tier is not empty and is large — that
`ρ₀` comes out at `10⁻⁵` while the conditional certificate stops helping at `10⁻¹` — and
that filling the band needs exactly the 34-variable interval propagation the `n = 11`
report warns against.
The second and fifth measurements decide that, and if they do, the correct reading is
that the certificate ladder should be pushed as high as it goes, the modulus lemma
should be recorded as the quantified rigidity result `H-022` asks for, and the case
analysis between them should be left for a method that does not exist yet.

The third is that Lemma 1’s case analysis is finite but not small: that the tight set at
the ladder’s top is thousands of cells with no cluster structure, so that the
exact-cover search of Corollary 1a is a search rather than a check.
The third measurement decides that, and a fat tight set would also be evidence that the
fractional optimum at that side is far from any integral configuration — which is what
an integrality gap looks like from the inside, and is itself worth knowing.

## What This Document Does Not Establish

No bound is proved, proposed, or estimated beyond arithmetic on recorded constants.
The three lemmas are elementary consequences of the certificate conditions and are
proved here; nothing built on them exists.
The modulus lemma’s derivation is sketched and its constants are not computed.
The tree’s size is not estimated because the three numbers that would set it are not
measured, and the ratio band of X-013 is quoted as the record’s own extrapolation, with
that report’s qualifications attached.
No hypothesis is registered, no agenda cell is amended, and the six measurements are
proposals for whoever runs the next block, not commitments.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
