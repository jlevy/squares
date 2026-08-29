---
title: X-003 — stratified chunk enumeration as a constructive proposer
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-003
  title: Stratified chunk enumeration as a constructive proposer
  date: '2026-08-26'
  author: Claude (agent), from a design discussion with the repository owner
  campaign: packing.squares
  brief: >-
    Consolidate a design discussion on enumerating packings as arrangements of aligned
    chunks plus a few rotating chunks: grade the discussion's intuitions against the
    archive, map its pipeline onto the built quench machinery, record the prior art on
    from-scratch rediscovery of Trump's packing, and mine hypothesis candidates for the
    unbuilt proposer layer.
  sources:
  - TUTORIAL.md
  - SYNOPSIS.md
  - docs/project/research/research-2026-08-22-packing-11-unit-squares.md
  - docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md
  - docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md
  - resources/papers/gensane-ryckelynck-2005-improved-dense-packings.raw.md
  - resources/papers/friedman-ds7-packing-unit-squares-in-squares.md
  - resources/papers/stromquist-2003-packing-10-or-11-unit-squares.md
  - resources/web/kingbird-squares-in-squares.md
  - resources/web/kingbird-squares-in-squares-compared.md
  - campaign/ideas.md
  - campaign/ledger.md
  proposes: [H-044, H-045, H-046, H-047, H-048]
---
# X-003 — stratified chunk enumeration as a constructive proposer

This report consolidates a 2026-08-26 design discussion between the repository owner and
an agent into a mineable idea source for the proposer layer, which the synopsis names as
the record-finding lane’s live bottleneck: the refiner takes proved controls to `1e-15`
and leaves the tested `n = 11` starts at `6e-02`, and proposal is the layer with the
fewest built parts. Nothing here spends experiment budget or asserts a scientific
verdict.

## The Ansatz

Record packings are arrangements of a few **chunks**: aligned bars, Ls, and rectangles
seated against walls and corners, plus one or two chunks that rotate as rigid groups at
a shared angle. The proposal is to enumerate the discrete arrangement data exhaustively
and let the built LP and quench machinery do everything continuous.

