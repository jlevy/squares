---
title: session-035 — agenda-005 block A, precision on demand and a frozen contact structure
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-035
  title: Manufacture precision from the published n = 29 system, and freeze the contact structure it rests on
  date: '2026-08-28'
  started_at: '2026-08-28T00:05:00-07:00'
  deadline_at: '2026-08-28T04:05:00-07:00'
  goal: >-
    Close agenda-005 block A by running its two independent lanes: BC-047 turns the
    already-transcribed n = 29 contact system into a refinement instrument that reports its
    own residual, and BC-042 freezes the measured n = 29 contact structure as a durable
    artifact while reproducing the known n = 11 structure as a known-answer check. Together
    they answer the block checkpoint question — can precision be manufactured on demand
    in-repository, and is the contact structure frozen at both sizes.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-047
    bead: think-y85e
    objective: >-
      Build `promote/refine.py` and drive the closed n = 29 system already transcribed in
      `cases/kingbird29/verify_svg.py` to a declared precision of 1000 digits or more,
      reporting a residual bound rather than assuming one, and verifying that the residual
      falls with precision as a Newton step should.
    status: in_progress
    entered_by: session_start
    switch_reason: null
    budget_minutes: 70
    started_at: '2026-08-28T00:05:00-07:00'
    deadline_at: '2026-08-28T01:15:00-07:00'
    expected_output: >-
      A `refine(system, seed, digits)` entry point returning a solution and a reported
      residual bound, a recorded refinement at n = 29 to 1000+ digits, a residual-versus-
      precision series showing the expected fall, and a negative control in which a seed far
      from the root produces a typed non-convergence rather than a silently returned value.
    validation_command: >-
      uv run --directory explorations/packing --frozen --all-extras --group dev packing-validate --fast --jobs 2 --inner-jobs 1
    kill_condition: >-
      Stop if the residual plateaus rather than falling with precision, which indicates a
      wrong system and must be reported as such rather than worked around; stop if the
      refinement is made to succeed by loosening a tolerance; stop if a claim about the
      algebraic nature of the root is made at this step, which reports precision only.
    fallback: >-
      Retain the measured residual-versus-precision series and a typed statement of which
      conditioning prevents the declared precision, rather than reporting a refined value
      whose residual is not bounded.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: >-
      On completion, open the BC-042 lane under think-zmh8 and freeze the n = 29 contact
      structure; on a typed refusal, record it and still open BC-042, which is independent.
  primary_bead: think-y85e
  status: in_progress
  budget:
    wall_minutes: 240
    max_cycles: 8
    slice_minutes: 30
    orientation_minutes: 10
    checkpoint_minutes: 20
    finalization_minutes: 25
  stop_conditions:
  - A typed refusal is a valid ending; an inference that cannot decide an incidence, or a checker defeated by conditioning, is recorded as a finding and not worked around by loosening a tolerance.
  - If the n = 11 calibration under BC-042 cannot reproduce the known contact structure, the lane stops rather than proceeding to n = 29 on an inference that fails where the answer is known.
  - No scientific verdict is accepted by this runner; anything needing a human accept decision is recorded unresolved with needs_review true.
  - The full gate runs at the block boundary in the background, never inside a foreground command with a short limit, and a hand-check is never substituted for it because the machine is loaded.
  - A quota or API failure halts the run; it is not retried on a timer.
  - Two consecutive blocks closing zero commitments stops the agenda for replanning.
  progress:
    metric: agenda-005 block A commitments closed, with each lane's instrument pinned by a control that is verified to fire
    before: >-
      No `promote/` package exists. Precision at n = 29 is read from the serialized source
      rather than manufactured, and X-004 measured that the roughly ninety-eight available
      digits cannot identify a minimal polynomial. The n = 29 contact structure is measured
      but not frozen as a durable artifact, and no extraction has been checked against the
      known n = 11 answer.
    after: null
  delegations: []
  outputs:
  - campaign/agent-sessions/session-035-agenda005-block-a.md
  checks:
  - 'Baseline before target work: `packing-ledger check` reports OK across 1 series, 4 reports, 48 hypotheses, 45 rounds, 34 agent sessions, 5 agendas, 1 logbook entries.'
  - 'Baseline `packing-validate --fast --jobs 2 --inner-jobs 1` was started before target work and its result is recorded in phase evidence when it lands.'
  - 'The branch is `packing/overnight-agenda-005`, cut from the head of PR 53 (`70770c2`), which already contains `origin/main` at `8f21bd9`; the merge of main was therefore a no-op and is recorded as one rather than as an integration.'
  stop_reason: null
  next_action: >-
    Continue the active slice: BC-047 under `think-y85e`, driving the transcribed n = 29
    system to a declared precision with a reported residual bound. The block's second lane,
    the contact-structure freeze, opens after it and is independent of its outcome. At the
    block boundary run the full packing-validate, not --fast, then finalize, commit and push
    before the 04:05 deadline.
