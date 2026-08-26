---
title: H-048 — does the cheap glued screen preserve the soft-mode ranking?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-048
  kind: hypothesis
  claim: >-
    On the proved cells n = 5 and n = 10, the stratum that is optimal under the soft
    fixed-angle LP is ranked in the top decile by the glued-chunk LP screen, so screening
    with glued equality rows and re-solving only the top decile finds the same winner as
    solving every stratum soft.
  lane: search
  derived_from: [X-003]
  strategy_refs: ['search:15', 'search:17']
  criterion:
    shape: paired
    metric: >-
      rank of the soft-mode winning stratum within the glued-mode ranking, per cell, and
      the LP-solve cost of screened versus exhaustive soft solving
    direction: soft-mode winner within the top decile of the glued ranking on every cell
    threshold: 0.1
  instrument: >-
    The stage-1 enumerator, the glued-chunk equality rows, and the existing soft
    cell-read LP quench, each stratum solved both ways with retained LP-solve counts.
  instrument_ready: false
  regime: >-
    numerical f64 LP under the measured 1e-11 solver floor; proved cells only, so the
    correct answer is known independently of either ranking
  instance: {axis: n, point: 10}
  sweep: {axis: n, points: [5, 10]}
  priority: 3
  cost_estimate: >-
    tier S; two LP solves per stratum on the proved cells, priced in counted solves
  prereqs: [stage-1 enumerator, glued-chunk LP rows]
  replication: true
  registered: '2026-08-26'
  notes: >-
    An efficiency claim about the pipeline, not about the packing landscape, and it is
    registered because the enumerator's whole cost model assumes it. If glued ranking
    does not preserve the soft winner, the cheap screen must be dropped and every
    stratum solved soft, which changes the budget for H-045 by roughly the decile
    factor. Running it on proved cells is deliberate: the correct answer is known from
    the analytic optimum, so a screen failure cannot be mistaken for a landscape fact.
    Aligned and glued strata are the most degenerate cells the pipeline solves, so this
    round is also where any residual D-059 instability would surface as an unstable
    ranking rather than as a wrong value.
---
# H-048 — whether the cheap screen can be trusted

The enumerator’s cost model has two tiers: a **glued** screen that treats each chunk as
a rigid tile, reducing the LP to roughly `2k + 1` variables, and a **soft** re-solve
that frees every square within its angle class.
Screening is only worth doing if the glued ranking keeps the eventual winner near the
top.

This is a pipeline-efficiency question rather than a claim about packings, but it is
registered rather than left informal because the budget for
[H-045](H-045-chunk-grammar-rediscovery.md) depends on the answer.
If the screen is faithful, enumeration costs one cheap solve per stratum plus one
expensive solve per top-decile stratum.
If it is not, every stratum needs the full soft solve and the enumerable `n` shrinks
accordingly.

The cells are the proved ones on purpose.
At `n = 5` and `n = 10` the analytic optimum is known, so a disagreement between the two
rankings is unambiguously an instrument fact.
It is also the natural place for any leftover degenerate-cell instability
([D-059](../../defects.md)) to appear, since a glued aligned stratum is the most
tie-rich linear program this pipeline will ever hand a solver.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
