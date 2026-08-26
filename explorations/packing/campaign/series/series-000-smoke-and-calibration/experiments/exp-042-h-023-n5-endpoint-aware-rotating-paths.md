---
title: exp-042 — endpoint-aware exact n = 5 rotating paths
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-042
  series: series-000
  title: Certify the six R4/R5 paths with endpoint-aware axis inventories
  date: '2026-08-25'
  hypotheses:
  - H-023
  tier: confirmatory
  subject:
    label: exact fixed-side nonlinear realization of the n = 5 R4 and R5 rays
    engine: n = 5 rotating-release checker 0.3.0
    engine_commit: 2980fdc
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance:
    axis: n
    point: 5
    role: target
  method:
    control: >-
      passing exact baseline before mutations; typed production failure identifiers;
      case-indexed base, open-interval, and endpoint axis inventories; source replay;
      independent fixtures; derived tied features; positive multiplier and coefficient
      identities; twenty semantic mutations; positive R3/R6 paths; deterministic replay
    candidate: >-
      exp-040's unchanged six rational half-angle and affine-center R4/R5 paths, with
      exp-041's exact endpoint-only axis fact and three surviving instrument guards
      corrected without changing the path, interval, source map, stress support, or claim
      boundary
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: 2980fdc
    dirty: false
    entry_point: explorations/packing/cases/n5/rotating_release_paths.py
    command: >-
      timeout 30 uv run --directory explorations/packing --frozen --quiet python -m
      cases.n5.rotating_release_paths --record
      campaign/series/series-000-smoke-and-calibration/results/exp-042-h-023-n5-endpoint-aware-rotating-paths.json
      && timeout 30 uv run --directory explorations/packing --frozen --quiet python -m
      cases.n5.rotating_release_paths --replay
      campaign/series/series-000-smoke-and-calibration/results/exp-042-h-023-n5-endpoint-aware-rotating-paths.json
    budget: >-
      one 30-minute preregistration, correction, measurement, and review slice ending
      2026-08-25T17:28:09-07:00; preserve a checkable artifact by minute twenty; stop on
      a failing baseline, an unclassified root, a wrong mutation failure identifier, a
      sentinel tied-row control, coupled partial results, replay drift, scope promotion,
      or the phase deadline
    record: campaign/series/series-000-smoke-and-calibration/results/exp-042-h-023-n5-endpoint-aware-rotating-paths.json
  results:
  - shape: determination
    question: >-
      Do all six unchanged R4/R5 paths have exact universal feasibility certificates
      with complete base, open-interval, and positive-endpoint zero-axis inventories?
    role: outcome
    outcome: criterion_met
    checked_by: >-
      exact retained generation and replay, case-indexed exhaustion of 240 owner-axis
      polynomials, independent endpoint-inventory review, and twenty semantic controls
  - shape: determination
    question: >-
      Do both owner branches on all six paths have independently executable exact
      positive first-order stress certificates that cannot erase a feasibility result?
    role: mechanism
    outcome: criterion_met
    checked_by: >-
      exact retained generation and replay, independent owner-system and partial-result
      review, coefficient cancellation on both branches in six cases, and a stress-only
      mutation that preserved the successful feasibility result
  effort:
    timebox: one 30-minute correction, measurement, and independent-review slice
    wall_seconds: 26.17
    agent_minutes: 28
    stopped_by: criterion
  complexity:
    lines_changed: 516
    new_dependencies: []
    new_failure_modes:
    - an endpoint factor can be lost by treating all nonpersistent axes as closed-interval strict
    - one baseline exception can shadow the intended failure reason of every mutation
    notes: >-
      Preregistered after exp-041's terminal endpoint result and before any further
      checker edit. The exact path, interval, sources, stresses, and claim boundary remain
      unchanged. The retained checker correction and both measurements ran from clean
      engine commit 2980fdc.
  verdict:
    decision: accepted
    primary_criterion: >-
      accept only if independently executed feasibility and stress determinations both
      meet their exact six-case criteria, the endpoint-aware inventories and root
      multiplicities regenerate case by case, a passing baseline precedes twenty
      production-path mutations with exact expected failure identifiers, a stress-only
      control retains successful feasibility, positive controls pass, replay is
      identical, and every forbidden inference is refused
    reason: >-
      All six unchanged paths have exact universal feasibility certificates with the
      frozen base, open-interval, and endpoint inventories, and both owner branches have
      exact positive first-order stress certificates. Generation and replay agree, all
      twenty production-path controls reject with their expected identifiers, and the
      stress-only control retains feasibility while making the combined verdict
      unresolved. The result is pathwise only and refuses every broader H-023 claim.
    commit: 2980fdc
---
# exp-042 — accepted endpoint-aware exact R4/R5 rotating paths

Exp-041 found that one nonpersistent owner axis becomes zero exactly at the positive
endpoint of every frozen path.
That fact does not harm feasibility, but it falsified the round’s claimed pointwise
inventory.
Exp-042 keeps the six paths and all mathematical claims unchanged while making
endpoint roots and partial dispositions explicit.

## Frozen feasibility criterion

