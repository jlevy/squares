---
title: session-041 — agenda-006 block 7, the shortfall was a missing equation
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-041
  title: Derive the stationarity conditions, and find there are none to derive
  date: '2026-08-29'
  started_at: '2026-08-28T23:55:59-07:00'
  deadline_at: '2026-08-29T00:55:59-07:00'
  goal: >-
    Close agenda-006 block 7 by deriving the closure conditions `close` has only ever
    sized -- one at n = 5, four at n = 11, seven at n = 29 -- into a form a solver
    accepts, or by stating which formulation the contact graph resists.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-059
    bead: think-9c40
    objective: >-
      Find out what the null space of the contact Jacobian actually describes, by walking
      the direction that most decreases the side and watching the packing, before writing
      down any condition.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 25
    started_at: '2026-08-28T23:55:59-07:00'
    deadline_at: '2026-08-29T00:20:59-07:00'
    expected_output: >-
      A characterisation of the flex directions in terms of what they do to the packing,
      not in terms of what the rank says about them.
    validation_command: >-
      uv run --frozen --group dev python -m pytest tests/test_promote_system.py -q
    kill_condition: >-
      Stop before writing a condition whose only justification is that it makes the counts
      meet. A closure that is not derived from the geometry is an invented constraint.
    fallback: >-
      Record which formulation the graph resists rather than shipping a determinant whose
      correctness rests on the shortfall it was sized to fill.
    outcome: >-
      There was nothing to derive at either large size, because the shortfall was a bug.
      An `edge-edge` contact was assembled as one equation where collinearity is two.
      With the second, the contact Jacobian reaches full rank at n = 11 and n = 29 and
      `close` refuses at both.
    evidence:
    - >-
      'Walking the null direction that most decreases the side, at n = 11: along `+v` the
      packing is violated at `O(t^2)` -- `-1.36e-7`, `-1.36e-9`, `-1.36e-11` at steps
      `1e-3`, `1e-4`, `1e-5` -- which is a second-order obstruction. Along `-v`, the
      direction that matters for optimality, it is violated at `O(t)`: `-5.12e-4`,
      `-5.12e-5`, `-5.12e-6`. A first-order violation of a constraint whose equation has
      zero derivative along `v` means the equation is not the constraint.'
    - >-
      'The violating pairs named themselves. All three worst were declared contacts and
      all three were typed `edge-edge`: `(8,9)`, `(7,9)`, `(6,7)`. Nothing else in the
      typing behaved this way.'
    - >-
      'Coincident lines in the plane are two conditions -- the edges parallel and one
      point shared -- and assembly wrote one, putting a single endpoint of the right edge
      on the left edge''s line. That says the lines *meet*. It leaves the right square
      free to pivot about that point, which is precisely the motion measured above.'
    - >-
      'With both endpoints on the line: n = 11 goes from rank 30 of 34 to **34 of 34**,
      n = 29 from 81 of 88 to **88 of 88**, and the projection of `e_s` onto the null
      space falls from `1.86e-1` and `1.14e-1` to exactly zero at both. The residuals do
      not move -- `8.9e-16` and `1.3e-15` -- so the added equations are true at the poses
      they were assembled from, which is what makes this a repair rather than a
      constraint invented to make the counts meet.'
    - >-
      'Göbel''s n = 5 has no `edge-edge` contact at all. It is untouched by the repair and
      keeps its shortfall of one, which is now the only size where a stationarity
      condition still has to be derived -- and the only clean case to derive it on.'
    stop_reason: criterion
    next_action: >-
      Land the repair, then correct every record that carried the shortfall as a fact
      about the mathematics.
  - workflow: process-review
    recording: contemporaneous
    clock_role: finalization
    focus: process
    commitment: BC-059
    bead: think-9c40
    objective: >-
      Land the second equation with controls, and correct the four artifacts that recorded
      the shortfall as a property of the packings rather than of the assembler.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: The measurement reached its criterion and the repair follows from it.
    budget_minutes: 35
    started_at: '2026-08-29T00:20:59-07:00'
    deadline_at: '2026-08-29T00:55:59-07:00'
    expected_output: >-
      Controls that fire, corrected records, and a green gate.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: >-
      Stop if the n = 5 shortfall moves. It is the control on the repair: a change that
      alters a size with no edge-edge contact is doing something other than fixing
      edge-edge.
    fallback: Push with the failing step named.
    outcome: >-
      Landed. n = 5 is unmoved at shortfall one, both new controls fire, and D-361 records
      what the bug cost the record.
    evidence:
    - >-
      'Two controls. One restores the single-endpoint equation and requires the n = 11
      equation count to move; the other disables `close`''s `already-determined` guard and
      requires the test to catch a closure invented for a determined system. Controls rise
      103 to 105.'
    - >-
      'A third control was written and withdrawn rather than kept. It faked `side_leak` to
      zero, and it cannot fire: after the repair the true leak *is* zero at every size, so
      a mutation reporting zero is indistinguishable from the truth. What replaced it is
      better -- the checks in `main` are ordered so the leak assertion runs before the
      equation count, which makes the edge-edge control prove that a contact-preserving
      motion can now shrink the container rather than merely that a count moved.'
    - >-
      'A public `side_leak` came out of this. `jacobian_rank` now reports the norm of the
      projection of the side''s unit vector onto the null space, because that is the
      number the whole block turned on and it belongs in the measurement rather than in a
      test reaching into a private helper.'
    - >-
      '`close`''s `already-determined` refusal had **no case** when it was written, and
      `tests/test_promote_system.py` said so in as many words rather than contriving one.
      It has two now, and that the branch went from unreachable to reached by fixing an
      equation is the clearest evidence the shortfall it used to report was an artefact.'
    - >-
      'D-361, class `soundness`, direction `conservative`. The error made the pipeline
      look further from a solvable system than it was, and it blocked BC-060, which needs
      a square system to work on. It is the reason session-040''s null-space section, this
      run''s SYNOPSIS handoff and BC-059''s own framing all now carry corrections.'
    - >-
      'The n = 29 interval certificate is untouched by this, and that is worth stating
      rather than leaving a reader to work out. It was produced from the *published*
      Kingbird system -- six equations in `{s, a, b, c, d, i}` transcribed from the source
      -- not from the contact system assembled here. D-361 is a defect in assembly, and
      assembly has never been in the certificate''s path.'
    - >-
      'The consumer contract caught this session record too, for the third time in this
      run: a stop condition naming `verified_upper_bound` without declaring what the
      record takes the field to mean. Three catches in three attempts is the check earning
      its keep rather than a nuisance.'
    - >-
      'The correction reaches a conclusion drawn one block earlier. session-040 measured
      the same projections and concluded that no first-order stationarity condition could
      close n = 11 or n = 29, which followed correctly from the numbers and was wrong
      because the system they came from was wrong. Its measurements stand; its
      interpretation is superseded, and the record says so where it was written.'
    stop_reason: criterion
    next_action: >-
      Open block 8 as session-042 under BC-060 and `think-ovp7`, which this unblocks.
  primary_bead: think-9c40
  status: completed
  budget:
    wall_minutes: 60
    orientation_minutes: 3
    checkpoint_minutes: 7
    slice_minutes: 25
    finalization_minutes: 35
  stop_conditions:
  - The block deadline at 2026-08-29T00:55:59-07:00
  - Any movement in the n = 5 shortfall, which is the control on the repair
  - A closure condition written down whose justification is that it makes the counts meet
  - Any move of verified_upper_bound, which is a human decision
  progress:
    metric: >-
      Whether the assembled contact system determines the pose it was assembled from
    before: >-
      No, and the gap was misnamed. `close` reported four missing stationarity conditions
      at n = 11 and seven at n = 29, described as Lagrange or Fritz-John determinants.
    after: >-
      Yes at both. The contact Jacobian has full rank once `edge-edge` contributes the
      collinearity it always meant, and `close` refuses to add anything. n = 5 keeps a
      genuine shortfall of one, which is the remaining derivation.
  delegations: []
  outputs:
  - src/sqpack/promote/system.py
  - tests/test_promote_system.py
  - devtools/controls.yaml
  - defects.yaml
  - campaign/agent-sessions/session-040-block6-chirality.md
  checks:
  - 'n = 11: rank 34/34, shortfall 0, residual 8.88e-16, close refuses already-determined'
  - 'n = 29: rank 88/88, shortfall 0, residual 1.33e-15'
  - 'n = 5 unmoved: shortfall 1, closure 1, residual 1.11e-16'
  - 'projection of e_s onto null(A): 0 at n = 11 and n = 29, was 1.86e-1 and 1.14e-1'
  - 'uv run --frozen --group dev python -m devtools.run_negative_controls: 105 registered, both new ones fire; a third was written and withdrawn as unable to fire'
  - 'the n = 29 interval certificate is not in assembly''s path and is unaffected by D-361'
  stop_reason: >-
    The measurement reached its criterion and the repair it implied is landed, inside the
    block clock read from `date -u` at each boundary.
  next_action: >-
    Open block 8 as session-042 under BC-060 and `think-ovp7`, which this unblocks: n = 29
    is now an overdetermined, full-rank system of 122 contact equations in 88 unknowns,
    which is what an exact solve needs.
