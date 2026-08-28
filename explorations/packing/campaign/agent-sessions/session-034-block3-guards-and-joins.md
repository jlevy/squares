---
title: session-034 — agenda-004 block 3, guard and join consolidation
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-034
  title: Consolidate the pipeline guards and make the record-model joins checkable
  date: '2026-08-27'
  started_at: '2026-08-27T17:33:50-07:00'
  deadline_at: '2026-08-27T22:33:50-07:00'
  goal: >-
    Close BC-035 and BC-041 by repairing the guards that stopped guarding and by making
    the record model's unchecked joins machine-checkable, so the drift class that produced
    five separate incidents becomes a gate failure rather than an invisible one.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: process
    objective: >-
      Add an invariant that at most one commitment per bead may be `ready`, resolving the
      one live violation it exposes, and pin lefthook the way flowmark is pinned.
    status: in_progress
    entered_by: session_start
    switch_reason: null
    budget_minutes: 45
    started_at: '2026-08-27T17:33:50-07:00'
    deadline_at: '2026-08-27T18:18:50-07:00'
    expected_output: >-
      A checked invariant that rejects two simultaneously-ready commitments on one bead, a
      resolved `think-kdil` duplication, and a pinned lefthook install.
    validation_command: >-
      uv run --directory explorations/packing --frozen packing-ledger check
    kill_condition: >-
      Stop on an invariant that flags legitimate dependency chains, on resolving a
      duplication by deleting a commitment rather than dispositioning it, on pinning
      lefthook to a version not verified working here, or on editing a terminal record.
    fallback: >-
      Retain the measured violations and the proposed invariant shape without enforcing
      it, rather than enforcing a rule that produces false positives.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: >-
      Refine the invariant from at-most-one-live to at-most-one-ready, resolve the
      `think-kdil` duplication, then pin lefthook.
  primary_bead: think-cja6
  status: in_progress
  budget:
    wall_minutes: 300
    slice_minutes: 45
    orientation_minutes: 15
    finalization_minutes: 30
  stop_conditions:
  - No invariant is enforced that flags a legitimate dependency chain.
  - No terminal session record or archived artifact is rewritten.
  - The full gate runs in the background, never in a foreground command with a ten-minute limit.
  - A quota or API failure halts the run; it is not retried on a timer.
  progress:
    metric: guard and join defects closed or explicitly deferred with a reason
    before: >-
      Six items are open across BC-035 and BC-041. Three beads back more than one live
      commitment, one of them with two simultaneously ready. `npx lefthook install` is
      unpinned against a repository policy that pins flowmark for exactly that reason.
    after: null
  delegations: []
  outputs: []
  checks:
  - Blocks one and two both closed with a green full gate; exp-045 is terminal at `unresolved` with `needs_review`.
  - >-
    Read-only scoping refined the invariant before any code was written. At-most-one-live
    would flag `think-sfzh`'s BC-018 and BC-021, which are both blocked and form a
    legitimate dependency chain rather than an ambiguity. At-most-one-ready captures the
    real question, which is which commitment a runner should pick up, and leaves chains
    alone.
  - 'Under the refined rule exactly one violation exists: `think-kdil` backs BC-028 and BC-038, both `ready`.'
  - '`think-306i` is currently dormant: exp-045 going terminal makes all 45 rounds terminal, so the synopsis assertion it forces is true today and there is no failing case to verify a fix against.'
  stop_reason: null
  next_action: >-
    Under BC-035 and think-cja6, add the ready-uniqueness invariant and pin lefthook.
---
# Session 034 — Agenda-004 Block 3

Blocks one and two produced results.
This block pays the debt that made both of them noisier than they needed to be: five
separate drift incidents in one day, each invisible until something forced a check.

The scoping pass changed the shape of the main invariant before any code was written,
which is the cheapest possible moment to find that out.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
