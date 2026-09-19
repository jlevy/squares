---
title: exp-166 — seedless auto plus windows 5 at n=32 29/5
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-166
  series: series-000
  title: Seedless auto plus windows 5 at n=32 29/5
  date: '2026-09-19'
  hypotheses: [H-220]
  tier: exploratory
  subject:
    label: >-
      Restricted covering optima at n=32 on the 181-direction net at B = 9977/10000,
      at side 29/5, on auto grids plus windows 5 with no certificate seed
    engine: >-
      sqpack.fractional.colgen through devtools.run_fractional_colgen; retain by
      declare_least_cell_mass then both routes of decide_certificate
    assurance: verified
    method: exact-algebraic
    host_system: Cursor cloud agent; project Python 3.14; no packing-campaign runner
  instance: {axis: n, point: 32, role: target}
  method:
    control: >-
      Nagamochi-only floor at n=32 (1 + sqrt(23) ≈ 5.79583152331) and no
      first-party covering rows recorded at this n. H-218 n=20 four-grid probes
      do not apply.
    candidate: >-
      Stock colgen with auto grids and windows 5 at 29/5, no --seed-certificate,
      then freeze-then-decide if the row loop converges below 32
    runs_per_condition: 1
    interleaved: false
    operator: Cursor session-141
    entry_point: packing/devtools/run_fractional_colgen.py
    command: >-
      cd packing && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run
      --frozen --all-extras --group dev python -m devtools.run_fractional_colgen
      --n 32 --side 29/5 --shrink 9977/10000 --direction-steps 181
      --grid-counts auto --seed-windows 5
      --support-cap 32 --column-rounds 1 --max-rounds 60
      --deadline-seconds 1200 --scale 4000000
      --freeze results/agenda-039/n32-29-5-auto-windows5-certificate.json
      --json results/agenda-039/n32-29-5-auto-windows5-run.json
    budget: >-
      Session-141 research wall to 2026-09-19T15:26:00Z. First H-220 probe only.
      No second attempt at a (n, side, site_set) already on covering-values.yaml.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-039/
  results:
  - shape: determination
    role: outcome
    question: >-
      Does a seedless auto plus windows-5 freeze at 29/5 have mass strictly below 32
      and print RETAINABLE?
    outcome: criterion_missed
    checked_by: >-
      1200 s deadline stopped the row loop after 35 LP rounds at 29.803318 with
      546 placements still violated. No freeze. Did not cross 32.
  verdict:
    decision: unresolved
    primary_criterion: >-
      Confirm H-220 only when decide_certificate prints RETAINABLE on a freeze with
      mass < 32 at a side strictly above the Nagamochi floor
    reason: >-
      Seedless auto plus windows 5 at 29/5 finished unconverged below 32.
      Remaining rows raise. That site set is not a retain. H-220 stays unconfirmed.
    budget_spent: Covering 1206.0 s on one core.
    best_reached: restricted optimum 29.803318 unconverged, no freeze
    resume_from: >-
      Do not replay n=32 29/5 auto plus windows 5. The next named set is exp-167
      at n=31 57/10 seedless auto plus windows 5. Remaining rows raise this set.
  effort:
    timebox: Session-141 n=32 29/5 seedless auto plus windows 5
    wall_seconds: 1206
    stopped_by: timebox
---
# Exp-166: H-220 First Nagamochi Probe

This is the first scientific round of
[H-220](../../../hypotheses/H-220-seedless-colgen-raises-nagamochi-floor.md).
[X-039](../../../explorations/X-039-n100-re-rank-after-session-140.md) ranks the side.
[Session 141](../../../agent-sessions/session-141-n100-research.md) owns the clock.

Auto resolved to `(42, 56, 70)`. The 1200 s run stopped at `29.803318`
unconverged below 32 after 35 LP rounds. No freeze. T-030 was not offered. The
follow-up is exp-167 at n=31 `57/10`.

Confirm only on `RETAINABLE`. There is no n=32 case package.

exp-161 is not this round. Do not `--search`. Do not mutate T-025 or T-026
`verify_claim.py`. Do not close `think-qqzs`, `think-g3j7`, `think-gyzw`, or
`think-jwb1`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
