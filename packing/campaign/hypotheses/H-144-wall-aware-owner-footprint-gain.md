---
title: "H-144 \u2014 container walls strengthen a coarse owner class"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-144
  kind: hypothesis
  claim: At q=96/25 and B=9977/10000, at least one of the sixteen frozen bottom-left owner classes is
    impossible or has a wall-aware common footprint that properly contains its old endpoint footprint.
  lane: proof
  derived_from: []
  criterion:
    shape: determination
    metric: Number of complete impossible or strictly enlarged owner classes
    direction: positive
    threshold: '0'
  instrument: packing/devtools/wall_owner_footprints.py
  instrument_ready: true
  regime: The unchanged two marks and eight closed signed sectors; all 361 canonical directions and 1444
    signed rays; physical container-center clipping; retain every nonempty point, segment and polygon
    center set.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: One five-minute external process after publication, with a 240-second internal deadline;
    all sixteen classes in frozen order.
  prereqs:
  - Twelve passing synthetic controls, including public-wrapper point/segment preservation and distinct
    constraining frame rectangles.
  - Astra Max source admission and its two required controls completed.
  - Clean published instrument and prospective exp146 protocol before any target class is evaluated.
  replication: false
  registered: '2026-09-09'
  notes: Exact nesting is required before strict area comparison. Complete feasible equality in every
    class refutes this frozen mechanism; invalid or partial construction is unresolved. This constructor
    reuses the production geometry helpers and is not an independent implementation. A gain is not yet
    an extra certified owner tuple or a global packing bound.
---
# H144: Do the Walls Strengthen the Owner Footprints?

Each owner class fixes a mark and a sector for a signed square axis.
Its common footprint is the region contained in every owner square allowed by that
class. Requiring the owner to stay inside the container can remove possible centers and
enlarge this common region.
Removing centers need not change the footprint, so the effect must be tested.

The [constructor contract](../../cases/n11_five_dot_cover/wall-constructor-contract.md)
derives the exact support bounds.
The [source review](../../cases/n11_five_dot_cover/wall-source-admission.md) approves
the frozen mathematics subject to two synthetic controls, both now passed.
Exp146 decides the finite all-sixteen mechanism.
Transferring an existing exclusion requires a separate component-containment experiment
under BC318.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
