---
title: session-006 — H-026 exact tangent screen
softschema:
  contract: packing.squares:AgentSession/v1
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-006
  title: Decide the generalized first-order geometry of Trump’s exact packing
  date: '2026-08-24'
  goal: >-
    Turn H-026 into one finite, executable exact calculation with a complete active
    branch inventory, replayable certificates, known-answer controls, and a disciplined
    verdict that does not overclaim nonlinear rigidity.
  focus: insight
  primary_bead: think-qd9t
  status: in_progress
  budget:
    wall_minutes: 180
    max_cycles: 4
  stop_conditions:
  - Exact active extraction disagrees with the independently verified 11 wall incidences or 14 pair contacts.
  - A zero-gap feature or one-sided support branch cannot be shown complete.
  - One exact normalized nonzero branch direction is found, which rejects H-026 immediately.
  - Every unique branch receives a replayable exact zero-cone certificate, which confirms H-026 at first order.
  - The certificate or branch audit cannot be closed inside 180 agent-minutes, which leaves the round unresolved.
  progress:
    metric: exact Trump tangent branches with replayable terminal certificates
    before: H-026 names the corrected first-order question, but no active table, branch enumerator, or certificate instrument exists.
    after: The round is claimed; independent branch and tooling audits are running before the instrument is implemented.
  delegations:
  - task: Independently derive every nonsmooth branch source and the finite exact certificate protocol
    operator: h026_exact_branch_audit
    status: in_progress
    outcome: Running; no result has been imported into the parent analysis yet.
    evidence: []
    files: []
    checks: [exact witness, wall incidences, pair features, one-sided derivatives, branch completeness]
    uncertainty: Branch counts and a certificate form remain to be derived independently.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Compare the independent derivation against the parent instrument before any verdict.
  - task: Inventory reusable exact tooling and design the smallest executable checker and controls
    operator: h026_tooling_inventory
    status: in_progress
    outcome: Running; no implementation recommendation has been imported yet.
    evidence: []
    files: []
    checks: [number-field arithmetic, exact verifier, contact extraction, LP tooling, schema and result contracts]
    uncertainty: The smallest independently replayable infeasibility certificate is not yet selected.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Use the inventory to avoid duplicating exact arithmetic or trusting a floating LP verdict.
  outputs:
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-013-h-026-trump-tangent.md
  - campaign/series/series-000-smoke-and-calibration/results/exp-013-h-026-trump-tangent.json
  - tools/check_trump_tangent.py
  checks:
  - Claim schema, ledger integration, and clean-tree provenance pending.
  stop_reason: null
  next_action: >-
    Commit and push the claim, then build the active-feature and exact certificate
    checker without inspecting a scientific outcome first.
---
# Session 006 — exact first-order geometry

The intended loop is derivation-heavy and compute-light.
The expensive part is proving that the finite model is the right tangent model; once
that is fixed, every branch should decide in seconds or less.

The stop rule protects against the central category error: a first-order zero cone is
evidence of first-order rigidity, not a proof of nonlinear isolation or optimality.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
