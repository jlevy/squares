---
title: session-082 — BC-141 n = 54 source-cell contract
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-082
  title: BC-141 n = 54 source-cell contract
  date: '2026-09-02'
  started_at: '2026-09-02T08:23:00Z'
  deadline_at: '2026-09-02T11:23:00Z'
  branch: claude/squares-pr-73-resume-5lp3bz
  goal: >-
    Freeze, implement, mutate and independently review a target-blind parser and
    labeled-correspondence contract for the declared n = 54 source structure using only
    a synthetic fixture and the readmitted quartic-field receipt. Do not fetch, retain
    or interpret the live source; inspect target geometry; or move H-055 from
    instrument-unready.
  workflow_phases:
  - workflow: insight-iteration
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Execute BC-141's fixed 180-minute sequence: freeze the parser grammar, 27 plus
      half-turn label rule, D4 action, orientation convention, field binding and witness
      correspondence semantics; implement them against a synthetic fixture; obtain a
      different-lane review; add geometry-structure and correspondence mutations plus a
      no-import verifier; obtain final readmission; and retain the contract or its first
      typed refusal.
    commitment: BC-141
    bead: think-pkgx
    status: in_progress
    entered_by: session_start
    switch_reason: null
    budget_minutes: 180
    started_at: '2026-09-02T08:23:00Z'
    deadline_at: '2026-09-02T11:23:00Z'
    expected_output: >-
      One frozen, independently reviewed parser and correspondence contract over a
      synthetic fixture, with a geometry-structure mutation and a correspondence
      mutation both refused, or an exact typed refusal naming the first unsound seam.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n54_source_contract.py tests/test_n54_source_contract_independent.py
    kill_condition: >-
      Stop on live-source, network, retained-source, target-witness, n = 54 geometry or
      production-parser access; acceptance of an incomplete or ambiguous formula;
      unsafe expression evaluation; a non-bijective label map; D4 or orientation drift;
      field-receipt drift; a mutation that passes; or independent replay disagreement.
    fallback: >-
      Retain `exact-source-parser-and-labeled-correspondence-absent`, leave H-055
      instrument-unready and the live source unretained, and do not run n = 39 design or
      n = 54 geometry.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: >-
      Use the first 20 minutes to freeze the contract with one Max judge and two XHigh
      read-only reviewers before any implementation write.
  primary_bead: think-pkgx
  status: in_progress
  budget:
    wall_minutes: 180
    max_cycles: 8
    orientation_minutes: 20
    checkpoint_minutes: 25
    slice_minutes: 25
    finalization_minutes: 0
  stop_conditions:
  - The fixed 2026-09-02T11:23:00Z wave-two boundary arrives.
  - The synthetic fixture cannot preserve the declared comment-formula structure without source interpretation.
  - A parser would require eval, exec, SymPy parse_expr or sympify, or XML entity expansion.
  - A frozen contract field, label, action, orientation rule, receipt hash or mutation would have to change.
  - An independent verifier or a named mutation disagrees with the author-side result.
  progress:
    metric: refusable target-blind n = 54 source-cell and labeled-correspondence contract
    before: >-
      BC-140's two n = 54 negative controls and complete frozen-input inventory are
      independently readmitted, but no parser, 54 stable labels, D4 convention,
      source-to-witness bijection or independent contract verifier exists.
    after: null
  delegations:
  - task: Freeze the mathematical and semantic contract
    operator: Codex Max contract judge
    status: in_progress
    recording: contemporaneous
    outcome: null
    evidence: null
    files: null
    checks: null
    uncertainty: null
    elapsed_seconds: null
    elapsed_quality: null
    next_action: Return Artifact / Result / Guard / Next without writing files.
    phase: 1
    budget_minutes: 20
    started_at: '2026-09-02T08:23:00Z'
    deadline_at: '2026-09-02T08:43:00Z'
    expected_output: >-
      A decision on the closed grammar, 27 plus half-turn labels, exact D4 and
      orientation semantics, field binding, bijection rule and ambiguity refusals.
    validation_command: Read-only comparison against the agenda, H-055 and the audited field receipt.
    kill_condition: Stop on any need to inspect source, target, geometry or network state.
    fallback: Name the first contract element that cannot be frozen target-blind.
    write_scope:
    - No repository writes; read-only review.
    excluded_commands:
    - source or network access
    - target or geometry execution
    - Git, tbd or repository-wide validation writes
  - task: Audit implementation patterns and package boundaries
    operator: Codex XHigh implementation-pattern auditor
    status: in_progress
    recording: contemporaneous
    outcome: null
    evidence: null
    files: null
    checks: null
    uncertainty: null
    elapsed_seconds: null
    elapsed_quality: null
    next_action: Return Artifact / Result / Guard / Next without writing files.
    phase: 1
    budget_minutes: 20
    started_at: '2026-09-02T08:23:00Z'
    deadline_at: '2026-09-02T08:43:00Z'
    expected_output: >-
      A target-blind package and test layout using safe closed parsing, canonical JSON
      and an independent no-import verifier.
    validation_command: Read-only inspection of existing refusable-tool and verifier patterns.
    kill_condition: Stop if a proposed pattern imports production parsing into the independent verifier.
    fallback: Return the narrowest safe reusable seams and name all rejected patterns.
    write_scope:
    - No repository writes; read-only review.
    excluded_commands:
    - source or network access
    - target or geometry execution
    - Git, tbd or repository-wide validation writes
  - task: Design the independent mutation and replay matrix
    operator: Codex XHigh verifier planner
    status: in_progress
    recording: contemporaneous
    outcome: null
    evidence: null
    files: null
    checks: null
    uncertainty: null
    elapsed_seconds: null
    elapsed_quality: null
    next_action: Return Artifact / Result / Guard / Next without writing files.
    phase: 1
    budget_minutes: 20
    started_at: '2026-09-02T08:23:00Z'
    deadline_at: '2026-09-02T08:43:00Z'
    expected_output: >-
      A no-import replay plan and named controls for formula ambiguity, label coverage,
      half-turn/D4 collisions, field drift, geometry structure and correspondence.
    validation_command: Read-only inspection of independent verifier and mutation tests.
    kill_condition: Stop if a control requires source contents, witness geometry or production imports.
    fallback: Return the minimum independent matrix that still proves both required mutations load-bearing.
    write_scope:
    - No repository writes; read-only review.
    excluded_commands:
    - source or network access
    - target or geometry execution
    - Git, tbd or repository-wide validation writes
  outputs:
  - packing/campaign/agent-sessions/session-082-bc141-n54-source-contract.md
  checks:
  - >-
    BC-143 routed only the independently readmitted n = 54 controls and frozen-input
    inventory; BC-139 remains stopped and no substitute target is authorized.
  - >-
    H-055 remains instrument_ready false; this session can validate a prospective
    source-cell contract but cannot establish source completeness, exact geometry,
    feasibility, optimality or a packing bound.
  stop_reason: null
  next_action: >-
    Complete BC-141 under think-pkgx: finish the 08:23--08:43Z contract freeze, then
    either admit the first implementation slice or retain the exact typed refusal.
---
# Session 082 — BC-141 `n = 54` Source-Cell Contract

This lane is target-blind.
Its only admissible scientific inputs are the retained audit README, the byte-stable
quartic-field receipt and BC-140’s two readmitted controls.
The fixture is synthetic and must express structure rather than copy or infer the live
SVG.

The contract may prove that a prospective parser and label map are refusable.
It cannot prove that the synthetic fixture matches the unretained source, that the
retained decimal witness corresponds to those labels, or that 54 squares form a valid
packing.

## 00:00--00:20 (08:23--08:43Z) — Contract Freeze

- **Artifact:** session-082 and three queued read-only reviews at Max/XHigh effort.
- **Result:** pending.
- **Guard:** no source, network, target, geometry or implementation write is authorized
  until the contract reviews return.
- **Next:** reconcile the closed grammar, labels, D4/orientation convention, field
  binding, bijection rule and mutation matrix without changing the frozen lane scope.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
