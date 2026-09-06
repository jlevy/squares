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
  lease:
    expires: '2026-09-06T21:12:35Z'
    host: local coordinator
  results: []
  verdict:
    decision: in-progress
    primary_criterion: Exact independently replayed finite-row upper certificate at most eleven.
    reason: Prospective protocol frozen before any target rows or optimized weights were evaluated.
---
# exp-113 — A Fixed-Support Ceiling Screen

This prospective record selects one invocation of the independently reviewed
[BC254 instrument](../results/agenda-026/bc-254-target-readiness-independent-review.md).
It does not start a geometric-support search or a complete arrangement build.
Experiment112 is already reserved to the separate H092 transport; these identities do
not replace that work.

The instrument and H099 readiness are retained at `e70458a9`. The target runs in an
immutable checkout of that source revision after this protocol is committed.
The command uses the existing frozen project interpreter with `PYTHONPATH=src`, avoiding
an editable-package reinstall from the isolated checkout.
The known-packing source control yields 88 labelled images, 60 distinct placements,
eight orbits and exact uniform mass11. No optimized target was used to select the
support, rows, arithmetic, cap or criterion.

## Frozen Decision and Retention

The screen starts at zero in the exact LP with the negative identity active basis.
It uses the fixed initial row sequence, checks the first certificate before any
conditional extension, and permits no replacement grid, basis, solver or placement.
The file checker independently reconstructs support preimages, determinant incidences,
positive neighborhoods and the rational upper inequality; it does not run an optimizer.
Shared sequence generation is not independent execution-history attestation.

- If the separate replay verifies an upper bound of eleven, reject H099 on exactly this
  support. The known feasible average rules out an upper bound below eleven; such an
  output is a failed control, not a stronger result.
- If the finite-row optimum exceeds eleven, leave H099 unresolved.
  Finite rows do not establish almost-everywhere depth, so there is no dual
  mass-above-eleven claim.
- A capped, invalid, unreplayable or incomplete run leaves H099 unresolved and retains
  the actual refusal and unchecked remainder.
  Do not label it a mathematical negative.

Retain stdout as `packet.json` and stderr as `run.log` in the declared result directory,
then retain separate file-checker output as `replay.json` and its costs as `replay.log`.
Record the actual exit status and process wall/CPU in this experiment, including startup
outside the internal worker clock.
A failed producer may leave empty stdout; that is not a certificate and must not be sent
to mathematical acceptance.
No new checksum manifest is needed for these same-tree artifacts.

The independent review and coordinator disposition follow in the same PR101. Nothing
here changes the global unit-square packing bound or the source certificate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