---
# session-041 — block 7, the shortfall was a missing equation

Block 7 of [agenda-006](../agendas/agenda-006-overnight-research-blocks.md).
The commitment was to derive the stationarity conditions
[`close`](../../src/sqpack/promote/system.py) has only ever counted.
There were none to derive at the sizes that matter, and finding that out is the block.

## Walking the flex before writing anything down

`close` reported the contact system four conditions short at `n = 11` and seven at
`n = 29`, and the previous block had gone as far as concluding — correctly, from those
numbers — that no *first-order* condition could close either, because the null space
contained directions that change the side.

Rather than write a determinant, this block stepped along the worst such direction and
looked at the packing.

| step `t` | side | worst pair separation |
| ---: | ---: | ---: |
| `+1e-3` | 3.877269600145 | `-1.364e-07` |
| `+1e-4` | 3.877102191035 | `-1.364e-09` |
| `+1e-5` | 3.877085450124 | `-1.364e-11` |
| `-1e-3` | 3.876897579901 | `-5.123e-04` |
| `-1e-4` | 3.877064989011 | `-5.123e-05` |
| `-1e-5` | 3.877081729922 | `-5.123e-06` |

Going one way the violation is `O(t²)` — a second-order obstruction, which is what one
expects. Going the other, the direction that would *shrink the container*, it is `O(t)`.

