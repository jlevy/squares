---
title: session-102 — angle-band theorems at 96/25
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-102
  title: Angle-band theorems at 96/25
  date: '2026-09-08'
  started_at: '2026-09-08T04:29:00Z'
  deadline_at: '2026-09-08T06:59:00Z'
  branch: claude/squares-n11-constraints-wl9atd
  goal: >-
    Lane BC-295 of Agenda 030 under H-130 and H-131: replay every planning-lane angle-count
    decision at 96/25 and U under a registered round with the exact verifier, widen the
    robust end band [0, α] ∪ [45° − β, 45°] excluded at 96/25 cell by cell until the exact
    decision fails or α + β reaches 3°, and record the angular support of the LP dual on the
    bands that stay at or above eleven.
  workflow_phases:
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: >-
      Replay the H-131 counts and the Section 2.3 end bands on the stated site set (grid 79,
      inset 1/10, the retained 181-direction net, B = 9977/10000) through
      decide_class_program; then widen the end band symmetrically and asymmetrically on the
      same site set; then read the dual's angular support where the value stays at or above
      eleven.
    commitment: BC-295
    bead: think-ndqj
    status: TBD_STATUS
    entered_by: session_start
    switch_reason: null
    budget_minutes: 120
    started_at: '2026-09-08T04:29:00Z'
    deadline_at: '2026-09-08T06:29:00Z'
    expected_output: >-
      A new section of results/agenda-030/lane-b-angle-classes.md with the replay table, the
      widening table, the histogram and the scripts; every verdict from decide_class_program.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      The exact verifier disagrees with a planning-lane mass on the same inputs, or the row
      loop cannot reach a decidable point on an end band within a hundred rounds.
    fallback: >-
      Publish the replay table alone with the disagreement named, and leave the widening as
      the next session's first task.
    outcome: TBD_OUTCOME
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-b-angle-classes.md
    stop_reason: TBD_PHASE_STOP
    next_action: TBD_PHASE_NEXT
  - workflow: documentation-pass
    focus: correctness
    recording: contemporaneous
    clock_role: finalization
    objective: >-
      Write the result section and this record, validate the records tier, and commit on the
      lane branch without pushing.
    commitment: BC-295
    bead: think-ndqj
    status: TBD_STATUS2
    entered_by: planned_checkpoint
    switch_reason: The research slice closed at its checkpoint; the remaining time is the finalization reserve.
    budget_minutes: 30
    started_at: 'TBD_P2_START'
    deadline_at: '2026-09-08T06:59:00Z'
    expected_output: The result section, this record, and one commit on lane/bc-295-angle-bands.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The deadline arrives before the records tier is green.
    fallback: Commit what is written with the failing step named in the checkpoint file.
    outcome: TBD_OUTCOME2
    evidence:
    - packing/campaign/agent-sessions/session-102-angle-band-theorems-at-q.md
    stop_reason: TBD_P2_STOP
    next_action: TBD_P2_NEXT
  primary_bead: think-ndqj
  status: stopped
  budget:
    wall_minutes: 150
    checkpoint_minutes: 30
    finalization_minutes: 30
  stop_conditions:
  - The 2.5-hour clock ends at 06:59Z; a promising result does not extend it.
  - Only decide_class_program and class_minima verdicts are results; a float optimum is context.
  - No identifier is allocated; a frozen claim is marked as needing an experiment id and left blank.
  - One worker on a machine shared with five other agents; wall times are not comparable with the planning lane's.
  progress:
    metric: exact-decided width α + β of the robust end band excluded at 96/25, and replayed counts
    before: 'α + β = 2.6937° (cells 0–5 ∪ 175–180, planning lane, unregistered); five H-131 counts decided in a planning lane only.'
    after: TBD_AFTER
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-b-angle-classes.md
  - packing/campaign/agent-sessions/session-102-angle-band-theorems-at-q.md
  checks:
  - TBD_CHECKS
  resource_rollups: TBD_ROLLUPS
  certification_pending: think-ndqj
  stop_reason: TBD_STOP
  next_action: TBD_NEXT
---
# Angle-Band Theorems at `96/25`

TBD_BODY

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
