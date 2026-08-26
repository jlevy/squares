---
title: exp-043 — exact n = 5 pure -W second-order test
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-043
  series: series-000
  title: Test the canonical pure -W direction by exact branchwise second order
  date: '2026-08-25'
  hypotheses:
  - H-023
  tier: exploratory
  subject:
    label: exact second-order feasibility of the canonical pure -W direction at n = 5
    engine: n = 5 pure -W obstruction checker 0.1.0
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
      exact exp-034, exp-035, exp-036, and exp-038 source binding; complete owner-axis
      and tied-row exhaustion; a realized sheet-curve anti-overobstruction control; deterministic
      replay; and eight typed direction, owner, row, coefficient, stratum, realized-ray,
      and scope mutations
    candidate: >-
      the exact sign reversal of exp-038's normalized W at A, the registered midpoint,
      and B, tested against both nearby pair (3,4) owner-axis branches without assuming
      that exp-036's +W coefficients are sign-even
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    entry_point: explorations/packing/cases/n5/minus_w_obstruction.py
    command: >-
      timeout 30 uv run --directory explorations/packing --frozen --quiet python -m
      cases.n5.minus_w_obstruction --record
      campaign/series/series-000-smoke-and-calibration/results/exp-043-h-023-n5-minus-w-obstruction.json
      && timeout 30 uv run --directory explorations/packing --frozen --quiet python -m
      cases.n5.minus_w_obstruction --replay
      campaign/series/series-000-smoke-and-calibration/results/exp-043-h-023-n5-minus-w-obstruction.json
    budget: >-
      one 30-minute preregistration, implementation, measurement, and review slice ending
      2026-08-25T17:59:27-07:00; preserve an exact branch record by minute twenty; stop
      on source drift, an incomplete owner or tied-row inventory, a falsely obstructed
      realized ray, an unclassified coefficient, replay drift, scope promotion, or the
      phase deadline
    record: campaign/series/series-000-smoke-and-calibration/results/exp-043-h-023-n5-minus-w-obstruction.json
  results:
  - shape: determination
    question: >-
      Is the canonical pure -W direction excluded from the true fixed-side Bouligand
      tangent cone at A, the source stratum labelled interior, and B by an exact
      acceleration-independent second-order contradiction in every nearby owner branch?
    role: outcome
    outcome: invalid
    checked_by: >-
      two independent post-change audits after bounded temporary generation and replay
  - shape: determination
    question: >-
      Do the derived -W contradictions equal exp-036's exact +W coefficients in every
      stratum-owner case?
    role: mechanism
    outcome: no_progress
    checked_by: >-
      the sign-symmetry result was not measured because the draft evaluator made it true
      by construction instead of deriving rowwise second-order constants
  effort:
    timebox: one 30-minute preregistration, implementation, and independent-review slice
    wall_seconds: 3.071
    agent_minutes: 20
    stopped_by: guard
  complexity:
    lines_changed: 596
    new_dependencies: []
    new_failure_modes:
    - a sign-even width expansion can hide sign-odd center or separating-axis terms
    - an obstruction helper can falsely reject a known realized release direction
    notes: >-
      The draft checker is retained as a resume point, but no campaign result JSON was
      accepted because independent review found that its green temporary run did not
      execute the frozen second-order instrument.
  verdict:
    decision: unresolved
    primary_criterion: >-
      accept only if the checker derives -W by exact negation of exp-038's stored W,
      proves it first-order tight at all three source strata, exhausts both nearby owner
      axes and all tied rows, eliminates arbitrary second-order corrections and derives a
      strict exact contradiction in all six stratum-owner cases, refuses every broader
      claim, leaves exp-034's realized sheet curve unobstructed, rejects eight typed
      semantic mutations with their expected identifiers, and replays identically; the
      equality of -W and +W coefficients is retained as a separate mechanism result and
      is not required for an accepted obstruction verdict
    reason: >-
      Temporary generation and replay passed, but independent review found that the
      evaluator ignored center velocities in its second-order constants, combined no
      production rowwise curvatures, supplied no checked sheet acceleration witness, and
      asserted rather than proved the owner-3 two-scale routing. No target result was
      retained and no -W disposition follows.
    reopen_when: >-
      A successor builds a shared exact truncated-series wall and SAT engine, feeds full
      center, angle, and acceleration jets for plus or minus W and the exp-034 sheet
      curve through it, retains rowwise second-order constants and their weighted sum,
      and mechanically routes the delta=o(t) scale split and scientific dispositions.
    resume_from: explorations/packing/cases/n5/minus_w_obstruction.py
---
# exp-043 — exact pure -W second-order test

Exp-038 proves that `W` is lineality in every branchwise linearization cone and records
its exact normalized coordinates.
Exp-036 excludes the `+W` orientation from the true Bouligand tangent cone at A, the
registered midpoint, and B. Neither result classifies the opposite orientation.
This round tests only the canonical `-W` vector obtained by negating the retained
exp-038 coordinates.

Throughout this round, “midpoint” means the source stratum labelled `interior` in
exp-035 and exp-038. Retained records and code must use `interior`.

Write `r = sqrt(2)`, `S = 1 + 5r/4`, and `w_i = cos(theta_i) + sin(theta_i)`. For
`t -> 0+`, a sequence normalized to `-W` has

```text
theta_3 = pi/4 - t + o(t)
theta_4 = pi/4 - t + o(t)
w_i = r - (r/2)t^2 + o(t^2)
delta = theta_3 - theta_4 = o(t).
```

