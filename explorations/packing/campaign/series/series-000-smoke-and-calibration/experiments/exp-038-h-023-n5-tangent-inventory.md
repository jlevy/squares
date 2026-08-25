---
title: exp-038 — exact n = 5 tangent-cone inventory
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-038
  series: series-000
  title: Certify the complete first-order cone along the exp-033 face
  date: '2026-08-25'
  hypotheses:
  - H-023
  tier: confirmatory
  subject:
    label: exact branchwise fixed-side tangent-cone factorization at n = 5
    engine: n = 5 tangent-inventory checker 0.1.0
    engine_commit: b8d0104
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance:
    axis: n
    point: 5
    role: target
  method:
    control: exact exp-034 through exp-036 semantic bindings, an independent analytic sheet oracle,
      and ten rigid, flexible, lineality, branch, ray, classification, and scope controls
    candidate: positive exact left-kernel certificates, exhausted left-kernel rank, explicit lineality
      and sheet bases, and a six-generator transverse-cone factorization for each of the six stratum
      and owner-axis matrices
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: b8d0104
    dirty: false
    entry_point: explorations/packing/cases/n5/tangent_inventory.py
    command: timeout 30 uv run --directory explorations/packing --frozen --quiet python -m cases.n5.tangent_inventory
      --record campaign/series/series-000-smoke-and-calibration/results/exp-038-h-023-n5-tangent-inventory.json
      && timeout 30 uv run --directory explorations/packing --frozen --quiet python -m cases.n5.tangent_inventory
      --replay campaign/series/series-000-smoke-and-calibration/results/exp-038-h-023-n5-tangent-inventory.json
    budget: one 30-minute implementation and measurement slice; separate 30-second generation and
      replay caps; stop on source drift, incomplete branch coverage, a failed exact certificate, a
      surviving control, a nonlinear overclaim, or retained-record drift
    record: campaign/series/series-000-smoke-and-calibration/results/exp-038-h-023-n5-tangent-inventory.json
  results:
  - shape: determination
    question: What is the complete branchwise fixed-side linearization cone at A, one interior point,
      and B after identifying the certified exp-034 sheet without treating exp-036's one obstructed
      orientation as a quotient symmetry?
    role: outcome
    outcome: criterion_met
    checked_by: exact Q(sqrt(2)) left-kernel exhaustion, physical generator and source checks, deterministic
      record regeneration, independent result review, and ten declared controls
  effort:
    timebox: 30m exact-inventory slice; 30s generation and 30s replay caps
    wall_seconds: 1.06
    agent_minutes: 30
    stopped_by: criterion
  verdict:
    decision: accepted
    primary_criterion: rebuild all six exact source matrices; certify their ranks, lineality, and
      complete positive left-kernel relations; prove that both owner branches have the same exact
      V-representation; identify the exp-034 sheet analytically; retain six transverse generators,
      their sole relation, and both pointed-quotient face vectors; replay identically; reject all
      ten controls; and leave -W and every transverse or mixed nonlinear lift unresolved
    reason: All six source matrices have the preregistered complete V-representation, both owner branches
      coincide at first order, both pointed-quotient face vectors are derived, replay is identical,
      and all ten controls reject their mutations. The verdict remains limited to branchwise linearization
      cones.
    commit: b8d0104
---
# exp-038 — accepted exact n = 5 tangent-cone inventory

Exp-035 retained one non-sheet vector but did not enumerate its branchwise cones.
An exact active-set pilot has now supplied discovery evidence: each endpoint branch has
eight pointed quotient rays, each interior branch has six, and the two owner-axis
branches have the same candidate V-representation.
The pilot fixed the proposed counts, so this round is confirmatory and uses a different,
analytic completeness certificate.

The original preregistration sentence said that “every nonlinear lift” remains
unresolved. That was too broad because exp-034 already supplies the declared nonlinear
sheet lifts.
Before any retained target run, the scope was corrected to “every transverse
or mixed-direction nonlinear lift.”
The acceptance counts and mathematical threshold did not change.

