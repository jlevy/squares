---
title: session-046 — the two sizes Göbel's family already answers and this repository had not built
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-046
  title: Build the exact constructions for n = 65 and n = 89
  date: '2026-08-30'
  started_at: '2026-08-30T15:03:00Z'
  deadline_at: '2026-08-30T15:48:00Z'
  goal: >-
    Session-045's handoff names this as the cheapest open work and it is: Goebel's family
    is exactly the best known at n = 5, 40, 65 and 89, the first two have case packages
    here and the last two do not. Both verify exactly in seconds and the general builder
    already exists, controlled against cases/gobel40. This is the whole session -- one
    slice, additive, and short.
  workflow_phases:
  - workflow: research-loop
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-049
    bead: think-xdly
    objective: >-
      Give n = 65 and n = 89 exact constructions in `cases/`, verified by the same exact
      separating-axis test the rest of the corpus uses, with the duplicated-square negative
      control and a witness-agreement bound that says what the residual is rather than
      tolerating it. One package for the family rather than two copies of gobel40.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 35
    started_at: '2026-08-30T15:03:00Z'
    deadline_at: '2026-08-30T15:38:00Z'
    expected_output: >-
      `cases/gobel_family` building any `(a, b)` in the family, verify_exact covering
      n = 65 and n = 89, both in the `exact verification` gate step, and tests that hold the
      counts and the negative control. Nothing promoted: the frontier witnesses stay
      `numerical-multiprecision` until someone checks the assurance contract.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --edit
    kill_condition: >-
      Feasible at the retained side is not optimal, and the witnesses may not be promoted
      here on the strength of a construction that matches a decimal. Also: the wall budget
      is short and the tests take twelve minutes, so nothing is pushed that has not run
      them -- D-393 is this run's own defect and repeating it at the end would be worse
      than not finishing.
    fallback: >-
      The builder and the verification without the gate wiring, if the clock runs out; the
      construction is the part that does not exist yet.
    outcome: >-
      Both built and verified. `cases/gobel_family` holds the general form of the rule and
      `verify_exact` covers n = 65 and n = 89: 2080 and 3916 pairs, every one decided by
      exact sign over Q(sqrt 2), 64 boundary coordinates each, and a duplicated square
      rejected at both sizes. One package rather than two copies of `gobel40`, and the
      control that makes the generalization trustworthy is that built at a = 3, b = 4 it
      reproduces `gobel40` corner for corner.

      **The witness comparison found more than it was set up to find.** The bound started at
      1e-11, on the reasoning that these are `numerical-multiprecision` records and might be
      independent optimisations that merely land on the same side. They agree to 4.81e-33
      and 3.28e-33. Nothing independently optimised lands within 1e-32 of a construction it
      was not built from, so these two decimals *are* materialisations of Goebel's family --
      exactly as n = 40's turned out to be. The bound was tightened to 1e-32 and now says
      so; the docstring that said the opposite is corrected.

      SYNOPSIS's Current Handoff was still describing the morning's state ("producing an
      exact construction is the real price") and now carries the day: n = 40 flexible and
      why that settles only the first-order question, the family exact at four sizes, and
      n = 28 as the near miss that stops the obvious guess.
    evidence:
    - packing/cases/gobel_family/packing.py
    - packing/cases/gobel_family/verify_exact.py
    - packing/tests/test_gobel_family_construction.py
    - packing/src/sqpack/cli/validate.py
    stop_reason: >-
      Exit reached inside the budget. The kill condition held: no witness moved to
      `exact-algebraic`, and nothing was pushed before the full suite ran -- 934 tests, all
      passing.
    next_action: >-
      Whether n = 65 and n = 89's witnesses can move to exact, which is an assurance
      contract question this session does not open.
  primary_bead: think-xdly
  status: completed
  budget:
    # Measured from session-045: twenty-three phases in 495 minutes, a mean of about 21.
    # This is one slice against a 45-minute remainder of the same mandate, so the wall
    # budget is what is actually left rather than a fresh allowance.
    wall_minutes: 45
    max_cycles: 2
    orientation_minutes: 5
    checkpoint_minutes: 10
    slice_minutes: 15
    finalization_minutes: 10
  stop_conditions:
  - >-
    A construction that matches a retained decimal is feasible at that side, not optimal.
    No witness moves to `exact-algebraic` in this session.
  - >-
    Nothing is pushed without the affected tests run directly. `--edit` does not run them
    (D-393), and that defect was recorded four hours ago by this same run.
  progress:
    metric: >-
      Sizes in Goebel's family that are exactly the best known and have an exact
      construction retained here
    before: >-
      Two of four: n = 5 and n = 40. n = 65 and n = 89 are exactly the best known and carry
      only numerical-multiprecision witnesses
    after: >-
      All four: n = 5, 40, 65 and 89. The two new ones also identify their retained
      witnesses, which agree with the construction to 5e-33
  delegations: []
  outputs: []
  checks: []
  # Same harness log as session-045 -- one continuous transcript spanning both. This
  # session spawned no sub-agents, so it names the log alone.
  resource_rollups:
  - packing/campaign/resource-usage/3930e045-47fc-5947-8bf6-0c92155bcd88.yaml
  stop_reason: >-
    The one slice this session declared is done and the mandate's wall budget is spent.
  next_action: >-
    `BC-049` on `think-xdly` stays open: n = 5 is done, n = 40 is decided at first order
    and open beyond it, n = 28 is untouched and its optimum is not in Goebel's family.
    Whether n = 65 and n = 89's witnesses can move from `numerical-multiprecision` to
    `exact-algebraic` is the question this session makes askable and does not open.
---
# Session-046 — The Two Sizes the Family Already Answers

Session-045 spent nine unplanned phases discovering that `n = 40`’s exact construction
had been published all along, and recorded that as [`D-389`](../../../defects.md).
Its last twenty minutes asked the general question that correction implies, and found
that the same family is exactly the best known at four sizes.

Two of them had no construction here.
This builds them.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
