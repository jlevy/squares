---
title: exp-162 — stock colgen on the X-038 first-wave floors
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-162
  series: series-000
  title: Stock colgen on the X-038 first-wave floors
  date: '2026-09-19'
  hypotheses: [H-218]
  tier: exploratory
  subject:
    label: >-
      Restricted covering optima at n in {12, 17, 19, 20} on the 181-direction net at
      B = 9977/10000, at sides strictly above the current verified floors, on named
      site sets built by run_fractional_colgen
    engine: >-
      sqpack.fractional.colgen through devtools.run_fractional_colgen; retain by
      declare_least_cell_mass then both routes of decide_certificate
    assurance: verified
    method: exact-algebraic
    host_system: Cursor cloud agent; project Python 3.14; no packing-campaign runner
  instance: {axis: n, point: 20, role: target}
  method:
    control: >-
      Standing verified floors T-017 99/25, T-019 459/100, T-020 24/5, T-021 97/20,
      and the covering-values rows already recorded for those n. H-062's wall at
      973/200 binds only the auto-grid and 97/20-seed constructions it named.
    candidate: >-
      New named site sets on the ranked sides in X-038: certificate seed plus a
      four-grid and/or --seed-windows, then freeze-then-decide if the row loop
      converges below n
    runs_per_condition: 1
    interleaved: false
    operator: Cursor session-140
    entry_point: packing/devtools/run_fractional_colgen.py
    command: >-
      cd packing && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run
      --frozen --all-extras --group dev python -m devtools.run_fractional_colgen
      --n N --side SIDE --shrink 9977/10000 --direction-steps 181 --grid-counts COUNTS
      --seed-windows W --seed-certificate CERT --seed-map scale --support-cap 32
      --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 --scale 4000000
      --freeze results/agenda-038/...-certificate.json
      --json results/agenda-038/...-run.json
    budget: >-
      Session-140 research wall to 2026-09-19T06:42:00Z. One probe family per ranked
      n. No second attempt at a (n, side, site_set) already on covering-values.yaml.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/
  effort:
    timebox: 238m
    wall_seconds: 14280
    stopped_by: timebox
  results:
  - shape: determination
    role: outcome
    question: >-
      Does any first-wave freeze have mass strictly below n at a side above the current
      verified floor and print RETAINABLE?
    outcome: no_progress
    checked_by: >-
      Session-140 first-wave and leftover probes at n in {12, 17, 19, 20} produced
      no freeze with mass below n. T-028 retained at n=18, which is off the H-218
      sweep. decide_certificate was not offered an H-218 freeze.
  verdict:
    decision: abandoned
    primary_criterion: >-
      Confirm H-218 only when decide_certificate prints RETAINABLE on a freeze with
      mass < n at a side above the current floor for some n in {12, 17, 19, 20}
    reason: >-
      The Session-140 research wall expired with no RETAINABLE freeze on the H-218
      sweep. Closest masses were leftover n=20 971/200 at 19.910044 unconverged
      and leftover n=12 3969/1000 at 12.091168 after crossing 12. T-028 at n=18
      does not confirm H-218.
    budget_spent: >-
      Session-140 research wall 238 minutes on one core. Leftover n=18 and the
      second-wave Nagamochi queue did not start.
    best_reached: >-
      T-028 s(18) >= 187/40 off-sweep. H-218 sweep closest: leftover n=20
      971/200 at 19.910044 unconverged below 20; leftover n=12 3969/1000 at
      12.091168 after crossing 12.
    reopen_when: >-
      A new named site set at n in {12, 17, 19, 20} whose restricted optimum is
      still below n, or leftover n=18 1871/400.
    resume_from: >-
      Leftover n=18 1871/400 T-028 auto plus windows 5, then second-wave
      Nagamochi n=32 29/5. Do not replay leftover n=12 3969/1000 four-grid plus
      windows 7, leftover n=20 971/200, leftover n=17 461/100, or leftover n=19
      241/50.
---
# Exp-162: First-Wave Stock Colgen

This is the first scientific round of
[H-218](../../../hypotheses/H-218-existing-colgen-raises-a-small-n-floor.md).
[X-038](../../../explorations/X-038-n100-lower-bound-survey.md) ranks the sides.
[Session 140](../../../agent-sessions/session-140-lb-survey.md) owns the clock.

The accept rule is the gate, not the float LP. A restricted optimum above `n` is a
site-set negative and is recorded on `covering-values.yaml`. T-028 is landed only on
`RETAINABLE`.

exp-161 is not this round. Do not `--search`. Do not mutate T-025 or T-026
`verify_claim.py`. Do not close `think-qqzs`, `think-g3j7`, `think-gyzw`, or
`think-jwb1`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
