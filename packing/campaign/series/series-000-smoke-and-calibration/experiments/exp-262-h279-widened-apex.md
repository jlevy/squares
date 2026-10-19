---
title: "exp-262 \u2014 exact conditional n17 apex radius and independent replay"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-262
  series: series-000
  title: Exact retained-position-dual residuals and an inner apex cube
  date: '2026-10-07'
  hypotheses:
  - H-279
  tier: confirmatory
  subject:
    label: Conditional fixed-container physical-packing apex bridge inside the widened n17 region.
    engine: devtools.check_n17_widened_apex, frozen by registration commit before target evaluation.
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, project Python3.14.7, one process; external scratch.
    selftest_passed: true
    engine_commit: 513adb1bf3da8f46d82b18197e8bcc9a38afbb1a
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: Sixteen synthetic matrix/dual/sign/domain/premise/radius and tampered-receipt controls,
      independently rerun; Sol mechanical and Astra mathematical reviews.
    candidate: Exact58 signed-position residuals, epsilon,C,alpha0,q0 and position headroom, with
      complete identities and fresh reconstruction.
    runs_per_condition: 1
    interleaved: false
    operator: Sol coordinator executes Astra's mathematical contract, Session184.
    entry_point: packing/devtools/check_n17_widened_apex.py
    command: 'From packing/ with required external scratch variables: /Volumes/spud-ext1/agent-scratch/n17-w3-01a114fb/venv/bin/python3
      -m devtools.check_n17_widened_apex --features campaign/series/series-000-smoke-and-calibration/results/exp-261-widened-feature-forcing/certificate.json
      --output campaign/series/series-000-smoke-and-calibration/results/exp-262-widened-apex/certificate.json;
      fresh invocation adds --certificate pointing to that receipt and writes replay.json.'
    budget: Combined180-second generation/replay ceiling, supervised with timeout; preserve failures;
      no new solve or parameter expansion.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-262-widened-apex
    commit: 513adb1bf3da8f46d82b18197e8bcc9a38afbb1a
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: Complete exact identities and premise joins; allweights nonnegative,epsilon<1,C>0,positive
      frozen-formula radii and fresh replay agreement.
    outcome: invalid
    checked_by: Production exact checker passes, but required fresh CLI replay refuses with oversized
      bare JSON integer. Replay failure prevents acceptance.
  verdict:
    decision: blocked
    primary_criterion: Complete exact identities and premise joins; allweights nonnegative,epsilon<1,C>0,positive
      frozen-formula radii and fresh replay agreement.
    reason: Apex arithmetic passed, but the receipt encodes retained integer weights beyond the reader
      guard; fresh replay refuses. Repair the serialization and preregister a successor before retry.
    needs_review: false
    resume_from: Preserved production certificate, failed replay and timing.log; instrument serialization
      repair plus same-claim replication exp264 required.
  effort:
    timebox: 180 seconds combined production and fresh replay
    wall_seconds: 3.87
    stopped_by: criterion
---
# exp-262: Conditional Apex Radius

This round reuses accepted witnesses without a new optimization search.
The H-278 feature receipt must pass its own reconstruction before use.
Exact finite arithmetic and the hand implication retain distinct assurance scopes.

Any acceptance concerns the declared apex subsystem and makes no new ledger admission.
The outer capture, annulus and slider-domain obligations remain open.

## Outcome

The production arithmetic check passed at clean source `513adb1bf`, but the required
fresh CLI replay refused an oversized bare JSON integer in the serialized selected dual
cell. The run is blocked and H-279 is not accepted.
The combined command took 3.87 seconds and returned exit1. The generated certificate,
failed replay and timing log are preserved.
A source repair and separately registered same-claim replication are required before
retry; no radius, weight, domain or criterion is retuned.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
