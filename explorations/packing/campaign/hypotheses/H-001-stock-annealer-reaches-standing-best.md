---
title: H-001 — the stock annealer reaches the standing best on every cell
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-001
  kind: hypothesis
  claim: >-
    The stock sqsearch annealer, at 100M moves per chain over 8 chains and 5 seeds,
    reaches within 1e-4 of the standing best on every cell of the sweep n = 10, 11, 12.
  lane: search
  derived_from: []
  strategy_refs: ['search:10']
  criterion:
    shape: record
    metric: best_side
    direction: lower
    threshold: 1e-4
  instrument: >-
    explorations/packing/run_baseline.sh, gated by sqsearch --selftest, scored against
    frontier/n-0{10,11,12}.md.
  regime: sqsearch 0.1.0, f64 screening, M1 Pro 8P+2E, deterministic seeds 1-5
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [10, 11, 12]}
  priority: 1
  cost_estimate: 12e9 moves, ~5 minutes wall
  prereqs: []
  replication: false
  registered: retroactive
  notes: >-
    The null hypothesis, and the one everybody would assume. Registered retroactive
    rather than dated because the artifact was written after the baseline numbers
    existed - the criterion and the control gates were fixed in the runbook first,
    but the registry entry was not, and back-dating it would launder that.
---
# H-001 — the null hypothesis

The claim anyone would make before looking: a general-purpose annealer, given a serious
budget, finds the best known packing.

It is worth registering precisely because it is expected to be *half* wrong, and the
shape of the failure is the campaign’s starting information.
Confirmed on `n = 10` and `n = 12` and refuted on `n = 11`, it says the instrument works
and the target is hard — which is a different and much more useful state of knowledge
than either “the searcher is broken” or “the searcher is fine”.

## Why the criterion is `1e-4`

That is the campaign’s `reached_basin` proxy: close enough that the search has almost
certainly found the right combinatorial class rather than a neighbouring one.
It is a proxy and not a proof — confirming the class means comparing contact graphs,
which is tier-2 work — so a round resolving this should say which it means.
