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
  status: completed
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
    outcomes:
    - scope: The parallel-lane research plan and its proved structural starting facts
      classification: achieved
      result: >-
        X-021, H-127 through H-134 and the disjoint Agenda 030 lane plan were published
        without opening a scientific target in the planning block. Later sessions ran
        under this contract and retain their own measurements and stop reasons.
      evidence:
      - packing/campaign/explorations/X-021-what-can-be-proved-about-eleven-squares.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/README.md
      disposition: retire-success
      follow_up: null
    next_evidence: The owner's research-start instruction; then the coordinator allocates session ids and dispatches the ready lanes below.
  - id: BC-292
    purpose: research
    owner_focus: insight
    instances: [11]
    state: stopped
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
    outcomes:
    - scope: The corner-class LP under the corner-pair condition on one site set, in session-109 (2026-09-08), halted by an external usage limit during run 4
      classification: time-limited
      result: >-
        The corner class does buy a surplus at 96/25 and the surplus is exactly bounded and
        far too small: on site set A the class lowers the ratio optimum by between 0.000535
        and 0.000573, which is 1.6 to 1.8 per cent of the 0.0325 gap to the certificate
        line, with the flush-four dual at lambda = 1.0325 and the free control at 1.0330,
        both exactly decided. On site set A, run 3's exact dual proves the ratio optimum
        is 1. Mark banking supplies an upper bound of 1 on other site sets, not equality.
        The ratio and slice normalizations have the same exclusion power; slice form
        may resolve a positive gap more clearly numerically. The reported opposite-both
        slice did not improve on the free program on its tested support.
        Run 4 did not converge and run 5, on the corner-refined site set, did not run.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-a-corner-structure.md
      - packing/campaign/agent-sessions/session-109-corner-class-at-q.md
      disposition: continue
      follow_up: think-kx2l
    next_evidence: Whether any corner information has value for a certificate at q; if the flush-four residual falls below seven, the first conditional exclusion with a named complement.
    note: Owns the region-class row generator and the centre-domain clip; no other lane edits those files.
  - id: BC-293
    purpose: research
    owner_focus: insight
    instances: [11]
    state: complete
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
    - packing/campaign/agent-sessions/session-101-corner-skeleton-ownership.md
    outcomes:
    - scope: The bounded corner-skeleton measure at 96/25 on the retained shrink and net, one site set, in session-101 (2026-09-08, one worker at load 3 to 8)
      classification: bounded-negative
      result: >-
        The tested finite support is unsuccessful: with the corner orbit bounded below by 3/20 the exactly
        swept measure has mass 23596423/2000000 = 11.798 (five-bound 11.819) against the free
        11.262 on the same site set, price M(forced) - M(free) = 33507/62500 = 0.536, and
        pricing the corner orbit leaves it at weight zero, so the corner atom's position, not
        the bound, is the obstacle; the bounded dual's proved floor for every valid D4 measure
        on this net is 10.785, below 11.15, so the obstruction is a site-set reading rather
        than a theorem for the net. The Lemma C dry run on T-018 keeps no diagonal displacement
        valid. This retires only the tested support, not H-128's continuum-support question.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-c-n10-transfer.md
      - packing/campaign/agent-sessions/session-101-corner-skeleton-ownership.md
      disposition: retire-negative
      follow_up: null
    - scope: The corner-pair containment theorem derived from the verified free measure
      classification: achieved
      result: >-
        From the exactly verified free measure and the ownership lemma applied to T-018's
        corner pair, every packing of eleven unit squares at 96/25 has four distinct
        squares, each containing one of its corner's two marks in its interior. The anchor
        for later work is therefore a corner pair, not a corner point.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-c-n10-transfer.md
      - packing/campaign/agent-sessions/session-101-corner-skeleton-ownership.md
      disposition: retire-success
      follow_up: null
    - scope: H-128 over unrestricted D4-symmetric measure support at 96/25
      classification: inconclusive
      result: >-
        The unsuccessful finite support and its bounded dual do not decide whether a
        qualifying measure exists on the full declared continuum support. That scientific
        question remains separate from the proved corner-pair theorem.
      evidence:
      - docs/project/reviews/review-2026-09-08-pr127-research-readiness.md
      - packing/campaign/hypotheses/H-128-corner-skeleton-ownership.md
      disposition: continue
      follow_up: think-1136
    next_evidence: Pinned anchors for the frame-conditioned certificate (BC-287, H-111) and the two-pattern case split of the ownership-conditioned certificate.
  - id: BC-294
    purpose: measurement_validation
    owner_focus: correctness
    instances: [11]
    state: stopped
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
      Per region an exact feasible family of value at least 10 can obstruct the specified
      one-body certificate; a smaller feasible family is inconclusive. An upper bound
      requires a covering certificate over the declared region. For B = 1, an exact
      depth-one family of value at least 11 at a side at most 3.87 refutes H-129;
      confirmation requires an upper certificate below 11 over its full declared domain.
      Record outside-neighbourhood weight separately for the particular capture test.
    bead: think-7lp3
    workflows: [research-loop, factual-review]
    depends_on: []
    parallel_group: lanes-duality
    program: n11-structure-and-conditional-dots
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md
    - packing/campaign/agent-sessions/session-100-duality-kill-tests-and-unit-value.md
    outcomes:
    - scope: The B = 1 value at 96/25 and the four restricted regions at the retained shrink, one block in session-100 (2026-09-08, one worker at load 4 to 8)
      classification: time-limited
      result: >-
        Every reading is undecided. The B = 1 family at 96/25 verifies exactly at
        89090463224/9989418081 = 8.918 (768 unit placements, maximum depth exactly 1 over
        2,877,776 vertices, replayed from the bytes and re-declared in the unit regime) on a
        203-direction net densified at the axis and at Trump's angle, warm from BC-200's
        state; its weight is diffuse in angle, 3.22 within a degree of the axis and 0.03
        near 40.18 degrees, with 5.93 of its mass outside Trump's neighbourhood, and s(10)
        supplies a floor of 10 after strict separation, so the family is below that floor and the site
        LP of 11.17 is unconverged. The four-corner region's verified families reach 6.173
        and, polished, 6.261; a single corner box and the corner triangle are not
        D4-symmetric programs and inherit sub-restriction floors of 7.64 and 8.15; the
        central box loop was cancelled under load. No reported result decides the
        relevant upper certificate or capture question. The measurable instrument finding is that the loop's depth
        scaling, not its LP, loses the value; a depth polisher on the fixed support is the
        next instrument. 3.86 and 3.87 were not started. The handoff review identified a
        stronger retained control: exp-070's depth-one family transports to unit squares
        at side 38200/9977 < 96/25 with unchanged mass 21342289572/2055263195, about 10.3842.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md
      - packing/campaign/agent-sessions/session-100-duality-kill-tests-and-unit-value.md
      disposition: continue
      follow_up: think-7lp3
    - scope: The B = 1 values at 3.86 and 3.87
      classification: never-opened
      result: >-
        The 3.86 and 3.87 target runs never started. The cancelled central-box loop is
        included in the time-limited outcome above. The scratch state named for a resume is absent; a future
        run must begin from the retained exp-070 family and preserve exact source and
        destination net identities. No upper certificate or H-129 disposition follows.
      evidence:
      - packing/campaign/agent-sessions/session-100-duality-kill-tests-and-unit-value.md
      - docs/project/reviews/review-2026-09-08-pr127-research-readiness.md
      disposition: defer-dependency
      follow_up: think-7lp3
    next_evidence: Improve the retained 10.3842 control or certify an upper bound over the specified domain; test each proposed one-body or capture obstruction at its own scope.
  - id: BC-295
    purpose: research
    owner_focus: insight
    instances: [11]
    state: complete
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
    - packing/campaign/agent-sessions/session-102-angle-band-theorems-at-q.md
    outcomes:
    - scope: The registered replay and the end-band widening at 96/25 in session-102 (2026-09-08, one worker, grid 79 then grid 119)
      classification: achieved
      result: >-
        Every count in H-131 and both Section 2.3 end bands replay exactly through
        decide_class_program with masses equal to the planning lane's to the fraction. The
        robust end band widens far past 3 degrees. Theorems A, B and C exclude the exact
        rational cell unions recorded in exp-130, with masses 5529/512, 351/32 and
        11083/1024 respectively. Theorem C uses grid 119, least core 4101/4096 and 296
        atoms; its folded boundaries are approximately 10.387466 and 43.0737 degrees.
        Rounded degree labels are not closed theorem endpoints. The 45-degree end binds.
        The dual of the band toward 40.19 degrees
        carries 7.47 of its 11.25 units within 1.32 degrees of the axis and only 0.45 near
        Trump's angle, and ceiling.py decides all three duals' continuum depth exactly with
        scaled totals below 5.5. These duals therefore do not establish a continuum
        obstruction; the true class values toward 40.19 degrees remain open from below.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-b-angle-classes.md
      - packing/campaign/agent-sessions/session-102-angle-band-theorems-at-q.md
      disposition: retire-success
      follow_up: null
    - scope: The true restricted-class values toward 40.19 degrees beyond the tested site sets
      classification: inconclusive
      result: >-
        The reported site-program duals fail the continuum depth checks. They do
        not establish a continuum obstruction for the classes toward Trump's angle or a new
        theorem below U, so that distinct band-ladder question remains open.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-b-angle-classes.md
      - docs/project/reviews/review-2026-09-08-pr127-research-readiness.md
      disposition: continue
      follow_up: think-ndqj
    next_evidence: The first band theorem new below U; whether the obstruction at q is Trump-shaped or an integrality artefact that geometric conditioning can target.
  - id: BC-296
    purpose: research
    owner_focus: insight
    instances: [11]
    state: stopped
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
    outcomes:
    - scope: The complete near-axis composition split and class-weighted packing boundary at 96/25
      classification: never-opened
      result: >-
        This lane never opened. No composition was frozen or refuted, no survivor family
        was produced and no class-weighted packing-polytope boundary was measured. The
        exact band result for composition (11, 0) belongs to BC-295 and does not supply
        this lane's complete case accounting.
      evidence:
      - packing/campaign/agendas/agenda-030-parallel-structural-lanes-at-n11.md
      - docs/project/reviews/review-2026-09-08-pr127-research-readiness.md
      disposition: defer-dependency
      follow_up: think-n6fr
    next_evidence: Either the composition route ends at q with a certificate of its own impossibility, or the survivors become the branch list for geometric conditioning.
  - id: BC-297
    purpose: measurement_validation
    owner_focus: correctness
    instances: [11]
    state: complete
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
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-f-plateau-at-3-82.md
    - packing/campaign/agent-sessions/session-103-plateau-artefact-at-3-82.md
    outcomes:
    - scope: The artefact test, one site-addition run and the exact tight-cell census at 191/50, in session-103 (2026-09-08, 56 minutes of a 150-minute block)
      classification: achieved
      result: >-
        Decided exactly: the plateau is not a Trump-strip artefact. Trump's packing scaled by
        (191/50)/U has fourteen overlap strips 0.0124 to 0.0254 wide and 45 of the 3365
        grid-seed sites, 822 of BC-200's 12761 retained sites, lie in two or more of its cores,
        so the hypothesis's mechanism is refuted; the general mechanism holds in that BC-200's
        dual folds half its weight within 2.5 degrees of the axes and one per cent near Trump's
        angle. Adding 70 strip sites moved the row-converged value from 1223/110 to 11.072443
        and the generator stopped by its own criterion, which prices only the heaviest 32 dual
        rows. The exact census at the different mass 11.118805 found 0 exactly tight cells
        and 1,934,092 within the gap in 18,440 components spread over the centre domain.
        That census does not establish an obstruction for the original mass-eleven measure.
        The shrink tax was not measured and full-dual pricing remains untested.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-f-plateau-at-3-82.md
      - packing/campaign/agent-sessions/session-103-plateau-artefact-at-3-82.md
      disposition: retire-success
      follow_up: null
    - scope: The shrink tax and full-dual pricing beyond the capped 32-row generator
      classification: never-opened
      result: >-
        The shrink tax was not measured and the retained generator priced only its 32
        heaviest dual rows. Rejecting the Trump-strip explanation does not decide whether
        full-dual pricing or net refinement moves the plateau.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-f-plateau-at-3-82.md
      - docs/project/reviews/review-2026-09-08-pr127-research-readiness.md
      disposition: defer-dependency
      follow_up: think-4uon
    next_evidence: Whether the ladder's top is the instrument's or the geometry's; the size of the ownership tree.
  - id: BC-298
    purpose: research
    owner_focus: insight
    instances: [11]
    state: stopped
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
    outcomes:
    - scope: The rectangle bound at heights 3.80, 3.81, 3.815 and 3.82
      classification: never-opened
      result: >-
        No rectangle center-domain run or certificate was opened. No value of H0 was
        established and no converged restricted optimum obstructed the proposed route.
      evidence:
      - packing/campaign/agendas/agenda-030-parallel-structural-lanes-at-n11.md
      - docs/project/reviews/review-2026-09-08-pr127-research-readiness.md
      disposition: defer-dependency
      follow_up: think-jsi8
    next_evidence: Every wall within 3.84 − H0 of a square, both extents at least H0, and with the spanning lemma the strongest symmetry-breaking premise available.
  - id: BC-299
    purpose: research
    owner_focus: insight
    instances: [11]
    state: stopped
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
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-g-anchors-at-q.md
    - packing/campaign/agent-sessions/session-108-anchors-at-q.md
    outcomes:
    - scope: What Theorem E.4 and the corner-pair theorem localise at 96/25, in session-108 (2026-09-08), halted by an external usage limit before its validation
      classification: time-limited
      result: >-
        Theorem G.1 proves the grazing localisation of the escape class over Theorem E.4;
        Lemma G.4 and Theorem G.6, the latter with an exact rational pose, complete the
        band question; the anchor is priced by weak duality on the site set. The lane also
        records where exactly-one ownership fails: a segment can be shared by two touching
        squares, so localisation transfers but Stromquist's ownership does not. Its
        validation, final checkpoint and the second LP run were not reached.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-g-anchors-at-q.md
      - packing/campaign/agent-sessions/session-108-anchors-at-q.md
      disposition: continue
      follow_up: think-4ifm
    next_evidence: The premise every conditional certificate needs, a square forced into a known box, combined with the nine-point band into a concrete two-branch split.
  - id: BC-300
    purpose: research
    owner_focus: insight
    instances: [11]
    state: stopped
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
    outcomes:
    - scope: The adversarial corner, deep-avoidance and confined-rattler witness searches
      classification: never-opened
      result: >-
        The tentative lane was not funded and no target search ran. No exact witness,
        scoped no-witness result, mixed-pocket realization or merging lemma was produced.
      evidence:
      - packing/campaign/agendas/agenda-030-parallel-structural-lanes-at-n11.md
      - docs/project/reviews/review-2026-09-08-pr127-research-readiness.md
      disposition: defer-dependency
      follow_up: think-dfof
    next_evidence: Which corner branches cannot close near U, and whether the structural lane should spend time on elimination motions at all.
  - id: BC-301
    purpose: research
    owner_focus: correctness
    instances: [11]
    state: stopped
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
    outcomes:
    - scope: The exact-side tree and capture-architecture cost at the three declared radii
      classification: never-opened
      result: >-
        The architecture lane never opened. BC-294 returned no qualifying upper
        certificate and no exact-side tree or radius-specific cost design was produced.
      evidence:
      - packing/campaign/agendas/agenda-030-parallel-structural-lanes-at-n11.md
      - docs/project/reviews/review-2026-09-08-pr127-research-readiness.md
      disposition: defer-dependency
      follow_up: think-lbqe
    next_evidence: The only honest statement about the endpoint; if BC-294 kills capture, this reduces to the exact-side tree and needs BC-302 to be finite.
  - id: BC-302
    purpose: research
    owner_focus: insight
    instances: [11]
    state: complete
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
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md
    - packing/campaign/agent-sessions/session-104-ownership-set-at-q.md
    outcomes:
    - scope: The falsifier engine, the point-mark catalogue and the segment-mark cover at 96/25 in session-104 (2026-09-08, one worker at load 4 to 14)
      classification: achieved
      result: >-
        H-134's claim is met in segment form (Theorem E.4): replace each of Stromquist's ten
        Figure-13 points at 96/25 by the horizontal segment of length 1/10 centred on it, and
        every contained closed unit square lies within sqrt(2) * 2121/500000 < 3/500 of one of
        them. The later independent replay closes a far-wall sliver in the original
        reader; the promoted exact reader verifies every leaf and discard at both that
        sharper tolerance and 3/500. At tolerance 3/500, lengths 9/100 and 8/100 are also
        certified, while 7/100 and 6/100 have exact escapes. The retained point-mark
        catalogue has exact escapes; the handoff review retracts the proposed rounded
        fractional-cover and enlargement arguments. It also distinguishes the
        distinct-point orbit count from segment ownership. Localization for route (a)
        survives. Unique ownership does not follow: two separated squares can share a
        segment.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md
      - packing/campaign/agent-sessions/session-104-ownership-set-at-q.md
      disposition: retire-success
      follow_up: null
    - scope: Unique ownership and pairwise compatibility for squares localized near the ten segments
      classification: inconclusive
      result: >-
        The segment cover localizes every contained square but does not assign a unique
        owner: two interior-disjoint squares may share a segment without touching. The
        rounded-measure and enlargement helpers proposed for that step are invalid and
        retracted. A guarded pair reader over the resulting thin pose slabs is a distinct
        scientific scope, not unfinished certification of Theorem E.4.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md
      - docs/project/reviews/review-2026-09-08-pr127-research-readiness.md
      disposition: continue
      follow_up: think-qfog
    next_evidence: If it succeeds, route (a) collapses to about two to the twenty exact LPs; the prior is about thirty per cent.
  - id: BC-303
    purpose: research
    owner_focus: insight
    instances: [11]
    state: complete
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
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md
    - packing/campaign/agent-sessions/session-107-first-wave-selection.md
    outcomes:
    - scope: Independent replays of the first wave's three strongest claims and the selection, in session-107 (2026-09-08)
      classification: achieved
      result: >-
        All three replays agree, each with a reader written from the statement rather than
        from the lane's script. Theorem E.4 (the ten segments of length 1/10 unavoidable at
        3/500) is confirmed, with two disagreements recorded: the threshold length is in
        (7/100, 8/100] rather than (7/100, 9/100], since 8/100 decides with no failure and
        the lane's own reader confirms it at a finer floor, and the lane's certified domain
        misses a far-wall sliver its stated constant does not strictly absorb, which this
        replay closes. The corner-pair containment theorem is confirmed from the exported
        free measure and the ownership step re-derived. Theorem C is confirmed, the
        composition (11, 0) refuted exactly on the band at grid 119. The selection funds the
        segment cover toward an ownership argument as the next sustained block and the
        B = 1 depth polisher as the efficiency block (with the plateau's full-dual pricing
        as its first task), retains the band ladder as filler rather than a block, and
        defers the corner-pair anchored certificate until the restricted fractional packing
        value is measured, since the duality lemma bounds a conditional certificate by it.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md
      - packing/campaign/agent-sessions/session-107-first-wave-selection.md
      disposition: retire-success
      follow_up: null
    next_evidence: The frozen claim for the next block and the remaining proof obligations.
  - id: BC-304
    purpose: research
    owner_focus: correctness
    instances: [11]
    state: complete
    priority: 0
    question: What survives independent checking, what did it change about the global problem, and what is the next consequential question?
    budget: One closeout block of two hours with the final hour reserved for verification, integration and publication.
    entry: BC-303's selection and the stopped second-wave handoff; the owner's 2026-09-08 instruction to review and merge the handoff before continuing on a new branch.
    exit: Independently checked strongest result, honest bound impact, complete domain accounting, disposition of every lane, the discharge edges into Agenda 029, and one next consequential question.
    bead: think-yrw1
    workflows: [factual-review, documentation-pass, review-planning-oversight]
    depends_on: [BC-303]
    program: n11-structure-and-conditional-dots
    artifacts:
    - docs/project/reviews/review-2026-09-08-pr127-research-readiness.md
    - packing/campaign/agent-sessions/session-110-pr127-handoff-review.md
    outcomes:
    - scope: Independent review and terminal disposition of the Agenda 030 handoff
      classification: achieved
      result: >-
        Independent exact replay preserves Theorem E.4's ten horizontal segments of
        length 1/10 at tolerance 3/500, the corner-pair theorem and the rational
        angle-cell exclusions. The review retracts the rounded-cover and enlargement
        helpers, corrects the corner clip, ratio scope, angle labels, retained-net cap
        and one-body acceptance rules, and records session 109 run 4 as partial and run 5
        as never run. The transported exp-070 family is a stronger retained depth-one
        control of weight 21342289572/2055263195 at side 38200/9977 below 96/25. No
        certified lower or upper bound changes. Unrun compositions, rectangle bounds,
        witnesses and closing-route cells remain stopped; missing scratch state and the
        corner and anchor complements remain named. The next principal question is
        whether two squares localized near one segment satisfy a checked pairwise
        compatibility restriction strong enough to reduce the ownership case split.
        Merge and the corrected-tree checkpoint remain pending.
      evidence:
      - docs/project/reviews/review-2026-09-08-pr127-research-readiness.md
      - packing/campaign/agent-sessions/session-110-pr127-handoff-review.md
      disposition: retire-success
      follow_up: null
    next_evidence: The owner reviews the mathematical result and the next selection.
  closeout:
    documentation_review:
    - path: README.md
      decision: checked-current
      reason: The certified packing bracket is unchanged, so the reader-facing summary needs no bound edit.
    - path: SYNOPSIS.md
      decision: updated
      reason: The generated agenda and session views will record this closeout and its selected continuation.
    - path: TUTORIAL.md
      decision: checked-current
      reason: No tutorial algorithm or user workflow changed in this research handoff.
    - path: conventions.md
      decision: checked-current
      reason: Existing evidential-status and historical-record rules already require the scoped corrections.
    - path: development.md
      decision: checked-current
      reason: The established full checkpoint and generated-view entry points remain the required closeout commands.
    - path: operating-rules.md
      decision: updated
      reason: The model-routing and continuation rules used by the reviewed handoff are now recorded there.
    changes:
    - name: proof-scope-corrections
      result: >-
        Unsupported cover, clip, ratio, acceptance, rounded-angle and retained-net claims
        are retracted or narrowed while historical runs and exact surviving results remain.
      paths:
      - docs/project/reviews/review-2026-09-08-pr127-research-readiness.md
      - packing/campaign/explorations/X-021-what-can-be-proved-about-eleven-squares.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-a-corner-structure.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md
    - name: portable-controls
      result: >-
        Guarded repository tools preserve the surviving segment theorem, audit the
        retracted rounded-measure claim and transport the stronger retained unit family.
      paths:
      - packing/devtools/rounded_measure_audit.py
      - packing/devtools/segment_cover_replay.py
      - packing/devtools/transport_ceiling_family.py
    - name: terminal-handoff
      result: >-
        Every lane is dispositioned at its actual scope, Agenda 029 receives its discharge
        edges and the funded continuation is separated from completed theorem scope.
      paths:
      - packing/campaign/agendas/agenda-029-structural-restrictions-and-conditional-dots.md
      - packing/campaign/agendas/agenda-030-parallel-structural-lanes-at-n11.md
      - packing/campaign/agent-sessions/session-110-pr127-handoff-review.md
    validation:
    - scope: corrected-integration-checkpoint
      status: pending
      evidence: >-
        The corrected integration tree has not yet completed its own full packing-validate
        checkpoint. Earlier c89c7646 records and focused tests and the 8176e389 deferred
        checkpoint are historical baselines only and do not certify this tree.
    replanning:
      candidates:
      - bead: think-yx4g
        workflow: remediation
        priority: 1
        rationale: Repair the failed checkpoint components and certify the integrated handoff before the authorized merge and new-branch research.
      - bead: think-qfog
        workflow: insight-iteration
        priority: 1
        rationale: >-
          Continue from the completed ten-segment theorem at a distinct scope: build a
          guarded pair reader for compatibility and ownership without assuming unique hits.
      - bead: think-7lp3
        workflow: efficiency-loop
        priority: 1
        rationale: >-
          Start from the retained 10.3842 depth-one control and measure full-dual pricing
          before any separately registered target continuation.
      - bead: think-kx2l
        workflow: insight-iteration
        priority: 2
        rationale: >-
          Retain the corner-class support question, missing run artifacts and unrun site-set
          complement behind the two higher-priority lanes.
      selected:
        bead: think-yx4g
        workflow: remediation
        rationale: >-
          The mathematical closeout is complete, but the corrected integration checkpoint
          failed local environment and record checks. Certify those repairs before releasing
          the funded ownership continuation.
      operator_input:
        status: confirmed
        note: The owner authorized closeout, merge once the corrected tree is ready, and continuation on a new branch.
