---
title: exp-143 — matched four-owner footprint covering pilot
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-143
  series: series-000
  title: Matched four-owner footprint covering pilot
  date: '2026-09-09'
  hypotheses:
  - H-141
  tier: exploratory
  subject:
    label: >-
      Four matched finite-support and finite-direction covering LPs for one compatible
      four-owner branch
    engine: >-
      devtools.run_owner_footprint_cover --owner-count 4 with exact rational
      multi-footprint decomposition and event-geometry fallback; the launch receipt
      must bind the published source
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 64
      rounding: >-
        SciPy HiGHS proposals and float event-cell search; ambiguous geometry is
        reconstructed from rational sites and component polygons. Output weights are
        rounded by rationalise_sites at scale 4000000 without treating that rounding
        as verification.
    tolerance: >-
      Numerical row generation uses the instrument's 1e-9 threshold and retained
      LP_FEASIBILITY allowance. The primary gain must be strictly greater than 0.001.
      No numerical comparison establishes an exact or all-direction claim.
    host_system: >-
      Darwin 25.5.0 arm64; ten logical CPUs; Python 3.14.7; one process, sequential
      arms, default solver threading
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: >-
      Unrestricted and four-bare-point B-core covering programs on the declared
      available support and direction subset
    candidate: >-
      Four-triangle and four-endpoint-footprint programs for the compatible reflected
      m1, sector-0 corner classes. All arms start from the same 19-by-19 grid plus the
      mark's D4 orbit; each site is an independent variable, and sites inside the
      selected closed footprint union are removed once.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra, max; session-113 coordinator
    entry_point: packing/devtools/run_owner_footprint_cover.py
    command: >-
      cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 10m
      .venv/bin/python3 -m devtools.run_owner_footprint_cover --output
      campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-143-four-owner-footprint-cover.json
      --owner-count 4 --class-id bottom-left:m1:j0 --grid-count 19 --inset 1/2
      --folded-indices 0,45,90,135,180 --rows-per-direction 12 --max-rounds 300
      --deadline-seconds-per-arm 120 --max-event-cells 5000000
      --max-round-cells 30000000 --scale 4000000
    budget: >-
      Four sequential arms with 120-second cooperative deadlines and 300 rounds each;
      a ten-minute external timeout with two-second TERM grace bounds the process.
      Twelve rows per direction per round, at most five million dense event cells per
      direction and thirty million per round. One support, one direction subset, one
      four-owner branch, no target retry or tuning. The instrument checkpoints every
      completed or partial arm.
    record: >-
      packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-143-four-owner-footprint-cover.json
  lease:
    expires: '2026-09-09T05:00:00Z'
  results: []
  complexity:
    new_dependencies: []
    new_failure_modes:
    - filling legal gaps by taking the convex hull of four collision polygons
    - forming an exponential product of obstacle exterior half-planes
    - counting one site once for every footprint that contains it
    - conflating a nine-direction numerical comparison with full-direction coverage
    - treating an unfinished arm as a measured covering objective
    notes: >-
      Thirty-three focused controls passed before registration. Seventeen directly
      cover multi-footprint geometry, including exact SAT, tangency, positive-area
      triangular cells, a fully covered container, and independent inclusion-exclusion
      area agreement. A separate control checks exact event fallback against the
      multi-footprint predicate, and a construction-only sweep checked all 361 endpoint
      directions. The estimate-only receipt has 369 available singleton sites.
      Retained variables are 369 unrestricted, 365 point, 361 triangle, and 353
      endpoint. The largest dense grid has 560965 cells; the largest one-round total is
      4443859. No objective was evaluated to select these settings.
  verdict:
    decision: in-progress
    primary_criterion: >-
      All four arms converge numerically and M_point minus M_endpoint is strictly
      greater than 0.001
    reason: >-
      Prospective numerical comparison; no target arm or objective has been evaluated.
---
# Exp-143: Four-Owner Footprint Pilot

This protocol fixes one numerical comparison before the target process starts.
The four arms are unrestricted, four bare owned points, four guaranteed triangles, and
four endpoint footprints.
All use the declared independent support and nine residual orientations.
The point, triangle, and endpoint geometry comes from the full 361-orientation owner
manifest.

Acceptance requires every arm to converge and `M_point − M_endpoint > 0.001`. The
instrument also records whether endpoint mass is below seven and reports
`M0 − M_endpoint − 4` as secondary diagnostics.
Those values cannot replace the primary criterion.
A settled `M0 − M_point` above four breaches the exact point-extension sanity bound and
invalidates the comparison.

The source must be committed and pushed before launch.
Retain the launch HEAD, UTC instant, exit status, process log, and incremental JSON
receipt. A guard, timeout, unresolved separator, point-extension breach, or incomplete
arm leaves the comparison unresolved.
A completed primary gain at most `0.001` rejects H-141 only in this finite regime.
No numerical outcome changes the global packing bracket, covers other owner branches, or
establishes exact coverage.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
