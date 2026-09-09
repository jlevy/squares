---
title: session-119 — publish and test the selected wall tuple
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-119
  title: Publish and test the selected wall tuple
  date: '2026-09-09'
  started_at: '2026-09-09T16:19:56Z'
  deadline_at: '2026-09-09T16:49:56Z'
  branch: codex/n11-independent-owner-audit
  goal: Publish and decide the unchanged exact five-dot cover for wall-owner tuple(0,0,0,7), preserving
    the earlier unrun allocation and result scope.
  workflow_phases:
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: Publish the admitted selected-cover source and prospective H147/exp149, then run the single
      guarded target.
    commitment: BC-319
    bead: think-ykd6
    status: stopped
    entered_by: session_start
    switch_reason: null
    budget_minutes: 15
    started_at: '2026-09-09T16:19:56Z'
    deadline_at: '2026-09-09T16:34:56Z'
    expected_output: One source-bound complete cover, replayed first-deficit refutation, or retained partial/invalid
      receipt for the fixed tuple.
    validation_command: Published exp149 command with five-minute external, two-second grace and 240-second
      internal guards
    kill_condition: No target before clean publication; launch only by16:29:54UTC so the unchanged302-second
      allowance fits before the work cutoff.
    fallback: Preserve unrun or partial status and the exact missing obligation; do not infer an H146 verdict.
    outcome: The admitted source and prospective H147/exp149 were published cleanly at
      b8731b30f9e501b6acb24946e57484a856aae7c2. The launch guard expired before a target could fit, so
      exp149 remained unrun.
    evidence:
    - packing/cases/n11_five_dot_cover/selected-cover-source-admission.md
    stop_reason: The16:29:54UTC latest launch passed during source/protocol publication. No scientific
      target ran.
    next_action: Session120 executes the unchanged published exp149 once before its fresh guarded cutoff.
  primary_bead: think-ykd6
  status: stopped
  budget:
    wall_minutes: 30
    max_cycles: 1
    orientation_minutes: 1
    checkpoint_minutes: 15
    slice_minutes: 15
    finalization_minutes: 15
  stop_conditions:
  - Exp149 keeps its five-minute external, two-second termination grace and240-second internal allowance;
    latest launch16:29:54UTC.
  - Stop new research at16:34:56UTC and reserve the final15minutes for reconciliation through16:49:56UTC.
  - A first replayed positive deficit refutes only H147. H146 remains unresolved; neither outcome proves
    a global n11 bound.
  progress:
    metric: Complete exact five-dot cover or replayed strict escape for tuple(0,0,0,7).
    before: Source admission passed; the Session118 allocation expired unrun.
    after: Source and protocol published from a clean exact head; exp149 remained prospective and unrun.
  delegations: []
  outputs:
  - packing/devtools/wall_owner_selected_cover.py
  - packing/tests/test_wall_owner_selected_cover.py
  - packing/cases/n11_five_dot_cover/selected-cover-source-admission.md
  - packing/campaign/hypotheses/H-147-selected-wall-tuple-cover.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-149-selected-wall-tuple-cover.md
  checks:
  - Session118 ends and this session begins at exactly2026-09-09T16:19:56Z.
  - Five focused controls passed in1.94seconds; Ruff and BasedPyright passed. Astra Max independently
    passed five controls in0.44seconds and gave source GO without target access.
  - No exp149 target has run.
  - Focused source, Ruff, format, BasedPyright, synopsis, documentation, ledger and diff checks passed;
    local and remote heads agreed exactly at publication.
  stop_reason: The clean source checkpoint was published after the latest launch that could preserve the
    full process allowance.
  next_action: Under think-ykd6, run the unchanged exp149 exactly once in Session120 before16:59:48UTC,
    then disposition H147 without inferring an H146 or global-bound verdict.
  certification_pending: think-ta8s
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-119.yaml
---
# Session119: Publish and Test the Selected Wall Tuple

**Entry point: W6 research loop.** Session118 admitted the exact thin wrapper but missed
its guarded publication window.
This fresh continuation keeps the tuple, dots, inputs, criteria and process limits
unchanged. It does not complete exp148’s seed bank.

The selected tuple is `(0,0,0,7)` in BL, BR, TL, TR order.
Acceptance requires exact zero uncovered area at all361 directions.
The first positive deficit must carry an independently replayed strict escape and
refutes only this selected H147 cover.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
