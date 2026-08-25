---
title: exp-038 — exact n = 5 fixed-angle optimal-position polytope
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-038
  series: series-000
  title: Certify the five-dimensional fixed-angle face containing four release classes
  date: '2026-08-25'
  hypotheses: [H-023]
  tier: confirmatory
  subject:
    label: exact fixed-angle common-cell optimal-position polytope at n = 5
    engine: n = 5 fixed-angle polytope checker 0.1.0
    precision: exact
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: false
  instance: {axis: n, point: 5, role: target}
  method:
    control: >-
      exact exp-033, exp-034, and exp-037 semantic bindings; independent exact packing
      verification; and ten normalization, transport, interval, inequality, dual,
      stress, branch, active-axis, and overclaim mutations
    candidate: >-
      exact elimination of the 30-row common cell to a five-coordinate polytope, a
      rank-six fixed-angle LP dual support, twelve affine release paths, and positive
      owner-branch first-order stresses along those paths
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    entry_point: explorations/packing/cases/n5/fixed_angle_polytope.py
    command: >-
      timeout 30 uv run --directory explorations/packing --frozen --quiet python
      -m cases.n5.fixed_angle_polytope --record
      campaign/series/series-000-smoke-and-calibration/results/exp-038-h-023-n5-fixed-angle-polytope.json
      && timeout 30 uv run --directory explorations/packing --frozen --quiet python
      -m cases.n5.fixed_angle_polytope --replay
      campaign/series/series-000-smoke-and-calibration/results/exp-038-h-023-n5-fixed-angle-polytope.json
    budget: >-
      one 30-minute implementation and measurement slice; separate 30-second generation
      and replay caps; stop on source drift, an inequivalent eliminated domain, a failed
      exact packing, a nonpositive stress, a surviving control, or retained-record drift
    record: campaign/series/series-000-smoke-and-calibration/results/exp-038-h-023-n5-fixed-angle-polytope.json
  lease:
    expires: '2026-08-25T09:30:00Z'
  results:
  - shape: determination
    question: >-
      Do the four fixed-angle release classes R1, R2, R3, and R6 lie in one connected
      five-dimensional common-cell polytope of exact side-optimal positions, and do their
      declared paths have positive branchwise first-order no-descent stresses?
    role: outcome
    outcome: no_progress
    checked_by: preregistered but not yet run
  verdict:
    decision: in-progress
    primary_criterion: >-
      bind exp-033, exp-034, and exp-037 exactly, including the canonical-ray
      normalization; prove that all 30 common-cell inequalities are equivalent to the
      declared bounded five-coordinate polytope; prove its affine dimension is five
      using six affinely independent feasible points and prove its LP dual fixes side
      1+5sqrt(2)/4; retain the twelve exact R1, R2, R3, and R6 paths with sharp
      stratum-specific intervals; independently verify endpoint and interior packings;
      rebuild every active owner branch and tied row and prove both branchwise stress
      identities, strict multiplier positivity, and active-axis exhaustion along every
      path; replay identically; reject all ten executable controls; and refuse global,
      second-order, quench-terminal, maximal-component, R4, R5, -W, mixed-angle, basin,
      census, and unequal-side claims
    reason: >-
      The exact formulas were discovered independently after exp-037. This confirmatory
      criterion and its refusal boundary are frozen before target implementation or a
      retained result.
---
# exp-038 — preregistered fixed-angle optimal-position polytope

Exp-037 certifies the complete branchwise linearization-cone inventory but makes no
nonlinear continuation claim.
A separate exact derivation found a stronger fixed-angle candidate than twelve isolated
fixtures: four release classes appear to lie in one five-dimensional connected
common-cell polytope.
This is discovery evidence only.
The round is confirmatory and must rebuild the result from the exact source models.

After the preregistration commit and before any target measurement, read-only review
found two remaining ambiguities in the same criterion defect recorded as D-254: `C_I`
was not explicitly defined, and the nonredundancy mutation did not name its input.
The text now fixes `C_I = (C_A + C_B)/2` coordinatewise and fixes that mutation as
removing `x0 >= 1/2`. No dimension, interval, multiplier, acceptance count, or verdict
threshold changed.

Write `r = sqrt(2)`, `L = 1 + 5r/4`, and `a = x4`. The proposed polytope fixes

`x2 = y2 = 1/2`, `x3 = y3 = 1 + 3r/4`, and `x4 + y4 = 2 + r/2`,

and has the following inequalities in `(x0,y0,x1,y1,a)`:

