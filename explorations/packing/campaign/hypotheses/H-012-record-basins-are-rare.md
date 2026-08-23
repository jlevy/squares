---
title: H-012 — record basins are rare in quench measure
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-012
  kind: hypothesis
  claim: >-
    The proved-optimal basin's quench probability at n = 10, and Trump's at n = 11, sits
    orders of magnitude below the modal basin's, and rarity tracks rigidity (contact
    count, algebraic degree).
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:12']
  criterion:
    shape: determination
    metric: ratio of record-basin quench probability to modal-basin quench probability
    direction: below 0.1
  instrument: >-
    Not yet built. A query over H-011's census: rank basins by quench frequency and
    locate the record basin in the ranking.
  instrument_ready: false
  regime: same multistart distribution and polish backend as the census
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [10, 11]}
  priority: 1
  cost_estimate: tier S (a query over H-011's data)
  prereqs: [H-011]
  replication: false
  registered: retroactive
  notes: >-
    The load-bearing premise of the whole cartography program, registered so it can fail
    cheaply. Kill: record-basin probability within ~10x of the modal basin's - then blind
    multistart plus polish is already adequate, cartography loses its justification, and
    the program reverts to raw throughput.
---
# H-012 — the premise, made falsifiable first

The strategy layer rests on one claim: records are rigid, rigid optima live in rare
basins, and so scaling a volume-weighted sampler multiplies effort against a probability
the problem drives toward zero.
If that is right, “anneal harder” is a plan for finding the grid family ever more often.

The grounding is real but thin — Ellsworth’s 4-in-3,004 for `s(51)`, the 14 zero-gap
pairs in Trump’s packing, and the double-funnel precedent from energy-landscape science.
None of it is a measurement of *this* landscape, which is why this is registered with an
explicit kill criterion rather than assumed.

## Why it is placed this early

Because if it is wrong, most of the cartography program stands down in favour of raw
throughput — and that verdict is reachable in the cheapest tier, as a query over a
census that is worth building anyway.
A strategy that names the observation that would kill it is the kind worth having.

## What this campaign has already seen that bears on it

[exp-001](../series/series-000-smoke-and-calibration/experiments/exp-001-baseline-sweep.md)
is weak evidence for the premise: five independent seeds at `n = 11` all landed in a
narrow band `[3.9144, 3.9361]`, well short of Trump’s `3.8771`, with the band five times
narrower than the remaining gap.
That is what a sampler repeatedly finding the same wrong funnel looks like — but it is a
single configuration of a single method, and it measures nothing about basin volumes
directly. H-012 is the measurement.
