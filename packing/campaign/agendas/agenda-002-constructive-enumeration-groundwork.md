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
  updated: '2026-08-27'
  status: active
  objective: >-
    Sequence the stratified chunk-enumeration program from X-003 so that each cell buys
    either coverage knowledge, a reusable instrument, or a measurement, and so that the
    foundational gaps a constructive proposer would otherwise inherit - degenerate-cell
    reproducibility, work-unit accounting, source/annotation separation, deterministic
    minimal partitioning, and the proposer comparison interface - are closed before they
    can silently invalidate a result rather than after.
  items:
  - id: BC-016
    purpose: measurement_validation
    owner_focus: correctness
    instances: [5, 10, 16]
    state: blocked
    blocked_on: >-
      Retained input poses and symbolic active-cell rows for `n005-seed007-known-answer`,
      `n010-seed014-known-answer` and `n016-grid-not-below`, at pool widths one and ten.
      No commitment in any agenda produces them, so this waits on an artifact rather than
      on a predecessor, and nothing but this sentence can say when it clears.
    priority: 0
    question: >-
      Do aligned and glued chunk strata, which are the most degenerate cells this design
      will ever solve, return the same endpoint and the same active cell across
      toolchains and pool widths?
    hypotheses: []
    budget: one bounded W7 slice; deterministic replay, no search
    entry: >-
      retained input poses and symbolic active-cell rows for
      `n005-seed007-known-answer`, `n010-seed014-known-answer`, and
      `n016-grid-not-below`; pool widths one and ten; and peer routes
      `.github/workflows/packing-validation.yml#validate` on `ubuntu-latest` and
      `.github/workflows/packing-validation.yml#macos-portability` on `macos-latest`,
      both using Python 3.14.7 and the frozen packing lock. Each receipt
      must retain the actual runner, architecture, Python, NumPy, SciPy, and HiGHS
      fingerprint rather than treating a moving runner label as the environment.
    exit: >-
      A complete `DegenerateCellDifferential/v1` receipt over every route, pool width,
      and frozen row. The checker independently recomputes settled status, the n=5/n=10
      proved-value or n=16 not-below guard, endpoint agreement at `LP_FEASIBLE_EPS`, and
      canonical symbolic active-cell equality including every tied owner/axis choice.
      A missing matrix row or first mismatch is a typed instability that blocks BC-018.
    bead: think-3yv8
    depends_on: []
    next_evidence: >-
      retain the three named input poses and an executable glued row, implement the
      symbolic tied-axis label, independent receipt checker, and focused synthetic
      mutations locally; then emit and compare the two workflow-route receipts
    note: >-
      Foundational, and specific to this design rather than generic hygiene: an
      enumerator spends most of its budget on exactly the symmetric, tie-rich cells
      where D-059 lives. If endpoint identity is toolchain-dependent there, an
      enumeration ranking is not replayable and no coverage claim survives. A bounded
      2026-08-27 entry audit found that pool widths one and ten were declared but no peer
      toolchain matrix was frozen, so it stopped without execution. The immediate W3
      repair selected the existing Linux and macOS workflow routes and froze the runtime
      receipt, intended target-free row ids, comparison floor, and symbolic tied-axis
      contract. A deeper inventory then found that the golden rows drop their poses,
      n=16 has only a value guard, terminal tie provenance is not retained, and glued
      rows are not executable. BC-016 therefore stays blocked on those local instrument
      inputs. Production `highs-ipm` remains only a status-4 fallback, not a peer arm.
      This narrow control does not settle D-059's broader stochastic golden surface.
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
    budget: two bounded W7 slices followed by one independent W2 audit
    entry: >-
      the completed source-free n=3 full-cell control, quench solver-attempt receipts,
      and the sqsearch pair-test meter as separate accounting references; no complete
      numerical full-cell semantics are yet frozen
    exit: >-
      Every enumerated stratum carries a retained LP-solve count and pair-test total;
      two runs under different host load produce identical counts.
    bead: think-u97a
    depends_on: []
    next_evidence: >-
      First retain a target-free tagged execution-plan receipt on the source-free n=3
      control, with every wall and pair role visible and semantic-swap, forged-count,
      and exact-replay controls. Then freeze the missing numerical semantics before any
      real LP run. BC-017 completes only after real n=5 and n=10 executions retain
      identical derived work and outcomes across declared pool widths and loaded and
      unloaded host conditions.

      The first sentence of this is already discharged and was before the slice started:
      the source-free n = 3 full-cell control retains a target-free tagged execution plan
      with every wall and pair role visible, and its execution-plan-forged-count,
      execution-plan-omitted-row, execution-plan-replay and execution-plan-role-swap
      controls all pass. Its own promotion_boundary says passing authorizes exactly a
      BC-016 or BC-017 readiness decision, so what this slice owed was that decision's
      input, not another receipt.

      Measured on the same three-square subject: the structural plan reports 4 seated-wall
      equalities and 8 open-wall inequalities against 2 contact equalities and 1 non-edge
      inequality; solve_cell builds 12 containment rows and 3 pair rows. The same twelve
      and the same three. The two instruments agree on every total and disagree on every
      composition.

      That is a narrower obstruction than the note reads and a better one. Exactly one unit
      survives all three vocabularies -- the LP solve attempt -- and it is the unit this
      commitment's own exit names, so the LP-solve half of the exit is reachable now. What
      does not transfer is pair_tests, which appears in two instruments and counts compiled
      rows in one and dynamic overlap tests in the other. The exit's pair-test total is not
      one number until which sense is meant is decided, and that decision is a judgement
      rather than a measurement.

      What remains for this commitment is unchanged in shape: freeze the numerical
      semantics, then real n = 5 and n = 10 counted executions agreeing across pool width
      and host load. Nothing here prices an enumerated stratum, and the audit carries no
      coordinates, side, geometry, feasibility or optimality claim.
    note: >-
      D-126 makes wall-clock budgets load-dependent, but the target-free control exposes
      an earlier instrumentation boundary. `solve_cell` counts actual retries while
      collapsing seated-wall and contact/nonedge roles; `contact_realization` refuses
      walls and omits nonedge separation; and sqsearch pair tests are dynamic overlap
      tests, not compiled rows. The first slice therefore retains only a tagged
      structural plan and derived accounting, with real LP attempts and sqsearch pair
      tests both zero. This calibration-only tool evidence carries no coordinates, side,
      geometry, feasibility, optimality, or n=11 target claim. BC-017 remains open until
      the numerical semantics freeze and real n=5/n=10 counted executions agree across
      pool width and host load. BC-018 separately still needs BC-016 plus the n=5, n=10,
      and n=16 grammar controls. `think-u97a` separately requires stable n=4/n=10 quench
      outcomes and work across pool widths and load.
    artifacts:
    - devtools/audit_work_accounting.py
    - campaign/series/series-000-smoke-and-calibration/results/bc-017-work-accounting.json
    - tests/test_work_accounting.py
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
    state: complete
    priority: 2
    question: >-
      Are standing records at n <= 30 already chunk-structured, and if not, which
      grammar move is missing?
    hypotheses: [H-044]
    budget: tier S; one corpus pass over archived geometry, no search
    entry: >-
      the imported Witness/v2 geometry and the bounded lattice-partition calibration;
      extend the candidate universe to contact graphs before any adjudicating round
    exit: >-
      A versioned contact-assembly contract with explicit sliding degrees of freedom,
      complexity cost, canonical ties, and per-record certificates or typed limitations.
      The inspected n=1..100 corpus receives no H-044 verdict.
    bead: think-6mcd
    depends_on: []
    next_evidence: >-
      independent review of CG-010's structural full-cell control and a BC-016 or BC-017
      readiness decision; numerical row compilation remains unbuilt

      Answered, and the last clause of the exit is the part that was missing. The contract
      already carried sliding degrees of freedom, a complexity cost and canonicalization;
      it had never carried per-record certificates. It does now, at version
      contact-assembly-v2-draft: 17 of the 30 records at n <= 30 have every component
      expressible as a rigid-lattice primitive and carry the complexity tuple, and 13 carry
      a typed limitation naming exactly which components fail and what X-008 measured about
      them.

      The missing grammar move is named rather than guessed: a primitive for axis-aligned
      polyominoes that are not a bar, rectangle or corner L. X-008 is what makes that
      statement safe -- every unexpressed component in the whole corpus is untilted, so the
      gap is not about tilted assemblies.

      Two contract fields the retained corpus cannot fill are listed rather than inferred.
      The census stores internal edges as square pairs with a residual and records no normal
      axis or sign, and a normal reconstructed from lattice deltas would be an assumption
      about the fit presented as a measurement. The full-cell square-by-wall inventory
      belongs to the full-cell control, not here.

      internal_slide_dof is zero throughout by the rigid-lattice primitive's own semantics
      and not by evaluating D = 2m - rank(A_normal) - 2, which prices a contact scaffold.
      The detector finds no contact scaffolds in this corpus, so reporting a rank would be
      pricing a primitive that is not there. That was the block's declared kill condition
      and it did not fire, because the contract answers the question itself.

      No H-044 verdict is emitted. A record without a certificate is one the current
      detector did not express, which the census's known_gap says is not a refutation.

      Recorded in atlas/known-best/contact-assembly-grammar.yaml,
      devtools/certify_assembly_coverage.py, tests/test_assembly_coverage.py, and
      campaign/series/series-000-smoke-and-calibration/results/bc-019-assembly-coverage.json.
    parallel_group: corpus-measurement
    note: >-
      Independent of the enumerator: it reads geometry rather than searching. The first
      bounded splitter certifies all grids and 3 of 36 non-grid cases inside the narrow
      budget; two cases are conclusively outside, 23 have no registered-universe
      partition, and eight are search-capped and therefore indeterminate. Broad contacts
      cover 1,780 of 1,860 non-grid squares. The versioned grammar, local uniform-angle
      prefilter, and 11,013-record abstract size-five atlas now represent and price
      sliding contact scaffolds without claiming geometry or feasibility. CG-010 now
      retains one literal target-free structural label, joint orbit, derived price, and
      typed mutations; numerical realization remains unbuilt. The 1-100 corpus was
      inspected during instrument repair and is calibration-only.
    artifacts:
    - atlas/known-best/contact-assembly-grammar.yaml
    - atlas/known-best/contact-assembly-grammar.schema.yaml
    - devtools/certify_assembly_coverage.py
    - campaign/series/series-000-smoke-and-calibration/results/bc-019-assembly-coverage.json
    - tests/test_assembly_coverage.py
  - id: BC-023
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 17, 18, 29, 68, 88]
    state: complete
    priority: 1
    question: >-
      Can the standing-record geometry for every n <= 100 with public full coordinates be
      imported into Witness/v2 with retained provenance and a numerical check?
    hypotheses: []
    budget: one to two bounded W7 slices; import and numerical check only, no search
    entry: the archived record catalogue captures and the Witness/v2 interchange
    exit: >-
      A per-case imported witness or a typed absent-or-ambiguous reason for every n <=
      100, each checked at declared precision, with no decimal import promoted past
      numerically-checked; source geometry, normalized witnesses, derived annotations,
      and house renderings remain separate layers.
    bead: think-osm7
    depends_on: []
    next_evidence: >-
      complete manifest with retrieval provenance, declared precision, retained-source
      policy, witness paths, and rendering paths
    artifacts:
    - atlas/known-best/manifest.json
    - witnesses/known-best/n-001.yaml
    - atlas/known-best/rendering/n-001.svg
    parallel_group: corpus-measurement
    note: >-
      The synopsis records that most public frontier entries carry side values without
      an imported geometry witness. The completed atlas has 100 witnesses and 100 house
      renderings: 64 exact grids, 34 attributed Kingbird-derived numerical fact records,
      and two explicitly rendering-derived UnitSquare cases. No raw Kingbird SVG is
      retained in this source inventory because the review located no express
      redistribution terms; this is a conservative retention policy, not a legal
      conclusion. Source adapters resolve units and coordinate conventions at the
      interchange boundary rather than guessing.
  - id: BC-024
    purpose: research
    owner_focus: insight
    instances: [11, 17, 18, 19, 26, 28, 29, 37, 40, 50, 68, 70, 83, 88]
    state: complete
    priority: 2
    question: >-
      Across the imported n <= 100 corpus, which chunk shapes, chunk sizes, tilted-chunk
      counts, and wall seatings actually recur, and what does the non-expressible
      residue have in common?
    hypotheses: [H-044]
    budget: tier S; a descriptive census over imported geometry, no search
    entry: BC-023 corpus available; descriptive contact detector built
    exit: >-
      A source-stratified taxonomy table over the corpus plus a characterized residue,
      feeding the partition-instrument design without emitting an H-044 verdict.
    bead: think-kr1d
    depends_on: [BC-023]
    next_evidence: >-
      extend the retained broad contact-component census with minimal-partition shapes,

      Answered descriptively and the answer inverts the expected shape of the residue.
      Stratified by the source each record's geometry came from, the corpus is three
      populations: exact-grid (64 records, 64 components, none tilted), kingbird-derived
      facts (34 records, 387 components, 237 tilted), and unitsquare-rendering (2 records,
      137 components, every one a singleton and 58 of them tilted).

      Every other-polyomino in the corpus has angle exactly zero -- one distinct value
      across all 109 -- so every tilted component the repository holds is a singleton, bar,
      L or rectangle, all of which the grammar expresses. Extending the grammar to reach the
      residue is a question about axis-aligned polyominoes, not about tilted assemblies.

      Wall seating, computed from witness corners because lattice coordinates are relative
      to a component, splits the residue into exactly two populations with nothing between:
      44 whole-record grid subsets touching all four walls, and 65 corner-seated blocks
      touching exactly two. None touches one, three or none. The seating agrees with n = 5's
      exactly known contacts from X-007, which is what stops it from measuring the decimal
      witnesses' precision instead of the packings.

      No H-044 verdict is emitted and none is available: the census's known_gap says an
      unexpressed component is not a refutation until the minimal-partition solver exists,
      and the record carries that sentence with a test asserting it is there.

      Recorded in campaign/explorations/X-008-the-residue-is-axis-aligned.md,
      devtools/census_chunk_taxonomy.py, tests/test_chunk_taxonomy.py, and
      campaign/series/series-000-smoke-and-calibration/results/bc-024-chunk-taxonomy.json.
      wall seating, and representative house-rendered overlays
    parallel_group: corpus-measurement
    note: >-
      Descriptive rather than adjudicating: the first contact census finds 1,780 of 1,860
      non-grid squares in same-angle positive-edge-contact assemblies, with 25 of 36
      cases inside a broad six-component/three-free budget. The strict bounded lattice
      splitter certifies 3 of 36 non-grid records inside its budget, places two outside,
      finds no registered-universe partition for 23, and leaves eight search-capped and
      indeterminate. Contact-graph complexity, wall seating, and overlays are retained
      as descriptive calibration. Exploratory work may not emit a W6 verdict.
    artifacts:
    - devtools/census_chunk_taxonomy.py
    - campaign/series/series-000-smoke-and-calibration/results/bc-024-chunk-taxonomy.json
    - tests/test_chunk_taxonomy.py
    - campaign/explorations/X-008-the-residue-is-axis-aligned.md
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
    blocked_on: >-
      Two things, neither an edge. First, the instrument does not exist: `H-047` carries
      `instrument_ready: false`, and of the three pieces it names, the class-bracketing
      quench and the D4-and-relabeling matcher are built while the regularizer that snaps
      intra-chunk contacts to exact and chunk angles to their fitted class value is not
      written. `chunks.py` computes the class values such a snapper would target; nothing
      snaps.

      Second, the declared inputs do not exist for most of the sweep. The entry asks for
      retained series-000 non-record endpoints across `[5, 10, 11, 17, 18, 28, 29]`, and a
      pose is retained for `n = 5` and `n = 10` only -- the quench-family results keep
      scalars and drop the pose, so `n = 11, 17, 18, 28` and `29` have none at all.
      Recovering them is a re-run with pose retention rather than a reformatting, which is
      `BC-016`'s note recurring on a different corpus.

      Both predecessors are complete, so the map reported this cell as takeable while
      neither of these was written anywhere a reader could see. That is `D-401`.
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
      Retained source and returned poses with objective and D4-and-relabeling
      pose-equivalence rates reported separately for record and non-record sources.
    bead: think-r45s
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
      Does the cheap glued screen retain the soft-mode winning stratum at its declared
      solve budget after boundary ties are charged?
    hypotheses: [H-048]
    budget: tier S; two LP solves per stratum on the proved cells
    entry: BC-018 enumerator and glued rows available
    exit: >-
      Per-cell recall of the soft-mode winner at B=max(1,ceil(0.1N)), with boundary ties,
      actual retention count, and solve counts for screened and exhaustive paths.
    bead: think-coyu
    depends_on: [BC-018]
    next_evidence: recall and actual cost of the glued budget per proved cell
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
    bead: think-cx85
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
[D-059](../../../defects.md) records that endpoint identity depends on floating-point
behaviour in a degenerate linear program.
Aligned and glued chunk strata are the most symmetric, tie-rich cells this pipeline will
ever solve, so an enumeration ranking is exactly the artifact most likely to fail to
replay. `BC-016` measures that before any ranking is trusted.

**Work-unit accounting comes next because it is nearly free here.**
[D-126](../../../defects.md) makes wall-clock budgets load-dependent.
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

Terminal-component identity ([D-034](../../../defects.md)) is not a prerequisite for
this lane. A stratum’s identity is its discrete label, so the upper-bound program can
produce a complete, deduplicated atlas over strata while the basin-map lane resolves
what a component is.
That independence is the main structural argument for the design and the reason this
agenda exists separately.

Unattended numerical execution is also not here.
The launch agenda’s numerical runner remains **NO-GO**, and nothing in this queue needs
it: every cell is a bounded, deterministic, supervised slice.

## Handoff

`BC-016` is blocked; `BC-017`, `BC-019`, and `BC-024` are ready; and `BC-023` is
complete.
The remaining `corpus-measurement` cells (`BC-019` and `BC-024`) are a disjoint
lane another agent may own concurrently with the instrument cells.
Everything else is blocked in the order above.
The grammar freeze at `BC-018` is the point after which no design change may be made
without invalidating `H-045`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
