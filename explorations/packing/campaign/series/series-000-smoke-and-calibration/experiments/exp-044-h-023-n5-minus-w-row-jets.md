---
title: exp-044 — exact n = 5 pure -W row-jet test
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-044
  series: series-000
  title: Test pure -W with exact production row jets and scale routing
  date: '2026-08-25'
  hypotheses:
  - H-023
  tier: confirmatory
  subject:
    label: exact second-order feasibility of canonical pure -W at n = 5
    engine: n = 5 pure -W row-jet checker 0.2.0
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: false
  instance:
    axis: n
    point: 5
    role: target
  method:
    control: >-
      exact exp-034, exp-035, exp-036, and exp-038 regeneration; accepted exact-jet
      helper; complete six-case source rows; full center-angle-correction jets; weighted
      rowwise curvature; independent target dispositions; an exact sheet witness; a
      fixed exp-036 positive fixture; explicit owner-3 scale routing with a symbolic real
      bounded limit; twelve typed production mutations; deterministic replay; and
      thirteen individually keyed scope refusals
    candidate: >-
      exp-043's canonical complete-vector -W candidate, reimplemented through the
      accepted case-free exact-jet layer without copying exp-036 coefficients or
      promoting the exp-043 draft's temporary output
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    entry_point: explorations/packing/cases/n5/minus_w_obstruction.py
    command: >-
      timeout 30 uv run --directory explorations/packing --frozen --quiet python -m
      cases.n5.minus_w_obstruction --record
      campaign/series/series-000-smoke-and-calibration/results/exp-044-h-023-n5-minus-w-row-jets.json
      && timeout 30 uv run --directory explorations/packing --frozen --quiet python -m
      cases.n5.minus_w_obstruction --replay
      campaign/series/series-000-smoke-and-calibration/results/exp-044-h-023-n5-minus-w-row-jets.json
    budget: >-
      one 30-minute criterion, integration, measurement, and review slice ending
      2026-08-25T18:49:44-07:00; stop on one helper bypass, missing row, unweighted
      curvature, invalid sheet witness, sampled bounded-scale limit, asserted scale case,
      coupled disposition, wrong mutation identifier, replay drift, scope promotion, or
      the phase deadline
    record: campaign/series/series-000-smoke-and-calibration/results/exp-044-h-023-n5-minus-w-row-jets.json
  results:
  - shape: determination
    question: >-
      Is canonical pure -W excluded at A, interior, and B by exact acceleration-independent
      production-row contradictions in both nearby owner branches?
    role: outcome
    outcome: invalid
    checked_by: >-
      two independent preregistration audits and one independent production-row-builder
      audit; no retained target run was opened
  - shape: determination
    question: >-
      Do the independently derived -W row-jet curvatures equal the accepted exp-036 +W
      coefficients in every case?
    role: mechanism
    outcome: no_progress
    checked_by: >-
      no sign-symmetry target was measured because the complete weighted stress, sheet,
      scale, mutation, and disposition instrument was not ready inside the frozen slice
  effort:
    timebox: one 30-minute criterion, integration, and independent-review slice
    wall_seconds: 100.41
    agent_minutes: 30
    stopped_by: guard
  complexity:
    lines_changed: 268
    new_dependencies: []
    new_failure_modes:
    - a correct generic jet can still be connected to an incomplete case-level row inventory
    - a t-squared jet alone cannot route every delta=o(t) relative-angle scale
    notes: >-
      Preregistered after exp-043's terminal invalid instrument result and after the
      case-free exact-jet helper passed source-bound tests, but before the pure -W draft
      is edited again.
  verdict:
    decision: unresolved
    primary_criterion: >-
      accept the instrument independently of the target outcome only if all six source
      cases build every production wall and selected SAT feature through exact_jets, full
      -W and arbitrary quadratic corrections reproduce the source first-order rows,
      positive Farkas weights are applied to actual row jets, an exp-034 sheet jet and a
      fixed exp-036 positive fixture pass, owner 3 mechanically exhausts bounded symbolic-real
      and unbounded abs(delta)/t^2 scales, twelve typed production mutations match only
      their expected identifiers, thirteen broader claims have individual refusal records,
      and retained generation replays identically; then report obstruction as met only if
      every case and scale route has a strict contradiction, missed if one complete owner
      branch has a compatible correction, or unresolved if none is compatible but one
      valid exact branch or scale remains undecided, with sign symmetry reported independently
    reason: >-
      The criterion and fresh-agent handoff passed two independent audits, and a new
      production builder now constructs all six exact owner-row inventories through the
      accepted helper. The slice stopped before weighted row substitution, the exp-034
      sheet evaluator, symbolic-real and unbounded scale routing, twelve mutations, or
      independent target dispositions were complete. No result JSON was written and no
      pure -W inference follows.
    reopen_when: >-
      A successor separately reviews a production stress evaluator that applies the
      exact nine-row weights to these row jets, checks the exp-034 sheet path, implements
      all five owner-3 scale records, and wires every frozen mutation and refusal before
      preregistering a new scientific target.
    resume_from: explorations/packing/cases/n5/minus_w_row_jets.py
