---
title: "exp-259 \u2014 current admitted n17 residue partition control"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-259
  series: series-000
  title: Complete D4 and composition/distance partition of the current admitted n17 residue
  date: '2026-10-07'
  hypotheses:
  - H-276
  tier: confirmatory
  subject:
    label: Current unique-state n17 cover at U=1169/250 under58 admitted entries.
    engine: devtools.stratify_n17_certified_residue; source frozen by the registration commit before
      measurement.
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, project Python3.14.7, one process; external scratch.
    selftest_passed: true
    engine_commit: 68a924c657171a413fbe7c6a9cfefb40f860b8aa
  instance:
    axis: n
    point: 17
    role: calibration
  method:
    control: Standing certified census from Session183 plus independent synthetic orbit enumeration;
      six focused controls pass.
    candidate: Full canonical orbit roster with composition/distance strata; no optional producer
      receipts.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6.1 Sol coordinator, Session184
    entry_point: packing/devtools/stratify_n17_certified_residue.py
    command: 'From packing/ with TMPDIR, UV_CACHE_DIR and CARGO_TARGET_DIR under verified external
      scratch: /Volumes/spud-ext1/agent-scratch/n17-w3-01a114fb/venv/bin/python3 -m devtools.stratify_n17_certified_residue
      --output campaign/series/series-000-smoke-and-calibration/results/exp-259-current-admitted-residue/partition.json'
    budget: Two-minute measurement ceiling; no exclusion search or admission mutation.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-259-current-admitted-residue
    commit: 68a924c657171a413fbe7c6a9cfefb40f860b8aa
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: Exact census36784states/4685orbits/58admissions, complete disjoint orbit and stratum
      sums, endpoint survives.
    outcome: criterion_met
    checked_by: 'Standing census and complete exact orbit/stratum accounting agree: {''admitted'':
      58, ''endpoint_survives'': True, ''orbits'': 4685, ''surviving_states'': 36784}; 32 strata.
      All attempt diagnostics mean no optional receipts supplied.'
  verdict:
    decision: accepted
    primary_criterion: Exact census36784states/4685orbits/58admissions, complete disjoint orbit and
      stratum sums, endpoint survives.
    reason: The complete current-ledger roster agrees with the standing census and preserves the endpoint;
      this admits no new exclusion.
    needs_review: false
  effort:
    timebox: 120 seconds for the population control
    wall_seconds: 2.232
    stopped_by: criterion
---
# exp-259: Actual Admitted Residue Control

This is the first population control for BC-432 in Session184. Its source and H-276
criterion are committed before the real-ledger command.
The accepted ledger remains unchanged from `f3a13e3a2`. The instrument must preserve
every surviving assignment state, endpoint included; no new exclusion is admitted by
this round.

The complete roster is retained for Astra’s subsequent workload selection.
All diagnostic labels initially mean only that no optional receipts were supplied.
They do not mean these states have never been attempted.

## Outcome

The complete retained partition has 36,784 states in 4,685 orbits under 58 admitted
entries, the endpoint surviving, across 32 strata.
Its measured census/partition phase took 2.232 seconds.
The four distance-two strata hold 95 orbits, matching the historical count but now
checked against the actual admitted ledger.
No attempt receipts were supplied; no state is declared historically untested.

The first invocation completed its computation but failed to publish because the
coordinator had not created the declared output directory.
No result was retained from that attempt, and its computation time is unavailable.
After creating the directory, the unchanged source and criterion produced the retained
result.
The effort field measures the retained successful census/partition phase and does
not claim total cost for the failed publication attempt.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
