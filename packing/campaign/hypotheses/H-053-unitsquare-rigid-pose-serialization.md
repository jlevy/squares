---
title: H-053 — the fixed UnitSquare n = 68 and n = 69 pairs admit compatible rigid poses
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-053
  kind: hypothesis
  claim: >-
    For each fixed UnitSquare Release 1 parent-child pair at n = 68 and n = 69, at least
    one declared BC-109 serialization model admits nonempty compatible rigid unit-square
    pose enclosures for both the parent and its corresponding child, with provenance and
    transform guards passing and every required container and pairwise-validity sign
    independently decided.
  lane: search
  derived_from: [X-011]
  strategy_refs: ['search:17', 'search:20']
  criterion:
    shape: determination
    metric: >-
      for each of the two fixed parent-child pairs, existence of one declared model with
      nonempty compatible rigid-pose sets for both members, hash-verified provenance and
      transforms, and independently decided wall and pairwise-validity signs
    direction: >-
      accepted only if both n = 68 and n = 69 have a qualifying model; rejected only if
      the frozen declared-model enumeration is complete and a sound evaluation exhausts
      it for at least one pair without a qualifying model; unresolved by typed refusal
      if provenance, transform semantics, interval enclosure, validity, or model
      exhaustiveness cannot be established
    threshold: at least one qualifying serialization model for each fixed pair
  instrument: >-
    The target-blind prototype at
    `packing/src/sqpack/research/unitsquare_precision.py`, baseline commit d7c94590 and
    SHA-256 92e7b6e43b8785c0b618f2a48c3a26c09afb1b5cd9009a69189dfab0f606b22c,
    implements digest guards, source cells, transforms, canonical point-pose fitting,
    serialization and a separate numerical replay verifier. It is not yet the required
    interval instrument: its fitted radii and predicate margins are heuristic, and its
    gated target plan is not a complete post-authorization measurement runner.
  instrument_ready: false
  regime: >-
    The UnitSquare Release 1 n = 68 and n = 69 child SVG hashes and cited parent digests
    are fixed before model evaluation. Each serialization model has its own declared
    decimal-cell semantics; models are never merged. The mathematical frame has
    container [0,L] by [0,L] and small-square side exactly 1. Raw parent retrieval,
    transform resolution, and any ambiguity are recorded explicitly.
  instance: {axis: release, point: unitsquare-release-1-n68-n69}
  priority: 1
  cost_estimate: >-
    one 130-minute two-pair experiment round, executed through the agenda's
    15–30-minute cells; freeze source hashes, model ids, model order, interval policy,
    and mutation fixtures before measurement, with typed refusal allowed at any failed
    guard
  prereqs:
  - retained child SVGs and hash-verified cited parent sources for both pairs
  - frozen declared-model inventory, stable ordering, and decimal-cell semantics
  - independently checked SVG-to-unit-square transform and validity fixtures
  replication: false
  registered: '2026-09-01'
  notes: >-
    Acceptance establishes compatible independently valid serializations for the fixed
    pairs only. It does not recover source precision, certify contacts, meet H-051's
    gain-relative surgery threshold, or adopt any released side interval. A typed
    refusal leaves H-053 unresolved rather than forcing a geometric verdict. The failed
    W7 prototype is bound additionally to test SHA-256
    9aeaf96d45fd94ba38af00a713a76297077a1aa7c55efc6783d6c94561c2038f and
    control-inventory SHA-256
    fe3a17fc3f4573c80ca0d9b00987b831d483ac4ba9ac13f288bad34e0e2cec4f; no target
    sample contributed to its target-blind stop. Reopen only with a sound outward-
    rounded existence verifier and a complete, injection-tested post-authorization
    runner that requires no readiness-code edit.
---
# H-053 — UnitSquare Rigid-Pose Serialization

This experiment separates source interpretation from geometric validity.
A model must first preserve the frozen source and transform semantics, then admit rigid
unit-square poses whose wall and nonoverlap signs can all be decided.

## Scope

The two values of `n` are a paired serialization control, not a surgery trial.
A compatible model may still be too imprecise for gain-scale comparison, and a refusal
is a valid measurement outcome when the retained source cannot support a sound decision.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
