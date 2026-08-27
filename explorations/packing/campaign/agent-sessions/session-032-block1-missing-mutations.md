---
title: session-032 — agenda-004 block 1, build the missing mutations
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-032
  title: Build exp-045's four missing pre-certificate mutations
  date: '2026-08-27'
  started_at: '2026-08-27T15:05:52-07:00'
  deadline_at: '2026-08-27T20:05:52-07:00'
  goal: >-
    Close BC-036 by raising the enforced pre-certificate mutation count from eight to the
    declared twelve, each new control exercising a proof invariant no existing mutation
    reaches, and without weakening any frozen criterion.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Extend the `ProofInputs` mutation surface so four currently unreachable proof
      invariants each become reachable by one declared perturbation, and raise the
      enforced control count to twelve.
    status: in_progress
    entered_by: session_start
    switch_reason: null
    budget_minutes: 60
    started_at: '2026-08-27T15:05:52-07:00'
    deadline_at: '2026-08-27T16:05:52-07:00'
    expected_output: >-
      Twelve keyed mutations, each mapping to a distinct expected failure identifier, with
      the count guard raised from eight to twelve and exp-045's admission re-checked.
    validation_command: >-
      uv run --directory explorations/packing --frozen pytest -q
      tests/test_minus_w_scale.py tests/test_minus_w_owner4.py
    kill_condition: >-
      Stop on amending exp-045's declared twelve down to the implemented count, on a
      mutation whose expected failure identifier duplicates one already covered, on
      targeting `control.keys` or `control.identifiers` (which guard the mutation
      machinery itself and would be circular), on weakening any frozen criterion, or on
      generating target data.
    fallback: >-
      Retain whichever mutations are built with their exact coverage, leave the enforced
      count at its true value, and record the first invariant that cannot be reached by a
      declared perturbation.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: >-
      Add one `ProofInputs` field per new control, wire each to its expected failure
      identifier, raise the count guard, and confirm every mutation still fails for its
      own declared reason rather than an incidental one.
  primary_bead: think-oyn9
  status: in_progress
  budget:
    wall_minutes: 300
    slice_minutes: 60
    orientation_minutes: 15
    finalization_minutes: 30
  stop_conditions:
  - The declared twelve is never amended downward to match what was built.
  - No mutation may share an expected failure identifier with another.
  - The full gate must be green before the block boundary closes.
  - A quota or API failure halts the run; it is not retried on a timer.
  progress:
    metric: enforced pre-certificate mutation count against exp-045's declared twelve
    before: >-
      Eight mutations are implemented and hard-enforced against a declared twelve, and
      BC-029 is blocked at execution admission because of the gap.
    after: null
  delegations: []
  outputs: []
  checks:
  - >-
    Orientation inventory before declaring this slice: the proof core raises 17 distinct
    failure identifiers and exactly 8 are exercised by mutations. Of the 9 uncovered,
    `control.keys` and `control.identifiers` guard the mutation machinery itself and
    cannot be mutation targets without circularity, leaving seven genuine candidates:
    `source.geometry`, `source.first_order`, `certificate.acceleration_elimination`,
    `baseline.obstruction`, `scope.refusal_set`, `source.replay` and `replay.drift`.
  - >-
    That retires BC-036's declared risk. The four required controls exist to be built, so
    exp-045's twelve was not aspirational and no preregistration amendment is warranted.
  - 'The mutation surface is narrow by construction: `ProofInputs` carries exactly eight fields, one per existing control, so each new control needs one new field.'
  stop_reason: null
  next_action: >-
    Under BC-036 and think-oyn9, build four of the seven candidate controls and raise the
    enforced count to twelve.
---
# Session 032 — Agenda-004 Block 1

The first block of the
[blocked agenda-004](../agendas/agenda-004-guard-repair-and-instrument-unblock.md) leads
with BC-036 because it is both the gate and the largest binary unknown: if four
genuinely distinct pre-certificate failure modes could not be defined, BC-037 and BC-038
would never run.

The orientation inventory settles that in the conservative direction.
Seven uncovered proof invariants exist, four are needed, and the two that cannot be used
are excluded for a stated reason rather than overlooked.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
