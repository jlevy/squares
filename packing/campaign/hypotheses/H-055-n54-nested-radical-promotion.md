---
title: H-055 — the selected n = 54 witness admits nested-radical promotion
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-055
  kind: hypothesis
  claim: >-
    If BC-111 selects n = 54, the fixed retained witness at reported side
    7 - sqrt(2)/2 + sqrt(1 + sqrt(2)) can be lifted to a complete exact representation
    in a named nested-radical field that satisfies a frozen labeling, symmetry, and
    source-precision compatibility receipt, with exact container and nonoverlap validity
    and rejection of named invalid mutations.
  lane: search
  derived_from: [X-011]
  strategy_refs: ['search:17', 'search:20']
  criterion:
    shape: determination
    metric: >-
      a complete 54-square certificate in the declared nested-radical field at the exact
      reported side, exact decisions for every wall and pairwise-validity predicate under
      an independently written verifier, a replayable compatibility receipt identifying
      the frozen source and manifest hashes, square-row bijection, selected allowed
      symmetry, and exact membership of every promoted pose value in its frozen
      source-precision cell, and rejection of the frozen geometry and compatibility
      mutations
    direction: >-
      accepted only if the exact lift, independent validity replay, and compatibility
      receipt all agree and both required mutations are rejected; rejected only if a
      sound exact contradiction proves the frozen witness-compatible lift system
      inconsistent in the declared field; recorded as unresolved with reason type
      `invalid_instrument`, without an H-055 disposition, if the independent replay
      disagrees or either required mutation is accepted; otherwise unresolved if source,
      source-precision, or contact-model ambiguity remains or the selected-run budget
      expires
    threshold: 7 - sqrt(2)/2 + sqrt(1 + sqrt(2))
  instrument: >-
    Agenda-012 BC-114, when routed to n = 54 by BC-111, defines the nested-radical field
    and its embeddings, reconstructs exact center and orientation data from the retained
    witness and source facts, and verifies every wall and pairwise predicate
    independently. Before reconstruction it freezes a source-compatibility manifest:
    source and witness hashes, square-row labels or a deterministic bijection rule,
    allowed global D4 actions, per-square quarter-turn and reflection conventions, a
    deterministic choice among passing symmetries, and source-justified precision cells
    for the stored pose scalars. The independent verifier replays the compatibility
    receipt and must reject both a preregistered overlap or wall-crossing mutation and a
    correspondence or source-cell mutation.
  instrument_ready: false
  regime: >-
    The selected retained W-known-best-n054 decimal pose is a starting approximation,
    while the reported side expression and frozen source facts define the algebraic
    target. The compatibility manifest is frozen before target construction, including
    its labeling rule, allowed symmetries, orientation periodicity, precision-model id,
    per-scalar cells, and tie-breaking rule. No nearest-rounding or truncation rule is
    inferred: each precision cell must follow from retained source semantics. Every
    promoted coordinate and orientation requires an exact field identity and exact
    membership in the corresponding frozen cell after the one recorded mapping;
    tolerance-only validity is excluded. If the source cannot justify the cells, the
    round is unresolved.
  instance: {axis: n, point: 54}
  priority: 2
  cost_estimate: >-
    at most one 180-minute selected-case experiment round, executed through the agenda's
    15–30-minute cells; freeze the field tower, compatibility manifest, reconstruction
    equations, exact-verifier interface, precision and search caps, and mutations before
    measurement
  prereqs:
  - BC-110 exact n = 50 control is usable
  - BC-111 selects n = 54 for this run
  - retained n = 54 source facts and witness with stable hashes
  - >-
    frozen labeling, symmetry, orientation-periodicity, source-precision, and
    deterministic tie-breaking manifest with defensible per-scalar cells
  - frozen geometry and compatibility mutation fixtures
  replication: false
  registered: '2026-09-01'
  notes: >-
    BC-111 selects at most one of H-055 and H-056 for this run. If it selects n = 39,
    H-055 stays unmeasured rather than rejected. Acceptance certifies one exact feasible
    construction; optimality, uniqueness, rigidity, and frontier adoption remain outside
    this claim.
---
# H-055 — Nested-Radical `n = 54` Promotion

The side expression identifies a plausible algebraic field but does not supply the
square poses. Promotion requires exact coordinates and orientations for every square,
plus exact geometric verification and a mutation that demonstrates the checker can
reject an invalid certificate.

## Selection Boundary

This record becomes measurable only when BC-111 selects `n = 54`. Selection of `n = 39`
leaves it registered and unmeasured for this run.

The accepted lift must match the retained witness under the frozen compatibility
manifest. An unrelated packing at the same exact side does not satisfy this record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
