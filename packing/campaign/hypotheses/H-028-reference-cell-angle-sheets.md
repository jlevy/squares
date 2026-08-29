---
title: H-028 — reference-cell angle sheets isolate the published minima locally
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-028
  kind: hypothesis
  claim: >-
    On preregistered two-degree class-angle boxes in the imported n = 11 and n = 17
    reference cells, adaptive refinement recovers the published class angles within
    0.01 degrees as the sole local minimizer, and every boundary point is at least 1e-5
    side units higher.
  lane: search
  derived_from: [X-002]
  strategy_refs: ['search:15', 'search:17']
  criterion:
    shape: conditions
    metric: refined local-minimum count, angular recovery error, and boundary gap on the declared fixed-cell value sheets
    direction: one local minimum within 0.01 degrees of the reference and boundary gap at least 1e-5
    threshold: 0.00001
  instrument: >-
    For n = 11 vary the axis and tilted class angles; for n = 17 hold the axis class at
    zero and vary the two oblique classes. Solve the imported separating cell at every
    adaptive grid point, refine every candidate local minimum under at least two grid
    offsets, label basis changes, and render the refined sheet.
  instrument_ready: false
  regime: one fixed imported cell and class assignment per n; plus or minus two degrees
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [11, 17]}
  priority: 2
  cost_estimate: tier S coarse sheet, tier M adaptive refinement only around observed features
  prereqs: [verified n = 17 pose]
  replication: true
  registered: '2026-08-24'
  notes: >-
    This is not the global two-class stratum. Competing assignments and separating
    cells are excluded by definition and must be mapped separately if the local sheet
    changes a decision. Continuity guarantees nearby points with nearby values, so the
    criterion concerns local minimizers and a boundary margin, not uniqueness inside a
    fixed objective-value tolerance.
---
# H-028 — the first honest two-dimensional local picture

Every pixel names its cell, basis, arithmetic method, actual precision, and tolerance.
The map is a local mechanism instrument, not evidence that no other valley exists.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
