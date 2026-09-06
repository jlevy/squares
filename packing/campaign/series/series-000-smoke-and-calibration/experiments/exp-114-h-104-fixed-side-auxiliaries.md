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
  lease:
    expires: '2026-09-06T21:14:00Z'
    host: local coordinator
  results: []
  verdict:
    decision: in-progress
    primary_criterion: All seven fixed-formula exact-angle auxiliary clauses hold.
    reason: Prospective record before any q-target geometry; independent protocol review precedes execution.
---
# exp-114 — A Ten-Second Point-Cover Discriminator

This one run tests [H-104](../../../hypotheses/H-104-fixed-side-point-cover-auxiliaries.md),
not the full H-036 packing statement. The root commits this protocol before accessing
target geometry and runs it from a clean immutable checkout of `e45c8a63`.
The [adapter review](../results/agenda-026/bc-255-fixed-side-discriminator-independent-review.md)
has accepted the source-preserving algorithm and its controls.

Accept H-104 only if all seven clauses are completely checked, the exact input and
receipt agree with this protocol, and independent output review accepts that scope.
The positive result relies on the reviewed exhaustive event-stratum algorithm; counts
alone are not a standalone geometric certificate.
Reject H-104 if an independent exact replay verifies one returned counterexample to a
clause, even if the remaining clauses are unchecked. With neither a complete positive
check nor a verified counterexample, leave it unresolved.

Retain producer stdout as `packet.json` and stderr/process costs as `run.log` in the
declared directory. The independent reviewer owns a separate ten-second receipt/witness
replay and retains its result and cost. It must not rerun the target producer or infer
positive exhaustive coverage from counts. A failed run with no checked negative witness
is not a mathematical negative. No unchanged retry is authorized.

A checked failure parks the continuous-angle extension of these point formulas. A
complete positive result permits pricing that extension, but no continuous-angle work
starts automatically. Neither outcome proves or refutes H-036; its original3.878 and
±0.25-degree criterion remains fixed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
