---
title: "Session 158 — Lock in rung 0, close BC-241, price rung 1"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-158
  title: Lock In Rung 0, Close BC-241, Price Rung 1
  date: '2026-09-24'
  started_at: '2026-09-24T19:00:00Z'
  deadline_at: '2026-09-25T15:00:00Z'
  branch: claude/n11-rung0-lock-in-and-rung1-pilot
  primary_bead: think-svmp
  status: in_progress
  goal: >-
    Lock in rung 0 of the n11 settlement ladder with a Fable max review, an off-repo
    archive of its certificate tree and a register decision rated by epistemics.md;
    close BC-241 so results ending in Trump-degenerate leaves lose their qualifier; and
    price rung 1 (H-112) with a parameterized-box pilot of the rung-0 instrument, run
    overnight on CPU. Stacked on PR 233.
  workflow_phases:
  - workflow: factual-review
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      BC-381 and BC-382: review the closed rung-0 tree and the BC-241 obligations, and
      admit the parameterized box preset for BC-383, while the tree is archived.
    status: in_progress
    entered_by: session_start
    switch_reason: null
    budget_minutes: 240
    started_at: '2026-09-24T19:00:00Z'
    deadline_at: '2026-09-24T23:00:00Z'
    expected_output: >-
      Two dated reviews, an archived tree with a checksum manifest, an admitted preset
      and a register decision for H-236.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: A review rejects the closed tree or finds the preset changes h236.
    fallback: Record the rejection or the defect and stop the dependent step.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: Collect the three lanes, then register and launch the pilot.
  budget:
    wall_minutes: 1200
    slice_minutes: 240
    finalization_minutes: 90
  stop_conditions:
  - The owner ends the run; a self-declared budget is not a stop condition (OR-8).
  - No register entry without the Fable max review and an epistemics.md derivation.
  - The h236 path of the instrument must stay byte-identical.
  progress:
    metric: Rung 0 locked in, BC-241 disposition, rung-1 pilot verdicts.
    before: >-
      Rung 0 closed and H-236 confirmed at its scope pending BC-241 (exp-232); rung 1
      unpriced; the certificate tree only in a worktree attic.
    after: In progress.
  delegations: []
  outputs: []
  checks: []
  stop_reason: null
  next_action: Collect the three lanes, then register and launch the pilot.
---
# Lock In Rung 0, Close BC-241, Price Rung 1

The owner selected the three next steps after rung 0 closed: secure what it proved,
remove the BC-241 qualifier its terminal leaves carry, and measure what rung 1 would
cost before building anything new for it.
Three lanes run in parallel, the pilot runs overnight on CPU, and the session is stacked
on PR 233.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
