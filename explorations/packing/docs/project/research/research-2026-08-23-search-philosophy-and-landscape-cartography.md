# Research: A Search Philosophy for Square Packing

**Date:** 2026-08-23 (last updated 2026-08-23)

**Author:** Claude (agent), for samanthadrakova@gmail.com

**Status:** Complete

## Overview

The five prior reports establish what is known about `s(n)`, how packings are computed
and verified, and what infrastructure to build.
The
[standing review](../reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md)
adds the experimental method: a hypothesis register with kill criteria, a run protocol,
and a series plan.
None of them answers the question the machinery raises once it exists:
**where should search effort point, and why should pointing beat scaling?**

This document is that strategy layer.
It captures a design discussion at agenda level — philosophical and structural
directions, written down *before* being reduced to experiments, so the general shape of
the research agenda is on record and criticizable on its own terms.
Each direction ends at a pointer into the review’s hypothesis register, where it is
boiled down to a test with a budget tier and a kill criterion (H-11 through H-15, series
S6). Nothing here spends budget; everything here says what budget would be for.

The working thesis, in one paragraph.
The instances worth winning may be ones a named volume-weighted search reaches rarely.
Record packings often appear highly constrained, but neither rigidity nor rare
attraction under the current proposer has been established as a general implication;
H-012 exists to measure the latter under a declared regime.
If that measurement supports the thesis, the response is not merely a faster random
walk. It is, in order: treat the set of local optima as the object of study — a **basin
atlas** built over the exact LP-quench map the review already validated; steer search by
**structural diversity under the true objective** rather than by reshaping the loss; put
the LLM at the **structural layer**, where it reads verified maps and writes constructor
programs, never coordinates; approach the hard instance along **relaxation ladders** —
families of easier problems connected to it by continuation; and calibrate on instances
that share the record’s **mechanism**, not merely its difficulty.
On this view the map is the deliverable and records are corollaries — which is also the
posture under which a search program produces publishable artifacts even in the likely
case that no record falls.

## Questions to Answer

1. Why should blind annealing be expected to fail precisely at record-quality packings —
   and what does that imply about scaling it?
2. What is “the map of the structure of the minima” for this problem, concretely, and
   what already-validated machinery builds it?
3. Should the loss function change?
   If not, what replaces loss-shaping as the way to steer search toward rare
   configurations?
4. Where can an LLM contribute to search *as an LLM* — and what discipline keeps its
   contributions honest?
5. Can generalizing or relaxing the problem buy structural intuition and shrink the
   space that has to be searched?
6. Which instances calibrate record-finding ability, as opposed to machinery
   correctness?

## Scope

Included: strategy for the search program — the failure mode of volume-weighted search,
landscape cartography, diversity-based steering, the LLM’s role, relaxation families,
and mechanism-matched calibration, each with its precedent and its register pointer.

Excluded: implementation (the
[infrastructure synthesis](research-2026-08-22-infrastructure-for-packing-exploration.md)
and the [plan spec](../specs/active/plan-2026-08-22-minimal-packing-toolkit.md)), the
proof-lane machinery as such (the
[Lean study](research-2026-08-22-lean-for-packing-proofs-and-validation.md)), and
concrete run design (the review’s register and series — the boil-down of this document
lives there, not here).

Precedents below are drawn from energy-landscape science and quality-diversity
optimization. They enter as *strategy precedents* — reasons to expect a direction to be
productive — not as facts about this problem’s landscape.
Every expectation transferred from them is restated as a falsifiable hypothesis with a
kill criterion before any budget is spent on it; that restating is what the register is
for.

## Findings

### The hypothesis: the baseline proposer may rarely enter record components

Start from what the exact verifier measured.
In Trump’s `n = 11` packing, 14 of the 55 square pairs touch with *exactly zero* gap,
and 20 corner coordinates lie on the container boundary in the exact witness.
Those contacts make the packing a strong rigidity candidate, but raw contact counts do
not establish independence or infinitesimal rigidity; that requires a rank or interval
certificate that the repository does not yet have.

