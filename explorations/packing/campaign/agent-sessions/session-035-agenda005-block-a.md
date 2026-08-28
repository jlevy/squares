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
  deadline_at: '2026-08-28T01:45:00-07:00'
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
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 10
    started_at: '2026-08-28T00:05:00-07:00'
    deadline_at: '2026-08-28T00:15:00-07:00'
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
    outcome: >-
      Precision can be manufactured on demand in-repository. The transcribed system solves
      to 1000 declared digits with a reported residual bound of `1.09829e-1039`, in about
      thirteen seconds, and the residual tracks the working precision across five rungs
      rather than plateauing. Two typed refusals were built and both fire. A third control
      was written, failed to fire for a reason worth keeping, and is retained as a
      measurement rather than deleted.
    evidence:
    - >-
      `promote/refine.py` and `cases/kingbird29/system.py` close the published system in
      its six unknowns by substituting each of the nine slide scalars by its closed form.
      `verify_svg` had transcribed all of it and evaluated residuals against the
      *serialized* scalars, which checks the publication for consistency but cannot yield a
      digit the publication does not already print. Substituting the closed forms is what
      turns the same transcription into something a solver can drive.
    - >-
      'Refinement at 1000 digits: residual `9.82918e-1041`, reported bound `1.09829e-1039`
      at a working precision of 1040 digits. Driver elapsed 13.4s.'
    - >-
      'Residual against declared digits, five rungs: 60 -> `5.00057e-101`, 125 ->
      `1.52625e-165`, 250 -> `5.61167e-291`, 500 -> `1.20367e-540`, 1000 -> `9.82918e-1041`.
      The residual tracks the working precision, which is what a Newton step on a correct
      system does.'
    - >-
      The refined pose moved `2.89737e-99` from its seed, so it agrees with the published
      value across every digit the source prints and then continues past where the
      publication stops. X-004's measurement that roughly ninety-eight available digits
      cannot identify a minimal polynomial is therefore no longer the binding constraint.
    - >-
      'Two typed refusals fire. A seed displaced five degrees in `a` returns
      `left-trust-region`; a square but rank-deficient system, `f6` replaced by a copy of
      `f5`, returns `non-convergent` with mpmath reporting a numerically singular matrix.'
    - >-
      Three negative controls are registered in `devtools/controls.yaml` and all three fire:
      disabling the trust-region check, disabling the squareness check, and disabling the
      plateau comparison each make `tests/test_promote_refine.py` fail with its own message.
      Negative controls rise from 80 to 83.
    - >-
      'A finding, recorded rather than worked around. The wrong-system control as first
      written -- displace one equation by `1e-12` and require the residual to plateau -- does
      not fire. Measured: the displaced system still reaches `1.10229e-290` at 250 digits,
      because a square consistent system perturbed by a constant simply has its own nearby
      root and Newton finds it. So "the residual falls" is close to unfalsifiable here and is
      recorded as an observation, not as a control. The plateau failure mode the spec
      anticipates belongs to an over-determined system, which is what a wrong contact
      structure produces, so detecting it is BC-042 and BC-043 work and not this step''s.'
    - >-
      The known-answer check in `tests/test_promote_refine.py` refines a system whose root
      this repository cannot influence, `x^2 = 2` and `y^2 = 3`, to 200 digits and compares
      against `mpmath`'s own square roots.
    stop_reason: >-
      The declared expected output is complete at minute ten of a seventy-minute budget: a
      refinement past 1000 digits with a reported residual bound, the residual-versus-
      precision series, and a typed refusal from a far seed. The phase closed early rather
      than spending its remaining allocation.
    next_action: >-
      Open the BC-042 lane under think-zmh8 and freeze the n = 29 contact structure, with
      the n = 11 reproduction as the known-answer check on the extraction itself.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-042
    bead: think-zmh8
    objective: >-
      Extract and freeze the measured `n = 29` contact structure as a durable artifact
      carrying its incidences and separations, and reproduce the known `n = 11` structure
      with the same extraction as a known-answer check on the extractor.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The BC-047 lane closed early against its declared output, and block A's second lane is
      independent of it rather than sequenced behind it.
    budget_minutes: 50
    started_at: '2026-08-28T00:15:00-07:00'
    deadline_at: '2026-08-28T01:05:00-07:00'
    expected_output: >-
      A retained contact-structure artifact for `n = 29` carrying its incidences and the
      measured separation, the same extraction reproducing the `n = 11` structure, and a
      perturbation control in which a margin moved to straddle the floor produces a refusal.
    validation_command: >-
      uv run --directory explorations/packing --frozen --all-extras --group dev packing-validate --fast --jobs 2 --inner-jobs 1
    kill_condition: >-
      Stop the lane if the `n = 11` calibration cannot reproduce the known contact structure;
      do not proceed to `n = 29` on an extraction that fails where the answer is known. Stop
      if any incidence is decided by widening the floor rather than by the measured margin.
    fallback: >-
      Retain the measured margins and a typed statement of which incidences the extraction
      cannot decide, rather than a structure whose ambiguous entries were resolved by
      loosening a tolerance.
    outcome: >-
      The `n = 29` contact structure is frozen with its 89 incidences and its measured
      separation, and the same extraction reproduces the known `n = 11` structure exactly.
      The perturbation control fires. One design decision was forced by measurement rather
      than taken on preference: the extractor decides through the injected `sign` rather
      than through any comparison of its own, because exact field elements do not provide
      an ordering and `max` cannot be used on them.
    evidence:
    - >-
      '`promote/contacts.py` classifies every pair and every corner-to-wall relation and
      reports three outcomes rather than two: contact, strict separation, and a refused band
      between the floor and an ambiguity ceiling. `require_decided` turns any occupant of
      that band into a typed `undecidable-incidence` refusal.'
    - >-
      'Frozen at `n = 29`: 52 touching pairs and 37 corner-on-wall incidences, 89 in total,
      across 6 orientation classes, with an empty ambiguity report. These are the counts the
      spec declared in advance.'
    - >-
      'The floor is safe because of the gap around it, not because of its value. The worst
      contact margin is `3.65694e-100` and the smallest strict separation `0.0116001`, which
      is `97.5013` decades apart; the record carries that number so a reader can tell a
      measurement from a guess.'
    - >-
      'Known answer at `n = 11`: 14 touching pairs and 20 corner-on-wall incidences, 34 in
      total, agreeing with `verify_packing` computed independently under `exact_sign`, and 2
      orientation classes splitting 6 axis-aligned and 5 tilted -- Trump''s published
      construction. Under exact arithmetic the ambiguity band is empty by construction, which
      is the correct behaviour rather than a gap in the record.'
    - >-
      'The extraction is the same code at both sizes and only the injected `sign` differs.
      That is what makes the calibration meaningful: an extractor with one arithmetic wired
      in could not be checked against an exact answer at all.'
    - >-
      A design correction the calibration forced. The first draft ordered candidate margins
      with `max`, which works on floats and raises `TypeError` on an exact field element,
      because an ordering on algebraic numbers is itself a sign decision. Ordering now runs
      through the injected `sign`, so the module makes no sign decision of its own.
    - >-
      'Orientation classes are decided by vanishing cross or dot products rather than by
      comparing angles, so the classification is certified over exact scalars and uses no
      `atan2` over any scalar type. The reported degree value is descriptive only and is
      `null` where the scalars do not convert to floats.'
    - >-
      'Perturbation control fires: displacing one square by `1e-75`, above the `1e-80` floor
      and below the `1e-70` ceiling, produces three undecidable incidences and an
      `undecidable-incidence` refusal.'
    - >-
      Three negative controls are registered and all three fire: disabling the ambiguity
      band, neutering `require_decided`, and collapsing the orientation classifier each make
      `tests/test_promote_contacts.py` fail with its own message. Negative controls rise from
      83 to 86, and from 80 across both lanes of this block.
    - >-
      A harness constraint found by running the controls rather than by reading the harness.
      Two controls first pointed at the retained `n = 29` SVG and did not fire, because
      `run_negative_controls` deliberately excludes `resources/` from its worker snapshot to
      stay under a size cap. They were re-pointed at a two-square synthetic pose built in the
      test. A control that cannot run in the harness is not a control.
    - >-
      'Both structures are retained as one soft-schema artifact,
      `atlas/known-best/contact-structures.json` under `ContactStructureAtlas/v1`, generated
      by `devtools.generate_contact_structures` with the usual `--update` / `--check` pair
      and wired into the known-best atlas gate step. The schema records margins and
      separations, not only incidence lists, because an incidence list alone cannot be
      audited: it looks the same whether the contact was certified, measured across
      ninety-seven decades, or chosen at a convenient tolerance.'
    stop_reason: >-
      The declared expected output is complete: a retained artifact at both sizes, the known
      answer reproduced at `n = 11`, and a perturbation control that fires.
    next_action: >-
      Run the full packing-validate at the block boundary, then finalize block A and open
      block B under BC-045 and `think-75ll`.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: finalization
    focus: process
    objective: >-
      Reconcile block A: run the full packing-validate rather than `--fast`, regenerate the
      views whose sources changed, verify them after the commit, and leave the block closed
      with an exact next action for block B.
    status: in_progress
    entered_by: planned_checkpoint
    switch_reason: >-
      Both block-A lanes closed against their declared outputs well inside their budgets, so
      the block boundary arrived early; this phase opens no new research.
    budget_minutes: 40
    started_at: '2026-08-28T01:05:00-07:00'
    deadline_at: '2026-08-28T01:45:00-07:00'
    expected_output: >-
      A green full gate on the block-A revision, regenerated ledger and document views, a
      commit on `packing/overnight-agenda-005` pushed to the remote, and updated beads.
    validation_command: >-
      uv run --directory explorations/packing --frozen --all-extras --group dev packing-validate --jobs 2 --inner-jobs 1
    kill_condition: >-
      Stop and report if the full gate is red twice; do not substitute a hand-check for it
      because the machine is loaded, and do not open new research inside a finalization phase.
    fallback: >-
      Commit the retained evidence with the gate result recorded as red and stop the session
      rather than carrying an unvalidated block boundary into block B.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: >-
      Open block B as session-036 under BC-045 and `think-75ll`, phases 1 and 2 of
      plan-2026-08-28-interval-certification.
  primary_bead: think-y85e
  status: in_progress
  budget:
    wall_minutes: 100
    max_cycles: 8
    slice_minutes: 30
    orientation_minutes: 10
    checkpoint_minutes: 20
    finalization_minutes: 40
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

