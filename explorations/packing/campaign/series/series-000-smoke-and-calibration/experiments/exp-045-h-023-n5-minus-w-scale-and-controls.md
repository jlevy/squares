---
title: exp-045 — exact n = 5 pure -W scale and controls
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-045
  series: series-000
  title: Test pure -W in the frozen owner models with exact scale routing and controls
  date: '2026-08-26'
  hypotheses:
  - H-023
  tier: confirmatory
  subject:
    label: exact second-order feasibility of canonical pure -W at n = 5
    engine: n = 5 pure -W production-row checker 0.3.0
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
      exact exp-034 sheet compatibility and same-evaluator bad correction; the exp-036
      positive obstruction through the same production builder; accepted exact row,
      stress, and sheet helpers; all fifteen owner-3 scale records; twelve typed
      pre-certificate mutations; deterministic retained replay; and thirteen
      individually keyed scope refusals
    candidate: >-
      exp-043's canonical complete-vector -W at A, interior, and B, rebuilt through the
      accepted production rows and both frozen pair-(3,4) owner models without copied
      coefficients or a mathematical branch-completeness claim
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    entry_point: explorations/packing/cases/n5/minus_w_obstruction.py
    command: >-
      timeout 30 uv run --directory explorations/packing --frozen --quiet python -m
      cases.n5.minus_w_obstruction --record
      campaign/series/series-000-smoke-and-calibration/results/exp-045-h-023-n5-minus-w-scale-and-controls.json
      && timeout 30 uv run --directory explorations/packing --frozen --quiet python -m
      cases.n5.minus_w_obstruction --replay
      campaign/series/series-000-smoke-and-calibration/results/exp-045-h-023-n5-minus-w-scale-and-controls.json
    budget: >-
      BC-029 has a 105-minute W3-W6-W7-W2-W3 ceiling inside session 026. Every slice
      stops within 30 minutes. Before target execution, stop on incomplete production
      rows, stress, sheet, scale, mutation, refusal, replay, or independent-review
      coverage. Preserve a typed dependency blocker rather than create target data from
      an incomplete instrument.
    record: campaign/series/series-000-smoke-and-calibration/results/exp-045-h-023-n5-minus-w-scale-and-controls.json
  effort:
    timebox: one 105-minute W6 mini-cycle inside agenda-004 block two
    wall_seconds: 6.64
    agent_minutes: 45
    stopped_by: criterion
  results:
  - shape: determination
    question: >-
      Is canonical pure -W excluded at A, the interior, and B through the accepted
      production rows and both frozen pair-(3,4) owner models?
    role: outcome
    outcome: criterion_met
  - shape: determination
    question: >-
      Do the -W coefficients equal the separately derived +W values, so the sign symmetry
      holds through the same production builder?
    role: guard
    outcome: criterion_met
  verdict:
    decision: unresolved
    needs_review: true
    primary_criterion: >-
      report criterion_met only when every owner-4 case and all fifteen owner-3 scale
      records yield strict exact contradictions after the complete instrument passes;
      report criterion_missed when one completely evaluated declared route admits a
      compatible second-order correction; report determination no_progress and verdict
      unresolved when no compatible correction is found but a finite exact route remains
      undecided; and report invalid with no scientific disposition when a source, row,
      witness, mutation, control, or replay guard fails
    reason: >-
      The instrument is now complete and the round executed. Twelve production mutation
      paths, thirteen refusal records, six cases, and deterministic record-and-replay
      agreement all hold, and both declared determinations report criterion_met: canonical
      pure -W is excluded at A, the interior, and B, and the -W coefficients equal the
      separately derived +W values. This is recorded `unresolved` with `needs_review`
      rather than accepted, because an unattended runner may apply the accept rule only in
      the conservative direction, and because the sixth admission condition, an
      independent post-change audit of the complete instrument, has not been performed.
      Every broader claim remains refused: no whole-component identity, no A-to-B
      stationary connection, no local isolation, no terminality, and no H-023 disposition
      beyond the excluded direction.
---
# exp-045 — Exact Pure -W Scale and Controls

Exp-044 built and accepted the production row-jet substrate but stopped before it could
measure pure `-W`. This successor freezes the remaining case-level contract before
implementation. It tests only the six declared owner models and the exact owner-3 scale
partition. Exact implementation-key equality does not by itself prove that these are
every mathematical nonlinear branch.

## Execution Admission

The experiment is registered, but target execution is blocked.
The first two admitted implementation slices add the owner-3 scale perimeter and the
three-stratum owner-4 proof-data helper.
Both run only on the exp-036 `+W` control and make no pure `-W`, sign-symmetry, or H-023
disposition. An accepted execution-scoped active-row inventory now lets those two
controls share one exact row construction per field identity and stratum while every
owner view repeats authoritative key and gradient validation.

Target generation and replay remain closed until all of these hold:

- the accepted row-jet, stress, sheet, scale, and owner-4 helpers are used rather than
  the exp-043 hand-formula path;
- the same builder passes the exp-034 sheet control and the exp-036 positive
  obstruction;
- all twelve mutations enter before certificate construction and match only their frozen
  failure identifiers;
- all thirteen refusal records are individually present with claim-specific reasons;
- retained generation and replay agree; and
- an independent post-change audit accepts the complete instrument.

A missing prerequisite before target execution is a dependency blocker, not a failed
obstruction.

