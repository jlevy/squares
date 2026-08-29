---
title: session-017 — research-loop efficiency infrastructure
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-017
  title: Research-loop efficiency infrastructure
  date: '2026-08-25'
  started_at: '2026-08-25T18:45:05-07:00'
  deadline_at: '2026-08-25T20:45:05-07:00'
  goal: >-
    Establish a trustworthy loop-1, loop-2, local-validation, and CI timing baseline;
    publish a staged W5 efficiency plan; and land a reusable recursive Codex-log scanner
    without changing the Square Packing workflow or weakening an assurance gate.
  workflow_phases:
  - workflow: efficiency-loop
    recording: contemporaneous
    clock_role: work
    focus: efficiency
    objective: >-
      Measure where time went in both named Codex research loops and representative
      packing CI, distinguish critical-path wall time from recursive overlap and model
      timing bounds, then retain the scanner, review, plan, and bounded tbd work packages.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 75
    started_at: '2026-08-25T18:45:05-07:00'
    deadline_at: '2026-08-25T20:00:05-07:00'
    expected_output: >-
      A versioned recursive JSONL rollup with focused tests, a dated full efficiency
      review, a new-plan-spec artifact, developer documentation, and linked Efficiency
      beads that preserve the existing W5 acceptance guards.
    validation_command: >-
      uv run --directory explorations/packing --frozen pytest -q
      tests/test_codex_log_rollup.py && uv run --directory explorations/packing --frozen
      ruff check devtools/codex_log_rollup.py tests/test_codex_log_rollup.py && uv run
      --directory explorations/packing --frozen basedpyright
      devtools/codex_log_rollup.py tests/test_codex_log_rollup.py && git diff --check
    kill_condition: >-
      Stop on an unresolvable legacy-history ambiguity, a model-time label unsupported by
      the logs, overlap with the active loop-2 worktree, a weakened validation or
      portability contract, or the fixed phase deadline.
    fallback: >-
      Retain the manually checked CI and loop totals with explicit timing limits, leave
      the scanner bead open, and record the smallest failing fixture or missing log field
      before finalization.
    outcome: >-
      The phase retained a tested `CodexEfficiencyRollup/v1` scanner and a dated review
      of 139 loop-1 sessions, seven live loop-2 sessions, twelve recent successful CI
      runs, representative step timings, local exact-test delays, model/thinking usage,
      and a staged infrastructure plan under the existing Efficiency epic.
    evidence:
    - >-
      Five focused scanner tests pass, including current and legacy child-history
      de-duplication, live and interrupted turns, model/thinking/token splits, command
      polling, and recursive overlap; Ruff and BasedPyright are clean.
    - >-
      The accepted legacy ownership rule removes 101 replayed parent responses and
      14,641,508 falsely attributed input tokens from three child logs.
    - >-
      CI run 32912699602 records 266.24 seconds on Linux validation and 190.69 seconds
      on the duplicated macOS full gate before a separate 75.05-second deep check.
    stop_reason: >-
      The scanner, review, plan, documentation, and bounded backlog were complete and
      focused checks passed at the planned finalization boundary.
    next_action: >-
      Enter the reserved W5 finalization phase, rebase onto loop 2's terminal checkpoint,
      add this session without a numbering collision, run the complete packing gate,
      reconcile generated views and beads, then push a clean branch.
  - workflow: efficiency-loop
    recording: contemporaneous
    clock_role: finalization
    focus: efficiency
    objective: >-
      Reconcile the W5 artifacts, session ledger, generated views, tbd state, full
      validation receipt, commits, and remote branch while preserving the measured
      efficiency baseline and one exact implementation order.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The measured baseline and scanner contract completed within the work phase; the
      remaining forty-five minutes were reserved for integration and validation.
    budget_minutes: 45
    started_at: '2026-08-25T20:00:05-07:00'
    deadline_at: '2026-08-25T20:45:05-07:00'
    expected_output: >-
      A schema-valid terminal session, fresh ledger and synopsis, complete packing gate
      receipt, closed scanner bead, synced backlog, and pushed efficiency branch based
      on loop 2's terminal commit.
    validation_command: >-
      uv run --directory explorations/packing --frozen --all-extras --group dev
      packing-validate --jobs 2 --inner-jobs 1
    kill_condition: >-
      Stop on a changed loop-2 terminal branch, stale generated view, three consecutive
      validation failures, unrelated user changes, a weakened gate, or the session
      deadline.
    fallback: >-
      Preserve the last validated checkpoint, exact failing command and output, terminal
      session state, open scanner bead, and one repair action; do not hide a failure or
      modify CI policy in this planning session.
    outcome: >-
      Finalization integrated session 017 without disturbing the scientific handoff,
      refreshed the ledger and synopsis document-map block, closed the completed scanner
      bead, and passed the unchanged full packing gate after repairing two bounded
      integration findings from its first run.
    evidence:
    - >-
      Checkpoint e66dc41 contains the scanner, focused tests, dated review, staged plan,
      developer guidance, and document-map entries on the isolated efficiency branch.
    - >-
      The branch is rebased onto loop 2's terminal a69feea checkpoint; no live research
      worktree or session artifact was edited.
    - >-
      The first full gate completed in 288.63 seconds and found only a Ruff formatting
      change in the new scanner and a stale generated synopsis document-map block; both
      focused repairs then passed their direct checks.
    - >-
      The unchanged rerun passed all thirty-two validation steps in 284.29 wall-seconds,
      including 124 behavioral tests in 213.97 seconds and all 62 negative controls in
      138.04 seconds.
    stop_reason: >-
      The terminal session, generated views, documentation contracts, tbd state, and
      complete validation surface were clean before the fixed deadline; no kill
      condition fired.
    next_action: >-
      Preserve BC-010 under think-1s0h as the scientific handoff. Begin the W5
      implementation plan with think-l7hi timing artifacts and the required Linux fast
      lane while think-rthe profiles identical-result negative-control concurrency.
  primary_bead: think-ma71
  status: completed
  budget:
    wall_minutes: 120
    max_cycles: 2
    checkpoint_minutes: 60
    slice_minutes: 75
    finalization_minutes: 45
  stop_conditions:
  - The finalization phase begins at 20:00:05-07:00.
  - Two W5 phases open, including finalization.
  - A proposed speedup would weaken a correctness, mutation, portability, or record guard.
  - The isolated branch cannot be rebased cleanly onto loop 2's terminal checkpoint.
  - A clean validated commit and exact next implementation action cannot be preserved.
  progress:
    metric: measured research-loop bottlenecks with reusable recursive telemetry
    before: >-
      The project has prior gate timings and performance beads, but no recursive
      Codex-log rollup, no comparable loop-1 and loop-2 task tree, no model/thinking
      tally, and no current CI lane plan tied to exact local-test delays.
    after: >-
      CodexEfficiencyRollup/v1 recursively reports session, turn, model, thinking,
      tokens, commands, model timing bounds, active union, and overlap; the dated review
      compares both named loops with current CI and local gates; the staged plan and five
      bounded work packages preserve exact assurance guards; the complete gate passes.
  delegations: []
  outputs:
  - devtools/codex_log_rollup.py
  - tests/test_codex_log_rollup.py
  - docs/project/reviews/review-2026-08-25-research-loop-efficiency.md
  - docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
  - development.md
  - docs/project/document-map.yaml
  - campaign/agent-sessions/session-017-research-loop-efficiency.md
  - campaign/ledger.md
  checks:
  - >-
    Scanner fixtures pass 5 of 5; Ruff reports no findings and BasedPyright reports zero
    errors, warnings, or notes.
  - >-
    Loop 1 closes at 45h28m27s wall envelope, 37h02m09s parent active, 57h07m47s
    recursive agent-time, and 20h05m37s overlap across 139 sessions.
  - >-
    The live loop-2 snapshot records 3h48m27s parent active and 8h16m19s recursive
    agent-time; its branch has no pull request, so local gates and exact tests rather
    than GitHub CI account for its measured command delays.
  - >-
    Twelve recent successful packing workflows range from 4m50s to 7m10s with a 5m51.5s
    median; the 65 serial inner-worker negative controls lead both representative jobs.
  - >-
    The unchanged full packing gate passes all thirty-two steps in 284.29 wall-seconds;
    the new scanner is included in 124 passing behavioral tests, all 62 negative controls
    fire, and documentation covers 248 durable documents.
  stop_reason: >-
    The declared W5 baseline, reusable scanner, staged plan, session log, complete gate,
    synced backlog, and clean remote handoff were all preserved within the fixed session
    budget.
  next_action: >-
    Preserve BC-010 under think-1s0h as the sole scientific handoff and preregister its
    named exp-045 successor before scientific implementation or target work. Separately,
    begin W5 implementation with think-l7hi timing artifacts and the required Linux fast
    lane while think-rthe profiles identical-result negative-control concurrency.
