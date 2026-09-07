---
title: exp-114 — one fixed-side exact-angle auxiliary screen
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-114
  series: series-000
  title: Test the frozen point-cover auxiliaries at side1939/500
  date: '2026-09-06'
  hypotheses: [H-104]
  tier: confirmatory
  subject:
    label: Seven exact-angle auxiliary clauses on the fixed BC255 point sets
    engine: BC255 fixed-side discriminator and reviewed exhaustive center-stratum algorithm
    engine_commit: e45c8a633090476121701d94d50c034e85e3f7c7
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Python3.14.7, one worker on the shared host
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: Original exact source side; all seven source clauses and boundary/refusal controls independently replayed.
    candidate: Fixed q=1939/500 and unchanged point formulas; exactly zero then45 degrees.
    runs_per_condition: 1
    interleaved: false
    operator: Codex coordinator, max reasoning, think-d2d1 in Session089
    commit: e45c8a633090476121701d94d50c034e85e3f7c7
    dirty: false
    entry_point: packing/devtools/run_restricted_orientation_discriminator.py
    command: >-
      cd packing && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
      VECLIB_MAXIMUM_THREADS=1 PYTHONPATH=src
      /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.run_restricted_orientation_discriminator --target-fixed-side
      --timeout-seconds 10
    budget: >-
      One producer with a ten-second child wall cap. One independent receipt/witness
      replay has a separate ten-second cap. No target retry, changed formula,
      sampled angle or longer run. Record startup and review costs separately.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-114-h-104-fixed-side-auxiliaries/packet.json
  effort:
    timebox: One ten-second producer and one independent ten-second reader, each run once
    wall_seconds: 2.46
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: Do the fixed point formulas satisfy all seven exact-angle auxiliary clauses?
    outcome: criterion_met
    checked_by: >-
      The reviewed exhaustive producer completed both exact angles with all seven
      clauses true. One independent rational-quadratic input/receipt check accepted
      the retained packet; positive coverage relies on the reviewed exhaustive
      algorithm, not a standalone packet certificate. H036 remains unresolved.
  verdict:
    decision: accepted
    primary_criterion: All seven fixed-formula exact-angle auxiliary clauses hold.
    reason: >-
      All seven fixed-formula auxiliaries hold at q=1939/500 for exactly zero and45
      degrees in the reviewed exact computation. The independent reader verifies
      inputs and complete receipt scope. No nearby-angle or H036 conclusion follows.
    commit: 2153cb0278200e1cc11251c17b765f80155f6547
---
# exp-114 — A Ten-Second Point-Cover Discriminator

H-104 is accepted at its narrow auxiliary scope.
The producer completed all seven clauses, and its single independent file replay
accepted the exact inputs and receipt.
There were no unchecked clauses or returned obstructions.
H-036 remains unresolved; this does not improve the already known exact-0/45 packing
bound or cover nearby angles.

The prospective claim and protocol were committed before target access; `2153cb02`
retains the independently reviewed reader and final operational lease.
All 31 record checks passed before the single producer run from clean `e45c8a63`. The
reader ran once from clean `2153cb02`, at 21:35:35 UTC, and returned exit 0. The
[independent output review](../results/exp-114-h-104-fixed-side-auxiliaries/target-output-independent-review.md)
accepts computational verification through the reviewed exhaustive algorithm plus
independent exact input/receipt checks, not a standalone exhaustive certificate.

Producer process cost was 2.41 seconds wall and 2.37 seconds CPU; the worker reported
2.280254 seconds wall and 2.249838 seconds CPU. The independent reader used 0.05 seconds
wall and 0.05 seconds CPU. Summed process wall was 2.46 seconds and CPU 2.42 seconds;
these do not measure operator attention.
Both process exits were 0, within their separate ten-second caps, and neither was
repeated.

Event-product stratum counts were `[280,526,247]` at 0 degrees and `[668,1397,728]` at
45 degrees. Six 45-degree strata avoid the ten-set, one in the canonical region.
These are diagnostic counts, not the independent proof of exhaustive coverage.
The next decision is whether to fund the separately priced continuous-angle instrument.
No such extension is automatically authorized by this result.

## Retained Readiness and Prospective Protocol

The target remained unopened during reader development.
The independent reader’s author stopped at 21:13:28 UTC with nine passing source/toy
tests, but explicitly withheld reader readiness pending cold review and two targeted
regressions. The original 21:14 operational lease expired without a target invocation.
`think-slox` then returned cold-review GO, with twelve source/toy tests passing and
writer stop at 21:26:39 UTC. Root accepts reader readiness and prospectively opens the
unused target/replay allowances through 21:40 UTC. No process budget has been consumed,
shortened or reset.

The independent command, run from the committed reader checkout, is:

```bash
PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.check_restricted_orientation_discriminator PACKET --target-fixed-side --producer-exit-code STATUS
```

`PACKET` is the absolute retained producer path and `STATUS` its actual exit code.
The reader installs its own fixed ten-second alarm.
Retain its stdout as `replay.json`, stderr and process costs as `replay.log`, and the
independent scope review beside them.
There is no second producer or source-distinct exhaustive positive certificate.

This one run tests
[H-104](../../../hypotheses/H-104-fixed-side-point-cover-auxiliaries.md), not the full
H-036 packing statement.
The root commits this protocol before accessing target geometry and runs it from a clean
immutable checkout of `e45c8a63`. The
[adapter review](../results/agenda-026/bc-255-fixed-side-discriminator-independent-review.md)
has accepted the source-preserving algorithm and its controls.

Accept H-104 only if all seven clauses are completely checked, the exact input and
receipt agree with this protocol, and independent output review accepts that scope.
The positive result relies on the reviewed exhaustive event-stratum algorithm; counts
alone are not a standalone geometric certificate.
Reject H-104 if an independent exact replay verifies one returned counterexample to a
clause, even if the remaining clauses are unchecked.
With neither a complete positive check nor a verified counterexample, leave it
unresolved.

Retain producer stdout as `packet.json` and stderr/process costs as `run.log` in the
declared directory. The independent reviewer owns a separate ten-second receipt/witness
replay and retains its result and cost.
It must not rerun the target producer or infer positive exhaustive coverage from counts.
A failed run with no checked negative witness is not a mathematical negative.
No unchanged retry is authorized.

A checked failure parks the continuous-angle extension of these point formulas.
A complete positive result permits pricing that extension, but no continuous-angle work
starts automatically.
Neither outcome proves or refutes H-036; its original3.878 and ±0.25-degree criterion
remains fixed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