## Frozen Owner and Scale Inventory

The six case keys are the Cartesian product of `A`, `interior`, and `B` with `owner3`
and `owner4`. One execution-scoped inventory may construct the full production rows
through `exact_jets` once per stratum.
Each owner case must then regenerate the complete stored `-W` vector, derive a fresh
owner-specific row mapping from that inventory, independently require exact source-key
and gradient equality, apply the positive production stress, retain all fifteen
correction columns, and copy no expected exp-036 coefficient.
No inventory may cross field identities, record/replay processes, or production-input
mutations. For owner 4, all fifteen weighted correction coefficients must vanish exactly
before the sign of the constant term decides the route.

For each source stratum, owner 3 has exactly these five scale records:

- `bounded_beta_negative`
- `bounded_beta_zero`
- `bounded_beta_positive`
- `unbounded_delta_negative`
- `unbounded_delta_positive`

The three strata therefore yield exactly fifteen records.
Every record retains the normalized nine-row stress, both tied rows, and both weights.
The five keys partition scale and sign regimes; they are not five sampled values.

For bounded `abs(delta)/t^2`, retain the formal affine real expression

```text
P(a, beta) = C + sum(G_j * a_j, j=0..14) + B * beta
B = G dot d_beta
d_beta = e_theta3
```

The checker must derive and retain all fifteen `G_j` and `B` from production rows and
prove them exactly zero before the sign of `C` decides anything.
It must not represent or sample `beta` as a `FieldElement`.

For unbounded `abs(delta)/t^2`, derive `tau`, both tied-row gradients, `b_plus`,
`b_minus`, `h`, `kappa_positive`, and `kappa_negative` from current production rows.
Verify `b_plus = -(h + tau)` and `-b_minus = -(h - tau)`, and require both cusp
coefficients to be strictly negative.
Retain nuisance-column cancellation and the three normalized remainder limits
`t^2/abs(delta) -> 0`, `t*abs(delta)/abs(delta) -> 0`, and `delta^2/abs(delta) -> 0`.
Stored expected constants are not proof data.
The scale-only helper retains typed symbolic reductions from explicit, sign-stable route
premises and derives tied-row sign ownership from the production projection.
This proves only what follows if those premises hold.
Target admission still requires the driver to establish `t -> 0`, eventual `t > 0`,
`delta = o(t)`, `abs(delta)/t^2 -> infinity`, eventual nonzero `delta`, and its stable
sign for the actual route.
Neither a handler label nor a declared route premise is a contradiction certificate.

## Frozen Outcomes

After the complete instrument passes:

- `criterion_met`: all three owner-4 cases and all fifteen owner-3 scale records have
  strict exact contradictions
- `criterion_missed`: at least one completely evaluated declared route admits a
  compatible second-order correction; this does not realize a nonlinear curve or prove
  `-W` is tangent
- validly undecided: no compatible correction is found, but at least one exact route
  remains undecided; retain the finite undecided list, use determination `no_progress`,
  and set the verdict to `unresolved`
- invalid: a source, row, witness, mutation, control, or replay guard fails; use
  determination `invalid` and make no scientific disposition

The sign-symmetry mechanism receives its own met or missed determination and never gates
the obstruction outcome.

## Frozen Controls and Failures

Run an instrument-valid target baseline of any scientific disposition, the exp-034
compatible sheet witness, and the exp-036 `+W` positive obstruction before mutations.
Each mutation changes a production input or intermediate before rebuilding a fresh
certificate and must match exactly one typed exception and specific message:

1. complete-vector negation: `source.minus_w`
2. exact three-stratum inventory: `source.strata`
3. exact six-case inventory: `source.owner_exhaustion`
4. actual tied production row deletion: `source.tied_rows`
5. nonzero center-angle Hessian mutation: `jet.center_axis_cross`
6. declared-versus-applied correction mismatch: `jet.correction_unused`
7. strict SAT feature-sign mutation: `jet.absolute_branch`
8. zero-correction `W` and `2W` homogeneity mutation: `jet.curvature_homogeneity`
9. production stress-weight mutation: `certificate.weighted_curvature`
10. same-evaluator bad sheet correction: `control.sheet_witness`
11. real scale-handler deletion: `certificate.scale_exhaustion`
12. emitted claim-map promotion: `scope.overclaim`

A sentinel, broad exception catch, post-result alteration, or copied expected
coefficient cannot pass a control.

Retain these exact refusal keys as thirteen separate records with `status: refused` and
a nonempty claim-specific reason:

- `Ri_plus_lambda_W_plus_s`
- `other_mixed_direction`
- `other_transverse_direction`
- `whole_polytope_classification`
- `whole_stationary_component`
- `A_to_B_stationary_connection`
- `local_isolation`
- `terminality`
- `quench_selection`
- `basin_mass`
- `census_completeness`
- `unequal_side_clearance`
- `minus_W_obstruction_from_candidate_failure`

## Claim Boundary

Even `criterion_met` establishes only canonical pure `-W` obstruction at the three
registered poses under the justified local owner and scale inventory.
It does not establish nonlinear realization, other mixed directions, whole-component
stationarity or identity, an A-to-B stationary connection, connectivity frequency, local
isolation, terminality, quench selection, basin mass, census completeness, unequal-side
clearance, or any `n = 11` claim.
H-023 remains an open question whose bidirectional-continuation instrument is not ready.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
