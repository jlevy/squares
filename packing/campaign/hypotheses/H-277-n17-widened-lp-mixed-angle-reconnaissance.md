---
title: H-277 — numerical mixed-angle challenge of the n17 widened LP
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-277
  kind: hypothesis
  claim: >-
    At the accepted rational-root midpoint, the conditional 19-pair bounded_tube
    LP with position radius 1/100 has a numerically resolved positive side margin
    greater than 1/1000000 above its nominal side on the frozen 48-point mixed-angle
    roster, under complete terminal numerical execution of all 256 rawbranches.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: positive_numerical_evidence_on_frozen_mixed_angle_roster
    direction: criterion_met
    threshold: Every complete target point has finite primal and dual-candidate minima greater than nominal S0+1e-6; all controls pass.
  instrument: >-
    packing/devtools/probe_n17_widened_lp.py; retained point roster in
    packing/campaign/series/series-000-smoke-and-calibration/results/exp-260-widened-lp-reconnaissance/points.json.
    Mathematical contract in docs/project/research/research-2026-10-07-n17-proof-interfaces-and-lp-contract.md.
    Freeze source and roster before solves. Independent Sol review and focused
    synthetic, geometry, endpoint, domain, partial-output and ceiling controls precede targets.
  instrument_ready: true
  regime: >-
    n17 nominal rational-root midpoint from accepted exp237 certificate;16retained
    labels in order1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17. Position radius 1/100;
    outer half-angle radius 1/200, inner1/2000. Forty-eight bounded_tube points:
    all 32signed coordinate directions at outerradius, both signs of Bcommon,
    Bsplit,Fcommon,Fsplit at both radii. Eight matched drop_sliders controls at
    outer ±e11,±e14,±e16,±Fsplit. The frozen JSON owns exact vectors/order/aliases.
    macOS one worker, BLAS/OpenMP1; HiGHS; tolerance 1e-8; branchlimit256;
    solver1 second/branch,15 seconds/point,540 seconds whole invocation including
    readiness and matched controls. Preserve partial output; do not enlarge budgets.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: At most540 seconds for controls and56point/profile evaluations on one worker.
  prereqs: [H-255, H-256, H-257, H-258, H-265]
  replication: false
  registered: '2026-10-07'
  notes: >-
    This is numerical reconnaissance of a conditional subsystem, not a theorem or
    acceptance of a relaxation bound. Numerically optimal or numerically infeasible
    branches may count toward execution completeness only in the labelled heuristic
    aggregation; numeric infeasibility is not certified infinity. Every point needs
    at least one finite optimum. Missing, timeout, error, residual-failure, unknown
    or unbounded branches make positive evidence unavailable. All-numerical-infeasible
    points are inconclusive. Failed readiness or matched monotonicity controls refuse
    interpretation. A complete primal gap below-1e-6 is a relaxation-counterexample
    candidate requiring exact-root/row verification, not a packing counterexample.
    A gap within±1e-6 is inconclusive. bound_coverage_certified remains false.
    Exact uniform angle coverage, feature forcing and outer capture remain open;
    sampled dual-support signatures imply no basis/patch forecast.
---
# H-277: Widened LP Mixed-Angle Reconnaissance

Astra selected this bounded challenge before any target solve.
It tests whether a wider local relaxation warrants further proof work and exposes soft
mixed directions that coordinate directions alone could miss.
The accepted local theorem keeps its existing radius and scope.

The primal and dual-candidate **values** must each exceed the nominal side plus `1e-6`;
equivalently, both reported gaps must exceed `1e-6`. The dual candidates are floating
calculations with residual checks.
They are not exact certificates.
Each matched relaxed optimum must be no greater than its bounded partner plus `1e-8`;
this is a control, not a prescribed negative historical slope.

The JSON roster freezes all 48 targets and8 matched controls before execution.
It starts with signed Fsplit directions, then the remaining outer mixed directions, then
coordinates, then inner mixed directions; matched controls immediately follow their
target. No missing exp244 primal witness is invented as a direction source.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
