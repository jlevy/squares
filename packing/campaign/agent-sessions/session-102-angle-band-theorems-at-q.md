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
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 78
    started_at: '2026-09-08T04:29:00Z'
    deadline_at: '2026-09-08T05:47:00Z'
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
    outcome: >-
      The registered replay reproduced every planning-lane exact mass to the fraction (nine
      classes at 96/25 and three at U; the trailing-six class alone stays undecided as
      before). The end band widened from α + β = 2.6937° to Theorem A, [0°, 1.7139°] ∪
      [43.5293°, 45°] (mass 5529/512), and Theorem B, [0°, 10.3875°] ∪ [43.5293°, 45°] (mass
      351/32), both exact-decided on grid 79; on grid 119 the band widens further to Theorem C,
      [0°, 10.3875°] ∪ [43.0737°, 45°] (mass 11083/1024, α + β = 12.3138°), with the
      symmetric (12, 12) band [0°, 3.0318°] ∪ [42.3876°, 45°] refuted there too. Every grid-79 dual that
      reached eleven has continuum depth two or more under ceiling.py, so those readings are
      site-set artefacts, not obstructions.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-b-angle-classes.md
    stop_reason: The research slice closed at its checkpoint with the exit reached; the remaining clock is the finalization reserve.
    next_action: >-
      Under think-ndqj, sweep the end band at grid 119 and 159 and run the band toward 40.19° at grid 119 before any continuum family is built.
  - workflow: documentation-pass
    focus: correctness
    recording: contemporaneous
    clock_role: finalization
    objective: >-
      Write the result section and this record, validate the records tier, and commit on the
      lane branch without pushing.
    commitment: BC-295
    bead: think-ndqj
    status: stopped
    entered_by: planned_checkpoint
    switch_reason: The research slice closed at its checkpoint; the remaining time is the finalization reserve.
    budget_minutes: 72
    started_at: '2026-09-08T05:47:00Z'
    deadline_at: '2026-09-08T06:59:00Z'
    expected_output: The result section, this record, and one commit on lane/bc-295-angle-bands.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The deadline arrives before the records tier is green.
    fallback: Commit what is written with the failing step named in the checkpoint file.
    outcome: >-
      The result section, this record and the receipt were written; the records tier was
      run and its verdict is in checks; one commit on lane/bc-295-angle-bands, not pushed.
    evidence:
    - packing/campaign/agent-sessions/session-102-angle-band-theorems-at-q.md
    stop_reason: The record and result section were written and the records tier run inside the clock; the session stops at its fixed deadline with certification pending.
    next_action: >-
      Under think-ndqj, the coordinator allocates the experiment ids for the two theorems and the replay and integrates the branch.
  primary_bead: think-ndqj
  status: stopped
  budget:
    wall_minutes: 150
    checkpoint_minutes: 30
    finalization_minutes: 72
  stop_conditions:
  - The 2.5-hour clock ends at 06:59Z; a promising result does not extend it.
  - Only decide_class_program and class_minima verdicts are results; a float optimum is context.
  - No identifier is allocated; a frozen claim is marked as needing an experiment id and left blank.
  - One worker on a machine shared with five other agents; wall times are not comparable with the planning lane's.
  progress:
    metric: exact-decided width α + β of the robust end band excluded at 96/25, and replayed counts
    before: 'α + β = 2.6937° (cells 0–5 ∪ 175–180, planning lane, unregistered); five H-131 counts decided in a planning lane only.'
    after: 'α + β = 12.3138° (Theorem C, grid 119, cells 0–39 ∪ 172–180, mass 11083/1024), 11.8582° on grid 79 (Theorem B, mass 351/32), 3.1846° for the exit band (Theorem A); the symmetric band reaches 5.6442° on grid 119; the eight H-131 counts replayed exactly under this record.'
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-b-angle-classes.md
  - packing/campaign/agent-sessions/session-102-angle-band-theorems-at-q.md
  checks:
  - 'full gate: fast at cbe9fd76: passed'
  - packing-validate --records on the lane branch at 05:16Z, before this record was filled, failed only on this record's placeholders (six steps, all naming session-102); every other step passed.
  - >-
    packing-validate --records at 05:58Z on the final tree: every step passed except three
    generated-view drifts that a new terminal record always causes and that this lane was
    told not to touch — check_synopsis (SYNOPSIS.md's Current Handoff marker and agenda-021's
    selected bead must name think-ndqj), close_session --check (session-close-report.yaml and
    SYNOPSIS.md; run devtools.close_session --render), and the ledger (run packing-ledger
    render). No full gate was run in this lane.
  - >-
    The receipt is a harness-generated efficiency rollup of this session's own log, written by
    devtools.log_rollup at the last commit; it is an active-session lower bound, not a final
    cost.
  resource_rollups: [packing/campaign/resource-usage/agent-ae5b122129d330f9e.yaml]
  stop_reason: Stopped at the lane's fixed clock with the exit reached; no full gate was run in this lane (the coordinator owns integration and the pull-request surface), so certification is pending under the agenda's coordinating bead think-kbci; the lane's own bead think-ndqj is complete.
  next_action: >-
    Under think-kbci the coordinator allocates experiment ids for Theorems A, B and C and the H-131 replay and certifies the branch on the pull-request surface; BC-303 (think-znzj) reads this lane and decides whether the end band continues at grid 119 and 159 from k = 9 and whether the band toward 40.19° runs at grid 119.
