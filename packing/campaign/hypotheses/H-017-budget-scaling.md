---
title: H-017 — 100x the budget reaches Trump's basin
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-017
  kind: hypothesis
  claim: >-
    The stock annealer at 100x the baseline budget (1e10 moves per chain) reaches within
    1e-4 of Trump's packing at n = 11 on at least one seed of five.
  lane: search
  derived_from: []
  strategy_refs: ['search:10']
  criterion:
    shape: record
    metric: best_side
    direction: lower
    threshold: 1e-4
  instrument: 'sqsearch --n 11 --budget-moves 10000000000, five seeds, gated by --selftest'
  instrument_ready: true
  regime: sqsearch 0.1.0, f64 screening, M1 Pro 8P+2E
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [11]}
  priority: 4
  cost_estimate: 4e11 moves, ~3 hours wall on 8 cores
  prereqs: []
  replication: false
  registered: '2026-08-22'
  runner:
    command: './sqsearch/target/release/sqsearch --n {n} --seed {seed} --chains 8 --budget-moves 10000000000'
    cells: [11]
    seeds: [1, 2, 3, 4, 5]
    timebox: 8h
  notes: >-
    Demoted to priority 4 and parked behind a short response curve. H-012 estimates a
    different P/Q/E attraction-probability ratio; it neither answers this fixed-budget
    reachability claim nor comes for free from the n <= 10 census. This recipe is
    operationally shaped but is not scientifically admissible unattended while D-044
    leaves independent pose validation and selftest receipts unresolved.
---
# H-017 — the crude version of the premise test

This probes one point on the budget-response curve for exp-001’s `n = 11` method.
Passing would show that this budget can reach the threshold on at least one declared
seed; failing would rule out neither larger budgets nor other schedules.

[H-012](H-012-record-basins-are-rare.md) asks a different question: the record-to-modal
attraction-probability ratio under one named `P/Q/E`. It needs a new identified `n = 11`
sample beyond H-011, so it is not a free or interchangeable substitute.
H-017 remains a low-priority response-curve cell rather than the default eight-hour run.

**The prediction is that it fails**, because the baseline proposer may assign very low
hit probability to the terminal component containing Trump’s construction.
Rigidity alone would not establish that: an isolated endpoint can have a positive-
measure preimage under a named quench, and the repository has not supplied its own
rigidity certificate for Trump’s packing.
H-012 is the direct proposer-conditioned measurement.
Recorded before the run, so the failure is evidence rather than a shrug.
A partial improvement — say `3.89` — resolves neither branch and should be recorded
`unresolved`, not argued into whichever story is preferred.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
