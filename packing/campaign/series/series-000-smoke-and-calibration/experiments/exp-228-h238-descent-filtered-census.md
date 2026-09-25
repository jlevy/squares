---
title: exp-228 — a descent-filtered census of n11 minima near Trump and Stromquist
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-228
  series: series-000
  title: A descent-filtered census of n11 minima near Trump and Stromquist
  date: '2026-09-23'
  hypotheses: [H-238]
  tier: confirmatory
  subject:
    label: >-
      1,000 jolted starts about Trump's and Stromquist's packings, quenched and passed
      through a descent filter over all 33 pose coordinates and the side; every
      rejection carries an exact rational packing verified by sqpack.verify below the
      endpoint's side
    engine: >-
      devtools.run_basin_hopping census with sqpack.research.descent_filter (frozen
      4b7c57d; driver 9260d0f, amended to 10635d6 by a resume-only flag after an
      external SIGTERM), stock sqpack.research.quench and sqpack.verify
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 53
      rounding: nearest-even
    tolerance: >-
      A rejection needs an exact rational packing verified at least 1e-8 below the
      endpoint side; dedup side 1e-9; orientation classes merged within 1e-3 rad
    host_system: macOS, Claude Session 156 lane; project Python 3.14.7; four workers under host load 100 to 230
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Ten controls gate the census: Trump's and Stromquist's packings (the latter in
      exact Q(sqrt 2) coordinates) are stable; Trump scaled apart with one square turned,
      Trump with square 10 turned, and all six X-046 probe-C stalls are rejected, each
      stall descending to within 1.5e-11 of U
    candidate: >-
      The census. Kill H-238 with one descent-stable minimum having at least three
      orientation classes and exact-witness side below 3.885618; otherwise the census
      is support only.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 156, Opus extra-high lane
    entry_point: packing/devtools/run_basin_hopping.py
    command: >-
      cd packing && uv run --frozen --all-extras --group dev python -m
      devtools.run_basin_hopping census --starts 1000 --bases trump,stromquist --scales
      0.02,0.05,0.1,0.2,0.3 --seed 238 --quench-seconds 8 --filter-seconds 60
      --control-seconds 120 --workers 4 --wall-seconds 6600 --stalls
      <X-046 probe-C stalls, retained as exp-228-x046-probe-c-stalls.jsonl.gz> --out
      <dir>, resumed after 604 starts with --resume-from on the interrupted records
    budget: About three hours; the census took 41 minutes for 604 starts and 21 for the resumed 396.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/
  effort:
    timebox: 6,600 s declared wall
    wall_seconds: 3720
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: >-
      Does any descent-stable census minimum with at least three orientation classes lie
      below 3.885618?
    outcome: criterion_met
    checked_by: >-
      None of 1,000 terminals: the quench stopped at 85 three-or-more-class endpoints
      below 3.885618 and the filter rejected every one with an exact descending packing;
      655 endpoints rejected in all, 345 survivors, 0 filter budgets exhausted; the only
      descent-stable minimum below the threshold is Trump's two-class packing (363 hits)
  - shape: determination
    role: mechanism
    question: Which descent-stable minima lie within U + 0.02?
    outcome: criterion_met
    checked_by: >-
      Stromquist's 3.8856180831 (two classes plus freely turning squares), a two-class
      0 and 41.56 degree minimum at 3.8867460286, and a genuine three-class minimum with
      no free squares at 3.8943218738 (38 hits); 34 rows over 22 sides in the minima
      record
  verdict:
    decision: accepted
    primary_criterion: >-
      No descent-stable minimum with at least three classes below 3.885618 among the
      census terminals.
    reason: >-
      The census found none, and every apparent candidate was refuted by an exact
      descending packing; this confirms H-238 at its declared census scope only, since
      descent-stability is empirical and starts are jolts of at most 0.3 about two known
      packings.
---
# Exp-228: A Descent-Filtered Census Near Trump and Stromquist

[H-238](../../../hypotheses/H-238-n11-no-third-class-minimum-below-stromquist.md) is the
cheap falsifier for the settlement ladder: a genuine three-orientation local minimum
close to $U$ would make the three-orientation rung mandatory.
The census found none.
Its quench stopped 85 times at a three-or-more-class point below Stromquist’s value, and
the descent filter moved every one of them down with an exact, verified packing, which
is why the filter had to exist before a census could be read.

Two minima within $U+0.02$ are new to the record and set how sharp any profile theorem
must be: a two-orientation packing at $0°$ and $41.56°$ with side $3.8867460$, and a
genuine three-orientation packing at $3.8943219$. The census cannot be replayed bit for
bit, because the quench’s limit is wall-clock time and the host was heavily loaded; only
94 of 1,000 quenches converged, so the filter did most of the descent.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
