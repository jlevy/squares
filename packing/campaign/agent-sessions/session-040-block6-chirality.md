---
title: session-040 — agenda-006 block 6, a pose gets a chirality
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-040
  title: Give the pose model a reflection so the n = 29 contact system assembles
  date: '2026-08-29'
  started_at: '2026-08-28T23:09:01-07:00'
  deadline_at: '2026-08-28T23:54:00-07:00'
  goal: >-
    Close agenda-006 block 6 by making the n = 29 contact system assemble at its published
    pose. Assembly refused seven of the twenty-nine squares by name because a
    centre-plus-rotation cannot produce a clockwise winding; either the corner model
    carries a reflection or the block states what one costs the feature naming.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-058
    bead: think-km5r
    objective: >-
      Carry a per-square chirality from extraction through assembly, and measure whether
      the n = 29 equations vanish at the pose they were extracted from.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-08-28T23:09:01-07:00'
    deadline_at: '2026-08-28T23:39:00-07:00'
    expected_output: >-
      An n = 29 residual at the noise floor, or a typed statement of what re-winding a
      square costs the feature indices.
    validation_command: >-
      uv run --frozen --group dev python -m pytest tests/test_promote_system.py -q
    kill_condition: >-
      Stop if the n = 11 calibration moves. Its residual, rank and shortfall are the fixed
      points that say the change did not buy n = 29 by breaking the case with a known
      answer.
    fallback: >-
      Keep the refusal and record which of the two repairs -- re-indexing features or
      giving the pose a chirality -- the contact structure resists, rather than shipping a
      model that poses a mirror image.
    outcome: >-
      Assembled. The n = 29 residual falls from 2.0 to 1.3e-15, the n = 11 calibration is
      unmoved at 4.4e-16 with rank 30 and shortfall 4, and the coupling the block was
      warned about turned out not to exist.
    evidence:
    - >-
      'The corner model is now `corner_k = c + R(t) . (sigma * ox_k / 2, oy_k / 2)` with
      `sigma = +1` or `-1`, reflecting the *local* x axis before the rotation turns it. At
      `sigma = +1` it is the old formula unchanged, which is why n = 11 does not move.'
    - >-
      'The note on BC-058 expected the hard part to be that feature indices refer to a
      corner order, so re-winding a square would rename its features. That cost was not
      paid: reflecting the local axis leaves the corner *indices* alone and changes only
      where each one sits, so `corner:2` still names the corner the extractor found. No
      feature name changed and no structure needed re-indexing.'
    - >-
      'Chirality is recorded on the structure, not inferred at assembly. Inferring it
      would be right for most packings and wrong for exactly the one that motivated the
      field, so a structure that does not carry it is refused as `chirality-missing`.'
    - >-
      'The old `reflected-squares` refusal is replaced rather than deleted. A reflection is
      now representable; what is still refused is substituting a mirrored pose into a
      system assembled for the upright packing, as `chirality-mismatch` -- otherwise it
      would surface as residuals that read like a bad structure rather than a mismatched
      caller.'
    - >-
      'Measured, n = 29: 94 contact equations against 88 unknowns, Jacobian rank 81,
      shortfall 7. The rank is not a judgement call -- the smallest counted singular value
      is 0.114 and the largest discarded 6.7e-161.'
    stop_reason: criterion
    next_action: >-
      Characterise the shortfall before handing it to BC-059, then close the block.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-058
    bead: think-km5r
    objective: >-
      Describe the seven-dimensional null space the assembled n = 29 system leaves, and
      say whether it contains directions that change the side, so BC-059 starts from a
      measurement rather than from the count.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The system assembles; the question changes from whether it can be written down to
      what it does not determine.
    budget_minutes: 8
    started_at: '2026-08-28T23:39:00-07:00'
    deadline_at: '2026-08-28T23:47:00-07:00'
    expected_output: >-
      The norm of the projection of `e_s` onto the null space, at every size with a
      structure to measure.
    validation_command: >-
      uv run --frozen --group dev python -m pytest tests/test_promote_system.py -q
    kill_condition: >-
      Stop before proposing a closure. Sizing the shortfall is this block; deriving the
      conditions is BC-059 and doing it here would be an invented constraint.
    fallback: Record the rank alone and leave the null space to BC-059.
    outcome: >-
      Characterised, and n = 5 is the odd size out rather than n = 29. The quantity that
      matters is the norm of the projection of `e_s` onto the contact Jacobian's null
      space: `1.0e-16` at n = 5, `1.86e-1` at n = 11, `1.14e-1` at n = 29. The first is
      zero and the other two are not. SUPERSEDED by session-041 and D-361: the two
      non-zero readings were caused by an `edge-edge` contact assembled as one equation
      where collinearity is two, and both fall to zero once it is repaired. The
      measurements below stand; the conclusion drawn from them does not.
    evidence:
    - >-
      'The measurement is the projection norm, not whether a basis vector happens to show
      an `s` entry. A null space is only defined up to an orthonormal basis, so a
      per-vector reading answers a question nobody asked; `sqrt(sum_k V[k,s]^2)` is basis-
      independent and is what the condition is about.'
    - >-
      'n = 5: `1.0015e-16` on a single null vector whose largest coordinate is `1.0`. No
      contact-preserving first-order motion changes the side, so the first-order condition
      already holds there and the one missing condition is of some other character.'
    - >-
      'n = 11 (four null vectors, `s` components `4.3e-2`, `1.7e-1`, `6.4e-2`, `1.3e-2`)
      and n = 29 (seven, from `1.3e-2` to `6.1e-2`) behave the same way, and it is the
      consequential way. If `A v = 0` then every active contact is preserved to first
      order along both `+v` and `-v`, so one of the two decreases the side to first order.
      Neither packing is a strict first-order local minimum of its contact system, and no
      first-order stationarity condition can close either -- what rules those motions out
      is second order.'
    - >-
      'That is the handoff BC-059 needs and it inverts the one this block first wrote
      down. The discriminating pair is n = 5 against n = 11 and n = 29, not n = 29 against
      n = 11: a formulation that closes n = 5 may never have to look at curvature, and one
      that closes the other two always does.'
    - >-
      'The first version of this phase recorded the opposite -- that `s` was absent from
      the n = 29 null space -- and it was read off a printout that showed the eight largest
      coordinates per vector and collected only names beginning `x`, `y` or `t`, which
      excludes `s` by construction. `s` was there at `1.2e-2` to `6.1e-2` the whole time.
      Caught before the commit, by measuring the projection instead of re-reading the
      display. A filtered display is not a measurement.'
    stop_reason: criterion
    next_action: >-
      Register controls, run the gate, and close the block.
  - workflow: process-review
    recording: contemporaneous
    clock_role: finalization
    focus: process
    commitment: BC-058
    bead: think-km5r
    objective: >-
      Register the block's controls, freeze the structures with their chirality, and leave
      the checkpoint pushed.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: The scientific phases reached their criteria.
    budget_minutes: 7
    started_at: '2026-08-28T23:47:00-07:00'
    deadline_at: '2026-08-28T23:54:00-07:00'
    expected_output: Controls that fire, a green gate, and a pushed checkpoint.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: Stop if a control is registered without having been watched to fire.
    fallback: Push with the failing step named.
    outcome: >-
      Closed. Four controls replace the one the change made obsolete and all four fire. A
      pre-existing reproducibility defect surfaced on the way and is recorded rather than
      fixed in passing.
    evidence:
    - >-
      'Four controls: the corner model dropping its chirality sign, a missing chirality
      defaulted to all `+1`, a mismatched pose substituted unchecked, and extraction
      reporting every square counter-clockwise regardless of winding. Each was watched to
      fire. The control they replace mutated a refusal that no longer exists.'
    - >-
      'The frozen structures now carry `chirality` as required data:
      `[1]*11` at n = 11 and `[1,1,1,-1,-1,-1,-1,-1,-1,-1,1,...]` at n = 29. Required
      rather than nullable, because unlike `contact` there is no structure in the record
      that predates it -- both were regenerated here.'
    - >-
      'D-359, found by this block and belonging to none of it. Running
      `tests/test_promote_system.py` before `tests/test_known_best_atlas.py` fails the
      composite PNG receipt, at HEAD as well as under this change: `format_svg_number`
      renders a scalar at whatever precision it was last refined to, so the atlas SVG
      carries 27 fractional digits in a fresh process and 50 after any caller refines the
      shared field. The check passes today on test ordering rather than on whether the PNG
      is stale. Fixing it re-hashes every stored SVG and PNG receipt in the repository, so
      it is `think-mt4h` and not a change made in passing.'
    - >-
      'The lint floor caught the threading and the repair was the better design anyway.
      Passing `sigmas` alongside `xs, ys, ts` pushed three helpers past the positional-
      argument ceiling; the four are now a `_Pose` bundle, which is what they always
      were -- any function taking three of them was taking the wrong three. The n = 29
      residual, chirality and rank are unchanged across the refactor.'
    - >-
      'The gate refused the block once, correctly. This session record names
      `verified_upper_bound` in a stop condition, and the contract requires every file
      that names the field to declare what it takes it to mean. Declared: the block builds
      the pose model and does not touch the ceiling. That is the second time in this run
      the consumer contract has caught a record before it landed.'
    - >-
      'The clock was read rather than estimated, and the estimate was wrong again. Partway
      through the block the coordinating agent believed it was an hour over budget; `date
      -u` said 22 minutes in. D-358''s practice change is doing the work it was written
      for.'
    stop_reason: criterion
    next_action: >-
      Open block 7 as session-041 under BC-059 and `think-9c40`.
  primary_bead: think-qs6k
  status: completed
  budget:
    wall_minutes: 45
    orientation_minutes: 3
    checkpoint_minutes: 8
    slice_minutes: 30
    finalization_minutes: 7
  stop_conditions:
  - The block deadline at 2026-08-28T23:54:00-07:00
  - Any movement in the n = 11 calibration's residual, rank or shortfall
  - Any move of verified_upper_bound, which is a human decision
  - Proposing a closure condition, which is BC-059's work and not this block's
  progress:
    metric: >-
      Whether the n = 29 contact system can be assembled at the pose it was extracted from
    before: >-
      No. Assembly refused seven of twenty-nine squares by name, and reading them as
      rotations left the residual at 2.0 -- the model described their mirror images.
    after: >-
      Yes. The residual is 1.3e-15, the n = 11 calibration is unmoved, and the system's
      seven-dimensional shortfall is characterised for BC-059 -- including that it contains
      side-changing directions, so no first-order condition closes it.
  delegations: []
  outputs:
  - src/sqpack/promote/contacts.py
  - tests/test_verified_upper_bound_contract.py
  - src/sqpack/promote/system.py
  - atlas/known-best/contact-structure.schema.yaml
  - atlas/known-best/contact-structures.json
  - devtools/generate_contact_structures.py
  - tests/test_promote_system.py
  - devtools/controls.yaml
  - defects.yaml
  checks:
  - 'n = 29 assembled residual: 1.33e-15 across 94 equations (was 2.0)'
  - 'projection of e_s onto null(A): 1.00e-16 at n = 5, 1.86e-1 at n = 11, 1.14e-1 at n = 29'
  - 'n = 11 calibration unmoved: residual 4.44e-16, rank 30, shortfall 4'
  - 'uv run --frozen --group dev python -m devtools.run_negative_controls -k chirality: 4 of 4 fire'
  - 'uv run --frozen --group dev python -m devtools.validate_schemas: OK'
  stop_reason: >-
    Both work phases reached their criteria inside the block clock, read from `date -u` at
    each boundary.
  next_action: >-
    Open block 7 as session-041 under BC-059 and `think-9c40`: derive the stationarity
    conditions `close` currently only sizes. This block hands it the measurement it needs
    -- the projection of `e_s` onto the contact null space is zero at n = 5 and is not at
    n = 11 or n = 29, so a first-order condition cannot close the latter two and BC-059
    must reach for second-order information there.
