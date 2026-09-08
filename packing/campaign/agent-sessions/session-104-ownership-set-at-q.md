---
title: session-104 — a robust unavoidable set of at most eleven marks at 96/25
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-104
  title: A robust unavoidable set of at most eleven marks at 96/25 (BC-302, H-134)
  date: '2026-09-08'
  started_at: '2026-09-08T04:38:00Z'
  deadline_at: '2026-09-08T07:08:00Z'
  branch: claude/squares-n11-constraints-wl9atd
  goal: >-
    Decide BC-302 within one 2.5-hour block: build a checked falsifier for candidate mark
    sets at side 96/25 (marks thickened by 3/500), run it on the sets built from T-018's
    atom skeleton and on Stromquist-style sets, catalogue every exact escape, and either
    prove a survivor's nonavoidance regions or record the catalogue as the obstruction the
    closing route needs.
  workflow_phases:
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: >-
      Orientation on the lane inputs, then the engine: a numpy grid and Nelder-Mead search
      over poses followed by exact rational verification of containment and of distance
      above 3/500 to every mark, self-tested on lane C's exact escape at q, on exp-121's
      frozen square, and on two controls that must have no escape.
    commitment: BC-302
    bead: think-qfog
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-09-08T04:38:00Z'
    deadline_at: '2026-09-08T05:08:00Z'
    expected_output: escape_engine.py and its self-test, both retained verbatim in the lane document's appendix.
    validation_command: uv run --frozen --all-extras --group dev python selftest.py (from the scratch directory, with the project interpreter)
    kill_condition: The exact verifier disagrees with lane C's retained margin 14979/1060025 or with exp-121's strict escape.
    fallback: Reduce the engine to the fixed-candidate exact checker of exp-121 and search by hand.
    outcome: >-
      Engine written and self-tested: lane C's escape reproduced to the exact margin,
      exp-121's frozen square reproduced as a strict escape, the search rediscovers an
      escape of P10 at q (a larger one, at the bottom wall), and both controls report none.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md
    stop_reason: Bounded output complete and self-tested.
    next_action: Run the candidate sets and the adversarial and exact searches.
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: >-
      Candidate sets from the atom skeleton scaled by 384/381, Stromquist's ten points plus
      one, adversarial min-max over free and K4-symmetric eleven-point sets, and an exact
      branch-and-bound over test squares driven by the falsifier as a cutting-plane loop.
    commitment: BC-302
    bead: think-qfog
    status: PHASE2_STATUS
    entered_by: planned_checkpoint
    switch_reason: The engine is verified; the block's question needs the candidate sets and their escapes.
    budget_minutes: 90
    started_at: '2026-09-08T04:48:00Z'
    deadline_at: '2026-09-08T06:18:00Z'
    expected_output: The escape catalogue with exact poses and the branch-and-bound verdict, in the lane document.
    validation_command: uv run --frozen --all-extras --group dev python candidates.py, minimax.py, loop.py (scratch directory, project interpreter); every reported escape re-verified by escape_engine.exact_verify.
    kill_condition: A candidate set with no verified escape at step 0.02 and angle step 1.5 degrees, which switches the lane to the proof attempt.
    fallback: Publish the catalogue at its current scope with the resolution of every non-refutation.
    outcome: PHASE2_OUTCOME
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md
    stop_reason: PHASE2_STOP
    next_action: Write the lane document, the README line and this record; validate the records tier; commit.
  - workflow: documentation-pass
    focus: correctness
    recording: contemporaneous
    clock_role: finalization
    objective: The lane document, the one-line README entry, this record, the records-tier validation and the commit.
    commitment: BC-302
    bead: think-qfog
    status: PHASE3_STATUS
    entered_by: planned_checkpoint
    switch_reason: The computations are at their block scope; the remaining time is the record.
    budget_minutes: 30
    started_at: 'PHASE3_START'
    deadline_at: '2026-09-08T07:08:00Z'
    expected_output: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md and this record.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The block's deadline.
    fallback: Commit what is written with the checkpoint file naming what is missing.
    outcome: PHASE3_OUTCOME
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/README.md
    stop_reason: PHASE3_STOP
    next_action: The coordinator integrates the branch, allocates an experiment id if the frozen claim is registered, and closes this record with the harness rollup under think-qfog.
  primary_bead: think-qfog
  status: in_progress
  budget:
    wall_minutes: 150
    checkpoint_minutes: 30
    finalization_minutes: 30
  stop_conditions:
  - The block's 2.5-hour clock; no extension for a promising result.
  - An escape is a result only when verified exactly; a no-escape reading carries its resolution and is never a theorem.
  - No identifiers allocated, no shared registry edited, no push.
  progress:
    metric: PROGRESS_METRIC
    before: >-
      H-134 registered with a prior of about thirty per cent; the only escape instrument
      is exp-121's fixed-candidate checker; no candidate eleven-mark set at 96/25 has been
      tested.
    after: PROGRESS_AFTER
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/README.md
  checks:
  - CHECKS_LINE
  resource_rollups: []
  stop_reason: null
  next_action: >-
    Coordinator: integrate the lane branch, register the document in the document map, and
    close this record under think-qfog once the harness rollup exists; the lane document's
    section 7 names what the next session does first.
---
# session-104 — A Robust Unavoidable Set of at Most Eleven Marks at 96/25

SESSION_BODY

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