---
# Session 035 — Agenda-005 Block A

Block A is two independent lanes, not a sequence.
Neither gates the other, and neither gates blocks B and C.

## Why this block can start at `n = 29` without an assembler

The earlier plan sequenced extraction and assembly ahead of refinement, on the premise
that precision had to come from a system this repository assembles.
[X-004](../explorations/X-004-n29-exact-promotion.md) withdrew that premise on
measurement. The provenance SVG publishes the closed system — nine slide scalars in
closed form and six equations `f1 … f6` in `{s, a, b, c, d, i}` — and the symbolic
layout map with it, and
[`cases/kingbird29/verify_svg.py`](../../cases/kingbird29/verify_svg.py) has already
transcribed both. It evaluates residuals and never solves.
BC-047 drives that existing transcription, which is why it is `ready` rather than
`blocked` behind BC-042 and BC-043.

## The slot plan

One absolute deadline at `04:05`, no slot over thirty minutes, and at least fifteen
minutes of protected finalization.
Only slot 2 is frozen; every later slot is a maximum allocation to be revised from
measured elapsed time at each boundary.

| Slot | Window | Objective | Lane | Expected evidence | Defer or kill rule |
| --- | --- | --- | --- | --- | --- |
| 1 | 00:05–00:15 | Orientation: handoff, agenda, specs, baseline | — | Baseline commands recorded | Already complete on entry |
| 2 | 00:15–00:45 | `promote/refine.py` over the transcribed system | BC-047 | A refinement at 1000+ digits with a reported residual | Kill if the residual plateaus; that is a wrong-system finding |
| 3 | 00:45–01:15 | Residual-versus-precision series and the far-seed control | BC-047 | Typed non-convergence from a far seed | Defer the series to finalization if the control is not yet typed |
| 4 | 01:15–01:45 | `promote/contacts.py` extraction and classification | BC-042 | Pair, wall and angle-class counts at `n = 29` | Kill on any incidence decided by widening the floor |
| 5 | 01:45–02:15 | Freeze `n = 29`; reproduce `n = 11` as a known answer | BC-042 | 52 pair, 37 wall, 6 angle classes, empty `ambiguous` | Stop the lane if `n = 11` does not reproduce |
| 6 | 02:15–02:45 | Perturbation control and retained artifacts | BC-042 | A straddling margin produces a refusal | Defer the artifact shape, never the control |
| 7 | 02:45–03:15 | Full `packing-validate`, not `--fast` | — | Green gate on the block boundary | Wait for it; never substitute a hand-check |
| 8 | 03:15–03:40 | Reserve | — | — | Unused reserve rolls into finalization |
| 9 | 03:40–04:05 | Finalization: records, generated views, commit, push, beads | — | Durable checkpoint on the remote branch | Protected; not spent on new research |

## What this block may not claim

Nothing here certifies anything.
BC-047 reports precision and no algebraic claim; BC-042 freezes a measurement and infers
nothing that the measured separation does not already decide.
The certification question belongs to blocks B and C under BC-045.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
