---
title: exp-117 — full near-axis ten-point coverage on the fixed grid
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-117
  series: series-000
  title: Test the complete near-axis ten-point clause with unchanged source labels
  date: '2026-09-07'
  hypotheses: [H-106]
  tier: confirmatory
  subject:
    label: Fixed q1939/500 P10 formulas on both complete closed near-axis angle slabs
    engine: Fixed-grid quartic producer and source-distinct rectangle/Bernstein reader
    engine_commit: cf0f4d4c5b4c540225d53f4724496ba33442607c
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Python3.14.7; GNU coreutils timeout9.9 for the external process guard
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Original zero-angle source grid and independent corner replay passed;
      continuous producer34source-free controls and independent reader16controls
      passed separate mathematical reviews. No target geometry was evaluated.
    candidate: >-
      Side1939/500; unchanged four P10 seeds and K4 reflections; fixed6x3normalized
      center grid and source assignment matrix; two closed half-angle slabs
      [-110880/50803079,0] and[0,110880/50803079]; producer864inequalities at
      sign-depth0, independent reader576corner inequalities with fixed sign-depth12.
    runs_per_condition: 1
    interleaved: false
    operator: Codex coordinator, max mathematical reasoning, Session090 BC255
    commit: cf0f4d4c5b4c540225d53f4724496ba33442607c
    dirty: false
    entry_point: packing/devtools/angle_near_axis_control.py
    command: >-
      /usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 10s
      env PYTHONPATH=src OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
      /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.angle_near_axis_control --target-near-axis
      --output /Users/levy/wrk/github/squares/packing/campaign/series/series-000-smoke-and-calibration/results/exp-117-h-106-continuous-near-axis/packet.json
      --log /Users/levy/wrk/github/squares/packing/campaign/series/series-000-smoke-and-calibration/results/exp-117-h-106-continuous-near-axis/worker.log
    budget: >-
      One producer with a ten-second external process kill and its existing
      ten-second child cap. Only complete positive output with actual exit0 earns
      one independent file replay, also externally capped at ten seconds. No
      grid/label/point/side/slab changes, subdivision increase, retry or target
      repair. Retain external exits and wall/CPU independently of packet claims.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-117-h-106-continuous-near-axis/packet.json
  effort:
    timebox: One ten-second producer and one independent ten-second reader, each invoked once
    wall_seconds: 0.37
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: Does the unchanged ten-set cover every contained square in the full closed near-axis neighborhood?
    outcome: criterion_met
    checked_by: >-
      Producer completed all864triangle inequalities with actual exit0. A separate
      exact rectangle reader returned actual exit0, decisionproved,36rectangles,
      144corners and576inequalities with no unresolved inventory. Both signs and
      all boundaries are covered. No conclusion about H036 or a packing bound.
  verdict:
    decision: accepted
    primary_criterion: Complete independently verified near-axis P10 coverage on both closed angle signs and all contained centers.
    reason: Complete fixed-side near-axis ten-point coverage passed the source-distinct exact reader within both frozen caps.
    commit: 676f775a
---
# exp-117 — Continuous Near-Axis Coverage

This tests [H-106](../../../hypotheses/H-106-continuous-near-axis-ten-point-cover.md),
one auxiliary clause for H-036, using the unchanged point formulas and complete angle
neighborhood. H-106 is accepted at precisely that scope.
The sole producer and independent reader completed from a clean detached `cf0f4d4c`
checkout, after the protocol was committed and the record checks passed.
Both commands run from that checkout’s `packing/` directory, with `PYTHONPATH=src`
selecting its isolated source.
The existing project interpreter supplies dependencies; it does not select the
integration checkout’s source.

The producer ran between the observed clocks `02:48:02Z` and `02:48:22Z`, returned
actual exit zero, and checked all 864 inequalities without unresolved entries.
The independent reader ran once between `02:49:59Z` and `02:50:00Z`, returned actual
exit zero and `decision=proved`, and checked all 36 slab-rectangles, 144 corners and 576
inequalities. Both closed angle signs, every center-grid seam and the endpoints are
covered. The reader retained the exact side and slab binding and reported H-036
unresolved.

Outer process costs were 0.24 seconds wall and 0.22 CPU for the producer, then 0.13
seconds wall and 0.12 CPU for the reader: 0.37 wall and 0.34 CPU seconds in total.
The producer worker reported 0.164891 wall and 0.160650 CPU seconds; the reader reported
0.062017 wall and 0.061722 CPU seconds.
These are process costs, not operator attention.
The reader’s assigned operator interval was `02:49:20Z`–`02:50:19Z`, 59 seconds.
Neither process was repeated or approached its ten-second cap.

The result directory retains the packet, worker log, outer producer log and stdout, and
the source-distinct `replay.json` and `replay.log`. The prospective protocol below is
unchanged.

The
[independent review](../results/agenda-026/bc-255-near-axis-reader-independent-review.md)
accepts the separate rectangle calculation and states its arithmetic and process limits.
The positive rational denominator, complete affine center map and closed grid prove
coverage for each parameter.
The bound `T=110880/50803079` is an outward enlargement of `tan(pi/1440)`, as proved in
the registered hypothesis’s design reference.

The producer tests 864 signed triangle-vertex polynomials.
A complete positive packet and actual exit zero permit exactly one independent reader
invocation:

```bash
/usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 10s env PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.check_angle_near_axis_control ABSOLUTE_PACKET_PATH --target-control
```

Retain producer stdout as `stdout.log`, external stderr/timing as `run.log`, and the
separate reader stdout/stderr as `replay.json` and `replay.log` in the declared result
directory. All paths must be absent before the first invocation.
The producer’s atomic publication does not refuse overwrite; the coordinator checks
freshness before launch.
No reader is invoked on an incomplete, negative-status, missing or externally failed
producer. Its non-invocation is recorded explicitly, not represented by a fake receipt.

Accept only after the independent reader returns actual exit zero, `decision=proved`, 36
slab-rectangles, 144 corners, all 576 inequalities and no unresolved inventory.
An externally killed process cannot accept a packet it happened to write before death.
A failed fixed assignment or bounded Bernstein test is unresolved, not a geometric
counterexample. This instrument has no rejection path: an independently checked avoider
in the actual angle interval would need a separate experiment.
The outward sliver does not broaden H-106’s rejection criterion.

Success proves only the near-axis ten-point clause.
Near-45-degree localization, the three forced points and both twelve-point clauses
remain separate; no packing bound or H-036 acceptance is inferred.
Exp-114’s exact-angle result and the earlier source controls remain unchanged, and no
target outcome changes this protocol’s caps.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