What matters for search is not the stratum (measure zero) but its **basin of
attraction** (positive measure, but how much?). Here the energy-landscape literature has
a well-worn expectation: annealing-class methods sample basins roughly in proportion to
their volume at the sampling temperature, so they find the funnel whose *entropy* wins,
not the funnel whose *optimum* wins.
The canonical cautionary example is the 38-atom Lennard-Jones cluster, whose global
minimum (an fcc truncated octahedron) sits at the bottom of a narrow funnel beside a
broad icosahedral funnel that captures almost every unbiased run — the double-funnel
landscape of Doye, Miller and Wales.
Glassy systems generalize the lesson: when low-energy states are rare and structured,
volume-weighted dynamics is systematically worst exactly where the prize is.

Square packing has one suggestive proposer-specific observation: Ellsworth reports 3,004
basins from his `s(51)` search and four refinements to the record.
That frequency belongs to his proposal and refinement regime; it is not an intrinsic
volume of the packing landscape.
The idea that loosely constrained grid-like arrangements have larger attraction sets
than oblique cores is a hypothesis to measure, not a consequence of contact count.

If H-012 confirms a small hitting probability for a named baseline, throughput merely
multiplies samples against that measured probability.
If it does not, this strategic argument contracts and throughput remains competitive.

This is the strategy layer’s load-bearing premise, so the register is arranged to test
it first and cheaply: H-12 measures the record basin’s quench probability directly at
`n = 10` and `n = 11`. If the premise is wrong — if record basins turn out to be hit at
rates comparable to the modal basin — this document’s program contracts sharply, and
that outcome is deliberately made cheap to reach.

### The provisional quench map: endpoint keys are not yet terminal components

The review’s verified result (R-2) supplies the tool this whole approach stands on.
Fix each square’s angle and, for each pair, which candidate axis separates it, and
minimizing `s` becomes a **linear program**; the configuration space partitions into
combinatorial *cells*, and solving the cell’s LP takes any float configuration to a
floating-point optimum of its cell at the solver’s precision.
At Trump’s angles this reproduced `s(11)` and every centre to machine precision.

That resembles the **inherent-structure decomposition** of Stillinger and Weber — a
quench map sending configurations toward terminal structures — but two qualifications
are load-bearing here.
The current LP solve is floating-point at the polished tier, not an exact certificate,
and terminal structures need not be discrete.
At `n=3`, the side-2 optimum contains a connected sliding family: centres `(1/2,1/2)`,
`(3/2,1/2)`, and `(t,3/2)` for `t in [1/2,3/2]`. One further caveat the same build
produced: a quench whose angle search merges nearby angles returns the optimum of a
*constrained* problem, so its landing point — and hence basin identity, which the atlas
defines as where the quench lands — would inherit a tuning parameter
([D-020](../../../defects.md), now fixed by a free-angle pass that checks
coordinate-wise stationarity under the declared schedule and tolerances).
The lesson generalises: **whatever defines a basin must be independent of the search’s
own knobs**, and that has to be checked rather than assumed.

Combined with the review’s canonical identity keys (R-1: contact graph up to
isomorphism, `D4`-canonicalized geometry), a numerical endpoint becomes a reproducible
comparison candidate.
It becomes a basin/component only after convergence, local stationarity, isolation or
connected-component identity, validity, and numerical ambiguity are resolved.

Two consequences frame everything downstream:

1. **Each fixed separating-axis cell exposes a lower-dimensional continuous problem.**
   Trump’s packing uses one non-trivial tilt and the `s(17)` record uses two, but those
   two cases do not establish that record packings generally have few raw orientation
   classes. The primary `n = 29` SVG is already a counterexample candidate to the
   registered three-class bound.
   The useful question is effective angular dimension— rank, algebraic dependence, or
   compressibility—rather than a universal class count.
2. **Declared landscape views can become statistical questions.** Under a versioned
   proposer, quench, and terminal-component relation: how much component support was
   observed; what unseen mass remains; what polished or exact side evidence each
   component carries; and which cells are adjacent.
   These are conditional census questions with uncertainty — see H-11.

#### The correction: exactly valued does not mean discrete