```text
1/2 <= x0 <= 1/2 + r/4
3/2 <= y0 <= 1/2 + 5r/4
3/2 <= x1 <= 1/2 + 5r/4
1/2 <= y1 <= 1/2 + r/4
r/2 <= a <= 2
x1 - x0 >= 1
y0 - x0 + 2a >= 3 + r
x1 - y1 + 1 >= 2a
```

Acceptance requires exact bidirectional implication between this system and all 30 rows
of the exp-033 common cell at the fixed angles, plus nonemptiness and boundedness.
The six proposed dual-support rows must have rank six in the eleven position-and-side
variables and contain the side row in their span.
Rank alone is not a dimension proof: the checker must also retain six affinely
independent exact feasible points consisting of one base and positive steps along `s`,
`R1`, `R2`, `R3`, and `R6`. The exact LP dual must prove that every feasible point in
the declared cell has side at least `S = 1 + 5r/4`; its side-`S` intersection is
therefore an LP-optimal face.
This is optimality in one fixed-orientation labelled separating cell, not global
fixed-angle or terminal optimality.

All omitted pose coordinates below are zero.
The canonical normalization is

```text
s:  dx0 = 1, dy0 = 1
R1: dx0 = -1, dx4 = -1/2, dy4 = 1/2
R2: dx0 = -1
R3: dx0 = -1, dy1 = 1, dx4 = -1/2, dy4 = 1/2
R6: dx0 = -1, dx1 = -1, dx4 = -1/2, dy4 = 1/2
```

The checker must bind these to exp-037 explicitly.
Its stored interior and B vectors named `R1` and `R2` are `r` times the canonical
vectors, while its stored A vectors are `r(Ri+s)` for `i` in `{1,2}`. Its stored
interior and B vectors named `R3` and `R6` are canonical, while its stored A vectors are
`Ri+s`. This source map prevents a scale change or double-added slide from passing as
the declared continuation.

Let `delta = 3r/2 - 2` and define `C_I = (C_A + C_B)/2` coordinatewise.
For `i` in `{1,2,3,6}`, the declared paths are

```text
C_A,i(epsilon) = C_A + epsilon (Ri + s)
C_I,i(epsilon) = C_I + epsilon Ri
C_B,i(epsilon) = C_B + epsilon Ri.
```

The checker must derive the sharp intervals `[0,delta]`, `[0,delta/2]`, and `[0,delta]`
at A, the interior, and B, respectively, by evaluating every common-cell row.
It must identify square 0’s upper-y wall as the unique limiting row at A and square 0’s
lower-x wall as the unique limiting row at the interior and B, and prove that the named
row is violated immediately beyond each endpoint.
Endpoint and strict-interior fixtures must also pass the independent exact packing
verifier.
At every retained path point, both active owner branches and every tied feature
row must be rebuilt from source.

Along the four declared path classes, the checker must rebuild the positive owner-branch
stress.
Square 2’s four lower-wall rows have weight `r/4`, square 3’s two upper-wall rows
have weight `r/2`, and contact `(2,4)` has weight one.
On the owner-3 branch for contact `(3,4)`, the weights are

```text
w+ = 5/4 - r(1+q)/2
w- = -1/4 + r(1+q)/2,
```

where `q = epsilon` for a path moving square 4 and `q = 0` for `R2`. On the owner-4
branch both weights are `1/2`. Acceptance requires exact zero pose-column sums, the
identity `sum_j w_j z_j = r dL`, strict positivity on every declared interval, and
exhaustion of the zero separating axes for contacts `(2,4)` and `(3,4)`. In particular,
both owner-3 multipliers must have the exact uniform lower bound `r/2 - 1/4 > 0`. This
proves first-order no descent along the twelve declared path segments only; it does not
prove stress on the rest of the polytope or second-order local minimality.

The ten controls mutate proof inputs and rerun the proof.
They reject: an omitted A slide correction; an added B slide correction; `R6` without
`dx4 = -1/2`; an overlong interior path; removal of the proved nonredundant inequality
`x0 >= 1/2`, which admits the exact unbounded ray `x0 -> x0 - t`; a perturbed LP-dual
coefficient; a perturbed owner-3 stress multiplier; a missing owner branch; a false
zero-axis claim; and any promotion to local minimum, quench terminal, or maximal
stationary component.

An accepted result would certify one fixed-orientation labelled separating cell’s
connected five-dimensional LP-optimal face and first-order stationarity along the twelve
declared paths only.
It would not prove that A and B are joined inside the stationary set, or classify the
rest of the polytope, global fixed-angle optima, `R4`, `R5`, `-W`, a mixed-angle
direction, second-order local minimality, the maximal stationary component,
deterministic quench selection, basin mass, census completeness, or unequal-side
clearance.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
