---
title: exp-040 — exact n = 5 rotating R4/R5 release paths
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-040
  series: series-000
  title: Classify the six canonical R4/R5 rotating release cases
  date: '2026-08-25'
  hypotheses:
  - H-023
  tier: confirmatory
  subject:
    label: exact fixed-side nonlinear realization of the n = 5 R4 and R5 rays
    engine: n = 5 rotating-release checker 0.1.0
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
      exact exp-033, exp-038, and exp-039 source replay; direct checks of both signs,
      all three strata, both owner branches, and every tied feature; independent exact
      fixtures; and source-map, interval, axis, stress, and scope mutations
    candidate: >-
      one rational half-angle orientation with the common R4/R5 center path, a universal
      exact wall and separating-axis proof over the declared interval, and regenerated
      positive branchwise first-order stresses
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    entry_point: explorations/packing/cases/n5/rotating_release_paths.py
    command: >-
      timeout 30 uv run --directory explorations/packing --frozen --quiet python -m
      cases.n5.rotating_release_paths --record
      campaign/series/series-000-smoke-and-calibration/results/exp-040-h-023-n5-rotating-release-paths.json
      && timeout 30 uv run --directory explorations/packing --frozen --quiet python -m
      cases.n5.rotating_release_paths --replay
      campaign/series/series-000-smoke-and-calibration/results/exp-040-h-023-n5-rotating-release-paths.json
    budget: >-
      one 30-minute criterion and implementation slice; separate 30-second generation
      and replay caps; stop on source drift, one missing sign, stratum, owner, tied
      feature, wall, or pair, one undecided exact numerator, a failed control, scope
      promotion, or retained-record drift
    record: campaign/series/series-000-smoke-and-calibration/results/exp-040-h-023-n5-rotating-release-paths.json
  results:
  - shape: determination
    question: >-
      Do explicit exact fixed-side one-sided families realize the canonical R4 and R5
      representatives at A, the registered midpoint, and B, and do those six paths
      retain positive branchwise first-order no-descent stresses?
    role: outcome
    outcome: invalid
    checked_by: independent proof-perimeter review after bounded temporary generation and replay
  - shape: determination
    question: >-
      Did the draft checker independently establish the six feasible Bouligand
      continuations even if its stronger stress claim remained unresolved?
    role: mechanism
    outcome: no_progress
    checked_by: >-
      independent review found that open-interval strictness and tied-feature identities
      were asserted rather than derived, so no partial feasibility verdict was retained
  effort:
    timebox: 30m criterion, implementation, and independent-review slice
    wall_seconds: 12
    agent_minutes: 30
    stopped_by: guard
  complexity:
    lines_changed: 711
    new_dependencies: []
    new_failure_modes:
    - an identically-zero path axis can be confused with an axis active only at the base point
    - stress cancellation can pass without proving every multiplier stays positive
    - hard-coded feature labels can survive without a regenerated tied-feature identity
    notes: >-
      The draft checker is retained as the resume point, but no campaign result JSON was
      accepted because the independent guard fired before retained measurement.
  verdict:
    decision: unresolved
    primary_criterion: >-
      bind the six derivatives exactly to exp-038, including A's slide correction; prove
      every wall and pair feasible over the full interval by exact rational-polynomial
      signs with all owner and tied-feature cases present; pass independent exact
      fixtures; exhaust the exact zero-axis inventory; regenerate and cancel positive
      stress identities for both owner branches; replay identically; reject all twenty
      named controls; and refuse component, terminal, second-order, -W, mixed-angle,
      basin, census, and unequal-side claims
    reason: >-
      Temporary generation and replay passed, but independent review found five finite
      proof-perimeter gaps before any retained target result was accepted.
    reopen_when: >-
      A successor round derives pointwise and identically-zero axis inventories,
      full-interval multiplier positivity, tied wall-feature numerators, true semantic
      controls including the anti-sampling polynomial, and separate feasibility and
      stress determinations.
    resume_from: explorations/packing/cases/n5/rotating_release_paths.py
---
# exp-040 — preregistered exact R4/R5 rotating release paths

Exp-038 leaves six transverse release rays after quotienting the certified sheet.
Exp-039 realizes R1, R2, R3, and R6 on exact fixed-angle paths.
This round asks only whether explicit nonlinear paths realize the two remaining
canonical rays, R4 and R5, at the three registered strata.

Let `r = sqrt(2)`, `delta = 3r/2 - 2`, and `0 <= u <= delta/2`. For `sigma = -1` (R4) or
`sigma = +1` (R5), orient square 1 by the exact axes

```text
c = (4-u^2)/(4+u^2)
s = sigma 4u/(4+u^2)
(c,s), (-s,c).
```

Thus its angle is represented algebraically without storing `atan`, while its angular
derivative at zero is `sigma`. The checker must prove `c^2+s^2 = 1` identically and
prove the exact feature-sign guards needed to keep every absolute-value branch fixed on
the full interval. Move the centers affinely by the shared positional part of R4 and R5:

```text
A:        dy0 = +u
interior: dx0 = -u
B:        dx0 = -u
all:      dx1 = -u/2, dy1 = +u/2, dx4 = -u/2, dy4 = +u/2.
```