| Slot | Window | Objective | Lane | Outcome |
| --- | --- | --- | --- | --- |
| 1 | 00:05–00:15 | Orientation: handoff, agenda, specs, baseline | — | Complete on entry; baseline green |
| 2 | 00:05–00:15 | `promote/refine.py` over the transcribed system | BC-047 | Closed: 1000 digits, residual `9.82918e-1041` |
| 3 | — | Residual series and the far-seed control | BC-047 | Folded into slot 2; the lane closed at minute ten |
| 4 | 00:15–01:02 | `promote/contacts.py`, freeze, calibrate, control | BC-042 | Closed: 89 incidences at `n = 29`, 34 at `n = 11` |
| 5 | 01:05–01:45 | Finalization: full gate, views, commit, push, beads | — | This phase |

The plan allocated four hours and eight slots.
Both lanes closed inside ninety minutes, so the later slices were revised from measured
elapsed time rather than spent: the session deadline moved from `04:05` to `01:45` and
the finalization reserve grew from twenty-five minutes to forty.
The cap was an inventory point, not a quota.

The recorded phase budgets are the revised ones, not the originally declared maxima.
Phase 1 was allocated seventy minutes and closed at minute ten against its declared
output; phase 2 was allocated ninety and closed at minute forty-seven.
Each was cut at the boundary that followed it, from measured elapsed time, which is the
direction the session guide allows -- a lease may be shortened once its work is done and
may never be extended after the fact.

## What this block may not claim

Nothing here certifies anything.
BC-047 reports precision and no algebraic claim; BC-042 freezes a measurement and infers
nothing that the measured separation does not already decide.
The certification question belongs to blocks B and C under BC-045.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
