---
title: session-091 — exact P12 escape and conditional compatibility
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-091
  title: Exact P12 escape and conditional compatibility
  date: '2026-09-07'
  started_at: '2026-09-07T05:49:00Z'
  deadline_at: '2026-09-07T07:49:00Z'
  branch: codex/structural-compatibility-continuation
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-091.yaml
  goal: >-
    Resolve the selected H-110 instrument and single fixed candidate, then use the
    evidence to choose the next useful BC-255 conditional-compatibility or
    localization obligation. Preserve progress on one integrated successor PR at
    checkpoints no more than two active hours apart.
  workflow_phases:
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: Build independent source-free H-110 controls and assess the conditional proof obligation.
    commitment: BC-255
    bead: think-qv73
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-09-07T05:49:00Z'
    deadline_at: '2026-09-07T06:19:00Z'
    expected_output: Two source-free control packages and a bounded assessment of conditional compatibility.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --push
    kill_condition: A failed control blocks the target; author work ends before the integration reserve.
    fallback: Preserve the failed premise and separately price any changed instrument; do not run the target.
    outcome: Independent source-free instruments and swapped reviews pass; diamond reduction is reviewed and checkpoint961d9923 is published on PR109.
    evidence: [packing/devtools/p12_escape_candidate.py, packing/devtools/check_p12_escape_candidate.py, packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-conditional-compatibility-assessment.md]
    stop_reason: Reviewed readiness permits prospective registration; no target has run.
    next_action: Commit exp-121 and conduct its sole exact producer and independent reader.
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: Resolve the frozen H-110 candidate and choose the next conditional-cover or localization discriminator.
    commitment: BC-255
    bead: think-qv73
    status: in_progress
    entered_by: evidence_checkpoint
    switch_reason: Independent source-free controls and swapped reviews passed, and the integrated instrument checkpoint is published.
    budget_minutes: 30
    started_at: '2026-09-07T06:13:00Z'
    deadline_at: '2026-09-07T06:43:00Z'
    expected_output: Retained exact H-110 outcome, scoped scientific disposition and one evidence-selected prospective next task.
    validation_command: uv run --frozen --all-extras --group dev packing-ledger check
    kill_condition: A frozen scientific cap or guard fails, or the phase deadline arrives; never repeat a completed invocation.
    fallback: Record refusal or non-invocation and choose a changed future obligation without claiming mathematical rejection.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: Pass prospective record checks, commit exp-121, then invoke its producer exactly once.
  primary_bead: think-fqhr
  status: in_progress
  budget:
    wall_minutes: 120
    max_cycles: 4
    orientation_minutes: 10
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 20
  stop_conditions:
  - End each phase by its recorded deadline; reserve the last twenty minutes for checkpoint reconciliation.
  - No H-110 target invocation before independently reviewed controls and a committed prospective experiment.
  - A failed guard or incomplete receipt is unresolved, not evidence against the mathematical claim.
  - Never restart a completed scientific invocation or change its frozen budget after seeing evidence.
  - H-107 stays paused; exp-116 and the unchanged density source attempts are not retried.
  progress:
    metric: Independently checked structural obligations and actionable next proof contracts
    before: H-106, H-108 and H-109 accepted as auxiliary lemmas; H-110 instrument not ready; conditional compatibility and localization open.
    after: null
  delegations:
  - task: H-110 source-free producer and controls (think-h51i)
    operator: Codex angle_reader_recovery, max thinking
    status: completed
    recording: contemporaneous
    outcome: Frozen at 06:00:52 UTC; thirteen source-free controls pass, with no target invocation.
    evidence: [packing/devtools/p12_escape_candidate.py, packing/tests/test_p12_escape_candidate.py]
    files: [packing/devtools/p12_escape_candidate.py, packing/tests/test_p12_escape_candidate.py]
    checks: [13 tests pass; 0.30 seconds wall and 0.28 CPU, Ruff and format clean, BasedPyright clean; 0.82 seconds wall]
    uncertainty: Scientific validity is untested; independent review remains required.
    elapsed_seconds: 702
    elapsed_quality: operator_reported_approximate
    next_action: Independent swapped review, followed by coordinator readiness disposition.
    phase: 1
    budget_minutes: 20
    started_at: '2026-09-07T05:49:10Z'
    deadline_at: '2026-09-07T06:09:00Z'
    expected_output: Exact candidate producer, source-free tests, and a timed handoff.
    validation_command: uv run --frozen --no-sync pytest tests/test_p12_escape_candidate.py
    kill_condition: Deadline or an unproved instrument premise; no target run to debug the author work.
    fallback: Return the exact missing control and retained files without extending the allocation.
    write_scope: [packing/devtools/p12_escape_candidate.py, packing/tests/test_p12_escape_candidate.py]
    excluded_commands: [Scientific target constructors or candidate CLI invocation, Git or shared-record writes, Dependency changes or repo-wide gates]
  - task: H-110 independent corner reader and controls (think-x5sw)
    operator: Codex density_control_recovery, max thinking
    status: completed
    recording: contemporaneous
    outcome: Frozen at 06:01:51 UTC; twelve source-free controls pass, with no producer inspection or target reconstruction.
    evidence: [packing/devtools/check_p12_escape_candidate.py, packing/tests/test_check_p12_escape_candidate.py]
    files: [packing/devtools/check_p12_escape_candidate.py, packing/tests/test_check_p12_escape_candidate.py]
    checks: [12 tests pass; 0.51 seconds wall and 0.36 CPU, Ruff and format clean, BasedPyright clean; 1.02 seconds wall]
    uncertainty: Scientific validity is untested; independent review remains required.
    elapsed_seconds: 737
    elapsed_quality: operator_reported_approximate
    next_action: Independent swapped review, followed by coordinator readiness disposition.
    phase: 1
    budget_minutes: 20
    started_at: '2026-09-07T05:49:34Z'
    deadline_at: '2026-09-07T06:09:00Z'
    expected_output: Independent exact reader, refusal controls, and a timed handoff.
    validation_command: uv run --frozen --no-sync pytest tests/test_check_p12_escape_candidate.py
    kill_condition: Deadline, missing source binding or accidental dependence on the producer; no target evaluation.
    fallback: Return the exact readiness gap without running the candidate.
    write_scope: [packing/devtools/check_p12_escape_candidate.py, packing/tests/test_check_p12_escape_candidate.py]
    excluded_commands: [Reading or importing the producer, Scientific target evaluation, Git or shared-record writes, Dependency changes or repo-wide gates]
  - task: Conditional-compatibility proof assessment (think-ceb9)
    operator: Codex scalar_followup_assessment, max thinking
    status: completed
    recording: contemporaneous
    outcome: Closed at 06:02:31 UTC with independently reviewed diamond inclusion and closed-core counting reduction.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-conditional-compatibility-assessment.md]
    files: []
    checks: [Independent analytic review of projection inequalities and strict-sublevel counting, Global coordinate-reflection scope clarified; no target evaluation]
    uncertainty: Localization and both-band conditional coverage remain unproved.
    elapsed_seconds: 769
    elapsed_quality: operator_reported_approximate
    next_action: After H-110 disposition, select a prospective fixed-frame conditional-cover falsifier if warranted.
    phase: 1
    budget_minutes: 20
    started_at: '2026-09-07T05:49:42Z'
    deadline_at: '2026-09-07T06:09:00Z'
    expected_output: Read-only derivation with exact definitions, proof obligations and an evidence-based next allocation.
    validation_command: Independent mathematical review against H-106, H-108, H-109 and the strict-sublevel argument.
    kill_condition: Deadline, dependence on an unproved uniform clearance, or a claim needing a fresh measured target.
    fallback: State the missing premise and propose one bounded discriminator rather than a new framework.
    write_scope: [Read-only assessment; no file writes]
    excluded_commands: [Scientific target evaluation, File or shared-record writes, New hypothesis or experiment allocation]
  - task: Swapped H-110 producer review (think-uu0z)
    operator: Codex density_control_recovery, max thinking
    status: completed
    recording: contemporaneous
    outcome: GO at 06:06:19 UTC; no severity findings or scientific invocation.
    evidence: [packing/devtools/p12_escape_candidate.py, packing/tests/test_p12_escape_candidate.py]
    files: []
    checks: [13 source-free tests pass; 0.83 seconds wall, Ruff and format clean, BasedPyright clean; 2.14 seconds wall]
    uncertainty: This establishes instrument readiness, not the fixed candidate's mathematical outcome.
    elapsed_seconds: 100
    elapsed_quality: operator_reported_approximate
    next_action: Coordinator combines both reviews before prospective target registration.
    phase: 1
    budget_minutes: 10
    started_at: '2026-09-07T06:04:39Z'
    deadline_at: '2026-09-07T06:14:00Z'
    expected_output: Independent source-free producer readiness decision.
    validation_command: .venv/bin/python3 -m pytest tests/test_p12_escape_candidate.py
    kill_condition: A correctness finding or the ten-minute deadline ends review without authorizing the target.
    fallback: Return the precise unresolved premise for coordinator disposition.
    write_scope: [Read-only review; no file writes]
    excluded_commands: [Scientific target invocation, File or shared-record writes, Repo-wide gates]
  - task: Swapped H-110 corner-reader review (think-o6wj)
    operator: Codex angle_reader_recovery, max thinking
    status: completed
    recording: contemporaneous
    outcome: GO at 06:07:43 UTC; no soundness findings or target invocation.
    evidence: [packing/devtools/check_p12_escape_candidate.py, packing/tests/test_check_p12_escape_candidate.py]
    files: []
    checks: [12 source-free tests pass; 0.64 seconds wall and 0.28 CPU, Author lint/type/format evidence inspected]
    uncertainty: Requires an external whole-process cap; mathematical outcome remains untested.
    elapsed_seconds: 198
    elapsed_quality: operator_reported_approximate
    next_action: Coordinator records readiness and commits the prospective candidate test before dispatch.
    phase: 1
    budget_minutes: 10
    started_at: '2026-09-07T06:04:25Z'
    deadline_at: '2026-09-07T06:14:00Z'
    expected_output: Independent source-free reader readiness decision.
    validation_command: .venv/bin/python3 -m pytest tests/test_check_p12_escape_candidate.py
    kill_condition: A correctness finding or the ten-minute deadline ends review without authorizing the target.
    fallback: Return the precise unresolved premise for coordinator disposition.
    write_scope: [Read-only review; no file writes]
    excluded_commands: [Scientific target invocation, File or shared-record writes, Repo-wide gates]
  outputs:
  - packing/campaign/agent-sessions/session-091-structural-compatibility.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-conditional-compatibility-assessment.md
  - packing/devtools/p12_escape_candidate.py
  - packing/tests/test_p12_escape_candidate.py
  - packing/devtools/check_p12_escape_candidate.py
  - packing/tests/test_check_p12_escape_candidate.py
  checks:
  - Baseline 3c4fd4e2 has exactly the origin/main aae108a6 tree after PRs 105 and 106 merged.
  - Inherited merge evidence is composed fast validation plus a corrected shared-bead-tree check, not a fresh full checkpoint gate.
  - Instrument push gate took 135.71 seconds; all steps passed except two process-cleanup tests denied ps by the sandbox. Reachable tests recorded 627 passed, two failed, three deselected.
  - The two unchanged failed tests passed with process visibility in 4.67 seconds pytest, 4.98 seconds wall. This is composed push evidence, not a fresh full gate.
  stop_reason: null
  next_action: Complete the independently reviewed H-110 instrument under think-qv73, then prospectively register its sole candidate test.
