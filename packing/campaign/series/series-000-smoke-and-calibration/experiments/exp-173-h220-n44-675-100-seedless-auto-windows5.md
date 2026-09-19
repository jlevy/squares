---
title: exp-173 — seedless auto plus windows 5 at n=44 675/100
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-173
  series: series-000
  title: Seedless auto plus windows 5 at n=44 675/100
  date: '2026-09-19'
  hypotheses: [H-220]
  tier: exploratory
  subject:
    label: >-
      Restricted covering optima at n=44 on the 181-direction net at B = 9977/10000,
      at side 675/100, on auto grids plus windows 5 with no certificate seed
    engine: >-
      sqpack.fractional.colgen through devtools.run_fractional_colgen; retain by
      declare_least_cell_mass then both routes of decide_certificate
    assurance: verified
    method: exact-algebraic
    host_system: Cursor cloud agent; project Python 3.14; no packing-campaign runner
  instance: {axis: n, point: 44, role: target}
  method:
    control: >-
      Nagamochi-only floor at n=44 (1 + sqrt(33) ≈ 6.74456264654) and no
      first-party covering rows recorded at this n. H-218 n=20 four-grid probes
      do not apply.
    candidate: >-
      Stock colgen with auto grids and windows 5 at 675/100, no --seed-certificate,
      then freeze-then-decide if the row loop converges below 44
    runs_per_condition: 1
    interleaved: false
    operator: Cursor session-141
    entry_point: packing/devtools/run_fractional_colgen.py
    command: >-
      cd packing && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run
      --frozen --all-extras --group dev python -m devtools.run_fractional_colgen
      --n 44 --side 675/100 --shrink 9977/10000 --direction-steps 181
      --grid-counts auto --seed-windows 5
      --support-cap 32 --column-rounds 1 --max-rounds 60
      --deadline-seconds 1200 --scale 4000000
      --freeze results/agenda-039/n44-675-100-auto-windows5-certificate.json
      --json results/agenda-039/n44-675-100-auto-windows5-run.json
    budget: >-
      Session-141 research wall to 2026-09-19T15:26:00Z. Eighth H-220 probe only.
      Do not replay n=32 29/5, n=31 57/10, n=30 559/100, n=26 513/100, n=27 525/100,
      n=29 548/100, or n=45 684/100 auto plus windows 5.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-039/
  results:
  - shape: determination
    role: outcome
    question: >-
      Does a seedless auto plus windows-5 freeze at 675/100 have mass strictly below 44
      and print RETAINABLE?
    outcome: criterion_missed
    checked_by: >-
      1200 s deadline stopped the row loop after 28 LP rounds at 41.236782 with
      546 placements still violated. No freeze. Did not cross 44.
  verdict:
    decision: unresolved
    primary_criterion: >-
      Confirm H-220 only when decide_certificate prints RETAINABLE on a freeze with
      mass < 44 at a side strictly above the Nagamochi floor
    reason: >-
      Seedless auto plus windows 5 at 675/100 finished unconverged below 44.
      Remaining rows raise. That site set is not a retain. The eight queued
      Nagamochi sides are measured. H-220 stays unconfirmed.
    budget_spent: Covering 1300.3 s on one core.
    best_reached: restricted optimum 41.236782 unconverged, no freeze
    resume_from: >-
      Do not replay n=44 675/100 auto plus windows 5. The next named set is
      exp-174 at n=19 481/100 T-020 four-grid plus windows 7. Remaining rows
      raise this set.
  effort:
    timebox: Session-141 n=44 675/100 seedless auto plus windows 5
    wall_seconds: 1300
    stopped_by: timebox
---
# Exp-173: H-220 Eighth Nagamochi Probe

This is the eighth scientific round of
[H-220](../../../hypotheses/H-220-seedless-colgen-raises-nagamochi-floor.md), after
[exp-172](exp-172-h220-n45-684-100-seedless-auto-windows5.md) stopped at `42.137360`
unconverged below 45. Remaining rows raise that set.

Auto resolved to `(50, 67, 83)`. The 1200 s run stopped at `41.236782`
unconverged below 44 after 28 LP rounds. No freeze. T-030 was not offered. The
eight queued Nagamochi sides are measured. The follow-up is exp-174 at n=19
`481/100` four-grid plus windows 7.

Confirm only on `RETAINABLE`. There is no n=44 case package.

exp-161 is not this round. Do not `--search`. Do not mutate T-025 or T-026
`verify_claim.py`. Do not close `think-qqzs`, `think-g3j7`, `think-gyzw`, or
`think-jwb1`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
