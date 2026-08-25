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
    engine_commit: 199de54
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
    commit: 199de54
    dirty: false
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
  lease:
    expires: '2026-08-25T23:41:44Z'
    host: local
  results:
  - shape: determination
    question: >-
      Do explicit exact fixed-side one-sided families realize the canonical R4 and R5
      representatives at A, the registered midpoint, and B, and do those six paths
      retain positive branchwise first-order no-descent stresses?
    role: outcome
    outcome: no_progress
    checked_by: Target execution has not started; this result is a preregistration placeholder.
  verdict:
    decision: in-progress
    primary_criterion: >-
      bind the six derivatives exactly to exp-038, including A's slide correction; prove
      every wall and pair feasible over the full interval by exact rational-polynomial
      signs with all owner and tied-feature cases present; pass independent exact
      fixtures; regenerate positive stresses for both owner branches; replay identically;
      reject every declared control; and refuse component, terminal, second-order, -W,
      mixed-angle, basin, census, and unequal-side claims
    reason: >-
      The exact six-case criterion is frozen before target execution; no target result
      has yet been measured.
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
derivative at zero is `sigma`. Move the centers affinely by the shared positional part
of R4 and R5:

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
- rebuild both active owner branches for contact `(3,4)`, retain both tied feature rows
  in each branch, and cancel the exact stress identity with strictly positive
  multipliers over the interval; and
- regenerate and replay the retained record identically.

Two nonlinear margins are mandatory fixtures for the universal proof.
Square 1’s selected upper-x and lower-y features acquire slack

`u^2(u+2)/(2(4+u^2)) > 0`,

and contact `(1,4)` acquires owner-4 `a-` slack

`r u^2/(4+u^2) > 0`.

The controls must reject a sign-label swap, a missing A slide or added B slide, a
changed square-4 displacement, omission of either sign, stratum, owner branch, or tied
feature, promotion of a sampled fixture to a universal proof, a perturbed numerator or
stress multiplier, a false claim that either mandatory slack stays active, an overlong
interior interval, and any forbidden scope promotion.
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
A true obstruction would require a separately preregistered exhaustive second-order-jet
argument over every nearby owner and feature branch.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
