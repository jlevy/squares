---
title: session-034 — agenda-004 block 3, guard and join consolidation
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-034
  title: Consolidate the pipeline guards and make the record-model joins checkable
  date: '2026-08-27'
  started_at: '2026-08-27T17:33:50-07:00'
  deadline_at: '2026-08-27T22:33:50-07:00'
  goal: >-
    Close BC-035 and BC-041 by repairing the guards that stopped guarding and by making
    the record model's unchecked joins machine-checkable, so the drift class that produced
    five separate incidents becomes a gate failure rather than an invisible one.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: process
    commitment: BC-035
    bead: think-cja6
    objective: >-
      Add an invariant that at most one commitment per bead may be `ready`, resolving the
      one live violation it exposes, and pin lefthook the way flowmark is pinned.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 45
    started_at: '2026-08-27T17:33:50-07:00'
    deadline_at: '2026-08-27T18:18:50-07:00'
    expected_output: >-
      A checked invariant that rejects two simultaneously-ready commitments on one bead, a
      resolved `think-kdil` duplication, and a pinned lefthook install.
    validation_command: >-
      uv run --directory explorations/packing --frozen packing-ledger check
    kill_condition: >-
      Stop on an invariant that flags legitimate dependency chains, on resolving a
      duplication by deleting a commitment rather than dispositioning it, on pinning
      lefthook to a version not verified working here, or on editing a terminal record.
    fallback: >-
      Retain the measured violations and the proposed invariant shape without enforcing
      it, rather than enforcing a rule that produces false positives.
    outcome: >-
      Four of BC-035's and BC-041's six items are closed with four new guards, each
      verified to fire and each pinned by its own negative control. Negative controls rise
      from 76 to 80. One item is decided without a code change and one is deferred with a
      stated reason.
    evidence:
    - 'Ready-uniqueness invariant added and verified: injecting the violation names both commitments and their agendas. The rule was refined from at-most-one-live before any code was written, because at-most-one-live would flag think-sfzh''s legitimate blocked dependency chain.'
    - 'The one violation it exposed is resolved: `think-kdil` backed BC-028 and BC-038, both ready, and BC-028 is stopped as superseded with nothing measured retracted.'
    - 'Declared-command guard added: it parses every declared packing-validate and packing-ledger invocation against those tools'' own parsers, importing them rather than reimplementing the flag set. 70 invocations parse today.'
    - >-
      That guard exposed a flaw in how it was first verified. `packing-validate`'s parser
      overrides `error()` to raise `UsageError` rather than exiting, so catching only
      `SystemExit` let exactly the tool that carried the original defect escape as a
      traceback. The first verification used a `packing-ledger` command, which is stock
      argparse, and so confirmed the guard fired on the path that was never broken. Both
      exception types are now caught and both CLIs are verified.
    - 'Commitment-to-phase join added as optional `commitment` and `bead` fields on a phase and an optional `workflows` list on a commitment, so no terminal record needs rewriting. Both are populated for real rather than only declared.'
    - >-
      The agenda schema duplicates the session schema's workflow enum because a cross-file
      `$ref` does not resolve for these loaders, which was measured rather than assumed
      after the reference failed. A checker now compares the two lists, so the duplication
      cannot drift silently, and that check is itself verified to fire.
    - 'lefthook pinned to 2.1.10, the version verified working here, closing an unpinned zero-install runner that the repository''s own policy warns against.'
    - >-
      The `controls.yaml` anchor question is decided without a change. Literal anchors that
      embed generated values do rot, but the harness already catches it loudly, reporting
      that an anchor appeared zero times where exactly one was expected. The
      round-aggregate control was not undetected; it was unrun, because `negative controls`
      is a full-tier step and the edit loop runs `--fast`. The fix is the cadence, which
      agenda-004 now encodes as a full gate at every block boundary, not a new anchor
      mechanism.
    stop_reason: >-
      Four items closed with verified guards, one decided, one deferred with a reason, so
      the block met its own split threshold of at least four of six.
    next_action: >-
      `think-306i` is deferred, not abandoned. exp-045 going terminal makes all 45 rounds
      terminal, so the false statement the contract forces is true today and there is no
      failing case to verify a fix against. Fix it when a round is next in-progress, or
      construct a deliberate fixture; do not patch a checker with no way to prove the
      change correct.
  primary_bead: think-cja6
  status: completed
  budget:
    wall_minutes: 300
    slice_minutes: 45
    orientation_minutes: 15
    finalization_minutes: 30
  stop_conditions:
  - No invariant is enforced that flags a legitimate dependency chain.
  - No terminal session record or archived artifact is rewritten.
  - The full gate runs in the background, never in a foreground command with a ten-minute limit.
  - A quota or API failure halts the run; it is not retried on a timer.
  progress:
    metric: guard and join defects closed or explicitly deferred with a reason
    before: >-
      Six items are open across BC-035 and BC-041. Three beads back more than one live
      commitment, one of them with two simultaneously ready. `npx lefthook install` is
      unpinned against a repository policy that pins flowmark for exactly that reason.
    after: >-
      Four guards exist that did not, each verified to fire rather than merely to pass,
      and each pinned by its own negative control so it cannot stop guarding unnoticed.
      Negative controls rise from 76 to 80. The one remaining defect is dormant and
      deferred with a stated reason rather than patched blind.
  delegations: []
  outputs:
  - Makefile
  - campaign/agendas/agenda-003-balanced-ten-hour-research-program.md
  - campaign/agendas/agenda-004-guard-repair-and-instrument-unblock.md
  - campaign/agent-sessions/session-034-block3-guards-and-joins.md
  - campaign/schemas/agenda.schema.yaml
  - campaign/schemas/agent-session.schema.yaml
  - devtools/check_declared_commands.py
  - devtools/controls.yaml
  - src/sqpack/campaign/ledger.py
  - src/sqpack/cli/validate.py
  checks:
  - Blocks one and two both closed with a green full gate; exp-045 is terminal at `unresolved` with `needs_review`.
  - >-
    Read-only scoping refined the invariant before any code was written. At-most-one-live
    would flag `think-sfzh`'s BC-018 and BC-021, which are both blocked and form a
    legitimate dependency chain rather than an ambiguity. At-most-one-ready captures the
    real question, which is which commitment a runner should pick up, and leaves chains
    alone.
  - 'Under the refined rule exactly one violation exists: `think-kdil` backs BC-028 and BC-038, both `ready`.'
  - '`think-306i` is currently dormant: exp-045 going terminal makes all 45 rounds terminal, so the synopsis assertion it forces is true today and there is no failing case to verify a fix against.'
  stop_reason: >-
    The block met its declared split threshold with four of six items closed, one decided
    and one deferred on a stated reason.
  next_action: >-
    Under BC-038 and think-kdil, run block four: wire `evaluate_stress` to the shared row
    inventory now that exp-045 is terminal and the path is no longer frozen.
---
# Session 034 — Agenda-004 Block 3

Blocks one and two produced results.
This block pays the debt that made both of them noisier than they needed to be: five
separate drift incidents in one day, each invisible until something forced a check.

The scoping pass changed the shape of the main invariant before any code was written,
which is the cheapest possible moment to find that out.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
