---
title: exp-263 — exact all-owner n17 patch readiness on a frozen ladder
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-263
  series: series-000
  title: One exact closed 16-angle patch covering all selected owner branches
  date: '2026-10-07'
  hypotheses: [H-280]
  tier: confirmatory
  subject:
    label: Exact bounded-residual patch on fixed S*,wide position tube and B_W',seeded by exp260 negative omega16.
    engine: devtools.check_n17_widened_annulus_patch,frozen by registration commit before target evaluation.
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64,project Python3.14.7,one process; external scratch.
    selftest_passed: true
  instance: {axis: n, point: 17, role: target}
  method:
    control: Thirty-three synthetic geometry,row-order,Decimal seed,closed-box,owner-hull,bounded-input,strict-margin,CLI-roundtrip and tamper controls; independent Sol mechanics and Astra mathematics.
    candidate: The frozen five-level clipped16-angle box ladder using one deterministic rationalized dual and all 256 owner combinations.
    runs_per_condition: 1
    interleaved: false
    operator: Sol coordinator executes Astra's mathematical contract,Session184.
    entry_point: packing/devtools/check_n17_widened_annulus_patch.py
    command: >-
      From packing/ with required external scratch variables:
      /Volumes/spud-ext1/agent-scratch/n17-w3-01a114fb/venv/bin/python3 -m
      devtools.check_n17_widened_annulus_patch --features
      campaign/series/series-000-smoke-and-calibration/results/exp-261-widened-feature-forcing/certificate.json
      --apex campaign/series/series-000-smoke-and-calibration/results/exp-264-widened-apex-replay-repair/certificate.json
      --output campaign/series/series-000-smoke-and-calibration/results/exp-263-one-annulus-patch/certificate.json;
      fresh invocation adds --certificate pointing to that receipt and writes replay.json.
    budget: Combined180-second production/fresh replay ceiling supervised by timeout; no new solve,seed,branch split or ladder change.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-263-one-annulus-patch
  lease:
    expires: '2026-10-07T08:40:00Z'
    host: macOS arm64
  results: []
  verdict:
    decision: in-progress
    primary_criterion: Strict positive eta and positive_patch_certified=true,complete 147 rows/all 256choices/closed 16angle box/exact prerequisite joins,fresh replay agrees.
    reason: Registered before target; execution waits for accepted H279 production and fresh replay in exp264.
---
# exp-263: One Exact Patch Readiness Check

This freezes the H-280 deterministic seed and five-box ladder before target evaluation.
The repaired apex prerequisite must pass first.
Structural verification alone cannot accept a patch whose exact margin is nonpositive.

All attempted boxes and margins are preserved.
A nonpositive ladder remains inconclusive; it supplies neither an annulus cover nor a
packing counterexample.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