All omitted center coordinates and all other orientations remain fixed.
At zero, the derivative must equal exp-038’s stored R4 or R5 representative exactly; at
A this includes its recorded sheet-slide correction.
The center path must also equal the pointwise midpoint of exp-039’s R3 and R6 center
paths, not merely share its first derivative.

Acceptance is conjunctive over both signs and all three strata.
For each of those six cases, the checker must:

- replay the exact exp-033, exp-038, and exp-039 sources and their canonical map;
- prove the full interval feasible by exhausting every container wall and every square
  pair, using all relevant SAT owner axes and tied support features rather than sampled
  fixtures;
- clear the positive denominator `4+u^2` and retain the finite numerator sign table;
- prove independently checked exact packings at `u = delta/4` and `u = delta/2`;
- prove that the full zero separating-axis inventory contains exactly `(0,4):owner4:a-`,
  `(2,4):owner4:a+`, `(3,4):owner3:a+`, and `(3,4):owner4:a+` throughout each path, with
  no missing or extra zero axis;
- rebuild both active owner branches for contact `(3,4)`, retain both tied feature rows
  in each branch, and cancel every exact coefficient of the resulting rational stress
  identity with strictly positive multipliers over the interval; and
- regenerate and replay the retained record identically.

Two nonlinear margins are mandatory fixtures for the universal proof.
Square 1’s selected upper-x and lower-y features have slack

`u^2(u+2)/(2(4+u^2)) >= 0`,

and contact `(1,4)` has owner-4 `a-` slack

`r u^2/(4+u^2) >= 0`.

Both are zero at `u = 0` and must be proved strictly positive for `0 < u <= delta/2`.
For R5, the small nonlinear wall slack belongs to the `x-upper:-` and `y-lower:-`
features while the `+` features open at first order; for R4 those roles reverse.
The checker must retain that exact sign-to-feature map, including the other feature’s
additional slack `4u/(4+u^2)`.

The stress support and weights are frozen before measurement.
Square 2’s four lower-wall rows have weight `r/4`, square 3’s two upper-wall rows have
weight `r/2`, and contact `(2,4)` has weight one.
On the owner-3 branch for contact `(3,4)`, the tied-row weights are

```text
w+ = 5/4 - r(1+u)/2
w- = -1/4 + r(1+u)/2.
```

On the owner-4 branch both tied-row weights are `1/2`. The checker must prove each
weight strictly positive, with owner-3 lower bound `r/2 - 1/4 > 0`; derive the rational
numerator degree bound from the source rows, affine centers, and these affine weights;
and cancel every pose-column numerator coefficient while retaining side coefficient `r`.
Fixtures at finitely many `u` values are not this identity proof.

Exactly twenty controls must reject: a non-unit orientation formula; an R4/R5 sign-label
swap; a missing A slide; an added B slide; a changed square-1 center displacement; a
changed square-4 displacement; a false R3/R6 midpoint identity; omission of R4; omission
of R5; omission of one stratum; omission of one owner branch; omission of one tied
feature; promotion of sampled fixtures to a universal proof; a perturbed sign numerator;
a perturbed stress multiplier; a false claim that either mandatory slack remains active;
an overlong interior interval; a missing zero axis; a false extra zero axis; and any
forbidden scope promotion.
Positive controls replay exp-039’s R3 and R6 paths through the independent exact packing
checker.

An accepted result would prove six explicit feasible Bouligand tangents and pathwise
first-order no descent only.
It would not connect A to B inside the stationary set, classify the whole polytope,
prove a terminal or second-order local minimum, identify a maximal component, realize
`-W` or a mixed direction, determine quench selection or basin mass, complete a census,
or bound unequal-side clearance.

Failure of this candidate path is not an obstruction to R4 or R5. If any exact sign or
branch remains undecided at the phase deadline, the round must retain the finite case
and numerator list and end unresolved.
A proved six-case feasible continuation is retained as its own determination even if the
stronger stress determination remains unresolved; only both determinations together can
accept this round.
A true obstruction would require a separately preregistered exhaustive
second-order-jet argument over every nearby owner and feature branch.

## Checkpoint result

The 30-minute slice stopped on its independent-review guard.
The draft checker generated six cases and twenty passing control booleans in about six
seconds, then replayed the temporary record identically in about six seconds.
That is implementation progress, not an accepted scientific result.

Two independent reviews retained five finite blockers:

1. Distinguish the four axes that are identically zero along each path from the five
   axes active at `u = 0`; prove every other residual strictly positive on the
   appropriate open or closed interval.
2. Prove and retain every stress multiplier’s full-interval positivity, not just the
   exact coefficient cancellation.
3. Derive both tied square-1 wall-feature numerators and their sign-to-label map instead
   of storing the expected labels as constants.
4. Split feasibility and stress certificates so a future proved Bouligand continuation
   survives even if the stress extension does not.
5. Make the exact twenty-control key set a guard and replace sentinel failures with
   semantic mutations, including the sample-deceptive polynomial passed through the same
   universal prover; also retain the exact positive-denominator certificate.

No retained result JSON was written, no obstruction was inferred, and none of the
forbidden component, terminal, basin, census, or unequal-side claims changed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
