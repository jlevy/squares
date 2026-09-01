---
title: exp-047 — H-053 UnitSquare rigid-pose serialization
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-047
  series: series-000
  title: Test compatible rigid-pose serializations for the fixed n = 68/69 pairs
  date: '2026-09-01'
  hypotheses:
  - H-053
  tier: confirmatory
  subject:
    label: compatible rigid-pose serialization of the fixed UnitSquare Release 1 n = 68/69 pairs
    engine: sqpack UnitSquare precision bridge 0.1.0-unready-prototype
    engine_commit: d7c94590
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 53
      rounding: IEEE 754 binary64 roundTiesToEven; Decimal parsing precedes explicit float conversion
    tolerance: >-
      Prototype only: rigid-corner cell violation, wall and overlap tolerance 2e-12;
      transformed trigonometric endpoint pad 2e-15; emitted fitted scalars quantized to
      1e-14; fitted center radius is maximum source-cell width plus 3e-12; fitted angle
      radius is four times maximum source-cell width plus 6e-12; reconstructed edge-
      length tolerance 5e-13; a midpoint edge shorter than or equal to 0.5 is not used
      to seed an angle. None is an outward interval certificate.
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance:
    axis: n
    point: 68
    role: target
  method:
    control: >-
      Hash-verified retained child and ephemeral parent fixtures; exact identity,
      translation, scale and nested-transform squares; known wall-tangent, interior and
      wall-crossing poses; separated, tangent and overlapping pairs; positive and
      negative nearest-6 and truncate-6 boundary cells; cyclic and reversed corner
      enumerations; deterministic replay; and digest, transform-order, decimal-cell,
      duplicate-id, wall-crossing and overlap mutations.
    candidate: >-
      For each fixed n = 68 and n = 69 parent-child pair, evaluate separate
      declared:svg-literal, nearest-6 and truncate-6 source-cell models in that order,
      fit compatible rigid unit-square pose enclosures, and verify all wall and pairwise
      validity signs through an independently written receipt verifier. Seal the first
      valid n = 68 parent model from parent-only facts before any child or released-gain
      access, with no fallthrough.
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: d7c94590
    dirty: true
    entry_point: src/sqpack/research/unitsquare_precision.py
    command: >-
      uv run --frozen python -m sqpack.research.unitsquare_precision --record
      campaign/series/series-000-smoke-and-calibration/results/exp-047-h-053-unitsquare-rigid-pose-serialization.json
    budget: >-
      115 minutes remain after the target-blind W3 contract cell, ending no later than
      2026-09-01T11:11:55Z. W7 must pass provenance, transform, known-answer,
      deterministic-serialization, independent-verifier and mutation guards before any
      target fit. A failed readiness guard retains a typed premeasurement stop without
      target samples or a scientific verdict.
    record: campaign/series/series-000-smoke-and-calibration/results/exp-047-h-053-unitsquare-rigid-pose-serialization.json
  effort:
    wall_seconds: 1932
    agent_minutes: 39
    stopped_by: guard
  results:
  - shape: determination
    question: >-
      Did the W7 prototype satisfy the interval-enclosure and complete executable-runner
      admission guards before target access?
    role: guard
    outcome: no_progress
    checked_by: >-
      Independent terminal review found heuristic pose radii and binary64 tolerances
      rather than outward enclosure/sign proofs, and found that `--record` always stops
      at the W6 gate instead of exposing a complete authorized measurement route.
  verdict:
    decision: blocked
    needs_review: false
    primary_criterion: >-
      Accept only if both fixed pairs have at least one same-model parent and child with
      nonempty compatible rigid-pose enclosures, verified provenance and transforms, and
      every required wall and pairwise-validity sign independently decided. Reject only
      if a sound instrument exhausts all three frozen models for at least one pair
      without a qualifier. Any provenance, transform, enclosure, verifier or
      exhaustiveness failure is an unresolved refusal.
    reason: >-
      Typed premeasurement stop `interval-enclosure`: the numerical prototype's selftest
      and synthetic controls pass, but a float midpoint fit with fixed tolerance and
      heuristic radii does not prove a nonempty compatible-pose enclosure or outward-
      rounded wall and pair signs, and the preregistered command lacks a complete post-
      authorization runner. No parent retrieval, target parse or target fit ran, so
      H-053 remains unresolved.
    commit: d7c94590+sha256-92e7b6e43b8785c0
---
# Exp-047 — H-053 UnitSquare Rigid-Pose Serialization

This record was allocated only after session-066 returned its complete target-blind W3
contract. It binds the future result path above and does not reserve an empty result
file.

## Frozen source and selection boundary

The retained child digests are
`d7385d6ce1b5a959d06893c94f3c0355f17175bd68608db6f012ca309854ed66` for `n = 68` and
`b32aa37d37b07248ac92e683bbfd9be7ca6eb6aafa35a35e46a2484467afee41` for `n = 69`. The
ephemeral parent digests are
`558fbdddfeb0b2f8752b88e172d2776544beb4d2a7122189ef77c1e1c5ebdc6d` and
`0333814c7b43ddc7db549a54771de117f8a6b7b3db0f89c12fe035115546fd08`. Raw parent bytes may
not enter the repository.

The downstream H-051 receipt is chosen from the `n = 68` parent alone in the frozen
model order and sealed before child or gain access.
Its separate surgery-grade interval-width threshold is `1.9215450105403275e-5` in
unit-square-length coordinates; that screen does not decide H-053.

## W7 admission

Target measurement remains closed until the reusable fitter and separate receipt
verifier pass every synthetic fixture and named mutation, reproduce serialization
byte-for-byte, and bind their exact validated revision into H-053. A changed source
model or selection rule after target access contaminates this round and requires a new
registration.

## W7 premeasurement stop

The target-blind prototype stopped at baseline commit `d7c94590` with instrument SHA-256
`92e7b6e43b8785c0b618f2a48c3a26c09afb1b5cd9009a69189dfab0f606b22c`, test SHA-256
`9aeaf96d45fd94ba38af00a713a76297077a1aa7c55efc6783d6c94561c2038f`, and control-
inventory SHA-256 `fe3a17fc3f4573c80ca0d9b00987b831d483ac4ba9ac13f288bad34e0e2cec4f`.
The focused suite passed 13 tests normally and under optimized Python; Ruff and
BasedPyright passed; the module self-test passed under optimized Python; and the exact
preregistered `--record` command returned the typed W6 gate at exit 3. Those facts
validate the prototype’s numerical behavior, not the preregistered interval claim.

Admission failed because the fitter constructs a floating-point midpoint witness,
accepts a fixed tolerance and assigns heuristic enclosure radii.
The separate verifier replays the same point geometry numerically; it does not check
outward enclosures of the trigonometric image or prove every retained wall and pair
sign. The target-plan API also has no complete authorized route through retrieval,
parent-only sealing, child evaluation, independent verification and atomic result
writing. Adding those pieces after target access would violate the frozen readiness
boundary.

The record-wide validator reached and passed lint, soft-schema, research-result and
other substantive record checks, then failed on concurrent generated-view/session drift
outside BC-109 (`SYNOPSIS.md`, `agenda-map.md`, session-close views, the ledger and
session-065 phase status).
Those integration surfaces are coordinator-owned and do not weaken the target-blind
stop. W6 remains closed.
Reopening requires a sound interval existence/sign verifier and a complete target-blind
orchestration test; it does not require new target evidence.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
