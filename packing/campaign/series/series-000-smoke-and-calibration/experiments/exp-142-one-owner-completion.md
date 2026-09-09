---
title: "exp-142 \u2014 complete the one-owner matched comparison"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-142
  series: series-000
  title: Fresh one-owner comparison with a sufficient round allowance
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
    engine_commit: 44bf815f
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
      -m devtools.run_owner_footprint_cover --output campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-142-owner-footprint-cover.json
      --class-id bottom-left:m1:j0 --grid-count 19 --inset 1/2 --folded-indices 0,45,90,135,180 --owner-count
      1 --rows-per-direction 12 --max-rounds 300 --deadline-seconds-per-arm 120 --max-event-cells 5000000
      --max-round-cells 30000000 --scale 4000000
    budget: Four sequential arms with 120 seconds and 300 rounds per arm, twelve rows per direction per
      round. Ten-minute external timeout plus two-second TERM grace; unchanged 5 million per-direction
      and 30 million per-round event guards. Fresh run from initial rows, no warm start or in-run tuning.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-142-owner-footprint-cover.json
    commit: 44bf815fcf424469fddb2258548341c3d4c5b7f0
  results:
  - shape: determination
    role: outcome
    question: Do all arms converge with point-minus-endpoint gain above0.001?
    outcome: criterion_met
    checked_by: All four converged; M0=11.884615384615364, Mpoint=11.574514991181658, Mtriangle=10.555555555555555,
      Mendpoint=10.38888888888889; gain=1.185626102292769. Point-extension and nested-monotonicity guards
      pass. Numerical nine-direction scope only.
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
      evaluated to select these settings. The controlled owner-count extension defaults to the unchanged
      single-owner path; 31 combined controls pass. Dry-run estimates remain unchanged.
  verdict:
    decision: accepted
    primary_criterion: All four arms converge numerically and M_point minus M_endpoint is strictly greater
      than 0.001
    reason: All four numerical arms converged; point-minus-endpoint gain1.185626102292769>0.001. Point-extension
      and monotonicity guards pass. This accepts the finite numerical mechanism claim only; exact full-net
      verification remains separate.
  effort:
    timebox: Four120second arms,300rounds and12rows per direction under10minute external timeout
    wall_seconds: 24.54
    stopped_by: criterion
---
# Exp142: Completed Numerical Footprint Comparison

Published source `44bf815f` completed the four arms in 24.54 seconds.
Unrestricted mass is 11.884615384615364; point mass 11.574514991181658; triangle mass
10.555555555555555; endpoint mass 10.38888888888889. The point-minus-endpoint gain is
1.185626102292769, above the declared 0.001 threshold.
Both internal comparison guards pass.

The one-owner endpoint objective remains above the residual threshold of ten.

The following prospective protocol is retained below, including its original limits.

Exp140 remains unresolved, with its original partial receipt and cost intact.
Its point arm exhausted sixty rounds after 9.62 seconds, before either area arm ran.
This fresh experiment raises the declared round allowance to 300 and adds twelve
violating rows per direction per round.
The support, directions, geometry, 120-second wall allowance per arm, and primary
mathematical criterion are unchanged.

All four programs restart from their normal initial rows.
Accept H139 only if all four converge and the point-minus-endpoint objective gain
exceeds 0.001. A timeout or incomplete arm is unresolved, even if the process writes a
receipt and exits zero.
No comparison between incomplete objectives is evidence of a gain.

On this matched support, the point-extension lemma gives the optimum sanity bound M0
minus Mpoint at most one.
A material violation prompts contract review; arbitrary feasible primal values alone do
not establish an optimum-gap theorem.

Commit and push the instrument and this protocol before a single bounded invocation.
Retain launch source, UTC, dirty state, stdout, process time, exit, and all arm data.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
