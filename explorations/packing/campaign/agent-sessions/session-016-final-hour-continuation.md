---
title: session-016 — final-hour exact-instrument continuation
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-016
  title: Final-hour exact-instrument continuation
  date: '2026-08-25'
  started_at: '2026-08-25T19:08:08-07:00'
  deadline_at: '2026-08-25T20:08:08-07:00'
  goal: >-
    Preserve the last hour of the four-hour BC-010 loop after session 015 reaches its
    declared phase cap: use one bounded W7 slice to derive the remaining exact scale and
    mutation contract, then reserve thirty minutes for validation and handoff.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: insight
    objective: >-
      Derive a finite exact scale-routing and production-mutation design for the
      remaining exp-044 instrument boundary, using the accepted row, stress, and sheet
      helpers without implementing or measuring a pure -W target.
    status: in_progress
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-08-25T19:08:08-07:00'
    deadline_at: '2026-08-25T19:38:08-07:00'
    expected_output: >-
      A source-bound scale case split, mutation-to-guard map, and exact implementation
      boundary retained in this session, or a smaller finite blocker list.
    validation_command: >-
      uv run --directory explorations/packing --frozen softschema validate
      campaign/agent-sessions/session-016-final-hour-continuation.md && uv run
      --directory explorations/packing --frozen packing-ledger check && git diff --check
    kill_condition: >-
      Stop on one assumed scale, copied target coefficient, mutation after certificate
      construction, scientific disposition, missing source identity, or at the phase
      deadline.
    fallback: >-
      Retain the unresolved scale branches, unguarded mutation, and exact next test in
      this session; begin finalization at its fixed absolute start without target work.
    outcome: null
    evidence:
    - >-
      Published checkpoint 8ee367b provides the accepted row, normalized-stress, and
      formula-derived sheet substrate from which the remaining contract can be audited.
    stop_reason: null
    next_action: >-
      Delegate independent scale and mutation analyses, reconcile their finite contract,
      and stop for finalization no later than 19:38:26-07:00.
  primary_bead: think-1s0h
  status: in_progress
  budget:
    wall_minutes: 60
    max_cycles: 2
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 30
  stop_conditions:
  - The finalization phase begins at 19:38:08-07:00.
  - Two phases open, including finalization.
  - The scale or mutation design would require a scientific target execution.
  - A clean committed checkpoint and exact repository handoff cannot be preserved.
  progress:
    metric: exact pure -W instrument blockers reduced before finalization
    before: >-
      Exact production row jets, normalized nine-row stresses, and the exp-034 positive
      sheet control are accepted. Scale routing, production mutations, and all target
      dispositions remain open; exp-044 is terminal with no result JSON.
    after: null
  delegations: []
  outputs:
  - campaign/agent-sessions/session-016-final-hour-continuation.md
  checks:
  - Session 015 stopped at its declared eight-phase cap with checkpoint 8ee367b pushed.
  stop_reason: null
  next_action: >-
    Under think-1s0h and BC-010, finish only the active W7 scale-and-mutation design
    phase, then enter finalization at 19:38:08-07:00.
---
# Session 016 — Final-Hour Exact-Instrument Continuation

Session 015 used its eighth declared phase after publishing the reviewed exact row,
stress, and sheet helpers.
This explicit continuation preserves the original four-hour deadline without weakening
that cap or relying on a controller’s private memory.

## Fresh-Agent Resume

The authoritative branch is `origin/codex/packing-4h-research-loop-2026-08-25`;
checkpoint `8ee367b` contains the accepted helper implementation.
Fetch and switch to that branch, then read:

1. [`session-015`](session-015-four-hour-r4-r5-loop.md) for the complete prior phase and
   audit history.
2. The terminal
   [`exp-044`](../series/series-000-smoke-and-calibration/experiments/exp-044-h-023-n5-minus-w-row-jets.md)
   for the frozen target boundary and unimplemented obligations.
3. [`minus_w_row_jets.py`](../../cases/n5/minus_w_row_jets.py),
   [`minus_w_stress.py`](../../cases/n5/minus_w_stress.py), and
   [`minus_w_sheet.py`](../../cases/n5/minus_w_sheet.py) with their focused tests.
4. [`H-023`](../hypotheses/H-023-n5-terminal-connectivity.md), `BC-010` in
   [`agenda-001`](../agendas/agenda-001-basin-confidence-ladder.md), and the owning bead
   `think-1s0h` for the wider dependency state.

From the repository root, verify the checkout before writing:

```shell
git fetch origin codex/packing-4h-research-loop-2026-08-25
git switch codex/packing-4h-research-loop-2026-08-25 2>/dev/null || \
  git switch --track -c codex/packing-4h-research-loop-2026-08-25 \
  origin/codex/packing-4h-research-loop-2026-08-25
git pull --ff-only
tbd prime
date -Iseconds
git status --short --branch
tbd show think-1s0h --max-lines 260
uv run --directory explorations/packing --frozen packing-ledger check
```

Before 19:38:08-07:00, continue only the declared scale-and-mutation design.
At or after 19:38:08-07:00, open or continue only the finalization phase.
At or after 20:08:08-07:00, stop all substantive work and preserve the terminal records,
validation receipt, pushed commit, synced bead note, and exact next action.

Do not run a pure `-W` target, create a result JSON, infer an obstruction, or launch the
generic numerical campaign.
A native goal, heartbeat, chat history, or Codex memory may wake an agent, but none is
part of the scientific state.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