---

# Exact P12 escape and conditional compatibility

This is the first autonomous two-active-hour continuation of Agenda 024, serving
BC-255/H-102. The user authorized continued work, with a reviewable checkpoint every
two hours. A checkpoint closes this bounded session, not that authorization.

## Allocation

| Slice | Work | Decision at the boundary |
| --- | --- | --- |
| First 30 minutes | Independent H-110 producer and reader controls; parallel conditional-theorem assessment | Ready for independent review, or a precise unresolved instrument obligation |
| Next 30 minutes | Review controls, commit a prospective experiment, and run the single fixed candidate only if ready | Accepted auxiliary counterexample, rejected fixed candidate, or unresolved instrument |
| Next 30 minutes | Select a narrow conditional-compatibility or localization obligation from the evidence | A proved lemma, a registered discriminator, or an explicit missing premise |
| Final 30 minutes | At most ten minutes of remaining research, then twenty minutes protected for integration | Records, validation, costs, PR checkpoint and one exact next action |

The coordinator owns shared records, IDs, integration and scientific disposition.
Workers have disjoint files and must return elapsed time, checks, uncertainty and a
resume instruction. Mathematical construction and review use max thinking; mechanical
follow-through may use high or extra-high thinking. The independent reader cannot read
or import the producer before its own implementation is complete.