Consequence 2 does not follow from consequence 1, and the gap between them is
[D-034](../../../defects.md).

The exact `n=3` optimum supplies the counterexample directly: centres `(1/2,1/2)`,
`(3/2,1/2)`, and `(t,3/2)` for `t in [1/2,3/2]` form one connected side-2 family.
The current contact certificate is constant on sampled members while the geometric key
changes, so the atlas count depends on its quantum.

The `n=5` golden gives a second, unresolved signal: two rows share side, short form,
contact certificate, angle signature, and contact count while differing geometrically.
The merged branch originally called this a five-dimensional family by subtracting 11 raw
contacts from 16 variables.
That subtraction is not a rigidity-rank calculation, and matching side/contact data do
not prove path-connectedness.
They establish an identity ambiguity that must be measured, not its answer.

**The LP supplies one useful test, not the whole definition.** Within one fixed-angle,
fixed-separating-cell LP, the optimal-face dimension can be computed from the rank of
the active constraint matrix and objective row.
The full quench also moves angles and crosses cell/contact strata, so component identity
requires the full active-constraint Jacobian, null-direction continuation, and a rule
for joining boundary strata.
Until those checks run, the `n=5` pair remains unresolved and the safe artifact is an
endpoint-key map with lower/upper component-count bounds.

That reframing keeps D-034 as a blocker with executable work.
`think-1s0h` and `think-0yo9` must be reconciled around the exact `n=3` control,
rank/nullity evidence, and continuation rather than contact counting.

**The lesson, restated one level up.** This section already said *“whatever defines a
basin must be independent of the search’s own knobs, and that has to be checked rather
than assumed”* — the D-020 lesson.
D-034 is the same sentence with a wider referent: a basin must also be independent of
the **representation’s** knobs, and must not presume a structure — discreteness — that
the mathematics does not supply.
The first version of that lesson was learned and written down; the second was available
from the same argument and was not.

### The map itself: a basin atlas, and what it buys both lanes

“A map of the structure of the minima” has an established form: the **disconnectivity
graph** of Becker and Karplus, popularized by Wales — minima as leaves, joined at the
lowest barrier connecting them, giving the landscape’s tree structure at a glance
(funnels are visible as long unbranched spines).

Our target, concretely: an **atlas** with one record per resolved terminal component —

- both endpoint keys (geometric and structural), together with component-identity
  evidence, per the review’s R-1 and D-034;
- the polished side and, where separately certified, the exact side and algebraic
  degree;
- hit frequency under a versioned proposer `P`, quench `Q`, and terminal equivalence `E`
  (an empirical probability conditional on `P/Q/E`, not an intrinsic volume);
- the contact graph and angle signature;
- symmetry group of the packing;
- neighbor links: which basins it merges with, and at what container inflation `δ` — the
  natural barrier scale here, and (deliberately) the same quantity the δ-ladder below
  computes anyway.

The atlas pays four ways.
It is **steering data** — the review’s H-3 (rarity versus contact count) becomes a
readable chart instead of a conjecture.
It gives **negative results semantics** — “searched to saturation” (R-4) becomes “found
this fraction of the atlas, with the discovery curve attached.”
It is a **transfer corpus** — mechanisms visible across `n`, which is how the human
record table actually advances (R-6). And it connects to the proof lane:
Stromquist-style optimality proofs are, under the hood, exhaustive case analyses over
structural families of configurations, so **a complete small-`n` atlas is the empirical
shadow of the case tree an eventual proof must walk.** Cartography is the one search
artifact the proof side can inherit directly.

Hence the reframing this document recommends adopting explicitly: **the map is the
deliverable; records are corollaries.** A campaign that produces a validated atlas of
the `n ≤ 11` landscape has produced the field’s first such object — publishable,
reusable, and proof-adjacent — whatever happens at the record line.
That removes the program’s dependence on luck, which is what a strategy is for.

The census starts at `n ≤ 10`, where the landscape is believed simple and the answers
are proved, so atlas machinery is validated against ground truth before it is pointed at
`n = 11` (H-11).

### Steering: keep the loss, change what you keep

