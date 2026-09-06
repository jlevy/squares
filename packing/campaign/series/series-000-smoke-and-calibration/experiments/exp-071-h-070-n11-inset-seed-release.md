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
    selftest_passed: false
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
  lease:
    expires: '2026-09-06T07:22:10Z'
    host: spud10.local
  results: []
  verdict:
    decision: in-progress
    primary_criterion: >-
      strict exact-mass comparison after equal stopping class and completed-round count,
      with every ineligible, time-limited, and guard-refused run retained
    reason: >-
      The paired round is preregistered and claimed; its strict-JSON control must pass
      after the T+0 dispatch commit before the first screen starts.
---
# exp-071 — Margin-Biased Seed With Support Released

The screens choose a proposal; only the matched unrestricted arms test H-070. If the
statuses cannot be matched by T+2, the honest result is time-limited or unresolved, not
a rescued comparison.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
