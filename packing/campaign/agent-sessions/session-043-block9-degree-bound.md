---
title: session-043 — agenda-006 block 9, how high the search would have to reach
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-043
  title: Rationalise the n = 29 system and bound the algebraic degree of s(29)
  date: '2026-08-29'
  started_at: '2026-08-29T01:01:48-07:00'
  deadline_at: '2026-08-29T01:46:48-07:00'
  goal: >-
    Establish whether the integer-relation refusal at n = 29 surveyed the space or a
    corner of it, by rationalising the published closed system and computing a bound on
    the algebraic degree of s(29) -- the half of BC-060's declared scope the
    integer-relation route could not reach.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-065
    bead: think-obgk
    objective: >-
      Make the one transcription serve a third arithmetic, rationalise the system by the
      half-angle substitution, and compute what bounds the degree.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 25
    started_at: '2026-08-29T01:01:48-07:00'
    deadline_at: '2026-08-29T01:26:48-07:00'
    expected_output: >-
      Six polynomials over Q in six unknowns, their degrees, and a bound that says whether
      degree twenty was a survey or a corner.
    validation_command: >-
      uv run --frozen --group dev python -m pytest tests/test_promote_system_degree.py -q
    kill_condition: >-
      Stop if the polynomials carry anything transcendental or any coefficient that is not
      exactly rational. A bound computed over an opaque generator is not a bound, and an
      elimination over floats is not exact.
    fallback: >-
      Record which part of the transcription resists rationalisation rather than a bound
      whose inputs were not checked.
    outcome: >-
      Bounded, and the answer settles the question. Six polynomials over Q with total
      degrees `[11, 15, 10, 15, 7, 6]`, so the Bezout bound on the solution variety is
      `1,039,500`. Degree twenty was a corner of the space, not a survey of it.
    evidence:
    - >-
      '`sin_degrees` and `cos_degrees` now dispatch to SymPy as well as to floats and
      intervals, so the same six-equation transcription serves all three routes. The
      symbolic arm is a branch rather than a fall-through because `mp.radians` raises on a
      SymPy symbol -- which is how the route was unavailable without anything reporting
      it.'
    - >-
      'Every equation is degree **one** in `s`, which is the structural fact an
      elimination starts from. Solving the smallest for `s` gives it as a rational
      function of `u_b` and `u_c` alone -- three of the five half-angles do not appear --
      and leaves five equations in five unknowns with degrees `[16, 20, 15, 20, 12]`.'
    - >-
      'What this does *not* do is the elimination itself. A resultant chain over five
      variables at these degrees is where the route either succeeds or is shown to be out
      of reach, and that is a measurement with its own budget rather than a step taken in
      passing.'
    - >-
      'Read as "not small" rather than "this large". Bezout is an upper bound and is loose
      for a structured system, so the true degree may be far below a million. It is not,
      on any reading, twenty.'
    stop_reason: criterion
    next_action: >-
      Correct the first number this block produced, then close it.
  - workflow: process-review
    recording: contemporaneous
    clock_role: finalization
    focus: correctness
    commitment: BC-065
    bead: think-obgk
    objective: >-
      Correct the bound this block first reported, register controls for the two ways it
      was computed wrongly, and leave the checkpoint pushed.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The bound is in hand; what remains is that the first version of it was wrong and
      said so to the user before the tool existed.
    budget_minutes: 20
    started_at: '2026-08-29T01:26:48-07:00'
    deadline_at: '2026-08-29T01:46:48-07:00'
    expected_output: Controls that fire, a corrected number, and a green gate.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: Stop if a control is registered without having been watched to fire.
    fallback: Push with the failing step named.
    outcome: >-
      Corrected from `12,690,480` to `1,039,500`. Three controls registered and all three
      fire; two needed retargeting against what the mutation actually reports.
    evidence:
    - >-
      'The first computation of this bound was a throwaway script and it was wrong. It
      reported degrees `[11, 20, 23, 22, 19, 6]` for a Bezout bound of `12,690,480`,
      because composing rotations adds angles and the raw equations therefore contain
      `cos(b - i)` and similar. Substituting only `sin(a)` and `cos(a)` leaves those
      alone, and `Poly` then treats each as an opaque generator. `expand_trig` first is
      what makes the substitution complete rather than merely plausible.'
    - >-
      'The tool caught it, which is the argument for the tool. The script had already
      reported its number and it had already been repeated in conversation; the guard that
      refuses a non-rational coefficient is what surfaced the surviving `cos(b - i)`
      term.'
    - >-
      'Second way it was wrong: the transcription writes its constants as `mp.mpf(1)`,
      which arrive in the symbolic branch as SymPy `Float`s. A Groebner basis or resultant
      over floats is a numerically unstable computation wearing an exact answer''s
      clothes, so every coefficient is converted to an exact rational and a conversion
      that is not exact is a refusal.'
    - >-
      'Two of the three controls needed retargeting, which is why each is watched rather
      than assumed. The unexpanded-angle mutation is caught by the rational-coefficient
      guard before the trig assertion is reached; and mutating a converted coefficient is
      *not* a control at all, because `Poly.from_dict(domain=QQ)` coerces a small integer
      float to the same rational either way. What is testable is that the declared domain
      is load-bearing, so the control changes `QQ` to `RR`.'
    stop_reason: criterion
    next_action: >-
      Open block 11 as session-044 under BC-066 and `think-obgk`.
  primary_bead: think-qs6k
  status: completed
  budget:
    wall_minutes: 45
    orientation_minutes: 3
    checkpoint_minutes: 5
    slice_minutes: 25
    finalization_minutes: 20
  stop_conditions:
  - The block deadline at 2026-08-29T01:46:48-07:00
  - Any polynomial carrying a transcendental term or a non-rational coefficient
  - Attempting the five-variable elimination, which needs its own budget
  progress:
    metric: >-
      Whether the degree-twenty integer-relation refusal can be read as a survey
    before: >-
      No. The refusal was real and its scope was unknown, because nothing said what degree
      s(29) actually has.
    after: >-
      It cannot. The rationalised system bounds the solution variety at 1,039,500 by
      Bezout, so degree twenty surveyed a corner. The elimination that would give the true
      degree is set up and not attempted.
  delegations: []
  outputs:
  - src/sqpack/promote/interval.py
  - devtools/probe_system_degree.py
  - tests/test_promote_system_degree.py
  - tests/test_promote_krawczyk.py
  - devtools/controls.yaml
  checks:
  - 'rationalised degrees [11, 15, 10, 15, 7, 6]; Bezout 1,039,500; all degree 1 in s'
  - 'after eliminating s: 5 equations in 5 unknowns, degrees [16, 20, 15, 20, 12]'
  - 's is a rational function of u_b and u_c alone'
  - 'uv run --frozen --group dev python -m devtools.run_negative_controls -k "symbolic system": 2 of 2 fire'
  - 'uv run --frozen --group dev python -m devtools.run_negative_controls -k "trig dispatch": fires'
  stop_reason: >-
    The bound is measured, pinned by a test, and the number this block first reported is
    corrected. The elimination itself is deliberately left to its own budget.
  next_action: >-
    Open block 11 as session-044 under BC-066 and `think-obgk`: eliminate the five
    equations in five half-angles this block left, inside a declared wall-clock cap, and
    record whatever the chain reaches. It runs before the remaining pipeline blocks because
    it is the only one that can change what this run concludes about n = 29 -- a refusal
    there is the measured justification for the interval route carrying that bound. The
    ordering through block 18 is agenda-006's continuation schedule.
