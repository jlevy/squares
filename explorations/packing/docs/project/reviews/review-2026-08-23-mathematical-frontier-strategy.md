# Review: The Mathematical Frontier, Its Gaps, and How to Search It Fast

**Date:** 2026-08-23

**Author:** Claude (agent), for joshuadlevy@gmail.com

**Status:** Complete

## Overview

This is a strategy review along the creativity and mathematical-depth axis: given the
tooling now standing (exact verifier, LP-in-cell quench, campaign record, readiness
agenda), where should aggressive, high-iteration search point so that the program’s most
likely outcome is a novel mathematical result rather than a well-documented miss?

The verdict in one paragraph.
The registered portfolio is sound and its critical path (H-023 → H-021 → H-011 → H-012)
is correctly sequenced, but it undersells four things.
First, several of the highest-value mathematical results do **not** wait on the
identity-resolution path at all: a local certificate for Trump’s packing, the two-class
angle map of `n = 11`, the ceiling of the unavoidable-set method, and the `m² − 3`
analytic attempt are all runnable now in fast loops.
Second, the record contains a small number of checkable mathematical observations that
nobody has written down, the sharpest being that Trump’s contact count is **exactly
isostatic** — 14 pair contacts plus 20 boundary coordinates equals 34, the number of
configuration variables — which sharpens H-022 into a specific prediction and supplies a
search filter. Third, the program’s likeliest publishable results are not the `n = 11`
record; they are certificates, classifications, and method-limitation theorems that can
be banked with near-certainty while the record search runs as a portfolio of lottery
tickets. Fourth, loop latency should be treated as a first-class allocation input: the
measured record is about 25 agent-minutes per round against 2 wall-minutes of compute,
so the binding constraint is round overhead, and the strategy should prefer experiments
whose output is a generated map over experiments needing bespoke interpretation.

## Scope and Method