The checker must negate the complete stored W vector, including its center and angle
coordinates, rather than reconstructing an angle-only surrogate.
It must regenerate the exp-035 and exp-038 source poses, active rows, zero-axis
inventories, and both pair `(3,4)` owner branches at A, the midpoint, and B. Both tied
support rows remain a conjunction.
It must prove the exact `-W` vector is first-order tight in every regenerated branch
before using any second-order statement.

## Frozen obstruction criterion

For each of the six `(A, midpoint, B) x (owner3, owner4)` cases, derive the complete
second-order necessary inequality from the sign-reversed center and angle expansion.
Each branch proof must quantify over and eliminate arbitrary second-order center
corrections, arbitrary `o(t)` angle corrections, and feasible subsequences.
It must retain an acceleration-independent necessary inequality or equivalent exact
Farkas certificate; expanding one chosen center path is insufficient to exclude a
Bouligand tangent. No coefficient may be copied from exp-036 as an expected constant.
The separate sign-symmetry mechanism predicts:

- owner 4 has exact positive excess coefficient `sqrt(2)/8`;
- owner 3 has exact obstruction coefficient `1/4`; and
- the relative-angle cusp has exact positive margin `sqrt(2)/2 - 1/4`.

The obstruction outcome is `criterion_met` when every case has any strict exact
acceleration-independent contradiction.
The mechanism is `criterion_met` only when the three predicted values are separately
derived in all six cases.
A different strict contradiction can therefore accept the obstruction outcome while
missing the sign-symmetry mechanism.
If any complete exact branch admits a compatible second-order correction, the
obstruction criterion is missed; that does not realize `-W`. With a complete valid
source and branch inventory, an undecided exact sign or correction elimination leaves
the outcome unresolved with the finite case list.

Source drift, an omitted production row or branch, a failed realized-curve oracle, a
wrong mutation identifier, or replay drift invalidates the run and yields no scientific
disposition. Those validity failures are not `unresolved` outcomes.

## Frozen controls

Run a valid unmutated baseline whose obstruction outcome is `criterion_met` before
controls; the independent sign-symmetry mechanism may be met, missed, or unresolved.
Retain exactly eight semantic mutations, each through the same source builder and
validator and each with a stable expected failure identifier:

1. negate only `dtheta3` and `dtheta4` while retaining the `+W` center entries and fail
   `source.minus_w`;
2. remove one owner branch and fail `source.owner_exhaustion`;
3. remove one actual tied support row and fail `source.tied_rows`;
4. replace the production width second-order term `-sqrt(2)/2` by `+sqrt(2)/2` before
   owner-4 elimination, destroy its strict contradiction, and fail
   `certificate.owner4_sign`;
5. add `1/2` to the production owner-3 upper-bound second-order wall term before
   elimination, destroy its strict contradiction, and fail `certificate.owner3_sign`;
6. omit the midpoint and fail `source.strata`;
7. claim the known exp-034 sheet-angle curve is obstructed and fail
   `control.realized_direction`; and
8. promote the scope to mixed-direction or component obstruction and fail
   `scope.overclaim`.

The realized-direction control must send exp-034’s exact sheet-angle center, row, and
angle expansions through the same generic necessary-inequality evaluator and retain a
compatible, no-contradiction certificate before a mutation tries to relabel it.
Checking only exp-034’s accepted flag, rejecting it because it is not `-W`, or branching
to a sentinel is insufficient.
Exp-036’s accepted `+W` record is a positive obstruction control, not a substitute for
deriving `-W`. Coefficient mutations alter production inputs before derivation; changing
a derived coefficient or expected constant afterward fails the control criterion.
Catching an undifferentiated exception likewise fails it.

## Verdict and refusal boundary

The round is accepted only after retained generation and exact replay agree, all six
branch certificates give strict acceleration-independent contradictions, the realized
sheet-curve control stays unobstructed, all eight typed mutations fail for their
declared reasons, and independent review finds no omitted row, correction, branch, sign,
source, or refusal. The coefficient-equality mechanism is reported independently.
Neither sign-destruction control may pass because the unmutated sign-symmetry mechanism
already missed; each must compare the mutated obstruction sign with the valid unmutated
outcome through the production evaluator.

Acceptance would exclude only the canonical pure `-W` direction from the fixed-side
Bouligand tangent cone at the three registered poses.
It would not classify `R_i + lambda W + s`, any other mixed or transverse direction, the
whole polytope or stationary component, an A-to-B stationary connection, local isolation
or terminality, quench selection, basin mass, census completeness, or unequal-side
clearance. Candidate-checker failure is not a `-W` obstruction.

## Guard result

The scientific instrument guard fired before retained target measurement.
Temporary generation completed in 1.709 seconds and replay in 1.362 seconds, but those
green runs do not meet the frozen criterion.
Two independent reviews found five finite defects:

- the evaluator has no production rowwise second-order wall or SAT jets;
- center velocities enter only first-order checks, while hand-written angle-squared
  formulas make `+W` and `-W` certificates identical by construction;
- the positive Farkas weights cancel linear correction columns but are never applied to
  derived rowwise nonlinear constants;
- the exp-034 control does not feed a full exact center, angle, and acceleration witness
  through the shared evaluator; and
- the owner-3 `delta=o(t)` two-scale argument is asserted rather than mechanically
  routed.

No campaign result JSON was written.
This round is unresolved and retains no scientific disposition for pure `-W`,
coefficient sign symmetry, mixed directions, connectivity, or any broader H-023 claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
