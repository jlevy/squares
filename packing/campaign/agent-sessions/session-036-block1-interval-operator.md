---
title: session-036 — agenda-006 block 1, an interval operator and a verifier that refuses
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-036
  title: Build the interval-certification bridge as far as a Krawczyk operator and a separating-axis test that both refuse correctly
  date: '2026-08-28'
  started_at: '2026-08-28T20:10:00-07:00'
  deadline_at: '2026-08-28T22:40:00-07:00'
  goal: >-
    Close agenda-006 block 1 by running phases 1 and 2 of
    plan-2026-08-28-interval-certification: interval arithmetic with a sign that refuses,
    a Krawczyk operator reporting existence and uniqueness separately, the outward-rounded
    layout map, and separating-axis verification over enclosures. The block question is
    whether each stage can be caught refusing, not whether anything certifies at n = 29,
    which is block 2's question and is deliberately not asked here.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-052
    bead: think-pr0m
    objective: >-
      Build `promote/interval.py` and `promote/krawczyk.py`: outward-rounded interval
      scalars over `mpmath.iv`, a sign that refuses on a straddling enclosure, forward-mode
      automatic differentiation in interval arithmetic so the Jacobian is enclosed over a
      box rather than differenced at a point, and the Krawczyk operator with `exists` and
      `unique` reported separately. Calibrate against a root an independent implementation
      already isolates.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 60
    started_at: '2026-08-28T20:10:00-07:00'
    deadline_at: '2026-08-28T21:10:00-07:00'
    expected_output: >-
      A `certify(system, box, digits)` entry point returning a `CertifiedRoot`, agreement
      with `sqpack.field`'s Sturm isolation on `sqrt(2)`, and the two controls the spec
      names: a box with no root must not report existence, and a box with two roots must
      never report uniqueness.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: >-
      Stop if the operator is made to succeed by widening a box until containment holds
      trivially; stop if `unique` is reported without testing interior containment, since
      containment alone does not give uniqueness; stop if any claim is made about n = 29,
      which this phase does not ask about.
    fallback: >-
      Retain the interval arithmetic and a typed statement of which conditioning prevents
      contraction, rather than an operator whose verdict is not backed by an interior
      containment test.
    outcome: >-
      Built and calibrated. The operator certifies a unique root of `x^2 - 2` in a box of
      radius `2.33e-61` and of a 2x2 system in one of radius `2.00e-51`. Two soundness bugs
      were found by the calibration rather than by inspection, and both were in the
      direction that flatters.
    evidence:
    - >-
      Forward-mode AD over intervals reproduces four hand-computed partial derivatives of
      `[x^2 y + sin x, x / y]` exactly, and over a box returns an enclosure of width
      `0.979` that contains the pointwise value, which is what a Jacobian over a box has
      to do and what numerical differencing cannot supply.
    - >-
      'Cross-check against an implementation sharing no code with this route: `sqpack.field`
      isolates `sqrt(2)` by Sturm sequences over exact rationals to a width of `7.006e-46`,
      and that interval lies inside the certified box.'
    - >-
      'First bug, found by the cross-check. The certified box did not contain the root. The
      operator was right and the *serialization* was wrong: writing endpoints with
      `mp.nstr` rounds to nearest, and at 40 significant digits that lifts `sqrt(2)`''s
      lower endpoint from `...0785696` to `...078570`, above the root. Serializing a
      certificate is arithmetic too. Fixed by rounding endpoints strictly outward through
      `decimal` after an exact dyadic conversion, and the trap itself is now asserted in the
      test so the fix cannot silently regress.'
    - >-
      'Second bug, found by the same calibration. The iteration reported its final state
      rather than the verdict it had proved: contraction eventually drives the box tight
      enough that the operator''s own rounding makes `K(X)` marginally wider than `X`, and
      a uniqueness proof obtained at iteration 2 was being discarded at iteration 4. A
      proof about a box cannot be undone by a later iteration, so the best verdict is now
      kept with the box that earned it.'
    - >-
      'Controls. A box around `5.0` holding no root of `x^2 - 2` reports neither existence
      nor uniqueness. Three boxes each containing both roots of `(x-1)(x-2)` never report
      uniqueness. Recorded rather than smoothed over: all three return no verdict at all
      rather than `exists` without `unique`, because `exists and not unique` needs `K(X)`
      to touch the boundary of `X` exactly, which floating point does not produce. The
      safety claim under test is "never unique", and that is what is asserted.'
    stop_reason: criterion
    next_action: >-
      Enter phase 2 and build the layout map and interval separating-axis test, with the
      two controls the spec names for them.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-052
    bead: think-pr0m
    objective: >-
      Build `promote/enclose.py` and `promote/interval_verify.py`: propagate a certified
      pose box through the layout map to outward-rounded corner boxes, and verify
      containment and pairwise separation over enclosures so that an undecidable pair is a
      named refusal rather than a pass.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      Phase 1's operator is calibrated and its controls fire, which is this phase's entry
      condition; the objective changes from certifying a root to certifying a packing.
    budget_minutes: 60
    started_at: '2026-08-28T21:10:00-07:00'
    deadline_at: '2026-08-28T22:10:00-07:00'
    expected_output: >-
      A verifier returning separated, overlapping and undecided as three distinct verdicts,
      with the spec's two controls: a container shrunk below the packing must be refused,
      and a pose box widened until separation is undecidable must produce a typed refusal
      naming the pair rather than a silent pass.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: >-
      Stop if an undecided separation is ever folded into a pass, which is the failure the
      whole route exists to prevent; stop if a tolerance is introduced anywhere to make a
      tight packing certify.
    fallback: >-
      Retain the layout map and report which pairs are undecidable at which box widths,
      rather than a verifier whose "certified" includes anything it could not decide.
    outcome: >-
      Built, with all four verdicts exercised. The load-bearing result is a refusal: four
      unit squares packed exactly into a side-2 container return six undecided pairs and
      zero separated, which is the correct answer and the one a tolerance-based checker
      would get wrong.
    evidence:
    - >-
      'The same four squares with a tenth of a unit of clearance certify: 6 pairs tested, 6
      strictly separated, no refusal. So the undecided verdict above is about exact
      contacts, not about the verifier being unable to certify anything.'
    - >-
      'Spec control, container: shrinking the side to 1.5 under a packing that spans 2.1
      returns "square 1 corner 2 is proved outside the container on y" rather than a pass.'
    - >-
      'Spec control, widening: inflating every corner enclosure by `0.06` under a layout
      with `0.1` clearance returns all six pairs undecided and names the first,
      distinguishing "cannot tell" from "invalid" -- a genuinely interpenetrating pair is
      reported as proved overlapping instead.'
    - >-
      A finding, recorded rather than worked around. The spec expected `verify_packing` to
      be reusable by injecting an interval `sign`, and it is not: measured here, that
      refuses on a layout with a tenth of a unit of clearance on every pair. Two independent
      causes, both in the float-shaped fold rather than in the geometry. `project` orders
      corner projections whose enclosures overlap, so it refuses before any separation
      question is asked; and `separated` folds four axes together, so one axis's undecided
      sign discards a pair that another axis separates strictly. The fold is reimplemented
      and the geometry -- `edge_axes` -- is still shared. The measurement is asserted in the
      test, so if that function is ever made refusal-tolerant the reimplementation can be
      retired rather than left standing on a stale claim.
    - >-
      Why shape checking is off, measured rather than assumed. A rotated unit square's
      edge-length enclosure contains 1 and is not the degenerate `[1, 1]`, so
      `check_unit_squares` refuses on every square. Squares are unit by construction from a
      centre and an angle instead, and the test asserts the refusal so the reason stays
      visible.
    stop_reason: criterion
    next_action: >-
      Register the negative controls, run the gate, and close the block at its checkpoint.
  - workflow: process-review
    recording: contemporaneous
    clock_role: finalization
    focus: process
    commitment: BC-052
    bead: think-pr0m
    objective: >-
      Register the block's negative controls in the shared harness, bring the new modules
      up to the lint and type floor, run the fast gate, and leave the checkpoint committed,
      pushed and carried by the run's PR.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      Both scientific phases reached their criteria; what remains is reconciliation rather
      than measurement.
    budget_minutes: 30
    started_at: '2026-08-28T22:10:00-07:00'
    deadline_at: '2026-08-28T22:40:00-07:00'
    expected_output: >-
      Four registered negative controls that fire in the shared harness, a green fast gate,
      and a pushed checkpoint.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: >-
      Stop if a control is registered without having been watched to fire, which would make
      the control file a claim rather than evidence.
    fallback: >-
      Push the work with the failing step named rather than leaving the block's result only
      in a working tree on an ephemeral container.
    outcome: >-
      Closed. Negative controls rise from 86 to 90 and all 90 fire. The fast gate is green
      at 4m03s, against the 4m15s baseline measured on this container at the start of the
      run.
    evidence:
    - >-
      'Four controls registered and each watched to fire: rounding certificate endpoints to
      nearest, a straddling sign answering zero instead of refusing, the operator reporting
      its last state rather than the verdict it proved, and an undecided separation counted
      as separated. Each reproduces one of the two bugs found in this block or one of the
      two refusals the route depends on.'
    - >-
      'A process finding worth keeping. Verifying those controls by hand -- mutate, run,
      restore -- left stale `__pycache__` bytecode that made a later run read the mutated
      module and report a wrong verdict. The shared harness runs each control in a
      throwaway snapshot precisely to avoid this, which its own docstring says; the ad-hoc
      script did not. Nothing was concluded from the stale run, and the lesson is to use the
      harness rather than reproduce it badly.'
    - >-
      'Two gate failures found and fixed rather than worked around: `mpmath`''s interval
      constructor is annotated as taking `int` alone, now suppressed once behind two
      constructors rather than at each call site; and this file''s own first draft depended
      on ambient precision, so a 300-digit context left by another test made a
      literal-versus-enclosure comparison fail on rounding. Precision is now pinned for the
      module.'
    - >-
      A declared-consumer entry was required for agenda-006, because it names
      `verified_upper_bound`. That contract behaved exactly as designed and the entry says
      the ceiling does not move in this run.
    stop_reason: criterion
    next_action: >-
      Open block 2 as session-037 under BC-053, merging origin/main first, and run spec
      phases 3 and 4.
  primary_bead: think-pr0m
  status: completed
  budget:
    wall_minutes: 150
    orientation_minutes: 10
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 30
  stop_conditions:
  - The block deadline at 2026-08-28T22:40:00-07:00
  - Any claim about n = 29, which belongs to block 2 and is out of scope here
  - A verdict reached by loosening a tolerance rather than by tightening an enclosure
  - Three consecutive guard refusals or crashes
  progress:
    metric: >-
      Stages of plan-2026-08-28-interval-certification built with their controls firing,
      out of the four the spec names
    before: '0 of 4; the witness contract named `interval-certified` and `exact_verify` raised `checker-not-built`'
    after: >-
      2 of 4. Phases 1 and 2 are built and controlled; phases 3 and 4, calibration and
      n = 29, remain, and `exact_verify` still raises `checker-not-built` because no witness
      branch was touched in this block.
  delegations: []
  outputs:
  - src/sqpack/promote/interval.py
  - src/sqpack/promote/krawczyk.py
  - src/sqpack/promote/enclose.py
  - src/sqpack/promote/interval_verify.py
  - tests/test_promote_krawczyk.py
  - tests/test_promote_interval_verify.py
  - devtools/controls.yaml
  - campaign/agendas/agenda-006-overnight-research-blocks.md
  checks:
  - 'uv run --frozen --all-extras --group dev packing-validate --fast: green, 4m03s, 16 of 38 steps'
  - 'uv run --frozen --group dev python -m devtools.run_negative_controls: 90 of 90 fire'
  - 'uv run --frozen --group dev basedpyright src/sqpack/promote tests/test_promote_*.py: 0 errors'
  - 'uv run --frozen --group dev ruff check: all checks passed'
  stop_reason: >-
    Both declared phases reached their criteria inside the block clock, and the finalization
    reserve closed the checkpoint.
  next_action: >-
    Open block 2 as session-037 under BC-053 and `think-9ida`. Merge origin/main first,
    then run phases 3 and 4 of plan-2026-08-28-interval-certification: certify n = 5 and
    n = 10 against the exact route, n = 11 against Trump's published polynomial,
    demonstrate a refusal on a plausible-but-infeasible pose, and only then drive the
    n = 29 system from BC-047's refinement. Record any n = 29 success as `unresolved` with
    `needs_review: true`; the ceiling does not move in this run.
