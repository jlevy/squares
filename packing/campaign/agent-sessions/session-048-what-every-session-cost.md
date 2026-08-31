---
title: session-048 — the join between what a session did and what it cost
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-048
  primary_bead: think-atm1
  status: completed
  title: Report every session's cost, over distinct rollups rather than sessions
  date: '2026-08-30'
  started_at: '2026-08-30T21:05:00Z'
  deadline_at: '2026-08-30T23:35:00Z'
  goal: >-
    Session-047 wrote the rollups and `check_session_rollups` refuses a terminal session
    that declares none, so the link now exists. What did not exist was anything that reads
    it: a session record carries phases and outcomes, a rollup carries turns and wall-clock
    keyed by harness log id, and no artifact held both. "What did this session cost" was
    answered by hand and "what has the campaign cost" was not answered at all. Close that,
    and close this session with the tool it builds.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: process
    bead: think-atm1
    objective: >-
      Make the session-to-cost join a validated artifact rather than a question answered by
      hand, with a schema that refuses the ways of getting it wrong.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 60
    started_at: '2026-08-30T21:05:00Z'
    deadline_at: '2026-08-30T22:05:00Z'
    expected_output: >-
      `campaign/session-close-report.yaml` as a pure-yaml softschema dataset under
      `packing.squares:SessionCloseReport/v1`, registered in `validate_schemas` and written
      by `devtools.close_session --render`.
    validation_command: >-
      uv run --frozen --all-extras --group dev python -m devtools.validate_schemas
    kill_condition: >-
      A report that silently omits the sessions with no measurement. A total that reads as
      the campaign's cost while being a fraction of it is worse than no total.
    fallback: >-
      The dataset without the reader view; the dataset is the part that cannot be
      reconstructed by reading.
    outcome: >-
      47 entries, one per session, each joining the record's phases to its rollups. Sessions
      with no measurement carry `measured: false` and a reason, which the schema requires by
      an `allOf` clause rather than by convention. Two bugs of my own found on the way: the
      `--check` branch still referenced a `SUMMARY`/`render_summary` pair deleted in favour
      of the dataset and would have raised `NameError` the first time the gate called it,
      and `totals()` returning `dict[str, object]` produced ten type-floor errors the first
      time anything summed it.
    evidence:
    - packing/campaign/session-close-report.yaml
    - packing/campaign/schemas/session-close-report.schema.yaml
    - packing/devtools/close_session.py
    stop_reason: >-
      The dataset validates and the gate step that calls `--check` was already wired from
      session-047; it now has something to check.
    next_action: >-
      The reader view, and the arithmetic behind it read adversarially rather than trusted.
  - workflow: general-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    bead: think-atm1
    objective: >-
      Put the report in `SYNOPSIS.md` in a form a reader can use, and check the totals
      against the rollups on disk rather than against the sessions' own claims.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      The focus changes from process to correctness because the first numbers the reader
      view produced were wrong, and wrong in the flattering direction both times.
    budget_minutes: 45
    started_at: '2026-08-30T22:05:00Z'
    deadline_at: '2026-08-30T22:50:00Z'
    expected_output: >-
      A generated, drift-checked block under a new `## Sessions Conducted` in `SYNOPSIS.md`,
      and totals that account for every rollup on disk.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: >-
      Two owners for one region of text. If flowmark and the generator both rewrite the same
      bytes the drift check and the pre-commit hook undo each other on every commit.
    fallback: >-
      Tables in the generated block and every sentence outside it.
    outcome: >-
      Three findings, each from running the thing rather than reading it. Summing the
      per-session figures triple-counted the harness log that sessions 045, 046 and 047 each
      declare in full, reporting 117.9 hours for a campaign that had spent 43.7; totals are
      now taken over distinct rollups and the shared log occupies its own table row, so the
      column adds to the campaign figure instead of carrying a footnote. Ten rollups on disk
      are claimed by no session at all -- 1,460 turns and 6.87 hours -- so `totals` splits
      into `attributed`, `unattributed` and their union `measured`, and no owner is inferred
      for the unclaimed ten because the spans overlap enough that the guess would be
      unfalsifiable. And the first version put prose inside the generated block, which
      `make format-check` refused immediately: flowmark rewraps prose and the generator
      rewrites it. The block is tables only.
    evidence:
    - SYNOPSIS.md
    - packing/campaign/session-close-report.yaml
    - packing/src/sqpack/cli/validate.py
    stop_reason: >-
      `--fast` green on the tree that was pushed, `--records` green, ruff and basedpyright
      clean, `make format-check` clean, and drift detection confirmed to fail on a
      deliberately perturbed table before being trusted.
    next_action: >-
      Close this session with the tool it just built, and correct what PR #63 says about its
      own validation.
  - workflow: general-improvement
    recording: contemporaneous
    clock_role: finalization
    focus: process
    bead: think-atm1
    objective: >-
      Record this session, roll up what it cost with the tool this session built, and make
      the PR say what is true about it.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The clock role changes from work to finalization. The session that built the
      cost-reporting tool is the first one obliged to close with it.
    budget_minutes: 45
    started_at: '2026-08-30T22:50:00Z'
    deadline_at: '2026-08-30T23:35:00Z'
    expected_output: >-
      This record, the regenerated report and synopsis view carrying it, and a PR whose
      title and description match the branch.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      A session record dated into the future, which `D-358`'s guard refuses and which caught
      session-047 on its first attempt.
    fallback: >-
      The rollup alone; it is the part that cannot be reconstructed once the harness log is
      gone.
    outcome: >-
      This session appears in its own report. PR #63's description claimed `validate` is the
      full 54-step gate; it runs `packing-validate --fast`, 32 of 56 steps, which is what
      `D-403` on this branch records, and the claim is corrected rather than left standing.
    evidence:
    - packing/campaign/agent-sessions/session-048-what-every-session-cost.md
    - packing/campaign/resource-usage/3930e045-47fc-5947-8bf6-0c92155bcd88.yaml
    - packing/campaign/session-close-report.yaml
    stop_reason: >-
      The report includes this session, the gate is green on the tree that carries it, and
      the PR's own description no longer overstates what its CI ran.
    next_action: >-
      `agenda-009` is the queue. `BC-085`, `BC-086` and `BC-087` are ready and `BC-088` is
      blocked on the first two by design; none were started, because the owner asked for
      hygiene and planning rather than research this session.
  budget:
    wall_minutes: 150
    finalization_minutes: 45
  stop_conditions:
  - >-
    No research loop is started. The owner scoped this session to hygiene and planning so
    the PR can merge, and a research block begun here would be work nobody asked for.
  - >-
    A total is never taken over sessions. Sessions share harness logs, so adding their
    figures counts a shared log once per claimant; every total is over distinct rollups and
    the report says so where a reader will see it.
  - >-
    Nothing is pushed without the pull-request surface run directly on the exact tree.
    Three red cycles earlier on this branch were all pushes that skipped it.
  progress:
    metric: >-
      What can be answered about the campaign's cost from an artifact rather than by hand.
    before: >-
      Nothing. 47 session records and 41 rollups existed side by side with no join. This
      session is the 48th and the first to close with the tool. The
      campaign's total cost had never been computed, and the two obvious ways to compute it
      -- summing sessions, or summing only what sessions claim -- were both wrong.
    after: >-
      A validated 48-entry dataset and a drift-checked view in `SYNOPSIS.md`. 41 rollups,
      10,721 turns, 6,271 tool calls and 52.2 hours measured, of which 6.87 hours are
      claimed by no session; 44 of 48 sessions carry no measurement and say why.
  delegations: []
  outputs:
  - packing/campaign/session-close-report.yaml
  - packing/campaign/schemas/session-close-report.schema.yaml
  - packing/devtools/close_session.py
  - SYNOPSIS.md
  - packing/campaign/agent-sessions/session-048-what-every-session-cost.md
  checks:
  - uv run --frozen --all-extras --group dev packing-validate --fast
  - uv run --frozen --all-extras --group dev packing-validate --records
  - uv run --frozen --all-extras --group dev python -m devtools.close_session --check
  - make format-check
  resource_rollups:
  - packing/campaign/resource-usage/3930e045-47fc-5947-8bf6-0c92155bcd88.yaml
  stop_reason: >-
    The join exists, validates, and is checked; this session is in its own report; and the
    PR is green, mergeable, and no longer overstates what its CI ran.
  next_action: >-
    `BC-085` on `think-9k5k`, the first ready cell of `agenda-009` and the one the
    reassessment behind it is blocked on. The ten unclaimed rollups stay unclaimed: they
    predate the field, and inventing owners for them would be worse than counting them
    separately, which the report now does.
