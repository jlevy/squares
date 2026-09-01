---
title: agenda-001 — basin-map confidence ladder
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-001
  title: Validate the basin stack before scaling genuine landscape research
  updated: '2026-09-01'
  status: active
  objective: >-
    Build confidence from exact and proved controls upward, distinguish failures of our
    tooling from facts about the packing landscape, and admit research cells only after
    the event, identity, and coverage layers they depend on have passed their own tests.
  items:
  - id: BC-001
    purpose: tool_validation
    owner_focus: correctness
    instances: [3]
    state: complete
    priority: 0
    question: >-
      Does the stack reproduce the exact n=3 optimal quotient and retain a complete,
      independently valid four-seed BasinEvent/v3 control block?
    hypotheses: [H-021, H-032]
    budget: completed in exp-014, exp-021, and exp-022
    entry: exact small-moduli checker and BasinEvent/v3 replay exist
    exit: >-
      Exact quotient is one interval; four of four events replay, 10,401 of 10,401
      fixed-point evaluations are settled, and no endpoint key is called a component.
    bead: think-wbra
    depends_on: []
    next_evidence: permanent replay in the focused and normal gates
    artifacts:
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-014-h-032-n3-optimal-moduli.md
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-021-h-021-n3-basin-event-v3.md
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-022-h-021-n3-basin-event-v3-completion.md
  - id: BC-002
    purpose: tool_validation
    owner_focus: correctness
    instances: [4]
    state: complete
    priority: 0
    question: >-
      Does the stack reproduce the exact n=4 optimum and retain four admissible events
      after the solver-boundary defect exposed by the first v3 block?
    hypotheses: [H-021, H-032]
    budget: completed in exp-015, exp-023, and exp-024; latest four-seed wall 16.97s
    entry: BC-001 complete and D-171 remedy preregistered
    exit: >-
      Exact quotient is one point; exp-023 preserves the failed control; exp-024 replays
      four of four events with 14,301 of 14,301 evaluations settled at proved side 2.
    bead: think-pwd0
    depends_on: [BC-001]
    next_evidence: full normal gate on engine f15d036 and durable exp-024 checkpoint
    artifacts:
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-015-h-032-n4-optimal-moduli.md
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-023-h-021-n4-basin-event-v3.md
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-024-h-021-n4-basin-event-v3-repair.md
  - id: BC-003
    purpose: tool_validation
    owner_focus: correctness
    instances: [5]
    state: complete
    priority: 0
    question: >-
      Under the unchanged v3 regime, can the first non-grid proved case retain four
      complete event receipts without censoring a solver or transition failure?
    hypotheses: [H-021]
    budget: four fixed seeds; 10s per quench; 60s command cap; one 30m agent slice
    entry: BC-002 committed, pushed, and green under the normal gate
    exit: >-
      Every start has an independently valid, balanced event or a typed retained stop.
      Any unsettled evaluation opens a defect and blocks all n=5 research scaling.
    bead: think-wbra
    depends_on: [BC-002]
    next_evidence: permanent semantic replay in the focused and normal gates
    parallel_group: event-calibration
    note: >-
      Exp-025 replays four of four admissible events with 14,219 of 14,219 fixed-point
      evaluations settled. Hitting the proved optimum was not the criterion.
    artifacts:
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-025-h-021-n5-basin-event-v3.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-025-h-021-n5-basin-event-v3.jsonl
  - id: BC-004
    purpose: tool_validation
    owner_focus: correctness
    instances: [6]
    state: complete
    priority: 1
    question: >-
      Does the same event contract remain complete at the first proved side-3 case, with
      every nonoptimal endpoint preserved rather than interpreted as a new component?
    hypotheses: [H-021]
    budget: four fixed seeds; 10s per quench; 90s command cap; one 30m agent slice
    entry: BC-003 exits without an open launch-path defect
    exit: four replayable events or one retained blocker; no component-count claim
    bead: think-wbra
    depends_on: [BC-003]
    next_evidence: permanent semantic replay of exp-026 and exp-027 in the focused and normal gates
    parallel_group: event-calibration
    note: >-
      Exp-026 retains three admissible events, then crashes before retaining seed 3's
      independent-validity failure. Exp-027 retains all four outcomes: three admissible
      side-3 events and one valid typed time-budget stop. D-183 is fixed; D-126 remains.
    artifacts:
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-026-h-021-n6-basin-event-v3.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-026-h-021-n6-basin-event-v3.jsonl
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-027-h-021-n6-basin-event-v3-retention.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-027-h-021-n6-basin-event-v3-retention.jsonl
  - id: BC-005
    purpose: tool_validation
    owner_focus: correctness
    instances: [7]
    state: complete
    priority: 1
    question: >-
      Does event generation, independent validity, and canonical-key computation remain
      stable one size beyond n=6 under the identical frozen regime?
    hypotheses: [H-021]
    budget: four fixed seeds; 10s per quench; 90s command cap; one 30m agent slice
    entry: BC-004 exits without an open launch-path defect
    exit: four replayable events or one retained blocker; exact costs recorded
    bead: think-wbra
    depends_on: [BC-004]
    next_evidence: permanent exp-028 replay and the n=3 through n=7 cost comparison
    parallel_group: event-calibration
    note: >-
      Exp-028 retains four valid events with 18,286 of 18,286 evaluations settled: one
      admissible endpoint and three typed time-budget stops. D-126 remains explicit.
    artifacts:
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-028-h-021-n7-basin-event-v3.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-028-h-021-n7-basin-event-v3.jsonl
  - id: BC-006
    purpose: tool_validation
    owner_focus: correctness
    instances: [8]
    state: complete
    priority: 1
    question: >-
      Does the basic event stack still close at the upper edge of H-021's intended
      small-n classifier range before any statistical census is attempted?
    hypotheses: [H-021]
    budget: four fixed seeds; 10s per quench; 120s command cap; one 30m agent slice
    entry: BC-005 exits without an open launch-path defect
    exit: four replayable events or one retained blocker; no unseen-mass inference
    bead: think-wbra
    depends_on: [BC-005]
    next_evidence: exp-029 plus event replay and a bounded quench/screen/key/replay timing audit
    parallel_group: event-calibration
    note: >-
      Exp-029 retains four independently valid events: one admissible side-3 endpoint,
      one typed unsettled cell-cycle stop, and two typed time-budget stops. Median
      four-event screen and key batches cost 0.000684s and 0.004956s; D-126 remains.
    artifacts:
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-029-h-021-n8-basin-event-v3.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-029-h-021-n8-basin-event-v3.jsonl
  - id: BC-007
    purpose: tool_validation
    owner_focus: efficiency
    instances: [9]
    state: complete
    priority: 2
    question: >-
      Can one proved perfect-grid cell traverse the full event and key path before the
      measured canonicalizer scaling makes broader sampling uneconomic?
    hypotheses: [H-021]
    budget: one seed first; 20s quench cap; 60s command cap; stop for profile if wall exceeds 30s
    entry: BC-006 complete and no unresolved validity defect
    exit: one replayable event with stage timings, or a profile-backed performance blocker
    bead: think-xzew
    depends_on: [BC-006]
    next_evidence: retained event plus canonicalization share of wall time
    parallel_group: performance
    note: >-
      Exp-030 retains one independently valid typed time-budget stop in 21.36s complete
      command wall, below the 30s profile trigger. Median one-event keying is 0.001074s;
      no additional n=9 sampling is authorized.
    artifacts:
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-030-h-021-n9-basin-event-v3.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-030-h-021-n9-basin-event-v3.jsonl
  - id: BC-008
    purpose: tool_validation
    owner_focus: correctness
    instances: [10]
    state: complete
    priority: 1
    question: >-
      Can the current event path start from a perturbation of the proved 45-degree
      optimum, return to it, and independently verify the full pose under v3?
    hypotheses: [H-002, H-021]
    budget: four preregistered perturbations; 15s each; 90s command cap
    entry: >-
      The source-bound `gobel10-svg-v1` entry point replays the retained published pose,
      deterministic perturbation, full start, and independent validity without changing
      the quench criterion.
    exit: proved-value return and complete receipts, or a typed retained failure
    bead: think-ouf0
    depends_on: [BC-003]
    next_evidence: permanent exp-031 semantic replay in the focused and normal gates
    parallel_group: known-answer-controls
    note: >-
      Exp-031 converges on all four declared source perturbations, independently validates
      every endpoint, settles all 6,631 evaluations, and returns within 2.221e-15 of the
      proved side. This validates a local known-answer control, not basin frequency.
    artifacts:
    - cases/gobel10/packing.py
    - cases/campaign_smoke/basin_events.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-031-h-002-n10-source-return.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-031-h-002-n10-source-return.jsonl
  - id: BC-009
    purpose: measurement_validation
    owner_focus: correctness
    instances: [3, 4]
    state: complete
    priority: 0
    question: >-
      Does a frozen terminal-component classifier recover the exact n=3 interval and
      exact n=4 point without equating endpoint keys, contact strata, or samples with
      connected components?
    hypotheses: [H-021, H-032]
    budget: completed in exp-032; 10 agent-minutes and 0.92 seconds generation plus replay
    entry: exact-model assignment and ambiguity-preserving fallback committed
    exit: >-
      Exact n=3 interval and n=4 point replay; seven key, stratum, sample, scope, and
      f64-assignment mutations fail; unsupported observations stay unresolved.
    bead: think-a2v6
    depends_on: [BC-001, BC-002]
    next_evidence: classifier contract, positive fixtures, and negative mutations
    parallel_group: identity
    artifacts:
    - cases/small_n/terminal_components.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-032-h-021-terminal-component-controls.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-032-h-021-terminal-component-controls.json
  - id: BC-010
    purpose: research
    owner_focus: insight
    instances: [5]
    state: ready
    priority: 0
    question: >-
      Are the equal-side n=5 candidates connected in the stationary set, and what
      verified minimax clearance connects unequal-side candidates?
    hypotheses: [H-023]
    budget: >-
      One final 90-minute block in three 30-minute cells. During 0--30, write and hash
      packing/cases/n5_transfer_gate/registration.yaml with the exact n = 5 fixture,
      matched n = 10 fixture, observable, pass threshold, and refusal conditions; no
      target output may be read first. During 30--60, execute the frozen n = 5
      discriminator. During 60--90, execute the identical observable at n = 10, record
      `transfer=passed` or `transfer=refused`, and apply the terminal transition below.
      No additional H-023 or local-geometry block is authorized by this commitment;
      only the already-declared BC-011 transfer-validation row may clear on a pass.
    entry: >-
      BC-003 and BC-009 complete; exp-033 binds the first declared pair to exact poses
      and exp-034 embeds its exact face in a two-parameter optimal sheet. The target run
      is inadmissible until the retained registration freezes both fixtures, the single
      observable, its threshold, and every premeasurement refusal condition.
    exit: >-
      Certified connection, certified separation bound, or explicit ambiguity interval
      for the declared n = 5 pair, plus a matched n = 10 transfer result or typed
      instrument refusal. An executed positive or negative result marks BC-010
      `complete`; a guard that fires before measurement marks it `stopped`. Close
      think-iivb in either case with a reason naming the scientific outcome—task closure
      is not scientific success. If transfer passes, mark BC-011 `ready` and remove the
      blocked hold from think-v3u5. If transfer is refused or BC-010 stops before
      measurement, mark BC-011 through BC-014 `stopped` and close their dedicated beads
      with the same stop reason. Leave H-023 unresolved but explicitly parked. The
      legacy think-1s0h remains the broader H-023 owner and must never be closed merely
      to clear an edge. On the refused or premeasurement-stop branch, however, the
      coordinator must place think-1s0h on `paused` hold with the same portfolio-stop
      reason; on the passing branch its status and hold remain independent of this
      chain.
    bead: think-iivb
    depends_on: [BC-003, BC-009]
    next_evidence: >-
      X-011 caps the lane after twelve rounds. The first cell must retain
      packing/cases/n5_transfer_gate/registration.yaml before reading any target output.
      It may select one final discriminator from -W, mixed-angle realization, or
      stationary continuation beyond the twelve exp-039 and six exp-042 paths, but must
      bind the exact n = 5 and n = 10 fixtures, one observable, one pass threshold, and
      every refusal condition in that file. Do not infer whole-polytope terminality from
      positive first-order stresses. The final AgentSession must record
      `transfer=passed` or `transfer=refused` and execute the agenda-and-tbd transition in
      `exit` before handoff.
    parallel_group: identity
    note: >-
      This is the first genuine basin-structure experiment in the ladder. Exp-033
      proves one exact fixed-angle optimal face, and exp-034 proves it lies in an exact
      two-parameter angle-and-slide sheet. Full nonsmooth stationary connectivity and
      unequal-side minimax clearance remain later bounded slices, so BC-010 stays ready
      rather than complete. After PR 19 merged, the campaign resumed on a fresh branch
      with a four-hour horizon. Pre-measurement review found D-194 and D-195 in the
      exp-035 candidate checker: one contact differential was reused across slide
      strata, and tied support rows were treated as alternatives. The corrected
      instrument is committed at `aa63cf4`; exp-035 froze the
      two-owner, tied-row-conjunction criterion before execution and then met it in
      0.28 wall-seconds. All three declared strata admit an exact non-sheet linearized
      direction. The post-run normal gate passes all 30 steps in 70 wall-seconds with
      all six exact small-n records replayed. Think-1582 is closed; think-imav owns the
      next bounded nonlinear-realization slice. Its independent instrument is committed
      at `f2d2e53`; exp-036 freezes exact owner-4 and owner-3 obstruction margins, source
      topology, six mutations, and separate 30-second generation and replay caps.
      Exp-036 meets that criterion in 0.21 external wall-seconds: exact owner-4 and
      owner-3 contradictions exclude exp-035's displayed direction from the true
      Bouligand tangent at all three strata. Exp-038 then certifies the complete
      branchwise linearization-cone inventory from engine commit `b8d0104`: the owner
      branches coincide, endpoint quotients have eight rays, the interior quotients have
      six, both face vectors are derived, and all ten controls pass. This is not local
      isolation; transverse and mixed nonlinear realization remains unclassified.
      Exp-039 then certifies the discovered connected five-dimensional fixed-angle
      cell-local LP-optimal position polytope from engine commit `27b999e`. Exact
      structural stresses cover twelve R1, R2, R3, and R6 paths, separate exact packing fixtures and
      ten controls pass, and D-256/D-257 preserve the proof shortcuts removed before the
      retained run. The rest of the polytope is not thereby stationary, so BC-010 remains
      ready.
      D-197 records and repairs the intervening shared-workspace branch race without
      adding a lease or worktree protocol. Think-imav and think-nm35 are complete:
      exp-038 supplied the remaining-cone inventory, and exp-039 supplied the twelve
      R1, R2, R3, and R6 paths. Think-1s0h now owns one preregistered exact R4/R5
      nonlinear-realization slice. Exp-040 stopped that first slice unresolved before
      retained measurement after independent review retained five finite proof-perimeter
      gaps; its rotating-path checker is a draft resume point, not an R4/R5 result. The
      first successor, exp-041, rejects its complete-zero-inventory criterion on the
      exact endpoint-only axis `0-3:owner3:a-`; the root does not refute path feasibility.
      Exp-042 accepts the corrected endpoint inventory and operationally separate
      feasibility and stress determinations from engine commit `2980fdc`: all six R4/R5
      cases and twenty semantic controls pass retained generation and replay. This is
      pathwise first-order evidence, not an exhaustive release-class result or
      stationary connection. Exp-043 stops its pure `-W` test before retained
      measurement on five exact instrument defects in rowwise second-order jets,
      weighted curvature, the sheet witness, and scale routing. Pure `-W`, mixed-angle,
      whole-stationary-component, and unequal-side-clearance questions remain later
      bounded slices. The following W7 phase adds a case-free exact-jet helper whose six
      tests bind the complete n=5 first-order row inventory, but it refuses branch,
      scale, and obstruction conclusions; exp-044 must preregister that case-level
      integration separately. Exp-044 now freezes the rowwise curvature, sheet-witness,
      scale-routing, disposition, control, and refusal criterion before the case draft
      changes. The repaired
      D-199/D-203 solver path no longer orders
      this scientific cell, and D-239 remains a separate W7 robustness line.
    artifacts:
    - cases/n5/equal_side_face.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-033-h-023-n5-equal-side-face.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-033-h-023-n5-equal-side-face.json
    - cases/n5/angle_sheet.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-034-h-023-n5-angle-sheet.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-034-h-023-n5-angle-sheet.json
    - cases/n5/tangent_cones.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-035-h-023-n5-tangent-cones.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-035-h-023-n5-tangent-cones.json
    - cases/n5/second_order_obstruction.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-036-h-023-n5-second-order-obstruction.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-036-h-023-n5-second-order-obstruction.json
    - cases/n5/tangent_inventory.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-038-h-023-n5-tangent-inventory.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-038-h-023-n5-tangent-inventory.json
    - cases/n5/fixed_angle_polytope.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-039-h-023-n5-fixed-angle-polytope.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-039-h-023-n5-fixed-angle-polytope.json
    - cases/n5/rotating_release_paths.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-040-h-023-n5-rotating-release-paths.md
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-041-h-023-n5-rotating-release-proof-perimeter.md
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-042-h-023-n5-endpoint-aware-rotating-paths.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-042-h-023-n5-endpoint-aware-rotating-paths.json
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-043-h-023-n5-minus-w-obstruction.md
    - cases/n5/minus_w_obstruction.py
    - src/sqpack/research/exact_jets.py
    - tests/test_exact_jets.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-044-h-023-n5-minus-w-row-jets.md
  - id: BC-011
    purpose: measurement_validation
    owner_focus: correctness
    instances: [5, 6, 7, 8]
    state: blocked
    priority: 1
    question: >-
      With n=5 ambiguity resolved or bounded, does the classifier leave at most five
      percent of sampled endpoint mass unresolved at each successive size?
    hypotheses: [H-021]
    budget: one fixed four-seed block per n first; expand only under a preregistered interval rule
    entry: BC-010 provides the first nontrivial identity control
    exit: >-
      Per-n unresolved fractions with 95% upper bounds. If every included cell meets
      the preregistered threshold, mark BC-011 `complete` with a passing result, mark
      BC-012 `ready`, and remove think-nbhe's blocked hold. At the first failed cell,
      mark BC-011 `complete` with a measured-negative result, mark BC-012 through
      BC-014 `stopped`, and close their dedicated tasks with the same stop reason.
    bead: think-v3u5
    depends_on: [BC-010]
    next_evidence: ambiguity-preserving classified event archive through the first failed or n=8 cell
    parallel_group: identity
    note: >-
      This dedicated task is held `blocked`. It may become ready only when BC-010 ends
      `complete` with a retained `transfer=passed` result and the coordinator removes
      that hold. If BC-010 takes its refusal transition, this row and BC-012 through
      BC-014 become `stopped` and their dedicated tasks close with the stop reason; they
      do not wait for or inherit another n = 5 task. A measured BC-011 failure also
      stops BC-012 through BC-014; task closure records the measured negative and does
      not turn it into a scientific pass.
  - id: BC-012
    purpose: research
    owner_focus: insight
    instances: [5, 6, 7, 8]
    state: blocked
    priority: 1
    question: >-
      Under fixed proposer, quench, and component relation, does estimated unseen
      component mass fall below 0.05 by n=8 and predict held-out discoveries?
    hypotheses: [H-007, H-011]
    budget: successive halving; start with two independent four-seed blocks per n
    entry: BC-011 passes every included n and the estimator is frozen before held-out data
    exit: >-
      The preregistered coverage interval passes, fails, or exhausts its tier-S budget.
      On a pass, mark BC-012 `complete` with a passing result, mark BC-013 `ready`, and
      remove think-3rv3's blocked hold. On failure or exhaustion, mark BC-012 `complete`
      with that measured outcome, mark BC-013 and BC-014 `stopped`, and close their
      dedicated tasks with the same reason.
    bead: think-nbhe
    depends_on: [BC-011]
    next_evidence: discovery curves, held-out predictions, uncertainty, and stop verdict
    parallel_group: census
    note: >-
      This dedicated task remains held `blocked` until BC-011 passes and the coordinator
      removes the hold. Stop with BC-011 when BC-010 records `transfer=refused`; only the
      successful transfer branch may clear the dependency chain. A completed BC-011
      row that records a failed cell does not pass this gate. If BC-012 itself fails or
      exhausts its budget, stop BC-013 and BC-014 rather than clearing them from task
      closure alone.
  - id: BC-013
    purpose: measurement_validation
    owner_focus: efficiency
    instances: [9, 10]
    state: blocked
    priority: 2
    question: >-
      Can the validated classifier and coverage loop scale past n=8 without
      canonicalization or quench cost dominating the information gained?
    hypotheses: [H-007, H-011]
    budget: one priced seed block at a time; stop when projected next block exceeds one 30m slice
    entry: >-
      BC-007 and BC-008 are complete, and BC-012 records a passing coverage result;
      BC-012 completion after failure or exhaustion does not pass this gate.
    exit: >-
      A measured viable extension or a profile-backed scale ceiling. On a viable
      extension, mark BC-013 `complete` with a passing result, mark BC-014 `ready`, and
      remove think-81mn's blocked hold. On a scale ceiling, mark BC-013 `complete` with
      that measured-negative result, mark BC-014 `stopped`, and close think-81mn with
      the same reason.
    bead: think-3rv3
    depends_on: [BC-007, BC-008, BC-012]
    next_evidence: component discoveries per wall-second and per pair-test with profile
    parallel_group: performance
    note: >-
      This dedicated task, rather than the shared performance bead think-xzew, owns the
      agenda gate and remains held `blocked` until BC-012 passes. Stop with BC-011 when
      BC-010 records `transfer=refused`, stop after a BC-011 classifier failure or
      BC-012 coverage failure/exhaustion, and do not infer authorization from task
      closure alone. A closed or paused n = 5 bead is not by itself authorization to
      scale this lane.
  - id: BC-014
    purpose: research
    owner_focus: insight
    instances: [11]
    state: blocked
    priority: 2
    question: >-
      What is the Trump record component's conditional attraction mass and which
      proposer most improves verified component discovery at matched cost?
    hypotheses: [H-004, H-012, H-013, H-029, H-031, H-040]
    budget: one preregistered strategy comparison at a time after an n=10 matched control
    entry: BC-013 passes and each proposer has a mechanism-matched control and pair-test budget
    exit: retained positive, negative, or exhausted strategy verdict; no record claim without exact promotion
    bead: think-81mn
    depends_on: [BC-013]
    next_evidence: paired component-level comparison with full poses and independent validity
    parallel_group: frontier-search
    note: >-
      This dedicated task remains held `blocked` until BC-013 passes and the coordinator
      removes the hold. Stop after BC-010 refusal, BC-011 classifier failure, BC-012
      coverage failure/exhaustion, or BC-013's profile-backed scale ceiling; a terminal
      predecessor is not necessarily a passing predecessor. The Trump search lane may
      be reconsidered later only under a new agenda with its own matched control.
  - id: BC-015
    purpose: tool_validation
    owner_focus: correctness
    instances: [12, 16, 17]
    state: complete
    priority: 1
    question: >-
      Do the standing cross-cell guards distinguish an open side-4 calibration, a proved
      not-below-4 validity guard, and an oblique mechanism-matched search calibration?
    hypotheses: [H-016, H-020]
    budget: permanent focused controls; rerun whenever a proposer or validity path changes
    entry: standing frontier artifacts and existing experiment controls
    exit: n=12 is never called a negative control; n=16 rejects below 4; n=17 failure stays strategy evidence
    bead: think-ouf0
    depends_on: []
    next_evidence: focused guard replay on every affected engine revision
    artifacts:
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-004-baseline-n12-negative-control.md
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-011-h-020-n17.md
---
# Basin-Map Confidence Ladder