Operational interruptions are not active research time. Record their actual boundaries
and preserve the original deadlines and scientific caps; any continuation is declared
prospectively, rather than rewriting the elapsed history.

## Scope and scientific guardrails

[H-110](../hypotheses/H-110-fixed-near-axis-p12-escape.md) fixes one near-axis unit
square and the unchanged twelve points. Its success would refute an unconditional P12
covering step, not produce eleven disjoint squares and not refute H-036 or H-102.
The frozen constructor is not a source-free test fixture. All twelve point identities,
closed boundary membership, box containment and the actual angle domain need checking.

The parallel assessment asks whether a near-45-degree square forced to contain
A1, A2 and A3 restricts the other squares enough for a conditional cover. A uniform
positive clearance is not established: scaling a strict-sublevel packing gives
interior slack for that packing, but the slack can vanish as its side approaches the
threshold. Neither this idea nor a single incompatible escape establishes a complete
conditional cover. Localization of the forced square remains a separate obligation.

H-107 remains paused. No unchanged exp-116 scalar retry or density-control retry is
allocated. Small numerical improvements remain recorded without complicating the core
exposition or displacing work toward stronger structural results.

The parallel [conditional assessment](../series/series-000-smoke-and-calibration/results/agenda-026/bc-255-conditional-compatibility-assessment.md)
now gives a fixed diamond contained in every distinguished square with the two forced
anchors. Its counting reduction needs no uniform clearance. Localization and a complete
nine-point cover for squares avoiding that diamond remain unproved.

