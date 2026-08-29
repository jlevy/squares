---
title: session-038 — agenda-006 block 3, contact features and system assembly
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-038
  title: Identify which features meet, assemble the contact equations, and measure what they leave
  date: '2026-08-29'
  started_at: '2026-08-29T02:35:00-07:00'
  deadline_at: '2026-08-29T05:35:00-07:00'
  goal: >-
    Close agenda-006 block 3 by building the unbuilt middle of the exact route: extraction
    that identifies which features realise each contact, assembly that turns a structure
    into scalar equations, and a measurement of whether those equations determine the
    packing or leave it short. The block question is what the contact graph actually
    supports, not whether an exact value comes out.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-054
    bead: think-zm3f
    objective: >-
      Extend `promote/contacts.py` to identify the realising feature pair of every contact
      and refuse when it is not unique, which the promotion spec names as a prerequisite
      for assembly and which the frozen structure did not carry.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 60
    started_at: '2026-08-29T02:35:00-07:00'
    deadline_at: '2026-08-29T03:35:00-07:00'
    expected_output: >-
      Every contact typed `corner-edge`, `edge-edge`, `corner-corner` or `corner-wall`
      with both features named, reproducing the known n = 11 counts and extending to
      n = 29 without ambiguity.
    validation_command: >-
      uv run --frozen --group dev python -m pytest tests/test_promote_system.py -q
    kill_condition: >-
      Stop if a contact is typed by picking one of several candidate readings rather than
      by a rule that decides; stop if the typing is tuned to n = 11 and does not survive a
      second packing.
    fallback: >-
      Report which contacts cannot be typed and why, rather than a structure whose types
      are guesses.
    outcome: >-
      Built. n = 11 types as 7 edge-edge, 6 corner-edge and 1 corner-corner across its 14
      zero-gap pairs, with 20 corner-wall relations; n = 29 types as 28, 19 and 5 across
      52 pairs with 37 wall relations, matching BC-042's frozen counts exactly.
    evidence:
    - >-
      'A first implementation read the supporting corners off each realising axis
      separately, and that is wrong in a way n = 11 exhibits: squares 4 and 5 touch at a
      single point, and per-axis they support a full edge each on both x and y. Read that
      way the pair is two different edge-edge contacts, and the packing has neither.
      Intersecting the supports across every realising axis gives the corner-corner contact
      those squares actually have.'
    - >-
      The extractor refuses rather than choosing when the intersection is not a corner or
      an edge, and the refusal is typed `degenerate-contact`.
    - >-
      'The typing is not tuned to one packing: Göbel''s n = 5 types cleanly under the same
      rule, and n = 29 reproduces the 52 pair and 37 wall counts frozen in session-035 by
      a separate extraction.'
    stop_reason: criterion
    next_action: >-
      Enter phase 2 and assemble the equations these features determine.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-054
    bead: think-zm3f
    objective: >-
      Build `promote/system.py`: one scalar equation per corner-edge, edge-edge and wall
      contact, two per corner-corner contact, and a measurement of whether the resulting
      system determines the pose.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      Features are identified, which is assembly's entry condition; the objective changes
      from describing contacts to writing equations.
    budget_minutes: 75
    started_at: '2026-08-29T03:35:00-07:00'
    deadline_at: '2026-08-29T04:50:00-07:00'
    expected_output: >-
      Equations that vanish at the packing they were extracted from, a reported count of
      what they leave, and a closure sized by whatever that is.
    validation_command: >-
      uv run --frozen --group dev python -m pytest tests/test_promote_system.py -q
    kill_condition: >-
      Stop if a closure is added to make counts meet rather than to take up a measured
      shortfall; stop if the equations do not vanish at the known pose, which means
      assembly wrote down a different system.
    fallback: >-
      Report the residual and the rank and say what they imply, rather than a system
      presented as solvable.
    outcome: >-
      Built, and three things came out against what the spec expected. The equations vanish
      at Trump's pose to `4.44e-16`, the raw system is overdetermined by the count and
      four conditions short by the rank, and the n = 29 layout turns out to contain squares
      this pose model cannot represent at all.
    evidence:
    - >-
      'The decisive check is not a count but a residual: assembled from the extracted
      structure, the equations vanish at the n = 11 packing to `4.44e-16` and at Göbel''s
      n = 5 to the same order. Retyping a single contact drives the residual above `1e-6`,
      so the check discriminates rather than merely passing.'
    - >-
      'Counting rows is the wrong instrument, measured. At n = 11 there are 35 contact
      equations against 34 unknowns -- overdetermined -- while the Jacobian has rank 30. The
      system is redundant *and* four conditions short at the same time. The spec''s phase-2
      control proposes requiring the unclosed system to be reported underdetermined, and
      that control cannot fire as written. `close` is therefore sized by the rank shortfall:
      n = 5 needs one condition, n = 11 needs four, and a closure sized by the count would
      have added none to either.'
    - >-
      'The rank verdict rests on a gap wide enough not to be a judgement call: at n = 5 the
      smallest counted singular value is `0.511` against a largest discarded one of
      `7.3e-42`. The gap is asserted in the test, not just the rank.'
    - >-
      'An angle class does not license an angle identity, and n = 29 is what showed it.
      Classes are decided modulo ninety degrees by an exact cross-or-dot-product test, so
      `t_i = t_j` is false for any member a quarter or half turn from another. Emitting
      those identities left n = 11 at the noise floor -- its classes happen to have equal
      angles -- and drove the n = 29 residual to `3.142`, one whole pi. They are no longer
      emitted, and the rank reaches its reported values without them.'
    - >-
      'A limit of the pose model, found the same way. Seven of the twenty-nine n = 29
      squares are built inside `scale(-1 1)` mirror groups and have clockwise corner
      winding, which a centre-plus-rotation pose cannot produce; read as rotations they
      left the residual at `2.0`. `pose_values` now refuses them by name. Fixing it properly
      means either re-indexing the contact features to match a re-wound square or giving
      the pose a chirality of its own, and both change what a feature name means, so
      neither was done in passing.'
    stop_reason: criterion
    next_action: >-
      Register controls, regenerate the frozen structure with its new fields, run the gate,
      and close the block.
  - workflow: process-review
    recording: contemporaneous
    clock_role: finalization
    focus: process
    commitment: BC-054
    bead: think-zm3f
    objective: >-
      Extend the contact-structure schema for the feature fields, regenerate the frozen
      artifact, register the block's controls, and correct a defect entry that a later
      measurement falsified.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: Both scientific phases reached their criteria.
    budget_minutes: 45
    started_at: '2026-08-29T04:50:00-07:00'
    deadline_at: '2026-08-29T05:35:00-07:00'
    expected_output: >-
      A regenerated structure that validates, four controls that fire, and a defect record
      that says only what is established.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: >-
      Stop if a control is registered without having been watched to fire; stop if a defect
      entry is left asserting something a later run contradicted.
    fallback: >-
      Push with the failing step named rather than leaving the block's result in a working
      tree on an ephemeral container.
    outcome: >-
      Closed. Controls rise from 93 to 97 and all 97 fire, including the one the previous
      session recorded as a standing failure. That reversal forced a correction rather than
      an addition.
    evidence:
    - >-
      'Four controls registered and each watched to fire: per-axis supports taken instead
      of their intersection, a corner-corner contact contributing one equation instead of
      two, reflected squares posed as rotations instead of refused, and an angle identity
      emitted for a modulo-ninety class. Each reproduces one of the block''s findings.'
    - >-
      'A correction, not an addition. Session-037 recorded D-356 as a standing control
      failure -- the cold-start synopsis control reporting a dead link instead of the drift
      it introduces -- reproduced four times including against a stashed clean tree. In this
      session the same control fired correctly and the suite passed 97 of 97, with no change
      to the checker, the synopsis or the prune list. D-356 is rewritten to cover only what
      is established, that the archive prune puts the n = 29 chain outside what this harness
      can control; the intermittency becomes D-357, which says plainly that the trigger is
      not identified rather than inventing one.'
    - >-
      The contact-structure schema gains three nullable fields and the frozen artifact is
      regenerated to carry them. Nullable rather than required so a structure extracted
      before they existed still loads, and assembly refuses on a null rather than reading
      it as "no features involved".
    stop_reason: criterion
    next_action: >-
      Open the endpoint check as BC-056 under `think-lo3p`.
  primary_bead: think-zm3f
  status: completed
  budget:
    wall_minutes: 180
    orientation_minutes: 10
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 45
  stop_conditions:
  - The block deadline at 2026-08-29T05:35:00-07:00
  - A closure added to make counts meet rather than to take up a measured shortfall
  - Equations presented as the packing's when they do not vanish at it
  - A defect entry left asserting what a later run contradicted
  progress:
    metric: Phases of the exact promotion route that are built, of the five the spec names
    before: >-
      3 of 5 -- extraction, refinement and the exact-LP stub existed; assembly and closure
      did not, so the pipeline ran from a structure to a hand-transcribed system
    after: >-
      4 of 5. Assembly is built and measured. Closure is *sized* rather than derived: the
      shortfall is known at both sizes and the determinant conditions themselves are the
      next step. Phase 4's exact solve was not reached in this block.
  delegations: []
  outputs:
  - src/sqpack/promote/system.py
  - src/sqpack/promote/contacts.py
  - tests/test_promote_system.py
  - atlas/known-best/contact-structure.schema.yaml
  - atlas/known-best/contact-structures.json
  - devtools/controls.yaml
  - defects.yaml
  checks:
  - 'uv run --frozen --group dev python -m devtools.run_negative_controls: 97 of 97 fire'
  - 'uv run --frozen --group dev python -m pytest tests/test_promote_system.py -q: passed'
  - 'uv run --frozen --all-extras --group dev packing-validate --fast: see the block commit'
  stop_reason: >-
    Assembly reached its criterion and the closure question was answered by measurement.
    Phase 4's exact solve was not started: the block clock went to the three findings above,
    each of which changed what assembly had to do.
  next_action: >-
    Open the endpoint check as BC-056 under `think-lo3p`: full strict gate, generated views
    regenerated, a logbook entry for the run, and a green PR. The efficiency and rigidity
    lanes were not run and are recorded as stopped rather than deferred silently; the exact
    solve of the closed system, and the two questions this block left open -- deriving the
    determinant conditions, and giving the pose model a chirality so reflected layouts can
    be assembled -- are the next slices after it.
