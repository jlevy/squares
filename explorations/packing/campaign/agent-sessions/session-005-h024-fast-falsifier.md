---
title: session-005 — H-024 fast falsifier
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-005
  title: Reconstruct the n = 29 source witness and decide H-024
  date: '2026-08-24'
  goal: >-
    Complete one preregistered, independently checked, high-information research round
    on the new main-based branch and leave its instrument, source, raw result, verdict,
    successor, logbook entry, and execution cost durable.
  workflow_phases:
  - workflow: research-loop
    focus: insight
    recording: retrospective
    objective: Run H-024's cheapest source-bound falsifier and retain every result.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: null
    started_at: null
    deadline_at: null
    expected_output: null
    validation_command: null
    kill_condition: null
    fallback: null
    outcome: Exp-012 found six orientation classes and refuted H-024 at its first stop cell.
    evidence:
    - The source witness reconstructs and passes the independent separating-axis guard.
    - The terminal artifact records 0.158 machine-seconds and routes H-025 as successor.
    stop_reason: One verified witness exceeded three classes and met the kill condition.
    next_action: Move the portfolio to H-026 or H-032; do not rerun H-024.
  primary_bead: think-w5rb
  status: completed
  budget:
    wall_minutes: 45
    max_cycles: 3
  stop_conditions:
  - The retained SVG does not reconstruct to exactly 29 unit squares.
  - The independent separating-axis guard rejects the reconstructed witness.
  - Orientation intervals overlap, so the class count is ambiguous.
  - One verified witness exceeds three classes, which refutes the universal claim immediately.
  progress:
    metric: decided fast-first hypotheses with retained executable evidence
    before: H-024 was a registered six-class counterexample candidate with no retained source, importer, or experiment.
    after: >-
      Exp-012 reconstructs and numerically verifies all 29 squares, finds six disjoint
      classes, refutes H-024 in 0.158 machine-seconds, and promotes H-025's quantitative
      compressibility pilot. The pushed result passes the 25-step strict/deep gate with
      31 negative controls and 135 reconciled defects.
  delegations:
  - task: Rank the five smallest proposed research rounds by readiness and information per agent-minute
    operator: fast_first_run_selector
    status: completed
    outcome: >-
      Ranked H-026 first for mathematical depth, H-032 second, and H-024 third; exposed
      that all three need generic categorical determination outcomes rather than the
      campaign's search-only basin labels.
    evidence:
    - H-026 already has an exact Trump witness and SAT verifier but needs a complete branch derivation.
    - H-024 had a direct primary-source falsifier but no retained source or importer.
    files: []
    checks: [registry, tooling, dependency, and bead cross-check]
    uncertainty: H-026's seconds of LP solve time hide one to three agent-hours of branch derivation and certificate audit.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Run H-026 next with branch completeness as the guarded deliverable.
  - task: Independently derive the n = 29 square formulas, transform order, class counts, and numerical validity margins
    operator: n29_svg_independent_derivation
    status: completed
    outcome: >-
      Reconstructed 15 aligned and 14 rotated squares, independently obtained class
      multiplicities 15/1/9/1/2/1, confirmed SVG matrix order, and matched the final
      checker's 4.05464e-101 worst nominal penetration.
    evidence:
    - Live primary SVG SHA-256 30c725b27e1b90ff0c9c238fb8923c3da6ce26e046cdd46d5c33a485bbec821c.
    - Minimum class gap a-d is 0.296067318913687 degrees.
    - Smallest strict SAT separation is about 0.03617094266289048.
    files: []
    checks: [independent 120-digit reconstruction, all 406 SAT pairs, nine offsets, six source equations]
    uncertainty: The SVG serializes a high-precision numerical root; it is not an interval or symbolic certificate of the record value.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Keep the six-class determination numerical and separately certify exactness only if a later claim needs it.
  - task: Apply mechanical formatting, Ruff, and BasedPyright cleanup to the new checker
    operator: n29_checker_lint
    status: completed
    outcome: >-
      Formatted the checker and removed only mechanical lint/type issues without running
      or interpreting the experiment.
    evidence: []
    files: [tools/check_kingbird_svg.py]
    checks: [Ruff format, Ruff check, BasedPyright, git diff-check]
    uncertainty: None beyond the semantic review and source replay owned by the parent.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Re-run the same mechanical checks after any semantic checker edit.
  outputs:
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-012-h-024-n29-angle-classes.md
  - campaign/series/series-000-smoke-and-calibration/results/exp-012-h-024-n29.json
  - resources/papers/kingbird-square-29-provenance.svg
  - tools/check_kingbird_svg.py
  - campaign/hypotheses/H-024-record-angle-class-count.md
  - frontier/n-029.md
  - defects.yaml D-133 through D-135
  - think-d4hm H-025 pilot successor
  checks:
  - The final exp-012 replay checked 29 squares and all 406 pairs at 160 decimal digits in 0.157556 wall-seconds.
  - Schema, ledger, synopsis, README, defect view, and six generated frontier tables agree.
  - Ruff format, Ruff check, and BasedPyright pass on the source checker with zero warnings.
  - The generic-determination and defect-count mutation controls both fire under isolated replay.
  - The focused frontier-corpus step replays the source equations, validity guard, and six class multiplicities.
  - The strict/deep gate passes all 25 steps, 31 negative controls, and 135 defects in 38 wall-seconds.
  stop_reason: >-
    H-024's preregistered first falsifier fired: one valid reconstructed witness has six
    disjoint classes against the universal upper bound of three. Continuing the n <= 30
    sweep would spend the session on a dead criterion, so the work stopped and moved
    the surviving compression question to H-025.
  next_action: >-
    Begin H-026 from Trump's exact active-contact table, with complete one-sided branch
    enumeration and replayable tangent-cone certificates as the guarded deliverable.
---
# Session 005 — fast result before broad expansion

The round spent human-scale effort once to make a subsecond mathematical check durable.
That is the intended loop shape: use a primary-source falsifier early, stop on the first
decisive cell, and move the surviving mechanism—not the refuted slogan—forward.

H-024’s literal three-class law is dead.
H-025’s bounded-loss compression hypothesis and H-026’s exact tangent screen are the
next distinct questions; neither inherits more confidence than exp-012 earned.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
