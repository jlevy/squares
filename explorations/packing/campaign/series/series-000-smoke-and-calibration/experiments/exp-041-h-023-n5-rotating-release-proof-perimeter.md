---
title: exp-041 — exact n = 5 rotating-release proof perimeter
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-041
  series: series-000
  title: Close the audited proof perimeter for the six R4/R5 paths
  date: '2026-08-25'
  hypotheses:
  - H-023
  tier: confirmatory
  subject:
    label: exact fixed-side nonlinear realization of the n = 5 R4 and R5 rays
    engine: n = 5 rotating-release checker 0.2.0
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
      exact source replay and independent target fixtures; exact denominator, axis,
      wall-feature, universal-sign, stress-weight, coefficient-cancellation, control-key,
      replay, and claim-scope guards; twenty named semantic mutations; positive R3/R6
      path controls
    candidate: >-
      exp-040's frozen rational half-angle orientation and shared affine-center R4/R5
      paths, with its five independently retained proof-perimeter blockers corrected
      without changing the candidate path or claim boundary
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    entry_point: explorations/packing/cases/n5/rotating_release_paths.py
    command: >-
      timeout 30 uv run --directory explorations/packing --frozen --quiet python -m
      cases.n5.rotating_release_paths --record
      campaign/series/series-000-smoke-and-calibration/results/exp-041-h-023-n5-rotating-release-proof-perimeter.json
      && timeout 30 uv run --directory explorations/packing --frozen --quiet python -m
      cases.n5.rotating_release_paths --replay
      campaign/series/series-000-smoke-and-calibration/results/exp-041-h-023-n5-rotating-release-proof-perimeter.json
    budget: >-
      one 30-minute correction, measurement, and review slice ending
      2026-08-25T17:06:30-07:00; preserve a checkable artifact by minute twenty; stop on
      one surviving proof-perimeter blocker, missing semantic control, source drift,
      replay drift, scope promotion, or the phase deadline
    record: campaign/series/series-000-smoke-and-calibration/results/exp-041-h-023-n5-rotating-release-proof-perimeter.json
  lease:
    expires: '2026-08-26T00:06:30Z'
    host: spud10.local
  results:
  - shape: determination
    question: >-
      Do the six frozen R4/R5 paths have exact full-interval feasibility certificates,
      including distinct base-point and pathwise zero-axis inventories and derived tied
      wall-feature identities?
    role: outcome
    outcome: no_progress
  - shape: determination
    question: >-
      Do both owner branches on all six paths have exact coefficient-cancelling
      first-order stress identities whose declared multipliers stay strictly positive
      over the full interval?
    role: mechanism
    outcome: no_progress
  complexity:
    lines_changed: 0
    new_dependencies: []
    new_failure_modes:
    - a semantic control can accidentally test a sentinel instead of the production proof path
    - a combined verdict can discard a valid feasibility result when only stress remains unresolved
    notes: >-
      Preregistered before changing the exp-040 draft checker. No target result may be
      retained unless an independent review confirms every conjunct below.
  verdict:
    decision: in-progress
    primary_criterion: >-
      accept only if the exact feasibility and exact positive-stress determinations both
      meet their separately retained criteria for all six cases, the exact twenty-key
      semantic control set and positive controls pass through production proof paths,
      retained generation replays identically, and every forbidden inference is refused
    reason: >-
      The successor criterion is frozen before the retained draft checker changes or a
      target result is measured.
---
# exp-041 — exact R4/R5 rotating-release proof perimeter

Exp-040 retained a candidate checker but stopped before measurement when independent
review found five finite proof-perimeter blockers.
This round changes neither the six candidate paths nor the claim boundary.
It accepts only after the checker closes those five blockers through exact production
code and independent review.

## Frozen feasibility criterion

For each sign `sigma = -1` (R4) and `sigma = +1` (R5), and for strata A, the registered
midpoint, and B, the checker must regenerate exp-033, exp-038, and exp-039 and prove the
same source bindings, derivative representatives, center midpoint identity, walls,
pairs, owner branches, endpoint fixtures, and positive R3/R6 controls required by
exp-040. It must additionally:

