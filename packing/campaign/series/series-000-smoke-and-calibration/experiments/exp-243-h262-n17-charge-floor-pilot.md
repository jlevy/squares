---
title: "exp-243 — n17 charge-floor census pilot"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-243
  series: series-000
  title: Subcontainer cuts and R068 per-cell charge floors on the H259 grid at cap 1169/250
  date: '2026-10-02'
  hypotheses:
  - H-262
  tier: exploratory
  subject:
    label: H260 closed-assignment D4 orbits on the H259 grid; the s(6) and s(10) subcontainer cuts; per-cell
      floors of R068's charge with its sites, rules and weights kept and the parent side forced to
      A_U = 4.613/4.676, evaluated on open parents.
    engine: devtools.pilot_n17_charge_floors, with an independent review that recomputed the floors by
      direct rule evaluation and recounted the census by two separate methods
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64 remote session container, project Python 3.14.7, two workers
    selftest_passed: true
    engine_commit: 1a8a5e4a5e61721831ff6e35d3b3aecdc5831726
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: The H260 universe (161,100,756 states, 20,155,518 orbits) and the route review's cut-only state
      count reproduce; at R068's own parent side the corner minimum is exactly Gamma = 1,000,026,844, as
      the replayed ledger says; the endpoint's own pattern survives with direct pose charges summing to
      11,797,143,406, below M. Fourteen tests, ruff and BasedPyright clean.
    candidate: Floors sampled as charges of legal poses (exact arrangement sweep in position over a refined
      angle grid), so each is an upper estimate of the exact floor and every survivor count is a lower
      bound on an exact instrument's.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 167; lane B built the pilot, the coordinator replayed it from a clean worktree
    entry_point: packing/devtools/pilot_n17_charge_floors.py
    command: 'From packing: .venv/bin/python3 -m devtools.pilot_n17_charge_floors --output FILE --workers 2.
      Exact lines in run-001 command.txt.'
    budget: Planning pilot of about two hours; target run about two minutes on two workers.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-243-n17-charge-floor-pilot/run-001
    dirty: false
    commit: 1a8a5e4a5e61721831ff6e35d3b3aecdc5831726
  results:
  - shape: determination
    role: outcome
    question: How many H260 orbits survive the two cuts and the R068 floors at U?
    outcome: criterion_missed
    checked_by: Floors run from 0.063 (corner) to 0.930 (interior edge) of M/17, so the floor test excludes
      nothing. The cuts leave 61,563,363 states and 7,703,312 orbits by exact Burnside count, and the floors
      leave the same. The independent review reproduced every floor to the unit and recounted the census
      by Burnside and by a row transfer DP.
  - shape: determination
    role: guard
    question: Can any single D4-symmetric linear per-cell floor vector meet the 10^4 threshold?
    outcome: criterion_missed
    checked_by: An antipodal-pair argument over the recounted class-count table leaves at least 30,966
      orbits for every such vector and every valid charge, so H-262's confirmation branch is impossible for
      its registered class. The bound lies inside H-262's inconclusive band, and it does not apply to
      asymmetric, multi-charge, orientation-refined or nonlinear floors.
  verdict:
    decision: rejected
    primary_criterion: At most 10^4 surviving orbits confirms; more than 10^5 rejects the engine; between is
      inconclusive.
    reason: The registered claim (at most 10^4 survivors) is false for every D4-symmetric per-cell floor
      vector by the ceiling theorem; R068's dictionary at U leaves 7,703,312, rejecting that engine outright.
      The exact six-sweep instrument is unnecessary. Asymmetric and nonlinear floors remain open and belong
      to a new hypothesis.
    needs_review: false
    commit: 1a8a5e4a5e61721831ff6e35d3b3aecdc5831726
  effort:
    timebox: 900 seconds; two workers
    wall_seconds: 133
    stopped_by: criterion
---
# exp-243: n17 Charge-Floor Census Pilot

[H-262](../../../hypotheses/H-262-n17-conditional-charge-occupancy-census.md) asked
whether the s(6) and s(10) subcontainer cuts and per-cell charge floors could take the
20,155,518 n17 occupancy orbits down to at most $10^4$. That many geometric leaves is
affordable at an estimated one to two CPU-hours each.
Session 167 ran it as a one-sided pilot before building the exact six-sweep instrument.
A sampled floor is the charge of a legal pose, so it can only overstate what a floor
test excludes.

## Outcome

R068’s charge collapses at the cap.
Its sites are spaced for cores of $0.9999993\,A_{\rm R068}$, and at $A_U$ the smaller
square slips between them: the corner floor falls to 6% of its R068 value.
No pattern is excluded, and the 7,703,312 orbits the cuts leave all survive.
The
[independent review](../../../../../docs/project/reviews/review-2026-10-02-n17-charge-floor-pilot.md)
reproduced every floor by direct rule evaluation and recounted the census by two
methods. It confirmed that the open-parent charge is a valid packing charge at $U$, and
that the one-sided inequality runs in the direction the no-go needs.

It also proved a ceiling for H-262’s registered class: one D4-symmetric linear per-cell
floor vector leaves at least 30,966 orbits, whatever the charge.
H-262 therefore cannot be confirmed, and the exact instrument is not worth building.
The ceiling is narrower than lane B first stated: asymmetric floors escape it, and a
free search over asymmetric floor vectors reached 6 orbits.
Whether any charge realises such floors is the next question, not a settled one.

## Runs

`run-001` is the coordinator’s replay from a clean worktree at the engine commit.
Lane B’s own run, from the session tree before commit with the same tool bytes, is
retained beside the other pilot receipts in
[X048-session-167-pilots](../../../explorations/X048-session-167-pilots/README.md).
The reviewer’s scripts and logs are under
[`audit/`](../results/exp-243-n17-charge-floor-pilot/audit/).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
