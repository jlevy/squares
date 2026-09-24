---
title: "Session 157 — Overnight CPU runs, finishing rung 0 and resuming the n12 ceiling"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-157
  title: Overnight CPU Runs, Finishing Rung 0 and Resuming the n12 Ceiling
  date: '2026-09-24'
  started_at: '2026-09-24T06:40:00Z'
  deadline_at: '2026-09-24T15:00:00Z'
  branch: claude/n11-rung0-overnight-2026-09-24
  primary_bead: think-ie35
  status: in_progress
  goal: >-
    Spend one night of CPU on registered work with frozen instruments and little agent
    reasoning, as the owner asked: finish rung 0 of the n11 settlement ladder (H-236,
    BC-375) with the unchanged Amendment 1 bytes and run the independent reader over the
    whole tree; as cores free up, resume the n12 additive-ceiling loop (H-241) from its
    retained warm state and, if time remains, extend the descent-filtered census
    (H-238). Stacked on PR 231.
  workflow_phases:
  - workflow: research-loop
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Resume the 58 wall-cap rung-0 subtrees, heavy partials first, with the frozen
      instrument; then run the reader over the complete tree and record H-236's verdict;
      use freed cores for the n12 ceiling resume.
    status: in_progress
    entered_by: session_start
    switch_reason: null
    budget_minutes: 420
    started_at: '2026-09-24T06:40:00Z'
    deadline_at: '2026-09-24T13:40:00Z'
    expected_output: >-
      A reader verdict on the whole rung-0 tree and a new experiment record for H-236;
      an n12 ceiling record if its run settles or reaches its clock.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      A verified non-degenerate leaf below U, or an instrument byte differs from the
      Amendment 1 digests.
    fallback: Record the bounded stop with the remaining frontier and hand off.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: Monitor the rung-0 run; start the n12 resume when the bulk of subtrees has closed.
  budget:
    wall_minutes: 500
    slice_minutes: 120
    finalization_minutes: 80
  stop_conditions:
  - The owner ends the run; a self-declared budget is not a stop condition (OR-8).
  - Frozen instruments only; no new mathematics or instrument changes overnight.
  - At most two sub-agents, and none needed for the CPU runs themselves.
  progress:
    metric: Rung-0 subtrees closed and reader-verified; n12 ceiling state.
    before: >-
      198 of 256 rung-0 subtrees closed with every certificate reader-accepted and three
      Trump-degenerate leaves; the n12 ceiling loop unsettled near 11.98 (exp-230).
    after: In progress.
  delegations: []
  outputs: []
  checks: []
  stop_reason: null
  next_action: Monitor the rung-0 run and start the n12 resume when cores free up.
---
# Overnight CPU Runs: Finishing Rung 0 and Resuming the n12 Ceiling

The owner asked for a night of CPU on the registered work, with limited tokens and no
risky reasoning.
Rung 0’s remaining 58 subtrees run with the unchanged frozen instrument,
heavy partial subtrees first so the critical path starts at once; the independent reader
then replays the whole tree.
Freed cores go to the n12 ceiling loop from its retained warm state.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
