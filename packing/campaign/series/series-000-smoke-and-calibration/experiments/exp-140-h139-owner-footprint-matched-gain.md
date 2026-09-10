---
title: "exp-140 \u2014 matched generic owner-footprint covering pilot"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-140
  series: series-000
  title: Matched generic owner-footprint covering pilot
  date: '2026-09-09'
  hypotheses:
  - H-139
  tier: exploratory
  subject:
    label: Four matched finite-support and finite-direction covering LPs for one generic owner class
    engine: devtools.run_owner_footprint_cover with exact rational owner geometry and event-geometry fallback;
      the launch receipt must bind the published source
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 64
      rounding: SciPy HiGHS proposals and float event-cell search; ambiguous geometry is reconstructed
        from rational sites and component polygons. Output weights are rounded by rationalise_sites at
        scale 4000000 without treating that rounding as verification.
    tolerance: Numerical row generation uses the instrument's 1e-9 threshold and retained LP_FEASIBILITY
      allowance. The primary gain must be strictly greater than 0.001. No numerical comparison establishes
      an exact or all-direction claim.
    host_system: Darwin 25.5.0 arm64; ten logical CPUs; Python 3.14.7; one process, sequential arms, default
      solver threading
    selftest_passed: true
    engine_commit: e3340cac
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Unrestricted and bare-point B-core covering programs on the declared available support and
      direction subset
    candidate: Triangle and endpoint-footprint programs for bottom-left m1, sector 0. All arms start from
      the same 19-by-19 grid plus the mark's D4 orbit; each site is an independent variable, and sites
      inside the selected closed footprint are removed.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra, max; session-113 coordinator
    entry_point: packing/devtools/run_owner_footprint_cover.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 10m .venv/bin/python3
      -m devtools.run_owner_footprint_cover --output campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-140-owner-footprint-cover.json
      --class-id bottom-left:m1:j0 --grid-count 19 --inset 1/2 --folded-indices 0,45,90,135,180 --rows-per-direction
      3 --max-rounds 60 --deadline-seconds-per-arm 120 --max-event-cells 5000000 --max-round-cells 30000000
      --scale 4000000
    budget: Four sequential arms with 120-second cooperative deadlines and sixty rounds each; a ten-minute
      external timeout with two-second TERM grace bounds the process. Three rows per direction per round,
      at most five million dense event cells per direction and thirty million per round. One support,
      one direction subset, no target retry or tuning. The instrument checkpoints every completed or partial
      arm.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-140-owner-footprint-cover.json
    commit: e3340cac137b620c57a333f15cb70a3c60551c9e
  results:
  - shape: determination
    role: guard
    question: Did all four numerical arms converge so that the declared matched gain could be read?
    outcome: criterion_missed
    checked_by: Retained raw status partial and process exit0. Unrestricted converged at 11.884615384615401;
      point reached its60-round cap with least surveyed mass 0.955338364468638 and an incomplete objective11.570153761669404.
      Triangle and endpoint were not run, and comparison is null.
  complexity:
    new_dependencies: []
    new_failure_modes:
    - conflating a nine-direction numerical comparison with full-direction coverage
    - tying singleton variables by D4 symmetry in an asymmetric owner branch
    - deriving an owner footprint from the nine numerical directions instead of the full manifest
    - filling gaps between separate exterior domain components
    - treating an unfinished arm as a measured covering objective
    notes: Fourteen focused controls passed before registration, including reflection, exact SAT, tangency,
      positive-area thin cells, and exact generic-event fallback. The estimate-only receipt has 369 available
      singleton sites. Retained variables are 369 unrestricted, 368 point, 367 triangle, and 365 endpoint.
      The largest dense grid has 554280 cells; the largest one-round total is 4436740. No objective was
      evaluated to select these settings.
  verdict:
    decision: unresolved
    primary_criterion: All four arms converge numerically and M_point minus M_endpoint is strictly greater
      than 0.001
    reason: 'Process exit0 preserved a valid partial receipt, but it did not mean scientific completion:
      only unrestricted converged. Point exhausted60 rounds without convergence, triangle and endpoint
      were not run, and the primary difference was not measured. The partial point objective is not a
      covering value or negative result for H139.'
    resume_from: Exp142 freshly restarts the same four arms with 300 rounds and twelve rows per direction;
      exp140 remains unchanged as partial evidence.
  effort:
    timebox: Four sequential arms with120seconds and60rounds per arm inside a ten-minute external timeout
    wall_seconds: 15.98
    stopped_by: timebox
---
# Exp-140: Generic Owner-Footprint Pilot

The published process exited0 after15.98seconds, but its raw scientific status is
`partial`. The unrestricted arm converged at `11.884615384615401`. The point arm reached
the declared60-round limit with least surveyed mass `0.955338364468638`; its last
objective `11.570153761669404` is an incomplete LP point.
The fail-fast runner therefore did not start triangle or endpoint, and `comparison` is
null.

H139 remains unresolved.
No point-minus-endpoint gain was measured, and the clean process exit means only that
the partial checkpoint was written successfully.

This protocol fixes one numerical comparison before the target process starts.
The four arms are unrestricted, bare owned point, reviewed triangle, and endpoint
footprint. All use the declared independent support and nine residual orientations.
The point, triangle, and endpoint geometry comes from the full 361-orientation owner
manifest.

Acceptance requires every arm to converge and `M_point − M_endpoint > 0.001`. The
instrument also records `M_point − M_triangle`, `M_triangle − M_endpoint`, and
`M0 − M_endpoint − 1` as secondary diagnostics.
Those values cannot replace the primary criterion.

The source must be committed and pushed before launch.
Retain the launch HEAD, UTC instant, exit status, process log, and incremental JSON
receipt. A guard, timeout, unresolved separator, or incomplete arm leaves the comparison
unresolved. A completed primary gain at most `0.001` rejects H-139 only in this finite
regime. No numerical outcome changes the global packing bracket or establishes exact
coverage.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