The two most celebrated oblique records are instances.
Trump’s `n = 11` packing decomposes as one corner square, one mirrored against the
opposite side, one offset along the top, an L-shaped block of three, and a five-square
group tilted as one rigid unit
([the exact construction](../../../docs/project/research/research-2026-08-22-packing-11-unit-squares.md#trumps-packing-1979-structure-and-exact-characterization)).
Bidwell’s `n = 17` record is an aligned frame plus two tilted groups at `+39.80496°` and
`-36.62379°`.

## The Discussion’s Intuitions, Graded Against the Record

1. **Records use few angle classes.** Partially true.
   Trump uses two classes and Bidwell three, but
   [exp-037](../series/series-000-smoke-and-calibration/experiments/exp-037-h-042-n29-numerical-angle-classes.md)
   measures six numerical classes in the retained `n = 29` record serialization,
   rejecting the registered three-class claim.
   The defensible quantitative form is
   [H-025](../hypotheses/H-025-record-angle-compressibility.md) (compressibility to
   three fitted classes at `1e-4` side cost), registered and never run.
2. **Squares cluster in adjacent groups, rows, and offset rows.** True of the
   constructive record corpus: 45° families, diagonal strips, strip-plus-L augmentation,
   and composition are catalogue strategies 3 through 8, and a grep of the archived
   compared catalogue capture counts 15 extension, based-on, combining, or rearrangement
   annotations.
3. **Optima are perturbations of cleaner, slightly larger regular predecessors.**
   Partially true, with two cautions.
   Friedman’s DS7 records that Trump improved Göbel’s earlier 11-square packing, and
   Bidwell’s record is annotated as based on Hämäläinen’s 1980 packing.
   But Stromquist’s Theorem 3 proves no `0°/45°` packing reaches Trump’s side, so the
   `n = 11` “perturbation” crosses a proved structural boundary; and
   [T-3](../../../SYNOPSIS.md#the-corner-and-the-method-it-forced) shows the
   perturbation endpoint is a nonsmooth corner, not a smooth critical point.
4. **Perturbing a regular packing beats cold search.** Plausible and registered three
   ways ([H-004](../hypotheses/H-004-neighbor-transfer-seeding.md),
   [H-013](../hypotheses/H-013-delta-continuation.md),
   [H-030](../hypotheses/H-030-public-parent-surgery.md)), none run.
   Two counter-data: the exactly jammed grid admitted no escaping local move (the
   fixed-side dead end on the [idea board](../ideas.md#dead-ends)), and
   [exp-005](../series/series-000-smoke-and-calibration/experiments/exp-005-basin-entry-n11.md)
   showed the default schedule wandering away from a start `1e-5` off Trump’s pose.
   Perturbation needs slack, which is the container-inflation ladder’s role.
5. **Regularity returns at large `n`.** Supported: Erdős–Graham asymptotic constructions
   are grid bulk plus structured boundary layers, and the `m² - 3` grid records at
   `n = 61, 78, 97` carry the narrowest gaps in the corpus.
   The weakest regime for the ansatz is the mid-range annealing records, where minimal
   polynomial degrees reach 42 (`n = 41`) and 44 (`n = 87`).

## The Pipeline, and What Is Already Built

A **stratum label** is discrete data: a partition of `n` into chunk sizes, a lattice
skeleton per chunk (bar, L, rectangle), an angle-class assignment naming which chunks
tilt, and a contact hypothesis on the graph of chunks plus the four container walls.

| Stage | Action | Status |
| --- | --- | --- |
| 1 | Enumerate stratum labels, symmetry-reduced | **unbuilt — the invention** |
| 2 | Glued LP screen: equality rows fix intra-chunk offsets | unbuilt, but only the glue rows are new |
| 3 | Soft LP to a cell fixed point: free centers at fixed angles | built ([`sqpack.research.quench`](../../src/sqpack/research/quench.py) inner loop) |
| 4 | Class-angle bracketing: tilted chunks rotate as units | built (quench outer loop; T-3’s corner mandates bracketing over gradients) |
| 5 | Free-angle audit: each of the `n` angles bracketed individually | built (the quench’s final pass) |

Three facts from the built record make the division of labor exact:

- **Slides are free.** At fixed angles the optimal placement is one LP solve at the
  measured `1.28 ms` ([T-2](../../../SYNOPSIS.md#the-cell-decomposition)); brickwork
  offsets and row compressions are outputs, not search dimensions, so stage 1 enumerates
  lattice skeletons only.
- **The cell is the pairwise constraint.** A stratum compiles to a cell by realizing a
  placement and reading the cell off it; the fixed-point loop then repairs imperfect
  hypotheses by migrating one arrangement at a time.
  The reverse direction is already verified: rebuilding the LP from the cell read off
  Trump’s certificate returns the published side to `4.4e-16` with the centers never
  given to the solver.
- **The combinatorics collapses at the chunk level.** The unrestricted cell count is
  `8^C(11,2) ≈ 5e49`; with `k ≈ 5` chunks the free inter-chunk combinatorics is on the
  order of `8^C(5,2) ≈ 1e9` before symmetry reduction and feasibility pruning, times
  polynomial partition and skeleton counts.
  That reduction is substantial, but `1e9` before partition and skeleton factors is
  still a feasibility blocker.
  A finite bound, an orbit count, and an omission control must precede implementation.

Angle constraints, stated once: the LP requires every angle fixed to a number and places
no restriction on the values; the class count controls only the outer search dimension
and the enumeration size.
No angle can be pinned without loss of generality in a square container, so “the frame
chunk sits at `0°`” is part of the stratum label.

## The Ranking Rule

Aligned stage-1 side values cannot rank strata: every all-aligned arrangement of 11
squares sits at side `4.0`, including the stratum that becomes Trump’s after rotation,
so the coarse stage systematically undervalues exactly the strata that become records.
The consequence is a design rule, not a defeat: **every stratum surviving feasibility
gets a coarse angle sweep before any triage**, at roughly `0.13 s` per tilted-chunk
dimension for a 100-point scan at the measured LP cost.
This is the residue, inside a stratified design, of the grid-funnel lesson that a scalar
shared by the grid and the record cannot separate them.

## Prior Art on From-Scratch Rediscovery

- **Gensane–Ryckelynck 2005** (billiard/inflation, archived): *“We have obtained this
  packing several times with s11 = 3.87708359…”*, after thousands of random-start
  billiard runs; the same section notes the procedure *“seems to be ‘attracted’ by
  configurations with angle θ = 0 which are rarely good.”* Their program also “leads to”
  Bidwell’s `n = 17` figure, with the text ambiguous about cold versus seeded starts.
- **Berthold, Kamp, Mexi, Pokutta, Pólik 2026** (SCIP 10 and FICO Xpress 9.8, recorded
  in
  [the algorithms report](../../../docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md#general-purpose-global-optimization)):
  `3.87709` at `n = 11` from scratch on a 48-core budget; `4.00001` at `n = 16`, missing
  the trivial grid; `4.67682` at `n = 17`, short of Bidwell.
- **This repository’s negatives**:
  [H-016](../hypotheses/H-016-stock-annealer-reaches-standing-best.md) refuted (`3.9144`
  at `n = 11` on every seed), and
  [exp-011](../series/series-000-smoke-and-calibration/experiments/exp-011-h-020-n17.md)
  returning the bare grid at `n = 17` on all five seeds.

So `n = 11` rediscovery exists at cost, and a cold `n = 17` rediscovery would be, on
this archive’s evidence, a first for any published method.
The differentiating deliverable of enumeration is therefore not rediscovery but
**coverage semantics**.

## Coverage Semantics, and the Proof-Shaped Upgrade

Enumerate-then-solve can be exhaustive within each emitted stratum, and a stratum’s
identity is its label rather than a floating-point endpoint key.
Completeness of the atlas is conditional: the grammar and every bound must be finite and
explicit, the label generator must have an omission control, and the symmetry quotient
must have a coverage certificate.
With those controls, the upper-bound lane can sidestep the terminal-component identity
blocker ([D-034](../../../defects.md)) rather than waiting on it, and the method prices
itself in counted LP solves, the machine-independent work unit
[D-126](../../../defects.md) asks for.

The certified upgrade is the interesting endgame: per-stratum optimization made rigorous
(exact or interval LP over the cell, certified bracketing over the class angles) yields
restricted-class optimality statements of the form “no packing expressible as `k`
aligned chunks plus one rotating chunk beats Trump’s.” Stromquist’s Theorem 3 is the
only existing theorem of that shape at `n = 11`; the prerequisite is the exact LP named
as the general fix for [D-021](../../../defects.md).

## Registry Relations

[H-001](../hypotheses/H-001-angle-class-reduction.md) asserts the angle-class half of
the ansatz with no enumeration stage behind it; this design supplies that stage.
[H-025](../hypotheses/H-025-record-angle-compressibility.md) prices how large `k` must
be for the grammar to cover the record corpus, and
[H-030](../hypotheses/H-030-public-parent-surgery.md) is the registered calibration for
the insertion and surgery moves.
[D-052](../../../defects.md) (a stopped quench is not a certified optimum) and
[D-059](../../../defects.md) (degeneracy at symmetric angles) bound what stage-5
endpoints may claim.

## Hypotheses Codified From This Report

Five claims are registered; all five carry `instrument_ready: false`, so the ledger
reads them as blocked until the tooling beads land.

- **[H-044](../hypotheses/H-044-chunk-expressibility-of-records.md) — coverage.** Are
  standing records already chunk-structured?
  Measurable from archived geometry with no search, so it can refute the ansatz before
  an enumerator exists.
  Registered first for that reason.

- **[H-045](../hypotheses/H-045-chunk-grammar-rediscovery.md) — rediscovery ladder.**
  Does a grammar frozen on the proved cells rank the standing best first at `n = 11`,
  with `n = 16` as guard and `n = 17` as differentiator?

- **[H-046](../hypotheses/H-046-regular-predecessor-continuation.md) — predecessor
  continuation.** Does a class-angle path run from Trump’s aligned form to the record
  without chunk fission, and how many cells does it cross?

- **[H-047](../hypotheses/H-047-chunk-regular-predecessors.md) — predecessor round
  trip.** Does rounding a pose to its chunk-regular predecessor and re-quenching return
  the pose, for ordinary endpoints as well as records?
  This is what decides whether the chunk decomposition is a coordinate system for search
  or only a description of one.

- **[H-048](../hypotheses/H-048-glued-screen-fidelity.md) — screen fidelity.** Does the
  cheap glued screen keep the soft-mode winner in its top decile?
  An efficiency claim the enumerator’s cost model already assumes.

## Risks and Open Edges

Coverage is a reduction: the grammar may exclude records.
The six angle classes measured at `n = 29` price the fitted-angle count `A` and the
outer bracketing dimension; they do not determine the chunk count `C`. Chunk fission
must be a grammar move or the coverage claim silently shrinks.
Stage 3 endpoints sit on corners, so nothing gradient-based enters the angle stage.
No rigidity-style bound on candidate chunk contact graphs exists to prune stage 1 beyond
feasibility; [H-043](../hypotheses/H-043-trump-incidence-rigidity-cores.md) is the
nearest registered step toward one.

## Post-Review Calibration Evidence

The 2026-08-26 PR review built the previously missing known-best atlas for every
`n = 1..100`. At the registered descriptive tolerances, 1,780 of 1,860 squares in the 36
non-grid records belong to a same-angle positive-edge-contact component; 25 of those 36
records use at most six such components and three free squares.
This strongly supports the broad assembly intuition.
Those non-grid components retain 859 internal slide degrees under their contact-normal
equalities before overlap intervals and wall seating are applied, so component count is
not a rigidity or low-dimensionality certificate.

It does not validate the narrower bar/L/rectangle grammar.
A conservative detector of maximal lattice components certifies only 21 of all 100
records. A subsequent bounded exact-cover splitter handles irregular components and
certifies all 64 grid-derived records and 3 of 36 non-grid records inside the proposed
six-chunk/two-free budget.
Two non-grid cases are conclusively outside that budget, 23 have no partition in the
implemented universe, and eight are search-capped and therefore indeterminate under the
declared limit.

The natural revision is to enumerate same-angle contact graphs with LP-resolved sliding
offsets, keeping rigid lattice chunks as a strict subgrammar rather than the whole
grammar.
The retained 1–100 corpus is now descriptive and calibration evidence because it
was inspected while the instrument was being designed.
Any confirmatory coverage claim needs a prospectively frozen corpus after the partition
contract and revised grammar are committed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
