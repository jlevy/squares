---
title: H-052 — the fixed n = 17 certificate agrees under independent accumulation
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-052
  kind: hypothesis
  claim: >-
    The fixed retained Massaccesi n = 17, L = 4.5058 certificate agrees on every
    preregistered exact invariant when evaluated by an independently written exact
    accumulation implementation that does not copy the published two-dimensional
    difference-array sweep.
  lane: proof
  derived_from: [X-011]
  strategy_refs: ['proof:22']
  criterion:
    shape: determination
    metric: >-
      exact agreement on the frozen certificate totals, 181 rational direction cells,
      event-cell reductions and minima, global minimum 576/576, and declared
      shrink-and-scaling preconditions, together with rejection of the named mutations
    direction: >-
      accepted only if every frozen invariant agrees exactly and every named mutation is
      rejected; rejected if the independently written path produces a reproducible exact
      disagreement after both paths and their fixtures pass their guards; unresolved if
      implementation independence, provenance, or a guard cannot be established
    threshold: exact equality on every frozen invariant
  instrument: >-
    Agenda-012 BC-108 freezes the retained certificate and invariant manifest, replays
    the source-faithful path, and evaluates the same atoms with a separately written
    exact accumulator whose control flow does not reproduce the published
    two-dimensional difference-array sweep. It records exact rational outputs and runs
    atom, weight, direction-cell, event-boundary, and scaling mutations.
  instrument_ready: false
  regime: >-
    The retained 168-atom Massaccesi certificate, its source hash, the 181-cell rational
    direction net, and the published shrink-and-scaling argument are fixed before either
    evaluation. All comparisons use exact rationals; the second implementation may
    share the fixed certificate, mathematical definitions, and invariant manifest but
    not the published accumulation control flow.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    one 150-minute experiment round, executed through the agenda's 15–30-minute cells;
    freeze the invariant and mutation manifests before measurement, and stop unresolved
    when a provenance or independence guard fails
  prereqs:
  - hash-verified retained certificate and source-faithful replay
  - frozen exact invariant and mutation manifests
  - separately authored exact accumulation path with an auditable independence receipt
  replication: false
  registered: '2026-09-01'
  notes: >-
    Acceptance establishes implementation agreement for this fixed certificate. It is
    neither proof-method independence nor adoption of 4.5058 as a reviewed lower bound,
    and it makes no cross-n or LP-generalization claim. A disagreement rejects this
    agreement claim but does not by itself refute the mathematical lower bound; the
    discrepancy remains for independent adjudication.
---
# H-052 — Independent `n = 17` Certificate Agreement

The experiment holds the mathematical input fixed and changes only the exact
accumulation implementation.
The second path must be independently authored and must not translate the published
difference-array sweep line by line.

## Scope

The result measures agreement between two implementations on one retained certificate.
Any later lower-bound adoption requires separate source review and disposition.
The experiment cannot establish a distinct proof method, certificate uniqueness, or
transfer to another value of `n`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
