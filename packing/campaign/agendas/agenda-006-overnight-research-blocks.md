---
title: agenda-006 — four bounded overnight blocks, each ending in a checkpoint that holds
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-006
  title: Four bounded overnight blocks, each ending in a checkpoint that holds
  updated: '2026-08-29'
  status: active
  objective: >-
    Schedule one unattended overnight run across three independent agenda-005 lanes, in
    blocks small enough that an interruption costs one block rather than the night. This
    agenda owns the clock, the ordering, and what a block must leave behind; it does not
    own a single scientific exit. Those stay with the agenda-005 commitments each block
    advances, so a block that stops early narrows the schedule and never a claim. The
    ordering is deliberate: the interval-certification lane runs first because it is the
    only one that can move a verified bound, and because session-035 left it declared and
    unstarted.
  items:
  - id: BC-052
    purpose: tool_validation
    owner_focus: correctness
    instances: [5, 10, 11, 29]
    state: complete
    priority: 0
    question: >-
      Can the interval-certification bridge be built as far as a Krawczyk operator and an
      interval separating-axis test that both refuse correctly, inside one 150-minute
      block, without any claim being made about n = 29?
    hypotheses: []
    budget: >-
      150 minutes from 2026-08-29T03:10Z, in slices of at most 30; a 20-minute
      finalization reserve inside that total
    entry: >-
      BC-047 is complete, so a refined n = 29 pose to 1000 declared digits already exists;
      the witness contract already names `interval-certified`; and PR 60 is merged so the
      block starts from a green main
    exit: >-
      Phases 1 and 2 of plan-2026-08-28-interval-certification are implemented with every
      control that spec names firing, or a typed statement of which conditioning stopped
      them. Either way the block ends committed, pushed, and carried by an open PR whose
      fast gate is green.
    artifacts:
    - src/sqpack/promote/interval.py
    - src/sqpack/promote/krawczyk.py
    - src/sqpack/promote/enclose.py
    - src/sqpack/promote/interval_verify.py
    - tests/test_promote_interval.py
    - tests/test_promote_krawczyk.py
    bead: think-pr0m
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      Session-035 closed with this as its declared next action, naming BC-045 and
      `think-75ll` and the spec's phases 1 and 2. Nothing has been built against it since,
      so the block starts exactly where that handoff points.
    note: >-
      A scheduling container. The scientific exit is owned by BC-045 in agenda-005 and by
      plan-2026-08-28-interval-certification; this item owns only the clock and the
      checkpoint. The uniqueness half of the Krawczyk verdict is the load-bearing part: a
      box holding two roots does not identify which pose was certified, so interior
      containment is checked rather than containment.
      Closed in session-036, inside the block clock. Phases 1 and 2 are built and every
      stage that can refuse was watched refusing; negative controls rise from 86 to 90 and
      the fast gate is green at 4m03s. The calibration against `sqpack.field` found two
      soundness bugs that inspection had not, both flattering: certificate endpoints were
      serialized by rounding to nearest, which lifted both ends of a box above the root it
      enclosed, and the operator reported its final iteration rather than the verdict it had
      proved, discarding a uniqueness result obtained two iterations earlier. The block's
      load-bearing result is a refusal: four unit squares packed exactly into a side-2
      container return six undecided pairs and zero separated, which is correct and is what
      a tolerance-based checker gets wrong. Nothing here certifies n = 29 and
      `verified_upper_bound` is untouched.
  - id: BC-053
    purpose: tool_validation
    owner_focus: correctness
    instances: [5, 10, 11, 29]
    state: complete
    priority: 0
    question: >-
      Does the checker agree with the exact route where the answer is already known, and
      what does it return at n = 29 — a certificate, or a typed refusal naming its cause?
    hypotheses: []
    budget: >-
      180 minutes from about 2026-08-29T05:40Z, in slices of at most 30; a 20-minute
      finalization reserve inside that total
    entry: >-
      BC-052 left a Krawczyk operator and an interval separating-axis test whose controls
      fire; origin/main has been merged at the start of this block
    exit: >-
      Phases 3 and 4 of the same spec: n = 5 and n = 10 certified in agreement with the
      exact route, n = 11 certified against Trump's published polynomial, a demonstrated
      refusal on a plausible-but-infeasible pose, and then whatever n = 29 actually
      returns. Any n = 29 success is recorded `unresolved` with `needs_review: true`; this
      runner may not accept it.
    artifacts:
    - src/sqpack/promote/relax.py
    - cases/kingbird29/layout.py
    - cases/kingbird29/certify_interval.py
    - tests/test_promote_relax.py
    - campaign/series/series-000-smoke-and-calibration/results/bc-053-n29-interval-certificate.json
    bead: think-9ida
    depends_on: [BC-052]
    workflows: [pipeline-improvement]
    next_evidence: >-
      Calibration is the test here and it is stronger than for the exact route, because
      n = 5, n = 10 and n = 11 have answers this implementation cannot influence. Agreeing
      with the exact route on valid input proves nothing about discrimination, which is
      why the refusal demonstration is part of the exit rather than a nicety.
    note: >-
      Advances BC-045. `verified_upper_bound` does not move in this block and no document
      may describe the reported n = 29 value as certified until a human accepts it. The
      bound move is a reviewed change through the evidence contract, never a search
      result written into the record.
      Unblocked by block 1. BC-052 delivered an operator whose controls fire and a verifier
      that refuses by name, which is this commitment's entry criterion, so the dependency is
      discharged rather than merely older. The schema decision phase 4 needs -- whether a
      fourth `scalar.kind` extends `Witness/v1` or forces a `v2` migration -- is taken in
      this block with calibration results in hand, not before them.
      Closed in session-037, slightly past the nominal boundary against block 4's slack.
      Phases 3 and 4 are built and calibrated. The route agrees with the exact one on
      n = 5, n = 10 and n = 11 -- strictly above each exact side and falling with the
      relaxation -- and proves an overlap of 1e-30 that a float check at 1e-9 accepts,
      which is the discrimination agreement alone cannot demonstrate. At n = 29 the chain
      completes: `s(29) <= 5.93383346267692918974379895098` at eps = 1e-20, all 406 pairs
      strictly separated, recorded `unresolved` with `needs_review: true` and promoting
      nothing. The strongest check was unplanned: verified unrelaxed, the 52 pairs the
      chain cannot decide are exactly the 52 contacts BC-042 extracted by a different
      route. D-356 records a control-harness limitation found on the way and reproduced on
      a clean tree.
  - id: BC-054
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 29]
    state: complete
    priority: 1
    question: >-
      Can the contact equations be assembled and closed from a frozen structure, and can
      the closed system then be solved exactly and discharged rather than trusted?
    hypotheses: []
    budget: >-
      180 minutes from about 2026-08-29T08:40Z, in slices of at most 30; a 20-minute
      finalization reserve inside that total
    entry: >-
      BC-042 froze the n = 29 contact structure with an empty ambiguity report, which is
      BC-043's entry criterion; BC-047 supplies the refinement BC-044 needs; origin/main
      has been merged at the start of this block
    exit: >-
      A reduced system in `s` and the distinct non-axis-aligned angles, closed by
      determinant conditions and reproducing the known n = 11 system — or a typed
      statement of which reduction the particular contact graph does not admit. Then, if
      the clock allows, BC-044's exact solve under its frozen margin rule.
    artifacts:
    - src/sqpack/promote/system.py
    - src/sqpack/promote/contacts.py
    - tests/test_promote_system.py
    - atlas/known-best/contact-structures.json
    bead: think-zm3f
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      This is the unbuilt middle of the exact route: `promote/contacts.py` and
      `promote/refine.py` exist, and `promote/system.py` and `promote/solve.py` do not, so
      the pipeline currently runs from a structure straight to a refinement with no
      assembly between them.
    note: >-
      Advances BC-043 and then BC-044, both in agenda-005, which own their exits. This
      lane is independent of BC-052 and BC-053: the exact and interval routes are
      complements, and neither unblocks the other. X-004 found no integer relation through
      degree twenty below 10^22, so BC-044 may terminate in a refusal, and a refusal here
      is a result rather than a failure of the block.
      Closed in session-038, and it reached BC-043 rather than BC-044: the block clock went
      to three findings that each changed what assembly had to do. Contacts now identify
      which features meet -- typed from the intersection of their supports across every
      realising axis, because per-axis reading turns a corner-corner contact into two
      edge-edge ones that do not exist -- and assembly turns a structure into equations that
      vanish at the packing they came from, `4.44e-16` at n = 11. Counting rows is the wrong
      instrument: n = 11 is overdetermined by the count and four conditions short by the
      rank, so closure is sized by the shortfall. An angle class does not license an angle
      identity, which n = 29 showed with a residual of exactly pi. And seven n = 29 squares
      are reflected, which a centre-plus-rotation pose cannot represent, so assembly refuses
      them by name. Phase 4's exact solve was not reached.
  - id: BC-055
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5]
    state: stopped
    priority: 1
    question: >-
      Can verification run only the steps a change can reach without ever running fewer
      than it should, and are the three packings the catalogue annotates "Rigid." actually
      rigid on evidence of our own?
    hypotheses: []
    budget: >-
      150 minutes from about 2026-08-29T11:40Z, split between the two lanes, in slices of
      at most 30; a 20-minute finalization reserve inside that total
    entry: >-
      A measured baseline for the gate exists — 4m15s for `--fast` on this container,
      recorded in block 1 — and origin/main has been merged at the start of this block
    exit: >-
      Either a reachability-scoped verification selector with a control proving it cannot
      under-run, measured against that baseline, or a measured rejection. Then a bounded
      n = 5 rigidity pass that produces our own evidence or names exactly what it would
      take.
    bead: think-ojlr
    depends_on: []
    workflows: [efficiency-loop, research-pass]
    next_evidence: >-
      The 4m15s baseline was measured on this container at the start of the run rather
      than assumed, and its breakdown is already known: 250.86s of fast behavioural tests
      against 40.38s of soft-schema validation and 30.29s of lint. Any selector that does
      not move the test figure has not moved the gate.
    note: >-
      Advances BC-051 and BC-049 in agenda-005. Deliberately last: both lanes are
      independent and bounded, so this is the block that can absorb overrun from the three
      ahead of it without any scientific commitment being cut short. Under-running the
      gate is the failure mode that matters; a selector that is merely slow is a
      disappointment, and one that skips a step a change can reach is a soundness defect.
      Not run, and recorded as stopped rather than left ready so the queue does not imply
      work that this run did not do. The reason first written here -- that blocks 2 and 3
      overran into this cell's slack -- was false, and is corrected under D-358: the commit
      timestamps give blocks of 31, 42, 29 and 23 minutes against declared budgets of 150,
      180, 180 and 40, so nothing overran and the run stopped with most of its budget
      unspent. The coordinating agent misread its own clock by about a factor of four.
      Nothing measured here is retracted: the 4m15s baseline stands, and BC-051 and BC-049
      remain ready in agenda-005, rescheduled inside this agenda as BC-062 and BC-063.
      An earlier version of this note sent them to an `agenda-007` that was never written.
  - id: BC-056
    purpose: tool_validation
    owner_focus: process
    instances: [5, 10, 11, 16, 29]
    state: complete
    priority: 0
    question: >-
      After a night of unattended work, does the whole record still hold together at the
      endpoints — gate, generated views, schemas, links, and the PR?
    hypotheses: []
    budget: 40 minutes from about 2026-08-29T14:10Z
    artifacts:
    - campaign/research-loop-logbook/run-002-2026-08-29-overnight-promotion-blocks.md
    entry: >-
      The four blocks have reached terminal states, whatever those states are: BC-052,
      BC-053 and BC-054 complete, BC-055 stopped unrun
    exit: >-
      A full strict `packing-validate` receipt, every generated view regenerated from its
      source, a research-loop logbook entry covering the run, agenda and session artifacts
      reconciled with what actually happened, and a pushed PR whose checks are green.
      Blocks that stopped early are recorded as stopped with their exact limitation, never
      quietly dropped.
    bead: think-lo3p
    depends_on: [BC-052, BC-053, BC-054]
    workflows: [process-review]
    next_evidence: >-
      The strict gate is the only receipt that exercises the slow tiers, and no block
      above runs it; each runs the fast gate instead. So the run's one end-to-end check
      belongs here, where there is still clock left to repair what it finds.
    note: >-
      The endpoint check is a commitment rather than a courtesy: an unattended run that
      ends without one has produced work nobody has seen fail.
      Closed. The full strict gate passes all 38 steps in 6m20s, generated views are
      regenerated from their sources, and run-002 records the whole run. It earned its
      place: the first strict run failed, because the logbook entry names
      `verified_upper_bound` and the consumer contract required it to say what it takes
      the field to mean. That is the contract working, and it is the kind of thing only an
      end-to-end check finds.
  - id: BC-057
    purpose: tool_validation
    owner_focus: correctness
    instances: [29]
    state: complete
    priority: 0
    question: >-
      Can an interval certificate be written into the record as a witness the contract
      accepts, rather than living as a script and a JSON file beside it?
    hypotheses: []
    budget: 45 minutes, sized from the 28-42 minute blocks this run actually measured
    entry: >-
      The n = 29 certificate exists and has survived an independent re-verification round;
      the witness contract already names `interval-certified` as a method but has no
      scalar kind for an enclosure and no checker branch
    exit: >-
      A fourth `scalar.kind` carrying the operator verdict, the pose box and the declared
      relaxation; an `exact_verify` branch that replays an interval witness instead of
      raising `checker-not-built`; the n = 29 witness emitted and replayable; and an
      evidence entry recording assurance, method and replay. `verified_upper_bound` does
      not move.
    artifacts:
    - witnesses/witness.schema.yaml
    - src/sqpack/witness.py
    - frontier/evidence.yaml
    - witnesses/kingbird-n029-2026-interval.yaml
    - tests/test_witness_interval.py
    bead: think-pfwx
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      `exact_verify` has raised `checker-not-built` on this branch since the contract was
      written. The socket was left open deliberately; this closes it.
    note: >-
      The first of the missing middle layers, and the one that decides whether anything
      built in this run is reviewable by someone else. Recording is not promotion: the
      certificate enters as evidence with its assurance stated, and whether the ceiling
      moves stays a human decision.
      Closed in session-039, in 45 minutes read from a clock rather than estimated.
      `exact_verify` replays an interval witness instead of raising `checker-not-built`,
      and the n = 29 certificate verifies through the public tool at 406 of 406 pairs.
      The replay found a real bug on its first run -- 52 undecided pairs, the packing's
      contact count, because 40-digit enclosures were parsed at mpmath's ambient 15 and
      widened past the 1e-20 relaxation -- and precision is now pinned from the witness.
      Controls rise from 97 to 100. `verified_upper_bound` is untouched, and the block
      also corrected this run's own clock record under D-358.
  - id: BC-058
    purpose: tool_validation
    owner_focus: correctness
    instances: [29]
    state: complete
    priority: 0
    question: >-
      Can the pose model carry a chirality, so a layout built from mirror groups can be
      assembled instead of refused?
    hypotheses: []
    budget: 45 minutes
    entry: >-
      Assembly refuses seven of the twenty-nine n = 29 squares by name, because a
      centre-plus-rotation pose cannot produce a clockwise winding
    exit: >-
      Either the n = 29 contact system assembles with equations that vanish at the
      published pose, or a typed statement of what a chirality costs the feature naming
      and why that price is not worth paying.
    artifacts:
    - src/sqpack/promote/contacts.py
    - src/sqpack/promote/system.py
    - atlas/known-best/contact-structure.schema.yaml
    - atlas/known-best/contact-structures.json
    - tests/test_promote_system.py
    - devtools/controls.yaml
    - campaign/agent-sessions/session-040-block6-chirality.md
    bead: think-km5r
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      Closed in session-040. The corner model now reflects the local x axis before the
      rotation turns it, and the n = 29 assembled residual falls from `2.0` to `1.3e-15`
      across 94 equations with the n = 11 calibration unmoved at `4.4e-16`, rank 30 and
      shortfall 4. The assembled n = 29 system has rank 81 against 88 unknowns.
    note: >-
      A middle layer. This commitment was written expecting the hard part to be that
      feature indices refer to a corner order, so re-winding a square would rename its
      features. That cost was not paid: reflecting the *local* axis leaves the corner
      indices alone and changes only where each one sits, so no feature name changed and no
      structure needed re-indexing. Recorded because the expectation was wrong and a reader
      should meet the correction where the expectation was set.
  - id: BC-059
    purpose: tool_validation
    owner_focus: correctness
    instances: [5, 11]
    state: complete
    priority: 1
    question: >-
      Can the stationarity conditions that `close` currently only counts be derived, so a
      closed system can actually be solved?
    hypotheses: []
    budget: 60 minutes
    entry: >-
      `close` sizes the shortfall from the contact Jacobian's rank -- one condition at
      n = 5, four at n = 11 -- and returns descriptions rather than equations
    exit: >-
      Determinant or Lagrange conditions in a form a solver accepts, reproducing the known
      n = 11 system; or a typed statement of which formulation the contact graph resists.
    artifacts:
    - src/sqpack/promote/system.py
    - tests/test_promote_system.py
    - devtools/controls.yaml
    - defects.yaml
    - campaign/agent-sessions/session-041-block7-collinearity.md
    bead: think-9c40
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      Closed in session-041, and the answer was that there were none to derive at either
      large size. `edge-edge` was assembled as one equation where collinearity is two, so
      the shortfall `close` reported was a bug rather than a property of the packings. With
      the second equation the contact Jacobian reaches full rank -- 34 of 34 at n = 11 and
      88 of 88 at n = 29 -- residuals unmoved at `8.9e-16` and `1.3e-15`, and `close`
      refuses at both. Recorded as D-361, class soundness, direction conservative. n = 5
      has no edge-edge contact, is untouched, and keeps a genuine shortfall of one.
    note: >-
      The layer between assembly and the exact solve. It turned out to be an assembly
      repair rather than a derivation, and what remains is one condition at n = 5 -- now
      the only size that needs one and the cleanest case to derive it on. Carried into
      BC-063, which is already the n = 5 rigidity cell.
  - id: BC-060
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 29]
    state: complete
    priority: 1
    question: >-
      Can the closed system be solved exactly and the result discharged rather than
      trusted?
    hypotheses: []
    budget: 60 minutes
    entry: >-
      A full-rank contact system from BC-059. Not "closed" in the sense this commitment was
      written expecting: nothing was added, an `edge-edge` equation was repaired, and the
      contacts then determine the pose on their own -- 122 equations in 88 unknowns at
      n = 29, overdetermined and full rank.
    exit: >-
      A minimal polynomial by elimination or integer relation under the spec's frozen
      margin rule, discharged by back-substitution at n = 11 against Trump's published
      degree-8 polynomial; then whatever n = 29 returns, including a refusal.
    artifacts:
    - src/sqpack/promote/solve.py
    - devtools/probe_minimal_polynomial.py
    - devtools/probe_contact_system.py
    - tests/test_promote_solve.py
    - campaign/agent-sessions/session-042-block8-exact-solve.md
    bead: think-ovp7
    depends_on: [BC-059]
    workflows: [pipeline-improvement]
    next_evidence: >-
      Closed in session-042, with one answer and one refusal. At n = 11 the frozen margin
      rule recovers Trump's published degree-eight polynomial from digits alone -- C=12420,
      B=36.85, M=200, residual `4.99e-338` at B+M falling to `3.38e-412` at 2B+2M -- and
      discharges it as irreducible over Q with an isolating interval. At n = 29, on 1000
      digits with a reported residual bound of `1.09829e-1039`, `pslq` returns nothing at
      any degree from 2 through 20 below `10^22`: not one degree reached a clause. So if
      `s(29)` is algebraic of degree twenty or less, some coefficient is at least `10^22`.
    note: >-
      Advances BC-044 in agenda-005. The refusal is the result the commitment anticipated,
      and it is now measured rather than expected: the planning probe found relations at
      almost every degree from ~98 digits and the same search finds none from 1000, which
      is evidence about the number rather than about the search. That is the concrete
      reason the interval route carries the n = 29 bound.
  - id: BC-061
    purpose: tool_validation
    owner_focus: correctness
    instances: [5, 11]
    state: ready
    priority: 1
    question: >-
      Can an exact LP over certified coefficients replace the float solver where a
      certified answer is required?
    hypotheses: []
    budget: 60 minutes
    entry: >-
      D-021 records a `1e-11` floor on the float LP, which is what keeps the quench usable
      only on someone else's high-precision data
    exit: >-
      An LP over exact rational or algebraic coefficients agreeing with the float path
      where both are valid, and a report of which cells need algebraic rather than
      rational coefficients; or a typed statement of what blocks it.
    bead: think-twa7
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      Phase 5 of the promotion spec, unbuilt since it was written. It is the last of the
      middle layers and the one that makes the route usable on poses this repository
      produces rather than only on published ones.
    note: >-
      Advances BC-048 in agenda-005.
  - id: BC-062
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5]
    state: ready
    priority: 2
    question: >-
      Can verification run only the steps a change can reach, without any chance of
      running fewer than it should?
    hypotheses: []
    budget: 45 minutes, only if the middle layers above are terminal
    entry: A measured baseline of 4m15s for `--fast` on this container
    exit: >-
      A reachability-scoped selector with a control proving it cannot under-run, measured
      against that baseline; or a measured rejection.
    bead: think-d0q7
    depends_on: []
    workflows: [efficiency-loop]
    next_evidence: >-
      D-355 measured a two-file edit at `979.79s` against the `12.06s` its two affected
      steps need, an 82x overrun.
    note: >-
      Deliberately behind the middle layers. This is a tool for the loop rather than for
      the mathematics, and the run has now twice been in a position to cut it; saying so in
      its priority is more honest than leaving it nominally next.
  - id: BC-063
    purpose: research
    owner_focus: insight
    instances: [5]
    state: ready
    priority: 3
    question: >-
      Are the three packings the catalogue annotates "Rigid." actually rigid, on evidence
      of our own?
    hypotheses: []
    budget: 45 minutes, only if everything above is terminal
    entry: The catalogue's annotation, and no independent check of it
    exit: Our own rigidity evidence at n = 5, or a statement of what producing it would take.
    bead: think-298s
    depends_on: []
    workflows: [research-pass]
    next_evidence: >-
      Advances BC-049 in agenda-005. The only genuinely research-shaped cell in this
      continuation; everything above it is tooling.
    note: >-
      Last on purpose. It is the cell that can be cut without leaving a tool half-built.
  - id: BC-065
    purpose: tool_validation
    owner_focus: correctness
    instances: [29]
    state: complete
    priority: 0
    question: >-
      Did the integer-relation refusal at n = 29 survey the space, or a corner of it?
    hypotheses: []
    budget: 45 minutes
    entry: >-
      BC-060 named two routes -- elimination via SymPy and integer relation via mpmath
      pslq -- and only the second was built. It refused through degree twenty below `10^22`
      on a thousand digits, and nothing said what degree `s(29)` actually has.
    exit: >-
      A bound on the algebraic degree of `s(29)`, computed from the published system rather
      than estimated; or a typed statement of what in the transcription resists
      rationalisation.
    artifacts:
    - src/sqpack/promote/interval.py
    - devtools/probe_system_degree.py
    - tests/test_promote_system_degree.py
    - campaign/agent-sessions/session-043-block9-degree-bound.md
    bead: think-obgk
    depends_on: [BC-060]
    workflows: [pipeline-improvement]
    next_evidence: >-
      Closed in session-043. Under `u = tan(theta/2)` the six equations rationalise over Q
      with total degrees `[11, 15, 10, 15, 7, 6]`, so the Bezout bound on the solution
      variety is `1,039,500` -- degree twenty was a corner. Every equation is degree one in
      `s`, and solving the smallest for it gives `s` as a rational function of `u_b` and
      `u_c` alone, leaving five equations in five unknowns with degrees `[16, 20, 15, 20,
      12]`.
    note: >-
      The elimination itself is deliberately not attempted here and stays on `think-obgk`:
      a resultant chain over five variables at these degrees is where the exact-algebraic
      route either succeeds or is shown to be out of reach at n = 29, and it needs its own
      budget. Read the bound as "not small" rather than "this large" -- Bezout is loose for
      a structured system.
  - id: BC-066
    purpose: tool_validation
    owner_focus: correctness
    instances: [29]
    state: complete
    priority: 0
    question: >-
      Can the five-unknown system be eliminated to an eliminant in `s`, or is the
      exact-algebraic route out of reach at n = 29?
    hypotheses: []
    budget: 90 minutes, with a declared wall-clock cap inside it
    entry: >-
      BC-065 leaves five equations in five half-angles over Q, total degrees
      `[16, 20, 15, 20, 12]`, after `s` is solved out of the smallest equation.
    exit: >-
      An eliminant in `s` whose degree is measured rather than bounded, discharged through
      `promote/solve.discharge`; or a typed statement of where the chain stopped and what
      it cost, which is itself the answer that the interval route carries n = 29.
    artifacts:
    - devtools/probe_elimination.py
    - tests/test_promote_elimination.py
    - campaign/series/series-000-smoke-and-calibration/results/bc-066-n29-elimination-wall.json
    bead: think-obgk
    depends_on: [BC-065]
    workflows: [pipeline-improvement]
    next_evidence: >-
      The Bezout bound is `1,039,500`, an upper bound and loose. Two failure modes are
      known in advance and the block should measure which one it hits. A **resultant
      chain** multiplies degrees at every step -- from `[16, 20, 15, 20, 12]` one
      elimination gives about `320`, the next about `10^5` -- and introduces extraneous
      factors, so a successful chain still ends in factoring a very large polynomial.
      A **Grobner basis** in lex order is doubly exponential in the worst case, but what
      kills it in practice is intermediate coefficient swell: coefficients reach thousands
      of digits from single-digit inputs and memory runs out before the steps do. Report
      the sizes reached at each step rather than running until something dies.
    note: >-
      A refusal here is a result and should be recorded as one: it would say the exact
      route does not reach n = 29 at any practical cost, which is the measured
      justification for the interval route carrying that bound. Do not widen the cap to
      reach a positive answer.

      **"Intractable in SymPy" is not "intractable", and the block should say which it
      found.** Four things are worth reaching for before concluding the route is closed,
      roughly in order of expected return: `msolve` or Singular or Magma, which implement
      F4/F5 and compute a rational univariate representation of a zero-dimensional system,
      and are orders of magnitude past SymPy's Buchberger; **multi-modular** computation,
      which does the work mod several primes where coefficients stay bounded and lifts by
      CRT and rational reconstruction, attacking the swell directly; **homotopy
      continuation** (`HomotopyContinuation.jl`, Bertini), which tracks the solution paths
      numerically and yields the *degree of the projection to the s-axis* without the
      polynomial -- which is what would turn BC-060's blind sweep into a targeted search at
      a known degree; and **LLL over a scaled integer lattice** (`fplll`) in place of
      mpmath's pure-Python `pslq`, plausibly two to three orders of magnitude faster and so
      a real change in reachable degree. None is in this repository today, so adding one is
      part of the block rather than a prerequisite for it.

      The two routes compose rather than compete. A successful elimination returns an
      eliminant whose roots are the sides of *every* complex solution of the system, so the
      irreducible factor carrying our root still has to be identified -- which needs the
      high-precision numerics back again.

      Closed in session-044, and the answer is a measured wall rather than an eliminant.
      Three runs, all on the six-equation system with `s` ordered last, all guarded by an
      export that re-parses its own text: over `Q` in an elimination order, F4 was
      OOM-killed at degree 32 after 25m09s with 13.8 GB resident, having reached matrices
      of `656126 x 1670545` at degree 31; mod `1073741827` in the same order the matrix
      dimensions were *identical* and the memory about 70 per cent of it; and mod the same
      prime in plain grevlex -- an order of magnitude cheaper, largest matrix
      `20611 x 49890`, 2.7 GB -- the pair list still grew monotonically to 21,661 and no
      basis was reached inside a declared 25-minute cap.

      **Neither predicted failure mode is what stopped it.** Coefficient swell cannot
      occur over `F_p`, where every coefficient is one machine word, and the cheapest
      monomial order did not terminate either. What the runs measure is the size of the
      ideal itself, not the arithmetic carried through it -- so `msolve` with F4 and
      multi-modular arithmetic does not reach `n = 29` on this hardware, and the reason is
      not the one the block was written expecting.

      Scope of the claim, which is narrower than "out of reach": this is a measurement on
      two threads and 15 GB, not a proof of intractability. It does not exclude a machine
      with more memory, a different order, or Magma. What it does establish is that the
      interval route carries the `n = 29` bound for a reason now measured rather than
      assumed, and that the next thing to try is a smaller ideal rather than a bigger
      computer -- the degree of the projection to the `s`-axis by homotopy continuation,
      which needs no basis at all.
  - id: BC-067
    purpose: tool_validation
    owner_focus: correctness
    instances: [11]
    state: ready
    priority: 1
    question: >-
      Can a recovered minimal polynomial be discharged all the way back to a verified
      packing, rather than only to an isolated root?
    hypotheses: []
    budget: 60 minutes
    entry: >-
      `promote/solve.discharge` proves irreducibility and isolates the root, and stops at
      the side. The promotion spec's phase 4 asks for the whole round trip.
    exit: >-
      A `NumberField` built from the candidate, every pose unknown solved exactly, the
      packing rebuilt and passed to `verify_packing` under `exact_sign`, and the
      reconstructed side compared against the input pose; or a typed statement of which
      step the field cannot support.
    bead: think-2q2c
    depends_on: [BC-060]
    workflows: [pipeline-improvement]
    next_evidence: >-
      Feasible now and not before: since BC-059 the n = 11 contact system has full rank
      34 of 34, so the pose is determined by the contacts and there is something to solve.
    note: >-
      Compare the reconstructed *side*, not merely validity. A wrong contact structure can
      yield a valid but suboptimal packing, which verification alone does not catch -- the
      spec names that trap and it is the reason this step is not just a second call to
      `verify_packing`.
  - id: BC-068
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 100]
    state: ready
    priority: 1
    question: >-
      Can the generated atlas SVG be made reproducible from its inputs alone?
    hypotheses: []
    budget: 60 minutes
    entry: >-
      D-359, open: `format_svg_number` renders a scalar at whatever precision it was last
      refined to, so `known-best-1-100.svg` carries 27 fractional digits in a fresh process
      and 50 once anything has refined the shared field.
    exit: >-
      A pinned emission precision, every stored SVG and PNG receipt regenerated against it,
      and the composite-PNG check passing for the reason it states rather than on test
      ordering; or a typed statement of which stored artifact cannot be regenerated.
    bead: think-mt4h
    depends_on: []
    workflows: [general-improvement]
    next_evidence: >-
      The detector is already written down:
      `pytest tests/test_promote_system.py tests/test_known_best_atlas.py -p no:randomly`
      fails on the composite receipt, and either module alone passes.
    note: >-
      This re-hashes every stored SVG and every PNG receipt in the repository, which is why
      it was left open rather than fixed inside a block about chirality. It is a
      regeneration and a review, and it needs its own block for exactly that reason.
  - id: BC-069
    purpose: tool_validation
    owner_focus: correctness
    instances: [5]
    state: ready
    priority: 1
    question: >-
      What is the one stationarity condition n = 5 still needs, in a form a solver accepts?
    hypotheses: []
    budget: 60 minutes
    entry: >-
      After BC-059's edge-edge repair, Göbel's n = 5 is the only retained size with a
      genuine shortfall: rank 15 of 16, `side_leak` `1.0e-16`, and no edge-edge contact for
      the repair to have touched.
    exit: >-
      A condition whose addition takes the n = 5 rank to 16 of 16 with the residual unmoved
      at the retained pose; or a typed statement of which formulation the contact graph
      resists.
    bead: think-864y
    depends_on: [BC-059]
    workflows: [pipeline-improvement]
    next_evidence: >-
      n = 5 is now the clean case rather than the odd one out. Its first-order condition
      already holds -- no contact-preserving motion changes the side -- so what is missing
      is a genuine closure and not another missing equation, which is what BC-059's repair
      established by elimination.
    note: >-
      `close` reports that one condition is needed and refuses to invent it. This block is
      allowed to derive one; it is not allowed to size one to make the counts meet, which
      is the failure BC-059 recorded as D-361.
  - id: BC-064
    purpose: tool_validation
    owner_focus: process
    instances: [5, 10, 11, 16, 29]
    state: ready
    priority: 0
    question: >-
      Does the whole record still hold at the endpoints after the continuation, and does
      run-002 describe the run that actually happened?
    hypotheses: []
    budget: 30 minutes, reserved and never borrowed from
    entry: The continuation blocks have reached terminal states, whatever those states are
    exit: >-
      A full strict `packing-validate` receipt, generated views regenerated, run-002
      extended to cover every session of this run with measured clocks, and a green PR.
    bead: think-c7oo
    depends_on: [BC-057]
    workflows: [process-review]
    next_evidence: >-
      The first endpoint check earned its place by failing: the logbook entry named
      `verified_upper_bound` and the consumer contract required it to say what it meant by
      it. A second one closes the continuation the same way.
    note: >-
      This run has already recorded one wrong reason for stopping early. The endpoint check
      is where that is caught, and it is reserved rather than optional for that reason.
