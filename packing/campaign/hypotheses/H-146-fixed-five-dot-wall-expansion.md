---
title: H-146 — the fixed five dots exclude another wall-owner tuple
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-146
  kind: hypothesis
  claim: The unchanged five-dot pattern D covers at least one wall-footprint tuple beyond the two already
    certified baseline tuples.
  lane: proof
  derived_from: []
  criterion:
    shape: determination
    metric: Existence of an additional completely verified fixed-five-dot owner tuple
    direction: positive
    threshold: '0'
  instrument: packing/devtools/wall_owner_fixed_pattern.py
  instrument_ready: true
  regime: The exact exp143 five dots, exp146 sixteen wall footprints, and exp147 baseline tuple set at
    q=96/25 and B=9977/10000. Nine fixed seed directions and at most one selected candidate checked on
    all361 required directions.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: One five-minute external process plus two-second termination grace, 240-second shared
    internal guard and60-second seed-stage guard.
  prereqs:
  - Astra Max fixed-pattern source admission and focused strict-witness, SAT, mask, provenance and deadline
    controls.
  - Clean published source and prospective exp148 before any target witness or cover is computed.
  replication: false
  registered: '2026-09-09'
  notes: Accept only a new all361 zero-deficit cover with valid physical transfer. Refute only if independently
    replayed escapes cover every nonbaseline tuple. A failed selected candidate normally leaves the existence
    hypothesis unresolved. Counts of removed labels are mechanism evidence, not substitutes for the existence
    question.
---
# H146: Do the Same Five Dots Cover Another Owner Case?

Exp147 rules out transferring either existing certificate by component containment.
A direct five-dot cover can still work: it need not contain those particular occupied
patches. This experiment therefore keeps the dots fixed and tests the residual domains
themselves.

A rational escaping core gives a negative witness for every four-owner tuple whose
footprints it avoids.
The [reviewed strategy](../../cases/n11_five_dot_cover/after-wall-gain-strategy.md) uses
nine fixed directions to collect reusable witnesses, then tests only the first surviving
new tuple on the complete direction net.

Exp148 returned partial at its seed-stage guard in 74.03 seconds.
Two checked escapes reject 49,152 labels, but no seed direction finished and no
candidate was checked.
The existence hypothesis remains unresolved.

One failed candidate does not refute existence over the other tuples.
Refutation needs checked escapes for all nonbaseline labels.
Any new cover remains a conditional packing exclusion; the global case-coverage gap and
shared analytic transfer remain explicit.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