---
# session-040 — block 6, a pose gets a chirality

Block 6 of [agenda-006](../agendas/agenda-006-overnight-research-blocks.md), and the
second of the missing middle layers.

## The refusal that was standing in the way

`assemble` could not describe the packing it was built for.
Seven of the `n = 29` layout’s twenty-nine squares are placed inside `scale(-1 1)`
mirror groups, and a pose that is a centre plus a rotation cannot produce a clockwise
winding — so the previous block made it refuse them by name rather than quietly describe
their mirror images.
Read as rotations, the assembled residual sat at `2.0`.

A pose is now a centre, an angle, **and** a chirality:

```
corner_k = c + R(t) . (sigma * ox_k / 2, oy_k / 2)
```

`sigma` reflects the local *x* axis before the rotation turns it.
At `sigma = +1` the formula is the old one character for character, which is why the
`n = 11` calibration does not move.

The residual falls from `2.0` to `1.3e-15`.

## The cost that was not paid

BC-058 was written with a warning attached: feature indices refer to a corner order, so
re-winding a square renames its features, and that coupling was “the actual problem and
the reason this was not done in passing”.

It did not turn out that way.
Reflecting the *local* axis leaves the corner indices alone and changes only where each
one sits, so `corner:2` still names the corner the extractor found.
No feature name changed and no structure needed re-indexing.
Recorded because the expectation is in the agenda and a reader deserves to know it was
wrong.

