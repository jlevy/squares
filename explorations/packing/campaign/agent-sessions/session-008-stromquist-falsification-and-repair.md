---
title: session-008 — exact Stromquist falsification and repair
softschema:
  contract: packing.squares:AgentSession/v1
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-008
  title: Audit, falsify, and repair the unrestricted Stromquist lower-bound proof
  date: '2026-08-24'
  goal: >-
    Decide Stromquist's printed Theorem 2 mechanism against the primary source, preserve
    any failure as an exact counterexample, and test a separately preregistered repair
    with a complete replayable proof certificate.
  focus: correctness
  primary_bead: think-ciwv
  status: completed
  budget:
    wall_minutes: 300
    max_cycles: 6
  stop_conditions:
  - A strict open box exactly avoids the printed Figure 14 set, which terminally rejects H-010 without rejecting the numerical bound.
  - Any Figure 13 or repaired Figure 14 cell, boundary, lemma premise, sign condition, or capacity implication fails exact replay, which rejects or leaves H-041 unresolved.
  - The primary source tuple, symmetry group, or open-box semantics cannot be reconstructed unambiguously.
  - A source-distinct repair passes every finite proof node and adversarial mutation, which confirms H-041 and stops the repair search.
  - The exact falsification-and-repair pair cannot be closed inside the session budget.
  progress:
    metric: independently replayed terminal proof claims with source-bound provenance
    before: >-
      H-010 was treated as a known-answer reconstruction, the Figure 13 coordinates and
      symmetry were mistranscribed, the printed Figure 14 cover had not been checked,
      and no exact end-to-end lower-bound certificate existed.
    after: >-
      Exp-016 exactly refutes the proof as printed; exp-017 exactly certifies a
      source-distinct one-coordinate repair and proves s(11) >= 2 + 4/sqrt(5). Both
      results replay in the strict gate, while provenance keeps the paper's failure and
      the repository's repaired theorem distinct.
  delegations:
  - task: Reconstruct both figures and every finite lemma-cover obligation from the primary PDF
    operator: h010_source_reconstruction
    status: completed
    outcome: >-
      Corrected the Figure 13 seed tuple and Klein-four symmetry, found the paper's
      extraneous Lemma 4 stationary root, located the unique failing G-A1 cell, produced
      an exact strict escape, and reconstructed the complete repaired face routing.
    evidence: [primary PDF page 9 vector paths, exact radical witness, exact face and edge inventory]
    files: []
    checks: [source hashes, K4 orbit, strict open-box margins, Lemma 4 sign filter, planar cover incidence]
    uncertainty: The source-distinct repair has not undergone external peer review.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Keep source and repair provenance separate in every current summary.
  - task: Build the smallest exact printed-set falsifier and retained semantic replay
    operator: h010_tooling_design
    status: completed
    outcome: >-
      Implemented the H-010 exact checker, retained the strict Figure 14 escape, and
      added source, geometry, capacity, and record controls plus a focused gate step.
    evidence: [exact Q(sqrt(5),sqrt(829)) certificate, exp-016 generation and replay]
    files: [tools/check_stromquist_theorem2.py]
    checks: [eleven mutation controls, Ruff, BasedPyright, retained replay, focused gate]
    uncertainty: The terminal refutation is scoped to the printed proof and does not decide whether another proof of the same numerical inequality exists.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Preserve exp-016 as the negative control for every successor proof synthesizer.
  - task: Certify the preregistered one-coordinate repair with a complete exact finite cover
    operator: h041_repair_checker
    status: completed
    outcome: >-
      Implemented an exact 18-cell Figure 13 cover, four-exception orbit, A-triple
      forcing, 26-face repaired Figure 14 tiling, root and sign certificates, and the
      final 3+9 count; complete generation and replay each take about 0.35 seconds.
    evidence: [exp-017 exact result, deterministic complete-record replay, 13 adversarial mutations]
    files: [tools/check_stromquist_repair.py]
    checks: [vertex containment, edge incidence, boundary closure, noncrossing, exact area, lemma premises, capacity, duplicate-record rejection]
    uncertainty: The certificate proves the historical lower-bound value, not Trump's conjectured optimum, and is not externally peer-reviewed.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Use exp-016/017 as the failure-and-success calibration for H-039 at n = 12.
  outputs:
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-016-h-010-stromquist-printed-figure14.md
  - campaign/series/series-000-smoke-and-calibration/results/exp-016-h-010-stromquist-printed-figure14.json
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-017-h-041-stromquist-repaired-figure14.md
  - campaign/series/series-000-smoke-and-calibration/results/exp-017-h-041-stromquist-repaired-figure14.json
  - campaign/series/series-000-smoke-and-calibration/results/exp-017-h-041-stromquist-repaired-figure14-replay.json
  - tools/check_stromquist_theorem2.py
  - tools/check_stromquist_repair.py
  checks:
  - Exp-016 certifies a strict side-10001/10000 box avoiding all twelve printed Figure 14 points, with eleven passing mutations.
  - Exp-017 certifies all five repaired proof nodes, the complete 26-face tiling, and thirteen passing mutations.
  - Both records rebuild and replay semantically rather than by JSON equality alone.
  - The focused H-010 and H-041 gate lanes pass in under one second of checker time each.
  - Schemas, ledger, frontier tables, synopsis, defect log, strict gate, and deep gate agree on the terminal dispositions.
  stop_reason: >-
    The source-faithful claim was exactly refuted, and the separately registered repair
    then met every exact acceptance condition. Continuing to tune this coordinate would
    answer a new optimization question rather than strengthen the decided H-041 claim.
  next_action: >-
    Preserve both fast proof controls, register any coordinate-minimization question as
    a successor, and move the main proof rotation to H-039's first fixed-threshold n=12
    certificate candidate.
---
# Session 008 — proof failure became a proof instrument

The useful result is the pair, not either run alone.
Exp-016 prevents the program from calling a plausible diagram a proof; exp-017 shows
that the same architecture can produce a complete exact certificate after one
preregistered source-distinct change.

Machine time was negligible.
The work was source reconstruction, branch completeness, and adversarial proof checking.
That is the intended proof loop for the next frontier: cheap continuous falsification
first, exact finite certificates only for survivors, and permanent negative controls for
every failure already understood.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