## PR and parallel-agent handoff

Continue on `codex/structural-compatibility-continuation`, based on merged PRs 105 and
106. Publish one integrated successor PR early, then update it at each checkpoint.
Each update leads with measured cost (or an explicitly incomplete running lower bound),
states which checks actually ran, and links unfinished obligations and exact resume
commands. Beads are synchronized separately on `tbd-sync`; their IDs and scope are
mirrored here so a PR reader can recover the plan.

This branch has allocated **Session 091** and **exp-121**, and owns **H-110 / BC-255**.
No new hypothesis, agenda or exploration ID is allocated at this checkpoint.
The last audited external allocation is PR 107: X-017, Agenda 027, BC-258–268 and
H-111–117, with no session or experiment IDs. Its current head is `96be087f`;
PR 108 has merged into that branch and allocated no scientific IDs. Neither has landed
on main at this check.
Choose each next required ID sequentially after checking current remote claims;
publish it on this PR rather than reserving speculative ranges.

Merge only landed `origin/main` changes, following the upstream-merge shortcut.
Unmerged PRs 107 and 108 are coordination context, not prerequisites and not automatic
merge targets. If interrupted, read this session, its bead `think-fqhr`, the latest PR
checkpoint and the current H-110 record before dispatching anything. Never repeat a
completed or still-running scientific invocation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