---
# agenda-006 — four bounded overnight blocks

One unattended run, 2026-08-29, from about `03:10Z` to about `14:50Z`. The blocks are
sized so that an interruption costs one block rather than the night, and so that the
lane most likely to move a verified bound runs while the clock is longest.

## The schedule

| Block | Clock | Advances | Lane |
| --- | --- | --- | --- |
| `BC-052` | `03:10Z`, 150 min | BC-045, spec phases 1–2 | Interval certification |
| `BC-053` | `05:40Z`, 180 min | BC-045, spec phases 3–4 | Interval certification |
| `BC-054` | `08:40Z`, 180 min | BC-043, then BC-044 | Exact promotion |
| `BC-055` | `11:40Z`, 150 min | BC-051 and BC-049 | Efficiency and rigidity |
| `BC-056` | `14:10Z`, 40 min | — | Endpoint check |

Start times are nominal.
A block that finishes early starts the next one early; a block that overruns eats into
BC-055, which is placed last precisely because it can absorb that without cutting a
scientific commitment short.
No block may borrow from BC-056.

## The continuation schedule

That first stretch closed at `BC-056` and the run then resumed rather than ending: a
review of the commit timestamps showed it had misread its own clock by about a factor of
four and stopped with most of its budget unspent ([D-358](../../../defects.md)).
Measured from the commits, blocks 1–4 took **31, 42, 29 and 23 minutes** against
declared budgets of 150, 180, 180 and 40.

