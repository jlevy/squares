---
title: "exp-136 \u2014 repaired fixed-corner matched pilot"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-136
  series: series-000
  title: Repaired fixed-corner matched pilot
  date: '2026-09-09'
  hypotheses:
  - H-136
  tier: exploratory
  subject:
    label: matched finite-site and finite-direction covering LPs with zero or four fixed corner obstacles
    engine: devtools.run_residual_cover_pilot with exact event fallback; launch-head receipt binds published
      repair
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 64
      rounding: scipy HiGHS proposals and float event-cell search; output atoms rounded by the retained
        rationalise_sites routine at scale 4000000, without treating rounding as verification
    tolerance: Numerical convergence uses the instrument's 1e-9 row-addition threshold and retained LP_FEASIBILITY
      allowance. The paired accept margin is strictly greater than 0.001. No numerical comparison establishes
      a packing bound.
    host_system: Darwin 25.5.0 arm64; ten logical CPUs; Python 3.14.7; one process, sequential arms, default
      solver threading
    selftest_passed: true
    engine_commit: 03d2925e
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Unrestricted B-core covering program on the declared grid and direction subset
    candidate: The same program with cores restricted to avoid the interiors of four fixed axis-aligned
      unit squares flush in the container corners
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra, max; coordinator of session-113
    entry_point: packing/devtools/run_residual_cover_pilot.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 5m .venv/bin/python3
      -m devtools.run_residual_cover_pilot --side 96/25 --shrink 9977/10000 --grid-counts 19 --direction-steps
      180 --direction-indices 0,23,45,68,90,113,135,158,180 --deadline-seconds 120 --max-rounds 60 --rows-per-direction
      4 --max-event-cells 2000000 --max-round-cells 15000000 --scale 4000000 --output campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-136-paired-cover.json
    budget: Two sequential arms with 120-second cooperative deadlines and sixty rounds each; a five-minute
      external timeout with two-second TERM grace bounds the process. Four rows per direction per round,
      at most two million dense event cells per direction and fifteen million per round. One site grid,
      one direction subset, no target retries or tuning. An interrupted arm may lack its final solver
      point; preserve any completed arm and partial receipt and record the missing evidence explicitly.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-136-paired-cover.json
    commit: 03d2925e
  results:
  - shape: determination
    role: outcome
    question: Did both arms converge with Mglobal minus Mresidual minus4 greater than0.001?
    outcome: criterion_met
    checked_by: 'Raw paired receipt: unrestricted11.981481481481488; residual7.804878048780487; matched
      gap improvement0.17660343270100132. Both arms converged; no exact validation in this experiment.'
  complexity:
    lines_changed: 0
    new_dependencies: []
    new_failure_modes:
    - conflating a finite-direction numerical cover with an all-angle exact certificate
    - comparing different supports or forgetting the four-unit change in contradiction threshold
    - filling gaps between the six convex residual-domain components
    - treating an uncompleted arm as a negative result
    notes: Pre-target estimate only, with 361 sites in 55 orbits. Maximum dense cells per direction are
      525625 unrestricted and 546121 residual; the corresponding sums over nine directions are 4206521
      and 4370649. No objective was evaluated to select this regime.
  verdict:
    decision: accepted
    primary_criterion: Both arms converge numerically and M_global minus M_residual minus 4 is strictly
      greater than 0.001
    reason: The predeclared numerical paired margin is positive by0.17660343270100132. Residual mass remains
      above7; this is a finite-support finite-direction mechanism result, not a packing exclusion or exact
      optimum-gap bound.
  effort:
    timebox: Five-minute external timeout with two-second grace;120seconds perarm
    wall_seconds: 3.06
    stopped_by: criterion
---
# Exp136: Repaired Fixed-Corner Pilot

The published-source process completed successfully in3.06seconds. Both numerical arms
converged: unrestricted11.981481481481488, residual7.804878048780487, and gap
improvement0.17660343270100132. The original numerical criterion is accepted; exact
verification is a separate promotion.
Raw launch, exit, process and paired receipts are retained inresults/agenda032.

This is a fresh experiment after exp135 stopped on an unrepresentable thin-cell witness.
The repair has an independent synthetic regression control.
It rebuilds ambiguous event geometry from original rational sites; LP weights remain
numerical. The support, direction indices, guards, round counts and accept margin match
exp135. No target tuning or silent retry is permitted.
Source must be committed and pushed; retain launch HEAD, UTC instant, exit status,
process log and the raw paired receipt.

Both numerical arms must converge and `Mglobal − Mresidual − 4 > 0.001` for acceptance.
A residual mass below seven is an additional signal, not a proof.
Any guard, timeout or separator failure leaves the comparison unresolved.
A completed score at most 0.001 rejects this fixed numerical claim only.
Full-direction and exact coverage would require a separate promotion protocol.

Admission is within session113 BC310; external timeout is five minutes with two-second
TERM grace. Only one target process is admitted by this record.
The earlier exp135 artifacts are retained without alteration.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