---
# session-038 — block 3, contact features and system assembly

Block 3 of [agenda-006](../agendas/agenda-006-overnight-research-blocks.md), advancing
`BC-043` under
[plan-2026-08-28-promotion-pipeline-implementation](../../../docs/project/specs/active/plan-2026-08-28-promotion-pipeline-implementation.md).

## What was missing

The exact route ran from a frozen contact structure straight to a refinement of a system
somebody had transcribed by hand.
Nothing turned the first into the second, and the frozen structure could not have fed
one anyway: it recorded *which squares* touch and not *which features* meet, and the
equation depends on the features.

## Three findings, each against what the spec expected

**Per-axis supports are not the contact.** Squares 4 and 5 of Trump’s packing touch at a
single point, and on each axis separately they support a full edge.
Read per-axis that is two different edge-edge contacts and the packing has neither;
intersecting the supports across every realising axis gives the corner-corner contact
they actually have.

**Counting rows cannot answer whether the system determines the pose.** At `n = 11`
there are 35 equations against 34 unknowns — overdetermined — and the Jacobian has rank
30\. The system is redundant *and* four conditions short at once.
So `close` is sized by the rank shortfall: one condition at `n = 5`, four at `n = 11`.
The spec’s phase-2 control, which asks for the unclosed system to be reported
underdetermined, cannot fire as written.

**An angle class does not license an angle identity.** Classes hold modulo ninety
degrees, so `t_i = t_j` is false for a member a quarter or half turn from another.
Emitting them left `n = 11` at the noise floor — its classes happen to have equal angles
— and drove `n = 29` to a residual of exactly `pi`.

## What the equations are worth

They vanish at the packings they came from: `4.44e-16` at `n = 11`, the same order at
`n = 5`. Retyping one contact drives the residual above `1e-6`, so the check
discriminates rather than merely passing.

At `n = 29` they do not, and the reason is worth keeping: seven of the twenty-nine
squares are built inside `scale(-1 1)` mirror groups and have clockwise corner winding,
which a centre-plus-rotation pose cannot produce.
Assembly refuses them by name rather than describing their mirror images.

## What this block did not reach

Phase 4’s exact solve.
The closure is sized and not derived — the determinant conditions themselves are the
next step — and the reflected-square limit is a second open question.
The block clock went to the three findings above, each of which changed what assembly
had to do, and none of them was visible before the code existed to be wrong.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