The continuation runs the promotion pipeline’s missing middle first, then efficiency and
research, with the endpoint check reserved and last.
Blocks 6–10 are closed; 11 onward are the remaining map.

| Block | Commitment | Clock | State |
| ---: | --- | --- | --- |
| 6 | `BC-057` — witness contract, checker, evidence entry | `05:10Z`, 45 min | complete, took 58 |
| 7 | `BC-058` — chirality in the pose model | `06:09Z`, 45 min | complete, took 46 |
| 8 | `BC-059` — the closure, which was a missing equation | `06:56Z`, 60 min | complete, took 29 |
| 9 | `BC-060` — exact solve under the frozen margin rule | `07:26Z`, 60 min | complete, took 31 |
| 10 | `BC-065` — rationalise the system, bound the degree | `08:02Z`, 45 min | complete, took 20 |
| 11 | `BC-066` — eliminate the five-unknown system | `08:30Z`, 90 min | ready |
| 12 | `BC-061` — exact LP over certified coefficients | `10:00Z`, 60 min | ready |
| 13 | `BC-069` — the one condition `n = 5` still needs | `11:00Z`, 60 min | ready |
| 14 | `BC-067` — close the round trip at `n = 11` | `12:00Z`, 60 min | ready |
| 15 | `BC-068` — pin the atlas SVG’s emission (D-359) | `13:00Z`, 60 min | ready |
| 16 | `BC-062` — reachability-scoped verification | `14:00Z`, 45 min | ready |
| 17 | `BC-063` — `n = 5` rigidity in the catalogue | `14:45Z`, 45 min | ready |
| 18 | `BC-064` — endpoint check and run close | `15:30Z`, 30 min | reserved |