A constraint violated at first order along a direction where its own equation has zero
derivative is not being described by that equation.

## What was wrong

The three worst-violating pairs were all declared contacts, and all three were typed
`edge-edge`.

Two coincident lines in the plane are **two** conditions: the edges parallel, and one
point shared.
Assembly wrote one — a single endpoint of the right edge on the left edge’s
line — which says the lines *meet*. That leaves the right square free to pivot about
that point, and the pivot is exactly the motion in the table.

With both endpoints on the line:

|  | rank before | rank after | ‖proj of `e_s` onto null(A)‖ |
| --- | ---: | ---: | ---: |
| `n = 11` | 30 / 34 | **34 / 34** | `1.86e-1` → `0` |
| `n = 29` | 81 / 88 | **88 / 88** | `1.14e-1` → `0` |

The residuals do not move — `8.9e-16` and `1.3e-15` — so the added equations are true at
the poses they were assembled from.
That is what separates a repair from a constraint invented to make the counts meet.

## What this costs the record

The shortfall was reported as a property of the packings and was a property of the
assembler. [D-361](../../../defects.md) carries it: class `soundness`, direction
`conservative`, because it made the pipeline look further from a solvable system than it
was.

It also reaches backwards.
[session-040](session-040-block6-chirality.md) measured these same projections one block
earlier and concluded that no first-order stationarity condition could close either
size. That followed correctly from the numbers and is wrong, because the system the
numbers came from was wrong.
Its measurements stand; the interpretation is superseded, and the correction is written
where the claim was made rather than only here.

## What this does not touch

The `n = 29` interval certificate came from the *published* Kingbird system — six
equations in `{s, a, b, c, d, i}`, transcribed from the source — not from the contact
system assembled here.
`D-361` is a defect in assembly, and assembly has never been in that certificate’s path.
The bound stands exactly as recorded, and so does the fact that nothing has promoted it.

## What is left

Göbel’s `n = 5` has no `edge-edge` contact at all.
It is untouched by the repair, keeps a genuine shortfall of one, and is now both the
only size where a stationarity condition still has to be derived and the cleanest case
to derive it on.

`close`’s `already-determined` refusal, which had no case when it was written and which
the test file said so of rather than contriving one, now has two.

One control was written and withdrawn.
It faked `side_leak` to zero, and after the repair the true leak *is* zero everywhere —
so the mutation is indistinguishable from the truth and the control can never fire.
Reordering the checks so the leak assertion runs before the equation count did the job
instead, and did it better: restoring the bug now trips an assertion about the geometry
rather than one about a count.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
