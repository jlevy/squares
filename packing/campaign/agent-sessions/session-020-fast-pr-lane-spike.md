---
title: session-020 — fast pull-request lane spike
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-020
  title: Fast pull-request lane spike
  date: '2026-08-25'
  started_at: '2026-08-25T23:43:00-07:00'
  deadline_at: '2026-08-26T00:53:00-07:00'
  goal: >-
    Cut the required pull-request path toward one minute with the smallest measured
    changes that retain complete Linux, macOS, exact-test, and mutation assurance at
    declared integration boundaries.
  workflow_phases:
  - workflow: efficiency-loop
    recording: contemporaneous
    clock_role: work
    focus: efficiency
    objective: >-
      Make pull requests run a bounded fast validator, keep complete Linux and
      full/deep macOS on main, manual, and scheduled runs, give full negative controls
      their measured two-worker setting, and test every selection and trigger contract.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 27
    started_at: '2026-08-25T23:43:00-07:00'
    deadline_at: '2026-08-26T00:10:00-07:00'
    expected_output: >-
      A tested workflow and validator patch with unchanged full test discovery, exact
      fast exclusion, direct integration assurance, local before/after receipts, and a
      stable required-job contract.
    validation_command: >-
      uv run --directory explorations/packing --frozen pytest -q
      tests/test_module_boundaries.py tests/test_validation_cli.py && uv run
      --directory explorations/packing --frozen --all-extras --group dev
      packing-validate --fast --jobs 2 --inner-jobs 1
    kill_condition: >-
      Stop if any exhaustive test or full validator step disappears from every surface,
      a macOS integration failure becomes nonblocking, the fast lane still runs an
      exhaustive exact node, or the required local path exceeds ninety seconds twice.
    fallback: >-
      Keep only the dedicated two-worker control change if its focused contracts and
      full gate pass, discard unsafe workflow selection, and preserve the exact failing
      contract under the spike bead.
    outcome: >-
      Pull requests now select a bounded Linux fast surface and stable aggregate, while
      main, manual, and scheduled events retain complete Linux, complete macOS, and
      deep-golden assurance. Core and exhaustive pytest form an explicit 101 plus 30
      partition, and complete controls use two dedicated workers.
    evidence:
    - >-
      The clean fast gate passed in 27.38 wall-seconds; its 101-test branch passed in
      12.93 seconds with exactly 30 exhaustive exact tests deselected.
    - >-
      Full collection contains 131 tests: 101 core and 30 exhaustive exact, with the
      marker contract limited to the four measured slow modules.
    - >-
      All 62 controls passed at two workers in 100.32 seconds, 58.22 seconds below the
      measured one-worker baseline.
    - >-
      The complete-gate attempt ran all 30 exact tests successfully in 254.16 seconds,
      then failed its concurrent core branch only because the host had 359 MiB free.
      That same 101-test core passed alone in 15.26 seconds.
    stop_reason: >-
      The bounded implementation, selection proof, and local timing receipts completed
      before the revised work boundary; remaining activity is reconciliation,
      publication, and hosted verification.
    next_action: >-
      Reconcile the plan, session, ledger, and synopsis; run focused and fast checks;
      commit and push PR 41; then measure the hosted required path.
  - workflow: efficiency-loop
    recording: contemporaneous
    clock_role: finalization
    focus: efficiency
    objective: >-
      Publish the tested fast-lane spike with its complete selection proof, resource
      limitation, plan receipt, bead state, and hosted pull-request timing.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      The implementation and local benchmarks completed the work objective; unused
      work minutes moved into finalization without extending the fixed session deadline.
    budget_minutes: 43
    started_at: '2026-08-26T00:10:00-07:00'
    deadline_at: '2026-08-26T00:53:00-07:00'
    expected_output: >-
      Schema-valid session and generated views, green focused and fast gates, reviewed
      commit on PR 41, terminal hosted required timing, and exact remaining beads.
    validation_command: >-
      uv run --directory explorations/packing --frozen pytest -q
      tests/test_module_boundaries.py tests/test_validation_cli.py && uv run
      --directory explorations/packing --frozen --all-extras --group dev
      packing-validate --fast --jobs 2 --inner-jobs 1
    kill_condition: >-
      Stop on generated-view drift after one render, an unrelated concurrent edit, a
      failed fast-lane contract, a hosted required path over ninety seconds twice, or
      the fixed session deadline.
    fallback: >-
      Preserve the exact green checkpoint and resource failure, keep the spike open,
      push only reviewed non-conflicting work, and hand off hosted measurement.
    outcome: >-
      Commit ccc1bb5 is pushed on PR 41. The first hosted required path passes in 46
      seconds with macOS skipped, and a one-worker local retry passes the complete
      integration surface despite the constrained host.
    evidence:
    - >-
      GitHub Actions run 32941767003 passed in 46 seconds end to end: validate used 37
      seconds, the required step used 24 seconds, packing-required used 2 seconds, and
      macOS portability was skipped.
    - >-
      The one-worker complete gate passed all 33 steps in 533.42 seconds, including 101
      core tests, 30 exhaustive exact tests, and all 62 controls.
    - >-
      Thirty-eight focused contracts, repository-wide Ruff and BasedPyright, session
      schema, generated ledger, synopsis, and tbd sync are clean.
    stop_reason: >-
      The implementation, complete assurance proof, hosted sub-minute result, durable
      records, bead state, commit, and remote branch are reconciled before the fixed
      deadline.
    next_action: >-
      Close the bounded spike, retain the remaining hosted samples under think-l7hi,
      and proceed to exact row-jet reuse under think-kdil.
  primary_bead: think-b784
  status: completed
  budget:
    wall_minutes: 70
    max_cycles: 2
    checkpoint_minutes: 20
    slice_minutes: 27
    finalization_minutes: 43
  stop_conditions:
  - The fixed 00:53:00-07:00 deadline arrives.
  - The fast and full surfaces do not have an exact checked union.
  - A workflow condition makes an invoked assurance job advisory or silently skipped.
  - Concurrent work edits the workflow, validator, marker modules, or session-020.
  progress:
    metric: required pull-request critical-path seconds with complete integration assurance
    before: >-
      PR 41 required Linux for 5m10s and duplicate full/deep macOS for 10m01s; local
      behavioral tests used 241.96 seconds and one-worker controls used 167.23 seconds.
    after: >-
      PR 41 run 32941767003 passes in 46 seconds end to end: Linux validate is 37
      seconds, its required step is 24 seconds, the aggregate is 2 seconds, and macOS
      is outside the pull-request critical path. Complete integration passes separately.
  delegations: []
  outputs:
  - .github/workflows/packing-validation.yml
  - explorations/packing/pyproject.toml
  - explorations/packing/src/sqpack/cli/validate.py
  - explorations/packing/tests/test_exact_jets.py
  - explorations/packing/tests/test_minus_w_row_jets.py
  - explorations/packing/tests/test_minus_w_sheet.py
  - explorations/packing/tests/test_minus_w_stress.py
  - explorations/packing/tests/test_module_boundaries.py
  - explorations/packing/tests/test_validation_cli.py
  - explorations/packing/development.md
  - explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
  - explorations/packing/SYNOPSIS.md
  - explorations/packing/campaign/agent-sessions/session-020-fast-pr-lane-spike.md
  checks:
  - Thirty-eight focused workflow and validator contracts pass.
  - Repository-wide Ruff formatting, Ruff lint, and BasedPyright pass.
  - The clean fast gate passes in 33.85 seconds; a prior clean sample used 27.38 seconds.
  - Full test collection is the disjoint union of 101 core and 30 exhaustive exact tests.
  - All 62 controls pass at two workers in 100.32 seconds.
  - The complete one-worker gate passes all thirty-three steps in 533.42 seconds.
  - Hosted run 32941767003 passes end to end in 46 seconds.
  stop_reason: >-
    The fast lane, full assurance surface, hosted receipt, records, bead state, commit,
    and pushed PR are complete within the fixed session budget.
  next_action: >-
    Preserve BC-010 under think-1s0h as the sole scientific handoff. Collect the
    remaining hosted acceptance samples under think-l7hi and implement exact row-jet
    reuse under think-kdil; add larger matrices only if measured tails require them.
---
# Session 020 — Fast Pull-Request Lane Spike

This W5 `efficiency-loop` session changes execution cost, not the W1–W7 research process
or its scientific authority.
The spike keeps complete assurance on integration events while measuring a smaller
required pull-request surface.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
