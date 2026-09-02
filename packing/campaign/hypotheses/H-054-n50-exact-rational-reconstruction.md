---
title: H-054 — the reported n = 50 side admits an exact rational reconstruction
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-054
  kind: hypothesis
  claim: >-
    The retained source facts for the reported n = 50 construction at side 53/7 admit a
    complete reconstruction whose 50 square centers and orientation data are exact over
    the rationals, whose frozen square correspondence, symmetry convention, and
    source-precision cells certify compatibility with the retained witness, and whose
    container and nonoverlap validity is verified exactly, including rejection of named
    invalid mutations.
  lane: search
  derived_from: [X-011]
  strategy_refs: ['search:17', 'search:20']
  criterion:
    shape: determination
    metric: >-
      a complete 50-square certificate over the rationals at L = 53/7, exact nonnegative
      wall and pairwise-separation predicates under an independently written verifier,
      a replayable compatibility receipt identifying the frozen source and manifest
      hashes, square-row bijection, selected allowed symmetry, and exact membership of
      every reconstructed pose value in its frozen source-precision cell, and rejection
      of the frozen geometry and compatibility mutations
    direction: >-
      accepted only if the complete exact certificate, independent validity replay, and
      compatibility receipt all agree and both required mutations are rejected;
      rejected only if a sound exact contradiction proves the frozen source-derived,
      witness-compatible reconstruction system inconsistent; recorded as unresolved
      with reason type `invalid_instrument`, without an H-054 disposition, if the
      independent replay disagrees or either required mutation is accepted; otherwise
      unresolved if missing or ambiguous source rules prevent a defensible precision
      model or complete exact pose, or if the budget expires
    threshold: exact construction side 53/7
  instrument: >-
    Agenda-012 BC-110 reconstructs the retained geometry as rational center coordinates
    and rational unit-direction data, emits a complete exact certificate at L = 53/7,
    and checks every wall and pairwise predicate with a separate exact verifier. Before
    reconstruction it freezes a source-compatibility manifest: source and witness
    hashes, square-row labels or a deterministic bijection rule, allowed global D4
    actions, per-square quarter-turn and reflection conventions, a deterministic choice
    among passing symmetries, and a source-justified precision cell for every stored pose
    scalar. The independent verifier replays the resulting compatibility receipt and
    must reject both a preregistered overlap or wall-crossing mutation and a
    correspondence or source-cell mutation.
  instrument_ready: false
  regime: >-
    The retained n = 50 source snapshot and witness are fixed before reconstruction.
    The compatibility manifest is frozen before target construction, including its
    labeling rule, allowed symmetries, orientation periodicity, precision-model id,
    per-scalar cells, and tie-breaking rule. Decimal coordinates and angles are candidate
    clues only: no nearest-rounding or truncation rule is inferred. Each precision cell
    must follow from retained source semantics, and every adopted center and direction
    value requires both a source-derived or algebraically verified rational identity and
    exact membership in the corresponding frozen cell after the one recorded mapping.
    If the retained source cannot justify such cells, the round is unresolved.
  instance: {axis: n, point: 50}
  priority: 1
  cost_estimate: >-
    one 120-minute experiment round, executed through the agenda's 15–30-minute cells;
    freeze source facts, the compatibility manifest, reconstruction equations, verifier
    interface, and mutations before measurement, and stop unresolved at the time cap
    unless an exact determination has already been obtained
  prereqs:
  - retained n = 50 source facts and witness with stable hashes
  - >-
    frozen labeling, symmetry, orientation-periodicity, source-precision, and
    deterministic tie-breaking manifest with defensible per-scalar cells
  - exact rational certificate format and independently written validity checker
  - frozen geometry and compatibility mutation fixtures
  replication: false
  registered: '2026-09-01'
  notes: >-
    Acceptance certifies one feasible exact construction and therefore an exact upper
    bound at 53/7 after review. It establishes neither optimality nor frontier adoption,
    and the exact reported side alone is insufficient without the reconstructed pose.
---
# H-054 — Exact Rational `n = 50` Reconstruction

The reconstruction must account for all 50 rigid squares, not merely recognize the
reported side or a few suggestive angles.
Rational orientation data means exact sine and cosine components in the chosen
coordinate frame; it does not require a rational angle measured in degrees.

## Scope

The hypothesis concerns feasibility of one reconstruction compatible with the retained
witness under the frozen source model.
A different packing at the same side cannot satisfy the criterion.
Optimality, uniqueness, rigidity, and any update to the frontier remain separate review
decisions.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
