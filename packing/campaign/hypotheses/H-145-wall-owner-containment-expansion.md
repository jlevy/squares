---
title: H-145 — wall-aware footprints extend a five-dot exclusion
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-145
  kind: hypothesis
  claim: The frozen wall-aware owner footprints inherit at least one additional labelled four-owner exclusion
    by component containment of one of the two certified patch families.
  lane: proof
  derived_from: []
  criterion:
    shape: determination
    metric: Additional labelled owner tuples covered beyond the two baseline tuples
    direction: positive
    threshold: '0'
  instrument: packing/devtools/wall_owner_containment.py
  instrument_ready: true
  regime: The exact exp143 patches and dots, exp144 and exp145 completed coverage receipts, and exp146
    sixteen wall-aware classes at q=96/25 and B=9977/10000; 128 logical containment slots.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: One 120-second external process plus two-second termination grace; 60-second cooperative
    internal clock after input loading.
  prereqs:
  - Astra Max source review and its three guard corrections pass focused synthetic controls.
  - Clean published implementation and prospective exp147 before any target relation.
  replication: false
  registered: '2026-09-09'
  notes: Count the union of two Cartesian products, excluding impossible labels and subtracting overlap.
    Complete zero expansion refutes this method only; partial or invalid execution is unresolved. Labels
    overlap in physical pose space. T-023 and the global bound remain unchanged unless separately justified.
---
# H145: Can Larger Owner Footprints Extend the Exclusion?

A guaranteed owner footprint lies inside every square in its owner class.
If four new footprints contain the four occupied patches used by an existing five-dot
certificate, that certificate also excludes the new four-owner class tuple.
All four component containments must use the same certificate family.

[Exp146](../series/series-000-smoke-and-calibration/experiments/exp-146-wall-owner-footprints.md)
found twelve strict footprint enlargements.
This hypothesis asks whether those gains actually transfer an exclusion beyond the two
already certified tuples.
The [containment contract](../../cases/n11_five_dot_cover/wall-containment-contract.md)
and
[source admission](../../cases/n11_five_dot_cover/wall-containment-source-admission.md)
define the transfer and its exact controls.

The 16⁴ label combinations are a finite bookkeeping space.
Their overlap means a count of covered labels is not a fraction of all physical
packings. A complete negative result rules out this component-containment extension,
while direct coverage by the same dots may still work without component containment.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
