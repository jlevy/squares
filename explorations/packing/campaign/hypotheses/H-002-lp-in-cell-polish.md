---
title: H-002 — LP-in-cell polish is exact and sufficient
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-002
  kind: hypothesis
  claim: >-
    Alternating per-cell LP solves with local angle moves refines any annealer output to
    a genuine cell-optimum whose side matches the analytic value to LP precision on
    solved cases.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:17', 'search:19']
  criterion:
    shape: record
    metric: best_side
    direction: lower
    threshold: 1e-12 against the analytic value
  instrument: >-
    Not yet built. A scipy LP over the fixed-angle cell (the review implemented the
    single-cell half: 1056 constraints at Trump's angles), wrapped in an angle-move loop.
  instrument_ready: false
  regime: perturbed starts from known optima; n = 5, 10, 11
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 10, 11]}
  priority: 1
  cost_estimate: tier S (1e9 pair-tests)
  prereqs: []
  replication: false
  registered: retroactive
  notes: >-
    The single-cell half is already established, not hypothesised: the standing review's
    1056-constraint LP at Trump's angles reproduced s(11) to solver precision and every
    centre to 9e-16. What remains under test is the LOOP - angle moves between LP solves,
    and behaviour at cell boundaries. Kill: cycling between cells, or systematic gaps to
    the analytic optima.
---
# H-002 — the highest-priority item in the registry

Nearly everything waits on this.
Basin identity is unstable without a refiner, because “where the annealer stopped” is a
property of the cooling schedule rather than of the landscape.
The census, the rarity premise, the descriptors and the atlas all need a quench map with
a well-defined endpoint.

## The result this rests on is already verified

For fixed angles, and with each pair’s separating axis fixed, minimising `s` is a
**linear program**: corners are affine in centres, the separating-axis conditions are
linear inequalities, containment is linear, the objective is linear.
All of this problem’s nonconvexity lives in the angles and in the combinatorial choice
of cell.

The standing review implemented it: a 1,056-constraint LP at Trump’s eleven angles, with
the axis assignment read from the exact certificate, returned `s = 3.877083590023` —
matching the reference below `1e-12` — and recovered all eleven centres to `9e-16`. The
cell containing Trump’s packing, solved as an LP, *is* Trump’s packing.

## Why this campaign needs it specifically

[exp-001](../series/000-smoke-and-calibration/experiments/exp-001-baseline-sweep.md)
found the right basin at `n = 10` and stopped `4.19e-04` short of the proved optimum — a
polish failure, not an exploration failure, and the exact defect this hypothesis fixes.
It is also the campaign’s missing tier 2: without it, no screening result can be
sharpened into something the exact layer can certify.
