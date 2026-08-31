---
title: "agenda-010 — the two-lane overnight run: instruments first, then theorems"
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-010
  title: "The two-lane overnight run: instruments first, then theorems"
  updated: '2026-08-31'
  status: active
  objective: >-
    Nine hours, unattended, done before the owner's morning. The program is X-010's two
    ladders mapped onto blocks: Lane A (proof) builds the general unavoidable-set
    certifier and falsifier, then machine-checks Bentz 2010's m = 4 argument; Lane B
    (structure) reprices the chunk enumeration D-406 left unpriced, measures the
    exact-LP cost gate, and takes the H-044 expressibility verdict. Tools run before
    research in both lanes, the lanes alternate so a gate never idles the run (OR-3),
    and a 30-minute checkpoint between the tool blocks and the research blocks
    resequences the tentative half on the night's actual evidence rather than tonight's
    guesses.

    The wall-clock structure the owner asked for: blocks of two to three hours, each
    run as its own contemporaneous AgentSession taking research loops in 15-30 minute
    slices. Block 1 (150m): BC-093 then BC-094. Block 2 (120m): BC-095 then BC-096.
    Checkpoint (30m): BC-098. Block 3 (120m): BC-099. Block 4 (90m + 30m
    finalization): BC-100, then close every open session with the close tool, refresh
    the PR description and cost block (OR-9), and write the handoff. Committed total
    540 minutes. BC-097 is deliberately unscheduled: it is gate filler, taken only
    while waiting on something else. The tentative blocks BC-101 through BC-105 are
    next-run material and start tonight only if the checkpoint promotes one into time
    that actually exists.

    The 8 a.m. deadline is an owner-imposed wall, not a self-declared budget, so OR-8
    does not apply to it: when a block's budget ends, the block ends at the slice
    boundary with its remainder recorded on the bead. Standard unattended rules hold
    throughout: any candidate mathematical verdict is recorded unresolved with
    needs_review rather than promoted; no verified_* field moves without a reviewed
    evidence-contract change; nothing is pushed without packing-validate --push green
    on the exact tree; the PR opens at the first block boundary and its description and
    cost block refresh at every boundary after (OR-9). A checkpoint may resequence or
    stop lanes; it may not skip validation, promote a verdict, or extend the wall.
    BC-089's remainder on think-d0j1 stays open in agenda-009 and is legitimate gate
    filler alongside BC-097.
  items:
  - id: BC-093
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 13]
    state: complete
    priority: 0
    question: >-
      Can the Stromquist certifier-falsifier pair become one resource-system instrument
      that any published unavoidable-set proof can be encoded against?
    hypotheses: []
    budget: >-
      about 90 minutes, W7, in slices of 30
    entry: >-
      cases/stromquist carries 2,645 lines that certify exactly one figure of one paper:
      repaired_cover.py proves the repaired Figure 14 cover over a bespoke Q(sqrt 5)
      embedding, printed_cover.py exhibits the strict escape from the printed set, and
      both are exact. Every rung of Lane A stands on generalizing them: a declared
      resource system (points, weighted points, segments with length thresholds,
      threshold charges, moving families) over sqpack.field scalars or rational
      intervals, a box family at a declared container side, a replayable cover
      certificate. The controls already exist and are exact (exp-016, exp-017).
    exit: >-
      The exp-016/exp-017 pair replayed through the general instrument -- printed
      refuses, repaired certifies, byte-stable on replay -- with the bespoke module
      reduced to a caller and the field seam resolved: the instrument consumes
      sqpack.field, or the reason it cannot is recorded where the next reader will
      look. A resource kind the Stromquist proof does not exercise may land as a typed
      not-yet-supported refusal rather than untested code.
    bead: think-y2ju
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      Discharged by session-054 phase 1: sqpack/cover.py carries the general core
      (geometry, tiling/mesh/partition validators parameterized by side, box
      predicates, record plumbing, typed resource-kind refusals), both case modules
      are callers (-403 lines), the exp-016/exp-017 replays are byte-stable through
      it, eight tests pin the core on a third scalar, and the FieldElement seam
      (no ordering, no text()) is recorded in the module docstring rather than
      papered over.
    artifacts:
    - src/sqpack/cover.py
    - tests/test_cover.py
    - cases/stromquist/repaired_cover.py
    - cases/stromquist/printed_cover.py
  - id: BC-094
    purpose: tool_validation
    owner_focus: correctness
    instances: [11]
    state: complete
    priority: 0
    question: >-
      Can an escaping-pose search decide "this set is avoidable" mechanically, with the
      known-answer triple as its calibration?
    hypotheses: [H-010]
    budget: >-
      about 60 minutes, W7, in slices of 20
    entry: >-
      The falsifier half of the instrument: search (x, y, theta) for a box avoiding a
      declared resource set. think-yrvm's known-answer triple is already specified --
      it MUST find the escape on Stromquist's 10-point Figure 13 set at s = 2 +
      4/sqrt(5), MUST saturate on the repaired 12-point set, and a refusal must report
      the pose that defeats it. This is the CEGIS inner loop for every synthesis block
      behind it and the audit tool for every published set.
    exit: >-
      The triple passing: found escape, saturation, and typed refusal reporting, each
      replayable. A saturation is never promoted as a proof of unavoidability -- the
      certifier decides that -- and the search's failure to escape is recorded as
      exactly that.
    bead: think-yrvm
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      Discharged by session-054 phase 2: sqpack/falsify.py searches (x, y, theta)
      deterministically and certifies only through exact signs; the known-answer
      triple is green as tests -- the Figure 13 escape found at margin 1.3e-2 in the
      45-degree family, the repaired set saturating at -(L-1) with the not-a-proof
      caveat fixed in code, refusals naming their defeating pose -- and the retained
      Figure 13 escape replays through the generic bridge over Q(sqrt 2 + sqrt 5).
    artifacts:
    - src/sqpack/falsify.py
    - tests/test_falsify.py
  - id: BC-095
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5, 11]
    state: complete
    priority: 0
    question: >-
      What does chunk-level stage-1 enumeration actually cost in counted LP solves,
      once the measured orbit quotient and the realizability prefilter are applied?
    hypotheses: []
    budget: >-
      about 75 minutes, W5, in slices of 25
    entry: >-
      D-406: BC-092 was stopped on "9.3e9 raw orbit work at n = 5", a figure with no
      artifact behind it. What the tree records: 1,533,696 size-five coloring
      candidates collapse to 11,013 orbits (a measured 139x quotient), the local
      realizability prefilter in contact_realization is unpriced, and MAX_SCAFFOLD_SIZE
      = 5 is a typed cap rather than a measured wall. X-003's own caution stands --
      8^C(5,2) ~ 1e9 raw at the chunk level, and it required a finite bound, an orbit
      count, and an omission control before implementation.
    exit: >-
      The price of X-003 stage-1 at the chunk level (k <= 5 assemblies over ~11
      squares) in counted LP solves (D-126), with the quotient and prefilter applied,
      an omission-control design stated, and the cost of lifting the size cap named. A
      go/no-go number for BC-104 -- either direction is the block succeeding.
    bead: think-kp7o
    depends_on: []
    workflows: [pipeline-improvement, efficiency-loop]
    next_evidence: >-
      Discharged by session-051 phase 1: devtools/price_stage1_chunks.py prices the
      space with factor standings labeled -- counted raw 4.357e20 at K <= 6 (orbit
      floor 2.763e18), a K <= 3 slice under X-008's measured wall seatings at
      24,611,472 raw / 2.250e6 orbit floor, prefilter rate 0.457 measured on 300
      size-five scaffolds at 4.8 ms each, the square-to-chunk transfer named ASSUMED.
      Go/no-go: exhaustive stage-1 is out of reach above K <= 3 (~2.1e8
      sweep-inclusive LP solves there, ~73 h; ~3 h realization-only), and Trump's own
      ~five-chunk decomposition sits outside the exhaustive range -- BC-104/BC-105
      are honest only as restricted-class statements at K <= 3, or need canonical
      enumeration with pruning rather than raw generation. Four tests pin the counted
      closed forms as the enumerator's omission control. The 9.3e9 correction is
      D-406's amendment, found and recorded by this block.
    artifacts:
    - devtools/price_stage1_chunks.py
    - tests/test_price_stage1_chunks.py
  - id: BC-096
    purpose: measurement_validation
    owner_focus: efficiency
    instances: [11]
    state: complete
    priority: 1
    question: >-
      What does the exact LP cost at the full n = 11 cell, and does that route or the
      interval route carry per-stratum certification?
    hypotheses: []
    budget: >-
      about 45 minutes, W5, in slices of 15
    entry: >-
      sqpack.exact_lp decides a cell without tolerance (the D-021 fix) and builds its
      own phase-1 feasible vertex, tested at promote scale. The restricted-class peak
      needs it at Trump's full cell, where T-2's float LP solves in 1.28 ms over 55
      pairs; the exact pivot cost there has never been measured.
    exit: >-
      Wall time and pivot count for the exact solve plus certificate check on the exact
      Trump cell, Fraction against FieldElement coefficients, recorded beside the float
      baseline. The number decides BC-105's certification route; no threshold is
      declared in advance and no route is committed tonight.
    bead: think-nu4y
    depends_on: []
    workflows: [efficiency-loop, pipeline-improvement]
    next_evidence: >-
      Discharged by session-051 phase 2, first-hand on this container: assembly 0.41 s
      for the 1,056-row, 23-variable exact cell; phase 1 58.8 s over 42 pivots;
      phase 2 22.1 s over 16 pivots; lands on the published side exactly. Float-seeded
      path ~2.6 s at zero pivots per the retained test. Route decision recorded:
      sweep in float, certify winners exactly -- whole-class exact certification at
      K <= 3 scale is out of reach at ~1.4 s per pivot.
    artifacts:
    - tests/test_promote_exact_phase1.py
    - tests/test_promote_exact_lp.py
  - id: BC-097
    purpose: tool_validation
    owner_focus: process
    instances: [12, 61, 97]
    state: ready
    priority: 3
    question: >-
      Is the queue readable -- the gap ranking on a durable surface, and the 25 stale
      in_progress beads reconciled?
    hypotheses: []
    budget: >-
      about 45 minutes, W5, in slices of 15, taken only as gate filler
    entry: >-
      devtools/gap_ranking.py exists and X-010 carries its table, but the measurement
      has no durable surface (D-405's regression note), and tbd's in_progress list
      carries 25 beads from long-closed sessions, which distorts what the ready queue
      says a session may take (OR-4 takes the next slice from the handoff, and the
      handoff should not point at ghosts).
    exit: >-
      The gap ranking wired to its chosen surface -- a records-tier step, a generated
      table, or a documented on-demand tool, decided and done -- and every stale
      in_progress bead closed with a reason, returned to open, or re-owned
      (think-a1g2). Explicitly unscheduled: this block is taken in fragments while
      something else gates, never as its own sitting.
    bead: think-6z95
    depends_on: []
    workflows: [pipeline-improvement, process-review]
    next_evidence: >-
      Not started. Gate filler alongside BC-089's remainder; if the night never
      gates long enough, it rolls forward undone and that is fine.
  - id: BC-098
    purpose: research
    owner_focus: insight
    instances: [12, 13, 61]
    state: complete
    priority: 0
    question: >-
      Given what the instrument and measurement blocks actually produced, which
      tentative blocks run in the remaining hours, and in what order?
    hypotheses: []
    budget: >-
      about 30 minutes, W3
    entry: >-
      The run's steering valve, modeled on BC-088: agendas written before their tools
      exist mis-sequence what comes after, and the fix agenda-009 proved is to make the
      resequencing decision itself a bounded block with an exit. By this point the
      night has real evidence: whether the certifier generalized cleanly, whether the
      falsifier triple passed, what enumeration costs, what the exact LP costs.
    exit: >-
      Agenda-010's tentative blocks each moved to ready, blocked, or stopped with a
      reason from the night's evidence; a dated addendum on X-010 recording what
      changed; the remaining wall clock allocated to named blocks. A checkpoint may
      resequence or stop lanes; it may not skip validation, promote a verdict, or
      extend the nine-hour wall.
    bead: think-cjxk
    depends_on: [BC-093, BC-094, BC-095, BC-096]
    workflows: [process-review, insight-iteration]
    next_evidence: >-
      Discharged by session-052 on four measured facts (instruments green, the K <= 3
      tractability boundary, the ~1.4 s/pivot exact-LP cost, ~3.5 h of recovered
      wall). Decisions: BC-101 promoted into tonight's window behind BC-099; BC-102
      runs tonight only if BC-101 completes with wall remaining, else it is the next
      run's first slice; BC-103's 60-minute sizing slice is authorized as gate filler
      after BC-099; BC-104 rescoped to the class the price says is enumerable
      (K <= 3, measured wall seatings, pruned canonical enumeration) and stays behind
      BC-100's verdict; BC-105 carries the measured route (sweep in float, certify
      winners exactly) and its statement narrows to the K <= 3 class. Remaining wall:
      BC-099 to ~09:00Z, BC-100 to ~10:30Z, BC-101 to ~12:00Z, BC-102's first slice
      if wall remains, finalization from 14:10Z. X-010 carries the dated addendum.
    artifacts:
    - campaign/explorations/X-010-two-lanes-two-ladders.md
    - campaign/agent-sessions/session-052-midrun-checkpoint.md
  - id: BC-099
    purpose: research
    owner_focus: correctness
    instances: [13]
    state: ready
    priority: 0
    question: >-
      Does Bentz 2010's m = 4 argument certify mechanically, or where exactly does it
      escape?
    hypotheses: []
    budget: >-
      about 120 minutes, W6, in slices of 30
    entry: >-
      Section 3 of bentz-2010-optimal-packings-13-and-46.md (~126 transcript lines, two
      subsections: non-adjacent and adjacent corner-restricted boxes) is the smallest
      published proof on the m^2 - 3 line, and no unavoidable-set proof in this
      literature has ever been machine-checked. The audit record says checking pays:
      one exact gap found in Stromquist (T-4), four defects recorded in El Moumni's
      route to s(7). Encode the resources and forcing steps in BC-093's instrument;
      every failed step gets BC-094's falsifier before any repair is invented.
    exit: >-
      A replayable certificate for the m = 4 argument, or a typed gap report carrying
      the escaping pose and the failed step -- either is a result. Any repair is
      preregistered and source-distinct per the H-041 pattern, and nothing is promoted
      tonight: a candidate verdict lands unresolved with needs_review.
    bead: think-1o1f
    depends_on: [BC-093, BC-094]
    workflows: [research-loop]
    next_evidence: >-
      Session-053 resequenced the block inside its own question and delivered the
      calibration half: Theorem 8 (s(46) = 7) is machine-certified as printed --
      cases/bentz46, 92 exact cells over Q(sqrt 2, sqrt 3), the Lemma 5 threshold by
      a rational interval subdivision bound of 0.955390, 45 of 45 points charged,
      five tests pinning certificate and refusals -- held unresolved with
      needs_review per the unattended rules. The m = 4 half is typed on think-1o1f
      from the completed extraction: Section 3.1 first, the sliding point Z as the
      one new premise type, tilings reconstructed from prose, the SA (1.74, 1) case
      split flagged as a candidate printed gap, Corollary 7 derived from Lemma 6.
      X-010 Lane A rung 2; the calibration case for H-033's m = 7 encoding and the
      m = 8 attempt behind it. Session-056 then certified the m = 4 foundation
      layer: Figure 2's base configuration (30 exact rational cells, 16/16
      charged) and Lemma 10 settled both ways -- refuted as printed by an exact
      escape certificate against the transposed point (1, 1.74), certified as
      corrected by all three replacement covers, whose Lemma 5 quads sit in
      exactly the parameter families the paper's Section 1 lists. Held
      unresolved with needs_review; Section 3.1's staged sets are the typed
      continuation on think-1o1f.
    artifacts:
    - cases/bentz46/verify_cover.py
    - tests/test_bentz46.py
    - cases/bentz13/verify_cover.py
    - cases/bentz13/lemma10_audit.py
    - cases/bentz13/lemma10_replacements.py
  - id: BC-100
    purpose: research
    owner_focus: insight
    instances: [11, 17, 26, 29]
    state: complete
    priority: 1
    question: >-
      Are the standing records chunk-expressible at K <= 6 with at most two free
      squares -- the H-044 verdict, taken before any enumerator exists?
    hypotheses: [H-044]
    budget: >-
      about 90 minutes, W3, in slices of 30
    entry: >-
      H-044 is refutation-first and search-free: measurable from archived geometry, and
      X-003 registered it first for exactly that reason, but its instrument_ready is
      still false. The delta from chunks.py's conservative component census to the
      registered instrument is bounded: exact-cover minimization over admissible
      bar/L/rectangle subsets within the declared adjacency bands, deterministic
      tie-breaking, typed no-partition, outside-budget, and search-limit refusals,
      replayable decomposition certificates. X-008 already proved the corpus's
      inexpressible residue is entirely axis-aligned, so the grammar's coverage
      question is narrower than it looks.
    exit: >-
      The H-044 criterion evaluated against the frozen corpus with a replayable
      certificate or typed refusal per record, recorded unresolved with needs_review if
      the fraction lands near the 0.80 threshold. A refutation kills the chunk ansatz
      before BC-104 spends anything; a confirmation makes stage-1's grammar
      evidence-based.
    bead: think-l48p
    depends_on: []
    workflows: [research-pass, insight-iteration]
    next_evidence: >-
      Discharged by session-055: the verdict is exp-046, exploratory per H-044's
      own calibration-only amendment, held unresolved with needs_review --
      criterion missed under both denominator readings the registered text
      supports (23/30 = 0.7667 all records at n <= 30; 3/10 = 0.30 over the
      non-grid sweep records), both bands identical, every miss typed and
      determinate under the frozen cap. devtools/score_h044.py carries the
      scoring with per-record re-derivation and byte-identical replay;
      instrument_ready is true; the preregistration-style ambiguities
      (denominator reading, singleton admissibility, contact relaxation) are
      typed in the record for the owner, with the relaxed-universe census re-run
      named as the follow-on.
    artifacts:
    - devtools/score_h044.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-046-h-044-chunk-expressibility-verdict.md
      two lanes can alternate without idling.
  - id: BC-101
    purpose: research
    owner_focus: correctness
    instances: [17, 18]
    state: complete
    priority: 1
    question: >-
      Can certified unavoidable sets beat Nagamochi's closed form at n = 17 and 18,
      where Green's unpublished bounds say the room exists?
    hypotheses: []
    budget: >-
      about 90 minutes, W6, in slices of 30
    entry: >-
      DS7 Table 2's non-trivial lower bounds at ~23 open cases rest on "T. Green, 2000,
      private communication" -- no primary exists, so certifying sets of our own is the
      only route by which the frontier can ever adopt values there (think-s1pc cannot
      be a read). First targets n = 17, 18: Green ~4.4452 against Nagamochi ~4.1623,
      with DS7 Figure 34 sketching the set shape. The verified lower lane has not moved
      at any open n since 2005.
    exit: >-
      Per size: a certified set above the closed form with its replayable certificate,
      recorded unresolved with needs_review, and the frontier move left to a reviewed
      evidence-contract change -- or a typed refusal naming the escaping pose that
      defeated every candidate.
    bead: think-q6vy
    depends_on: [BC-093, BC-094, BC-099]
    workflows: [research-loop]
    next_evidence: >-
      Discharged by session-057: s(17) >= 17/4 = 4.25 and s(18) >= 17/4,
      certified exactly by a sixteen-point unavoidable set (cases/green17) --
      the first verified-lane movement at those sizes since 2005, above
      Nagamochi's 4.1623, held unresolved with needs_review with frontier
      adoption left to a reviewed evidence-contract change. The falsifier
      corroborates by saturation (393,216 poses, best margin -1e-4, not-a-proof
      caveat intact); the side is pinned to exactly 17/4 by an 11/1000000
      slack in the near-slab corner bound. The dependency on BC-099 is
      satisfied by its calibration half (Theorem 8 plus the m = 4 foundation
      layer and Lemma 10 settlement); the m = 4 continuation stays typed on
      think-1o1f.
    artifacts:
    - cases/green17/packing.py
    - cases/green17/verify_cover.py
    - tests/test_green17.py
      it runs is the one BC-099 exercises first. Target window ~10:30Z-12:00Z.
  - id: BC-102
    purpose: research
    owner_focus: insight
    instances: [12]
    state: complete
    priority: 1
    question: >-
      Can synthesis produce the first bespoke certified lower bound at n = 12 -- any
      value strictly above the inherited 2 + 4/sqrt(5)?
    hypotheses: [H-039, H-006, H-034]
    budget: >-
      about 120 minutes, W6, in slices of 30
    entry: >-
      s(12)'s best lower bound is a theorem about n = 11: nothing specific to n = 12
      has ever been proved, so any certified epsilon above 3.7889 is the first result
      about the case, with s(12) = 4 the peak rather than the bar. Shape: eleven
      resources unavoidable at side above 2 + 4/sqrt(5), by counterexample-guided
      synthesis over BC-093's certifier and BC-094's falsifier, H-006's LP duals as the
      candidate generator, H-039's fixed-threshold discipline. First slice: the
      H-034-style tau* diagnostic at n = 12, side 4 - epsilon, which says whether pure
      points can suffice or thresholds and segments are forced -- a result about the
      method either way.
    exit: >-
      A certified bespoke bound recorded unresolved with needs_review, or the tau*
      diagnostic plus a typed account of how far synthesis got and what defeated it.
      H-039's rule holds: the threshold is fixed before synthesis and does not move
      after counterexamples.
    bead: think-0z9b
    depends_on: [BC-093, BC-094, BC-099]
    workflows: [research-loop, insight-iteration]
    next_evidence: >-
      The authorized first slice is discharged by session-059 through the exit's
      diagnostic branch: devtools/pierce_pilot.py carries the uncertified tau*
      pilot, and its ladder puts the eleven-crossing near side 3.83 (10.67 /
      11.00 / 12.53 at 3.80 / 3.83 / 3.86, comparable grids; every number typed
      not-a-bound), with the duality frame pinning the value at eleven or more
      above s(11). Reading: a pure eleven-point set has at most a ~0.04-wide
      window above 2 + 4/sqrt 5, and any ambitious bespoke s(12) bound forces
      the threshold/segment/moving-resource machinery. Synthesis deliberately
      not attempted tonight; the typed account and the certified-instrument gap
      live on think-0z9b for the successor agenda.
    artifacts:
    - devtools/pierce_pilot.py
    - campaign/agent-sessions/session-059-block8-tau-star-pilot.md
      needs exist; the most under-priced target in the corpus keeps its priority.
  - id: BC-103
    purpose: research
    owner_focus: correctness
    instances: [61]
    state: complete
    priority: 2
    question: >-
      Does the m = 7 argument, encoded machine-readably, survive the substitution to
      m = 8 -- and if not, which forcing step is the first to break?
    hypotheses: [H-033]
    budget: >-
      agent-days in total; the first slice is 60 minutes, W6, to size the m = 7
      encoding against BC-099's m = 4 experience
    entry: >-
      s(m^2 - 3) = m is proved for m = 3..7 and conjectured for all m >= 3 in Bentz
      2016; n = 61 is the next member and carries the third-narrowest verified gap in
      the corpus (0.0718). H-033's registered instrument is exactly this: express the
      m = 7 proof as checked moving resources, substitute m = 8, and falsify each
      failed forcing step before inventing a new resource.
    exit: >-
      For the first slice: a sizing statement -- how many lemmas, resources, and
      forcing steps the m = 7 encoding needs, priced against what m = 4 actually cost
      in BC-099 -- and a go/parking decision for the full attempt. The full exit
      belongs to a later agenda.
    bead: think-07t7
    depends_on: [BC-099]
    workflows: [research-loop]
    next_evidence: >-
      The authorized sizing slice is discharged by session-058, inside half its
      budget, with the parking decision taken: the m = 7 pattern's ceiling at
      m = 8 is 7 sqrt(3)/2 + 2 sqrt(2) - 1, exactly below side 8 (18816 < 21025)
      and below the standing 7.928203 at n = 61, with the first breaking premise
      the wall strip's depth cap and the lattice dilemma exact (8 rows overrun
      the pitch cap by 0.0157; 9 rows overrun the point budget by 7). The full
      attempt stays a later agenda's, typed on think-07t7 (paused), with the
      candidate new resources named.
    artifacts:
    - campaign/agent-sessions/session-058-block7-m8-sizing.md
      listed so the ladder's direction is on the map rather than in prose.
  - id: BC-104
    purpose: research
    owner_focus: insight
    instances: [5, 10, 11]
    state: tentative
    priority: 2
    question: >-
      Does the stage-1 pipeline -- enumerator, glued rows, class-angle sweep --
      reproduce the proved controls within the class the price says is enumerable:
      K <= 3 chunks under the measured wall seatings, by pruned canonical enumeration?
    hypotheses: [H-045, H-046, H-047, H-048]
    budget: >-
      about 150 minutes, W7 then W6, in slices of 30
    entry: >-
      X-003's pipeline with only stage 1 unbuilt, rescoped by BC-095's measured
      boundary: exhaustive treatment is honest only at K <= 3 under X-008's measured
      wall seatings (2.250e6 orbit floor; ~3 h realization-only, ~73 h with the
      universal sweep), Trump's own ~five-chunk decomposition is outside the
      exhaustive range, and anything larger needs pruned canonical enumeration rather
      than raw generation. The enumerator ships the counted closed forms of
      devtools/price_stage1_chunks.py as its omission control, with Trump's stratum
      as the known-answer inclusion at the K where it exists. Gated on BC-100's
      verdict.
    exit: >-
      The n = 5 and n = 10 controls reproduced through the full pipeline with glued and
      soft optima agreeing at the analytic values, work priced in counted LP solves,
      and the four registered hypotheses moved from instrument_ready false to runnable
      -- or a typed statement of which stage refused and why.
    bead: think-sfzh
    depends_on: [BC-095, BC-100]
    workflows: [pipeline-improvement, research-loop]
    next_evidence: >-
      Not started. X-010 Lane B rungs 2-4; reopens BC-092's question properly if
      BC-095's number says go.
  - id: BC-105
    purpose: research
    owner_focus: correctness
    instances: [11]
    state: tentative
    priority: 3
    question: >-
      Can a restricted-class optimality statement at n = 11 -- no packing of at most K
      chunks with at most two tilt classes beats Trump's side -- be certified per
      stratum?
    hypotheses: []
    budget: >-
      beyond this run; named so the map carries the peak the lane climbs toward
    entry: >-
      The Stromquist-Theorem-3-shaped statement X-003 names, and the first theorem of
      that shape since 1984 if it lands: exact or interval LP per stratum, a coverage
      certificate over the symmetry quotient, an omission control on the label
      generator. The stratum atlas is also the proposer corpus BC-090's gated search
      instrument needs, so the lane feeds the search block without betting on it.
    exit: >-
      The certified statement with its coverage certificate, recorded unresolved with
      needs_review and left to a reviewed promotion -- or the typed account of the
      stratum class that resisted certification and at what cost.
    bead: think-dbtx
    depends_on: [BC-096, BC-104]
    workflows: [research-loop]
    next_evidence: >-
      Route decided by BC-096's measurement (session-051): sweep in float, certify
      winners exactly at ~2.6 s float-seeded per stratum; whole-class exact
      certification is out of reach at ~1.4 s per pivot. The statement narrows with
      BC-104's rescope: a restricted-class result at K <= 3 under the measured wall
      seatings, or nothing tonight-adjacent.
---
# Agenda-010 — The Two-Lane Overnight Run

Instruments first, then theorems, and a checkpoint in between.

Blocks 1 and 2 build and measure: the general unavoidable-set certifier and falsifier
(`BC-093`, `BC-094`) in Lane A, the enumeration reprice and the exact-LP gate (`BC-095`,
`BC-096`) in Lane B. `BC-098` then spends thirty minutes resequencing the tentative half
on the night’s actual evidence — the same move `BC-088` proved, made into a standing
part of the process.
The committed research blocks close the night: the first machine-check of a published
unavoidable-set proof (`BC-099`) and the H-044 expressibility verdict (`BC-100`), one
per lane.

`X-010` carries the argument for the two lanes; the beads labeled `x-010` carry the work
items; this agenda carries the sequencing, the budgets, and the unattended rules.
`BC-097` and `BC-089`’s remainder are the sanctioned gate filler.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
