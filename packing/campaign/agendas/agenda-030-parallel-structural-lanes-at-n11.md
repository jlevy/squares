---
title: agenda-030 — parallel structural lanes at n = 11
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-030
  title: Parallel Structural Lanes at n = 11
  updated: '2026-09-08'
  status: active
  objective: >-
    Run X-021's research sessions as parallel lanes with disjoint deliverables and files:
    nine measurement-or-theorem lanes that each decide one question about structural
    constraints on eleven-square packings at 96/25 and what the constraint buys a
    certificate, two lanes on the closing route, then one selection cell and one closeout.
    The numerical goal is unchanged from Agenda 029: a global exclusion at 96/25. Every
    lane records its site set or inputs with its result, because a non-refutation on a
    finite site set is never evidence. This planning checkpoint launches no research.
  items:
  - id: BC-291
    purpose: research
    owner_focus: insight
    instances: [11]
    state: complete
    priority: 0
    question: Which structural constraints on eleven-square packings can be proved now, and what does each buy toward 96/25?
    budget: One W10 planning block on 2026-09-08 with four Fable mathematical lanes at maximum effort and two Opus lanes; zero scientific target invocations.
    entry: The owner's instruction, X-019 and Agenda 029, the retained certificates, Stromquist's memoranda and 2003 paper, and the current CI state of the stacked pull requests.
    exit: X-021, H-127 through H-134, this agenda, the four retained lane reports, and the operating-rule changes in OR-2, OR-3 and OR-6.
    bead: think-cm07
    workflows: [review-planning-oversight, insight-iteration]
    depends_on: []
    program: n11-structure-and-conditional-dots
    artifacts:
    - packing/campaign/explorations/X-021-what-can-be-proved-about-eleven-squares.md
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/README.md
    next_evidence: The owner's research-start instruction; then the coordinator allocates session ids and dispatches the ready lanes below.
  - id: BC-292
    purpose: research
    owner_focus: insight
    instances: [11]
    state: ready
    priority: 0
    question: Does pricing the four corner blockers' cores above the rest, or banking their corner boxes, give a covering surplus at 96/25?
    hypotheses: [H-126, H-127]
    budget: One session of three to four hours on one core; class programs cost one to eight minutes per run at grid 79.
    entry: >-
      X-021's corner-class certificate (lane A Theorem A) and complete corner cover
      (Theorem B); classcert's two-threshold LP with a region predicate for cores; the
      3.82 site sets or the 3.81 atoms dilated. The convex half-plane clip for a deep
      corner is a small extension of sweep.centre_domain, not a new engine.
    exit: >-
      A certificate at 3.82 or 3.84 with its complement listed, or the scoped obstruction
      naming the tight corner cells on the site set; both the flush-four and the
      three-plus-one branches reported with their exact residual values.
    bead: think-kx2l
    workflows: [insight-iteration, research-loop, factual-review]
    depends_on: []
    parallel_group: lanes-corners
    program: n11-structure-and-conditional-dots
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-a-corner-structure.md
    next_evidence: Whether any corner information has value for a certificate at q; if the flush-four residual falls below seven, the first conditional exclusion with a named complement.
    note: Owns the region-class row generator and the centre-domain clip; no other lane edits those files.
  - id: BC-293
    purpose: research
    owner_focus: insight
    instances: [11]
    state: in_progress
    priority: 0
    question: Does a valid D4-symmetric measure at 96/25 exist with T-018's four corner atoms at weight at least 3/20 and total mass below 11 + 3/20?
    hypotheses: [H-128]
    budget: One session of three to four hours; column generation with lower bounds on five atom weights is an LP bound change with no geometry change.
    entry: >-
      X-021's ownership corollary (lane C, Corollary C.2): the four corner atoms cannot
      share a core, so the measure's existence is the theorem. Seed with T-018 scaled by
      384/381; exact decision by the eighth-turn sweep.
    exit: >-
      The theorem that every packing at 96/25 has four distinct squares containing the four
      corner atoms, with the price M(forced) − M(free) recorded; or the obstruction with the
      converged mass. Then the transfer automation dry run on T-018 (Lemma C) if time remains.
    bead: think-1136
    workflows: [research-loop, factual-review]
    depends_on: []
    parallel_group: lanes-corners
    program: n11-structure-and-conditional-dots
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-c-n10-transfer.md
    next_evidence: Pinned anchors for the frame-conditioned certificate (BC-287, H-111) and the two-pattern case split of the ownership-conditioned certificate.
  - id: BC-294
    purpose: measurement_validation
    owner_focus: correctness
    instances: [11]
    state: in_progress
    priority: 0
    question: What are the restricted fractional packing values at 96/25 off a corner box, a corner triangle, a central box and the four corner boxes, and the B = 1 value at 3.84, 3.86 and 3.87?
    hypotheses: [H-129]
    budget: One session of three to four hours on one core; cutting-plane loops of at most thirty minutes per region; verify_ceiling on every final family.
    entry: >-
      BC-200's family and state at 191/50 as warm start; the cutting-plane loop with a
      disjointness filter on the dual side and, for B = 1, ceiling.py's unit regime with a
      direction net dense near 0° and 40.18°. X-021's duality lemma (lane D, Lemma D) is the
      reading rule.
    exit: >-
      Per region an exact depth-scaled total classified as kill (at least 10), alive (below
      9.5) or undecided; and for B = 1 either a verified family of value at least 11 at some
      side below U with its weight outside Trump's neighbourhood, or a converged covering LP
      below 11 at 3.87.
    bead: think-7lp3
    workflows: [research-loop, factual-review]
    depends_on: []
    parallel_group: lanes-duality
    program: n11-structure-and-conditional-dots
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md
    next_evidence: Whether the non-convex-domain instrument (BC-204) is worth building; whether routes (b) and (c) and every capture design survive; the input BC-301 needs.
  - id: BC-295
    purpose: research
    owner_focus: insight
    instances: [11]
    state: in_progress
    priority: 0
    question: How wide a band around 0° and 45° can be excluded at 96/25, how wide is the optimal nine-point band, and where does the fractional obstruction live in angle?
    hypotheses: [H-130, H-131]
    budget: One session of three to four hours on one core; replay the planning-lane decisions first under a registered round, then widen.
    entry: >-
      Lane B's exact-verified band certificates and nine-point sets at grid 79 as controls;
      class_minima and decide_class_program as the exact verifier; ceiling.py as the depth
      oracle. Every result records its site set.
    exit: >-
      An exact-decided robust band [0, α] ∪ [45° − β, 45°] excluded at 96/25 with α + β of at
      least 3°, the registered replay of the at-most-nine and at-most-ten counts, and the
      angular support histogram of the dual when the band toward 40.19° stays at or above 11.
    bead: think-ndqj
    workflows: [research-loop, factual-review]
    depends_on: []
    parallel_group: lanes-angles
    program: n11-structure-and-conditional-dots
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-b-angle-classes.md
    next_evidence: The first band theorem new below U; whether the obstruction at q is Trump-shaped or an integrality artefact that geometric conditioning can target.
  - id: BC-296
    purpose: research
    owner_focus: insight
    instances: [11]
    state: ready
    priority: 1
    question: Which compositions (n0, 11 − n0) by near-axis count close at 96/25, and does a class-weighted fractional packing certify that no site set closes the rest?
    hypotheses: [H-102]
    budget: One session of three hours on one core; grid 119 and the dilated T-018 atoms as site sets; at most two hundred rounds per composition.
    entry: >-
      Lane B's grid-79 margins as the control (both Trump-like compositions survive with
      near-axis and tilted cores priced almost equally); the near class of the leading
      twenty-five cells with its exact count of nine.
    exit: >-
      The refuted compositions frozen with exact atoms and thresholds, and for each survivor a
      depth-one fractional packing with class weights at least (n0, 11 − n0); the boundary of
      the class-weighted packing polytope at q as found.
    bead: think-n6fr
    workflows: [research-loop, factual-review]
    depends_on: []
    parallel_group: lanes-angles
    program: n11-structure-and-conditional-dots
    next_evidence: Either the composition route ends at q with a certificate of its own impossibility, or the survivors become the branch list for geometric conditioning.
  - id: BC-297
    purpose: measurement_validation
    owner_focus: correctness
    instances: [11]
    state: ready
    priority: 1
    question: Is the exactly-eleven plateau at 191/50 a site artefact, what is the shrink tax there, and can the plateau be closed as an exact cover?
    hypotheses: [H-133]
    budget: One session of four hours; the artefact test is thirty minutes; the net refinement pilots at 600 directions before 1800.
    entry: >-
      Lane C's plateau analysis: Trump-shaped B-cores at 3.82 overlap only in strips of width
      about 0.0124 that a grid of pitch 0.047 misses; the transfer lemmas at ε = 0 make the
      packing's cores an exact cover of the atoms by eleven mass-one cells.
    exit: >-
      A certificate below eleven at 3.82 after adding sites in the strips or refining the net
      (a new rung through the retention gate), the measured tax Δτ*/Δ(1 − B), or the tight-cell
      census and the exact-cover verdict; a census above one million cells with no clustering
      is recorded as the obstruction.
    bead: think-4uon
    workflows: [research-loop, factual-review]
    depends_on: []
    parallel_group: lanes-ladder
    program: n11-structure-and-conditional-dots
    next_evidence: Whether the ladder's top is the instrument's or the geometry's; the size of the ownership tree.
  - id: BC-298
    purpose: research
    owner_focus: insight
    instances: [11]
    state: ready
    priority: 1
    question: What is the largest H0 below 3.84 such that eleven unit squares provably do not fit in the rectangle 3.84 × H0?
    hypotheses: [H-132]
    budget: One session of three to four hours; the change is confined to the rectangle centre domain in sweep, generate and interval, with the net spanning a quarter turn.
    entry: >-
      Lane D's Session S1 and lane A's Session S5: a rectangular container is convex, so the
      T-018 pipeline runs unchanged except for the domain and the symmetry group; H in
      {3.80, 3.81, 3.815, 3.82}.
    exit: >-
      A frozen rectangle certificate at some H0 of at least 3.81, the first rectangle bound
      for n = 11, or the converged restricted optimum at or above eleven at H = 3.81 as the
      scoped obstruction.
    bead: think-jsi8
    workflows: [pipeline-improvement, research-loop, factual-review]
    depends_on: []
    parallel_group: lanes-walls
    program: n11-structure-and-conditional-dots
    next_evidence: Every wall within 3.84 − H0 of a square, both extents at least H0, and with the spanning lemma the strongest symmetry-breaking premise available.
  - id: BC-299
    purpose: research
    owner_focus: insight
    instances: [11]
    state: ready
    priority: 1
    question: For which angle band do Stromquist's ten points localise every avoiding square at 96/25, and can an escape-tolerant two-branch certificate close the escapes?
    hypotheses: [H-126, H-111]
    budget: One session of three to four hours; the localisation reuses H-106's polynomial guards with q and the band as parameters; the two-branch certificate needs a small event-cell filter mutation-tested against the unfiltered sweep at 3.81.
    entry: >-
      Lane B's Session S6 and lane C's Session S4: the ten Figure-13 formulas at q, the
      anchored certificate (Lemma B) with the escape class as a filter on event cells and an
      asymmetric second measure on a quarter-turn net.
    exit: >-
      A localisation theorem at q for a band of at least 2°, or the escaping square; and the
      trade-off curve h ↦ (M0(E), w(E0)) showing which pose classes carry the binding rows, or
      a two-branch certificate at q.
    bead: think-4ifm
    workflows: [insight-iteration, research-loop, factual-review]
    depends_on: []
    parallel_group: lanes-anchors
    program: n11-structure-and-conditional-dots
    next_evidence: The premise every conditional certificate needs, a square forced into a known box, combined with the nine-point band into a concrete two-branch split.
  - id: BC-300
    purpose: research
    owner_focus: insight
    instances: [11]
    state: tentative
    priority: 2
    question: Does any packing below side 3.96 have a snug 45° corner square, four deeply avoided corners, or a confined rattler whose feasible angles avoid every neighbour's class?
    hypotheses: [H-117, H-121]
    budget: One session of two to three hours; float search seeded by Trump, Hämäläinen and the loosened Trump family, with exact SAT verification of any candidate.
    entry: >-
      Lane A's Session S4 and lane B's Session S5: a found witness is decisive and a failed
      search proves nothing; the mixed pocket's realisability is the local step of H-121.
    exit: >-
      Exact witnesses with their corner data, or a scoped no-witness note with the search
      budget; for the pocket, an explicit verified packing or a merging lemma for 0°/45°
      confinement.
    bead: think-dfof
    workflows: [insight-iteration, factual-review]
    depends_on: []
    parallel_group: lanes-witnesses
    program: n11-structure-and-conditional-dots
    next_evidence: Which corner branches cannot close near U, and whether the structural lane should spend time on elimination motions at all.
  - id: BC-301
    purpose: research
    owner_focus: correctness
    instances: [11]
    state: blocked
    priority: 1
    question: What do the exact-side tree over Q(u) and the B = 1 capture run at U + σ cost, written as one architecture?
    hypotheses: [H-129]
    budget: One session of two to three hours after BC-294's first result; feature gaps at Trump's pose from the exact pose; field-valued LP pricing with sqpack.exact_lp.
    entry: BC-294's B = 1 value near U; lane D's stability argument (‖v‖ ≤ 2σ/κ on the half-ball) and σ_max = κρ0/4.
    exit: A costed design for capture radii 0.05, 0.1 and 0.3, or the proof that the annulus needs angle subdivision below what the exact LP tolerates.
    bead: think-lbqe
    workflows: [insight-iteration, factual-review]
    depends_on: [BC-294]
    program: n11-structure-and-conditional-dots
    next_evidence: The only honest statement about the endpoint; if BC-294 kills capture, this reduces to the exact-side tree and needs BC-302 to be finite.
  - id: BC-302
    purpose: research
    owner_focus: insight
    instances: [11]
    state: ready
    priority: 1
    question: Is there a robust unavoidable set of at most eleven marks at 96/25?
    hypotheses: [H-134]
    budget: One session of four hours; T-018's ninety-three heaviest atoms as candidate marks; the exp-121 escape instrument as the falsifier engine.
    entry: >-
      Lane D's Session S6 and lane C's ownership analysis: marks may be thickened by the
      transfer tolerance 0.006; nonavoidance regions proved by Stromquist's Lemmas 1–4 as
      repaired and by H-106-style interval readers.
    exit: >-
      An eleven-mark set with a verified cover, or the catalogue of escape squares showing that
      every set of at most eleven marks built from the atom skeleton is avoidable.
    bead: think-qfog
    workflows: [insight-iteration, research-loop, factual-review]
    depends_on: []
    parallel_group: lanes-ownership
    program: n11-structure-and-conditional-dots
    next_evidence: If it succeeds, route (a) collapses to about two to the twenty exact LPs; the prior is about thirty per cent.
  - id: BC-303
    purpose: research
    owner_focus: insight
    instances: [11]
    state: blocked
    priority: 0
    question: Which lane results earn the next sustained block, and what is the strongest claim to freeze?
    hypotheses: [H-127, H-128, H-129, H-130, H-132, H-134]
    budget: One coordinator block of two hours after the first wave, with independent review of every lane's strongest claim before selection.
    entry: Every ready lane terminal with a result, a scoped obstruction or a stopped attempt, each with its inputs recorded.
    exit: One or two selected routes with frozen claims and accept rules, every other lane dispositioned, and the branch list for geometric conditioning if the composition route ended.
    bead: think-znzj
    workflows: [review-planning-oversight, factual-review]
    depends_on: []
    blocked_on: First-wave evidence from the ready lanes; no route is selected or funded by this planning checkpoint.
    program: n11-structure-and-conditional-dots
    next_evidence: The frozen claim for the next block and the remaining proof obligations.
  - id: BC-304
    purpose: research
    owner_focus: correctness
    instances: [11]
    state: blocked
    priority: 0
    question: What survives independent checking, what did it change about the global problem, and what is the next consequential question?
    budget: One closeout block of two hours with the final hour reserved for verification, integration and publication.
    entry: BC-303's selection and the block it funded, terminal.
    exit: Independently checked strongest result, honest bound impact, complete domain accounting, disposition of every lane, the discharge edges into Agenda 029, and one next consequential question.
    bead: think-yrw1
    workflows: [factual-review, documentation-pass, review-planning-oversight]
    depends_on: [BC-303]
    program: n11-structure-and-conditional-dots
    next_evidence: The owner reviews the mathematical result and the next selection.
