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
    engine: sqpack UnitSquare one-parent production adapter 0.1.0-preregistered
    engine_commit: 81177148e404aa283c2a6ec7d696f2b39a9e361c
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: false
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
    commit: 81177148e404aa283c2a6ec7d696f2b39a9e361c
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
  lease:
    expires: '2026-09-02T02:45:00Z'
    host: local-macos-arm64
  results: []
  verdict:
    decision: in-progress
    needs_review: true
    primary_criterion: >-
      The literal production command reaches the injected adapter, normal and optimized
      receipts agree, all provenance, transform, model, proof, cleanup and publication
      mutations reject, and independent W2 readmission passes.
    reason: The adapter round is allocated and no target-blind command has run.
---
# Exp-054 — H-058 `n = 68` One-Parent Production Serialization

This is an instrument-admission round.
It cannot accept or reject H-058, open the network, read the parent, inspect a child,
measure a gain or run surgery.

Exp-047 and exp-051 retain their reviewed decisions.
Their current bytes differ from the historical review packet only through the authorized
review-flag transition recorded in Agenda 014.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