For every case in `(R4, R5) x (A, midpoint, B)`, regenerate the exact exp-033, exp-038,
and exp-039 source maps, derivatives, R3/R6 center midpoint identity, rational
half-angle unit identity, denominator certificate, universal wall and pair table,
derived tied square-1 feature numerators, independent exact fixtures, and positive path
controls required by exp-041.

Derive all forty owner-axis gap polynomials separately in each case.
For every nonidentically-zero polynomial, divide by its maximal base factor `u^k` and
maximal endpoint factor `(U-u)^l`, choose its exact fixed sign, and prove the remaining
residual strictly positive on the full closed interval.
Retain `k`, `l`, the signed residual, and its exact positivity certificate.
This must prove that every case has exactly:

- base zeros at `u = 0`: `0-4:owner4:a-`, `1-4:owner4:a-`, `2-4:owner4:a+`,
  `3-4:owner3:a+`, and `3-4:owner4:a+`;
- persistent zeros for `0 < u < U`: `0-4:owner4:a-`, `2-4:owner4:a+`, `3-4:owner3:a+`,
  and `3-4:owner4:a+`; and
- endpoint zeros at `u = U`: `0-3:owner3:a-` plus those four persistent axes.

The closed-path union therefore has six labels, but no point has six simultaneous zero
axes.
The endpoint-only cleared polynomial must regenerate as `(sqrt(2)/2)(u^2+4)^2(u-U)`
with endpoint multiplicity one.
Counts or one shared constant cannot replace six case-indexed derived inventories.

The feasibility determination executes and serializes independently.
It is `criterion_met` only when all six cases meet every clause.
An exact inventory mismatch is `criterion_missed` for this round, not a ray obstruction.
An undecided root, multiplicity, sign, source, or fixture leaves feasibility unresolved
with the finite case list.

## Frozen stress and partial-result criterion

Regenerate both `(3,4)` owner systems for every case from the production row builder,
derive the exact tied-row labels, retain every multiplier’s exact full-interval positive
lower bound, derive the cleared numerator degree bound, cancel every pose coefficient,
and retain side coefficient `sqrt(2)`. Execute and serialize this determination
independently of feasibility.

The perturbed-stress control must create a stress-only failure after a successful
feasibility run.
The retained control result must show feasibility still `criterion_met`,
stress non-met with its exact failure identifier, and the combined verdict unresolved.
Any exception path that discards or relabels successful feasibility fails the round.

## Frozen control criterion

Run the unmutated baseline first and require both determinations to meet their criteria
before executing controls.
Keep the exact twenty-key set frozen by exp-041. Every mutation record must name its
expected stable failure identifier, invoke the same production builder and validator as
the target, and pass only when its actual identifier equals the expected one.
Catching any `ValueError` or `TypeError`, failing before the mutation reaches its target
invariant, or returning a boolean sentinel fails the control.

The tied-feature mutation must remove one actual `(3,4)` tied row from production row
construction and be rejected by exact row-label or completeness validation.
It may not branch to a direct “missing feature” exception before construction.
The anti-sampling polynomial still passes through the production Bernstein prover.
The midpoint, numerator, stress, zero-axis, case, owner, feature, and scope controls
must likewise mutate their production data and match their declared failure identifiers.

## Verdict and refusal boundary

The round is accepted only when both independent determinations meet their frozen
criteria, the passing baseline and twenty identifier-specific controls pass, retained
generation replays identically, and independent review finds no omitted case, root, row,
weight, or scope refusal.
Feasibility meeting its criterion while stress is missed or unresolved is retained as a
partial result and leaves the round unresolved.

Acceptance would prove six explicit feasible Bouligand tangents with positive pathwise
first-order no-descent stresses.
It would not prove an A-to-B stationary connection, whole-polytope or whole-component
stationarity, terminal or second-order local minimality, maximal component identity,
exhaustive nonlinear R4/R5 realization, `-W` or mixed-direction realization, quench
selection, basin mass, census completeness, or unequal-side clearance.
Candidate failure remains distinct from an R4/R5 obstruction.

## Result

The frozen criterion is met.
Retained generation completed in 12.67 seconds and exact replay completed in 13.50
seconds. All six `(R4, R5) x (A, midpoint, B)` feasibility certificates and all six
two-owner stress certificates pass, and all twenty semantic controls reject with their
preregistered failure identifiers.

Every case has five base zeros, four persistent open-interval zeros, and five positive
endpoint zeros. The base-only `(1,4)` axis has multiplicity two; the endpoint-only
`0-3:owner3:a-` axis has multiplicity one and cleared factor
`(sqrt(2)/2)(u^2+4)^2(u-U)`. The stress-only control keeps feasibility `criterion_met`,
records `stress.pose_identity`, and leaves the combined determination unresolved.

This certifies six explicit feasible Bouligand tangents with positive pathwise
first-order no-descent stresses.
It does not promote any of the refused connection, component, second-order, `-W`,
mixed-direction, quench, basin, census, or unequal-side claims.

The retained
[`exp-042-h-023-n5-endpoint-aware-rotating-paths.json`](../results/exp-042-h-023-n5-endpoint-aware-rotating-paths.json)
contains the case certificates, determinations, controls, refusal set, and replayable
source receipt.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
