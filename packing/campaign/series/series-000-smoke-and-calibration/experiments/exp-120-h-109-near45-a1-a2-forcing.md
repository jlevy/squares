---
title: exp-120 — canonical A1 forcing and its A2 reflection
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-120
  series: series-000
  title: Test one complete A1 clause and transfer it to A2
  date: '2026-09-07'
  hypotheses: [H-109]
  tier: confirmatory
  subject:
    label: Fixed canonical two-point avoidance at q=1939/500 throughout both closed near-45 angle signs
    engine: Exact formal-vertex producer and independent polarized-Bernstein reader, closed A1 selector
    engine_commit: 57ad0deaa0fb9f57ccec7b606171de0507422c82
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Python 3.14.7; GNU coreutils timeout 9.9
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Source-free A1/A3 selector controls preserve the separately reviewed exact
      kernels and forbid both scientific constructors. They check cross-clause
      refusals, unchanged A3 identity, exact toy reflection covariance and closed
      slab reversal. Separate reviews passed 19 producer and 22 reader tests;
      neither review evaluated scientific geometry.
    candidate: >-
      Side 1939/500, A1=(1,439/500), canonical region [1,q/2]x[0,1],
      avoidance of L=(1,1) and M=(q/2,1), and both half-angle slabs
      [-110880/50803079,0] and [0,110880/50803079] about pi/4.
      Check E,F,G and their four signed margins: 24 unsplit inequalities.
      Transfer the complete A1 implication to A2=(1939/1000,439/500) by reflection.
    runs_per_condition: 1
    interleaved: false
    operator: Codex coordinator, max mathematical reasoning, Session 090 BC-255
    commit: 57ad0deaa0fb9f57ccec7b606171de0507422c82
    dirty: false
    entry_point: packing/devtools/angle_near45_triangle_control.py
    command: >-
      /usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 10s
      env PYTHONPATH=src OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
      /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.angle_near45_triangle_control --target-a1
      --output /Users/levy/wrk/github/squares/packing/campaign/series/series-000-smoke-and-calibration/results/exp-120-h-109-near45-a1-a2-forcing/packet.json
      --log /Users/levy/wrk/github/squares/packing/campaign/series/series-000-smoke-and-calibration/results/exp-120-h-109-near45-a1-a2-forcing/worker.log
    budget: >-
      One producer with a ten-second external cap and its existing internal caps.
      Only complete positive output with actual exit zero earns one independent
      file replay with a separate ten-second external and internal cap. No A2
      invocation, retries, subdivision, point changes, side changes or angle narrowing.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-120-h-109-near45-a1-a2-forcing/packet.json
  lease:
    expires: '2026-09-07T04:10:00Z'
    host: Session 090 coordinator
  results: []
  verdict:
    decision: in-progress
    primary_criterion: Independently verified A1 forcing on both closed angle signs and a complete reflection implication for A2.
    reason: Both independent reviews passed; commit this prospective protocol and pass record checks before the sole dispatch.
---
# exp-120 — A1 and A2 from One Certificate

This prospectively tests
[H-109](../../../hypotheses/H-109-near45-canonical-a1-a2-forcing.md).
No target has run. The producer review under `think-u3yi` independently passed 19
source-free tests in 0.35 seconds wall and 0.33 CPU. The reader review under
`think-rsvp` ran 03:43:26–03:47:14 UTC and passed 22 source-free tests in 0.50 seconds
wall and 0.46 CPU. Ruff, formatting and BasedPyright were clean.
Source commit `57ad0dea` freezes both reviewed adaptations; their generic mathematical
kernels are unchanged from `bdc68784`.

The claim assumes avoidance of only L and M, a weaker antecedent than avoiding P10. A
complete certificate therefore implies the A1 clause needed for H-036, while its
reflected version implies A2. P10 need not be invariant under the local reflection.

The producer checks the same three formal triangle vertices and four membership margins
as exp-119, now for the unchanged A1 formula.
The reader independently derives its own quartics and polarized Bernstein coefficients.
The generic two-point avoidance reduction, positive denominators, outward angle bound
and reflection proof are mathematical premises reviewed separately from the finite
coefficient checks. Their definitions and proof are in H-108 and H-109.

Both implementations have a closed A1/A3 selector.
They reject a packet for the other clause; neither command accepts arbitrary points.
This adaptation does not alter the generic polynomial kernels or authorize a repeat of
exp-119. Producer and reader share exact NumberField arithmetic, not the margin
construction or Bernstein calculation.
The reader also imports the existing bounded JSON loader; the producer parses its worker
packet separately.

## Launch and Decision

Finish independent review, freeze the source commit and commit this protocol before
dispatch. All record checks must pass.
Run from that clean detached checkout’s `packing/` directory with `PYTHONPATH=src`; the
existing Python 3.14 environment supplies dependencies.
Check that the entire result directory is absent before creating it.
Atomic publication does not protect against overwriting an existing experiment.

Retain producer stdout as `stdout.log`, external stderr/timing as `run.log`, and its own
`packet.json` and `worker.log`. Actual exit zero, `status=proved`, all 24 inequalities
and an empty unresolved inventory permit exactly one independent replay:

```bash
/usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 10s env PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.check_angle_near45_triangle_control ABSOLUTE_PACKET_PATH --target-a1
```

Retain its stdout as `replay.json` and external stderr/timing as `replay.log`. Accept
only actual exit zero, `decision=proved`, six vertex-slab checks, all 24 independent
inequalities, the exact side/A1/slab identity and no unresolved entries.
The reviewed reflection then establishes A2 without another target run.

If the producer is incomplete, nonpositive, missing or externally killed, do not run the
reader. Preserve an explicit non-invocation note, not an invented receipt.
A failed sufficient triangle margin or timeout is unresolved, not a counterexample.
No failure permits another invocation, changed point, smaller angle interval or
subdivision increase.
The lease expires before the block’s closing reserve; it is not a replacement for either
ten-second process cap.

Even success leaves near-45 localization and both twelve-point clauses open.
It does not establish H-036 or improve the global packing bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