## What the system still does not determine

> **Superseded by [session-041](session-041-block7-collinearity.md) and
> [D-361](../../../defects.md).** Everything measured in this section is correct and
> everything concluded from it is not.
> The shortfall was not a property of the packings: an `edge-edge` contact was assembled
> as one equation where collinearity is two, and with the second the rank reaches `34`
> of `34` at `n = 11` and `88` of `88` at `n = 29`, with the projection of `e_s` onto
> the null space falling to zero at both.
> There are no missing stationarity conditions at either size, first-order or otherwise.
> The section is kept as written because the numbers in it are what led to the repair.

The assembled `n = 29` system has 94 equations against 88 unknowns and rank 81 — seven
conditions short, with the smallest counted singular value at `0.114` against a largest
discarded of `6.7e-161`, so the rank is decided rather than judged.

What that null space contains is the finding.
The quantity to ask for is the norm of the projection of `e_s` onto it —
basis-independent, unlike whether some particular basis vector shows an `s` entry:

|  | shortfall | ‖proj of `e_s` onto null(A)‖ |
| --- | ---: | ---: |
| `n = 5` | 1 | `1.00e-16` |
| `n = 11` | 4 | `1.86e-1` |
| `n = 29` | 7 | `1.14e-1` |

`n = 5` is the odd size out, not `n = 29`.