The obvious response to “the objective doesn’t reward what we want found” is to change
the objective: add a bonus for contacts, for tilt, for whatever records look like.
Two things are wrong with it.

First, **auxiliary losses are hackable, and this problem hacks them immediately.** The
most contact-rich arrangements are grid-like — full-edge contacts everywhere — so a
naive contact reward steers search *into* the wide grid funnel, the exact opposite of
the intent. Note the trap’s shape, because it recurs: the grid is high-contact *and
common*; the record is high-contact *and rare*. Any single scalar that both share cannot
separate them.
(This also reconciles H-3 with the hackability point: H-3 is a claim about
*retention* — among basins already found, rarity tracks contact count — not a license to
reward raw contact count during sampling.)

Second, a reshaped loss **changes the minimizers**: what the search then finds relates
to the auxiliary objective, not to `s`, and the exact layer can no longer say what the
result means.

The alternative with an actual track record keeps the objective and changes *what is
retained*: **quality-diversity search**. A MAP-Elites archive keyed by structural
descriptors — keep the best-`s` packing in every descriptor cell — spreads search
pressure across *structure* instead of piling it into the biggest basin; this is Mouret
and Clune’s “illumination,” and its degenerate cheap version is novelty/taboo on
canonical basin keys: **never pay twice to rediscover a basin you have already named.**
The atlas makes both implementable, since canonical keys and descriptors are exactly
what its records carry.

The intelligence, and the risk, concentrate in **descriptor design**. Descriptors must
be computed from verified canonical data (not from raw float state), must be axes of
*mechanism* — distinct-tilt-class count, oblique-core size, boundary versus interior
contact split, gap topology — and must be used in combinations that separate the grid
funnel from oblique and record-like structures (tilt-class count × contact class, at
minimum; the grid has maximal contacts but zero non-trivial tilt classes).
The descriptors are discovery coordinates, not a claim that rigidity predicts rarity.
This is the honest version of the “different loss functions” instinct: same loss,
different retention rule, measurable either way (H-15).

### The LLM’s lane: read the atlas, write constructors, never coordinates

Continuous fine-tuning of 34 coupled coordinates is where a language model contributes
least; discrete structure, analogy across instances, and program-writing are where it
contributes most. Three roles, in dependency order:

1. **Atlas reading.** Qualitative analysis over the verified per-basin descriptors: what
   mechanisms recur where; what is conspicuously absent at `n = 11` relative to its
   neighbors; which descriptor cells are empty and whether emptiness looks structural or
   just unexplored. The output is candidate structures and moves — and because every
   candidate can be instantiated, LP-polished, and exactly verified, the model’s
   opinions convert immediately into machine-testable hypotheses rather than prose.
2. **Constructor induction** (the FunSearch shape).
   Search over a small DSL of packing constructors — lay a grid block, insert an oblique
   core of `k` squares at angle `θ`, straighten a row, splice two records — whose
   semantics *end in LP polish plus exact verification*. The model proposes programs;
   the evaluator is exact; the model is thereby forced away from the two things it is
   bad at (writing optimizers, emitting coordinates) and toward the thing it is good at
   (compositional structure).
   The record catalogue’s own annotations — “extends the `s(17)`…”, “two copies of the
   `s(50)`…”, “with 2 squares removed and 8 straightened” — read as a starter corpus for
   exactly this grammar.
3. **Cross-`n` transfer.** Mechanisms, not coordinates, moved between instances — the
   field’s dominant productive move (R-6/H-4), done deliberately with the atlas as the
   source of mechanisms.

The discipline that makes any of this safe is already house policy, and it has a
parable: the **phantom `10⁻¹⁰⁰`** — two published secondary sources agreeing on an
explicit constant that the primary paper does not contain.
Consensus among fluent texts is not evidence, and a model generates fluent text cheaply.
So: nothing enters a prompt that has not been machine-verified, and nothing leaves a
model into the atlas or the corpus without passing the exact layer.
The reason this rule is *affordable* is the same LP-quench exactness as everywhere else
— verification of a proposed structure costs milliseconds, so the model can be wrong at
high frequency and still be useful.
The LLM lanes therefore wait on the atlas existing (there must be something verified to
read); the DSL can be designed on paper in parallel.