---
# exp-044 — exact pure -W row-jet test

Exp-043 stopped before measurement because its draft combined no actual rowwise
second-order constants and did not check a full sheet acceleration witness.
The following W7 phase added a case-free exact value-gradient-Hessian engine whose tests
match the complete first-order wall and SAT inventory at A, `interior`, and B for both
owners. This round asks whether a case-level integration can now support a pure `-W`
determination without bypassing that helper.

## Frozen row-jet criterion

For every `(A, interior, B) x (owner3, owner4)` case, regenerate exp-034, exp-035,
exp-036, and exp-038. Negate all fifteen coordinates of the stored W vector.
Construct each required wall and selected SAT feature with `sqpack.research.exact_jets`,
using explicit exact feature signs and emitting both tied alternatives.
Retain each row’s value, gradient, Hessian, path-linear term, quadratic-correction
coefficient, and velocity curvature.
The keys and gradients must equal the authoritative source matrix exactly.

Apply the production positive stress weights to those same row jets.
Retain every weighted row curvature, prove all fifteen quadratic-correction columns
cancel, and derive the total curvature.
Copying exp-036’s `sqrt(2)/8`, `1/4`, or `sqrt(2)/2-1/4`, or canceling source rows
without weighting the derived quadratic terms, invalidates the run.

The exp-034 positive sheet-angle curve must supply its exact full center, angle, and
quadratic-correction jet to the same row builder.
A compatible result requires the exact 17-row A label set for each owner: the twelve
wall labels `wall:0:x-lower:+`, `wall:0:x-lower:-`, `wall:1:x-upper:+`,
`wall:1:x-upper:-`, `wall:1:y-lower:+`, `wall:1:y-lower:-`, `wall:2:x-lower:+`,
`wall:2:x-lower:-`, `wall:2:y-lower:+`, `wall:2:y-lower:-`, `wall:3:x-upper`, and
`wall:3:y-upper`; fixed contacts `contact:0-4:owner4:a-`, `contact:1-4:owner4:a-`, and
`contact:2-4:owner4:a+`; and both tied rows for the selected owner, either
`contact:3-4:owner3:a+:square4-feature+1` and `contact:3-4:owner3:a+:square4-feature-1`
or `contact:3-4:owner4:a+:square3-feature+1` and
`contact:3-4:owner4:a+:square3-feature-1`. Derive the 15-velocity and 15-correction
sheet jet from exp-034’s rational formula.
Its normalized nonzero velocity entries are `dx0=dy0=1/2` and `dtheta0=1`; its
normalized nonzero quadratic-correction entries are `dx0=dy0=-1/4`. For every expected
active row, compatibility is lexicographic: the linear coefficient is positive, or it is
zero and the quadratic coefficient is nonnegative.
A quadratic coefficient need not be nonnegative when the linear coefficient is positive.
An accepted flag, finite fixture, empty row set, or unchecked stored acceleration is
insufficient.

## Frozen owner-3 scale routing and dispositions

The owner-3 proof must split every subsequence with `delta=o(t)` into two exhaustive
cases after passing to sign-stable subsequences:

- bounded `rho=abs(delta)/t^2`, where a further subsequence has `delta/t^2 -> beta` for
  an arbitrary symbolic real `beta`; the checker must retain `beta` as a correction
  coordinate and either prove that the positive weighted coefficient of `beta`, together
  with all fifteen ordinary correction columns, is identically zero or prove the branch
  inequalities for every real `beta`; and
- unbounded `rho`, where a further subsequence has `rho -> infinity` and constant
  `sign(delta)`; the checker must derive both strict feature-branch cusp coefficients
  from production rows, divide by `abs(delta)`, and establish the contradiction sign for
  each sign branch.

