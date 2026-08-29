---
title: session-044 — agenda-006 continuation, the exact route at n = 29 and the middle layers behind it
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-044
  title: Eliminate the n = 29 system, close the exact route at n = 11, and finish the middle layers
  date: '2026-08-29'
  started_at: '2026-08-29T08:41:23Z'
  deadline_at: '2026-08-29T16:41:23Z'
  goal: >-
    Carry agenda-006's continuation blocks to terminal states, leading with the one that
    can still change what is known about n = 29: whether the five-unknown system left by
    BC-065 eliminates to an eliminant in `s`, or whether the exact-algebraic route is out
    of reach there at any practical cost. A measured refusal is the result that justifies
    the interval route carrying that bound, and is recorded as such rather than retried
    at a wider cap.
  workflow_phases:
  - workflow: process-review
    recording: contemporaneous
    clock_role: work
    focus: process
    objective: >-
      Repair four record defects found while picking the run up cold, before any of them
      can be inherited by a block that trusts them.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-08-29T08:41:23Z'
    deadline_at: '2026-08-29T09:11:23Z'
    expected_output: >-
      agenda-006 no longer points at a nonexistent agenda-007; the four continuation beads
      name the commitments the agenda actually gives them; think-ojlr's close reason no
      longer restates the claim D-358 retracted; and the session bootstrap guide's commands
      run against the layout the repository has.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: >-
      Stop if any repair needs a judgement about what a past run meant rather than what it
      recorded. A record whose intent is unclear is a defect to file, not to rewrite.
    fallback: >-
      File the unclear item as a defect and carry the rest.
    outcome: >-
      All four repaired inside the block. The bootstrap guide's four commands run here
      now; the two it opens with were executed to prove it rather than inspected.
    evidence:
    - >-
      'The session bootstrap guide pointed at `--directory explorations/packing` in seven
      places, a path retired when the packing tier was hoisted to the root. A cold-start
      agent following the guide failed on its first four commands. Repointed, and
      `packing-ledger check` and `packing-campaign status` were run from the repository
      root to confirm it.'
    - >-
      'agenda-006 sent BC-051 and BC-049 to an `agenda-007` that was never written. They
      were folded into agenda-006 itself as BC-062 and BC-063; the note now says so and
      says the earlier pointer was wrong.'
    - >-
      'Four continuation beads carried pre-renumbering commitment ids -- think-twa7 said
      BC-064, think-d0q7 BC-058, think-298s BC-062, think-c7oo BC-063 -- each pointing at
      a commitment that now belongs to different work.'
    - >-
      'think-ojlr was closed with the claim D-358 retracts, that blocks 2 and 3 overran
      into its slack. The close reason now carries the measured timestamps instead.'
    stop_reason: >-
      Bounded output complete at 08:43:59Z, 2.6 minutes into a 30-minute budget.
    next_action: >-
      Open the BC-066 phase against the six-equation system.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-066
    bead: think-obgk
    objective: >-
      Attempt the elimination BC-065 set up, and measure which of the two predicted
      failure modes it meets rather than running until something dies.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The record repairs are terminal; this opens the block the continuation exists for.
    budget_minutes: 90
    started_at: '2026-08-29T08:44:00Z'
    deadline_at: '2026-08-29T10:14:00Z'
    expected_output: >-
      An eliminant in `s` whose degree is measured rather than bounded, or a typed
      statement of where the chain stopped and what it cost.
    validation_command: >-
      uv run --frozen --all-extras --group dev python -m pytest
      tests/test_promote_elimination.py -q -p no:randomly
    kill_condition: >-
      Stop at the declared cap rather than widening it to reach a positive answer. A
      computation killed on memory is a measurement and is recorded as one.
    fallback: >-
      Report the sizes reached at each step, which is the answer that says the interval
      route carries n = 29.
    outcome: >-
      A measured wall rather than an eliminant, and the wall is not where the block
      expected it. Three runs, no basis, no bound moved.
    evidence:
    - >-
      'Over `Q` in an elimination order, F4 was OOM-killed at degree 32 after 25m09s with
      13.8 GB anon-RSS, having completed degree 31 on a `656126 x 1670545` matrix in
      382.84s. Exit 137, confirmed against the cgroup OOM record rather than inferred from
      the exit code.'
    - >-
      'Mod `1073741827` in the same order, the matrix dimensions are identical degree for
      degree -- `322322 x 912889` at 29, `484907 x 1300382` at 30 -- at about 70 per cent
      of the memory. Coefficients cannot swell over `F_p`, so those dimensions belong to
      the system rather than to its arithmetic.'
    - >-
      'Mod the same prime in plain grevlex, matrices are an order of magnitude smaller
      (largest `20611 x 49890`, 2.7 GB peak) and the pair list still grew monotonically to
      21,661 with no basis inside a declared 25-minute cap.'
    - >-
      'The export is guarded because an unguarded one already lied. Writing negative
      coefficients as `(-2)*x` -- a form msolve accepts and reads differently -- returned a
      reduced Groebner basis of `{1}`, no solutions in the algebraic closure, for a system
      whose solution this repository has refined to a thousand digits. The guard now
      re-parses the emitted text and requires it to vanish at the pose and to equal the
      cleared original.'
    stop_reason: >-
      The declared cap was reached and not widened. A typed statement of where the chain
      stopped and what it cost is the exit BC-066 names, so the block is complete rather
      than stopped.
    next_action: >-
      Open BC-067 on `think-er2h`: the n = 11 round trip, where the answer is published
      and the contact system has had full rank since BC-059.
  - workflow: general-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-068
    bead: think-mt4h
    objective: >-
      Make the generated atlas SVG a function of its inputs alone, so the composite
      receipt passes for the reason it states rather than on test ordering.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      Ran as a delegated lane against an isolated worktree while BC-066's elimination held
      the clock; integrated here once that block was terminal.
    budget_minutes: 60
    started_at: '2026-08-29T09:00:00Z'
    deadline_at: '2026-08-29T10:00:00Z'
    expected_output: >-
      A pinned emission precision, every stored artifact regenerated against it, and the
      composite-PNG check order-independent.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest tests/test_promote_system.py
      tests/test_known_best_atlas.py -q -p no:randomly
    kill_condition: >-
      Stop if a stored artifact cannot be regenerated from its inputs; name it rather than
      hand-editing it.
    fallback: >-
      Record which artifact resists regeneration, which is a typed outcome and not a
      failure to hide.
    outcome: >-
      Fixed, and no stored artifact moved. The defect had two halves and the entry had
      only found one of them.
    evidence:
    - >-
      'The ambient state came from `NumberField.decimal` setting the *thread-global*
      decimal precision and never restoring it. That is now a `localcontext`; a grep over
      `src`, `devtools` and `tests` found it to be the only global mutation, every other
      site already scoped its own.'
    - >-
      'The emission is pinned separately by `SVG_EMISSION_PRECISION`, applied as a
      decorator to the two document-level entry points so it covers arithmetic added
      inside them later rather than only the expressions someone remembered to wrap.'
    - >-
      'Pinned at 28 after measuring the alternatives rather than arguing them: at 32 the
      exact n = 5 face fails `validate_translation_only_trajectory` by `8e-32` and 66
      stored known-best outputs change; at 17 the coarsening reaches the subtractions that
      decide angle class and therefore hue.'
    - >-
      'No artifact changed a byte. All four generators -- known-best atlas, SVG rendering,
      contact overlays, prospective atlas -- rebuild identical output under the pin, which
      is the evidence that 28 is where they were already drawn.'
    - >-
      'The reproducer this repository recorded for D-359, `pytest tests/test_promote_system.py
      tests/test_known_best_atlas.py -p no:randomly`, went from 1 failed and 16 passed to
      17 passed. Both new controls fire.'
    stop_reason: >-
      Exit met inside the budget, and the regeneration the commitment was sized for turned
      out not to be needed.
    next_action: >-
      Open BC-067 on `think-er2h`.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-067
    bead: think-er2h
    objective: >-
      Discharge a recovered minimal polynomial all the way back to a verified packing at
      n = 11, rather than only to an isolated root.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      BC-066 and BC-068 are terminal; this is the next block in the continuation order.
    budget_minutes: 60
    started_at: '2026-08-29T10:17:00Z'
    deadline_at: '2026-08-29T11:17:00Z'
    expected_output: >-
      A `NumberField` built from the candidate, the pose unknowns solved exactly, the
      packing rebuilt and passed to `verify_packing` under `exact_sign`, and the
      reconstructed side compared against the input; or a typed statement of which step
      the field cannot support.
    validation_command: >-
      uv run --frozen --all-extras --group dev python -m pytest tests/test_promote_roundtrip.py
      -q -p no:randomly
    kill_condition: >-
      Stop if closing the loop needs the pose unknowns re-parameterised. The angles are
      transcendental and have no representation in `Q(s)`; saying so is the result, and
      re-parameterising the whole system is not this block's budget.
    fallback: >-
      A typed statement naming the step the field cannot support.
    outcome: >-
      The loop closes. Eleven squares, fourteen touching pairs, valid under `exact_sign`,
      and the reconstructed side equal to the field generator exactly.
    evidence:
    - >-
      'The obstacle is real: a pose unknown `t_i` is an angle and has no representation in
      `Q(s)`, so the exit''s literal reading is unsatisfiable while a pose is parameterised
      by angles. `n = 11` is reachable because its retained construction is already over
      `Q(u)` with `u = tan(a/2)`, built from `+ - * /` alone.'
    - >-
      '`u` is recovered by an exact rational linear solve rather than by integer relation:
      `Q(s) = Q(u)`, both degree eight, so writing each `s^i` in the power basis of `Q(u)`
      gives a square system with one solution. A singular system is refused as
      `subfield-too-small`. The coefficients agree with what a PSLQ search returns, and
      did not have to be believed to be used.'
    - >-
      'Rebuilding inside `Q(s)` makes the side comparison exact rather than approximate:
      reconstructed side and field generator live in one field, so the check is
      `(side - alpha).is_zero()`.'
    - >-
      'The spec''s trap is demonstrated, not asserted. A control rebuilds the real packing
      in a container one unit larger; `verify_packing` correctly reports it valid, and only
      the side comparison rejects it. Both negative controls fire.'
    - >-
      'The closed forms have one copy. `cases.trump11.packing.build_in` was split out so
      the round trip rebuilds *this* packing rather than one that resembles it, and the
      three existing consumers of that module are unmoved.'
    stop_reason: >-
      Exit met inside the budget.
    next_action: >-
      Integrate the delegated BC-069 and BC-061 lanes, then BC-062 and the reserved
      BC-064 endpoint check.
  - workflow: efficiency-loop
    recording: contemporaneous
    clock_role: work
    focus: efficiency
    commitment: BC-062
    bead: think-d0q7
    objective: >-
      Run only the verification steps a change can reach, with a control proving the
      selector cannot under-run, measured against a baseline taken on this container.
    status: stopped
    entered_by: planned_checkpoint
    switch_reason: >-
      The exact-route blocks are terminal and the two remaining middle-layer lanes are
      delegated; this is the next block the coordinator owns.
    budget_minutes: 45
    started_at: '2026-08-29T10:25:00Z'
    deadline_at: '2026-08-29T11:10:00Z'
    expected_output: >-
      A reachability-scoped selector with a control proving it cannot under-run, measured
      against the baseline; or a measured rejection.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: >-
      Stop if the selector can be shown to skip a step a change can reach. Under-running
      the gate is a soundness defect; a selector that is merely slow is a disappointment.
    fallback: >-
      A measured rejection, recorded with the baseline it was measured against.
    outcome: >-
      Stopped after design reading, without a measurement. Two reasons, and the second is
      the real one.
    evidence:
    - >-
      'It is a measurement block and the machine was not measurable. Two delegated lanes
      were running on four cores; a gate timing taken against them would not have been
      comparable to the 8m04s baseline, and a selector justified by a contended
      measurement is worse than no selector.'
    - >-
      '`Step` declares `name`, `action`, `fast` and `needs_engine` and no input paths at
      all, so a reachability selector needs a per-step read declaration first. The only
      safe shape is fail-open -- a step runs unless it can prove it is unreachable -- with
      the declaration verified against observed reads rather than trusted, since an
      incomplete declaration is exactly the under-run this block calls a soundness defect.
      That design is recorded here rather than half-built.'
    - >-
      'BC-066 redirected the clock. Its measured finding names homotopy continuation as
      the next thing to try at n = 29, and that is worth more of this session than a
      tool for the loop. BC-062 is the block this continuation twice judged cuttable, and
      cutting it here is that judgement rather than an overrun.'
    stop_reason: >-
      Deliberately cut in favour of BC-070, and left `ready` in the agenda rather than
      part-done.
    next_action: >-
      Open BC-070 on `think-xy0e`.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-070
    bead: think-xy0e
    objective: >-
      Bound and, if the tracking reaches it, count the isolated solutions of the n = 29
      system without computing a Groebner basis, and say what that makes the degree of
      `s(29)`.
    status: in_progress
    entered_by: evidence_checkpoint
    switch_reason: >-
      BC-066's measurement says the obstruction is the size of the ideal rather than the
      arithmetic, which makes a route that needs no basis the one worth the remaining
      clock.
    budget_minutes: 90
    started_at: '2026-08-29T10:31:00Z'
    deadline_at: '2026-08-29T12:01:00Z'
    expected_output: >-
      A bound tighter than Bezout's `1,039,500`, and where reachable the number of
      distinct `s` values among the isolated solutions.
    validation_command: >-
      uv run --frozen --all-extras --group dev python -m pytest tests/test_promote_elimination.py
      -q -p no:randomly
    kill_condition: >-
      Stop if the path tracking cannot account for its own paths. A count that loses or
      duplicates paths is not evidence about a degree, and must not be recorded as one.
    fallback: >-
      Record the mixed volume alone, which is a bound and does not depend on any path
      being tracked successfully.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: >-
      Report the bound and the count, then integrate the delegated lanes.
  primary_bead: think-obgk
  status: in_progress
  budget:
    wall_minutes: 480
    max_cycles: 16
    orientation_minutes: 30
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 40
  stop_conditions:
  - >-
    A typed refusal is a valid ending. An elimination that stops on size is a measurement,
    not a failure, and its reached sizes are the result.
  - >-
    No block may borrow from the 40-minute finalization reserve beginning at 16:01Z.
  - >-
    An unattended runner may not move `verified_upper_bound`. Any n = 29 result is recorded
    `unresolved` with `needs_review: true`.
  - >-
    Two consecutive blocks closing zero commitments stops the continuation for replanning.
  progress:
    metric: >-
      Agenda-006 continuation commitments in a terminal state, and whether the exact route
      has a measured verdict at n = 29
    before: >-
      Eight ready commitments (BC-061 through BC-064, BC-066 through BC-069); the exact
      route at n = 29 has a degree bound but no elimination attempt
    after: null
  delegations:
  - task: >-
      BC-068 -- pin the atlas SVG emission precision and stop the field refiner leaking
      into the global decimal context.
    operator: subagent
    recording: contemporaneous
    status: completed
    phase: 3
    budget_minutes: 60
    started_at: '2026-08-29T09:00:00Z'
    deadline_at: '2026-08-29T10:00:00Z'
    expected_output: >-
      A pinned emission precision with every stored artifact regenerated against it.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest tests/test_promote_system.py
      tests/test_known_best_atlas.py -q -p no:randomly
    kill_condition: >-
      Name any stored artifact that cannot be regenerated rather than hand-editing it.
    fallback: A typed statement of which artifact resists regeneration.
    write_scope:
    - packing/src/sqpack/field.py
    - packing/src/sqpack/render/numbers.py
    - packing/src/sqpack/render/packing.py
    - packing/devtools/build_known_best_atlas.py
    - packing/devtools/controls.yaml
    - packing/tests/test_emission_precision.py
    excluded_commands:
    - git push
    outcome: >-
      Fixed with no stored artifact changing a byte. Pinned at 28 after measuring that 32
      moves 66 outputs and breaks the translation-only trajectory check by `8e-32`.
    evidence:
    - >-
      'The recorded D-359 reproducer went from 1 failed and 16 passed to 17 passed.'
    - >-
      'Both new negative controls fire; the harness reports them under
      `run_negative_controls -k "emission precision"`.'
    files:
    - packing/src/sqpack/field.py
    - packing/src/sqpack/render/numbers.py
    - packing/tests/test_emission_precision.py
    checks:
    - uv run --frozen --all-extras --group dev packing-validate --fast
    uncertainty: >-
      Its worktree was branched from `main` rather than from this branch, so it could not
      see the promote work and reproduced the defect through `tests/test_motion_lab.py`
      instead. The fix is independent of that difference and was re-verified here against
      the reproducer the defect log actually records.
    elapsed_seconds: 4245
    elapsed_quality: platform_measured
    next_action: >-
      Landed by cherry-pick; D-359 closed and D-362 opened for the adjacent defect it
      surfaced.
  - task: >-
      BC-069 -- derive the one stationarity condition n = 5 still needs, in a form a
      solver accepts.
    operator: subagent
    recording: contemporaneous
    status: in_progress
    phase: 4
    budget_minutes: 59
    started_at: '2026-08-29T10:18:00Z'
    deadline_at: '2026-08-29T11:17:00Z'
    expected_output: >-
      A condition taking the n = 5 rank to 16 of 16 with the residual unmoved, or a typed
      statement of which formulation the contact graph resists.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: >-
      It may derive a condition; it may not size one to make the counts meet, which is
      D-361.
    fallback: A typed statement of what the contact graph resists.
    write_scope:
    - packing/src/sqpack/promote/system.py
    - packing/tests/test_promote_system.py
    - packing/devtools/controls.yaml
    excluded_commands:
    - git push
    outcome: null
    evidence: null
    files: null
    checks: null
    uncertainty: >-
      Running against a worktree branched from this branch's head, so unlike the BC-068
      lane it can see the promote work.
    elapsed_seconds: null
    elapsed_quality: null
    next_action: Integrate when it lands.
  - task: >-
      BC-061 -- an exact LP over certified rational or algebraic coefficients, replacing
      the float solver where a certified answer is required.
    operator: subagent
    recording: contemporaneous
    status: in_progress
    phase: 4
    budget_minutes: 59
    started_at: '2026-08-29T10:18:00Z'
    deadline_at: '2026-08-29T11:17:00Z'
    expected_output: >-
      An LP over exact coefficients agreeing with the float path where both are valid,
      and a report of which cells need algebraic rather than rational coefficients.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: >-
      If the exact LP needs a linear-algebra layer over `FieldElement` that does not
      exist, scope it and say so rather than building a half-finished matrix library.
    fallback: A typed statement of what blocks it.
    write_scope:
    - packing/src/sqpack/exact_lp.py
    - packing/tests
    - packing/devtools/controls.yaml
    excluded_commands:
    - git push
    outcome: null
    evidence: null
    files: null
    checks: null
    uncertainty: >-
      D-021's `1e-11` floor is the entry condition; whether the cells that matter need
      algebraic rather than rational coefficients is the open question the block reports.
    elapsed_seconds: null
    elapsed_quality: null
    next_action: Integrate when it lands.
  outputs: []
  checks: []
  stop_reason: null
  next_action: >-
    Carry BC-066 on `think-obgk` to a terminal state: record the measured wall the
    rational elimination hit, and take the eliminant's degree from the finite-field run.
---
# session-044 — the exact route at n = 29, and the middle layers behind it

## Why this session leads with `BC-066`

[`BC-065`](../agendas/agenda-006-overnight-research-blocks.md) left the `n = 29`
question in a specific state: the integer-relation route refused through degree twenty
below `10^22`, and the Bézout bound of `1,039,500` says that refusal surveyed a corner
rather than the space.
Elimination is the route that does not have to guess a degree.

It is worth being exact about what a success would and would not buy, because the
instinct that elimination is the “real” answer is right about rigour and easy to
over-read about consequence.
A complete elimination upgrades the `n = 29` upper bound from *certified at a relaxation
of `1e-20`* to *exactly this algebraic number*. It says nothing about optimality: the
`0.46` bound gap is untouched either way.

## The block plan

| Block | Commitment | Budget | Lane |
| --- | --- | ---: | --- |
| 1 | record repairs | 30 min | Process |
| 2 | `BC-066` — eliminate the five-unknown system | 90 min | Exact route, `n = 29` |
| 3 | `BC-067` — the `n = 11` round trip | 60 min | Exact route, known answer |
| 4 | `BC-069` — the one `n = 5` stationarity condition | 60 min | Exact route, last shortfall |
| 5 | `BC-061` — exact LP over certified coefficients | 60 min | Middle layer |
| 6 | `BC-068` — pin the atlas SVG emission precision | 60 min | D-359 |
| 7 | `BC-062` — reachability-scoped verification | 45 min | Efficiency, cuttable |
| 8 | `BC-063` — `n = 5` rigidity evidence | 45 min | Research, cuttable |
| 9 | `BC-064` — endpoint check | 40 min | Reserved |

Blocks 7 and 8 are the absorbers, and they are named as cuttable here rather than
discovered to be cuttable at 15:00Z. If `BC-066` is still producing measured progress at
its cap, the second slice comes from that slack and the replan is recorded at the
boundary.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
