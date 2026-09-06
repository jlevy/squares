---
title: exp-070 — resume H-064's exact-depth n = 11 bracket at side 3.82
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-070
  series: series-000
  title: Resume the retained 3.82 exact-depth fractional packing state for BC-232
  date: '2026-09-05'
  hypotheses: [H-064]
  tier: exploratory
  subject:
    label: >-
      the exact ceiling-family lower endpoint and row-converged covering upper endpoint
      at n = 11, side 191/50, B = 9977/10000, on the retained 181-direction net
    engine: devtools.run_fractional_cutting at launch base 04e6a2ce
    engine_commit: 04e6a2ce8ed20640598f2cd687c1e1dfd3141e92
    assurance: numerically-checked
    method: numerical-f64
    precision: {binary_bits: 64, rounding: nearest ties-to-even for LP work; exact rationals for frozen family and reported lower endpoint}
    tolerance: as declared by devtools.run_fractional_cutting; no float tolerance decides a certificate
    host_system: macOS arm64, one numerical thread, Python 3.14.7
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      retained state bc-200-state-191-50.json with SHA-256
      8df0b9aa530149b44367842a2e6389949b27189df038d68e9d1afa8fd87df8c6
    candidate: >-
      one 105-minute leg with two row rounds per iteration, preserving maximum exact
      best_scaled_total and minimum row-converged rows_objective under distinct labels
    runs_per_condition: 1
    interleaved: false
    operator: Codex /root/fractional_t2_manager at max reasoning, BC-232, think-gmdy
    commit: 04e6a2ce8ed20640598f2cd687c1e1dfd3141e92
    dirty: false
    entry_point: packing/devtools/run_fractional_cutting.py
    command: >-
      cd packing && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
      VECLIB_MAXIMUM_THREADS=1 uv run --frozen --all-extras --group dev python -m
      devtools.run_fractional_cutting --n 11 --side 191/50 --shrink 9977/10000
      --angle-limit 207107/500000 --steps 180 --minutes 105 --iterations 40 --cap 150
      --support-cap 96 --rows-rounds 2 --rows-per-direction 3 --warm
      campaign/series/series-000-smoke-and-calibration/results/bc-200-state-191-50.json
      --log campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01.log
      --state campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-state.json
      --json campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-summary.json
      --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-family.json
    budget: >-
      105 one-core process minutes in this leg; no leg 2 before the T+2 landing and no
      25-percent width decision before the full four-CPU-hour evidence budget
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-summary.json
  lease:
    expires: '2026-09-06T07:22:10Z'
    host: spud10.local
  results: []
  verdict:
    decision: in-progress
    primary_criterion: >-
      a zero-exit fresh checkpoint with exact lower endpoint, row-converged computational
      upper endpoint where available, four output hashes, and honestly recorded cost
    reason: >-
      The round is preregistered and claimed; no numerical process starts until the T+0
      dispatch commit and explicit coordinator GO.
---
# exp-070 — BC-232 Retained-State Resume

This round spends the first 105 minutes of BC-232’s retained four-CPU-hour evidence
budget. Its width remains provisional at T+2, and leg 2 is forbidden before the
coordinator lands the checkpoint.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
