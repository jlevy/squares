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
  status: stopped
  ended_at: '2026-09-24T13:03:00Z'
  certification_pending: think-7b3b
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
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 370
    started_at: '2026-09-24T06:40:00Z'
    deadline_at: '2026-09-24T12:50:00Z'
    expected_output: >-
      A reader verdict on the whole rung-0 tree and a new experiment record for H-236;
      an n12 ceiling record if its run settles or reaches its clock.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      A verified non-degenerate leaf below U, or an instrument byte differs from the
      Amendment 1 digests.
    fallback: Record the bounded stop with the remaining frontier and hand off.
    outcome: >-
      Rung 0 closed: all 58 remaining subtrees completed and the independent reader
      accepted the complete tree, confirming H-236 (exp-232). The n12 loop converged at
      11.980175 < 12, rejecting H-241 (exp-233). A certificate-count overstatement in
      exp-231 was found and corrected as D-508 on PR 231.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-232-h236-rung-zero-closed.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-233-h241-n12-ceiling-settles-below-12.md
    stop_reason: Both runs reached their criteria before their clocks.
    next_action: Record the outcomes and close the session.
  - workflow: review-planning-oversight
    focus: process
    recording: contemporaneous
    clock_role: finalization
    objective: >-
      Record exp-232 and exp-233, agenda outcomes, the handoff and PR 233, and close with
      certification pending on one hosted full gate.
    status: stopped
    entered_by: planned_checkpoint
    switch_reason: Both overnight runs finished and the reader closed the tree.
    budget_minutes: 20
    started_at: '2026-09-24T12:50:00Z'
    deadline_at: '2026-09-24T13:10:00Z'
    expected_output: Terminal records, a refreshed handoff and PR 233, and a dispatched gate.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: A records check fails that cannot be repaired from the record.
    fallback: Leave the session in progress and name the failing check.
    outcome: >-
      Records, handoff and PR updated; the session closes stopped with certification
      pending on think-7b3b, as Session 156 did, so a gate clock cannot refuse it.
    evidence:
    - packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
    stop_reason: The close is complete and certification is owned by think-7b3b.
    next_action: Dispatch one hosted full gate on the closed head.
  budget:
    wall_minutes: 500
    slice_minutes: 120
    finalization_minutes: 130
  stop_conditions:
  - The owner ends the run; a self-declared budget is not a stop condition (OR-8).
  - Frozen instruments only; no new mathematics or instrument changes overnight.
  - At most two sub-agents, and none needed for the CPU runs themselves.
  progress:
    metric: Rung-0 subtrees closed and reader-verified; n12 ceiling state.
    before: >-
      198 of 256 rung-0 subtrees closed with every certificate reader-accepted and three
      Trump-degenerate leaves; the n12 ceiling loop unsettled near 11.98 (exp-230).
    after: >-
      Rung 0 is closed and H-236 confirmed at its registered scope (exp-232), pending
      BC-241 and a Fable max review before any register entry; H-241 is rejected: the
      n12 additive route is not shown dead above 3.9609 (exp-233).
  delegations: []
  resource_rollups:
  - packing/campaign/resource-usage/e8d698c4-206a-4921-bcc4-4f7e12fa474f.yaml
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-232-h236-rung-zero-closed.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-233-h241-n12-ceiling-settles-below-12.md
  checks:
  - The rung-0 instrument digests matched Amendment 1 before the run.
  - The independent reader returned closed over all 256 subtree files.
  - packing-validate --records passed on the closed records.
  stop_reason: >-
    Both overnight runs decided their hypotheses; certification of the closed head is
    pending on think-7b3b.
  next_action: >-
    BC-381 (think-6w2y): a Fable max W2 review of the closed rung-0 tree and the register
    decision; think-7b3b certifies this head with one hosted full gate.
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
