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
    Demoted to priority 4 on merging with the standing review's register: H-012 answers
    the same question far better. This tests budget scaling as a proxy for basin rarity;
    H-012 measures basin rarity directly, off a census worth building anyway. Kept
    because it is the one runnable-today item bearing on the premise, and because a
    cheap crude confirmation before an expensive precise one is not waste.
---
# H-017 — the crude version of the premise test

This separates the two explanations for exp-001’s `n = 11` result — needs more compute
versus needs a different method — by the blunt instrument of multiplying the budget.

[H-012](H-012-record-basins-are-rare.md) tests the proposed explanation more directly,
by measuring the record component’s quench probability against the modal component’s
under a named regime, and it does so as a query over a census the campaign wants
regardless.
That is more discriminating evidence, so this is now the fallback rather than
the plan.

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
