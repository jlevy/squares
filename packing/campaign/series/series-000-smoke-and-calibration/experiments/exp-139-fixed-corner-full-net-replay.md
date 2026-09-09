---
title: "exp-139 \u2014 exact full-net fixed-corner residual replay"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-139
  series: series-000
  title: Exact full-net replay of unchanged fixed-corner residual weights
  date: '2026-09-09'
  hypotheses:
  - H-140
  tier: confirmatory
  subject:
    label: Published exp136 rationalized residual measure and fixed four-flush-corner domain
    engine: devtools.verify_residual_cover_pilot using exact_minimum_covered_mass; frozen source identified
      by launch receipt
    assurance: verified
    method: exact-algebraic
    host_system: Darwin arm64; project Python3.14.7; one process
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Validate the exact published exp136 settings, original361-site support and numerical-to-rational
      atom reconstruction; retain all88residualatoms unchanged.
    candidate: Exact rational event-domain minimum at every one of181folded directions, including omitted
      pilot directions; no repeated LP, new atom or newweight search.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra,max; session113 coordinator
    entry_point: packing/devtools/verify_residual_cover_pilot.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 5m .venv/bin/python3
      -m devtools.verify_residual_cover_pilot campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-136-paired-cover.json
      --expect-source-blob 2b34bdc8842edc836402bd42fe8362e9103ab253 --scope full-net --arms residual --max-atoms
      1000 --max-event-cells 2000000 --out campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-139-exact-full-net-residual.json
    budget: One target reader under five-minute externaltimeout plus2secondTERM grace. Max1000atoms and2millioneventcells
      per direction, checkedbeforeallocation. Complete181directions required. Flushed per-direction progress
      survives interruption; no retries or weight changes.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-139-exact-full-net-residual.json
  lease:
    expires: '2026-09-09T04:35:00Z'
  results: []
  verdict:
    decision: in-progress
    primary_criterion: Exact minimum over all181directions is at least1 for the unchanged residualatoms.
    reason: Prospective exact verification; no target minimum evaluated.
---
# Exp139: Exact Full-Net Residual Replay

This verification follows the positive numerical exp136 result.
The unchanged raw receipt is clean tracked Gitblob
`2b34bdc8842edc836402bd42fe8362e9103ab253`. The exact residual measure has88atoms and
mass `7804903/1000000`. No target minimum has been evaluated at registration.

Accept H140 only if the exact minimum over the complete181folded direction net is at
leastone. A smaller complete minimum rejects the unscaled claim.
A guard or incomplete run is unresolved.
The primary test does not normalize weights.

As a predeclared secondary consequence, if the completed full-net minimum m is positive,
report `7804903/(1000000*m)` as the mass of a feasible rescaled cover.
This is algebra applied to the verified minimum, not another LP experiment.
The full-net D4/strict-core transfer requires `B(1+D)<1`, with its exact bound proved in
the retained transfer review.
The conditional contradiction threshold is seven.
Neither a feasible rescaled cover above seven nor a difference of two primal objectives
proves an optimum-gap improvement.

Preserve per-direction progress, final receipt, actualHEAD/UTC/exit/wall evidence.
The source and reader must be committed and pushed before invocation.
The broader unavoidable-owner branch program remains separate from this fixed-corner
example.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