---
# session-036 — block 1, an interval operator and a verifier that refuses

Block 1 of [agenda-006](../agendas/agenda-006-overnight-research-blocks.md), advancing
`BC-045` through phases 1 and 2 of
[plan-2026-08-28-interval-certification](../../../docs/project/specs/active/plan-2026-08-28-interval-certification.md).

## What this block was for

The exact promotion route recovers a minimal polynomial and discharges it.
At `n = 29` that route is stalled: [X-004](../explorations/X-004-n29-exact-promotion.md)
found no integer relation through degree twenty with coefficients below `10^22`, so the
polynomial is large and may not be recoverable at all.

Interval certification does not need the polynomial.
It proves that a root exists and is unique inside a box, propagates that box to square
corners, and checks separation on enclosures.
Everything above it was already in place — `sqpack.assurance` lists `interval-certified`
among the methods that may carry `verified`, and `sqpack.verify` takes an injected
`sign` — so this block builds the arithmetic and the operator that socket was left open
for.

## The result

Two of the spec’s four phases are built, and every stage that can refuse has been
watched refusing.

The one worth stating plainly is a negative one.
Four unit squares packed exactly into a side-2 container come back **undecided**, not
certified: six pairs, none separated.
That is the correct answer.
A tight packing’s contacts are exact zeros, no enclosure of positive width certifies an
equality, and a verifier that passed that case would be accepting overlaps of the same
magnitude — the precise failure the assurance boundary exists to prevent.
It is also why a certified upper bound is stated at a side slightly above the optimum,
where every inequality has margin, rather than at the optimum, where half of them are
equalities.

