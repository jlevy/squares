---
title: agenda-002 — constructive enumeration groundwork
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-002
  title: Build the constructive proposer on foundations that can carry its results
  updated: '2026-08-26'
  status: active
  objective: >-
    Sequence the stratified chunk-enumeration program from X-003 so that each cell buys
    either coverage knowledge, a reusable instrument, or a measurement, and so that the
    foundational gaps a constructive proposer would otherwise inherit - degenerate-cell
    reproducibility, work-unit accounting, and the proposer comparison interface - are
    closed before they can silently invalidate a result rather than after.
  items:
  - id: BC-016
    purpose: measurement_validation
    owner_focus: correctness
    instances: [5, 10, 11, 16]
    state: ready
    priority: 0
    question: >-
      Do aligned and glued chunk strata, which are the most degenerate cells this design
      will ever solve, return the same endpoint and the same active cell across
      toolchains and pool widths?
    hypotheses: []
    budget: one bounded W7 slice; deterministic replay, no search
    entry: >-
      the built cell-read quench, the proved n=5 and n=10 controls, and the exact n=16
      not-below guard
    exit: >-
      A retained differential over declared toolchains showing either stable endpoints
      and active cells on aligned strata, or a typed instability report naming the
      affected rows. An instability finding blocks BC-018 rather than being carried into
      it.
    bead: think-zt29
    depends_on: []
    next_evidence: >-
      retained aligned-stratum differential with per-row active-cell identity, attached
      to the D-059 record
    note: >-
      Foundational, and specific to this design rather than generic hygiene: an
      enumerator spends most of its budget on exactly the symmetric, tie-rich cells
      where D-059 lives. If endpoint identity is toolchain-dependent there, an
      enumeration ranking is not replayable and no coverage claim survives.
  - id: BC-017
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5, 10]
    state: ready
    priority: 1
    question: >-
      Can a stratum be priced in counted LP solves end to end, so enumeration results
      are comparable to each other and to the annealer without reference to wall time?
    hypotheses: []
    budget: one bounded W7 slice
    entry: the quench's existing solve path and the sqsearch pair-test meter
    exit: >-
      Every enumerated stratum carries a retained LP-solve count and pair-test total;
      two runs under different host load produce identical counts.
    bead: think-u97a
    depends_on: []
    next_evidence: identical retained counts across a loaded and unloaded host
    note: >-
      D-126 makes wall-clock budgets load-dependent. A deterministic enumerator can
      satisfy the work-unit rule by construction, which is why this is cheap here and
      expensive everywhere else; doing it now also gives H-045 an admissible budget
      currency before its first round rather than after.
  - id: BC-018
    purpose: tool_validation
    owner_focus: correctness
    instances: [5, 10, 16]
    state: blocked
    priority: 1
    question: >-
      Does the stage-1 enumerator plus glued rows plus sweep driver reproduce the proved
      optima at n=5 and n=10 and return exactly 4 at n=16, from enumeration alone?
    hypotheses: [H-045]
    budget: >-
      one to three bounded W7 slices; priced in LP solves once BC-017 lands
    entry: BC-016 clean or its instability bounded, and BC-017 accounting in place
    exit: >-
      Enumeration ranks the analytic optimum first at n=5 and n=10 within the solver
      floor, returns exactly 4 at n=16, and every stratum carries a replayable label and
      solve count. This is the grammar freeze point for H-045.
    bead: think-sfzh
    depends_on: [BC-016, BC-017]
    next_evidence: >-
      retained per-stratum ranking on the proved cells with the frozen grammar commit
      named in the record
    note: >-
      Grammar design freedom is spent here and nowhere later. A grammar adjusted after
      seeing n=11 makes H-045's criterion vacuous.
  - id: BC-019
    purpose: research
    owner_focus: insight
    instances: [11, 17, 18, 19, 28, 29]
    state: blocked
    priority: 2
    question: >-
      Are standing records at n <= 30 already chunk-structured, and if not, which
      grammar move is missing?
    hypotheses: [H-044]
    budget: tier S; one corpus pass over archived geometry, no search
    entry: >-
      a chunk-decomposition detector over imported Witness/v1 geometry, and the frozen
      public-geometry corpus
    exit: >-
      A per-record decomposition certificate or typed non-expressible reason for every
      corpus member, and the measured expressible fraction against the 0.80 criterion.
    bead: think-im8q
    depends_on: []
    next_evidence: retained per-record decomposition table with minimal K per record
    parallel_group: corpus-measurement
    note: >-
      Independent of the enumerator and runnable in parallel: it reads geometry rather
      than searching. It is the cheapest way to refute the ansatz, so a coordinator with
      spare capacity should start it early even though its priority is below the
      instrument cells.
  - id: BC-023
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 17, 18, 29, 68, 88]
    state: ready
    priority: 1
    question: >-
      Can the standing-record geometry for every n <= 100 with public full coordinates be
      imported into Witness/v1 with retained provenance and a numerical check?
    hypotheses: []
    budget: one to two bounded W7 slices; import and numerical check only, no search
    entry: the archived record catalogue captures and the Witness/v1 interchange
    exit: >-
      A per-case imported witness or a typed absent-or-ambiguous reason for every n <=
      100, each numerically checked at declared precision, with no decimal import
      promoted past numerically-checked; and `tilt_angles_deg` plus the derived angle-
      class count populated in every frontier case artifact the import covers, replacing
      the nulls those artifacts currently carry.
    bead: think-osm7
    depends_on: []
    next_evidence: >-
      per-case import table with retrieval provenance, declared precision, and typed
      failures
    parallel_group: corpus-measurement
    note: >-
      The synopsis records that most public frontier entries carry side values without
      an imported geometry witness. This closes that gap for its own sake and supplies
      the corpus BC-019 and BC-024 both read. Source adapters resolve units and
      coordinate conventions at the interchange boundary rather than guessing.
  - id: BC-024
    purpose: research
    owner_focus: insight
    instances: [11, 17, 18, 19, 26, 28, 29, 37, 40, 50, 68, 70, 83, 88]
    state: blocked
    priority: 2
    question: >-
      Across the imported n <= 100 corpus, which chunk shapes, chunk sizes, tilted-chunk
      counts, and wall seatings actually recur, and what does the non-expressible
      residue have in common?
    hypotheses: [H-044]
    budget: tier S; a descriptive census over imported geometry, no search
    entry: BC-023 corpus available and the chunk-decomposition detector built
    exit: >-
      A taxonomy table over the corpus plus a characterized residue, feeding H-044's
      criterion and naming the grammar moves the enumerator lacks.
    bead: think-kr1d
    depends_on: [BC-023]
    next_evidence: >-
      recurrence table over chunk shape, size, tilted-chunk count, and seating, with the
      residue characterized rather than only counted
    parallel_group: corpus-measurement
    note: >-
      Descriptive rather than adjudicating: this cell reports what the corpus looks like
      and may not emit a W6 verdict. Exploratory chunk-and-quench play belongs here
      under W3, and anything it suggests becomes a registered claim before it is
      measured.
  - id: BC-020
    purpose: research
    owner_focus: insight
    instances: [11]
    state: blocked
    priority: 2
    question: >-
      Does a class-angle path run from Trump's aligned chunk form to the record without
      chunk fission, and how many active cells does it cross?
    hypotheses: [H-046]
    budget: tier S; roughly 4,100 LP solves, seconds of wall time
    entry: the sweep driver with retained per-step cell records
    exit: >-
      A retained sweep with per-step value, active cell, and chunk membership, and a
      verdict on the fission count and the refined minimum.
    bead: think-dh4b
    depends_on: [BC-017]
    next_evidence: retained per-step cell sequence with the cell-change count
    note: >-
      Cheap and decisive about the predecessor intuition. The scientific content is the
      cell-change sequence, not the value curve, which exp-010 already measured.
  - id: BC-025
    purpose: research
    owner_focus: insight
    instances: [5, 10, 11, 17, 18, 28, 29]
    state: blocked
    priority: 2
    question: >-
      Does rounding a pose to its chunk-regular predecessor and re-quenching return the
      pose, for records and for ordinary non-record endpoints alike?
    hypotheses: [H-047]
    budget: tier S; one quench per source pose
    entry: >-
      BC-023 corpus, the chunk-decomposition detector, and the retained series-000
      non-record endpoints
    exit: >-
      Retained source and returned sides per pose with the round-trip rate reported
      separately for record and non-record sources.
    bead: think-kr1d
    depends_on: [BC-023, BC-019]
    next_evidence: >-
      per-pose round-trip table with the record and non-record rates apart
    note: >-
      Decides whether a chunk decomposition is a coordinate system or only a
      description. Non-record sources are in the sweep on purpose: a representation
      fitted to twenty records would not be tested by them.
  - id: BC-026
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5, 10]
    state: blocked
    priority: 3
    question: >-
      Does the cheap glued screen keep the soft-mode winning stratum in its top decile?
    hypotheses: [H-048]
    budget: tier S; two LP solves per stratum on the proved cells
    entry: BC-018 enumerator and glued rows available
    exit: >-
      Per-cell rank of the soft-mode winner within the glued ranking, with retained
      solve counts for the screened and exhaustive paths.
    bead: think-vnm5
    depends_on: [BC-018]
    next_evidence: rank of the soft winner in the glued ranking per proved cell
    note: >-
      An efficiency claim the enumerator's cost model already assumes. Proved cells
      only, so a screen failure cannot be mistaken for a landscape fact.
  - id: BC-021
    purpose: research
    owner_focus: insight
    instances: [11, 16, 17]
    state: blocked
    priority: 3
    question: >-
      Does the frozen grammar rank the standing best first at n=11, hold the n=16 guard,
      and reach Bidwell's record at n=17?
    hypotheses: [H-045]
    budget: tier M at n=11 and n=17, priced in LP solves
    entry: BC-018 complete and the grammar freeze commit published
    exit: >-
      A retained ranking over enumerated strata per cell, with n=17 reported as its own
      cell and never folded into the n=11 verdict.
    bead: think-sfzh
    depends_on: [BC-018, BC-019]
    next_evidence: per-cell stratum ranking with the freeze commit named
    note: >-
      Depends on BC-019 as well as BC-018: a coverage measurement that lands after the
      target run cannot inform what the ranking means.
  - id: BC-022
    purpose: research
    owner_focus: correctness
    instances: [11]
    state: blocked
    priority: 4
    question: >-
      Can per-stratum optimization be made rigorous enough to prove a restricted-class
      statement of the shape "no k-chunk packing beats Trump"?
    hypotheses: []
    budget: not priced; a proof-lane program, not a round
    entry: >-
      an exact LP over certified rational or algebraic cell coefficients, which is
      D-021's named general fix and is unbuilt
    exit: >-
      A scoped restricted-class theorem with a replayable certificate, or a recorded
      determination that the enumeration cannot be made rigorous at this scale.
    bead: think-im8q
    depends_on: [BC-021]
    next_evidence: >-
      a decision on whether the exact LP is buildable for the cell shapes the enumerator
      actually produces
    note: >-
      The endgame that would make this program produce a theorem rather than a record
      candidate. Stromquist's Theorem 3 is the only existing restricted-class theorem at
      n=11, and this is its natural successor shape. Deliberately last: it is blocked on
      unbuilt exact arithmetic and on knowing which cells matter.
