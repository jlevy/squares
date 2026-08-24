---
title: H-025 — record orientations are quantitatively compressible
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-025
  kind: hypothesis
  claim: >-
    For at least 80 percent of standing-record poses at n <= 100 with public full
    geometry at the preregistered corpus freeze, constraining orientations to at most
    three fitted classes modulo quarter turns and reoptimizing centers and class angles
    increases the required side by at most 1e-4.
  lane: search
  derived_from: [X-002]
  strategy_refs: ['search:1', 'search:6', 'search:17']
  criterion:
    shape: conditions
    metric: fraction of the preregistered verified record corpus meeting the three-class refit loss bound
    direction: at least 0.8
    threshold: 0.8
  instrument: >-
    Freeze eligible source URLs and hashes before fitting; import and independently
    verify every eligible full pose or count it unresolved in the denominator. Cluster
    folded orientations under a preregistered loss, reoptimize centers and class angles
    with the common spine, and independently verify every refit. Report the whole loss
    distribution, unresolved fraction, and n = 29 separately.
  instrument_ready: false
  regime: public full-geometry record corpus frozen before fitting; n <= 100; 1e-4 side-loss threshold
  instance: {axis: corpus, point: verified-records-n-le-100}
  priority: 2
  cost_estimate: tier S on n = 17 and 29; tier M only after the geometry importer is checked
  prereqs: [verified geometry corpus]
  replication: true
  registered: '2026-08-24'
  notes: >-
    This is the non-brittle successor to H-024. Six raw orientation classes at n = 29
    can refute H-024 while still being well approximated by a low-dimensional class
    model. Compression is an algorithmic property of the declared refit, not an exact
    statement about the source pose.
---
# H-025 — replace a universal class count with a loss curve

Raw angle equality is too fine and too brittle to carry the strategy premise.
This test asks whether a small number of fitted class angles preserves record quality,
and records where it does not.
A negative result is useful: it tells the proposer not to compress that mechanism.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