### Relaxation ladders: continuation from easy problems into the hard one

The user’s instinct in the source discussion — *generalize the problem a little, get a
feel for the space, use it to shrink what must be searched* — has a standard
mathematical form: embed the hard instance in a one-parameter family whose far end is
easy, then **track solutions along the parameter** instead of searching for them cold.
Three ladders fit this problem, each watching for different events on the way.

| Ladder | Parameter | Easy end | Hard end | What to watch |
| --- | --- | --- | --- | --- |
| Container inflation | slack `δ` in side `s* + δ` | large `δ`: few, broad basins | `δ → 0`: the true instance | basin splits and vanishings (a bifurcation tree); merge-`δ` between basins = the atlas’s barrier scale; the `δ` at which the record basin appears |
| Superdisk shape | exponent `p` in `\|x\|^{2p} + \|y\|^{2p} ≤ 1` | `p = 1`: circles — orientation-free, mature literature | `p → ∞`: squares | where orientation symmetry breaks; which circle structures survive to the square end |
| Boundary-layer reduction | frozen grid bulk | the pure grid | grid plus a sheared band (the Cleemann mechanism) | whether any band re-synchronizes with the bulk at `m² − 3` |

**Container inflation** (equivalently, by scaling: shrink the squares slightly in a
fixed container) is the primary ladder.
At generous `δ` the landscape is simple and search is trivial; walking `δ` down with an
LP re-polish at every step is cheap path-following; and the recorded events are the
intuition, made durable: which basins die, which split, and at what `δ` the record’s
basin first exists as a distinct attractor.
Three payoffs from one computation: a search method that can *walk into* basins direct
sampling never hits (H-13); the merge-`δ` barrier estimates the atlas wants anyway; and
a scalar hardness measure per instance — “how much slack makes `n = 11` easy” is a
well-posed, reportable number.

**Superdisk continuation** makes “a square is a circle with orientation” quantitative.
Circle packing in a square is far better understood — proved optima into the dozens,
strong conjectured records beyond — and Jiao, Stillinger and Torquato’s superdisk
packings are the precedent that optimal structure deforms informatively along `p`. The
square-specific phenomena (edge alignment, tilt mechanisms) must *emerge* somewhere on
the path as orientation starts to matter; where they emerge, and which circle structures
they grow from, is structural information no amount of square-only search provides
(H-14).

**Boundary-layer reduction** is, strictly, a reduction rather than a relaxation:
restrict the configuration space to a structured slice — grid bulk frozen, a band of
squares free to shear and re-synchronize — because at the `m² − 3` frontier
(`n = 61, 78, 97`) everything the corpus knows says that if the conjecture fails at all,
it fails by exactly that mechanism (it is how Cleemann’s 272 killed the `n² − n`
family). The risk is stated plainly: the slice may exclude the true optimum.
The compensation: the dimension drops from `~3n` to `~3 ×` (band size), any find is
still a record, and the slice is where the review’s H-5 analytic attempt already lives.

Common shape of all three: **rare-event search becomes path-following plus event
detection**, and the events — bifurcations, symmetry breaking, re-synchronization — are
recordable artifacts rather than vibes.

### Calibration must match mechanism, not just difficulty

The review’s calibration ladder (R-3: `n = 5` and `n = 10`, both proved) is necessary
and stays — but it validates *machinery*, not *strategy*. Both proved optima are
45°-tilt mechanisms: symmetric, easily found, sitting in basins blind search reaches
without help. An engine can ace that ladder and remain structurally blind to what
`n = 11` actually demands — an oblique core locked at `≈ 40.182°`; its trigonometric
coordinates are algebraic while its nonzero radian angle is transcendental, a mechanism
**no proved case exercises**.

So record-finding ability needs its own targets, chosen by mechanism:

- **`s(17)`** — the nearest case whose (unproved) record uses genuinely oblique
  structure, with two distinct non-trivial angles; rediscovering *it* exercises the
  muscle that `n = 5, 10` cannot.
