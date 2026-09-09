---
title: exp-135 — matched nine-direction fixed-corner residual covering pilot
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-135
  series: series-000
  title: Matched nine-direction fixed-corner residual covering pilot
  date: '2026-09-09'
  hypotheses:
  - H-136
  tier: exploratory
  subject:
    label: matched finite-site and finite-direction covering LPs with zero or four fixed corner obstacles
    engine: devtools.run_residual_cover_pilot; source will be frozen and identified at launch
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 64
      rounding: scipy HiGHS proposals and float event-cell search; output atoms rounded by
        the retained rationalise_sites routine at scale 4000000, without treating rounding as verification
    tolerance: Numerical convergence uses the instrument's 1e-9 row-addition threshold
      and retained LP_FEASIBILITY allowance. The paired accept margin is strictly greater
      than 0.001. No numerical comparison establishes a packing bound.
    host_system: Darwin 25.5.0 arm64; ten logical CPUs; Python 3.14.7; one process,
      sequential arms, default solver threading
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Unrestricted B-core covering program on the declared grid and direction subset
    candidate: The same program with cores restricted to avoid the interiors of four fixed
      axis-aligned unit squares flush in the container corners
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra, max; coordinator of session-111
    entry_point: packing/devtools/run_residual_cover_pilot.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 5m
      .venv/bin/python3 -m devtools.run_residual_cover_pilot --side 96/25 --shrink 9977/10000
      --grid-counts 19 --direction-steps 180 --direction-indices 0,23,45,68,90,113,135,158,180
      --deadline-seconds 120 --max-rounds 60 --rows-per-direction 4 --max-event-cells 2000000
      --max-round-cells 15000000 --scale 4000000 --output
      campaign/series/series-000-smoke-and-calibration/results/agenda-031/exp-135-paired-cover.json
    budget: Two sequential arms with 120-second cooperative deadlines and sixty rounds each;
      a five-minute external timeout with two-second TERM grace bounds the process.
      Four rows per direction per round, at most two million dense event cells per direction
      and fifteen million per round. One site grid, one direction subset, no target retries
      or tuning. An interrupted arm may lack its final solver point; preserve any completed
      arm and partial receipt and record the missing evidence explicitly.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/exp-135-paired-cover.json
  lease:
    expires: '2026-09-09T03:30:00Z'
    host: Darwin 25.5.0 arm64
  results: []
  complexity:
    lines_changed: 0
    new_dependencies: []
    new_failure_modes:
    - conflating a finite-direction numerical cover with an all-angle exact certificate
    - comparing different supports or forgetting the four-unit change in contradiction threshold
    - filling gaps between the six convex residual-domain components
    - treating an uncompleted arm as a negative result
    notes: Pre-target estimate only, with 361 sites in 55 orbits. Maximum dense cells per
      direction are 525625 unrestricted and 546121 residual; the corresponding sums over
      nine directions are 4206521 and 4370649. No objective was evaluated to select this regime.
  verdict:
    decision: in-progress
    primary_criterion: Both arms converge numerically and M_global minus M_residual minus 4
      is strictly greater than 0.001
    reason: Prospective protocol; no target has run. A completed paired score at most 0.001
      rejects this finite numerical claim. A partial, guarded, errored or timed-out run
      stays unresolved. Source identity and passed controls will be retained before launch.
---
# exp-135 — Prospective Residual-Cover Pilot

At `L = 96/25` and `B = 9977/10000`, fix four axis-aligned physical unit squares flush
in the four corners.
The residual program covers all selected-direction `B`-squares inside the container
whose interiors avoid those obstacles.
This is a conservative family containing the seven strict inner cores of any completion
of that fixed branch.

Both arms use the same 19-by-19 grid with inset `1/2` and the same nine indices from the
retained 181-direction net.
Their score is `M_global − M_residual − 4`. Residual mass below seven is an additional
numerical signal, not the accept rule and not a packing certificate.
The subset does not supply the all-angle transfer.

## Domain and evidence contract

For direction `(c,s)`, let `h = B/2`, `e = h(c+s)`, `a = 1+e`, `b = L−1−e`, `u = cx+sy`
and `v = −sx+cy`. Intersect every piece below with container containment
`e ≤ x,y ≤ L−e`:

| Piece | Additional inequalities |
| --- | --- |
| Vertical strip | `a ≤ x ≤ b` |
| Horizontal strip | `a ≤ y ≤ b` |
| Bottom-left cap | `x ≤ a`, `y ≤ a`, `u ≥ c+s+h` |
| Bottom-right cap | `x ≥ b`, `y ≤ a`, `v ≥ c−s(L−1)+h` |
| Top-left cap | `x ≤ a`, `y ≥ b`, `v ≤ c(L−1)−s−h` |
| Top-right cap | `x ≥ b`, `y ≥ b`, `u ≤ (c+s)(L−1)−h` |

Two independent mathematical reviews derived this union by the separating-axis test.
For the bottom-left obstacle the alternatives reduce to `x ≥ a`, `y ≥ a`, or
`u ≥ c+s+h`; reflection gives the other corners.
The mixed-axis alternatives imply the horizontal or vertical alternatives using
`h+e(s−c)=Bs²` and `h+e(c−s)=Bc²`. The formulas hold for the final retained direction
slightly beyond 45 degrees as well as for the axis endpoint.
At the axis the caps collapse into boundaries already covered by the strips.
All inequalities are weak, admitting tangency.

The instrument must retain the union of reachable intervals, never its convex hull, and
propose witnesses from actual components.
Independent controls use full separating axes, exact touching/overlap fixtures, and
small exact event-cell comparisons.
The numerical run saves support coordinates, raw weights, rationalized proposals,
per-round objectives and stop reasons.
Exact validation fields remain unset unless a separate reader is actually run.

This is a prospective test of fully fixed corner obstacles.
It does not establish that four such poses occur in every packing.
The ownership-sector construction and the literature-based continuation remain separate
mathematical work.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
