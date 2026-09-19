---
title: exp-163 — T-028-seeded colgen at n=18 1871/400
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-163
  series: series-000
  title: T-028-seeded colgen at n=18 1871/400
  date: '2026-09-19'
  hypotheses: [H-219]
  tier: exploratory
  subject:
    label: >-
      Restricted covering optima at n=18 on the 181-direction net at B = 9977/10000,
      at sides in (187/40, 117/25), on named site sets seeded from T-028
    engine: >-
      sqpack.fractional.colgen through devtools.run_fractional_colgen; retain by
      declare_least_cell_mass then both routes of decide_certificate
    assurance: verified
    method: exact-algebraic
    host_system: Cursor cloud agent; project Python 3.14; no packing-campaign runner
  instance: {axis: n, point: 18, role: target}
  method:
    control: >-
      Standing verified floor T-028 187/40 and the covering-values rows already
      recorded at n=18, including the 117/25 plateau at 18.000000
    candidate: >-
      T-028 certificate seed plus auto grids and windows 5 at 1871/400, then
      freeze-then-decide if the row loop converges below 18
    runs_per_condition: 1
    interleaved: false
    operator: Cursor session-141
    entry_point: packing/devtools/run_fractional_colgen.py
    command: >-
      cd packing && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run
      --frozen --all-extras --group dev python -m devtools.run_fractional_colgen
      --n 18 --side 1871/400 --shrink 9977/10000 --direction-steps 181
      --grid-counts auto --seed-windows 5
      --seed-certificate cases/n18_fractional_certificate/certificate.json
      --seed-map scale --support-cap 32 --column-rounds 1 --max-rounds 60
      --deadline-seconds 1200 --scale 4000000
      --freeze results/agenda-039/n18-1871-400-t028-auto-windows5-certificate.json
      --json results/agenda-039/n18-1871-400-t028-auto-windows5-run.json
    budget: >-
      Session-141 research wall to 2026-09-19T15:26:00Z. First probe family only.
      No second attempt at a (n, side, site_set) already on covering-values.yaml.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-039/
  results:
  - shape: determination
    role: outcome
    question: >-
      Does a T-028-seeded freeze at a side in (187/40, 117/25) have mass strictly
      below 18 and print RETAINABLE?
    outcome: criterion_met
    checked_by: >-
      decide_certificate printed RETAINABLE on the leftover 1871/400 freeze:
      mass 17889361/1000000 = 17.889361, least cell mass 250001/250000, sha256
      dd06c0e39639f06af475459a2a63f9fc8d5836b0b83ea3b6c3a4de8f212892d4. T-029.
  verdict:
    decision: accepted
    primary_criterion: >-
      Confirm H-219 only when decide_certificate prints RETAINABLE on a freeze with
      mass < 18 at a side in (187/40, 117/25)
    reason: >-
      Leftover n=18 1871/400 T-028-seeded auto plus windows 5 converged at
      17.889237 and freeze-then-decide retained T-029. Confirms H-219. Does not
      confirm H-218.
    budget_spent: >-
      Covering 650.3 s, declare 19 s, decide 33 s on one core.
    best_reached: T-029 s(18) >= 1871/400 = 4.6775 at V4/C4/S3
  effort:
    timebox: Session-141 first probe family
    wall_seconds: 702
    stopped_by: criterion
---
# Exp-163: Next Rung Above T-028

This is the first scientific round of
[H-219](../../../hypotheses/H-219-t028-seeded-colgen-raises-s18.md).
[X-039](../../../explorations/X-039-n100-re-rank-after-session-140.md) ranks the side.
[Session 141](../../../agent-sessions/session-141-n100-research.md) owns the clock.

The accept rule is the gate, not the float LP. A restricted optimum above 18 is a
site-set negative and is recorded on `covering-values.yaml`. The next T-id is landed
only on `RETAINABLE`. That retain does not confirm H-218.

exp-161 is not this round. Do not `--search`. Do not mutate T-025 or T-026
`verify_claim.py`. Do not close `think-qqzs`, `think-g3j7`, `think-gyzw`, or
`think-jwb1`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