---
# Agenda 030 — Parallel Structural Lanes at `n = 11`

**This agenda is prepared, paused and unstarted.** BC-291 is the W10 planning block that
wrote it, on 2026-09-08, at the owner’s request to pursue X-019’s exploration and to map
the coming sessions so that they run in parallel.
[X-021](../explorations/X-021-what-can-be-proved-about-eleven-squares.md) carries the
mathematics; this agenda is the operational handoff.
No scientific target, experiment, session or overnight automation is opened by
publishing it.

## How It Relates to Agenda 029

[Agenda 029](agenda-029-structural-restrictions-and-conditional-dots.md) planned one
coordinator and three workers inside one eight-hour clock with sequential second and
third blocks.
This agenda replaces its first block with eleven lanes that are disjoint in
deliverables and in files, so they can be handed to fresh sessions on either harness
without the coordinator present, which is what
[OR-6](../../../operating-rules.md#or-6-plan-multi-hour-work-in-slices-before-starting-it-as-parallel-lanes-with-disjoint-deliverables)
now asks for. The correspondence is:

| Agenda 029 cell | Taken up by |
| --- | --- |
| BC-285, corner structure under H-126 | BC-292 (corner-class LP and corner cover), BC-293 (corner-skeleton ownership) |
| BC-286, complete angle-count classes under H-102 | BC-295 (angle-band theorems), BC-296 (composition split) |
| BC-287, frame-conditioned capture under H-111 | BC-294 (kill tests, which decide whether the instrument is worth building), BC-299 (the anchored certificate) |
| BC-288, contacts and angles under H-117 and H-121 | BC-300 (witnesses and the mixed pocket); the contact lemmas themselves are proved in X-021 |
| BC-289 and BC-290, selection and closeout | BC-303 and BC-304 |

Agenda 029’s cells are not edited here; BC-304 records the `discharged_by` edges at
closeout, once the lanes are terminal, so that the older queue stops offering work this
agenda finished.

## The Lane Contract

Every lane is one session of two to four hours, owned by one agent, with:

- **one question**, stated in its cell, and one exit that counts — a theorem, a
  counterexample, or a scoped obstruction with the inputs that produced it;
- **its own files**: a result document under
  [`results/agenda-030/`](../series/series-000-smoke-and-calibration/results/agenda-030/README.md)
  named for the lane, plus any instrument extension named in its `note`; no lane edits
  another lane’s files or any shared registry;
- **its inputs recorded**: site set, grid, inset, net, shrink, atom lists, seeds — a
  non-refutation without them is not a result;
- **the falsifier stated before the run**, and the exact verifier
  (`decide_class_program`, `class_minima`, the interval route, `verify_ceiling`) as the
  only thing that turns a float optimum into a claim;
- **a checkpoint at most thirty minutes apart**, in the existing session format, naming
  what changed mathematically, what remains, and what can finish in the block.

The coordinator owns identifiers, shared registries, integration, commits and the pull
request.
Before dispatch it allocates one `session-NNN` per lane serially — the next free
number is `session-100` on this branch, `session-098` is owned by PR 110 and
`session-099` by main — and hands each lane its exact path.
Experiment ids are allocated the same way when a lane freezes a claim; the next free is
`exp-130`.

Model and thinking tiers follow
[OR-2](../../../operating-rules.md#or-2-run-three-to-five-sub-agents-at-a-model-and-thinking-level-matched-to-the-task):
Fable at extra or max for every lane that carries a proof obligation, Opus at high or
max for instrument extensions, replays and record work.
Hosted CI runs beside the lanes, never ahead of them
([OR-3](../../../operating-rules.md#or-3-never-wait-on-a-gate-with-nothing-else-in-flight-run-ci-beside-the-research)).

## The First Wave

Nine lanes are ready and mutually independent: BC-292 through BC-299 and BC-302. They
group into six parallel groups so that lanes sharing an instrument can be scheduled on
one machine without contention:

| Group | Lanes | Shared instrument |
| --- | --- | --- |
| `lanes-corners` | BC-292, BC-293 | column generation and the exact sweep |
| `lanes-duality` | BC-294 | the cutting-plane loop and `ceiling.py` |
| `lanes-angles` | BC-295, BC-296 | `classcert` and the class program |
| `lanes-ladder` | BC-297 | column generation at 191/50 |
| `lanes-walls` | BC-298 | the rectangle centre domain |
| `lanes-anchors` | BC-299 | H-106’s guards and the event-cell filter |
| `lanes-ownership` | BC-302 | the escape instrument and `sqpack.cover` |
| `lanes-witnesses` | BC-300 (tentative) | float search and exact verification |

Priority within the wave: the three lanes that *decide* which routes survive come first
— BC-294 (the duality kill tests and the `B = 1` value), BC-295 (where the fractional
obstruction lives in angle), BC-293 (whether the four-corner theorem is free).
BC-301 starts as soon as BC-294 has its first `B = 1` reading.

If only three lanes can run, take BC-294, BC-293 and BC-295: they decide, respectively,
whether any one-body certificate can reach the endpoint, whether the corner anchors are
free at `q`, and whether the obstruction at `q` is Trump-shaped.

## What Would Count as Progress

The narrow tier succeeds when one lane produces either a certificate at `q` conditioned
on a proved constraint with its complement listed, or a proved structural theorem below
`U` that is new (the four-corner containment theorem, a rectangle bound, a band theorem
with `α + β ≥ 3°`). The ambitious tier is decided negatively by BC-294 alone if a
`B = 1` fractional packing of value at least eleven exists below `U` with a unit of
weight away from Trump’s placements, and positively only through BC-302 or an
integer-hull cut family that BC-292 and BC-294 would reveal.

A promising result does not extend a lane’s clock.
A lane that ends early because of tokens or an external limit publishes the same fields
at its current scope.

## Copyable Coordinator Handoff

> Start Agenda 030’s lanes only under the owner’s research-start instruction.
> Read X-021 and this agenda; check the current branch, the stacked pull requests and
> live beads. Allocate `session-NNN` and, when a lane freezes a claim, `exp-NNN`
> serially, after rechecking main and every open pull request, including PR 120.
> Dispatch the ready lanes with the lane brief below, each with its exact result path
> and its hypothesis. Fable at extra or max for proof obligations; Opus for instrument
> work. Push at the first commit worth a hosted run and read CI from its receipts at the
> next block boundary.
> At the end of the first wave, run BC-303 with independent review before selecting;
> BC-304 closes.

## Copyable Lane Brief

> Pursue your Agenda 030 lane within its budget.
> Begin from X-021’s proved facts and your lane’s retained report under
> `results/agenda-030/`. State the exact implication you are testing and the complete
> domain to which it would apply.
> Record your site set and every input with every result.
> Seek a proof, an independently checkable counterexample, or an exact-decided
> certificate; a float optimum is never a result.
> Retain legal touching, all angle and anchor parameters, and every complementary case.
> Write only to your lane’s result document and the instrument files your cell’s note
> names. At each checkpoint report what changed mathematically, what remains, and what
> can finish within the block.
> Do not allocate ids, extend your clock, mutate shared records, or begin another lane’s
> target.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
