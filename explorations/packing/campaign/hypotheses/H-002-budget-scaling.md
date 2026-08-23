---
title: H-002 — 100x the budget reaches Trump's basin
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-002
  kind: hypothesis
  claim: >-
    The same stock annealer at 100x the baseline budget (10^10 moves per chain) reaches
    within 1e-4 of Trump's packing at n = 11 on at least one seed of five.
  lane: search
  derived_from: []
  strategy_refs: ['search:10']
  criterion:
    shape: record
    metric: best_side
    direction: lower
    threshold: 1e-4
  instrument: >-
    sqsearch --n 11 --budget-moves 10000000000, five seeds, gated by --selftest.
  regime: sqsearch 0.1.0, f64 screening, M1 Pro 8P+2E
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [11]}
  priority: 1
  cost_estimate: 4e11 moves, ~3 hours wall on 8 cores
  prereqs: []
  replication: false
  registered: '2026-08-22'
  notes: >-
    Predicted to fail. Trump's packing is rigid, so it may be an isolated point rather
    than a basin with width, and no amount of undirected restarting finds a point of
    measure zero. Recording the prediction now is what makes the failure informative.
---
# H-002 — the cheapest fork in the campaign

This separates the two explanations for the baseline’s `n = 11` result, and almost
nothing else in the registry does it as cheaply.

If more compute closes the gap, the method is right and the campaign is about
efficiency: schedules, move sets, restart policies.
If 100× the budget moves the number barely at all, the method is wrong for this instance
and the campaign is about structure — priors, seeding, contact-graph enumeration — and
every budget-tuning row on the idea board is worth less than it looks.

**The prediction is that it fails**, and the reasoning is [H-004](H-004-basin-width.md):
rigidity means Trump’s configuration is determined by its contact conditions, so it
plausibly has no attracting neighbourhood at all.
Undirected restarts cannot find a point of measure zero.
A prediction written down before the run is what turns that failure into evidence rather
than a shrug.

## What would make this ambiguous

A partial improvement — say `3.89` — resolves neither branch cleanly.
That outcome should be recorded as `unresolved` with the number, not argued into
supporting whichever story the operator prefers.
