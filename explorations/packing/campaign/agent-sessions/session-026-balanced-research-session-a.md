---
title: session-026 — balanced research program, session A
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-026
  title: Repair the pipeline and complete the first half of the balanced research program
  date: '2026-08-26'
  started_at: '2026-08-26T22:18:23-07:00'
  deadline_at: '2026-08-27T03:18:23-07:00'
  goal: >-
    Complete session A of agenda 003: restore a first-failure-safe validation pipeline,
    measure the unloaded iteration loop, run the bounded BC-029 basin mini-cycle, shape
    the target-free BC-030 full-cell control, and leave a terminal midpoint review that
    determines the second five-hour session without widening any scientific claim.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Complete BC-027 by reproducing the misleading-success failure, adding one mutation
      regression, and repairing first-failure propagation at the narrowest shared gate
      boundary.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-08-26T22:18:23-07:00'
    deadline_at: '2026-08-26T22:48:23-07:00'
    expected_output: >-
      A focused red-green regression proving that an early failed validation command
      yields a nonzero step and gate result without printing an unqualified success.
    validation_command: >-
      uv run --directory explorations/packing --frozen pytest -q
      tests/test_validation_cli.py
    kill_condition: >-
      Stop on less than 4 GiB free before dependency sync, a change outside the shared
      gate failure boundary, a test that does not reproduce the original shell path, or
      any proposal to weaken, skip, or relabel a required check.
    fallback: >-
      Preserve the exact failing command and minimized shell reproducer under think-c90t,
      leave BC-027 open, and assign the next slice to the smallest verified control-flow
      boundary.
    outcome: >-
      Confirmed that the deleted Bash gate carried the reported errexit defect, while
      PR 41's Python validator already stops its multi-command steps on the first raised
      subprocess failure. Added an end-to-end CLI regression and a durable negative
      control that mutates the current boundary to swallow the first error.
    evidence:
    - The focused regression passed and observed exit 17, a failed step, no later marker, and no all-pass line.
    - The mutation control failed the regression when `_commands` was changed to catch and continue, then reported one expected control fire.
    - All 29 validation CLI tests passed in 7.42 seconds.
    stop_reason: The promised first-failure regression and mutation proof are green, so the slice closed 25 minutes early.
    next_action: >-
      Integrate the independent audit, write the mutation regression first, and make the
      focused validation CLI suite green before selecting another BC-027 slice.
  - workflow: factual-review
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Independently disposition the historical shell mechanism against the current
      Python validator and decide whether any production change remains necessary.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      The focused regression and mutation control are green; the independent audit can
      now decide whether this is a retained regression for an already-fixed boundary or
      requires a production correction.
    budget_minutes: 10
    started_at: '2026-08-26T22:23:29-07:00'
    deadline_at: '2026-08-26T22:33:29-07:00'
    expected_output: >-
      A source-backed root cause, current-path comparison, and explicit production-code
      disposition for think-c90t.
    validation_command: >-
      bash -c 'set -euo pipefail; f() { false; echo later-command-ran; }; if (
      set -euo pipefail; f ); then echo ALL-CHECKS-PASSED; else echo FAILED; fi'
    kill_condition: >-
      Stop on any disagreement between the historical reproducer, deleted gate source,
      current subprocess exception path, or mutation result.
    fallback: >-
      Leave think-c90t open with the first contradictory source line and do not claim
      the migration fixed the defect.
    outcome: >-
      Accepted the independent root cause and classified the current boundary as already
      fixed by the Python migration. Recorded D-340 as a recurrence of D-163; no
      production-code change is warranted.
    evidence:
    - The historical Bash shape printed the later-command and all-pass lines and exited zero after `false`.
    - The deleted gate placed its `run_step` subshell directly in an `if` condition.
    - The current Python chain raises, stops, records failure, and returns nonzero at four explicit boundaries.
    stop_reason: The source, executable reproducer, current path, and mutation control agree, so the review closed in under two minutes.
    next_action: >-
      Replay the historical Bash semantic failure, compare it with `_run`, `_commands`,
      `_execute_step`, and `_render_text`, then close or return the bead to W7.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: process
    objective: >-
      Integrate D-340 and the new control into generated views, then run the smallest
      gate surface that exercises the full mutation catalogue, synopsis, and campaign
      record before closing BC-027.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      Independent review found no production correction beyond the already-landed
      Python migration, leaving only durable defect integration and proportional gate
      evidence.
    budget_minutes: 25
    started_at: '2026-08-26T22:24:57-07:00'
    deadline_at: '2026-08-26T22:49:57-07:00'
    expected_output: >-
      A rendered D-340 record, green full negative-control catalogue, green coordination
      checks, and a terminal disposition for think-c90t and BC-027.
    validation_command: >-
      uv run --directory explorations/packing --frozen packing-validate --only
      'negative controls' --only 'defect log' --only 'synopsis agrees' --only
      'campaign record' --jobs 2 --inner-jobs 1
    kill_condition: >-
      Stop on any negative control that does not fire, generated-view drift, session
      disagreement, or a validation result that can still print unqualified success
      after a failed selected step.
    fallback: >-
      Keep BC-027 and think-c90t open with the first named failing control and assign
      another bounded W7 slice instead of opening research.
    outcome: >-
      Integrated D-340, corrected the three synopsis aggregates its new defect changed,
      and passed the declared mutation, defect, synopsis, and campaign-record surface
      with no skips.
    evidence:
    - The first integration run made all 68 negative controls fire and correctly failed only on the three stale D-340 synopsis aggregates.
    - After correcting those counts, 323 schema-bound artifacts, the synopsis, defect view, ledger, all 29 validation CLI tests, Ruff, and formatting passed.
    - The clean four-step replay passed in 268.79 seconds; the negative-control catalogue consumed 268.79 seconds and each other step consumed at most 2.82 seconds.
    stop_reason: BC-027's exit criterion is met, so the pipeline phase closed before its deadline.
    next_action: >-
      Render and validate D-340, run the four-step integration surface, and close BC-027
      only if every selected step passes without a skip.
  - workflow: efficiency-loop
    recording: contemporaneous
    clock_role: work
    focus: efficiency
    objective: >-
      Inventory command, coordination, delegation, and repeated-gate cost; distinguish
      the mutation catalogue from the row-jet scientific critical path; and admit no
      optimization without a repayment case over the remaining agenda.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      BC-027 is green 82 minutes before its maximum agenda allocation, while the clean
      integration replay exposes a 268.79-second mutation-catalogue long pole and free
      space has fallen below the full-gate admission threshold.
    budget_minutes: 15
    started_at: '2026-08-26T22:38:16-07:00'
    deadline_at: '2026-08-26T22:53:16-07:00'
    expected_output: >-
      A measured no-change or one bounded optimization decision with repayment
      arithmetic, plus a cheaper focused-check route for subsequent slices.
    validation_command: >-
      uv run --directory explorations/packing --frozen packing-validate --list
    kill_condition: >-
      Stop before implementation unless a profile names the hot path, equivalence is
      guarded, and expected savings in the remaining agenda exceed build and validation
      cost; do not run a full gate below 4 GiB free.
    fallback: >-
      Record the measurement, use the one-control selector after local control edits,
      and reserve the full catalogue for coherent integration checkpoints.
    outcome: >-
      Rejected a performance implementation for this checkpoint. The full mutation
      catalogue is a distinct integration cost, CI wait is passive coordination, and
      exact row-jet reuse cannot repay its required benchmark and build cost within the
      expected remaining invocations.
    evidence:
    - The clean replay spent 268.79 seconds in all 68 mutation controls; the one-control selector takes about two seconds and is the appropriate edit-loop check.
    - The retained exact profile attributes 54.00 seconds to row jets inside a 212.53-second exact group and predicts 167.53 to 182.53 seconds saved per complete invocation.
    - Three cold plus five warm acceptance runs and one implementation slice cost about 33 to 44 minutes, requiring about 11 to 16 future whole-group invocations to break even; the remaining agenda predicts two to four.
    stop_reason: The repayment trigger fails, so W5 closed without code changes in under two minutes.
    next_action: >-
      Integrate the independent W5 timing audit, price recurrence over the remaining
      agenda, and either reject implementation or freeze one bounded performance slice.
  - workflow: insight-iteration
    recording: contemporaneous
    clock_role: work
    focus: insight
    objective: >-
      Re-screen exp-044 and shape exp-045's precise mechanism, falsifier, information
      value, and smallest admissible frozen criterion before any target implementation
      or measurement.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      BC-027 is green and the W5 repayment trigger failed, making the dependency-ready
      H-023 successor the highest-information scientific cell.
    budget_minutes: 20
    started_at: '2026-08-26T22:40:00-07:00'
    deadline_at: '2026-08-26T23:00:00-07:00'
    expected_output: >-
      One source-grounded exp-045 design decision that names the exact criterion,
      controls, scale routes, instrument gap, kill condition, and scoped information
      value without creating the experiment artifact yet.
    validation_command: >-
      uv run --directory explorations/packing --frozen packing-ledger check
    kill_condition: >-
      Stop if the proposed criterion depends on unbuilt production rows, an undefined
      scale route, a changed H-023 claim, whole-component inference, or target geometry.
    fallback: >-
      Record the first missing instrument contract and return the line to W7 without a
      scientific round or verdict.
    outcome: >-
      Shaped exp-045 as an exact determination over the six frozen owner models and
      fifteen owner-3 scale records, with explicit met, missed, validly undecided, and
      invalid routes. Corrected the proposed scope so implementation key equality does
      not claim mathematical branch completeness.
    evidence:
    - Three independent audits agree that the criterion is coherent for preregistration but the target instrument is not ready.
    - A validly undecided result maps to determination `no_progress` and verdict `unresolved`; an instrument failure maps to `invalid` and carries no scientific disposition.
    - The smallest post-registration slice is W7 scale-only proof data exercised first on the exp-036 positive control, not pure -W target measurement.
    stop_reason: The mechanism, falsifier, finite outcome map, and W7 handoff are explicit, so W3 closed in under six minutes.
    next_action: >-
      Integrate the independent exp-045 readiness audit, inspect the terminal exp-044
      handoff and retained controls, and either shape one W6 preregistration or name the
      exact W7 blocker.
  - workflow: research-loop
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Preregister exp-045 with the independently accepted criterion, exact scale keys,
      controls, refusal records, outcome mapping, budget, stop conditions, and W7
      handoff before changing the instrument or running the target.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      The W3 design and independent W2 review agree after narrowing the conclusion from
      every mathematical branch to the six frozen owner models and their justified
      scale inventory.
    budget_minutes: 30
    started_at: '2026-08-26T22:45:20-07:00'
    deadline_at: '2026-08-26T23:15:20-07:00'
    expected_output: >-
      A schema-valid in-progress exp-045 artifact whose frozen prose and machine fields
      permit the scale-only W7 slice but forbid target execution until the full
      instrument and post-change review are green.
    validation_command: >-
      uv run --directory explorations/packing --frozen softschema validate
      campaign/series/series-000-smoke-and-calibration/experiments/exp-045-h-023-n5-minus-w-scale-and-controls.md
      && uv run --directory explorations/packing --frozen packing-ledger check
    kill_condition: >-
      Stop on any sampled beta, copied cusp constant, claim of nonlinear branch
      completeness, missing scale or refusal key, coupled sign-symmetry verdict,
      executed target command or result data, or ambiguous invalid-versus-unresolved
      route.
    fallback: >-
      Keep exp-045 unregistered, record the first rejected clause under think-1s0h, and
      return to W3 or W7 without implementation or target data.
    outcome: >-
      Preregistered the six-case and fifteen-scale-route criterion with twelve typed
      production mutations, thirteen claim refusals, distinct scientific outcomes,
      and no target data. Independent review also removed two false preregistration
      states by permitting empty in-progress results and correcting offset-aware lease
      comparison.
    evidence:
    - Exp-045, H-023, BC-029, the generated ledger, and the synopsis agree while H-023 remains an open question with instrument_ready false.
    - The experiment retains no result before execution; every terminal experiment must retain at least one result.
    - All 28 campaign-contract tests pass, including the live -07:00 lease and terminal-result regressions.
    stop_reason: The frozen contract, independent review, schema, ledger, synopsis, and focused pipeline regressions pass, so preregistration closed before its deadline.
    next_action: >-
      Write and independently replay the exp-045 contract, then hand the accepted
      scale-only proof-data slice to W7 without running pure -W.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Build the smallest admitted exp-045 instrument slice: exact owner-3 scale proof
      data and five-route exhaustion, exercised first on the exp-036 positive control
      without editing the target driver or creating pure -W data.
    status: in_progress
    entered_by: evidence_checkpoint
    switch_reason: >-
      Exp-045 is preregistered and independently accepted, but its target is blocked on
      an exact scale helper and certificate.scale_exhaustion guard.
    budget_minutes: 30
    started_at: '2026-08-26T23:02:07-07:00'
    deadline_at: '2026-08-26T23:32:07-07:00'
    expected_output: >-
      `minus_w_scale.py` and focused tests retain the three-by-five route inventory,
      formal bounded coefficients, source-derived unbounded identities, and a real
      missing-handler failure before any target disposition exists.
    validation_command: >-
      uv run --directory explorations/packing --frozen pytest -q
      tests/test_minus_w_scale.py && uv run --directory explorations/packing --frozen
      ruff check cases/n5/minus_w_scale.py tests/test_minus_w_scale.py
    kill_condition: >-
      Stop on sampled beta, copied cusp constants, fewer or more than five scale keys
      per stratum, use of the exp-043 hand-formula driver, any pure -W target result,
      or the 30-minute boundary.
    fallback: >-
      Retain the first typed scale blocker and return BC-029 to W7 without changing the
      target driver or experiment results.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: >-
      Implement and test the scale proof-data boundary only, then obtain an independent
      post-change audit before opening the next instrument slice.
  primary_bead: think-whwc
  status: in_progress
  budget:
    wall_minutes: 300
    max_cycles: 30
    orientation_minutes: 10
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 30
  stop_conditions:
  - The absolute deadline 2026-08-27T03:18:23-07:00 is reached.
  - At 2026-08-27T02:48:23-07:00, stop target work and use only the finalization reserve.
  - No phase may run for more than 30 minutes without terminal evidence and a newly declared slice.
  - Dependency sync and full integration validation are not admitted below 4 GiB free space.
  - The atlas remains calibration-only, and abstract or local evidence cannot become geometry or packing feasibility.
  - No n=11 constructive target run begins before the contact-assembly grammar freezes.
  - Three consecutive guard refusals or crashes stop the affected line and require a typed pipeline result.
  progress:
    metric: agenda-003 session-A cells completed with replayable artifacts and terminal dispositions
    before: >-
      Session 025 and the merged PR are terminal, but BC-027 still lacks a mutation
      control for the validation gate's misleading first-failure behavior; no scientific
      agenda cell may start until that boundary is green.
    after: null
  delegations:
  - task: Independently audit the multi-command validation failure path and mutation boundary.
    operator: gate_failure_audit
    status: completed
    recording: contemporaneous
    outcome: >-
      Confirmed that `if ( set -euo pipefail; "$fn" )` suppressed errexit inside the
      historical step function and that the current Python chain fails at the first
      nonzero subprocess before rendering a nonzero summary.
    evidence:
    - The exact historical Bash shape runs the later command, prints the all-pass line, and exits zero.
    - Current `_run` raises on nonzero, `_commands` stops iteration, `_execute_step` records failure, and `_render_text` returns one without the all-pass line.
    files: []
    checks:
    - Read-only comparison of the deleted test.sh implementation with the current Python validator.
    uncertainty: No production gap remains unless the deleted Bash gate is reintroduced.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Coordinator will integrate the reported reproducer and narrowest fix after writing the failing regression.
    phase: 1
    budget_minutes: 20
    started_at: '2026-08-26T22:18:23-07:00'
    deadline_at: '2026-08-26T22:38:23-07:00'
    expected_output: Exact shell semantics, affected paths, and one minimal regression and repair recommendation.
    validation_command: rg -n "run_step|ALL CHECKS PASSED" explorations/packing
    kill_condition: Stop before editing files, changing beads, running strict validation, or crossing the active phase deadline.
    fallback: Return the closest confirmed failure boundary and remaining uncertainty without proposing a speculative patch.
    write_scope:
    - none (read-only audit)
    excluded_commands:
    - git commit
    - git push
    - tbd
    - gh
  - task: Price row-jet and mutation-catalogue optimization against the remaining agenda.
    operator: w5_timing_audit
    status: completed
    recording: contemporaneous
    outcome: >-
      Rejected implementation because the mandatory benchmark and build cost needs 11
      to 16 future exact-group invocations to repay, while the remaining agenda predicts
      only two to four.
    evidence:
    - The exact group is 212.53 seconds with 54.00 seconds in row jets; predicted reuse saves 167.53 to 182.53 seconds per complete invocation.
    - The full mutation catalogue is a separate integration surface, and CI waiting should overlap active research.
    files: []
    checks:
    - Read-only comparison of agenda-003, sessions 018 through 020 and 025, and think-kdil.
    uncertainty: Reconsider only if the frozen BC-029 plan schedules at least 11 comparable whole-group invocations.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Use focused sentinels during edits and reserve whole-group or full-catalogue checks for coherent integration checkpoints.
    phase: 4
    budget_minutes: 15
    started_at: '2026-08-26T22:38:16-07:00'
    deadline_at: '2026-08-26T22:53:16-07:00'
    expected_output: Measured repayment arithmetic and the cheapest safe check routing.
    validation_command: rg -n "active_row_jets|row-jet|negative controls" explorations/packing/campaign explorations/packing/tests
    kill_condition: Stop before proposing code without a measured critical path, guarded equivalence, and positive remaining-horizon repayment.
    fallback: Record a no-change W5 decision and continue to BC-029.
    write_scope:
    - none (read-only audit)
    excluded_commands:
    - git commit
    - git push
    - tbd
    - gh
  - task: Reconcile stale and overlapping research owners from the startup queue.
    operator: ownership_reconcile
    status: completed
    recording: contemporaneous
    outcome: >-
      Identified one completed H-010 owner, three directional duplicates, and one broad
      quench bead whose discharged NumberField clause should be removed while its live
      fixed-angle and stationarity work remains open.
    evidence:
    - Exp-016 terminally rejects H-010's printed-set conjunction, while H-041 remains a source-distinct repair.
    - Durable specs assign the certificate, promotion, and fractional-transversal pairs to think-0md2, think-75ll, and think-28sq respectively.
    - D-053 and think-rsxe discharge NumberField preconditions; D-052 and coupled-direction semantics remain open.
    files: []
    checks:
    - Read-only comparison of the five bead pairs against their retained experiments, hypotheses, specs, synopsis, code, and tests.
    uncertainty: The n=17 promotion control must permit a typed failure rather than promise exact recovery from its numerical witness.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Coordinator will apply the directional duplicate closures and narrow think-zcx4 without merging distinct scientific work.
    phase: 3
  - task: Audit exp-045 preregistration and instrument readiness.
    operator: exp045_readiness
    status: completed
    recording: contemporaneous
    outcome: >-
      Accepted BC-029 for preregistration and a scale-only W7 slice, while rejecting
      target measurement until the full driver, controls, refusals, and post-change
      review exist.
    evidence:
    - The accepted row, stress, and sheet helpers exist; the scale helper, target driver replacement, twelve-control driver, and thirteen refusal records do not.
    - The exact five-key owner-3 inventory yields fifteen records across A, interior, and B.
    files: []
    checks:
    - Read-only comparison of H-023, exp-043, exp-044, session 016, schema, source helpers, and focused tests.
    uncertainty: H-023 remains an open question with an unready bidirectional-continuation instrument after any local exp-045 result.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Preregister exp-045, then build only scale proof data on the positive control before target work.
    phase: 5
  - task: Audit the exp-045 implementation boundary and production mutation seams.
    operator: exp045_instrument_audit
    status: completed
    recording: contemporaneous
    outcome: >-
      Classified exp-045 as W7 instrumentation before W6 target work and mapped the
      scale helper plus every remaining driver, mutation, refusal, and replay seam.
    evidence:
    - The existing 601-line obstruction driver is the inadmissible exp-043 hand-formula path and cannot be incrementally blessed.
    - The smallest retained implementation is `minus_w_scale.py` plus focused tests, run first on the exp-036 positive control.
    files: []
    checks:
    - Read-only file-level audit of the row-jet, stress, sheet, obstruction, and test surfaces.
    uncertainty: W6 becomes admissible only after scale and guard instrumentation passes focused controls and independent post-change review.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Keep the target driver and result JSON closed during the scale-only W7 slice.
    phase: 5
  - task: Independently review the exp-045 determination criterion and claim boundary.
    operator: exp045_independent_criterion
    status: completed
    recording: contemporaneous
    outcome: >-
      Accepted the criterion after narrowing its conclusion to both frozen owner models
      and their justified scale inventory rather than claiming mathematical branch
      completeness.
    evidence:
    - Exact key equality establishes implementation coverage, not completeness of the true nonlinear branches.
    - Met, missed, no-progress unresolved, invalid, and dependency-blocked outcomes remain distinct.
    files: []
    checks:
    - Independent read-only criterion review against H-023, exp-042 through exp-044, session 016, the runbook, and the experiment schema.
    uncertainty: Even criterion_met remains local to canonical pure -W at the three registered poses under the justified inventory.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Freeze the corrected wording and all twelve mutations and thirteen refusals in exp-045 before implementation.
    phase: 5
  - task: Independently audit the written exp-045 record and its pipeline semantics.
    operator: exp045_record_review
    status: completed
    recording: contemporaneous
    outcome: >-
      Accepted the scientific scope after requiring honest empty in-progress results,
      UTC-normalized lease comparison, and explicit owner-4 correction cancellation.
    evidence:
    - The first draft falsely recorded invalid and no-progress determinations before any target or guard executed.
    - A live -07:00 lease reproduced a seven-hour early-expiry defect in the ledger.
    - The six-case criterion, five-route scale inventory, controls, refusals, and H-023 claim boundary otherwise align.
    files: []
    checks:
    - Read-only review of exp-045, H-023, exp-044, BC-029, session 026, the schema, ledger, and generated synopsis.
    uncertainty: The target remains blocked until every remaining production guard and post-change review passes.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Run the scale-only W7 slice and keep results empty.
    phase: 6
  outputs:
  - campaign/agent-sessions/session-026-balanced-research-session-a.md
  checks:
  - Session launch had 4.8 GiB physical free space, above the frozen 4 GiB admission threshold.
  - Session 025 is terminal and the generated ledger records it as completed.
  stop_reason: null
  next_action: >-
    Under BC-029, think-whwc, and think-1s0h, build and independently review only the
    exp-045 scale proof-data boundary; do not run the pure -W target.