---
# Agenda 030 — Parallel Structural Lanes at `n = 11`

**This agenda is complete.** BC-291 wrote the parallel plan; sessions 100 through 104,
107 through 110 and the retained lane reports record what ran, what stopped and what was
never opened. [X-021](../explorations/X-021-what-can-be-proved-about-eleven-squares.md)
carries the structural mathematics, while the frontmatter above is the terminal
disposition and replanning record.
The corrected integration checkpoint and merge remain pending and therefore supply no
certification or bound change here.

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

BC-304 records the truthful `discharged_by` edges in Agenda 029 and stops its unmet or
never-opened cells, so the older queue no longer offers work this agenda already
handled.

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
request. At the planning checkpoint, the next free lane identity was `session-100` and
the next free experiment identity was `exp-130`; those historical allocation notes are
not current reservations and are not reused.

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
with `α + β ≥ 3°`). An exact `B = 1` fractional family of value at least eleven
obstructs a strict one-body covering certificate at its side.
Sufficient weight outside an exactly specified Trump neighbourhood additionally
obstructs that capture certificate.
These tests leave ownership, compatibility and integrality arguments open; BC-294 alone
cannot rule out the ambitious tier.

A promising result does not extend a lane’s clock.
A lane that ends early because of tokens or an external limit publishes the same fields
at its current scope.

## Original Coordinator Handoff

The following was the launch instruction used for the completed run.
It is retained as historical protocol, not as a live dispatch.

> Start Agenda 030’s lanes only under the owner’s research-start instruction.
> Read X-021 and this agenda; check the current branch, the stacked pull requests and
> live beads. Allocate `session-NNN` and, when a lane freezes a claim, `exp-NNN`
> serially, after rechecking main and every open pull request, including PR 120.
> Dispatch the ready lanes with the lane brief below, each with its exact result path
> and its hypothesis. Apply OR-2: Astra at extra high or max / Fable at extra or max for
> mathematical obligations, Sol / Opus at high, extra high or max as appropriate for
> mechanical work. Name the actual supported setting in the dispatch.
> Push at the first commit worth a hosted run and read CI from its receipts at the next
> block boundary. At the end of the first wave, run BC-303 with independent review before
> selecting; BC-304 closes.

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
