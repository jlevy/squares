---
title: H-103 — can complete typed coverage reduce every minimizer to Trump?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-103
  kind: open_question
  claim: >-
    Can a complete typed finite cover of every n = 11 side-minimizing configuration
    between the retained lower bound and Trump's exact side be rigorously excluded or
    mapped wholly into the retained strict Trump isolation neighborhood, modulo D4 and
    square relabelling?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:10', 'proof:11', 'proof:15', 'proof:17', 'proof:22', 'proof:27']
  instrument: >-
    BC-245's compactness and typed Fritz-John branch contract, independently replayed
    BC-246 endpoint and BC-247 completeness/pricing controls, then a separately priced
    complete cover using sound branch-specific exclusions and local capture.
    The general producer and complete-cover verifier are not ready.
  instrument_ready: false
  regime: >-
    all side minimizers in the declared interval; ordinary and abnormal Fritz-John
    branches, ties, zero multipliers, rattlers, and every feasibility inequality retained
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: price one nontrivial complete branch before any global enumeration
  prereqs: [reviewed BC-245 contract, exact local endpoint and complete branch-specific controls]
  replication: true
  registered: '2026-09-06'
  notes: >-
    Typed SAT/LP/interval exclusion, geometric conflicts, clique or Hall constraints,
    and conditional covering certificates are possible methods, not evidence of
    completeness. A valid covering measure M and epsilon = M - 11 are prerequisites
    only for mass-forcing or near-tight deductions that use them, not every geometric
    incompatibility or independently justified conditional certificate.
---
# H-103 — Complete Global Capture, with Restricted Precursors Kept Separate

[BC-245](../series/series-000-smoke-and-calibration/results/agenda-026/bc-245-typed-backbone-theorem-packet.md)
reduces the target to typed minimizers without assuming constraint qualification.
A finite branch language does not prove that enumeration is affordable or complete.
The [H-032 controls](H-032-small-n-optimal-moduli.md) cover all n = 3 and n = 4 optimum
strata; a known n = 5 packing is only a positive local control.

Every conditional certificate must name the configuration domain it excludes.
Clique, odd-cycle, Hall, and hyperedge cuts need a sound integral assignment model;
heavy-atom and near-tight forcing additionally need the actual valid covering measure.
[H-102](H-102-complete-restricted-angle-support-families.md) permits independently
useful restricted theorems without asserting this global cover.

The retained BC-240/241 endpoint is accepted only at its local,
retained-record-dependent scope.
A capture leaf must put its whole surviving box strictly inside that radius after an
exact symmetry and label map; the remaining leaves must cover the whole complement.
[Agenda 026’s BC-248](../agendas/agenda-026-density-stationarity-and-trump-capture.md)
keeps its existing valid-measure, at-most-2,311,290-of-23,112,904 survivor, and
below-four-CPU-hour pricing guards, plus BC-246/247 prerequisites.
These guards apply to that global residue, not all structural precursor lemmas.
The distinction comes from
[X-016’s exact-cover and closure routes](../explorations/X-016-after-381-two-managers-one-proof-boundary.md#closure-route).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