`BC-066` is first because it is the only remaining block that can change what this run
concludes about `n = 29`: everything else improves the pipeline, and that one decides
whether the exact route reaches at all.
`BC-064` is reserved and may not be borrowed from, for the reason D-358 records.

**Read block boundaries from `date -u`, not from an estimate.** That is the practice
change D-358 bought, and it has caught a wrong estimate twice since.

## What every block owes, regardless of what it found

1. **Merge `origin/main` first**, from block 2 onward.
   Another agent is landing cleanups in parallel, and a block that starts from a stale
   base pays for it at the checkpoint rather than at the start.
2. **Run `tbd sync`**, so bead state is not the thing that drifts overnight.
3. **Commit, push, and update the PR.** A checkpoint that exists only in the working
   tree is not a checkpoint; the container is ephemeral.
4. **Run the fast gate** and leave it green, or leave the failure named.
5. **Record the result where it belongs** — an experiment for a measurement,
   `defects.yaml` for an actual error, the owning bead for work state — and never in
   this agenda, which holds the schedule and nothing else.

A negative or refused result satisfies these just as a positive one does.
The run has no target it is allowed to reach by loosening something.

## Why this order

The interval route is first because it is the only lane here that can move
`verified_upper_bound`, and because it is the one session-035 left declared and
unstarted. It is also the tractable half of the promotion problem: it certifies a root
without needing the minimal polynomial that X-004 could not find.

The exact route is third because it is genuinely independent — neither route unblocks
the other — and because its likeliest outcome is a typed refusal, which is worth having
but is not worth the longest clock.

The efficiency and rigidity lanes are last because they are the two that can be cut
short without leaving a scientific question half-answered.

## What this agenda does not own

Every scientific exit.
BC-045, BC-043, BC-044, BC-051 and BC-049 in
[agenda-005](agenda-005-symbolic-promotion-and-identity.md) own their criteria, and the
specs own their phase contracts.
This agenda owns when work starts, when it must stop, and what it must leave behind.

The accept rule is untouched, and the one clause that is a judgment rather than
arithmetic stays out of reach: an unattended runner may decline a marginal result and
may not accept one. Anything at `n = 29` that passes is recorded `unresolved` with
`needs_review: true`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
