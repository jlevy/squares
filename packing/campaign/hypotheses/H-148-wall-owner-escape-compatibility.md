---
title: "H-148 \u2014 an owner class excludes the saved escape"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-148
  kind: hypothesis
  claim: At least one of the four selected owner classes admits no snapped B-core strictly disjoint from
    the fixed exp149 escaping B-core.
  lane: proof
  derived_from: []
  criterion:
    shape: determination
    metric: One complete selected class has nonpositive separation slack on every retained frame and signed
      SAT axis
    direction: positive
    threshold: '0'
  instrument: packing/devtools/wall_owner_escape_compatibility.py
  instrument_ready: true
  regime: The exact exp149 axis escape, tuple (0,0,0,7), q=96/25, B=9977/10000, complete exp146 centre/frame
    records; class order TR, BL, BR, TL.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: One 120-second external process plus two-second termination grace; 90-second cooperative
    guard after input loading.
  prereqs:
  - Astra Max source admission, complete frame/centre provenance and independent strict-pose replay controls.
  - Clean published source and prospective exp150 before target evaluation.
  replication: false
  registered: '2026-09-09'
  notes: Accept after exhaustive nonpositive slack in one class. Refute only when each of four classes
    supplies an independently replayed compatible B-core. Partial or invalid is unresolved. Positive examples
    do not establish unit-square parents or joint owner compatibility. Exp150 completed in 9.01 seconds
    and refuted this claim with one positive replayed witness in each of the four classes.
---
# H148: Does an Owner Class Exclude the Escape?

The [decision tree](../../cases/n11_five_dot_cover/after-exp149-strategy.md) selects
this one-pose test to distinguish a gap caused by the common-footprint approximation
from a gap that survives individual owner-core constraints.
Both shapes have side B; this is the finite necessary core model, not a test of sampled
unit-square orientations.

The
[source admission](../../cases/n11_five_dot_cover/owner-compatibility-source-admission.md)
is complete. Sol passed 21 focused controls in 8.51 seconds; Astra Max independently
passed 21 in 4.53 seconds and checked exact adversarial fixtures.
Exp150 now refutes H148: all four classes admit an individually compatible owner core.
This does not establish a joint packing.
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
