---
title: H-030 — public-parent surgery reproduces held-out record improvements
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-030
  kind: hypothesis
  claim: >-
    Starting only from the six cited parent geometries in UnitSquare Release 1, a
    preregistered deletion, insertion, block-shear, strip, and local-reoptimization
    proposer independently reproduces at least two of the six hidden child improvements.
  lane: search
  derived_from: [X-002]
  strategy_refs: ['search:5', 'search:7', 'search:8', 'search:20']
  criterion:
    shape: conditions
    metric: count of hidden release improvements matched or beaten by independently valid poses
    direction: at least two of six
    threshold: 2
  instrument: >-
    Import and verify each public parent, hide the released child pose and side from the
    proposer, run a versioned surgery grammar under equal per-case pair-tests, and
    interval-validate every claimed reproduction.
  instrument_ready: false
  regime: UnitSquare Release 1 parent-child pairs at n = 68, 69, 103, 105, 110, 131
  instance: {axis: release, point: unitsquare-2026-07-29}
  priority: 1
  cost_estimate: tier S n = 68 and 69; tier M all six only after a response curve
  prereqs: [verified geometry corpus beyond n = 100]
  replication: true
  registered: '2026-08-24'
  notes: >-
    This is a methods calibration, not a claim of independent discovery priority. A
    surgery family that cannot recover a hidden known child does not get an unseen
    record budget.
---
# H-030 — make construction grammar answer to held-out geometry

The release supplies unusually clean supervision: explicit parents, explicit children,
small but real improvements, and validity evidence.
The retained failures become a cross-`n` genealogy of which moves transfer.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
