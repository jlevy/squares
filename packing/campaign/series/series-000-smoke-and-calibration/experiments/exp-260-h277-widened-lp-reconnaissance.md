---
title: exp-260 — frozen numerical n17 mixed-angle widened-LP challenge
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-260
  series: series-000
  title: Forty-eight frozen mixed-angle targets and eight matched relaxed controls
  date: '2026-10-07'
  hypotheses: [H-277]
  tier: exploratory
  subject:
    label: Conditional 19-pair LP without square6, rational-root midpoint, position radius 1/100.
    engine: devtools.probe_n17_widened_lp, source frozen by registration commit before target solves.
    assurance: numerically-checked
    method: numerical-f64
    precision: {binary_bits: 53, rounding: IEEE 754 nearest; no outward rounding}
    tolerance: HiGHS and residual controls1e-8; positive margin 1e-6; matched monotonicity1e-8.
    host_system: macOS arm64, project Python3.14.7, SciPyHiGHS; one worker and one BLAS/OpenMP thread.
    selftest_passed: true
    engine_commit: 8f7b60276e57a10fe3ca0d306134773aab6580fb
  instance: {axis: n, point: 17, role: target}
  method:
    control: Synthetic LP/support/dual signs; zero-turn endpoint and nominal-centroid residuals; slider-domain and signed-geometry controls; eight matched drop_sliders evaluations.
    candidate: Frozen48-point bounded_tube numerical challenge, all 256rawbranches accounted perpoint.
    runs_per_condition: 1
    interleaved: true
    operator: GPT-6.1 Sol coordinator executes Astra's frozen mathematical contract, Session184.
    entry_point: packing/devtools/probe_n17_widened_lp.py
    command: >-
      From packing/ with TMPDIR, UV_CACHE_DIR and CARGO_TARGET_DIR under verified
      external scratch, OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1, MKL_NUM_THREADS=1:
      /Volumes/spud-ext1/agent-scratch/n17-w3-01a114fb/venv/bin/python3 -m
      devtools.probe_n17_widened_lp --points
      campaign/series/series-000-smoke-and-calibration/results/exp-260-widened-lp-reconnaissance/points.json
      --rho-position 1/100 --branch-limit 256 --wall-seconds 15 --solver-seconds 1
      --total-wall-seconds 540 --output
      campaign/series/series-000-smoke-and-calibration/results/exp-260-widened-lp-reconnaissance/run.json
    budget: 540 seconds total including controls;15 seconds/point,1 second/solver; cooperative wall ceiling with bounded solver leases.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-260-widened-lp-reconnaissance
    commit: 8f7b60276e57a10fe3ca0d306134773aab6580fb
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: All48 targets have complete execution and finite primal/dual minima above S0+1e-6, with all matched controls passing.
    outcome: no_progress
    checked_by: Retained run.json and Astra read-only review; all56 evaluations executed, but five bounded targets and two matched controls are wholly numerically infeasible, preventing the finite-minimum criterion.
  verdict:
    decision: unresolved
    primary_criterion: H277 numerical positive margin 1e-6 on all 48 complete targets, both finite primal/dual-candidate minima, all readiness and matched controls pass.
    reason: Forty-three targets have positive finite numerical minima; five all-infeasible targets lack exact Farkas witnesses. The frozen positive criterion is unavailable. Slider omission exposes a negative relaxed margin, so slider coverage remains essential.
  effort:
    timebox: 540 seconds including readiness and matched controls
    wall_seconds: 8.389171791961417
    stopped_by: criterion
---
# exp-260: Mixed-Angle Numerical Reconnaissance

This round executes the H-277 contract without changing its sample or wall ceiling.
Terminal numeric infeasibility may enter the labelled heuristic aggregation only; every
result keeps `bound_coverage_certified=false`. The point roster is retained before
target execution.

An incomplete point, failed control or exhausted ceiling prevents positive evidence.
Useful finite branch candidates and unstarted points remain recorded.
Any numerical counterexample concerns this conditional relaxation and requires
exact-root and row checks before mathematical use.

## Outcome

All 56 registered evaluations completed in 8.389 seconds at clean source `8f7b60276`.
The process returned exit1 for its declared inconclusive status; stderr was empty.
Outer signed Fsplit, signed Bsplit and negative Fcommon targets are wholly numerically
infeasible, as are both matched Fsplit controls.
These statuses do not provide exact infeasibility certificates.
The other 43 bounded targets have positive finite primal and dual-candidate minima.
The smallest finite primal margin is approximately0.000171915, at negative omega16.

Removing slider bounds at positive omega14 gives an approximately-0.000100223 relaxation
margin, against the bounded partner’s approximately0.002368279. This is a domain
control, not a physical packing counterexample.
The signed omega11 relaxed minima equal the nominal midpoint side.
No target, criterion or budget was changed after these observations.

The complete numerical receipt is retained.
An independently implemented reader will audit its accounting and frozen criterion;
exact geometry, infeasibility and uniform angle coverage remain separate obligations.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