---
# Session 017 — Research-Loop Efficiency Infrastructure

This session is entirely W5 `efficiency-loop` work with focus `efficiency`. It measures
and improves the implementation of existing workflows; it does not change their phases,
authority, scientific criteria, or assurance obligations.

The repository record was added after session 016 published its terminal checkpoint so
the concurrent tasks could not claim the same sequential id.
The W5 classification, bounded objective, isolated branch, and finalization reserve were
declared before the work; delaying the filename did not change the contract.

## Fresh-Agent Resume

The authoritative branch is `codex/packing-efficiency-infrastructure`, based on loop 2’s
terminal checkpoint `a69feea`. Read the
[dated efficiency review](../../../docs/project/reviews/review-2026-08-25-research-loop-efficiency.md),
the
[active plan](../../../docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md),
and `tbd show think-ma71`.

Before 20:45:05-07:00, perform finalization only:

```shell
uv run --directory explorations/packing --frozen softschema validate \
  campaign/agent-sessions/session-017-research-loop-efficiency.md
uv run --directory explorations/packing --frozen --all-extras --group dev \
  packing-validate --jobs 2 --inner-jobs 1
uv run --directory explorations/packing --frozen packing-ledger render
uv run --directory explorations/packing --frozen packing-ledger check
uv run --directory explorations/packing --frozen python -m devtools.check_synopsis
```

Do not implement the CI policy, tune worker counts, or add symbolic caches in this
session. The next implementation order is timing artifacts and the required Linux fast
lane, negative-control worker profiling, selected blocking macOS portability, then exact
row-jet reuse.

## Framework Limit

AgentSession/v2 represents this session’s type through its ordered W5 phases and focus.
It cannot safely carry the recursive task intervals, command excerpts, model responses,
or token histories.
Those remain linked evidence in the versioned scanner output contract
and dated review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
