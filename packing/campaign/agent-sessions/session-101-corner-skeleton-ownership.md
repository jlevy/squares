---
title: session-101 — corner-skeleton ownership at 96/25
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-101
  title: Corner-skeleton ownership at 96/25
  date: '2026-09-08'
  started_at: '2026-09-08T04:28:00Z'
  deadline_at: '2026-09-08T06:58:00Z'
  branch: claude/squares-n11-constraints-wl9atd
  goal: >-
    Decide Agenda 030's cell BC-293 (H-128): whether a valid D4-symmetric measure at side
    96/25 exists with T-018's four corner atoms, scaled by 384/381, at weight at least 3/20
    and total mass below 11 + 3/20, so that X-021's Corollary C.2 turns it into the theorem
    that every packing of eleven unit squares at 96/25 has four distinct squares containing
    the four corner atoms; record the price M(forced) - M(free) either way.
  workflow_phases:
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    commitment: BC-293
    bead: think-1136
    objective: >-
      Re-derive the ownership step exactly, build a lane-owned bounded column-generation
      driver on sqpack.fractional (an LP bound change, no geometry change), run it at 96/25
      seeded with T-018 scaled by 384/381 on the density-matched grids, decide every final
      measure with the exact eighth-turn sweep, and read the price on one site set.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 110
    started_at: '2026-09-08T04:28:00Z'
    deadline_at: '2026-09-08T06:18:00Z'
    expected_output: >-
      The session-101 section of results/agenda-030/lane-c-n10-transfer.md with every run's
      inputs, exact verdicts, the price, and the scripts in its appendix.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      The bounded LP does not converge inside its wall on the density-matched site set, or
      the exact sweep refuses every final measure on Condition 1, 3, 4 or 5.
    fallback: >-
      Publish the best unconverged mass with its site set and rows as the scoped
      obstruction, and leave the theorem conditional.
    outcome: OUTCOME_PLACEHOLDER
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-c-n10-transfer.md
    stop_reason: STOP_PLACEHOLDER
    next_action: >-
      Write the record, validate the records tier, commit on lane/bc-293-corner-skeleton.
  - workflow: documentation-pass
    focus: process
    recording: contemporaneous
    clock_role: finalization
    commitment: BC-293
    bead: think-1136
    objective: >-
      Write the result section and this record, run the records tier, commit; no research
      in this phase.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: The runs are terminal; what remains is the record and its validation.
    budget_minutes: 40
    started_at: '2026-09-08T06:18:00Z'
    deadline_at: '2026-09-08T06:58:00Z'
    expected_output: This record, the result section, one commit on the lane branch.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The lane clock ends before the records tier is green.
    fallback: Commit what is written and name the failing check in the report.
    outcome: FINAL_PLACEHOLDER
    evidence:
    - packing/campaign/agent-sessions/session-101-corner-skeleton-ownership.md
    stop_reason: The lane clock; nothing further is planned in this session.
    next_action: >-
      The coordinator disposes H-128 on the recorded verdict and decides whether the
      frozen obstruction needs an experiment id.
  primary_bead: think-1136
  status: stopped
  certification_pending: think-1136
  budget:
    wall_minutes: 150
    checkpoint_minutes: 30
    finalization_minutes: 40
  stop_conditions:
  - The 2.5 hour lane clock from 04:28Z; no extension.
  - A converged bounded run decided by the exact sweep, or the obstruction with the converged mass.
  - No identifier allocation, no registry, hypothesis, agenda or sqpack edit, no push.
  progress:
    metric: >-
      exactly verified mass of the least column-generation measure at 96/25 with the four
      corner atoms at weight at least 3/20, against the 11.15 criterion
    before: >-
      Unmeasured; H-128 registered on 2026-09-08 with the 3.85 free run at 11.23 unconverged
      as the only neighbour.
    after: AFTER_PLACEHOLDER
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-c-n10-transfer.md
  - packing/campaign/agent-sessions/session-101-corner-skeleton-ownership.md
  checks:
  - CHECKS_PLACEHOLDER
  stop_reason: >-
    The lane's bounded question is decided and recorded; the session stops at its clock
    without a full gate run, so certification is pending under think-1136, and no resource
    rollup exists for this lane's log yet.
  next_action: >-
    Under think-1136 the coordinator runs the certifying gate on the lane commit, attaches
    the resource rollup, and disposes H-128 on the recorded verdict.
---
# session-101 — corner-skeleton ownership at 96/25

The lane's result, with every input, every exact verdict and the scripts, is the
`Session-101` section of
[lane C's report](../series/series-000-smoke-and-calibration/results/agenda-030/lane-c-n10-transfer.md).
This record is the handoff: what was attempted, what came back, and what should happen
next.

SUMMARY_PLACEHOLDER

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
