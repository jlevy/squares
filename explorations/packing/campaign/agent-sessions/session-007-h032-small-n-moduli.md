---
title: session-007 — H-032 exact small-n moduli controls
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-007
  title: Classify and render the complete optimal spaces at n = 3 and n = 4
  date: '2026-08-24'
  goal: >-
    Establish two exhaustive, replayable ground-truth cells for the landscape atlas:
    the full arbitrary-rotation n = 3 family with every quotient stratum, and the rigid
    n = 4 grid quotient, while binding both to the directly relevant primary literature.
  workflow_phases:
  - workflow: research-loop
    focus: insight
    recording: retrospective
    objective: Classify and render the exact n=3 and n=4 optimal moduli controls.
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
    outcome: Exp-014 and exp-015 exhaustively classified both declared sweep cells.
    evidence:
    - The n=3 quotient interval and n=4 quotient point replay in under one second.
    - The deterministic SVG and 15 mutation controls preserve the declared distinctions.
    stop_reason: Both preregistered cells met their exhaustive exact criteria.
    next_action: Define the complete n=5 component relation before extending H-032.
  primary_bead: think-n82j
  status: completed
  budget:
    wall_minutes: 180
    max_cycles: 4
  stop_conditions:
  - A valid genuinely rotated side-2 packing at n = 3 or n = 4 rejects the proposed reduction.
  - The primary configuration-space papers cannot be recovered and checked, which blocks prior-art comparison but not a clearly scoped independent derivation.
  - The exact labelled cell counts, group quotients, stabilizers, or stratum incidences disagree across derivation and implementation.
  - Deterministic semantic and SVG replay passes for n = 3 and the exact 24-state replay passes for n = 4.
  - The classification or replay cannot be closed inside 180 agent-minutes, which leaves the affected cell unresolved.
  progress:
    metric: H-032 sweep cells with exhaustive classification, exact replay, and readable quotient maps
    before: H-032 has no filled cells, its instrument is absent, and the archive omits the literature directly about hard-square configuration spaces.
    after: Exp-014 exactly classifies the full n = 3 space and renders its quotients; exp-015 exactly classifies the rigid n = 4 cell. Both replay in under one second, while n = 5 and n = 6 remain open.
  delegations:
  - task: Independently derive the full arbitrary-rotation n = 3 classification and its quotient topology
    operator: h032_exact_math
    status: completed
    outcome: Derived the orientation-forcing lemma, two labelled circles, the unlabelled circle, the quotient interval and stabilizers, plus the rigid n = 4 corollary.
    evidence: [independent analytic proof, exact labelled-cell enumeration, primary-literature inventory]
    files: []
    checks: [orientation equality case, axis-aligned compatibility, labelled monodromy, D4 x S3 orbit types, n = 4 corollary]
    uncertainty: The derivation is not retained executable evidence until the parent checker and source archive replay it.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Compare the implementation and retained result against every derived count and scope boundary.
  - task: Design the smallest deterministic quotient and stratum visualization with executable checks
    operator: h032_visual_tooling
    status: completed
    outcome: Specified the full interval quotient, its C/G/M strata, exact active signatures and stabilizers; the retained SVG encodes the two labelled circles, unlabelled cycle, quotient interval, and packing glyphs.
    evidence: [exact separation enumeration, D4 action, deterministic SVG replay]
    files: [atlas/n-003-optimal-moduli.svg]
    checks: [labelled circles, S3 quotient, D4 quotient interval, stabilizers, contact and wall strata, representative glyphs]
    uncertainty: The map is a complete n = 3 semantic control, not a general high-dimensional basin renderer.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Reuse the stratum vocabulary and visual grammar only after the n = 5 component relation is defined.
  - task: Archive and route all directly relevant primary hard-square configuration-space papers
    operator: archive_hard_square_configuration_literature
    status: completed
    outcome: Archived Alpert et al. and Alvarado-Garduño–González with exact source hashes; verified that a candidate institutional Plakhta mirror contained a different paper and retained the publisher blocker.
    evidence: [two official primary PDFs, byte-faithful raw extractions, rejected mirror identity]
    files: [resources/papers/alpert-bauer-kahle-macpherson-spendlove-2023-hard-squares-configuration-spaces.pdf, resources/papers/alvarado-garduno-gonzalez-2025-square-section-braid-groups.pdf]
    checks: [official source provenance, PDF hashes, raw extraction preservation, claim routing]
    uncertainty: Plakhta 2021 remains unavailable, so no novelty comparison is complete.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Retrieve Plakhta from a verified primary copy before making a novelty claim.
  outputs:
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-014-h-032-n3-optimal-moduli.md
  - campaign/series/series-000-smoke-and-calibration/results/exp-014-h-032-n3-optimal-moduli.json
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-015-h-032-n4-optimal-moduli.md
  - campaign/series/series-000-smoke-and-calibration/results/exp-015-h-032-n4-optimal-moduli.json
  - tools/check_small_n_moduli.py
  - atlas/n-003-optimal-moduli.svg
  checks:
  - The orientation-forcing identity and strictness control pass before both cell enumerations.
  - Exp-014 enumerates 64 raw choices, 24 labelled one-cells, two labelled circles, one unlabelled circle, and the D4 x S3 interval with all declared strata.
  - Exp-015 enumerates 4,096 raw choices, 96 consistent zero-cells, and 24 labelled grids reducing to one quotient point.
  - All 15 mutation and source-scope controls pass; semantic replay is complete and the n = 3 SVG is byte-identical.
  - Generation plus replay costs 0.63 wall seconds at n = 3 and 0.65 seconds at n = 4.
  stop_reason: Both separately preregistered cells met their exhaustive exact criteria; H-032 remains open only for n = 5 and n = 6.
  next_action: >-
    Keep the n = 3 and n = 4 replays in the gate, then define the complete n = 5
    labelled component relation before attempting the next H-032 cell.
---
# Session 007 — exact small-`n` moduli

The completed loop was proof-heavy and compute-light.
The `n = 3` cell is the semantic control for every later basin atlas: it forces the
system to distinguish labelled configurations, unlabelled components, global-symmetry
orbits, active-contact changes, and pure stabilizer changes.

The `n = 4` cell was included because the same equality lemma reduces it to a finite
grid enumeration. It is still a separate round so the campaign ledger cannot confuse a
cheap corollary with evidence about an unmeasured sweep cell.

The two retained rounds total 1.28 wall seconds of generation and replay.
That is the right scale for calibration: these controls can run on every gate without
slowing the experimental loop, and later visualization code must continue to reproduce
their topology and stratum distinctions.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
