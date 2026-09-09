---
title: "H-137 \u2014 single owner dual salvage"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-137
  kind: hypothesis
  claim: At least one of the sixteen bottom-left endpoint-footprint classes retains exact fractional-family
    mass at least ten after strictly intersecting poses are deleted.
  lane: proof
  derived_from: []
  criterion:
    shape: determination
    metric: maximum retained mass over sixteen declared endpoint classes
    direction: at least ten
    threshold: '10'
  instrument: packing/devtools/screen_corner_dual_salvage.py with packing/devtools/owner_footprints.py
  instrument_ready: false
  regime: L=96/25, B=9977/10000; BC232 exp070 depth-one family translated by (1/100,1/100), scale1, full361
    canonical directions and full-net signed owner endpoints. Strict positive separation is required;
    touching is deleted.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: One shared exact screen with a five-minute external timeout after controlled instrument
    publication; no LP or full arrangement replay per class.
  prereqs:
  - controlled exact footprint/SAT geometry
  - source family Git identity and retained exact depth-one receipt
  - prospective exp137 before any target masks or survivor masses
  replication: false
  registered: '2026-09-09'
  notes: A qualifying survivor family is an all-site obstruction to the declared relaxed residual covering
    problem. Failure of the mass threshold is inconclusive about achievable covering mass and says nothing
    against geometric conditioning in general.
---
# H-137: Exact Residual-Cover Obstruction

At least one of the sixteen bottom-left endpoint-footprint classes retains exact
fractional-family mass at least ten after strictly intersecting poses are deleted.

The retained family has total mass21342289572/2055263195 and exact pointwise depth at
most one. Translation preserves depth; deleting nonnegative terms cannot increase it.
Every survivor is an admissible residual core, so any nonnegative covering measure has
effective mass at least the surviving weight.
This statement holds for arbitrary support, not just the pilot grid.

The test concerns guaranteed footprints alone.
It does not assert that the corresponding unknown owners coexist, and it does not
obstruct stronger constraints using their full poses or shared compatibility.
Triangle results are nested controls reported alongside the endpoint result; the
hypothesis is about the endpoint family.

No target screen was run to choose this claim.
Agenda032 BC311 owns the experiment.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