---
# session-043 — block 9, how high the search would have to reach

Block 9 of [agenda-006](../agendas/agenda-006-overnight-research-blocks.md), and the
half of `BC-060`’s declared scope the integer-relation route could not reach.

## The question the refusal left open

[session-042](session-042-block8-exact-solve.md) found no relation for `s(29)` through
degree twenty below a coefficient bound of `10^22`, on a thousand digits.
That is a real result and it is easy to over-read, because the reach of such a search is

```
(d + 1) · log10(C)  <  P − M
```

so pushing the degree up buys only *smaller* coefficients — and higher-degree algebraic
numbers have larger heights, not smaller.
Whether degree twenty was a survey or a corner is a question about the system, not about
the search.

## Rationalising the system

The published system is six equations in `{s, a, b, c, d, i}` with five of the unknowns
appearing through sines and cosines.
Under `u = tan(θ/2)` every trigonometric term becomes rational, and clearing
denominators leaves six honest polynomials over `Q`:

|  | f1 | f2 | f3 | f4 | f5 | f6 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| total degree | 11 | 15 | 10 | 15 | 7 | 6 |
| degree in `s` | 1 | 1 | 1 | 1 | 1 | 1 |
| terms | 95 | 214 | 69 | 364 | 25 | 20 |

**Bézout bound on the solution variety: `11 × 15 × 10 × 15 × 7 × 6 = 1,039,500`.**

Read that as “not small” rather than “this large” — Bézout is an upper bound and is
loose for a structured system.
What it settles is the question it was asked.
The degree of `s(29)` is not twenty.

The same transcription served all of this, because
[`sin_degrees`](../../src/sqpack/promote/interval.py) now dispatches to SymPy as well as
to floats and intervals.
A second copy of a six-equation contact system would be a second thing to keep correct.

## What the structure offers an elimination

Every equation is degree **one** in `s`. Solving the smallest for `s` gives it as a
rational function of `u_b` and `u_c` alone — three of the five half-angles do not appear
— and leaves five equations in five unknowns with degrees `[16, 20, 15, 20, 12]`.

That is where the route either succeeds or is shown to be out of reach, and it is
deliberately not attempted here: a resultant chain over five variables at these degrees
is a measurement with its own budget.

## The number this block first got wrong

The first computation of this bound was a throwaway script, it reported
`[11, 20, 23, 22, 19, 6]` for a Bézout bound of **`12,690,480`**, and that number had
already been said out loud before the tool existed.

Composing rotations adds angles, so the raw equations contain `cos(b − i)` and similar.
Substituting only `sin(a)` and `cos(a)` leaves those untouched and `Poly` treats each as
an opaque generator.
`expand_trig` first is what makes the substitution complete rather than merely
plausible.

The guard that refuses a non-rational coefficient is what surfaced it — the script had
no such guard, which is the whole argument for putting a cited measurement in a tool.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