---
# Angle-Band Theorems at `96/25`

Lane BC-295 of [Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md)
ran as one research session of two and a half hours on one worker, under
[H-130](../hypotheses/H-130-robust-end-band-theorem-at-q.md) and
[H-131](../hypotheses/H-131-near-axis-counts-at-q.md), with bead `think-ndqj`. The
result section is in
[lane B’s report](../series/series-000-smoke-and-calibration/results/agenda-030/lane-b-angle-classes.md#session-102--angle-band-theorems-at-9625-2026-09-08),
which holds the replay table, the widening table, the dual’s angular support with its
exact ceiling check, the grid-119 refinement, and every script.

Three things were decided.
The planning lane’s eight angle counts (H-131) and its Theorem 1.11 replay exactly on
the stated site set, every mass to the fraction.
The robust end band widened past H-130’s criterion in three steps: Theorem A,
`[0°, 1.7139°] ∪ [43.5293°, 45°]` with `α + β = 3.1846°`, and Theorem B,
`[0°, 10.3875°] ∪ [43.5293°, 45°]` with `α + β = 11.8582°`, both exact-decided by
`decide_class_program` on grid 79, and Theorem C, `[0°, 10.3875°] ∪ [43.0737°, 45°]`
with `α + β = 12.3138°` on grid 119; all three are frozen claims that need an experiment
id. And the site-set duals that reach eleven on grid 79 are not obstructions:
`ceiling.py` finds continuum depth two on the end bands and `1291/568` on the band
toward `40.19°`, grid 119 refutes the `(8, 8)` band grid 79 could not, and so the
fractional obstruction at `96/25` is, on this evidence, an artefact of the site set
rather than a property of the relaxation.

Three process notes.
Thirty minutes of queue time were lost to a chained waiter whose `pgrep -f` pattern
matched its own command line; the fix was a sequential queue script.
The grid-119 queue piped its output through `grep`, whose block-buffered file output hid
the finished rows for half an hour; the per-point `jsonl` logs were the record and are
what the result section is assembled from.
The machine ran at load average eight on four cores throughout, so the wall times in the
result section are not comparable with the planning lane’s. No identifier was allocated,
nothing was pushed, and no full gate was run in this lane; the record is stopped with
certification pending under `think-ndqj`.

## Integration Certification Addendum — 2026-09-08

The corrected integration checkpoint combines the 62-step fast pass at `cbe9fd76`, the
passing structured negative-control, slow and exhaustive component receipts at that same
revision, and four unchanged full-only geometry passes recorded in the retained raw
stdout from the failed `ef8a2e72` invocation.
The reviewed `ef8a2e72..cbe9fd76` source diff leaves those four components unaffected.
Together that log and the structured receipts cover all 69 declared validation steps.
The `ef8a2e72` full invocation remains failed; the later component runs are not called a
full invocation.

This later integration result discharges only the record’s certification debt.
It does not extend this stopped session’s clock, rerun its science, change a scientific
verdict, supply a missing artifact, or complete any target recorded as partial, stopped,
unrun or absent.
The original stop reason, resource accounting and unfinished complements
remain historical facts.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
