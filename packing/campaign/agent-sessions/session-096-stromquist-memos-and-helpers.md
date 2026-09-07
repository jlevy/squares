---
title: session-096 — Stromquist memos and systematic dots proofs
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-096
  title: Stromquist memos and systematic dots proofs
  date: '2026-09-07'
  started_at: '2026-09-07T16:09:58Z'
  branch: codex/stromquist-memos-and-helper-arguments
  resource_rollups: [packing/campaign/resource-usage/codex-task-tree-session-096.yaml]
  goal: Review all three Stromquist memos against the current explainer, correct source history, and pursue independently checked helper and pure-dots arguments without promoting a packing bound.
  workflow_phases:
  - workflow: research-survey
    focus: correctness
    recording: retrospective
    objective: Locate and inspect the three primary memos, compare the live explainer, and distinguish likely author hints from confirmed corrections.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: null
    deadline_at: null
    expected_output: Page-specific archive reading aids and ranked paper corrections.
    validation_command: packing-validate --records
    kill_condition: Unavailable or illegible primary evidence leaves the corresponding attribution unresolved.
    fallback: Retain exact source uncertainty without changing proof status or numerical bounds.
    outcome: All 47 pages reviewed; 1984 eleven-square statement and ten-square proof confirmed, along with construction credits, formula slips, and historical limits.
    evidence: [docs/project/research/research-2026-09-07-stromquist-memos-and-helper-arguments.md, packing/resources/README.md]
    stop_reason: Three linked memos and current explainer compared in full at the relevant claims.
    next_action: Derive the useful mathematical implications and state all geometric dependencies.
  - workflow: insight-iteration
    focus: insight
    recording: retrospective
    objective: Derive conditional weighted counting, assess symmetry, and make the email's five-dot limitation precise.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: The source review identifies forced occupancy and unweighted piercing as separate mathematical questions.
    budget_minutes: 30
    started_at: null
    deadline_at: null
    expected_output: Independently reviewed analytic statements with precise open/closed and unweighted/weighted scope.
    validation_command: Independent mathematical review recorded in the incorporation review.
    kill_condition: A failed geometric case, boundary equality or unstated hypothesis prevents accepting the affected proposition.
    fallback: Retain the missing premise and stop short of a theorem or packing-bound promotion.
    outcome: Reviewed conditional mass inequality, D4 averaging, arbitrary-five-point obstruction, rational 101/100 control and open-unit endpoint (12+2sqrt(2))/5; no packing bound changed.
    evidence: [docs/project/stromquist-helper-arguments-math-review.md, docs/project/reviews/review-2026-09-07-n6-pure-dots-obstruction.md, docs/project/reviews/review-2026-09-07-n6-quantitative-piercing-bound.md, docs/project/reviews/review-2026-09-07-stromquist-incorporation.md]
    stop_reason: Independent proof review accepted the statements at their declared scopes.
    next_action: Commission exact finite controls while keeping the geometric premises explicit.
  - workflow: pipeline-improvement
    focus: correctness
    recording: retrospective
    objective: Build reusable incidence and escape-square tools and validate them against independent finite oracles.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: The finite Memo I allocation and rational escape construction have precise, bounded verification contracts.
    budget_minutes: 30
    started_at: null
    deadline_at: null
    expected_output: Retained exact controls, premise-removal results, independent tests and documented evidence limits.
    validation_command: .venv/bin/pytest -q tests/test_incidence.py tests/test_stromquist_memo1.py tests/test_stromquist_five_point_obstruction.py
    kill_condition: Disagreement with the independent oracle, shared-site ownership, invalid exact geometry or an unverified premise blocks acceptance.
    fallback: Keep the failed control and missing premise without treating commissioning as a target experiment.
    outcome: Memo I finite assumptions yield four allocations in one D4 orbit; forced occupancy returns five. Rational escape tool checks strict closed-square avoidance. All 19 focused tests passed independently.
    evidence: [packing/src/sqpack/incidence.py, packing/cases/stromquist/memo1-incidence.json, packing/cases/stromquist/five-point-obstruction.json]
    stop_reason: Finite arithmetic and exact outputs were accepted at 9d69032c; diagram ownership and replay were integrated at dd92b2a0.
    next_action: Complete integrated validation and record the remaining geometric replay dependency.
  - workflow: documentation-pass
    focus: correctness
    recording: retrospective
    objective: Validate the reviewed research checkpoint, retain its cost, and prepare the source-directed geometric handoff and review publication.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: Scientific and instrument outputs are committed; final source-method corrections, integration validation and the publication handoff remain.
    budget_minutes: 30
    started_at: null
    deadline_at: null
    expected_output: Passing full validation, a reviewable branch and recoverable next dependency.
    validation_command: packing-validate
    kill_condition: A validation failure requires diagnosis and correction; the planning time is not authority to leave requested work unfinished.
    fallback: Retain the exact failed check and continue resolving it; do not claim the checkpoint passed.
    outcome: All 66 full-checkpoint steps passed at dd92b2a0 in 1360.51 seconds. Final prose, source-method and session-record changes receive the pre-push floor before review publication.
    evidence: [docs/project/research/research-2026-09-07-stromquist-memos-and-helper-arguments.md]
    stop_reason: The source review and bounded mathematical follow-up are complete and independently reviewed; remaining geometric replay is explicitly handed off.
    next_action: Finish validation, close the review record and publish the review branch.
  primary_bead: think-7u4s
  status: completed
  budget:
    wall_minutes: 120
    slice_minutes: 30
  stop_conditions:
  - Complete the source audit, independently checked bounded follow-up and integration; planning estimates are not stop authority.
  - Do not promote finite controls into continuum proofs or a new packing bound.
  - Preserve the existing BC264/H114 target-research handoff; source-directed helper work does not reopen H124.
  progress:
    metric: Confirmed source corrections and independently checked mathematical components
    before: Three memos were archived with short reading aids; the live explainer dated the prior eleven-square bound and ten-square proof to 2003, and the author's five-dot observation had no retained proof.
    after: Three reading aids expanded; paper chronology and construction credit corrected; analytic five-dot barrier, complete local segment-helper proof and reusable source-premised incidence control independently reviewed. D479 corrects five case summaries that substituted pure dots counting for the cited helper methods; source-method metadata and El Moumni archive links are repaired.
  delegations:
  - task: Review all Stromquist sources and implement exact five-point escape controls
    operator: Codex stromquist_sources, max thinking
    status: completed
    recording: retrospective
    outcome: Inspected all 47 scanned pages, expanded reading aids, checked related small-case proof descriptions and implemented the independently reviewed rational escape constructor with JSON and SVG.
    evidence: [packing/resources/README.md, packing/cases/stromquist/five_point_obstruction.py]
    files: [packing/resources/README.md, packing/cases/stromquist/five_point_obstruction.py, packing/tests/test_stromquist_five_point_obstruction.py]
    checks: [Eleven focused tests passed; Ruff and BasedPyright clean; independent combined suite passed.]
    uncertainty: Original intern identity, unpublished pure-dots proof and possible fourth memo remain unlocated.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Preserve the historical n18 attribution discrepancy for an author clarification.
  - task: Derive helper arithmetic, implement Memo I allocation control and refine the piercing obstruction
    operator: Codex helper_math, max thinking
    status: completed
    recording: retrospective
    outcome: Implemented exact incidence tools and independent controls; derived the rational and algebraic piercing bounds and verified the published upper-bound interval.
    evidence: [docs/project/stromquist-helper-arguments-math-review.md, docs/project/reviews/review-2026-09-07-n6-quantitative-piercing-bound.md]
    files: [packing/src/sqpack/incidence.py, packing/cases/stromquist/memo1.py, packing/tests/test_incidence.py, packing/tests/test_stromquist_memo1.py]
    checks: [Eight focused tests passed; Ruff and BasedPyright clean; analytic proofs independently reviewed.]
    uncertainty: A complete geometric replay of the source helpers remains separate from the finite allocation control.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Carry the source-directed segment helper to think-0krc.
  - task: Independently audit paper corrections, analytic proofs and exact controls
    operator: Codex paper_audit, max thinking
    status: completed
    recording: retrospective
    outcome: Accepted the ranked historical corrections, source-premised finite counting, arbitrary-five analytic obstruction, rational closed-square construction and explicit sufficient open endpoint.
    evidence: [docs/project/reviews/review-2026-09-07-stromquist-incorporation.md]
    files: [docs/project/reviews/review-2026-09-07-stromquist-incorporation.md]
    checks: [Nineteen combined tests passed in 0.56 seconds under project Python 3.14.7; no unresolved soundness findings.]
    uncertainty: Threshold optimality and the provenance of Stromquist's original argument are not established.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Preserve the analytic and finite-test distinction in final integration.
  - task: Independently derive and review Memo I's local segment helper
    operator: Codex paper_audit and helper_math, max thinking, independent source derivations
    status: completed
    recording: retrospective
    outcome: Complete local analytic proof of the greater-than-half demand and less-than-half accessible capacity, including independent angles, wall premises, all cap cases, axis endpoints and actual-edge validity. The coordinator integrated the reviewed four-facet clarification.
    evidence: [docs/project/reviews/review-2026-09-07-stromquist-segment-helper.md]
    files: [docs/project/reviews/review-2026-09-07-stromquist-segment-helper.md]
    checks: [Independent symbolic derivations and mutual review; no numerical target, sampled-angle proof or consumer expansion.]
    uncertainty: Executable clipping and universal inequality certificates, Lemmas6–7, exact-two-mark adjacency and the final forced marks and cover remain separate.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Preserve the proved local helper and continue the remaining dependencies under think-0krc.
  outputs:
  - docs/project/research/research-2026-09-07-stromquist-memos-and-helper-arguments.md
  - packing/devtools/templates/explainer-article.md
  - packing/cases/stromquist/memo1-incidence.json
  - packing/cases/stromquist/five-point-obstruction.json
  - docs/project/reviews/review-2026-09-07-stromquist-segment-helper.md
  checks:
  - Nineteen new focused tests passed independently; 51 tests covering the first two new modules and the explainer also passed before the final escape module was added.
  - The pre-push tier at 9d69032c passed all 45 selected steps in 80.31 seconds, including the reachable behavioral tests.
  - Revised explainer PDF rendered locally with temporary headless Chrome; print-layout checks passed and pages 1, 2, 4, 11, 12, 14 and 15 were visually inspected.
  - 'full gate: full at dd92b2a0: passed (all 66 steps passed in 1360.51 seconds; native process session 94559 exited zero, observed by root at 17:34 UTC; final source-method, prose and session-record deltas receive separate pre-push validation)'
  - First full checkpoint at 9d69032c passed 62 of 66 steps in 315.93 seconds. The new SVG lacked an ownership registration; all three behavioral lanes failed collection because macOS's existing libcairo was not on the loader path. Diagram ownership and replay were added, and the documented DYLD_FALLBACK_LIBRARY_PATH was used for the subsequent checkpoint.
  stop_reason: Research checkpoint completed, with full validation and a specific geometric replay dependency; review publication follows the local close record.
  next_action: After the final pre-push check and review publication, preserve BC-264 under think-mq0d as the existing H114 feature and kernel-contract pricing entry. The source brief separately retains the geometric replay dependency; this review activates no new target or unchanged retry.
---
# Stromquist Memos and Systematic Dots Proofs

The
[research brief](../../../docs/project/research/research-2026-09-07-stromquist-memos-and-helper-arguments.md)
contains the source findings, independent derivations and remaining geometric
dependency. This record accounts for the review and integration; it creates no campaign
hypothesis, experiment or packing-bound verdict.

The workflow entries were reconstructed from the working brief and agent receipts at
integration.
Their slice estimates were declared in the brief, but exact phase-transition
clocks were not retained; null clocks preserve that limitation.
The task-tree receipt measures the aggregate interval and does not supply invented
individual delegation durations.
Its branch attribution is operator-recorded.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
