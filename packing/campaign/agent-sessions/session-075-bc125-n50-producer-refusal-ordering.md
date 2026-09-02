---
title: session-075 — BC-125 n = 50 producer refusal ordering
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-075
  title: BC-125 n = 50 producer refusal ordering
  date: '2026-09-01'
  started_at: '2026-09-02T00:15:00Z'
  deadline_at: '2026-09-02T02:45:00Z'
  branch: codex/agenda014-six-hour-run
  goal: >-
    Verify prospectively that the hash-bound frozen n = 50 producer refuses an existing
    result before binding observation, fixture loading, receipt evaluation or
    publication, without changing exp-050.
  workflow_phases:
  - workflow: insight-iteration
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Bind the frozen producer, result, exp-050, session-070 and H-059 hashes; freeze the
      four live sentinel seams, exact refusal, fresh paths and normal/optimized mutation
      matrix before implementation.
    commitment: BC-125
    bead: think-17q7
    status: in_progress
    entered_by: session_start
    switch_reason: null
    budget_minutes: 15
    started_at: '2026-09-02T00:15:00Z'
    deadline_at: '2026-09-02T00:30:00Z'
    expected_output: A validated exp-055 sentinel and provenance contract with exp-050 read-only.
    validation_command: >-
      uv run --frozen softschema validate
      campaign/series/series-000-smoke-and-calibration/experiments/exp-055-h-059-n50-producer-refusal-ordering.md
    kill_condition: >-
      Stop if a frozen hash differs, an ordinary import would load the real intake before
      injection, a sentinel lacks liveness calibration, or source or geometry access is required.
    fallback: Retain the exact provenance or injection defect and stop before W7.
    outcome: null
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-055-h-059-n50-producer-refusal-ordering.md
    stop_reason: null
    next_action: Enter W7 only if all frozen hashes and the sentinel contract validate.
  primary_bead: think-17q7
  status: in_progress
  budget:
    wall_minutes: 150
    max_cycles: 6
    checkpoint_minutes: 20
    slice_minutes: 20
    finalization_minutes: 35
  stop_conditions:
  - Active BC-125 work reaches the fixed 2026-09-02T02:10:00Z cap.
  - The common 2026-09-02T02:45:00Z first-wave deadline arrives.
  - A frozen binding changes, exp-050 bytes move or a real source or geometry seam opens.
  - A sentinel calibration, mutation, interpreter-equivalence or independent-verifier guard fails.
  progress:
    metric: independently verified zero-call producer refusal receipts
    before: zero; exp-050 has a bounded unclosed producer-provenance gap
    after: null
  delegations: []
  outputs:
  - packing/campaign/agent-sessions/session-075-bc125-n50-producer-refusal-ordering.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-055-h-059-n50-producer-refusal-ordering.md
  checks: []
  stop_reason: null
  next_action: Run BC-125's first W3 cell under think-17q7 from the pushed launch revision.
---
# Session-075 — BC-125 `n = 50` Producer Refusal Ordering

A zero-call trace counts only after each sentinel fires in a separate synthetic
calibration. The independent verifier imports neither the new harness nor the frozen
producer.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
