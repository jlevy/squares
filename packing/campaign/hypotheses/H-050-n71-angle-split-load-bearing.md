---
title: H-050 — is the n = 71 two-class angle split load-bearing?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-050
  kind: hypothesis
  claim: >-
    The n = 71 incumbent's split of sixteen oblique squares across two angle classes
    0.0358 degrees apart is load-bearing: no configuration with those sixteen squares
    merged to one shared angle achieves side strictly less than 8.94407155757031 under
    the fixed-angle LP, anywhere in a bracketed sweep of the shared angle.
  lane: search
  derived_from: [X-009]
  criterion:
    shape: determination
    metric: >-
      minimum side over a fixed-angle LP sweep of the merged 16-square block's shared
      angle across at least [50.10, 50.21] degrees, against the incumbent side
    direction: >-
      refuted if any bracketed angle beats the incumbent by more than 1e-8; supported if
      the sweep's minimum is at or above the incumbent everywhere
  instrument: >-
    The LP-in-cell quench's fixed-angle solve with the angle bracketed by the outer
    loop, budgeted in LP solves per D-126, above the D-021 floor.
  instrument_ready: false
  regime: >-
    numerical f64 LP above the measured 1e-11 solver floor; any apparent gain below
    1e-8 reads as failure, and the assurance contract forbids a numerical result
    carrying beat_record
  instance: {axis: n, point: 71}
  priority: 2
  cost_estimate: >-
    tier S; one LP solve per bracketed angle, counted, not timed
  prereqs: [BC-090's s(17) calibration gate must pass first, per X-009]
  replication: true
  registered: '2026-08-31'
  notes: >-
    Registered by X-009 under BC-088. n = 71 is the one annealed incumbent where the
    retained catalogue records cold search failing (Schadt's from-randomness plateau at
    8.95539101419843 against the seeded record), so the split is either the last 2.7e-5
    of a real optimum or the residue of a stochastic polish; this hypothesis is the
    cheapest way to tell them apart, and a refutation is a direct search lead.
---
# H-050 — Is the n = 71 Two-Class Angle Split Load-Bearing?

The incumbent spends two angle classes `0.0358°` apart on one sixteen-square block that
the atlas's regularized sweep already merges at `1e-3` radians. Either the split buys
the last `2.7e-5` of side, or a cleaner nearby structure exists and cold search never
found it. A bracketed fixed-angle LP sweep decides which, for the price of counted LP
solves.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