- **`n = 11` at controlled inflation `δ`** — a fixed-side feasibility/projection family,
  not the existing side-minimizing quench, makes slack an actual continuation parameter.
  The minimum inflation needed to reach and then track Trump’s component is a progress
  metric; a smaller threshold is better.
  Branch events and retained valid paths remain useful even when the discovery
  comparison fails.
- **Basin-entry tests** — start inside or near the Trump cell’s neighborhood and ask
  whether the polish loop falls in and stays; this separates “search cannot find the
  region” from “the refiner cannot hold it,” two failures with identical symptoms and
  different fixes.

Finally, the accounting stance that makes all of this compound: **near-misses are the
data.** A serious campaign will produce thousands of non-record basins; they are not
waste, they are the atlas — the training set for descriptors, the corpus for the model’s
reading, the sample for rarity-versus-structure laws, the denominator for coverage
claims. The run protocol’s “every run leaves a residue” was written as hygiene; this is
the strategy that turns the residue into the asset.

## Key Insights

- **The candidate bottleneck is the proposer’s sampling measure.** The working premise
  is that record packings are unusually constrained and have low hit probability under
  named baseline proposers; H-012 is designed to measure or reject that premise before
  it is used to deprioritize raw throughput.
- **LP-in-cell is the bridge from continuous search to discrete cartography.** It turns
  “where the annealer stopped” into “which cell this is,” making minima nameable and
  numerically polishable — Stillinger–Weber quenching with a reproducible endpoint
  candidate. *Amended ([D-034](../../../defects.md)): not always countable.* An optimum
  is a point only where an appropriate active-constraint rank and local analysis
  establish isolation; otherwise the LP may have a non-unique optimal face or the full
  problem may have a positive-dimensional terminal family.
  Numerically valued, yes; discrete only conditionally — and the census inherits the
  condition.
- **The map is the deliverable; records are corollaries.** A validated basin atlas of
  `n ≤ 11` is publishable, steers search, gives negative results meaning, and is the
  empirical shadow of a future proof’s case analysis.
- **Keep the loss; change what you keep.** Quality-diversity retention over
  mechanism-descriptors replaces loss-shaping; single-scalar descriptors are hackable
  (the grid maximizes contact count), so descriptors come in separating combinations.
- **The model proposes structure; the LP disposes.** Atlas reading, constructor DSLs,
  and cross-`n` transfer put the LLM where it is strong, and exact verification makes
  its error rate affordable.
  Nothing unverified enters a prompt; nothing unverified leaves one into the corpus.
- **Continuation turns rare-event search into path-following**, and its events —
  bifurcations, symmetry breaking — are “a feel for the space” in recordable form, with
  the δ-ladder’s barrier data feeding the atlas for free.
- **Calibrate on mechanism, not difficulty.** Passing `n = 5, 10` proves the machinery;
  only oblique targets — `s(17)`, inflated `n = 11`, basin-entry tests — prove the
  strategy.

## Recommendations

1. **Adopt cartography as the organizing goal of the first search campaigns.** S0
   (machinery gates) and the calibration ladder stay exactly as reviewed; S1’s basin
   byproducts feed the atlas rather than a log file; a new series S6 (landscape
   cartography) carries the atlas census, the premise test, and the δ-ladder.
2. **Treat this document as agenda, the register as contract.** The boil-down — H-11
   (census), H-12 (rarity premise), H-13 (δ-continuation), H-14 (superdisk), H-15
   (descriptor-QD) — lives in the
   [standing review](../reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md)
   with tests, tiers, and kill criteria.
   Notably, H-11 and H-13’s first legs are prototypable *now*, in the existing Python
   plus the LP already validated — no Rust required to start learning.
3. **Version the descriptor definitions with the atlas** as a soft-schema artifact (same
   discipline as `frontier/`), so QD archive keys, atlas identities, and any generated
   tables cannot drift apart.
4. **Sequence the LLM lanes behind the first atlas artifact.** Reading requires
   something verified to read; the constructor DSL is designable on paper in parallel;
   both inherit the grounding rule as stated.
