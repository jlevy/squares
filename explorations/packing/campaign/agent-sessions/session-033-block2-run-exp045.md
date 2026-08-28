---
title: session-033 — agenda-004 block 2, run exp-045
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-033
  title: Run exp-045 to a terminal H-023 disposition
  date: '2026-08-27'
  started_at: '2026-08-27T16:47:43-07:00'
  deadline_at: '2026-08-27T21:47:43-07:00'
  goal: >-
    Close BC-037 by running exp-045 through its declared record-and-replay command now
    that the admission gap is closed, and record whatever it returns without writing an
    accepting verdict this runner is not permitted to write.
  workflow_phases:
  - workflow: research-loop
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Re-check exp-045's remaining admission conditions, run its declared command, and
      record a terminal outcome: a valid result including a finite unresolved one, or a
      typed instrument blocker.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 105
    started_at: '2026-08-27T16:47:43-07:00'
    deadline_at: '2026-08-27T18:32:43-07:00'
    expected_output: >-
      A recorded exp-045 outcome with retained raw evidence and an independent replay, or
      the first typed blocker preventing an honest round.
    validation_command: >-
      uv run --directory explorations/packing --frozen pytest -q
      tests/test_minus_w_scale.py tests/test_minus_w_owner4.py
    kill_condition: >-
      Stop on writing an accepting verdict, which this runner may not do: a round passing
      clauses one through four is recorded `unresolved` with `needs_review` and waits for
      a human. Also stop on relaxing any admission condition to make the run possible, on
      an H-023 disposition the run did not measure, on whole-component identity or
      connectivity language, or on editing the frontier to match a result.
    fallback: >-
      Retain the first typed blocker under think-1s0h, leave exp-045 in-progress with its
      lease held by the running branch, and enter no disposition.
    outcome: >-
      exp-045 ran and is terminal. Both declared determinations report `criterion_met`:
      canonical pure -W is excluded at A, the interior, and B, and the -W coefficients
      equal the separately derived +W values. The round is recorded `unresolved` with
      `needs_review` rather than accepted, because this runner may apply the accept rule
      only in the conservative direction and because the sixth admission condition, an
      independent post-change audit, has not been performed.
    evidence:
    - 'Record and replay both returned `{"status": "PASS", "cases": 6, "controls": 12}`, and they agree: the replay path raises `replay.drift` when the retained result differs from a regeneration, and it did not fire. That satisfies admission condition five.'
    - Twelve production mutation paths and thirteen individually keyed refusals are present in the retained artifact, so conditions three and four hold in the recorded data and not only in the source.
    - 'Every broader claim stayed refused: no whole-component identity, no A-to-B stationary connection, no local isolation, no terminality, and no H-023 disposition beyond the excluded direction.'
    - 'A stale hardcoded literal was found and fixed in the same slice: `main` printed `"controls": 8` in its summary while the recorded data carried the correct twelve. The summary now derives both counts from the result, so it cannot drift from the artifact again.'
    - 'Measured cost is 6.64 wall seconds for the replay; the round is recorded with `stopped_by: criterion`.'
    stop_reason: >-
      The measurement answered its declared question in both determinations, and the only
      remaining admission condition is a review this runner cannot perform on its own
      work.
    next_action: >-
      A human accept decision is required. exp-045 sits `unresolved` with `needs_review`,
      and an independent post-change audit of the complete instrument is the sixth
      admission condition still outstanding. Nothing downstream should treat the
      obstruction result as accepted until both are resolved.
  - workflow: insight-iteration
    recording: contemporaneous
    clock_role: work
    focus: insight
    objective: >-
      Give exp-045's valid result the immediate W3 mechanism pass BC-037's exit requires:
      state what the excluded direction changes about the n=5 terminal-family question and
      what the successor disposition is, without widening any refused claim.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      BC-037's exit requires that every valid exp-045 result receives an immediate W3
      mechanism pass, and the round returned a valid unresolved result rather than an
      invalid instrument.
    budget_minutes: 20
    started_at: '2026-08-27T16:52:25-07:00'
    deadline_at: '2026-08-27T17:12:25-07:00'
    expected_output: >-
      One mechanism reading bounded by the thirteen retained refusals, and a named
      successor direction or a typed reason none is available.
    validation_command: >-
      uv run --directory explorations/packing --frozen packing-ledger check
    kill_condition: >-
      Stop on any statement the retained refusal set excludes, in particular whole-component
      identity, an A-to-B stationary connection, local isolation, terminality, or an H-023
      disposition; and on treating an unaccepted round as accepted.
    fallback: >-
      Record that the excluded direction changes nothing reportable and leave H-023 exactly
      as it stands.
    outcome: >-
      One candidate escape direction is closed and nothing else moves. Canonical pure -W is
      excluded at all three strata, so the finite unresolved obstruction exp-044 left is
      narrower by exactly that direction. H-023's status is unchanged: the connectivity
      question it asks is explicitly among the thirteen refusals this round retained.
    evidence:
    - The result excludes canonical pure -W at A, the interior, and B, and confirms the -W coefficients equal the separately derived +W values through the same production builder.
    - 'The refusal set bounds the reading precisely: `A_to_B_stationary_connection`, `whole_stationary_component`, `local_isolation`, `terminality` and `whole_polytope_classification` are all retained as refused, so no connectivity or component claim follows.'
    - '`minus_W_obstruction_from_candidate_failure` is itself refused, so the exclusion may not be read backwards as evidence that a candidate failed for this reason.'
    - 'The named successor directions are the ones the refusal set still holds open as unexamined rather than excluded: `Ri_plus_lambda_W_plus_s`, `other_mixed_direction` and `other_transverse_direction`. Those are the next candidate routes, and none has an instrument yet.'
    stop_reason: >-
      The mechanism reading is complete and bounded by the retained refusals, and the
      successor directions are named without an instrument being promised for them.
    next_action: >-
      Under BC-035 and think-cja6, run block three. exp-045's acceptance waits on an
      independent audit and a human decision, and the mixed and transverse directions have
      no instrument, so neither is a slice this block can open.
  primary_bead: think-1s0h
  status: completed
  budget:
    wall_minutes: 300
    slice_minutes: 105
    orientation_minutes: 15
    finalization_minutes: 30
  stop_conditions:
  - No accepting verdict is written by this runner; conservative direction only.
  - No admission condition is relaxed to make the run possible.
  - The full gate must be green before the block boundary closes.
  - A quota or API failure halts the run; it is not retried on a timer.
  progress:
    metric: exp-045 terminal disposition under H-023
    before: >-
      Block one closed the admission gap: twelve mutations are enforced on twelve distinct
      identifiers, so conditions three and four hold. Conditions five and six, generation
      and replay agreeing and an independent post-change audit, remain untested.
    after: >-
      exp-045 is terminal at `unresolved` with `needs_review`. Both determinations report
      criterion_met and record-and-replay agree, so condition five is satisfied; condition
      six, the independent post-change audit, is the one thing still outstanding and is
      not something this runner can perform on its own work. The campaign gains its first
      executed research round in several sessions, and it gains it without any runner
      writing an acceptance.
  delegations: []
  outputs:
  - campaign/agent-sessions/session-033-block2-run-exp045.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-045-h-023-n5-minus-w-scale-and-controls.md
  - campaign/series/series-000-smoke-and-calibration/results/exp-045-h-023-n5-minus-w-scale-and-controls.json
  - cases/n5/minus_w_obstruction.py
  checks:
  - The full gate passed all steps at caffcc3 immediately before this session opened.
  - exp-045's lease names the previous branch and is reclaimed onto the running branch before any run.
  stop_reason: >-
    The round executed to a terminal outcome inside its slice, and the remaining step is a
    human judgment this runner is structurally barred from making.
  next_action: >-
    Under BC-035 and think-cja6, run block three's pipeline guard consolidation while
    exp-045's acceptance waits on an independent audit and a human accept decision.
---
# Session 033 — Agenda-004 Block 2

Block one closed exp-045’s admission gap.
This block runs the experiment itself, which is the first genuine research round the
campaign has reached in several sessions.

The campaign’s unattended-runner rule governs the ending: the harness cannot write the
accepting verdict, and a round passing clauses one through four is recorded `unresolved`
with `needs_review` and waits for a human.
So this session can produce evidence and a disposition request, but not an acceptance.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
