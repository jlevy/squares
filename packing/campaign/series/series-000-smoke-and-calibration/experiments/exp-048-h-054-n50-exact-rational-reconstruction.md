---
title: exp-048 — H-054 n = 50 exact rational reconstruction
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-048
  series: series-000
  title: Test witness-compatible exact rational reconstruction at n = 50 and L = 53/7
  date: '2026-09-01'
  hypotheses:
  - H-054
  tier: confirmatory
  subject:
    label: witness-compatible exact rational n = 50 construction at side 53/7
    engine: sqpack n = 50 exact reconstruction instrument 0.1.0-preregistered
    engine_commit: d7c94590
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: false
  instance:
    axis: n
    point: 50
    role: target
  method:
    control: >-
      Exact n = 18 over Q(sqrt(7)) and n = 19 over Q(sqrt(2)) with duplicated-square
      mutations; the rational exact-LP control; a source-refusal fixture whose decimals
      have no declared serialization semantics; independent exact geometry and
      compatibility checkers; deterministic D4 and matching replay; duplicated-pose,
      nonbijective-correspondence and reversed-source-cell mutations.
    candidate: >-
      A complete 50-pose rational certificate at L = 53/7, with exact unit directions,
      all wall and 1,225 pair predicates verified by an independently written checker,
      and a compatibility receipt mapping the certificate bijectively to the retained
      witness under the frozen D4, quarter-turn, winding, source-cell and lexicographic
      tie-breaking manifest.
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: d7c94590
    dirty: true
    entry_point: cases/n050_exact/verify.py
    command: >-
      uv run --frozen python -m cases.n050_exact.verify --record
      campaign/series/series-000-smoke-and-calibration/results/exp-048-h-054-n50-exact-rational-reconstruction.json
    budget: >-
      100 minutes remain after the target-blind W3 contract cell, ending no later than
      2026-09-01T11:01:55Z. W7 first has 25 minutes to establish source-justified cells,
      build the separated certificate, geometry and compatibility interfaces, and pass
      known-answer and mutation guards. If retained evidence cannot justify every source
      cell, stop E1 before reconstruction and create no target sample or scientific
      verdict.
    record: campaign/series/series-000-smoke-and-calibration/results/exp-048-h-054-n50-exact-rational-reconstruction.json
  effort:
    timebox: 25-minute W7 readiness cell inside the 120-minute BC-110 lane
    wall_seconds: 0
    agent_minutes: 8
    stopped_by: dependency
  results:
  - shape: determination
    question: >-
      Did retained evidence supply complete upstream serialization semantics from which
      W7 could construct a defensible closed source cell for every n = 50 witness scalar?
    role: guard
    outcome: no_progress
    checked_by: frozen E1 source/provenance admission gate and independent closure audit
  verdict:
    decision: unresolved
    needs_review: false
    primary_criterion: >-
      Accept only if one complete rational 50-pose certificate at L = 53/7 passes exact
      unit-direction, wall, pairwise and independent-verifier checks, maps bijectively
      into every frozen source-precision cell under the deterministic compatibility
      manifest, and rejects the required geometry and compatibility mutations. Reject
      only on a sound exact contradiction to the full frozen source-compatible system;
      otherwise retain a typed unresolved refusal or priced exhaustion.
    reason: >-
      Typed premeasurement stop E1 (source/provenance): the retained witness records
      numerical-checker precision and rounding settings, while the retained source
      inventory records only metadata and derived numerical facts. Neither declares the
      upstream serialization semantics needed to derive a defensible closed cell for
      every source scalar. This is process retention, not a scientific H-054 verdict;
      no target reconstruction, target verifier, sample or result file was created.
---
# Exp-048 — H-054 `n = 50` Exact Rational Reconstruction

This record was allocated only after session-067 returned its complete target-blind W3
contract. It binds the future result path above and does not reserve an empty result
file.

## Frozen fixture and compatibility boundary

The retained witness digest is
`8318cbc7ec4c4a8b3d15634531535b204f0106360361f81e71820a6e2308b21e`; the frontier digest
is `a5f9ead7cd94ee14bef77d4cdd3f37f64c9a803ff47f406a2dba9f8097f2c746`; and the
source-inventory digest is
`4fa25fab27f69a9c2d8e28c6924a36b8d0bfc00ac9b066fb53fa796412b0d687`. The witness
checker’s `rounding: nearest` field is a numerical replay setting, not evidence of the
upstream source serialization.

The frozen manifest tests global D4 actions in the declared order, treats square-edge
directions modulo quarter turns with reflected winding retained, requires a perfect
50-row matching, and selects the lexicographically first passing action, row vector,
quarter-turn vector and winding vector.
Every compatible scalar must lie in a source-justified closed cell.

## W7 admission and refusal

The registered source model is `source-semantics-required-v1` and presently supplies no
admissible cells. W7 may open target reconstruction only if retained evidence
independently establishes a declared exact, nearest-rounding, truncation or interval
meaning for every source scalar and the separated manifest, geometry and compatibility
instruments pass all controls and mutations.
Failure to establish those cells is premeasurement refusal E1: keep H-054
`instrument_ready: false`, retain the stop, and create no target output.

## Terminal W7 Receipt

- **Artifact:** This experiment record retains refusal E1 against frozen source model
  `source-semantics-required-v1`.
- **Result:** The source inventory declares retention of metadata and derived numerical
  facts only, and the witness’s `rounding: nearest` is a numerical-replay setting.
  Neither fixture declares exact-token, nearest-rounding, truncation or interval
  semantics for every upstream source scalar, so no admissible source cells can be
  constructed.
- **Guard:** W7 stopped at its first admission gate.
  No n = 50 reconstruction, solver, verifier, source-control execution, target sample or
  result JSON exists; H-054 remains `instrument_ready: false` and scientifically
  unresolved.
- **Next:** The coordinator may retain this typed stop and route the declared fallback.
  W6 remains unauthorized unless a new preregistered round first acquires complete,
  attributable source-serialization semantics.

A later executed decision remains `needs_review: true`; only BC-121 may clear that field
without changing the decision after BC-120 explicitly passes this exact record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