Let `A` be one retained active-row matrix and `z = A v` its nonnegative slack vector.
Acceptance requires exact positive left-kernel certificates that force these nine rows
to remain equalities in every stratum and owner branch:

- all four square-2 lower-wall rows;
- both square-3 upper-wall rows;
- contact `(2,4)`; and
- both tied-support rows of the selected `(3,4)` owner branch.

The checker must prove that the positive relations, together with

`X- + Y+ = X+ + Y-`,

exhaust the left kernel.
Here `X-`, `X+`, `Y-`, and `Y+` are square 1’s tied upper-x and lower-y wall slacks.
The surviving pointed transverse cone must therefore be

`R_+^2 × {X-, X+, Y-, Y+ >= 0 : X- + Y+ = X+ + Y-}`.

Its six exact rays open, respectively, only contact `(1,4)`, only contact `(0,4)`,
`Y- + Y+`, `X- + Y-`, `X+ + Y+`, and `X- + X+`. The four square-1 rays have the sole
positive relation `R3 + R6 = R4 + R5`. The checker must derive the five-dimensional face
vector `(1,6,13,13,6,1)` from the product of two orthant rays and the cone over a
quadrilateral, not accept it as an unverified constant.

The exp-034 sheet is an independent analytic oracle.
At the interior its tangent space is spanned by `dx0 = dy0 = 1` and `dtheta0 = 1`. At A
its one-sided rays are `(dx0,dy0,dtheta0) = (1/2,1/2,+1)` and `(1/2,1/2,-1)`; at B their
first two coordinates are `(-1/2,-1/2)`. Acceptance requires eight endpoint quotient
rays—two sheet and six transverse—and six interior transverse quotient rays.
At the interior, the sheet occupies two of the three lineality dimensions.
At each endpoint, only `W` is lineality and the sheet is the pointed cone on its two
one-sided rays; the slide direction is their positive sum, not a quotient symmetry.

The checker must derive the pointed transverse quotient face vector `(1,6,13,13,6,1)`
and the pointed endpoint quotient face vector `(1,8,26,45,45,26,8,1)`. Entry `k` counts
`k`-dimensional faces of the pointed quotient, including its apex and whole cone and
excluding the empty face.

The ten controls require a known rigid cone to have no pointed ray, a known orthant to
have its declared rays, and a cone with lineality to separate its kernel and pointed
generator. They also reject a missing owner record, a duplicated owner record, a dropped
transverse generator, either direction of a sheet/transverse label swap, a claim that
exp-036 covers `-W`, and a claim that any transverse lift has already been continued
nonlinearly.

An accepted result would be a complete branchwise linearization-cone generator and face
inventory only. Exp-036 excludes the displayed `+W` orientation; it does not exclude
`-W`, all of the linearized lineality, or a direction `R_i + lambda W + s` with sheet
motion `s`. Extreme-ray checks also do not classify face interiors of the true Bouligand
cone. This round therefore cannot establish terminal or stationary membership, local
isolation, component identity, basin mass, census completeness, or unequal-side
clearance.

## Result

The frozen criterion was met from clean engine commit `b8d0104`. Exact generation and
replay took 0.534 and 0.526 seconds, respectively, and every declared control rejected
its mutation.

At A and B, each owner branch has eight rays after quotienting by its one-dimensional
lineality; at the interior, each owner branch has six rays after quotienting by its
three-dimensional lineality.
The two owner branches have identical physical V-representations at every stratum.
Removing the endpoint sheet rays leaves the same six-generator transverse cone
throughout:

`R_+^2 × {X-, X+, Y-, Y+ >= 0 : X- + Y+ = X+ + Y-}`.

Its only positive ray relation is `R3 + R6 = R4 + R5`. The pointed transverse and
endpoint quotient face vectors are `(1,6,13,13,6,1)` and `(1,8,26,45,45,26,8,1)` under
the declared convention.

This settles the complete branchwise first-order linearization inventory only.
It does not promote `-W`, a transverse or mixed direction, a face interior, or any
terminal, stationary, component, basin, census, or unequal-side claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
