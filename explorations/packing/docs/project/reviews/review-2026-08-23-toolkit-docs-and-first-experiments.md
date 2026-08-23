# Review: The Toolkit Docs and the First Experiment Series

**Date:** 2026-08-23

**Author:** Claude (agent), for samanthadrakova@gmail.com

**Status:** Complete

**Reviewed:** the three documents added on the `claude/packing-infrastructure-synthesis`
branch (PR #4) —
[the infrastructure synthesis](../research/research-2026-08-22-infrastructure-for-packing-exploration.md),
[the Lean study](../research/research-2026-08-22-lean-for-packing-proofs-and-validation.md),
and
[the minimal-toolkit plan spec](../specs/active/plan-2026-08-22-minimal-packing-toolkit.md)
— against the four prior reports and the corpus, from a theory-first standpoint: not “is
this correct” but “what would a senior researcher say is *missing*, and what should the
first experiments actually be.”

## Overview

The three documents hold up.
The tier model, the one-predicate-many-scalars rule, certificate-first design, and the
upper-bound-formalizable finding all survive re-examination, and nothing reviewed here
reverses a conclusion.

What the review found instead is a **layer that none of the documents supplies**: the
experiments are specified as *deliverables* (E1–E4) but not as a *method*. There is no
definition of what a basin *is* (so E4’s statistics are currently ill-posed), no
refinement stage (the spec presumes a “refined side length” that no task produces), no
calibration ladder of known-answer cases, no protocol for running many small
hypothesis-driven experiments with discipline, and no register of the hypotheses worth
spending budget on. The single most useful theoretical observation surfaced by this
review — that **for fixed angles the whole problem is a linear program**, so the true
search space is angle space plus a combinatorial cell choice, not `ℝ^{3n+1}` — appears
nowhere in the five reports, and it reshapes both the refinement stage and the search
design.

The second half of this document therefore does three things the plan spec does not: it
states a **hypothesis register** (H-1–H-15, each with grounding, a test, and a kill
criterion; H-11 onward were added by the same-day strategy capture, below), a **run
protocol** that keeps freeform exploration disciplined and makes every run leave a
residue, and a **prioritized series plan** whose first item is the smoke-and-calibration
series the machinery needs before any result can be trusted.

Findings are numbered `R-*`; hypotheses `H-*`; series `S-*`.

## What holds up, briefly

- **The tier model is right and keeps paying.** This review reuses it twice: Lean and
  the LP solver both land in the agent tier; only the SAT predicate and the move loop
  are inner-loop.
- **One predicate, many scalars** is the correct spine, and the `PoseBox` hook is the
  cheapest good decision in the spec — several proposals below lean on it.
- **Certificates over booleans** is the right call and extends naturally to *runs*
  (below), not just packings.
- **The experiment set E1–E4 is the right skeleton.** Everything below refines or
  surrounds it; nothing replaces it.

## Findings: what is missing

### R-1 (blocking E4): “basin” is undefined, and without a canonical key the statistics are not statistics

The spec records “every local optimum reached, with its key” — but the key it has is the
*RNG* key, which identifies the *trajectory*, not the *optimum*. Two trajectories
reaching the same optimum must count as one basin, and the same geometric optimum
arrives in `n!·4ⁿ` relabelled/quarter-turned presentations times the container’s
dihedral group of order 8. Ellsworth’s “3,004 basins” for `s(51)` is only meaningful
under whatever dedup he applies, which is unpublished — one more reason our numbers must
define theirs.

**Fix:** define basin identity explicitly, two-level:

1. **Geometric key:** canonicalize under the container’s `D₄` and square relabelling
   (sort squares lexicographically after applying the best of the 8 container
   symmetries), quantize coordinates at a stated resolution, hash.
   Cheap, computed at record time.
2. **Structural key:** after refinement (R-2), the **contact graph up to isomorphism** —
   which square/wall pairs touch, and along which edge classes.
   This is the mathematically right identity (it is what “same packing” means in the
   record catalogue) and it is what makes basin statistics comparable across move sets,
   which is the entire point of H-3 below.

Report both; treat geometric-key collisions as the fast path and structural identity as
the ground truth.

### <a id="r-2"></a>R-2 (blocking E4, weakening E2/E3): the refinement stage is presumed but never built — and it is a *linear program*

The spec’s basin record includes “its refined side length” and its open questions say
“float-plus-refine plus a final exact check”, but no Phase-1 or Phase-2 task builds a
refiner.
Without one, an annealer’s stopping point is not a local optimum, basin identity
(R-1) is unstable, and E4 measures artifacts of the cooling schedule.

The good news is that the refiner is cheaper than anyone has said, because of a
structural fact none of the five reports states:

> **For fixed angles, minimizing `s` is a linear program.** Fix every `θᵢ` and fix, for
> each pair, *which* candidate axis separates it (a “cell” of the configuration space).
> Each square’s corners are then affine in its centre `(xᵢ, yᵢ)`; the separating-axis
> condition “every corner of `B` beyond every corner of `A` along the axis” is 16 linear
> inequalities per pair; containment is linear; the objective `min s` is linear.
> All the nonconvexity of this problem lives in the angles and in the combinatorial
> choice of cell.

**Verified numerically in this review**, not just by inspection: fixing the eleven
angles at Trump’s values and fixing each pair’s separating axis from the exact
certificate yields a 1,056-constraint LP whose optimum is `s = 3.877083590023` — equal
to the reference value at solver precision (difference below `10⁻¹²`) — and whose
solution recovers all eleven centres to `9 × 10⁻¹⁶`. The cell containing Trump’s
packing, solved as an LP, *is* Trump’s packing.

Consequences, in increasing order of ambition:

- **The polish step is an LP solve** per cell, exact to LP precision, with *rational*
  output. Alternate with local angle moves (the cell’s active set tells you which
  contacts bind, hence the gradient in angle space) and you have a refiner that
  terminates at genuine cell-optima.
  This should be a Phase-2 task.
- **The search space collapses.** The honest continuous dimension is `n` (the angles),
  not `3n + 1` — and empirically far less, because records use very few distinct angles
  (Trump’s `n = 11`: one non-trivial angle; `s(17)`: two).
  See H-1.
- **Rational-angle cells need no number field at all.** At a Pythagorean tilt like
  `arctan(3/4)`, every coordinate and the LP optimum are rational, so exact verification
  is `ℚ`-arithmetic — degree 1. The exact layer’s cost is a function of the *angle’s*
  algebraic complexity, which the search can choose.

This observation is this review’s main theoretical contribution and feeds H-1, H-2, and
H-5.

### R-3: there is no calibration ladder — the machinery has no health metric

The spec’s E2 tests `n = 11`, where the answer is *conjectured*. The machinery needs
targets where the answer is *proved and easy*: `n = 5` (`2 + ½√2`, one 45° square) and
`n = 10` (`3 + ½√2`). “Budget-to-known-optimum” on these, tracked run-over-run with
pinned seeds, is the speed-and-accuracy metric the user asked for: every engine change
re-runs the ladder, and a regression is a test failure, per the FrankenSim rule the docs
already adopted. The ladder also calibrates E4’s basin statistics on cases where the
landscape is believed simple before they are computed where it is not.

### R-4: E3’s negative-result standard is named as an open question but the answer is available — saturation

“We searched `n = 12` and found nothing” means nothing without a stated budget; the spec
says so and stops. The standard should be the **basin-discovery curve**: new (canonical)
basins found per unit budget, reported with its plateau.
“Searched to saturation” — the discovery rate fell below a pre-registered threshold with
the curve attached — is a defensible negative result, and it is *reusable*: the same
curve is E4’s main plot and H-7’s test object.

### R-5: the proof lane’s smoke test should be the falsifier, and it has a beautiful known answer

The spec’s proof-lane hook is `hits_all_poses` (prove a point set unavoidable).
But the *cheap* direction is the **falsifier**: search for a single pose avoiding all
points — three parameters, same predicate, no PoseBox needed.
And this repository already owns the perfect known-answer test: the review of 2026-08-22
established that Stromquist’s ten Figure-13 points are **not** unavoidable
("nonavoidance lemmas apply to all of the regions shown *except for the rectangles at
the top and bottom*") while his twelve Figure-14 points are.
So:

- falsifier on the 10-point set at `s = 2 + 4/√5` → must **find** the escaping box, in
  the top/bottom rectangle;
- falsifier on the 12-point set → must saturate without finding one;
- PoseBox, later, → must *prove* the 12-point set unavoidable on a coarse subdivision.

That triple is the proof-lane analogue of the verifier’s negative controls, it
machine-checks our own correction of Stromquist’s proof structure, and it turns the
lane’s first experiment from “build speculative machinery” into “reproduce a known
asymmetry.”

### R-6: seeding strategy is absent, and the corpus says what it should be

The record catalogue’s own annotations describe how records actually move: “Extends the
`s(17)`…”, “combining two copies of the `s(50)`…”, “with 2 squares removed and 8
straightened.” One entry even extends `s(11)` itself.
Neighbor transfer is the field’s dominant productive move and the spec never mentions
seeding at all. For `n = 12` specifically: seed from Trump’s 11 plus one square in the
gap region, from the 13-grid minus one, and from straightened variants.
Cheap, and H-4 makes it measurable.

### R-7: coverage is aspired to but not defined

“Cover a lot of the search space per run” needs an operational meaning or it will be
claimed and not measured.
Proposal: stratify restarts over **angle-signature space** — the multiset of distinct
tilt angles, binned — using low-discrepancy (Sobol-style) sampling within strata, and
report per-run: strata visited, new canonical basins, new contact-graph classes.
Coverage is then a number, and “the run explored broadly” is checkable.

### R-8: the target list is one case too narrow

`n = 11` and `n = 12` are right, but the frontier corpus built two days ago surfaced the
three narrowest open gaps in the table — `n = 97, 78, 61`, the unproved tail of
`s(m² − 3) = m` — and the plan ignores them.
They are *cheap* to attack opportunistically (any sub-grid packing at those `n` is an
instant new record and kills a conjectured family, exactly as Cleemann’s 272 killed
`s(n² − n) = n` at `n = 17`), and H-5 gives a concrete construction hypothesis.
A standing “opportunistic slot” in every campaign costs little and is where the
highest-variance payoff lives.

### R-9 (Lean doc): one verified checker, many certificates

The Lean study recommends formalizing `s(11) ≤ …` as a theorem, which reads as a
per-packing proof script.
The scalable architecture — and the one its own `K₈(4,2) = 23` deep-dive actually models
— is different: **formalize the certificate checker once** (a verified decision
procedure over the certificate JSON: field description, coordinates, per-pair
axis-or-contact witnesses), and then every packing theorem is one invocation over data.
Corollary for Phase 1: the certificate must embed the *field-element representations* of
the coordinates, not just decimals, so the Lean side replays without re-deriving.
This is a small change to the certificate schema and should be made before it is
versioned.

### R-10 (minor consistency): budgets should be denominated in pair-tests

Wall-clock budgets are machine-dependent and the repo rightly refuses unpinned
performance claims. The SAT counter is the natural machine-independent currency: express
run budgets, saturation thresholds, and the ladder metric in **pair-tests** (the
infrastructure doc already prices them: ~63.6 G/core-hour in Rust), with wall-clock
reported alongside as a courtesy.

## The hypothesis register

The user’s ask, made concrete: a standing list of *productive-looking hypotheses*, each
with grounding, a test, a budget tier (S/M/L in pair-tests: 10⁹ / 10¹¹ / 10¹³), and a
**kill criterion** decided before the run.
The register lives with the run ledger and is pruned in the open — a retired hypothesis
stays listed with its evidence.

**H-1 · Angle-class reduction.** *Optimal packings at `n ≤ ~30` use at most 3 distinct
tilt angles, so a two-level search — outer: (class count, class assignment, angles);
inner: LP-in-cell (R-2) — beats free `3n`-dimensional annealing per unit budget.*
Grounding: Trump’s 11 (one angle), `s(17)` (two), the rational-tilt families; the corpus
can be mined for the distribution once the SVG parser lands.
Test: ladder + `n = 11`, same budget, versus baseline annealer.
Kill: fails to reach known optima the baseline reaches, or the corpus mining shows angle
counts growing fast with `n`. Tier M.

**H-2 · LP-in-cell polish is exact and sufficient.** *Alternating per-cell LP with local
angle moves refines any annealer output to a genuine cell-optimum whose side matches the
analytic value to LP precision on solved cases.* The single-cell half is already
established — this review’s LP at Trump’s angles reproduced `s(11)` and the centres to
machine precision — so what remains under test is the *loop*: angle moves between LP
solves, and behaviour at cell boundaries.
Test: polish annealer output at `n = 5, 10, 11` from perturbed starts; compare against
the known algebraic values.
Kill: cycling between cells, or systematic gaps to the analytic optima.
Tier S. **Highest priority: R-1 and R-2 both wait on it.**

**H-3 · Basin frequency anti-correlates with contact count.** *Rarer basins are more
rigid: the record basin’s attraction frequency falls with its number of contacts (and
with the algebraic degree of its optimum).* Grounding: Ellsworth’s 4-in-3,004 for the
heavily-pinned `s(51)` record.
Test: E4 data on the ladder plus `n = 11`, correlation of canonical-basin frequency with
contact count from R-1’s structural key.
Kill: no monotone relationship at `n ≤ 11`. Tier M. If it *holds*, it yields a practical
steering rule: bias search toward high-contact configurations early.

**H-4 · Neighbor-transfer seeding dominates random restarts.** *Seeds built from `n ± 1`
records (add a square in the largest gap; remove one and straighten) reach target side
lengths in materially less budget than random starts.* Grounding: R-6 — it is how the
human record table actually advances.
Test: `n = 12` seeded from 11 and 13 versus cold starts, same budget.
Kill: no improvement in budget-to-side-4+ε. Tier S.

**H-5 · The `m² − 3` family fails at `m = 10`.** *A Cleemann-style construction with
squares tilted at `arctan(3/4)` (the 6–8–10 Pythagorean angle, mirroring Cleemann’s
8–15–17 `arctan(8/15)` at side 17) packs 97 unit squares in side `< 10`.* Honest prior:
**low** — the `m² − 3` slack is 3 cells against `m² − m`’s full row of `m`, and
Nagamochi *proved* offsets 1 and 2 tight — but the cost is near zero (the construction
can be attempted analytically, on paper, before any engine exists), the payoff is a new
record plus a dead conjecture, and the family is where the frontier table says the
narrowest gaps are. Test: analytic attempt, then targeted search at side `10 − ε` (and
`9 − ε` at `n = 78`). Kill: the analytic geometry visibly cannot re-synchronize with the
grid; search saturates.
Tier S analytic, M search.

**H-6 · LP duals design unavoidable sets.** *Discretize poses and candidate points,
solve the fractional-transversal LP at container side 4 (for `n = 12`) and at sides in
`(3.7889, 3.8771)` (for `n = 11`); the dual solution’s support concentrates on
structured loci — and those loci are where unavoidable points/segments/families want to
live.* Grounding: the main report’s transversal section — the field drifted to
fractional certificates by hand; the LP computes them.
A discretized LP proves nothing, but as a *generator* of candidate certificates for the
falsifier/PoseBox loop (R-5) it is the first mechanized step anyone would have taken in
the proof lane. Test: does the dual support at side 4 resemble any known unavoidable-set
geometry? Kill: dual support is diffuse/unstructured at all tested resolutions.
Tier M.

**H-7 · Saturation curves are lawful.** *Basin-discovery curves have a stable parametric
shape (per `n`, per move set), so “fraction of basins found” can be estimated from the
curve — turning negative results into estimates.* Test: fit on ladder cases where
near-exhaustion is plausible; check stability at `n = 11`. Kill: fits are unstable
run-to-run. Tier M, piggybacks on E4.

**H-8 · The false-basin rate is nonzero and grows with `n`.** *Float-refined basins that
the exact verifier rejects exist at measurable rate `r(n)`.* This is the
machinery-accuracy metric: `r` is why the exact layer exists, and tracking it quantifies
the tolerance blind spot on real search output rather than on constructed controls.
Test: exact-verify every recorded basin in every run (E4 already wants this).
Kill: none — any value of `r` is a result.
Tier free (a counter on existing work).

**H-9 · Symmetry dedup changes counts materially.** *Canonicalization (R-1) merges a
significant fraction of naively-distinct basins, so any comparison with Ellsworth’s
published counts requires stating the dedup.* Test: report raw vs canonical counts on
the ladder and `n = 11`. Kill: none — the ratio is the deliverable.
Tier free.

**H-10 · The Stromquist triple reproduces.** *The falsifier finds the stage-one escape
on the 10-point set, saturates on the 12-point set, and PoseBox later proves the latter
unavoidable.* (R-5.) This is a known-answer test, so its “kill criterion” is inverted: a
failure is a machinery bug by definition.
Tier S.

H-11 through H-15 were added later the same day as the boil-down of
[A Search Philosophy for Square Packing](../research/research-2026-08-23-search-philosophy-and-landscape-cartography.md)
— the strategy layer captured after this review was first committed.
They share one premise (record basins are rare because records are rigid, so the basin
*atlas* is the deliverable and records are corollaries), and they are ordered so that
the premise itself is tested first and in the cheapest tier.

**H-11 · The small-`n` landscape is censusable.** *LP-quenching multistarts at `n ≤ 10`
yields a basin count that saturates: the discovery curve plateaus within tier-S budget,
giving a near-complete atlas with canonical identities and exact side lengths.*
Grounding: R-2’s verified LP is the quench map; R-1’s keys are the identity; the
landscape at the proved cases is believed simple.
Test: multistart + LP polish + canonical dedup at `n = 5…10`; deliverables are the
discovery curves (R-4’s own standard) and the atlas as a soft-schema artifact.
Kill: no plateau by `n = 8` within tier S — enumeration will not scale to 11; fall back
to coverage estimation (H-7) over descriptor space.
Tier S. **Gates the atlas, and runs on the existing Python plus the validated LP — no
Rust required.**

**H-12 · Record basins are rare in quench measure.** *The proved-optimal basin’s quench
probability at `n = 10` — and Trump’s at `n = 11` — sits orders of magnitude below the
modal basin’s, and rarity tracks rigidity (contact count, algebraic degree).* This is
the strategy layer’s load-bearing premise, registered so it can fail.
Grounding: Ellsworth’s 4-in-3,004 at `s(51)`; the 14 zero-gap pairs of Trump’s packing;
extends H-3 from a correlation to the record-specific measurement.
Test: read directly off H-11’s census — rank basins by quench frequency and locate the
record basin in the ranking.
Kill: record-basin probability within ~10× of the modal basin’s — then blind multistart
plus polish is already an adequate strategy, cartography loses its main justification,
and the program reverts to raw throughput.
Tier S (a query over H-11’s data).

**H-13 · δ-continuation reaches basins that direct sampling misses.** *Tracking packings
from an inflated container (side `s* + δ`) down to `δ = 0` with an LP re-polish at every
step arrives in canonical basins — including record basins — at materially higher rate
than equal-budget direct multistart, and the bifurcation tree (basin splits and
vanishings along `δ`) is stable across seeds.* Grounding: continuation is the standard
rare-solution device, and the merge-`δ` between basins doubles as the atlas’s barrier
scale, so the same runs pay twice.
Test: `n = 10` first (does continuation reach the proved optimum from generic inflated
starts?), then `n = 11` (arrival rate in Trump’s cell versus direct sampling at equal
pair-test budget). Kill: at `n = 10`, continuation’s record-arrival rate is no better
than direct sampling’s — the ladder is retired as a discovery tool and kept only as a
landscape probe. Tier S for the `n = 10` leg, M for `n = 11`.

**H-14 · The superdisk ladder imports circle structure.** *Continuing packings along the
superdisk exponent from circles (`p = 1`) toward squares (`p → ∞`) preserves usable
structure: endpoints at `n ≤ 10` land in known square-packing basins, and the `p` at
which orientation symmetry breaks marks where square-specific mechanisms emerge.*
Grounding: the Jiao–Stillinger–Torquato superdisk results; the mature circle-packing
record literature at small `n`. Test: a small-`n` `p`-sweep with a float engine plus LP
polish at the square end; compare endpoint basins against the atlas.
Kill: endpoints are dominated by the same grid/45° basins direct search already finds —
no enrichment of oblique mechanisms, ladder retired.
Tier M, and last in line: it is the only hypothesis here needing new (non-square)
geometry machinery.

**H-15 · Illumination beats optimization for atlas-building.** *A MAP-Elites archive
keyed by mechanism descriptors (distinct-tilt-class count × contact-graph class, at
minimum) discovers more distinct canonical basins per pair-test than temperature-matched
restart annealing at `n = 10` and `11`, including rarer high-contact basins.* Grounding:
quality-diversity’s illumination results on deceptive landscapes — with the descriptor
caution from the strategy doc built in: single scalars are hackable (the grid maximizes
contact count), so the archive keys must separate the grid funnel from the rigid-rare
family, hence tilt-class × contact-class.
Test: equal budget, same move set and polish backend, archive versus restarts; the
deliverables are basins-per-`10⁹`-pair-tests (already a tracked series) and the filled
descriptor grid. Kill: distinct-basin rate under 1.5× restarts at equal budget — the
archive machinery is not paying for itself; descriptors are retained for dedup and the
atlas only, not for steering.
Tier M.

## The run protocol: freeform, with discipline

The register above only works if runs are cheap to start, uniform to compare, and
impossible to lose. Five rules:

1. **Every run has a manifest, and the manifest is a soft-schema artifact** in a `runs/`
   ledger (same discipline as `frontier/`): hypothesis id (or `explore`), engine version
   and config hash, seed block, budget in pair-tests (R-10), machine fingerprint,
   metrics out, and a freeform notes body.
   The frontmatter is for comparison; the body is for thinking.
2. **The portfolio split keeps runs freeform *and* comparable.** A standard run spends
   ~70% of budget on the current-best configuration (so the baseline series stays
   continuous), ~20% on stratified coverage (R-7), ~10% on the run’s registered
   hypothesis or wildcard.
   One hypothesis per run.
3. **Every run leaves a residue.** A metric point on a tracked series, a new canonical
   basin, a counterexample, or a retired hypothesis.
   A run that would leave nothing is redesigned before it is launched.
   (This is the claim-integrity rule applied to experiments.)
4. **Baselines are pinned; comparisons share seed blocks and budgets.** An engine change
   re-runs the calibration ladder (R-3) before its results are compared with anything;
   ladder regressions are failures, not footnotes.
5. **Kill criteria are written before the run**, in the register.
   Retirement is recorded with evidence, not deleted — negative results are corpus.

Tracked metric series (the “is the machinery getting better” dashboard the user asked
for): ladder budget-to-known-optimum; pair-tests/sec/core; basins per 10⁹ pair-tests;
canonical-dedup ratio (H-9); false-basin rate (H-8); exact-path filter rate;
saturation-curve parameters (H-7); determinism digest (must be bit-stable).

## Series and priorities

**S0 · Smoke and calibration (first, as the user proposed).** Purpose: prove all the
machinery works end to end and establish every baseline metric, on `n = 11` and the
ladder. Contents: oracle-conformance and determinism digests; ladder runs at `n = 5, 10`
(R-3); a small `n = 11` smoke (does the engine find *any* valid sub-4.0 packing; does a
seed replay bit-identically on 1 and 32 workers; does exact verification accept the
basins — H-8’s first data point); the Stromquist falsifier triple’s first two legs
(H-10); H-2’s polish check.
**Pass criteria:** ladder optima reached; digests stable; zero oracle divergence; every
metric series has its first point.
S0 is also the *machinery-improvement* loop: iterate engine speed/accuracy against the
ladder until the floors in the plan spec are met.

**S1 · `n = 11` baseline campaign.** E2 at scale with R-1/R-2 in place: canonical basin
statistics, saturation curve, H-3’s correlation, H-1 versus baseline.
`n = 11` is the right flagship exactly as the user says: the most straightforward to
search, however hard it may be to *win* — and any outcome (rediscovery statistics, a zoo
of near-optimal basins, or a surprise) is publishable into the frontier corpus.

**S2 · `n = 12`.** In parallel and cheap: H-4 seeding, saturation standard (R-4), and
H-6’s LP-dual probe at side 4 feeding the falsifier.
`n = 12` is where search and proof lanes meet — the search maps the side-4 neighborhood
while the LP dual suggests certificates for it.

**S3 · Opportunistic `m² − 3` slot.** H-5’s analytic attempt immediately (it needs no
engine), and a standing low-budget search slot at `n = 61, 78, 97` inside every campaign
(R-8).

**S4 · Proof-lane series.** After PoseBox: complete H-10’s third leg, then H-6’s
candidates into falsify-or-verify loops at `n = 12`.

**S5 · Structured search.** H-1’s two-level angle-class engine as a first-class
alternative move set, compared on the ladder and S1 baselines; contact-graph enumeration
for small `n` as its natural extension.

**S6 · Landscape cartography.** The strategy layer’s series (see
[A Search Philosophy for Square Packing](../research/research-2026-08-23-search-philosophy-and-landscape-cartography.md)):
build the basin atlas and test the premise behind it.
In order: H-11’s census at `n ≤ 10`, with the atlas shipped as a soft-schema artifact
and the descriptor definitions versioned alongside it; H-12’s rarity measurement read
off the census (the premise test — if it fails, S6 contracts to a dedup library and the
program reverts to throughput); H-13’s δ-continuation at `n = 10` then `11`, whose
merge-`δ` data doubles as the atlas’s barrier estimates; H-15’s archive-versus-restarts
comparison on the same machinery; H-14’s superdisk probe last, as the only item needing
new geometry. S6 *interleaves* with S1 rather than following it: S1’s E4 byproducts are
H-11’s inputs, and the atlas is where S1’s “zoo of near-optimal basins” outcome becomes
a publishable artifact.
The LLM lanes the strategy doc describes (atlas reading, constructor DSL) hang
downstream of S6’s first artifact and are deliberately not scheduled until it exists.

Ordering rationale: S0 gates everything (no trusted metric without it); S1 and S2 are
the flagship and its cheaper sibling and can interleave on the same machinery; S3 costs
almost nothing and carries the tail risk of an actual discovery; S4 and S5 are
hypothesis-driven and should wait for stable baselines rather than compete with them.
S6 rides S1’s machinery and byproducts, and its first two items (H-11, H-12) are the
cheapest available test of the strategy premise — worth running early for that reason
alone.

## Changes recommended to the plan spec

Applied as beads rather than edits (the spec stays Draft; these become tasks under its
epics): add the refinement/polish task (R-2) and canonical basin key (R-1) to Phase 2
with E4 dependent on both; add the calibration ladder (R-3) and the falsifier triple
(R-5) to Phase 2; add the run-ledger/hypothesis-register protocol as a toolkit-level
task; register H-5 and H-6 under the research program.
One Phase-1 amendment worth making before the certificate schema is versioned: embed
field-element coordinate representations (R-9).

## Methodology

Conducted 2026-08-23 against the branch at PR #4. This is a theory review: no new
measurements were taken and no external sources consulted; every grounding claim traces
to the five research reports, the frontier corpus, the archived primary sources, or the
record catalogue capture (checked: the `n!·4ⁿ` symmetry statement, the spec’s
presumed-but-unbuilt refiner, the catalogue’s neighbor-extension annotations, and the
Stromquist two-stage structure).
The LP-in-cell observation (R-2) was verified two ways: by inspection of the constraint
structure (corners affine in centres for fixed angles, 16 linear inequalities per pair
per axis choice, linear objective), and **by implementation** — a 1,056-constraint
`scipy` LP at Trump’s fixed angles, with the axis assignment read from the exact
certificate, reproduced `s(11)` to solver precision and every centre to `9 × 10⁻¹⁶`. H-2
remains registered because the *refinement loop* (alternating LP with angle moves, cell
changes at degeneracies) is still untested; the single-cell solve no longer is.
Confidence: high on R-1 through R-10 as gaps (each is checkable against the documents in
a minute); the hypotheses are deliberately stated with priors and kill criteria instead
of confidence claims — that is what the register is for.
Extended later the same day: H-11–H-15 and S6 register the directions of the
search-philosophy capture; their content traces to
[that document](../research/research-2026-08-23-search-philosophy-and-landscape-cartography.md)
and through it to the same grounding set (the verified LP result, the corpus statistics,
the archived primaries), with its external strategy precedents kept out of the packing
evidence base per that document’s methodology note.

## References

- [A Search Philosophy for Square Packing](../research/research-2026-08-23-search-philosophy-and-landscape-cartography.md)
  — the strategy layer behind H-11–H-15 and S6.
- [Infrastructure for Square-Packing Exploration](../research/research-2026-08-22-infrastructure-for-packing-exploration.md)
- [Lean for Square-Packing Proofs and Validation](../research/research-2026-08-22-lean-for-packing-proofs-and-validation.md)
- [Minimal packing toolkit plan spec](../specs/active/plan-2026-08-22-minimal-packing-toolkit.md)
- [Packing 11 Unit Squares in a Square](../research/research-2026-08-22-packing-11-unit-squares.md)
  — the Stromquist two-stage structure (R-5), the transversal/fractional-certificate
  thread (H-6), the strategy catalogues.
- [Frontier corpus](../../../frontier/README.md) — the `m² − 3` gaps behind R-8/H-5.
- Record catalogue capture (`resources/web/kingbird-squares-in-squares`) —
  neighbor-extension annotations behind R-6/H-4; the `s(51)` basin statistics behind
  H-3.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
