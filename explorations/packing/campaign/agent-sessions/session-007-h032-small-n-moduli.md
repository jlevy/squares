---
title: session-007 — H-032 exact small-n moduli controls
softschema:
  contract: packing.squares:AgentSession/v1
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
  focus: insight
  primary_bead: think-n82j
  status: in_progress
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
    after: The n = 3 and n = 4 cells are claimed separately; independent mathematical, visualization, and source-archive work is in progress.
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
    status: in_progress
    outcome: Running; the renderer and visual acceptance contract have not yet been imported.
    evidence: []
    files: []
    checks: [labelled circles, S3 quotient, D4 quotient interval, stabilizers, contact and wall strata, representative glyphs]
    uncertainty: The smallest readable SVG that remains semantically replayable is still being selected.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Bind the chosen encoding into the checker before rendering the result.
  - task: Archive and route all directly relevant primary hard-square configuration-space papers
    operator: archive_hard_square_configuration_literature
    status: in_progress
    outcome: Running; three missing primary papers have been identified and are being recovered under the archive convention.
    evidence: []
    files: []
    checks: [official source provenance, PDF hashes, raw extraction preservation, claim routing]
    uncertainty: The 2025 source may be less stable or harder to retrieve than the two published AGT papers.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Compare the exact n = 3 cell counts and topology against the archived statements before any novelty language.
  outputs:
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-014-h-032-n3-optimal-moduli.md
  - campaign/series/series-000-smoke-and-calibration/results/exp-014-h-032-n3-optimal-moduli.json
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-015-h-032-n4-optimal-moduli.md
  - campaign/series/series-000-smoke-and-calibration/results/exp-015-h-032-n4-optimal-moduli.json
  - tools/check_small_n_moduli.py
  - atlas/n-003-optimal-moduli.svg
  checks:
  - Claim schemas, source archive, ledger integration, clean-tree provenance, exact replays, and render replay are pending.
  stop_reason: null
  next_action: >-
    Commit and push both claims, then implement the exact enumerator and deterministic
    renderer without changing the preregistered counts or stop rules.
---
# Session 007 — exact small-`n` moduli

The intended loop is proof-heavy and compute-light.
The `n = 3` cell is the semantic control for every later basin atlas: it forces the
system to distinguish labelled configurations, unlabelled components, global-symmetry
orbits, active-contact changes, and pure stabilizer changes.

The `n = 4` cell is included because the same equality lemma reduces it to a finite grid
enumeration. It is still a separate round so the campaign ledger cannot confuse a cheap
corollary with evidence about an unmeasured sweep cell.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