## What the calibration caught

Both bugs found in this block were found by the known-answer check rather than by
reading the code, and both pointed the flattering way.

The first was in **serializing** the certificate, not in computing it.
Writing a box’s endpoints with rounding to nearest moved both of them above `sqrt(2)`,
so the operator proved something true and then wrote down something false.
Endpoints now round strictly outward.

The second was in the **iteration**. Contraction eventually drives a box tight enough
that the operator’s own rounding makes `K(X)` marginally wider than `X`; the loop
reported that final state and discarded a uniqueness proof it had obtained two
iterations earlier. A proof about a box is not undone by a later iteration, so the
verdict and the box that earned it are now kept.

Neither would have been caught by a checker that only ever ran on inputs it agreed with,
which is the argument for calibrating against `sqpack.field` — an implementation that
isolates the same root by Sturm sequences over exact rationals and shares no code with
this route.

## What did not work as specified

The spec expected `verify_packing` to be reusable by injecting an interval `sign`.
Measured, it is not: it refuses on a layout with a tenth of a unit of clearance on every
pair, for two reasons that are both properties of a float-shaped fold rather than of the
geometry. `project` orders corner projections whose enclosures overlap, and `separated`
folds four axes together so that one undecided axis discards a pair another axis
separates strictly.

The fold is reimplemented in `interval_verify`; the geometry, `edge_axes`, is still
shared. The measurement is asserted in the test, so if that function is ever made
refusal-tolerant the reimplementation can be retired rather than left standing on a
claim nobody rechecked.

## Claim boundary

Nothing here certifies `n = 29`, and nothing here touches `verified_upper_bound`.
`exact_verify` still raises `checker-not-built`, because no witness branch was written
in this block: the schema decision that gates it — whether a fourth `scalar.kind` is a
`Witness/v1` extension or a `v2` migration — is block 2’s, taken with the calibration
results in hand rather than before them.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