---
# Session-048 — What Every Session Cost

The repository could say what every session *did* and could not say what any of them
cost.

Both halves were on disk.
`campaign/agent-sessions/` holds phases and outcomes; `campaign/resource-usage/` holds
turns, tool calls and wall-clock, one rollup per harness log.
They are keyed differently — a session by its sequence number, a rollup by a UUID — so
going from one to the other meant knowing the mapping by heart, and nothing computed it.

The interesting part was not building the join.
It was that the first two ways of adding the numbers up were both wrong, and both wrong
in the same direction.

**Sessions share harness logs.** Sessions 045, 046 and 047 each declare the same log in
full, which is correct of each of them and cannot be charged to any one.
Adding the per-session rows reported 117.9 hours for a campaign that had spent 43.7.
Totals are now taken over distinct rollups, and the shared log gets a table row of its
own so the column adds up rather than needing a footnote saying why it does not.

**And a rollup exists whether or not a session claims it.** Ten do — 1,460 turns and
6.87 hours belonging to sessions that closed before the field existed.
Reporting only what sessions claim would have dropped them.
They are counted separately instead, with no owner inferred: the spans overlap enough
that assigning one to the session whose window contains it would look right and be
unfalsifiable.

A third finding was about ownership of a different kind.
The first version of the reader view put its explanatory prose inside the generated
block, and `make format-check` refused it on the spot — flowmark rewraps prose and the
generator rewrites it, so the hook and the drift check would have undone each other on
every commit. The block is tables only, and every sentence lives outside it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
