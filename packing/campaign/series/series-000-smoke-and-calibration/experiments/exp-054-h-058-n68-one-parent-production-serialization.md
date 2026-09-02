---
title: exp-054 — H-058 n = 68 one-parent production serialization
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-054
  series: series-000
  title: Admit the target-blind n = 68 one-parent production adapter
  date: '2026-09-01'
  hypotheses: [H-058]
  tier: exploratory
  subject:
    label: target-blind production reachability for one n = 68 parent source
    engine: sqpack UnitSquare one-parent production adapter 0.1.0-target-blind-admitted
    engine_commit: 909efafa
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance:
    axis: n
    point: 68
    role: calibration
  method:
    control: >-
      Injected bounded SVG streams, exact transforms, three isolated serialization
      models, rational pose proofs, cleanup paths and atomic-publication mutations under
      normal and optimized Python; no target or network access.
    candidate: >-
      A complete production adapter wrapping the frozen exp-051 proof runner with a
      bounded opener, digest-before-parse scanner, exact transform parser, model
      factory, whole-result verifier and verify-before-publication seam.
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: 909efafa
    dirty: true
    entry_point: cases/unitsquare_precision/production/run.py
    command: >-
      uv run --frozen python -m cases.unitsquare_precision.production.run --record
      campaign/series/series-000-smoke-and-calibration/results/exp-054-h-058-n68-one-parent-production-serialization.json
    budget: >-
      BC-124 receives 150 minutes through 2026-09-02T02:45:00Z. The literal command
      must reach an injected adapter boundary by minute 35; no network or target source
      is authorized in this round.
    record: campaign/series/series-000-smoke-and-calibration/results/exp-054-h-058-n68-one-parent-production-serialization.json
  effort:
    timebox: >-
      One target-blind 150-minute BC-124 wall through 2026-09-02T02:45:00Z; the
      admission criterion ended author work and cross-lane review before the deadline.
    wall_seconds: 5940
    agent_minutes: 99
    stopped_by: criterion
  results:
  - shape: determination
    question: >-
      Did the complete target-blind production adapter pass its literal command,
      provenance, transform, model, proof, cleanup, publication and independent-review
      admission gates without opening the n = 68 target?
    role: guard
    outcome: criterion_met
    checked_by: >-
      After a prepublication selected-path depth-guard repair, a fresh different-lane W2
      reviewer matched adapter SHA-256
      9b503050115a5a48b01ec9f4d348b869495fbe4ee4847dc83188b05a3352f539,
      run.py 8cef0f9cd4f473e594ed55e650be2fe7b286a798d2a94e5edb0a35efb7b12d54,
      verify.py e39a6a725e7af01a2e1796e1a218576f76b8a2ec2cecf7fbde3f38aeb9630a7a
      and test SHA-256
      17f4be0611fb02419d9007222f07b3f585b290c03866403a1d2bd5da954f01df;
      reproduced 35 focused tests, clean Ruff and BasedPyright checks, all 20 named
      mutations and byte-identical 1,112-byte normal and optimized receipts at SHA-256
      becb4c7f865f2f4b3a9d6bd22b11bb736efe73ba2d7dc97e025cd4becbd55906;
      and confirmed the canonical result remained absent.
  verdict:
    decision: unresolved
    needs_review: true
    primary_criterion: >-
      The literal production command reaches the injected adapter, normal and optimized
      receipts agree, all provenance, transform, model, proof, cleanup and publication
      mutations reject, and independent W2 readmission passes.
    reason: >-
      The target-blind adapter passed its complete author-side and different-lane W2
      admission gates, so H-058's instrument is ready for a separately preregistered
      target phase. This round opened no network or target source and created no exp-054
      result, so it supplies no H-058 sample and cannot accept or reject the claim.
      Whole-result verification shares the frozen refusal.verify proof-replay kernel with
      the producer path, although its shape, binding and publication checks are separate.
      The reported side token also remains intentionally unbound; the production path
      therefore yields three typed `serialization-refusal` outcomes until a later
      preregistration supplies admissible exact or directional semantics.
    commit: 909efafa+sha256-9b503050115a5a48
---
# Exp-054 — H-058 `n = 68` One-Parent Production Serialization

This is an instrument-admission round.
It cannot accept or reject H-058, open the network, read the parent, inspect a child,
measure a gain or run surgery.

Exp-047 and exp-051 retain their reviewed decisions.
Their current bytes differ from the historical review packet only through the authorized
review-flag transition recorded in Agenda 014.

## Terminal Target-Blind Admission

The literal command and its mutations ran only against injected in-memory SVG bytes and
temporary output roots.
The canonical result path remained absent throughout author work and independent W2. The
`unresolved` verdict protects the scientific boundary: instrument admission is not a
sample-based H-058 determination.

The phase-local hashes in session-074 preserve the original author and W2 evidence.
Prepublication review found one recursive precheck that preceded the declared depth
bound, repaired it, added a recursion-limit control and independently readmitted all
current instrument bytes.
H-058 and this record bind that corrected set.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
