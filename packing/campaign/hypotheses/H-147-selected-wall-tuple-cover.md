---
title: H-147 — fixed five dots cover the first analytically surviving tuple
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-147
  kind: hypothesis
  claim: The unchanged five-dot pattern D covers the full residual-core centre domain for the explicit
    wall-owner tuple (m1:j0,m1:j0,m1:j0,m1:j7) in BL,BR,TL,TR order.
  lane: proof
  derived_from: []
  criterion:
    shape: determination
    metric: Complete all361 required unique directions with exact zero uncovered area for the specified
      tuple
    direction: positive
    threshold: '0'
  instrument: packing/devtools/wall_owner_selected_cover.py
  instrument_ready: true
  regime: Exactly tuple(0,0,0,7), q=96/25, B=9977/10000, exp143 five dots and exp146 wall polygons; no
    seed stage or tuple search.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: One five-minute external process plus two-second termination grace and a shared240-second
    internal guard after input loading.
  prereqs:
  - Astra Max thin-wrapper source admission and focused complete/deficit/partial/provenance controls.
  - Clean published source and prospective exp149 before any target coverage.
  replication: false
  registered: '2026-09-09'
  notes: This is a specified-tuple claim. A complete zero-deficit full net accepts; a positive deficit
    with independently replayed strict escape refutes this tuple cover only. H146 existence over other
    tuples remains unresolved on a negative result. Selection follows analytic symmetry of exp148 witnesses;
    no completed seed bank is asserted.
---
# H147: Check One Small Surviving Tuple

The analytic symmetries of exp148’s two strict escapes leave 4,094 nonbaseline class
labels. The first is (0,0,0,7), using m1:j0 at BL, BR and TL, and m1:j7 at TR. All four
selected wall footprints equal their old endpoint footprints and have four vertices, so
the exact cover check avoids the large polygon families that slowed the seed bank.

The [selection argument](../../cases/n11_five_dot_cover/after-exp148-strategy.md) is
separate from cover validity.
This hypothesis fixes one tuple and requires all361 orientations.
Its failure would not refute existence of another fixed-dot cover.

**Result: refuted.** Exp149 stopped correctly at its first required direction.
The positive exact uncovered area and independently replayed rational strict escape
reject this selected tuple only; H146 remains unresolved.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