---
# agenda-002 — constructive enumeration groundwork

[agenda-001](agenda-001-basin-confidence-ladder.md) orders the **basin-map** lane, whose
head is the exact `n = 5` local geometry under `BC-010`. This agenda orders the
**constructive proposer** lane opened by
[X-003](../explorations/X-003-stratified-chunk-enumeration.md).
The two are independent: nothing here waits on terminal-component identity, and nothing
there waits on an enumerator.
A coordinator may run both, and should not merge their queues.

## Why this order

The synopsis names proposal, not refinement, as the record-finding lane’s live
bottleneck: the refiner takes the proved controls to `1e-15` and leaves the tested
`n = 11` starts at `6e-02`. A constructive enumerator is a proposer, so it inherits
every measurement-system gap the proposer layer already has.
Three of those gaps are load-bearing for *this* design specifically, which is why they
sit ahead of the instrument rather than beside it.

**Degeneracy comes first because the design maximizes exposure to it.**
[D-059](../../defects.md) records that endpoint identity depends on floating-point
behaviour in a degenerate linear program.
Aligned and glued chunk strata are the most symmetric, tie-rich cells this pipeline will
ever solve, so an enumeration ranking is exactly the artifact most likely to fail to
replay. `BC-016` measures that before any ranking is trusted.