The consequence is sharp.
If `A v = 0` then every active contact survives to first order along both `+v` and `-v`,
so when `e_s · v ≠ 0` one of the two *decreases the side to first order*. At `n = 11`
and `n = 29` such directions exist, so neither packing is a strict first-order local
minimum of its own contact system and **no first-order stationarity condition can close
either** — what forbids those motions is curvature.
At `n = 5` no such direction exists, and its single missing condition is of some other
character.

BC-059 inherits a discriminating pair from this: `n = 5` against the other two, where
the first version of this section had it the other way round.

## A correction made before the commit

That section first said the side was *absent* from the `n = 29` null space.
It was not. The reading came from a printout that showed each vector’s eight largest
coordinates and collected only names beginning `x`, `y` or `t` — which excludes `s` by
construction — and `s` sat at `1.2e-2` to `6.1e-2` in all seven vectors the whole time.

Measuring the projection instead of re-reading the display caught it.
A filtered display is not a measurement, and the filter was mine.

## A defect found on the way out

Running the assembly tests before the atlas tests fails the composite PNG receipt — at
`HEAD` as much as under this change.
`format_svg_number` renders a scalar at whatever precision it was last refined to, so
the generated atlas SVG carries 27 fractional digits in a fresh process and 50 once
anything has refined the shared field.

The check passes today because of test ordering, not because the stored PNG is current,
and a genuinely stale PNG would look identical.
That is [D-359](../../../defects.md) and `think-mt4h`. Fixing it re-hashes every stored
SVG and every PNG receipt in the repository, which is a regeneration and a review, not
something to do quietly inside a block about chirality.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
