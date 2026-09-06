---
title: exp-071 — test H-070's inset seed after unrestricted support release
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-071
  series: series-000
  title: Screen three n = 11 margins, then compare released seed and unseeded control
  date: '2026-09-05'
  hypotheses: [H-070]
  tier: exploratory
  subject:
    label: >-
      exact rational total mass from matched unrestricted n = 11 fractional
      column-generation arms at side 191/50 after a three-inset seed screen
    engine: devtools.run_fractional_colgen at launch base 04e6a2ce
    engine_commit: 04e6a2ce8ed20640598f2cd687c1e1dfd3141e92
    assurance: numerically-checked
    method: numerical-f64
    precision: {binary_bits: 64, rounding: nearest ties-to-even for LP work; rationalisation scale 4000000 for candidate weights}
    tolerance: no float tolerance decides the paired comparison; exact candidate total_mass does
    host_system: macOS arm64, one numerical thread per process, Python 3.14.7
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      an unseeded inset-1/2 arm with the same grids, eight column rounds, 2520-second
      deadline, thread pins, output contract, stopping class, and completed-round count
    candidate: >-
      the minimum exact-mass eligible candidate from inset screens 1/2,
      2962983/4505800, and 15513/20000, mapped by centre into a matched unrestricted arm
    runs_per_condition: 1
    interleaved: true
    operator: Codex /root/fractional_t2_manager at max reasoning, BC-233, think-jbat
    commit: 04e6a2ce8ed20640598f2cd687c1e1dfd3141e92
    dirty: false
    entry_point: packing/devtools/run_fractional_colgen.py
    command: >-
      Run agenda-025's three exact 540-second screen commands sequentially; if at least
      one is eligible, run its centre-mapped released arm and an unseeded control at
      inset 1/2 with --column-rounds 8 and --deadline-seconds 2520 using fresh stems
    budget: >-
      30 active portfolio minutes for screens plus at most 42 one-core process minutes
      per matched follow-on arm; minute 90 forbids a new long process
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-233-disposition.md
  effort:
    timebox: >-
      30 active portfolio minutes for the three screens plus at most 42 one-core
      process minutes for each matched arm
    wall_seconds: 491.483
    pair_tests: 1
    stopped_by: criterion
  results:
  - shape: paired
    metric: exact rational total mass after eight unrestricted column rounds
    role: outcome
    control_median: 11.142893
    candidate_median: 11.142893
    change_pct: 0.0
    passes_acceptance: false
    direction: unclear
    pairs: 1
  - shape: determination
    role: outcome
    question: >-
      Does the released candidate seeded from the best eligible inset screen finish at
      strictly smaller exact mass than the matched unseeded control?
    outcome: criterion_missed
    checked_by: >-
      Both strict-JSON summaries exited zero, converged in eight rounds, and emitted
      byte-identical candidates of exact mass 11142893/1000000; the complete hashes are
      recorded in results/agenda-025/bc-233-disposition.md.
  verdict:
    decision: rejected
    primary_criterion: >-
      strict exact-mass comparison after equal stopping class and completed-round count,
      with every ineligible, time-limited, and guard-refused run retained
    reason: >-
      The released seed and matched unseeded control converged after the same eight
      rounds to byte-identical candidates of exact mass 11142893/1000000, so the seeded
      arm missed the preregistered strict-improvement criterion.
    commit: c55726e1e885227f63110131c0a914665175ff89
---
# exp-071 — Margin-Biased Seed With Support Released

The screens chose the inset-`1/2` proposal.
The matched unrestricted arms then converged after eight rounds to byte-identical
candidates of exact mass `11142893/1000000`. H-070 is therefore rejected: the seed
neither helped nor hurt under this test.
Both candidates remain above eleven, so the round also opened no exact lower-bound
route.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