This is the mutable priority surface for one series of experiment loops.
It is neither a second hypothesis registry nor an executable runner queue.
The hypotheses say what could be true, experiment artifacts say what was measured, beads
own unfinished work, and an escalated agent-session artifact owns the active outer clock
when durable supervision state is needed.
This agenda says which bounded commitment should be attempted next and why.

The three purposes prevent calibration from being mistaken for discovery:

- **Tool validation** asks whether the repository emits, retains, replays, and
  independently checks the facts it claims to measure.
  Finding a bug is a successful outcome for this purpose.
- **Measurement validation** asks whether component identity, ambiguity, or coverage is
  operationally recoverable on cases with known structure.
  Passing code is not enough; the measured object must agree with mathematical ground
  truth.
- **Research** asks a genuine question about the packing landscape.
  A research row is blocked until all validation rows it depends on are complete.

The current order is deliberately conservative: finish the event stack at `n = 5`, then
continue cheap event controls through `n = 8` while the independent identity lane uses
exact `n = 3,4` ground truth.
The first genuine basin question is the focused `n = 5` connectivity problem.
Statistical census work begins only after that relation is decidable or its ambiguity is
bounded.

“Complete” in this file means that the declared bounded commitment produced its promised
evidence. It never means that the full basin map is complete.
A complete basin-map claim requires a validated component relation and a preregistered
coverage bound in addition to valid terminal events.

Agents may take different `parallel_group` values concurrently.
They should not take two items from the same group without splitting seeds, artifacts,
and write ownership first.
At each checkpoint, update the item state and evidence here, the scientific verdict in
its experiment or hypothesis artifact, and the implementation status in its bead.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
