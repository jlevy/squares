---
title: session-029 — finish the agenda-003 research cycles
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-029
  title: Close the remaining agenda-003 cycles on strict per-workflow budgets
  date: '2026-08-27'
  started_at: '2026-08-27T10:17:12-07:00'
  deadline_at: '2026-08-27T13:47:12-07:00'
  goal: >-
    Decide BC-028 by measurement, answer the preregistered Q-BC032-a under BC-032, and
    advance or type-block BC-029, each inside its declared per-workflow budget, leaving
    the full gate green and every result on PR 48.
  workflow_phases:
  - workflow: efficiency-loop
    recording: contemporaneous
    clock_role: work
    focus: efficiency
    objective: >-
      Decide the BC-028 entry trigger by measuring whether the `exhaustive_exact` group
      spends more than sixty seconds with `active_row_jets` dominant, without
      implementing any optimization in this slice.
    status: stopped
    entered_by: session_start
    switch_reason: null
    budget_minutes: 15
    started_at: '2026-08-27T10:17:12-07:00'
    deadline_at: '2026-08-27T10:32:12-07:00'
    expected_output: >-
      One measured verdict with retained numbers: either the trigger passes and BC-028
      opens with checkpoint arithmetic for expected time saved, or the trigger fails and
      BC-028 closes for this agenda.
    validation_command: >-
      uv run --directory explorations/packing --frozen --all-extras --group dev pytest -m
      exhaustive_exact --collect-only -q
    kill_condition: >-
      Stop on implementing or committing any optimization in this slice, on a benchmark
      without a retained revision, on comparing runs across different machines or load
      states, or on accepting BC-028 without its declared five-fold, 45-second median and
      55-second p95 evidence.
    fallback: >-
      Retain the measurement and close BC-028 for this agenda rather than opening an
      implementation slice on a hypothesis the profile does not support.
    outcome: >-
      No measurement. The instrument attempt was killed after 11 minutes 45 seconds by a
      900-second command timeout that this slice imposed on itself. `cProfile` writes its
      output file only at interpreter exit, so a killed run yields nothing at all rather
      than a partial profile. The BC-028 trigger is therefore still undecided, and no
      optimization was implemented or considered.
    evidence:
    - The `exhaustive_exact` group collects 24 tests, not the 17 recorded in the 2026-08-25 efficiency review; the group has grown.
    - The group costs 295.13 seconds inside the green full gate, so the trigger's sixty-second half is already satisfied without profiling; only dominance was ever in question.
    - cProfile overhead on exact-algebra code pushed the run past 900 seconds, which is the measured instrument cost this slice discovered.
    - No pytest-xdist is configured, so a single process was profiled and the profile would have been valid had it been allowed to finish.
    stop_reason: >-
      The slice hit its own instrument cap rather than a research answer. Extending this
      phase silently would have hidden a fifteen-minute budget being wrong by more than
      twice, so it is stopped and re-declared with the cost now measured.
    next_action: >-
      Re-run the same profile without a command cap under a slice budgeted from the
      measured instrument cost, and decide the dominance trigger from its output.
  - workflow: efficiency-loop
    recording: contemporaneous
    clock_role: work
    focus: efficiency
    objective: >-
      Decide the BC-028 entry trigger from a completed profile of the `exhaustive_exact`
      group, measuring the `active_row_jets` share of cumulative time without
      implementing any optimization.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      The first slice measured the instrument cost instead of the target: a 900-second
      cap killed a profile that needs longer, and cProfile writes nothing when killed.
    budget_minutes: 30
    started_at: '2026-08-27T10:30:23-07:00'
    deadline_at: '2026-08-27T11:00:23-07:00'
    expected_output: >-
      One measured verdict with retained numbers: either `active_row_jets` dominates and
      BC-028 opens with checkpoint arithmetic, or it does not and BC-028 closes for this
      agenda.
    validation_command: >-
      uv run --directory explorations/packing --frozen --all-extras --group dev pytest -m
      exhaustive_exact --collect-only -q
    kill_condition: >-
      Stop on implementing or committing any optimization in this slice, on a benchmark
      without a retained revision, on comparing runs across different machines or load
      states, or on accepting BC-028 without its declared five-fold, 45-second median and
      55-second p95 evidence.
    fallback: >-
      Retain the measurement and close BC-028 for this agenda rather than opening an
      implementation slice on a hypothesis the profile does not support.
    outcome: >-
      The BC-028 trigger passes decisively, so the cell opens, but this slice implements
      nothing and recommends that the implementation follow exp-045 rather than precede
      it. `active_row_jets` holds 93.0 percent of the group's cumulative time from only
      47 calls, and the reuse mechanism the cell hypothesises already exists and already
      works: the same function costs 11.95 seconds per call on the dominant path and
      0.025 seconds per call inside the shared-inventory test. The dominant caller
      `evaluate_stress` is simply not wired to it.
    evidence:
    - The profiled group ran 24 tests in 753.9 seconds against 295.13 seconds gated, an overhead factor of 2.554; shares below are cumulative and the ungated figures are divided by that factor.
    - '`active_row_jets` cumulative is 701.3 seconds, 93.0 percent of the profile and about 274.5 seconds of the 295.13-second group, over 47 calls at 14.92 seconds each.'
    - '40 of those 47 calls arrive through `owner_row_jets`, whose own 50 calls cost 597.3 seconds at 11.95 seconds each.'
    - 'The single dominant arm is `minus_w_stress.evaluate_stress` -> `owner_row_jets`: 35 calls, 434.5 seconds cumulative, 57.6 percent of the group and about 170.1 seconds ungated.'
    - '`exact_jets.product` is the inner hot spot at 484.9 seconds cumulative over 57,164 calls.'
    - 'The execution-scoped shared row inventory added in session 026 already collapses this cost where it is used: inside `test_shared_row_inventory_is_exact_isolated_and_builds_once_per_stratum`, four `owner_row_jets` calls cost 0.1 seconds total.'
    - "This step is the whole gate's critical path: 295.13 of the full gate's 320.91-second wall, so a five-fold reduction on the `evaluate_stress` arm would remove about 136 seconds per run, roughly 42 percent of full-gate wall time."
    - Whether `evaluate_stress`'s 35 calls share a field identity and stratum is not decidable from a profile and remains the implementation slice's first obligation, under BC-028's exact-semantic-equality exit bar.
    stop_reason: >-
      The declared trigger is answered with retained numbers and a named target inside the
      slice budget, and the kill condition forbids implementing the optimization here.
    next_action: >-
      Do not open the BC-028 implementation slice yet. exp-045 is preregistered against a
      frozen instrument that runs through this exact path, so optimizing `evaluate_stress`
      first would break the campaign's own freeze discipline. Run BC-029 to a terminal
      exp-045 disposition, then implement the inventory reuse against an unfrozen path.
  - workflow: research-loop
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Answer the preregistered Q-BC032-a: decide whether the 4.94e-11 side relaxation in
      `E-n029-schadt-rational-upper` is a property of the retained Schadt pose or an
      artifact of `promote_rational`'s fixed dilation ladder at the default
      `rational_digits = 36`.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      BC-028 is decided by measurement and its implementation is deferred behind exp-045,
      so the cheapest remaining registered question runs next.
    budget_minutes: 30
    started_at: '2026-08-27T10:45:24-07:00'
    deadline_at: '2026-08-27T11:15:24-07:00'
    expected_output: >-
      One accept-rule verdict over the declared `rational_digits` set with every achieved
      exact side retained, or a typed instrument blocker.
    validation_command: >-
      uv run --directory explorations/packing --frozen python -m
      devtools.check_rational_witness_independent
      witnesses/schadt-n029-2025-rational.yaml
    kill_condition: >-
      Stop on treating decimal precision as a certificate, on any record-improvement,
      rigidity, or optimality language, on accepting a promoted witness the independent
      checker did not verify, on writing generated witnesses into `witnesses/`, or on
      widening the claim beyond an upper bound at a relaxed rational side.
    fallback: >-
      Retain the first typed promotion or checker blocker under think-75ll and leave
      `E-n029-schadt-rational-upper` exactly as recorded.
    outcome: >-
      Q-BC032-a is answered: the relaxation is route-dependent, and decisively so. Every
      one of the six verified promotions is strictly smaller than the recorded baseline,
      and the achieved relaxation tracks the promotion ladder's first rung exactly rather
      than any property of the pose. The recorded certificate's own metadata confirms the
      mechanism. This is a tool-validation result about `promote_rational`; it improves no
      record, certifies no source decimal, and establishes no rigidity or optimality.
    evidence:
    - 'The accept rule was met six times over: promotions at rational_digits 18, 24, 30, 36, 48 and 60 all produced independently verified 29-square witnesses whose exact side is strictly below 296694289993118242899906513/50000000000000000000000000.'
    - 'Achieved relaxation over the source decimal side tracks the rung 10^-(d-5) exactly: d=18 gives 4.933899e-13, d=24 gives 4.933965e-19, d=30 gives 4.933868e-25, d=36 gives 4.933884e-31, d=48 gives 4.933849e-43 and d=60 gives 4.933851e-55, against the recorded 4.9339e-11.'
    - "The recorded witness carries its own generation parameters and they match the prediction: `rational_digits: 16` and `center_dilation: 100000000001/100000000000`, which is the rung 1 + 1e-11 that the ladder reaches first at d = 16."
    - The recorded baseline was therefore never produced at the CLI default of 36; it was produced at 16, and the 4.94e-11 figure is that choice made visible rather than a cost the pose imposes.
    - 'd = 12 was refused, correctly and by the declared bound rather than by infeasibility: its first admissible rung is 1 + 1e-7, whose side increase exceeds the --max-side-increase 1/10000000000 declared before the run.'
    - Each promotion was checked by devtools.check_rational_witness_independent, which shares no geometry or verification code with the promoter, and every one reported VERIFIED over 29 squares and 406 pairs.
    - Every generated witness was written to scratch; no file under `witnesses/` was created or modified by this slice.
    stop_reason: >-
      The preregistered accept rule returned an unambiguous verdict on the first sweep,
      well inside the slice budget, and the declared falsifier was satisfied six times
      rather than once.
    next_action: >-
      Do not silently replace the durable artifact. Regenerating
      `E-n029-schadt-rational-upper` at a higher `rational_digits` is a change to recorded
      evidence and needs its own W7 slice with the gate, the evidence record and the
      certificate metadata updated together; it is tracked as think-uzmh. Note also that
      this route has no minimum: the relaxation shrinks without bound as `rational_digits`
      rises, so the honest quantity is the ladder's factor-of-one-hundred rung
      granularity, not a discovered optimum.
  - workflow: insight-iteration
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Decide whether exp-045's six declared execution-admission conditions actually hold,
      and either admit the pure minus-W target run under BC-029 or retain the first typed
      instrument blocker without weakening the admission bar.
    status: in_progress
    entered_by: planned_checkpoint
    switch_reason: >-
      BC-032's registered question is answered, so the agenda rotates to its one ready
      research cell.
    budget_minutes: 20
    started_at: '2026-08-27T10:48:10-07:00'
    deadline_at: '2026-08-27T11:08:10-07:00'
    expected_output: >-
      A condition-by-condition admission verdict citing the specific artifact or test that
      satisfies or fails each of the six declared prerequisites, and either an admitted
      target run or one typed blocker.
    validation_command: >-
      uv run --directory explorations/packing --frozen pytest -q
      tests/test_minus_w_scale.py tests/test_minus_w_owner4.py
    kill_condition: >-
      Stop on relaxing any admission condition to make the run possible, on generating
      target data from an incomplete instrument, on an H-023 disposition that the run did
      not measure, on whole-component identity or connectivity language, or on optimizing
      the shared row-jet path while the instrument is frozen.
    fallback: >-
      Retain the first unmet condition as a typed dependency blocker under think-1s0h and
      leave exp-045 preregistered and unexecuted.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: >-
      Check each of exp-045's six execution-admission conditions against the retained
      helpers, mutation controls, refusal records and replay path before admitting any
      target generation.
  primary_bead: think-kdil
  status: in_progress
  budget:
    wall_minutes: 210
    slice_minutes: 30
    orientation_minutes: 5
    finalization_minutes: 30
  stop_conditions:
  - No phase may run past its declared budget without terminal evidence and a newly declared slice.
  - No optimization is implemented in a measurement slice.
  - No scientific claim widens beyond what its instrument measured; instrument blockers are typed, not worked around.
  - The full gate must be green before the session is terminalized.
  - Every commit lands on `codex/packing-ten-hour-research-agenda` and reaches PR 48.
  progress:
    metric: agenda-003 cells closed by measurement or evidence rather than left ambiguous
    before: >-
      The full gate is green at 3421481. BC-029 is the only ready research cell, BC-028 is
      tentative pending its trigger measurement, BC-032 carries the newly preregistered
      Q-BC032-a, and BC-033 stays blocked on unmet prerequisites.
    after: null
  delegations: []
  outputs: []
  checks:
  - The full gate passed all 36 steps at 3421481 before this session opened.
  - The declared validation command was executed before being written into the contract, per think-ldy8.
  stop_reason: null
  next_action: >-
    Under BC-028 and think-kdil, measure the row-jet dominance trigger and record a
    verdict either way.
---
# Session 029 — Finish the agenda-003 Research Cycles

This session closes the remaining cells of the
[balanced ten-hour agenda](../agendas/agenda-003-balanced-ten-hour-research-program.md)
on strict per-workflow budgets rather than a wall clock.
It opens from a fully green gate, so any failure it observes is its own.

## Bounded Slot Plan

| Slot | Minutes | Workflow | Bead | Intent |
| --- | ---: | --- | --- | --- |
| 1 | 15 | W5 efficiency-loop | think-kdil | Decide the BC-028 row-jet dominance trigger by measurement. |
| 2 | 30 | W6 research-loop | think-75ll | Answer the preregistered Q-BC032-a against the existing independent checker. |
| 3 | 105 | W3-W6-W2-W3 | think-1s0h | Advance or type-block BC-029 through exp-045. |
| 4 | 30 | W2 factual-review | think-whwc | Reconcile views, run the full gate, and land everything on PR 48. |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
