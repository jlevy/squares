---
title: session-006 — H-026 exact tangent screen
softschema:
  contract: packing.squares:AgentSession/v1
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-006
  title: Decide the branchwise linearized geometry of Trump’s exact packing
  date: '2026-08-24'
  goal: >-
    Turn H-026 into one finite, executable exact calculation with a complete active
    branch inventory, replayable certificates, known-answer controls, and a disciplined
    distinction between a linearized direction and a true feasible motion.
  focus: insight
  primary_bead: think-qd9t
  status: in_progress
  budget:
    wall_minutes: 180
    max_cycles: 4
  stop_conditions:
  - Exact active extraction disagrees with the independently verified 11 wall incidences or 14 pair contacts.
  - A zero-gap feature or one-sided support branch cannot be shown complete.
  - One exact normalized nonzero linearized direction is found, which rejects H-026 but only nominates nonlinear continuation.
  - Every unique branch receives a replayable exact zero-cone certificate, which confirms H-026 at first order.
  - The certificate or branch audit cannot be closed inside 180 agent-minutes, which leaves the round unresolved.
  progress:
    metric: exact Trump tangent branches with replayable terminal certificates
    before: H-026 names the corrected first-order question, but no active table, branch enumerator, or certificate instrument exists.
    after: The claim is pushed; two independent derivations agree on the complete finite inventory, and the exact instrument is implemented but not yet executed on this branch.
  delegations:
  - task: Independently derive every nonsmooth branch source and the finite exact certificate protocol
    operator: h026_exact_branch_audit
    status: completed
    outcome: Derived 20 wall rows, 24 raw SAT features, 512 raw selections, 128 derivative-distinct 42-row systems, and the positive-stress certificate protocol.
    evidence: [independent exact reconstruction of one branch certificate]
    files: []
    checks: [exact witness, wall incidences, pair features, one-sided derivatives, branch completeness]
    uncertainty: The retained checker still has to replay every branch after it is committed and pushed.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Complete the read-only delta audit of the retained instrument before execution.
  - task: Inventory reusable exact tooling and design the smallest executable checker and controls
    operator: h026_tooling_inventory
    status: completed
    outcome: Independently prototyped all 128 exact positive-stress certificates in 21.40 wall seconds and specified the minimum retained record and omission control.
    evidence: [128 exact Q(u) stress replays, exact wall-omission direction]
    files: []
    checks: [number-field arithmetic, exact verifier, contact extraction, LP tooling, schema and result contracts]
    uncertainty: The prototype is not retained evidence; only the committed checker run can decide exp-013.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Run the retained generator and its separate exact replay after the instrument commit is pushed.
  outputs:
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-013-h-026-trump-tangent.md
  - campaign/series/series-000-smoke-and-calibration/results/exp-013-h-026-trump-tangent.json
  - tools/check_trump_tangent.py
  checks:
  - Claim schema and ledger integration passed before the instrument was built; static instrument checks are pending.
  stop_reason: null
  next_action: >-
    Commit and push the reviewed instrument, then execute its retained generator and
    separate exact replay once from a clean tree.
---
# Session 006 — exact first-order geometry

The intended loop is derivation-heavy and compute-light.
The expensive part is proving that the finite model is the right tangent model; once
that is fixed, every branch should decide in seconds or less.

The stop rule protects against the central category error: the linearized cones
overapproximate the true Bouligand tangent.
A nonzero vector is not yet a feasible motion; a zero union is strong enough to justify
a separate finite-branch local-isolation argument, which this round will not silently
assume.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
