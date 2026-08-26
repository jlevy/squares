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
      rowwise curvature; an exact sheet witness; explicit owner-3 scale routing; twelve
      typed production mutations; deterministic replay; and thirteen scope refusals
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
      curvature, invalid sheet witness, asserted scale case, coupled disposition, wrong
      mutation identifier, replay drift, scope promotion, or the phase deadline
    record: campaign/series/series-000-smoke-and-calibration/results/exp-044-h-023-n5-minus-w-row-jets.json
  lease:
    expires: '2026-08-26T01:49:44Z'
    host: spud10.local
  results:
  - shape: determination
    question: >-
      Is canonical pure -W excluded at A, interior, and B by exact acceleration-independent
      production-row contradictions in both nearby owner branches?
    role: outcome
    outcome: no_progress
  - shape: determination
    question: >-
      Do the independently derived -W row-jet curvatures equal the accepted exp-036 +W
      coefficients in every case?
    role: mechanism
    outcome: no_progress
  complexity:
    lines_changed: 0
    new_dependencies: []
    new_failure_modes:
    - a correct generic jet can still be connected to an incomplete case-level row inventory
    - a t-squared jet alone cannot route every delta=o(t) relative-angle scale
    notes: >-
      Preregistered after exp-043's terminal invalid instrument result and after the
      case-free exact-jet helper passed source-bound tests, but before the pure -W draft
      is edited again.
  verdict:
    decision: in-progress
    primary_criterion: >-
      accept only if all six source cases build every production wall and selected SAT
      feature through exact_jets, full -W and arbitrary quadratic corrections reproduce
      the source first-order rows, positive Farkas weights cancel every correction column
      and combine actual rowwise quadratic terms into strict contradictions, an exp-034
      sheet jet supplies a checked compatible correction across its complete expected row
      set, owner 3 mechanically exhausts bounded and unbounded abs(delta)/t^2 scales,
      obstruction and sign-symmetry dispositions remain independent, twelve typed
      production mutations match their expected identifiers, thirteen broader claims are
      refused, and retained generation replays identically
    reason: >-
      The W7 exact-jet substrate closes exp-043's reusable algebraic blocker; the
      case-level scientific criterion is frozen separately before integration.
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
A compatible result requires the complete expected label set and exact nonnegative
second-order values.
An accepted flag, finite fixture, empty row set, or unchecked stored acceleration is
insufficient.

## Frozen owner-3 scale routing and dispositions

The owner-3 proof must split every subsequence with `delta=o(t)` into two exhaustive
cases after passing to a subsequence:

- bounded `abs(delta)/t^2`, handled by the exact tied row jets with the limiting signed
  quadratic correction retained; and
- unbounded `abs(delta)/t^2`, handled by a separately derived exact positive cusp
  margin.

The scale split, its exhaustiveness, and the sign in each branch must be executable
data, not prose or booleans.
A complete exact compatible branch makes the obstruction outcome `criterion_missed`; an
undecided exact scale or correction leaves it `unresolved`. Source, row, witness,
control, or replay failures invalidate the run and yield no scientific disposition.
The sign-symmetry mechanism is retained independently and never gates a valid
obstruction outcome.

## Frozen controls and refusals

Run a valid baseline with a met obstruction outcome before exactly twelve production
mutations. Their stable failure identifiers cover partial W negation, missing stratum,
missing owner, missing tied row, omitted center-axis cross term, ignored quadratic
correction, wrong absolute branch, copied curvature, perturbed weighted curvature,
invalid sheet witness, omitted scale case, and scope promotion.
A post-result mutation, sentinel, broad exception catcher, empty-set success, or
mechanism mismatch cannot pass.

Retain the same thirteen distinct refusals recorded by the exp-043 draft: mixed
`R_i+lambda W+s`, other mixed and transverse directions, whole-polytope and
whole-component classification, A-to-B connection, isolation, terminality, quench
selection, basin mass, census completeness, unequal-side clearance, and any pure `-W`
obstruction inferred from checker failure.

Acceptance would exclude only canonical pure `-W` at the three registered poses.
It would not resolve any refused claim.
Candidate or instrument failure remains distinct from a pure-direction obstruction.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
