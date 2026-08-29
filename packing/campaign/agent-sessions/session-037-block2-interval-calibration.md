---
title: session-037 — agenda-006 block 2, calibration against known answers and an n = 29 certificate
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-037
  title: Calibrate the interval route where the answer is already known, then run it at n = 29
  date: '2026-08-29'
  started_at: '2026-08-28T22:40:00-07:00'
  deadline_at: '2026-08-29T01:40:00-07:00'
  goal: >-
    Close agenda-006 block 2 by running phases 3 and 4 of
    plan-2026-08-28-interval-certification. Phase 3 asks whether the checker agrees with
    the exact route where both can speak, and whether it can be caught refusing something
    a float check accepts. Phase 4 asks what the chain returns at n = 29, where nothing is
    a known answer and a refusal is as admissible an outcome as a bound.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-053
    bead: think-9ida
    objective: >-
      Resolve the question block 1 left standing -- an interval checker cannot certify a
      tight packing, because its contacts are exact zeros -- and then calibrate against
      n = 5, n = 10 and n = 11, which the exact route already verifies.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 75
    started_at: '2026-08-28T22:40:00-07:00'
    deadline_at: '2026-08-28T23:55:00-07:00'
    expected_output: >-
      A certified upper bound at a declared relaxation for each of the three exactly
      verified cases, each strictly above the exact side and approaching it as the
      relaxation falls; the Krawczyk operator certifying Trump's published degree-8 root;
      and a demonstration that the checker refuses a pose a float check accepts.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: >-
      Stop if any certified bound comes out at or below an exactly verified side, which
      would be a soundness failure and not a tighter result; stop if agreement is obtained
      by widening a tolerance anywhere.
    fallback: >-
      Report which cases the relaxation cannot certify and at what width the separating-axis
      tests go undecidable, rather than a bound whose relaxation is not stated.
    outcome: >-
      Calibrated on all three. The route agrees with the exact one where both can speak,
      and -- the check that agreement alone cannot make -- it proves an overlap of `1e-30`
      that a float check at `1e-9` accepts as a valid packing.
    evidence:
    - >-
      'The way past block 1''s refusal is to certify a slightly worse packing rather than
      to loosen anything: scaling centres apart by `1 + eps` leaves every square exactly
      unit and exactly oriented, moves nothing toward the origin, and strictly opens every
      contact, because two squares with disjoint interiors have their centres on opposite
      sides of a separating line. What comes out is `s(n) <= S` with `S` above the optimum
      and approaching it, which is a different and weaker claim than the exact route makes
      and is stated as one.'
    - >-
      'Agreement, four rungs each. n = 5 reaches `2.70710678118654973150762554866` against
      an exact `2 + sqrt(2)/2`; n = 10 reaches `3.70710678118655073150762554866` against
      `3 + 1/sqrt(2)`; n = 11 reaches `3.87708359002281755439148708292` against Trump''s
      degree-8 root. Every rung is strictly above its exact side, and every bound falls
      as `eps` falls.'
    - >-
      'The operator against algebra it cannot influence: Krawczyk certifies a unique root
      of Trump''s published degree-8 polynomial in a box of radius `8.46e-63`, and that box
      contains the algebraic root computed independently by `sqpack.field` over its
      certified number field.'
    - >-
      'Discrimination, which is the half that matters. Pushing one n = 5 square into its
      neighbour by `1e-12`, `1e-20` and `1e-30` is *proved* overlapping by this route at
      every scale, while `verify_packing` under `float_sign(1e-9)` reports the same three
      poses valid. Both halves are asserted, so the contrast cannot rot into a claim
      nobody rechecks.'
    - >-
      'Refusals. A zero or negative relaxation opens no contact and is refused by kind; a
      side below the packing is refused by name; and the exact-to-interval bridge rounds
      outward on both endpoints, since rounding a rational inward would narrow an
      enclosure that was rigorous when it left the number field.'
    stop_reason: criterion
    next_action: >-
      Enter phase 2 and drive the n = 29 chain, where the layout map has to become a
      function of the unknowns rather than of the printed digits.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-053
    bead: think-9ida
    objective: >-
      Run the chain at n = 29: refine, certify the root, push the certified box through the
      source's layout map, relax, and verify. Record whatever comes back, including a
      typed refusal.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      Phase 1's calibration passed, which is this phase's entry condition; the objective
      changes from agreeing with a known answer to producing one where none exists.
    budget_minutes: 75
    started_at: '2026-08-28T23:55:00-07:00'
    deadline_at: '2026-08-29T01:10:00-07:00'
    expected_output: >-
      Either an interval-certified upper bound on `s(29)` with its relaxation declared and
      `needs_review` set, or a typed statement of which stage refused and why.
    kill_condition: >-
      Stop if the bound is obtained by widening the container until verification passes
      rather than by reading the side off the relaxed corners; stop if anything in the run
      writes to `frontier/`.
    validation_command: >-
      uv run --frozen python -m cases.kingbird29.certify_interval
    fallback: >-
      Retain the certified root and a typed statement of what the layout map cannot supply,
      rather than a bound whose layout is not the source's.
    outcome: >-
      The chain completes. `s(29) <= 5.93383346267692918974379895098` at a declared
      relaxation of `1e-20`, with all 406 pairs strictly separated and none undecided.
      This is recorded `unresolved` with `needs_review: true` and promotes nothing.
    evidence:
    - >-
      'The root is well conditioned, which the spec listed as an open question. Krawczyk
      certifies a unique root of the six-equation contact system in a box of radius
      `3.19e-62` after two iterations, in about a tenth of a second.'
    - >-
      'The layout map is the source''s, not a second transcription of it. The XML parser
      substitutes each `&a;` with the decimal the source prints, so the existing walk can
      only build the published pose; keeping entity references as markers until evaluation
      makes the same transforms a function of the unknowns. All fifteen entities resolve
      from the six unknowns, the nine slide scalars through the source''s own closed forms.'
    - >-
      'A bug the equivalence check caught and inspection would not have. The token pattern
      matched a bare marker, so `rotate(-&a;)` lost its minus and rotated the other way --
      which mirrors a square about its own rotation centre and leaves a plausible-looking
      packing. `agrees_with_materialised` found it at square 15, x = 1.8300 against
      2.1700, symmetric about the rotation centre at x = 2. With the sign folded into the
      pattern, all 29 squares agree with the numeric walk to `1e-40`.'
    - >-
      'Unit-square and right-angle checks, run over the propagated enclosures rather than
      assumed from the construction: across 29 squares and 116 edges, every edge-length
      enclosure contains 1 to within `3.53e-43` and every corner dot product encloses zero
      to within `3.06e-43`.'
    - >-
      'The strongest independent check in this block, and it was not planned. Verified
      *unrelaxed*, the chain cannot decide exactly 52 pairs -- and those 52 are precisely
      the 52 pair contacts BC-042 extracted by a completely different route in session-035.
      The sets are identical. Two implementations sharing no code agree on which pairs of
      this packing touch.'
    - >-
      'Controls at n = 29. A side `1e-6` below the bound is refused by name; a zero
      relaxation is refused by kind; and the unrelaxed layout refuses rather than
      certifying, which is the behaviour a tight packing must produce.'
    - >-
      'What the bound would do, stated without acting on it. The standing verified ceiling
      is Schadt''s rational `5.93388579981302587863645209`; this certificate sits
      `5.23371e-5` below it, which is the gap
      plan-2026-08-28-interval-certification names as closable by no amount of better
      sourcing. Moving `verified_upper_bound` is a reviewed human decision through the
      evidence contract, and nothing in this run touched `frontier/`.'
    stop_reason: criterion
    next_action: >-
      Register controls, run the gate, and close the block at its checkpoint.
  - workflow: process-review
    recording: contemporaneous
    clock_role: finalization
    focus: process
    commitment: BC-053
    bead: think-9ida
    objective: >-
      Register the block's negative controls, run the gate, record what the control harness
      cannot cover, and leave the checkpoint committed, pushed and carried by the run's PR.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      Both scientific phases reached their criteria; what remains is reconciliation.
    budget_minutes: 30
    started_at: '2026-08-29T01:10:00-07:00'
    deadline_at: '2026-08-29T01:40:00-07:00'
    expected_output: >-
      Registered controls that fire in the shared harness, a green gate, and a pushed
      checkpoint.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: >-
      Stop if a control is registered without having been watched to fire.
    fallback: >-
      Push with the failing step named rather than leaving the block's result in a working
      tree on an ephemeral container.
    outcome: >-
      Closed, slightly past the nominal boundary, against block 4's slack as agenda-006
      allows. Controls rise from 90 to 93 and all three new ones fire. One standing control
      failure was investigated and found to pre-date this work.
    evidence:
    - >-
      'Three controls registered and each watched to fire: a relaxation that moves squares
      inward rather than apart, a zero relaxation accepted anyway, and an exact-to-interval
      bridge that rounds inward -- the last one caught by `mpmath` itself refusing an
      inverted enclosure.'
    - >-
      'A limitation of the harness, found by trying to use it. Three further controls over
      the n = 29 chain cannot run: `run_negative_controls` prunes `resources/` from its
      snapshot to stay under the portable size cap, and the n = 29 source is the provenance
      SVG in that archive, so those controls would fail on a missing file rather than on
      the mutation. The n = 29 guards are asserted directly in the test instead, and the
      controls file says why they are not here.'
    - >-
      'A standing control failure, run down rather than absorbed. `synopsis - README
      cold-start link drifts from current handoff` does not fire: the same prune list drops
      `atlas/known-best/rendering`, so `check_synopsis` reports a dead link and exits before
      reaching the drift the control introduces. Reproduced on a clean stashed tree at this
      commit, so it is not a consequence of this work. Recorded as D-356 rather than
      repaired, because both candidate fixes change a shared trust boundary and belong in
      their own slice.'
    stop_reason: criterion
    next_action: >-
      Open block 3 as session-038 under BC-054, merging origin/main first.
  primary_bead: think-9ida
  status: completed
  budget:
    wall_minutes: 180
    orientation_minutes: 10
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 30
  stop_conditions:
  - The block deadline at 2026-08-29T01:40:00-07:00
  - Any write to frontier/, which this run may not make
  - A bound obtained by widening a container rather than by reading it off the corners
  - A certified bound at or below an exactly verified side
  progress:
    metric: >-
      Stages of plan-2026-08-28-interval-certification built and calibrated, out of the
      four the spec names
    before: '2 of 4; the operator and the verifier existed and nothing had been calibrated'
    after: >-
      4 of 4. All four phases are built, calibrated against three exactly verified cases,
      and run at n = 29. The witness branch is still unwritten, so `exact_verify` continues
      to raise `checker-not-built` and no witness is emitted.
  delegations: []
  outputs:
  - src/sqpack/promote/relax.py
  - src/sqpack/promote/enclose.py
  - src/sqpack/promote/interval.py
  - src/sqpack/field.py
  - cases/kingbird29/layout.py
  - cases/kingbird29/certify_interval.py
  - cases/kingbird29/system.py
  - cases/kingbird29/verify_svg.py
  - tests/test_promote_relax.py
  - devtools/controls.yaml
  - defects.yaml
  - campaign/series/series-000-smoke-and-calibration/results/bc-053-n29-interval-certificate.json
  checks:
  - 'uv run --frozen python -m cases.kingbird29.certify_interval: certified, 406/406 separated'
  - 'uv run --frozen --group dev python -m devtools.run_negative_controls: 92 of 93 fire; the one failure is D-356 and pre-dates this work'
  - 'uv run --frozen --all-extras --group dev packing-validate --fast: see the block commit'
  stop_reason: >-
    Both scientific phases reached their criteria, and the finalization reserve closed the
    checkpoint slightly past the nominal boundary against block 4's slack.
  next_action: >-
    Open block 3 as session-038 under BC-054 and `think-zm3f`. Merge origin/main first,
    then assemble the contact equations from the frozen n = 29 structure, eliminate the
    centres where the graph permits, close by determinant conditions, and reproduce the
    known n = 11 system -- or state which reduction the graph does not admit. Separately,
    and for a human rather than a runner: the n = 29 interval certificate is retained and
    unpromoted, and whether it moves `verified_upper_bound` is a reviewed decision through
    the evidence contract.
---
# session-037 — block 2, calibration and an n = 29 certificate

Block 2 of [agenda-006](../agendas/agenda-006-overnight-research-blocks.md), advancing
`BC-045` through phases 3 and 4 of
[plan-2026-08-28-interval-certification](../../../docs/project/specs/active/plan-2026-08-28-interval-certification.md).

## What block 1 left standing, and how it is answered

An interval checker cannot certify a record packing.
Its contacts are exact zeros, no enclosure of positive width certifies an equality, and
loosening anything to make it pass would accept overlaps of the same size.

So the packing that gets certified is a slightly worse one.
Scale the centres apart by `1 + eps`: every square stays exactly unit and exactly
oriented, nothing moves toward the origin, and every contact strictly opens, because two
squares with disjoint interiors have their centres on opposite sides of a separating
line. What comes out is `s(n) <= S` with `S` above the optimum and falling toward it as
`eps` falls.

That is a weaker claim than the exact route makes, and the relaxation is reported with
every bound so the two cannot be confused.

## Calibration

| Case | Exact side | Certified at `eps = 1e-15` |
| --- | --- | --- |
| `n = 5` | `2 + √2/2` | `2.70710678118654973150762554866` |
| `n = 10` | `3 + 1/√2` | `3.70710678118655073150762554866` |
| `n = 11` | Trump’s degree-8 root | `3.87708359002281755439148708292` |

Each is strictly above its exact side and falls monotonically with `eps`. Separately,
the operator certifies a unique root of Trump’s published degree-8 polynomial in a box
of radius `8.46e-63`, and that box contains the algebraic root `sqpack.field` computes
independently.

**Agreement is the easy half.** A checker that said “valid” unconditionally would pass
every row above. So the same packings are pushed into infeasibility by amounts no float
check can see: an overlap of `1e-30` is *proved* by this route, and `verify_packing`
under `float_sign(1e-9)` reports the same pose valid.

## `n = 29`

The chain completes.

```
s(29) <= 5.93383346267692918974379895098      (eps = 1e-20, 406 pairs, none undecided)
```

The root is well conditioned — an open question in the spec, now measured: Krawczyk
contracts to a unique root in a box of radius `3.19e-62` in two iterations.

The layout map had to become a function of the unknowns rather than of the printed
digits, which is what [`cases/kingbird29/layout.py`](../../cases/kingbird29/layout.py)
does, using the source’s own transforms with entity references kept as markers until
evaluation.

Two checks make that trustworthy, and one of them found a real bug.
The equivalence check — evaluate the symbolic map at the published values and require it
to reproduce the numeric walk — caught a token pattern that dropped the minus in
`rotate(-&a;)`, mirroring a square about its own rotation centre while leaving a
perfectly plausible packing.
It surfaced at square 15, `x = 1.8300` against `2.1700`, symmetric about the rotation
centre at `x = 2`.

The second is the one worth keeping.
Verified **unrelaxed**, the chain cannot decide exactly 52 pairs — and those are
precisely the 52 pair contacts BC-042 extracted from the same packing by an entirely
different route in session-035. Two implementations sharing no code agree on which pairs
touch.

## Claim boundary

This certifies an upper bound at a declared relaxation.
It is not the optimum, not an optimality result — the `n = 29` bound gap of about `0.46`
is untouched — and not a promotion.

The certificate sits `5.23371e-5` below the standing verified ceiling, which is the gap
the spec names as closable by no amount of better sourcing.
Whether it closes it is a reviewed human decision through the evidence contract.
Nothing in this run wrote to `frontier/`, the result carries `needs_review: true`, and
`exact_verify` still raises `checker-not-built` because no witness branch was written.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
