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
  effort:
    timebox: 105m one-core process deadline, with the current iteration allowed to finish
    wall_seconds: 6560.285289
    stopped_by: timebox
  results:
  - shape: determination
    role: outcome
    question: >-
      Did the retained exact-depth family reach total weight at least eleven during
      this leg and thereby close the tested one-body formulation from below?
    outcome: criterion_missed
    checked_by: >-
      verify_ceiling accepted depth at most one for the frozen 768-placement family but
      returned proved=false solely because exact total 21342289572/2055263195 is below
      eleven.
  - shape: determination
    role: mechanism
    question: >-
      Did the leg improve the exact lower endpoint while preserving a row-converged
      computational upper endpoint?
    outcome: criterion_met
    checked_by: >-
      Iteration 10 raised the verified exact lower endpoint to
      21342289572/2055263195 ≈ 10.384212408377215, while iteration 0 retained the
      only row-converged computational upper endpoint, 11.055616942909783. Later row solves reached
      their two-round or deadline limits and are not upper endpoints.
  verdict:
    decision: abandoned
    primary_criterion: >-
      an exact depth-scaled total of at least eleven at 191/50, which closes the
      formulation from below, or a row-converged and rationalized covering certificate
      below eleven, which yields a candidate lower-bound route; intermediate bracket
      improvement remains unresolved until the four-CPU-hour gate
    reason: >-
      The one authorized leg improved the exact lower endpoint but expired before
      reaching eleven; the bracket is still open and the frozen four-CPU-hour routing
      rule forbids a continuation decision from this 105-minute partial budget alone.
    commit: c55726e1e885227f63110131c0a914665175ff89
    budget_spent: >-
      The 105-minute one-core deadline plus its terminal in-flight tail: 6560.285289
      seconds recorded by the runner, with no leg 2; final CPU is unavailable and the
      last live sample, 104:50.95, is retained only as a lower bound.
    best_reached: >-
      21342289572/2055263195 <= nu*(3.82) <= tau*(3.82) <=
      11.055616942909783, with the lower endpoint exact at
      21342289572/2055263195 and the upper endpoint computational and row-converged.
    reopen_when: >-
      After the T+2 landing, spend the remaining 135 one-core process minutes of
      BC-232's frozen four-CPU-hour evidence budget; make the 25-percent routing
      decision only after that complete budget.
    resume_from: >-
      packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-state.json,
      using the exact unused leg-02 command preserved in bc-232-disposition.md
---
# exp-070 — BC-232 Retained-State Resume

This round spent the first 105-minute deadline of BC-232’s retained four-CPU-hour
evidence budget, plus the runner’s terminal in-flight tail.
It raised the exact lower endpoint from approximately `9.907905595` to
`21342289572/2055263195 ≈ 10.384212408377215`; the only row-converged computational
upper endpoint remains `11.055616942909783`. The resulting provisional width is about
`0.671404535`, roughly 41.5 percent narrower than the pre-resume bracket.

That percentage is a checkpoint, not the routing decision.
The frozen rule evaluates the full four-CPU-hour evidence budget, so the remaining 135
one-core minutes may begin only after this T+2 landing.
The retained state is resumable.
Its pre-add serialization does not include iteration 13’s terminal 150 selected orbits
or summary stop string; the terminal summary and frozen family carry the authoritative
last-iteration and stop receipt.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