---
# Session 026 — Balanced Research Program, Session A

This is the first five-hour source session in agenda 003’s ten-hour program.
Each row below is a maximum allocation, not a quota.
A slice closes as soon as it produces its promised evidence, and no continuation crosses
30 minutes without a fresh inventory.

## Bounded Slot Plan

| Maximum run time | Workflow | Objective | Evidence boundary | Defer or kill rule |
| --- | --- | --- | --- | --- |
| 0:00–1:45 | W7, W2 | Complete BC-027 in 10–30-minute slices | Mutation failure, focused green control, smallest integration check | Do not open W6 while the gate can report false success |
| 1:45–2:00 | W5 | Measure unloaded command, coordination, and delegation time | One timing inventory with the longest command and repeated work | Do not optimize without a remaining-horizon repayment case |
| 2:00–3:45 | W3, W6, W2 | Shape, freeze, execute, replay, and interpret the BC-029 mini-cycle | Preregistered exp-045 criterion and retained guarded outcome | Invalid instrumentation returns to W7 and produces no scientific verdict |
| 3:45–4:00 | W5 | Compare throughput with the first inventory | Second timing inventory and prospective queue adjustment | At most two implementation substitutions across the ten-hour program |
| 4:00–4:30 | W1, W3 | Read and shape the target-free BC-030 control | Smallest complete label, cap, price vector, and falsifying mutations | Do not consult target geometry or start n=11 enumeration |
| 4:30–5:00 | Finalization | Terminalize session A and conduct the midpoint review | Regenerated views, proportional checks, push, bead sync, and exact Session B decision | Start no new target work after 02:48:23-07:00 |

The `n = 1..100` atlas remains calibration-only.
The 11,013 contact scaffolds are abstract and geometry-free.
Fixed-angle local realization is not packing feasibility, BC-010 pathwise results do not
prove whole-component identity, connectivity, or frequency, and the unattended numerical
runner remains **NO-GO**.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
