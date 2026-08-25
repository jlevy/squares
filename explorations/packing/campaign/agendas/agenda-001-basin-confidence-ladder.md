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
  updated: '2026-08-24'
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
      The source-bound `gobel10-svg-v1` entry point replays the published pose, source
      digest, deterministic perturbation, full start, and independent validity without
      changing the quench criterion.
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
    - sqpack/packings/gobel10.py
    - tools/basin_census.py
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
      Exact n=3 interval and n=4 point replay; eight key, stratum, sample, scope,
      digest, and f64-assignment mutations fail; unsupported observations stay unresolved.
    bead: think-a2v6
    depends_on: [BC-001, BC-002]
    next_evidence: classifier contract, positive fixtures, and negative mutations
    parallel_group: identity
    artifacts:
    - tools/check_terminal_components.py
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
    budget: one 30m local-geometry slice per declared candidate pair; retain partial bounds
    entry: >-
      BC-003 and BC-009 complete; exp-033 binds the first declared pair to exact poses
      and exp-034 embeds its exact face in a two-parameter optimal sheet
    exit: certified connection, certified separation bound, or explicit ambiguity interval
    bead: think-1s0h
    depends_on: [BC-003, BC-009]
    next_evidence: >-
      enumerate the other wall-release and SAT-branch cone directions before attempting
      any further nonlinear continuation or local-isolation claim
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
      topology, seven mutations, and separate 30-second generation and replay caps.
      Exp-036 meets that criterion in 0.21 external wall-seconds: exact owner-4 and
      owner-3 contradictions exclude exp-035's displayed direction from the true
      Bouligand tangent at all three strata. This is not local isolation; other
      non-sheet directions remain unclassified. D-197 records and repairs the
      intervening shared-workspace branch race without adding a lease or worktree
      protocol. Think-imav is complete; think-nm35 owns the next remaining-cone slice.
      D-199's capped cumulative residual repair restores n=10 and all seven ladder rungs
      at `PACK_JOBS=10` and `PACK_JOBS=1`. Only n=4 seed 0 remains: a typed HiGHS
      status-4 Solve error under D-203 and `think-nr5w`. The committed golden is
      unchanged, and no further full-golden retry is authorized before the millisecond
      fixture is captured. The strict merge and handoff gate remains red.
    artifacts:
    - tools/check_n5_equal_side_face.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-033-h-023-n5-equal-side-face.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-033-h-023-n5-equal-side-face.json
    - tools/check_n5_angle_sheet.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-034-h-023-n5-angle-sheet.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-034-h-023-n5-angle-sheet.json
    - tools/check_n5_tangent_cones.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-035-h-023-n5-tangent-cones.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-035-h-023-n5-tangent-cones.json
    - tools/check_n5_second_order_obstruction.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-036-h-023-n5-second-order-obstruction.md
    - campaign/series/series-000-smoke-and-calibration/results/exp-036-h-023-n5-second-order-obstruction.json
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
    exit: per-n unresolved fractions with 95% upper bounds; stop at the first failed cell
    bead: think-0yo9
    depends_on: [BC-010]
    next_evidence: ambiguity-preserving classified event archive through the first failed or n=8 cell
    parallel_group: identity
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
    exit: preregistered coverage interval passes, fails, or exhausts its tier-S budget
    bead: think-ogv7
    depends_on: [BC-011]
    next_evidence: discovery curves, held-out predictions, uncertainty, and stop verdict
    parallel_group: census
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
    entry: BC-007, BC-008, and BC-012 complete
    exit: measured viable extension or a profile-backed scale ceiling
    bead: think-xzew
    depends_on: [BC-007, BC-008, BC-012]
    next_evidence: component discoveries per wall-second and per pair-test with profile
    parallel_group: performance
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
    bead: think-axbi
    depends_on: [BC-013]
    next_evidence: paired component-level comparison with full poses and independent validity
    parallel_group: frontier-search
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
own unfinished work, and the current agent-session artifact owns the active clock.
This agenda says which bounded cell should be attempted next and why.

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

“Complete” in this file means that the declared bounded cell produced its promised
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