**Work-unit accounting comes next because it is nearly free here.**
[D-126](../../defects.md) makes wall-clock budgets load-dependent.
A deterministic enumerator can be priced in counted LP solves by construction, so
`BC-017` closes for this instrument what remains open in general, and gives `H-045` an
admissible budget currency before its first round.

**Coverage runs in parallel because it can refute the ansatz without the instrument.**
`BC-023` imports the record geometry, `BC-019` scores the criterion on it, and `BC-024`
describes what the corpus actually looks like.
None of the three needs a search or an enumerator.
It is the cheapest cell in the agenda and the only one that can end the program early,
so a coordinator with spare capacity should start it as soon as a detector exists.

## What is deliberately not here

Terminal-component identity ([D-034](../../defects.md)) is not a prerequisite for this
lane. A stratum’s identity is its discrete label, so the upper-bound program can produce
a complete, deduplicated atlas over strata while the basin-map lane resolves what a
component is. That independence is the main structural argument for the design and the
reason this agenda exists separately.

Unattended numerical execution is also not here.
The launch agenda’s numerical runner remains **NO-GO**, and nothing in this queue needs
it: every cell is a bounded, deterministic, supervised slice.

## Handoff

`BC-016`, `BC-017`, and `BC-023` are `ready` and independent of each other.
The `corpus-measurement` group (`BC-023`, `BC-019`, `BC-024`) is a disjoint lane another
agent may own concurrently with the instrument cells.
Everything else is blocked in the order above.
The grammar freeze at `BC-018` is the point after which no design change may be made
without invalidating `H-045`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