5. **Keep the premise inversion honest.** If H-12 finds record basins are *not* rare,
   most of this document’s program stands down in favor of raw throughput — and that
   verdict is reachable in the cheapest tier.
   A strategy that names the observation that would kill it is the kind worth having.

## Methodology

Written 2026-08-23 as the capture of a design discussion held against the PR #4 branch;
no new computations were run for this document.
Internal grounding, all previously verified in this repository: the LP-in-cell
verification and canonical-identity design (standing review, R-1/R-2); the exact
verifier’s contact counts for Trump’s packing (14 zero-gap pairs, 20 boundary
coordinates); Ellsworth’s `s(51)` basin statistics as recorded in the infrastructure
synthesis; the record catalogue’s neighbor-extension annotations; the `m² − 3` gap
analysis in the frontier corpus; the phantom-constant correction in the main report.

External precedents are standard, load-bearing results *of their own fields* (inherent
structures, disconnectivity graphs, the LJ₃₈ double funnel, novelty search, MAP-Elites,
superdisk packings, FunSearch), cited from the literature as strategy precedents.
They are not packing literature and are deliberately **not** archived under
`resources/`, and no claim in the packing reports rests on them; if any is later
promoted to load-bearing for a packing claim, it first enters the source-availability
queue under the usual acquisition discipline.
Their role here is exhausted by the register: each transferred expectation is restated
as a hypothesis with a kill criterion before budget touches it.

## References

Internal:

- [Review: The Toolkit Docs and the First Experiment Series](../reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md)
  — R-1/R-2 (canonical identity, LP-in-cell), the register this document boils down into
  (H-11–H-15, S6).
- [Packing 11 Unit Squares in a Square](research-2026-08-22-packing-11-unit-squares.md)
  — rigidity and contact structure of Trump’s packing; the phantom-constant correction;
  the research program this strategy slots into.
- [Infrastructure for Square-Packing Exploration](research-2026-08-22-infrastructure-for-packing-exploration.md)
  — the tier model and the Ellsworth basin statistics.
- [Algorithms and Tooling for Square Packing](research-2026-08-22-square-packing-algorithms-and-tooling.md)
  — the AI-search landscape (FunSearch/AlphaEvolve context) the constructor-DSL lane
  builds on.
- [Frontier corpus](../../../frontier/README.md) — the `m² − 3` analysis behind the
  boundary-layer ladder; per-case editorial.
- Record catalogue capture (`resources/web/kingbird-squares-in-squares`) — the
  neighbor-extension annotations read here as a constructor-grammar corpus.

External (strategy precedents; see Methodology for their evidential status):

- F. H. Stillinger and T. A. Weber, “Hidden structure in liquids,” *Physical Review A*
  25, 978 (1982) — inherent structures and the quench map.
- O. M. Becker and M. Karplus, “The topology of multidimensional potential energy
  surfaces,” *Journal of Chemical Physics* 106, 1495 (1997) — disconnectivity graphs.
- D. J. Wales, *Energy Landscapes* (Cambridge University Press, 2003).
- J. P. K. Doye, M. A. Miller and D. J. Wales, “The double-funnel energy landscape of
  the 38-atom Lennard-Jones cluster,” *Journal of Chemical Physics* 110, 6896 (1999).
- S. Kirkpatrick, C. D. Gelatt and M. P. Vecchi, “Optimization by simulated annealing,”
  *Science* 220, 671 (1983).
- J. Lehman and K. O. Stanley, “Abandoning objectives: evolution through the search for
  novelty alone,” *Evolutionary Computation* 19(2), 189 (2011).
- J.-B. Mouret and J. Clune, “Illuminating search spaces by mapping elites,”
  [arXiv:1504.04909](https://arxiv.org/abs/1504.04909) (2015) — MAP-Elites.
- Y. Jiao, F. H. Stillinger and S. Torquato, “Optimal packings of superdisks and the
  role of symmetry,” *Physical Review Letters* 100, 245504 (2008).
- B. Romera-Paredes et al., “Mathematical discoveries from program search with large
  language models,” *Nature* 625, 468 (2024) — FunSearch.
- E. L. Allgower and K. Georg, *Numerical Continuation Methods* (Springer, 1990).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