Every production row uses the sense `gap >= 0`. In the bounded case, a positive weighted
combination contradicts feasibility only when its correction gradient, including the
symbolic `beta` coefficient, is zero and its velocity curvature is strictly negative.
In the unbounded case, the coefficient after normalization by `abs(delta)` must be
strictly negative for each sign branch.
A Boolean bounded/unbounded label, a sampled or `FieldElement`-restricted `beta`, or a
stored cusp constant is insufficient.

Instrument validity is independent of the target disposition.
The obstruction outcome is `criterion_met` only when all six cases and every required
scale route have strict contradictions; it is `criterion_missed` when at least one
complete owner branch has a compatible correction; it is `unresolved` when none is
compatible but at least one valid exact branch, correction, or scale route remains
undecided.
Source, row, witness, control, or replay failures invalidate the run and yield
no scientific disposition.
The sign-symmetry mechanism has its own `criterion_met` or `criterion_missed` outcome
and never gates a valid obstruction outcome.
A genuine baseline coefficient mismatch is a valid mechanism miss, not an instrument
failure.

## Frozen controls and refusals

Run an instrument-valid target baseline, whatever its valid obstruction disposition, and
a fixed exp-036 `+W` positive fixture that must reach a met obstruction through the same
production builder before running exactly twelve mutations.
Each mutation enters before certificate construction, re-enters the same builder and
validator, and passes only by matching its sole frozen failure identifier:

1. retain one `+W` center entry while negating the other fourteen input coordinates ->
   `source.minus_w`;
2. remove `interior` in source binding -> `source.strata`;
3. remove `owner4:a+` from the case inventory -> `source.owner_exhaustion`;
4. remove one actual tied row and its weight -> `source.tied_rows`;
5. omit one nonzero center-angle entry from an actual product Hessian before row
   substitution -> `jet.center_axis_cross`;
6. replace a supplied nonzero correction by zero in the shared substitution path ->
   `jet.correction_unused`;
7. flip one strict nonzero SAT feature sign supplied to `exact_jets` ->
   `jet.absolute_branch`;
8. run the zero-correction builder at `W` and `2W`, then replace the required scaled
   curvature by a copied fixed value before homogeneity validation ->
   `jet.curvature_homogeneity`;
9. perturb one production weight before applying it to row jets ->
   `certificate.weighted_curvature`;
10. change the exact sheet correction from `dx0=dy0=-1/4` to `-1/2`, making the tight
    x-lower row negative -> `control.sheet_witness`;
11. remove one actual bounded or unbounded scale handler ->
    `certificate.scale_exhaustion`; and
12. promote mixed-direction or component scope -> `scope.overclaim`.

A post-result mutation, sentinel, broad exception catcher, empty-set success, or a
mutation that claims success merely because the unmutated sign-symmetry mechanism missed
cannot pass.
A genuine unmutated mechanism mismatch remains a valid independent mechanism
disposition.

Retain exact key-set equality with these thirteen exp-043 refusals, each as its own
refusal record rather than one combined Boolean: `Ri_plus_lambda_W_plus_s`,
`other_mixed_direction`, `other_transverse_direction`, `whole_polytope_classification`,
`whole_stationary_component`, `A_to_B_stationary_connection`, `local_isolation`,
`terminality`, `quench_selection`, `basin_mass`, `census_completeness`,
`unequal_side_clearance`, and `minus_W_obstruction_from_candidate_failure`.

Acceptance would exclude only canonical pure `-W` at the three registered poses.
It would not resolve any refused claim.
Candidate or instrument failure remains distinct from a pure-direction obstruction.

## Guard result

The criterion and the repository-only resume path passed two independent audits before
target work opened. The bounded implementation slice then added a production row-jet
builder that derives every active wall and SAT feature through `exact_jets`, exposes
both tied owner alternatives, and validates exact labels and gradients against all six
authoritative source matrices.
Its 17 focused helper-and-builder tests pass, including a nonzero production
center-angle Hessian and the second-order tied-feature branch guard; Ruff and
BasedPyright are clean.

The full scientific instrument did not fit the frozen slice.
No weighted stress evaluator, exp-034 sheet-path evaluator, symbolic-real or unbounded
scale router, twelve-mutation suite, independent obstruction disposition, retained
generation, or replay was run.
No campaign result JSON was written.
This round is unresolved and provides no disposition for pure `-W`, sign symmetry, mixed
directions, connectivity, or any broader H-023 claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