Reviewed: the six research reports, `SYNOPSIS.md`, the 24-hypothesis registry, the idea
board, the PR #14 program review (its findings F-01–F-41, strategies A-01–A-04,
questions Q-01–Q-04, and omissions O-01–O-04), the readiness agenda, the defect log, and
the eleven recorded rounds.
One computation was rerun (`verify_trump11.py`, 0.15 s) to confirm the contact counts
used below. This document proposes; it registers nothing.
New claims are flagged as idea-board rows (status `raw`) and framed so the registry can
adopt them with kill criteria.
Where a proposal overlaps A-01–A-04 or Q-01–Q-04 of the
[PR #14 review](review-2026-08-23-square-packing-program-and-pr14.md), the overlap is
cited rather than restated.

## The Most Promising Frontier Areas

Ranked by probability of a novel result times value, divided by cost.
The striking feature of this ranking is that the `n = 11` record — the motivating target
— is not near the top.
The program’s near-certain results are certificates and classifications; the record is
the moonshot they collectively feed.

| Rank | Result | Probability | What it needs | Latency class |
| ---: | --- | --- | --- | --- |
| 1 | **A certified local statement about Trump’s packing** (isolation and local optimality, or its refutation) | high, if attempted | exact arithmetic on a known witness; no search | sub-second compute, days of derivation |
| 2 | **The complete local-optima landscape at one small `n`** (first such classification for this problem family) | high | the identity-resolution path already in flight | minutes per batch |
| 3 | **The first exact audit of the record catalogue** (every obtainable `n ≤ 100` record verified over its own field) | high | the geometry corpus (O-01) | agent-tier, embarrassingly parallel |
| 4 | **A ceiling theorem for the unavoidable-set method at `n = 11`** (either direction is informative) | medium | covering-LP machinery, shared with H-006/A-04 | hours per resolution level |
| 5 | **`s(12) = 4`** — the first new proved value since 2018 | medium-low | the proof lane through H-010, then A-04 | weeks |
| 6 | **An `m² − 3` record at `n ∈ {61, 78, 97}`** | low | paper and algebra first (H-005) | days, no engine |
| 7 | **A new `n = 11` upper bound** | very low | everything above it in this table | months |

Three comments on the ranking.

**Rank 1 is underweighted by the current agenda.** H-022 is registered and priority 1 in
the proof lane, but it is treated as a prerequisite for interpreting attraction
measurements. It is more than that: *either answer is a publishable fact about a
47-year-old object*, the computation is small and exact, and — see the isostatic
observation below — the expected answer is now specific enough to be falsifiable.
Nothing else in the portfolio has this ratio of certainty to cost.

**Rank 2 needs a scope cut to become bankable.** H-011 as registered runs to `n = 8`
with a coverage estimator.
The publishable unit is smaller: a *complete, certified* classification of terminal
components at one small `n` (5 or 6), with every component’s identity resolved by rank
and continuation evidence rather than sampling saturation.
Nobody has published even `n = 5`. Cutting the first deliverable to one `n` converts an
open-ended census into a finishable theorem-adjacent artifact, and H-023 is already its
first step.

**Ranks 4–6 are the surprise reservoir.** Where could a genuine surprise hide, at what
prior?

- **The ceiling is below 3.877** (prior: genuinely unknown, and that is the point) — a
  method-limitation theorem explaining a twenty-year stall.
- **A second competitive mechanism at `n = 11`** (prior: low) — visible, if it exists
  within two angle classes, on the two-class map proposed below.
- **The `m² − 3` family fails** the way `n² − n` failed at Cleemann’s 272 (prior: low;
  the precedent is the reason it is not negligible).
- **Trump’s packing is not isolated** (prior: low) — the rank computation decides, and a
  flat direction would be a mathematical surprise with immediate consequences for basin
  semantics.
- **Terminal families are pervasive rather than exceptional** (prior: medium, given the
  exact `n = 3` family) — already the program’s live concern (D-034); if true, the
  atlas’s objects change and the discovery is itself reportable.

## Gaps in the Research Record

Eight gaps, ordered by how directly each changes what to run next.
The first four are mathematical content absent from the record; the rest are method and
sequencing gaps.

### G-1: Trump’s contact count is exactly isostatic, and nothing says so

The exact verifier reports 14 pair contacts at exactly zero gap and 20 corner
coordinates exactly on the container boundary.
Each zero-gap pair contributes one scalar equality along its separating axis; each
boundary coordinate is one scalar equality.
The configuration has `3n + 1 = 34` variables.

**14 + 20 = 34.** The contact system has exactly as many scalar conditions as the
configuration has degrees of freedom.
If those 34 conditions are independent — a rank computation, not a count (D-041) — the
configuration is a locally isolated solution of its own contact system: precisely the
isolation H-022 asks about, now with a specific predicted rank (34) and a specific
falsification (any rank deficit names a flat direction).

This is the square-packing form of a fact the sphere- and disk-packing jamming
literature treats as a fingerprint: collectively jammed packings are isostatic, with
matching contact and freedom counts (Donev, Torquato, Stillinger, and Connelly’s line of
work). No packing report or campaign artifact records the count, and the connection to
the jamming literature is absent from the strategy layer even though that literature
already supplies the double-funnel precedent the rarity premise leans on.

Three uses, in increasing ambition:

1. **Sharpen H-022.** The first deliverable was already “a complete constraint matrix
   and tangent calculation”; the count says what answer to expect and makes the
   computation a test rather than an exploration.
2. **A corpus law candidate.** *Every record packing’s active scalar-contact count is at
   least `3n + 1` minus its symmetry dimension, with equality for records with trivial
   symmetry.* Testable mechanically once the geometry corpus (O-01) exists.
   The proved `45°` cases are symmetric and may be hyperstatic, so the law as stated may
   distinguish oblique records specifically — either way the measurement is cheap.
3. **A search filter.** A-01’s contact-graph-first search can prune any candidate
   contact structure whose scalar count falls short of the isostatic requirement, a
   Maxwell-count filter that costs integer arithmetic per node and removes the bulk of
   under-constrained topologies before any LP is solved.

### G-2: The LP dual is a self-stress, and it is the certificate H-022 needs

At the cell optimum, the LP’s dual multipliers on active constraints form an equilibrium
**stress** on the contact framework: nonnegative forces on contacts and walls balancing
the objective’s pull on the container side.
Complementary slackness puts stress only on touching pairs.
This is the standard rigidity-theory object (a self-stress), and it arrives free with
every quench — the solver already computes it and the code discards it.

The route this opens for H-022/Q-03(2) is more concrete than “interval active-set
certificate”:

- **Centre directions** are certified by LP duality itself — the dual certificate *is*
  the proof that no centre motion within the cell reduces the side.
- **Angle directions** have one-sided directional derivatives computable from
  parametric-LP sensitivity of the two adjacent bases.
  T-3’s measurement (`+0.1747` and `+0.3841` per radian on the two sides of the tested
  slice) says the side grows *at first order* in both directions along that slice —
  conical growth, stronger than a smooth minimum.
  A finite set of such one-sided derivatives, one pair per angle-class direction,
  certifies first-order strict growth in the full angle space, provided none vanishes (a
  vanishing one falls back to a second-order stress-matrix test, which is Connelly’s
  prestress stability).
- **Cell changes** are covered by bounding adjacent cells’ LPs below via their own dual
  feasible points.

All three pieces are finite, exactifiable over the packing’s field once the exact
rational LP exists, and independently replayable — exactly the certificate shape Stage 4
of the PR #14 program wants.
The same dual vector has two cheaper uses meanwhile: a **stress descriptor** for the
atlas (which contacts carry force, and how much), and **stress-guided moves** for
proposers (squares with zero stress are unloaded and can move; heavily stressed
substructures should move as blocks).

### G-3: The ceiling of the unavoidable-set method is measurable, and unmeasured

The `n = 11` report’s open question — *is there a proved ceiling below 3.877084 on what
a finite unavoidable point set can certify?* — is answerable by a computation the
portfolio already almost contains.

Define the covering LP at container side `s`: minimize total mass of a measure on the
container such that every unit-square pose receives mass at least 1. Call its value
`V(s)`. A 10-point unavoidable set at side `s` exists only if `V(s) ≤ 10`, so

> `s_frac = sup { s : V(s) ≤ 10 }`

is an upper bound on what any pure point-counting argument can prove for `s(11)`. By LP
duality, `V(s) > 10` is witnessed by a **fractional packing** — a pose measure of total
mass above 10 with pointwise density at most 1 — and ten disjoint unit squares already
fit at `s ≥ 3.708`, so the whole question lives in the sliver between Stromquist’s
3.7889 and Trump’s 3.8771: can fractional mass exceed 10 there?
Nobody knows, and either answer redirects the proof lane:

- `s_frac < 3.877`: a **method-limitation theorem**. The classical method cannot close
  the gap even in principle; effort shifts to threshold and continuously-varying
  refinements (Bentz) or genuinely new certificates, with a precise statement of *why*.
- `s_frac ≥ 3.877`: the hunt for a concrete certificate is justified, and the LP’s
  optimal measures say where its mass must sit.

Scoping caveats: threshold certificates (a box charged three points, as in Stromquist’s
Theorem 2) and Bentz’s families have their own relaxations and are not bounded by this
LP as stated; the pure-point form is the first-order answer, and the refinements are
follow-on measurements of the same shape.
H-006 currently tests dual-support *stability* as a certificate generator; this gap
elevates the same machinery to a decision measurement with a theorem-shaped output.
A-04’s synthesis loop is the natural home.

### G-4: The corner generalizes — a kink-codimension principle worth registering

T-3 established one corner on one slice.
The general picture it instantiates deserves statement as a corpus law candidate:

> **At a record optimum with `k` free angle classes, the class-angle objective attains
> its minimum at a point of non-smoothness of codimension `k` — every free angle is
> pinned by its own basis-exchange condition, and the objective grows at first order
> (conically) in every angle direction.**

The evidence: T-3’s two-sided positive one-sided slopes at `n = 11` (`k = 1`); the
isostatic count in G-1 (a fully pinned optimum is what exact determination looks like);
and the general fact that parametric-LP value functions are piecewise smooth with
structurally stable minima at breakpoints.
The prediction: the `s(17)` record (`k = 2` by its two non-trivial tilts) sits at a
codimension-2 corner; the corpus scan once O-01’s geometry lands.

Three consequences if it holds:

1. **Method selection is explained, not just observed.** Bracketing beats descent
   because the optimum has no gradient to follow; this stops being an empirical quirk
   and becomes a structural property of the target class (D-087’s separation of claims
   is respected: this is the registered-corpus-law version, not the algorithm claim).
2. **The optimum lies on the tie locus.** Basis-exchange points are where two cells’ LP
   optima agree — a codimension-1 set per condition.
   Records live on the intersection of `k` of them.
   A-01’s active-set search can walk *along* tie loci (follow a basis exchange,
   dimension drops by one each time) instead of sampling volume — the mathematically
   motivated version of the billiard/inflation family that produced records at
   `n = 29, 37`.
3. **Corner sharpness is a descriptor.** The one-sided slope pair per angle direction is
   a per-component invariant the atlas should retain; it measures the cone angle of the
   funnel near its tip and is a candidate predictor for entry probability (feeding
   Q-04’s held-out predictor question).

### G-5: H-012 as registered bounds rarity but cannot measure it, and cheaper evidence is available

If the record component’s attraction probability is of order `1e-6`, direct multistart
census (H-011’s data) will observe zero arrivals; that still *confirms* rarity at the
registered 0.1 ratio (a zero count with `N` samples upper-bounds the probability), but
it cannot say how rare, and the atlas’s per-component frequencies stay empty exactly
where the strategy needs them.
A-02 already names the fix (adaptive multilevel splitting, subset simulation on nested
side thresholds); the gap is that H-012 and A-02 are not wired together: H-012’s round
design should carry a splitting arm from the start rather than discovering the need
after a zero count.

Cheaper still, and absent from the portfolio: **extreme-value analysis of the multistart
side distribution already collected.** Fit the lower tail of the `n = 11` best-side
distribution (exp-001/exp-003 archives, extended by any future sweep) with a generalized
Pareto model and estimate the distribution’s left endpoint.
If the estimated support endpoint sits credibly *above* 3.8771, this proposer cannot
reach the record at any budget — H-017’s question answered from existing data, at the
cost of one afternoon and with honest model-dependence caveats.
It is evidence, not proof; it is also the fastest available quantitative version of
“scaling will not help.”

### G-6: The two-class stratum of `n = 11` is a plottable surface no one has plotted

The synopsis’s “thirty-four dimensions become one” section scans Trump’s cell along one
shared angle. One step up is the honest visualization coup of this problem: fix a
two-class structure — `k` squares at angle `a₁`, the rest at `a₂` — and map

> `Φ(a₁, a₂) = the best quenched side found with those class angles`,

a two-dimensional surface per class assignment.
Trump’s packing is the point `(0°, 40.18°)` on the `6 + 5` assignment’s surface, at a
corner (G-4). The map answers, visually and cheaply: is Trump’s the only competitive
valley in the two-class stratum, or are there others — and does any other assignment
(`7 + 4`, `8 + 3`) carry a valley anywhere near `3.877`?

Cost: with warm-started cell fixed-point solves at about 10 ms per grid point, a
`100 × 100` map is minutes of compute per assignment; a few random restarts per point to
probe alternative cells multiplies that by a small constant.
Discipline: the surface is a lower envelope over *found* cells, so it is provisional
(`f64_screen`/`polished` tier) and its valleys are candidate regions, not certified
components. The same scan at `n = 17` (the mechanism-matched case) doubles as
calibration: the map should show Bidwell’s oblique valley, and whether the proposer’s
samples ever enter it.

This is the cheapest new instrument in the portfolio, it produces the first genuinely
novel *picture* of the problem, and it directly serves the visualization ladder below.

### G-7: The geometry corpus gates four claims and the analytic frontier, and deserves its priority stated

O-01 (no executable geometry corpus) is recorded as a key omission; what is worth adding
is how much now stacks on it: H-024 (angle-class corpus law), G-1’s isostatic law, G-4’s
kink-codimension law, the constructor-grammar corpus (Q-04), and the rank-3 exact audit
of the record catalogue.
Five independent measurement programs blocked by one agent-tier parsing task with no
mathematical risk. On value-per-unit-effort it belongs at the top of the Insight-lane
build queue, not in the backlog.

### G-8: Sources whose absence could change the plan

Unchanged from the `n = 11` report’s open list, but three deserve their standing raised
because they bear on *strategy*, not completeness: **El Moumni (1999)** holds published
priority for three proved values and no summary describes his method — a third proof
technique may exist in that paper; **Stromquist’s 1984 memoranda** cover `n ≤ 65` and
would recalibrate the priority ledger; and **Gensane–Ryckelynck’s contact-class
enumeration** (did their billiard algorithm record which `n = 11` cells it explored?)
would tell this program which parts of cell space a serious prior search already covered
— negative information that would re-aim every proposer.
The phantom-constant episode is the standing reason to treat unretrieved primaries as
risk, not backlog.

## Seven Mathematicians, Seven Pushes

A completeness check on the portfolio: give the same tooling to seven senior
mathematicians of different schools and ask what each would do first.
Five of the seven pushes are at least partially in the portfolio; the exceptions are
noted.

**The rigidity theorist (Connelly school).** First move: the stress and rank computation
at Trump’s packing (G-1, G-2), then isostatic filters for enumeration.
Portfolio: H-022 and A-01 carry the destination but not the stress-certificate route or
the count observation.
This persona’s whole program is a week of exact linear algebra away, which is why it
ranks first above.

**The optimization and duality theorist (LP relaxation and SOS school).** First move:
compute `V(s)` (G-3) and read the optimal dual measures; second move, ask whether any
Positivstellensatz certificate has ever been tried (the report already answers: never,
at any `n`). Portfolio: A-04 and H-006 carry the machinery; the ceiling measurement is
the missing first-class question.
SOS itself stays parked on cost — the honest note is that it is the one untried proof
technology, and a small-`n` pilot (`s(2) = 2` via SOS) would be a methods paper on its
own.

**The algebraic number theorist and experimental mathematician.** First move: parse the
record catalogue’s minimal polynomials (degrees 4, 5, 6, 8, 12, 18, 20, 24, 42, 44, 82
in the open table) and ask what the fields are — Galois groups, discriminants, whether
degree is predicted by mechanism (angle-class count and contact pattern through the
elimination). Nothing in the portfolio touches this.
It is cheap once O-01 lands, it is publishable as a data note ("the algebra of record
packings"), and a degree-mechanism law would run *backwards*: the degree-8 target
constrains which mechanisms are worth searching at `n = 11`.

**The statistical physicist (Wales school).** First move: disconnectivity trees over the
container-inflation parameter (the δ-ladder is the natural barrier scale), and splitting
estimators for rare-basin measures.
Portfolio: the strategy report, H-013, and A-02 carry nearly all of it.
The missing scalar is **the record funnel’s depth**: the largest δ at which a quench
started in Trump’s component escapes it, and the merge-δ at which the component joins
its neighbors — one number per direction, computable today from the exact witness, and
the single most decision-relevant measurement for whether δ-continuation can walk in (it
is also exp-005’s registered successor, still undone).

**The enumerative combinatorialist (Friedman school).** First move: completely classify
local optima at `n = 5` (rank 2 above), and sweep *every* open `n ≤ 100` at tier S with
the standard spine — 31 open cases still have the bare grid as the record, and no one
with an exact verifier has ever swept the catalogue.
Portfolio: the small-`n` census is the critical path; the breadth sweep appears only
implicitly in the “Additional results” table.
The sweep is embarrassingly parallel, every cell is a lottery ticket, and its by-product
is rank 3’s audit corpus.

**The logician and formalizer.** First move: specify the certificate formats now — exact
upper-bound witness (T-1’s shape) and no-escape/unavoidability certificates — so every
artifact the search produces is born replayable; formalize Friedman’s lemma layer and
Stromquist Theorem 1 as the Lean pilot.
Portfolio: the Lean report and Stage 4 carry this; the sequencing point is that the
certificate *format* costs days now and months to retrofit, and the `n = 11` upper-bound
formalization remains unclaimed in the literature — a stand-alone publishable artifact
whose difficulty is bounded (one packing, one field, one polynomial identity).

**The probabilist.** First move: G-5’s extreme-value endpoint estimate from existing
multistart data; then proper splitting estimators inside H-012; then coverage estimators
(H-007) treated as survey statistics with honest intervals.
Portfolio: H-007 and A-02 carry two of three; the EVT read of data already on disk is
new, and it is the fastest honest answer to “would 100× budget help?”

The consolidated answer to “which directions would senior mathematicians push”: the
portfolio already spans the physicist, combinatorialist, and formalizer well; the
rigidity theorist and the duality theorist are one derivation each away from their first
result and are underserved; the number theorist’s lane does not exist yet and costs
almost nothing once the geometry corpus lands.

## Basin Intuitions and a Visualization Ladder

Five intuitions to hold while mapping, then the ladder.

1. **The vertical axis of any landscape picture should be container slack, not energy.**
   δ-inflation is this problem’s barrier scale: two components are “adjacent at δ” when
   their basins merge under a δ-inflated container.
   That yields an ultrametric, hence a tree — the disconnectivity picture — and the
   δ-ladder computes it as a by-product of continuation (the strategy report already
   notes this; the ladder below operationalizes it).
2. **Draw families as intervals, never as points.** The exact `n = 3` sliding family is
   the standing warning (D-034): any endpoint plot must be able to show a component as a
   segment or region with lower/upper identity bounds, or the picture will silently
   re-assert the isolation assumption the program just spent a defect unlearning.
3. **Structural coordinates, not embeddings.** Layout by descriptors that mean something
   — tilt-class count, oblique-core size, boundary/interior contact split, stress
   pattern (G-2), corner sharpness (G-4) — and treat any learned 2-D embedding as a
   browsing aid. The README’s rule stands: an embedding is never evidence of adjacency.
4. **Frequency is conditional, always.** Every frequency shown is under a named `P/Q/E`;
   the map’s legend carries the regime or the map is wrong (D-040).
5. **The map should show its own incompleteness.** Discovery curves and unseen-mass
   estimates belong on the atlas view itself, so “searched to saturation” is a readable
   claim with an interval, not a vibe.

The ladder, easy to hard, each rung validated on proved ground before pointing at the
target:

| Rung | View | Instance | Needs | Cost class |
| --- | --- | --- | --- | --- |
| V-0 | Per-cell angle slices `φ(a)` with corner annotations | any discovered cell | exists (`lp_cell.py`) — systematize into a generated view | seconds |
| V-1 | Endpoint dot-plots with family intervals: side value vs. descriptor, D-034-safe | `n = 3…6` | quench + canonical keys (exist); interval rendering | minutes |
| V-2 | δ-dendrogram (disconnectivity tree) | `n = 5` first, proved ground | δ-ladder legs + merge detection (H-013’s first leg) | minutes–hours |
| V-3 | Two-class maps `Φ(a₁, a₂)` per assignment (G-6) | `n = 11` and `n = 17` | warm-started cell fixed-point sweep | minutes–hours |
| V-4 | Basin scatter: log attraction frequency vs. side, colored by tilt classes — the H-012 figure | `n = 10`, then 11 | H-011 data under named `P/Q/E` | after census |
| V-5 | Atlas adjacency graph, merge-δ edge weights, stress and sharpness per node | `n ≤ 10` | atlas + continuation events | after census |

V-0 through V-3 need nothing from the identity-resolution critical path; they are the
“maps that are easier to look at” available this week, and V-3 is the first picture of
`n = 11` that has never existed in any literature.

## Loop Speed as a Strategy Input

The measured latencies, consolidated:

| Operation | Measured | Source |
| --- | ---: | --- |
| Annealer move | ~0.025 µs (39.7 M/s local) | bench, readiness agenda |
| One LP cell solve (`n = 11`) | ~1.28 ms | infrastructure report |
| Class-bracketing quench to floor | ~70 LP solves | exp-007/008 mechanism note |
| Exact verification (`n = 11`, degree 8) | 0.15 s | rerun for this review |
| Canonicalization | 0.098 s at `n = 7`; **7.91 s at `n = 9`** | readiness agenda |
| Normal gate | 108–126 s | README |
| One recorded round | **~25 agent-minutes**, ~2.1 wall-minutes | 275 agent-min / 11 rounds |

Two structural conclusions.

**The binding constraint is the agent loop, not the compute.** At 12:1 agent-to-machine
time, halving compute buys almost nothing; halving per-round overhead doubles
throughput. The readiness agenda’s efficiency list already targets this (recipes,
generated views, delegated checks); the *strategy* consequence is new: prefer
experiments whose analysis is a generated artifact — a map, a table, a curve — over
experiments whose result needs bespoke interpretation.
Every rung of the visualization ladder qualifies; that is a second, independent reason
to build it early. Sweeps beat single cells for the same reason: one preregistration and
one analysis amortized over a hundred grid points is a hundredfold round-overhead
reduction, and the two-class map is exactly this shape.

**Two efficiency investments carry mathematical payoff, not just speed.** The
canonicalizer’s `n = 7 → 9` jump (81×) will dominate any census and is already tracked
(D-049, `think-xzew`); fix before H-011 scales.
The **exact rational LP** removes the `1e-11` polished floor (D-021), makes G-2’s
certificates exact rather than numerical, and makes every Pythagorean-angle construction
(H-005’s `arctan(3/4)`, and any 3-4-5 mechanism) verifiable in plain `ℚ` — one build
serving a defect, a certificate program, and a search lane at once.

The lane assignments below are functions of the measured latencies, not fixed judgments.
Efficiency work is a live lane of its own: when a latency moves by an order of magnitude
— the canonicalizer fix, a compiled or batched quench, a faster gate — re-derive the
assignment from the new numbers rather than inheriting it, since a lane demoted for
slowness may become a wide interactive lane overnight.

The lane assignment that follows from the current latencies:

- **Sub-second loops — run wide, now.** Rank and stress extraction (G-1, G-2), angle
  slices (V-0), EVT tail fits (G-5), dual-measure reads.
  Dozens of iterations per day per agent; these are the “fast to iterate, do more of up
  front” lanes.
- **Minute loops — daily cadence.** Small-`n` endpoint batches (V-1), δ-ladder legs
  (V-2), two-class map sweeps (V-3), basin-entry and funnel-depth probes.
- **Hour loops — queue for the runner.** `n = 11` sampling campaigns, splitting arms,
  fine-resolution ceiling LPs, MAP-Elites comparisons.
  These are the ones the launch gate governs; they should never occupy an interactive
  agent.
- **Day-plus loops — parallel background lanes.** Geometry corpus parsing (G-7), source
  retrieval (G-8), Lean certificate formats, superdisk geometry (H-014, correctly last).

## The Portfolio, Sequenced for Fast Rotation

The operating doctrine requested: push many directions fast, mark the barren ones, and
return to them when a new instrument or map changes their prior.
The registry’s status vocabulary already supports marking (`rejected`, `abandoned`,
`exhausted`, `parked`); the missing piece is the **revisit trigger** — a parked or
exhausted lane should name the event that would reopen it (an instrument landing, a map
redrawing a prior, a source arriving).
One line per parked row on the idea board suffices.

**Fast lanes to open now** (independent of the identity-resolution critical path):

| Lane | First deliverable | Loop | Gap/idea |
| --- | --- | --- | --- |
| Trump rank and stress | exact active-constraint matrix, rank, dual stress vector | sub-second compute, days of derivation | G-1, G-2 → H-022 |
| Two-class maps | `Φ(a₁, a₂)` at `n = 11` (assignments `6+5`, `7+4`, `8+3`) and `n = 17` | minutes per map | G-6, V-3 |
| Funnel depth | escape-δ and merge-δ from Trump’s exact witness | minutes | physicist’s scalar; exp-005 successor |
| EVT tail read | left-endpoint estimate from existing `n = 11` multistart data | one session | G-5 |
| `m² − 3` analytics | the Cleemann-style `arctan(3/4)` derivation, survive-or-die | paper only | H-005 |
| Ceiling LP pilot | coarse `V(s)` at one `s` in the gap, both bounds | hours | G-3 |
| Geometry corpus | SVG → exact `(x, y, θ)` importer for the first ten records | agent-tier | G-7 / O-01 |
| Source retrieval | El Moumni, Stromquist memoranda, G-R enumeration query | agent-tier | G-8 |

**The critical path stays as sequenced** — H-023 → H-021 → H-011 → H-012 — with two
amendments: profile and fix the canonicalizer before H-011 scales past `n = 8`, and
carry a splitting arm (A-02) inside H-012’s design from the start.

**Medium builds, after first maps:** A-01 prototype at `n = 5–7` with the isostatic
filter; descriptor freeze for H-015 (add stress pattern and corner sharpness to the
candidate descriptor set); H-013’s `n = 10` gate; H-004 seeded from *verified* record
geometry once the corpus lands.

**Deferred, deliberately:** H-014 (superdisk — only item needing new geometry), GPU work
(measured dead end at current `n`), full Lean formalization beyond the
certificate-format spec, SOS beyond a parked pilot note.

**Rotation rule.** Every fast lane above is sized to reach a keep-or-park verdict within
days. Park verdicts are recorded with their revisit trigger; the expected shape of the
portfolio a month out is two or three lanes promoted to registered rounds, the rest
parked with named triggers, and the critical path unblocked by the canonicalizer fix —
at which point the census, the atlas, and V-4/V-5 become the program’s center of
gravity, with the fast lanes’ maps steering where the census samples.

## Recommendations

1. **Open the rank-and-stress lane this week** (G-1, G-2): compute the exact
   active-constraint matrix and rank at Trump’s packing, extract the dual stress, and
   record the isostatic count as the observation motivating both.
   Route the result through H-022.
2. **Build the two-class maps** (G-6) at `n = 11` and `n = 17` as a preregistered sweep
   with a generated view, and adopt V-0–V-3 of the visualization ladder as the atlas
   explorer’s first three deliverables.
3. **Adopt the ceiling measurement** (G-3) as the proof lane’s decision experiment:
   pilot `V(s)` coarsely, and register the refinement only if the pilot is informative.
4. **Amend H-012’s design** to carry a splitting arm from A-02, and run the EVT tail
   read (G-5) on existing data now.
5. **Raise the geometry corpus** (G-7) to the top of the Insight build queue and start
   the three strategy-relevant source retrievals (G-8).
6. **Add the raw idea-board rows** for the isostatic law, the stress certificate, the
   ceiling measurement, the two-class map, and the kink-codimension law, so the registry
   can adopt them with kill criteria on its own schedule.
7. **Sequence by loop latency**: sub-second and minute lanes run interactively and wide;
   hour lanes queue for the runner behind its launch gate; day-plus lanes run as
   background agent work.
   Prefer experiments whose analysis is a generated artifact, and batch sweeps over
   single cells to amortize the measured ~25-minute round overhead.
8. **Bank the certain results deliberately**: the Trump local certificate, the complete
   `n = 5` classification, and the exact catalogue audit are the program’s near-certain
   publishable outputs; schedule them as first-class deliverables rather than
   by-products, and let the record search remain the portfolio of fast, cheap,
   marked-and-revisited lottery tickets it should be.

## References

Internal:

- [SYNOPSIS.md](../../SYNOPSIS.md) — results T-1–T-3, the terminology, the defect
  record, and the roll-up this review reads from.
- [Packing 11 Unit Squares in a Square](../research/research-2026-08-22-packing-11-unit-squares.md)
  — the mathematics, the open-frontier table, the research program, and the open
  questions G-3 and G-8 respond to.
- [A Search Philosophy for Square Packing](../research/research-2026-08-23-search-philosophy-and-landscape-cartography.md)
  — the strategy layer this review extends.
- [Review: Square-Packing Program and PR #14](review-2026-08-23-square-packing-program-and-pr14.md)
  — findings F-01–F-41, strategies A-01–A-04, questions Q-01–Q-04, omissions O-01–O-04.
- [Unattended Square-Packing Research Readiness](../specs/active/plan-2026-08-23-overnight-cartography-run.md)
  — the launch agenda whose sequencing this review amends at the margins.
- [Campaign idea board](../../campaign/ideas.md) and the
  [hypothesis registry](../../campaign/hypotheses/) — the artifacts recommendations 4
  and 6 modify.

External (strategy precedents, per the search-philosophy report’s evidential-status
discipline; none is load-bearing for a packing claim):

- A. Donev, S. Torquato, F. H. Stillinger, and R. Connelly, “A linear programming
  algorithm to test for jamming in hard-sphere packings,” *Journal of Computational
  Physics* 197, 139 (2004) — isostaticity and LP jamming tests.
- R. Connelly and W. Whiteley, “Second-order rigidity and prestress stability for
  tensegrity frameworks,” *SIAM Journal on Discrete Mathematics* 9, 453 (1996) — the
  stress-certificate machinery behind G-2.
- S. R. S. Varadhan-line rare-event methods as consolidated in F. Cérou and A. Guyader,
  “Adaptive multilevel splitting for rare event analysis,” *Stochastic Analysis and
  Applications* 25, 417 (2007) — the estimator class behind G-5.
- S. Coles, *An Introduction to Statistical Modeling of Extreme Values* (Springer, 2001)
  — the tail-endpoint estimation behind G-5’s cheap read.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
