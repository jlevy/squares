---
title: H-070 — a margin-biased seed improves the released n = 11 fractional search
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-070
  kind: hypothesis
  claim: >-
    At n = 11, outer side 191/50, and B = 9977/10000, the eligible minimum-mass
    candidate from the three declared one-round inset screens, when mapped by centre
    into the unrestricted inset-1/2 search, produces after the same stopping class and
    number of completed column rounds a frozen exact rational total mass strictly below
    an equal-budget unseeded control.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:21', 'proof:22', 'proof:23']
  criterion:
    shape: paired
    metric: >-
      exact rational total_mass of the released seeded candidate versus the unseeded
      control, conditional on strict JSON, equal stopping class, equal completed column
      rounds, and candidates from both arms
    direction: >-
      accepted only if the released seeded total is strictly smaller; rejected if it is
      equal or larger; a deadline stop, unequal status or round count, missing candidate,
      invalid JSON, or failure of all three screens leaves the comparison unresolved
    threshold: null
  instrument: >-
    devtools.run_fractional_colgen: three sequential one-column-round screens at insets
    1/2, 2962983/4505800, and 15513/20000, followed by matched seeded-release and unseeded
    runs at inset 1/2 with eight column rounds and 2520-second deadlines
  instrument_ready: true
  regime: >-
    One numerical thread per process; side 191/50; shrink 9977/10000; grid counts
    25,34,41; direction steps 180; rationalisation scale 4000000; three rows per
    direction. The published Massaccesi quantity M is doubled margin, so 15513/10000
    maps to the one-sided driver inset 15513/20000. The comparison is a routing result,
    not proof that the margin caused an improvement.
  instance: {axis: n, point: 11}
  sweep:
    axis: one-sided inset
    points: ['1/2', '2962983/4505800', '15513/20000']
  priority: 1
  cost_estimate: >-
    At most 30 active portfolio minutes for three screens and 42 minutes of one-core
    process time per matched follow-on arm; analysis and landing continue only through
    T+2.
  prereqs:
  - BC-219 frozen launch packet
  - strict deadline JSON controls for devtools.run_fractional_colgen
  replication: false
  registered: '2026-09-05'
  notes: >-
    A fully decided candidate of total mass below eleven takes the existing exact
    certificate route immediately and outranks this paired comparison. The optional
    scalar 61/16 process is deliberately not allocated in the T+0 through T+2 block:
    it is not one of the six opened cells and cannot finish before the minute-90 launch
    freeze.
---
# H-070 — Inset Seed, Then Unrestricted Release

This claim tests whether an inset is useful as a proposal distribution after its support
restriction is removed.
It does not treat the inset grid as an unavoidable set and does not infer that walls are
irrelevant.

The comparison is deliberately strict.
Both arms must leave readable exact candidate bytes after the same number of completed
rounds and the same stopping class.
A float LP objective or an unmatched deadline says nothing about the claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