- prove `D = 4 + u^2 >= 4` on `0 <= u <= U`, retain that exact certificate, and use only
  sign-equivalent numerator clearing through this denominator;
- retain two separate inventories: exactly five separating axes equal zero at `u = 0`,
  including contact `(1,4):owner4:a-`, and exactly four axes whose gap polynomial is
  identically zero throughout the path;
- factor every nonidentically-zero gap by its maximal base factor `u^k` and prove the
  residual strictly positive on the declared closed interval, so for `0 < u <= U` the
  four pathwise axes are the complete zero inventory and `(1,4):owner4:a-` is strictly
  positive;
- derive, rather than store as expected constants, both tied square-1 wall-feature
  numerators for each sign, verify the sign-to-label map, prove the selected numerator
  has residual `u + 2` after the maximal `u^2` factor, and prove the other feature adds
  the exact `4u/(4+u^2)` slack; and
- retain the universal sign proof, strict-residual facts, feature derivations, exact
  endpoint fixtures, source map, and denominator certificate in a feasibility
  certificate independent of stress.

The feasibility determination is `criterion_met` only if all six cases meet every
clause. If it meets those clauses but stress does not, the feasibility determination
remains retained as `criterion_met`; the round verdict remains unresolved.

## Frozen stress criterion

For both `(3,4)` owner branches in every case, the checker must regenerate the exact
support rows and weights frozen by exp-040. It must retain exact full-interval lower
bounds for every multiplier, including `sqrt(2)/2 - 1/4 > 0` for the smaller owner-3
tied-row weight. It must derive the cleared rational numerator degree bound from the
source rows, affine centers, and affine weights, cancel every pose-column coefficient
exactly, and retain side coefficient `sqrt(2)`.

The stress determination is `criterion_met` only if all weights are strictly positive
over the full interval and both owner identities cancel in all six cases.
Coefficient cancellation alone cannot meet this determination.

## Exact control contract

The checker must compare the control keys mechanically with one frozen set of exactly
twenty names, reject any missing or extra key, and execute a semantic mutation through
the same production proof function used by the target.
A direct sentinel exception or a boolean constant is not a control.
The twenty mutations are:

1. make the orientation non-unit;
2. swap the R4/R5 feature-sign map;
3. remove A’s slide correction;
4. add a B slide correction;
5. change square 1’s center displacement;
6. change square 4’s center displacement;
7. break the exact R3/R6 center midpoint identity;
8. omit R4;
9. omit R5;
10. omit one stratum;
11. omit one owner branch;
12. drop one tied source row or change its derived label;
13. pass `p_bad = (u-U/2)(u-U)`, whose selected samples are nonnegative but which is
    negative between them, through the universal Bernstein sign prover;
14. perturb one production sign numerator;
15. perturb one stress multiplier;
16. mutate the `(1,4):owner4:a-` identity into a false pathwise-active claim;
17. extend the interior interval beyond its first failing wall event;
18. remove one true base-point zero axis;
19. add one false pathwise zero axis; and
20. request one forbidden scope promotion.

Each control passes only when the production guard refuses the mutated certificate for
the intended semantic reason.
Independent exact target fixtures remain separate from the universal proof, and retained
generation must replay byte-for-byte as the same structured result.

## Verdict and refusal boundary

The round is accepted only when both determinations meet their frozen criteria, all
twenty semantic controls and positive controls pass, retained replay is identical, and
independent review finds no surviving proof-perimeter gap.
A proved feasibility determination without a proved stress determination is retained,
but the round ends unresolved.
Any remaining exact gap at the deadline is recorded as a smaller finite blocker list.

Acceptance would prove six explicit feasible Bouligand tangents with positive pathwise
first-order no-descent stresses.
It would not prove whole-component stationarity, connect A to B inside a stationary set,
classify a terminal or second-order local minimum, identify a maximal component, realize
`-W` or any mixed-angle direction, determine quench selection or basin mass, complete a
census, or bound unequal-side clearance.
Candidate failure is not an R4/R5 obstruction.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
