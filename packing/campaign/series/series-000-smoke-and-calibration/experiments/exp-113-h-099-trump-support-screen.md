---
title: exp-113 — exact ceiling screen on Trump's D4 support
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-113
  series: series-000
  title: One exact finite-row ceiling screen on the retained Trump D4 support
  date: '2026-09-06'
  hypotheses: [H-099]
  tier: confirmatory
  subject:
    label: Exact necessary-row LP upper bound on the fixed Trump D4 placement support
    engine: BC254 support-screen producer and determinant-based packet replay
    engine_commit: e70458a9c40cfab46d2f2233b0dfbb47501a4de8
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Python 3.14.7, one target process on the shared host
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Exact retained Trump packing, independent D4 preimages and uniform mass11;
      45 author/reviewer tests, including the repaired lexical parser refusal.
    candidate: >-
      trump11-v1 only: 60 placements in eight orbits; frozen center-first necessary
      rows and at most the 36-point dyadic extension, with no new placements.
    runs_per_condition: 1
    interleaved: false
    operator: Codex coordinator, max reasoning, think-2rxf in Session089
    commit: e70458a9c40cfab46d2f2233b0dfbb47501a4de8
    dirty: false
    entry_point: packing/devtools/run_full_size_density_support_screen.py
    command: >-
      cd packing && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
      VECLIB_MAXIMUM_THREADS=1 PYTHONPATH=src
      /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.run_full_size_density_support_screen --solve-target
      --source trump11-v1 --timeout-seconds 60
    budget: >-
      One target invocation, 60-second child wall cap, at most two exact LP solves
      of at most64pivots each. A separate file replay has its own60-second cap.
      Startup, teardown and review costs are recorded separately. No unchanged retry
      on timeout, pivot refusal, malformed output or missing source premise.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-113-h-099-trump-support-screen/packet.json
  effort:
    timebox: One60-second producer and one separate60-second file replay
    wall_seconds: 28.79
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: Does the exact independently replayed finite-row ceiling reach eleven?
    outcome: criterion_missed
    checked_by: >-
      One separate file replay verifies20necessary rows, nonnegative rational
      multipliers, and matching primal and upper witnesses of56/5. Finite-row
      feasibility is not complete a.e.-depth feasibility; H099 remains unresolved.
  verdict:
    decision: unresolved
    primary_criterion: Exact independently replayed finite-row upper certificate at most eleven.
    reason: >-
      The verified ceiling56/5 exceeds11. It bounds the fixed-support problem but
      neither refutes H099 nor supplies the missing complete a.e.-depth proof.
    commit: e70458a9c40cfab46d2f2233b0dfbb47501a4de8
    reopen_when: A newly priced and prospectively frozen separator or complete arrangement instrument.
---
# exp-113 — A Fixed-Support Ceiling Screen

The screen returned an exact finite-row optimum of $56/5=11.2$, independently replayed
once. H-099 remains unresolved.
The known feasible mass-eleven average and this finite-row upper certificate place the
fixed-support supremum in $[11,56/5]$; they do not exhibit an a.e.-feasible weighting of
mass $56/5$.

The prospective protocol was committed as `b3046532`, with record-view corrections at
`cc18f64c`; all 31 record checks passed before target access.
The producer ran once from clean `e70458a9`, returned exit code 0, and used two solves
with 6 and 8 pivots.
Twenty distinct necessary rows survived the fixed sequence.
The separate checker also returned exit code 0. The
[independent review](../results/exp-113-h-099-trump-support-screen/independent-review.md)
records its scope and shared foundations.

The producer process took 19.69 seconds wall and 17.36 seconds CPU; the worker reported
19.561851 seconds wall and 17.245133 seconds CPU. The separate replay took 9.10 seconds
wall and 9.06 seconds CPU. Their summed process wall time is 28.79 seconds and CPU time
is 26.42 seconds; operator attention and review prose time are not measured or included
in those totals. The output replay finished within its lease; final review formatting
ended at 21:01:02, twelve seconds after the review deadline.
No target or replay allowance was extended.

## Retained Prospective Protocol

The prospective protocol selected one invocation of the independently reviewed
[BC-254 instrument](../results/agenda-026/bc-254-target-readiness-independent-review.md).
It authorized neither a geometric-support search nor a complete arrangement build.
Experiment 112 remains reserved for the separate H-092 transport; this experiment does
not replace that work.

The instrument and H-099 readiness are retained at `e70458a9`. The target ran in an
immutable checkout of that revision after the protocol was committed.
The command used the existing frozen project interpreter with `PYTHONPATH=src`, avoiding
an editable-package reinstall from the isolated checkout.
The known-packing source control yields 88 labelled images, 60 distinct placements,
eight orbits, and exact uniform mass 11. No optimized target was used to select the
support, rows, arithmetic, cap, or criterion.

## Frozen Decision and Retention

The screen starts at zero in the exact LP with the negative identity active basis.
It uses the fixed initial row sequence, checks the first certificate before any
conditional extension, and permits no replacement grid, basis, solver, or placement.
The file checker independently reconstructs support preimages, determinant incidences,
positive neighborhoods, and the rational upper inequality; it does not run an optimizer.
Shared sequence generation is not independent execution-history attestation.

- If the separate replay verifies an upper bound of eleven, reject H-099 on exactly this
  support. The known feasible average rules out an upper bound below eleven; such an
  output is a failed control, not a stronger result.
- If the finite-row optimum exceeds eleven, leave H-099 unresolved.
  Finite rows do not establish almost-everywhere depth, so there is no dual
  mass-above-eleven claim.
- A capped, invalid, unreplayable, or incomplete run leaves H-099 unresolved and retains
  the actual refusal and unchecked remainder.
  Do not label it a mathematical negative.

Retain stdout as `packet.json` and stderr as `run.log` in the declared result directory,
then retain separate file-checker output as `replay.json` and its costs as `replay.log`.
Record the actual exit status and process wall/CPU in this experiment, including startup
outside the internal worker clock.
A failed producer may leave empty stdout; that is not a certificate and must not be sent
to mathematical acceptance.
No new checksum manifest is needed for these same-tree artifacts.

The independent review and coordinator disposition are retained in the same PR #101.
Nothing here changes the global unit-square packing bound or the source certificate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
