---
title: exp-115 — one exact overweight-pair screen of exp-113's fixed candidate
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-115
  series: series-000
  title: Test one fixed density candidate for a positive-area pair obstruction
  date: '2026-09-06'
  hypotheses: [H-105]
  tier: confirmatory
  subject:
    label: Exact exp113 weights on the retained D4 Trump support
    engine: BC254 pair separator and independent axis/determinant certificate replay
    engine_commit: cf299e6c7516c2ad41ba05c8e4ac8bb3ca16b5c6
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Python 3.14.7, one target process on the shared host
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Exact source and uniform-average controls, strict overlap/contact/separation
      toys, higher-order limitation and tampered-packet refusals. Independent
      readiness review passed 42 source/toy tests without target construction.
    candidate: >-
      trump11-v1 only; exact retained side and 60 canonical D4 placements;
      eight per-member weights (1,0,2/5,1/10,0,1/10,3/10,0), with 134 eligible pairs.
    runs_per_condition: 1
    interleaved: false
    operator: Codex coordinator, max reasoning, think-whmn in Session089
    commit: cf299e6c7516c2ad41ba05c8e4ac8bb3ca16b5c6
    dirty: false
    entry_point: packing/devtools/run_full_size_density_pair_separator.py
    command: >-
      cd packing && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
      VECLIB_MAXIMUM_THREADS=1 PYTHONPATH=src
      /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.run_full_size_density_pair_separator
      --candidate campaign/series/series-000-smoke-and-calibration/results/exp-113-h-099-trump-support-screen/packet.json
      --timeout-seconds 30
    budget: >-
      One producer with a 30-second child wall cap, stopping at the first witness
      or complete eligible-pair exhaustion. One separately dispatched file replay
      has its own 30-second cap. No unchanged retry, new weights, LP, necessary row,
      higher-order separator or support extension. Record actual process costs.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-115-h-105-fixed-candidate-pair-obstruction/packet.json
  lease:
    expires: '2026-09-06T22:17:50Z'
    host: local coordinator
  results: []
  verdict:
    decision: in-progress
    primary_criterion: A strict positive-area overweight-pair obstruction exists for these fixed weights.
    reason: Prospective candidate-only record before target construction; reviewed source instrument is committed separately.
---
# exp-115 — A Pair Test of the Fixed Candidate

This prospectively frozen experiment tests
[H-105](../../../hypotheses/H-105-exp113-overweight-pair-obstruction.md), not H-099. The
coordinator accepted the independent source/toy review at `cf299e6c`, which freezes both
the producer and checker.
No target construction or target binding roundtrip ran during instrument development or
review.

The parent is
`packing/campaign/series/series-000-smoke-and-calibration/results/exp-113-h-099-trump-support-screen/packet.json`
at the same `cf299e6c` revision; its accepted outcome was first retained at `a105f729`.
The source is `packing/cases/trump11/packing.py`, named `trump11-v1`. Both target entry
points bind its exact algebraic side, canonical orbit ordering, 60 placement keys, eight
unchanged rational weights and the $56/5$ parent label.
The parent LP proof, row generation and pivot history are not replayed.
Git provenance and the accepted parent review supply that prerequisite.

The sole producer runs from a clean immutable `cf299e6c` checkout after this protocol is
committed and its record checks pass.
Retain stdout as `packet.json` and stderr plus the process timer as `run.log` in the
declared result directory.
After successful complete output, the independent reviewer runs once from that same
frozen source revision:

```bash
PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.check_full_size_density_pair_separator PAIR_PACKET --parent PARENT_PACKET --timeout-seconds 30
```

`PAIR_PACKET` is the retained producer file and `PARENT_PACKET` the frozen parent path.
Retain reader stdout as `replay.json`, stderr and process costs as `replay.log`, and the
independent scope review beside them.
Both CLIs bound worker startup and computation; their internal alarms also guard direct
worker invocation. The 30-second limits are caps, not target-runtime measurements.

Accept H-105 only for an independently checked strict positive-area overweight witness,
including the canonical separated prefix.
The executable’s `candidate-refuted` decision therefore **accepts the obstruction
hypothesis**. Reject H-105 only if all 134 eligible pairs have independently checked
separating axes. Timeout, incomplete output, failed source binding or failed replay
leaves it unresolved, with the actual guard or process failure retained instead of an
invented negative. A failed producer receives refusal review only, not another target
invocation.

A witness refutes only exp-113’s fixed weight assignment.
It does not refute H-099, change the $[11,56/5]$ supremum bracket or yield a packing
bound. No pair obstruction would still leave higher-order overlap unchecked.
The next possible branch after a witness is a separately priced full-support
off-boundary cut and bounded same-support ceiling update; after no pair obstruction, it
is complete positive-area-face verification of the unchanged weights.
Neither branch is funded here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
