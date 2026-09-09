---
title: "exp-138 \u2014 shared-screen four-owner obstruction verdict"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-138
  series: series-000
  title: Four-owner verdict from the shared exact footprint screen
  date: '2026-09-09'
  hypotheses:
  - H-138
  tier: exploratory
  subject:
    label: Exact translated BC232 depth-one family and full-net guaranteed owner footprints
    engine: devtools.screen_corner_dual_salvage and devtools.owner_footprints; published launch-head receipt
      binds source
    assurance: verified
    method: exact-algebraic
    host_system: Darwin arm64; project Python3.14.7; one process
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Source768 family has exact pointwise depth1 and mass21342289572/2055263195; point and triangle
      filters are nested geometric controls.
    candidate: Translate all original poses by(+1/100,+1/100), scale1; retain only full canonical direction
      members strictly separated from each endpoint footprint. Enumerate16one-corner and65536four-corner
      combinations for each of point,triangle,endpoint.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra, max; session113 coordinator
    entry_point: packing/devtools/screen_corner_dual_salvage.py
    budget: This record consumes the single shared exp137 producer receipt; it authorizes no second target
      process. All producer wall time is charged once to exp137. Complete65536endpoint classes required,
      with point/triangle nested controls.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-137-corner-dual-salvage.json.gz
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 5m .venv/bin/python3
      -m devtools.screen_corner_dual_salvage campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-family.json
      --footprint-kinds point,triangle,endpoint --corner-counts 1,4 --target-side 96/25 --expect-source-blob
      8a0bf1a264a1361649bc0acd0f70907ba8125f2f --out campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-137-corner-dual-salvage.json.gz
  lease:
    expires: '2026-09-09T04:15:00Z'
  results: []
  verdict:
    decision: in-progress
    primary_criterion: The minimum endpoint survivor mass over all65536four-owner combinations is at least7.
    reason: Prospective exact screen; no target masks or masses have been evaluated.
---
# Exp138: Four-Owner Verdict from the Shared Screen

This separate prospective verdict applies H138 to the four-owner portion of exp137’s
single producer receipt.
It authorizes no second process and charges no duplicate producer wall time.
The source, geometry, direction membership, exact SAT, complete class enumeration,
timeout and provenance obligations are exactly those declared in
[exp137](exp-137-corner-dual-salvage.md).

Accept H138 only if all65536endpoint-footprint combinations retain exact mass at least
seven. A lower mass rejects this specific retained-family claim; it does not prove that
the affected residual covering problem has a useful solution.
Incomplete data or a guard failure is unresolved.
This record was created before any target filtering, so a result on H137 cannot silently
dictate H138’s verdict.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
