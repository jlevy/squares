---
title: "exp-261 \u2014 exact widened n17 feature-forcing certificate"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-261
  series: series-000
  title: Complete exact fixed-corner and pair-distance bounds over the widened tube
  date: '2026-10-07'
  hypotheses:
  - H-278
  tier: confirmatory
  subject:
    label: Conditional n17 omitted-feature bounds over the accepted root inclusion interval and B_W'.
    engine: devtools.check_n17_widened_features, frozen by the registration commit before target evaluation.
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, project Python3.14.7, one process; external scratch.
    selftest_passed: true
    engine_commit: bd391f8516c0f9bcbc186087a0eee6db55fc531d
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: Seventeen synthetic root/domain/identity/constants/arithmetic and receipt-rejection controls;
      independent Sol mechanical and Astra mathematical review.
    candidate: All152 distance bounds and1000 fixed-corner bounds, with exact complete identities
      and fresh reconstruction on replay.
    runs_per_condition: 1
    interleaved: false
    operator: Sol coordinator executes Astra's mathematical contract, Session184.
    entry_point: packing/devtools/check_n17_widened_features.py
    command: 'From packing/ with required external scratch variables: /Volumes/spud-ext1/agent-scratch/n17-w3-01a114fb/venv/bin/python3
      -m devtools.check_n17_widened_features --output campaign/series/series-000-smoke-and-calibration/results/exp-261-widened-feature-forcing/certificate.json;
      fresh invocation repeats with --certificate pointing to that receipt and --output replay.json.'
    budget: Combined180-second generation/replay ceiling; retain failure or partial receipts; no parameter
      expansion.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-261-widened-feature-forcing
    commit: bd391f8516c0f9bcbc186087a0eee6db55fc531d
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: Complete1152 exact bounds pass frozen constants and identity/domain controls; fresh
      receipt replay agrees.
    outcome: criterion_met
    checked_by: Production certificate and fresh replay each pass:19pairs,125features,eight vertices,
      exact analytic allowance -71/21000; root and complete identity/domain controls pass.
  verdict:
    decision: accepted
    primary_criterion: Complete1152 exact bounds pass frozen constants and identity/domain controls;
      fresh receipt replay agrees.
    reason: All1152 exact finite bounds pass and fresh reconstruction agrees; the uniform analytic
      bridge remains the separately scoped Astra hand derivation.
    needs_review: false
  effort:
    timebox: 180 seconds combined generation/replay; supervised with timeout
    stopped_by: criterion
    wall_seconds: 0.58
---
# exp-261: Widened Feature Forcing

This checks the H-278 finite interval contract without a numerical optimizer.
The generator and fresh checker each reconstruct the accepted-root geometry.
The source is frozen before the production receipt is generated.

Any acceptance concerns the declared feature-forcing subsystem.
It adds no exclusion to the admitted ledger and changes no published side bound.

## Outcome

The generation and fresh receipt replay both passed all 1,152 finite interval bounds.
The fixed analytical allowance is `-71/21000`. Source was frozen at `bd391f851`. No
numerical solve was used, and no admission or global side bound changed.
The command finished inside its 180-second ceiling; precise production/replay elapsed
time was not instrumented and is not inferred from synthetic-test timing.
A further fresh receipt replay was timed under a separate 60-second routine verification
ceiling and passed. The effort field records only that measured replay (0.58 seconds),
not total production and replay cost.
All three receipts and the timing log are retained.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
