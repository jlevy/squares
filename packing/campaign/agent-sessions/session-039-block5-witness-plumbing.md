---
title: session-039 — agenda-006 block 5, the interval certificate enters the record
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-039
  title: Widen the witness contract for enclosures, build the checker branch, and record the n = 29 certificate as evidence
  date: '2026-08-29'
  started_at: '2026-08-28T22:40:00-07:00'
  deadline_at: '2026-08-28T23:25:00-07:00'
  goal: >-
    Close agenda-006 block 5 by making the n = 29 interval certificate reviewable by
    someone else: a scalar kind that can express an enclosure, a checker branch that
    replays one, the witness itself, and an evidence entry stating its assurance. Also
    correct this run's own clock record, which a review of the commit timestamps showed to
    be wrong by about a factor of four.
  workflow_phases:
  - workflow: process-review
    recording: contemporaneous
    clock_role: work
    focus: process
    commitment: BC-057
    bead: think-pfwx
    objective: >-
      Establish what this run actually did, against the commit timestamps rather than
      against the coordinating agent's estimate, and correct every artifact the estimate
      reached.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 12
    started_at: '2026-08-28T22:40:00-07:00'
    deadline_at: '2026-08-28T22:52:00-07:00'
    expected_output: >-
      Measured clocks in the three session records and the run entry, a corrected stop
      reason for the block that did not run, and a defect saying plainly what went wrong.
    validation_command: uv run --frozen packing-ledger check
    kill_condition: >-
      Stop if a correction is made that cannot be checked against the commit timestamps;
      an estimate replacing an estimate is not a correction.
    fallback: >-
      Record the discrepancy as a defect without amending the artifacts, rather than
      substituting a second set of numbers nobody measured.
    outcome: >-
      Corrected. The run declared 150, 180, 180 and 40-minute blocks and took 31, 42, 29
      and 23; it declared a 690-minute target and had spent 143 minutes when it stopped.
      The bookkeeping was the smaller half of the problem.
    evidence:
    - >-
      'Measured from the commit timestamps: planning at 03:04:56Z, then the four block
      commits at 03:36:09Z, 04:18:15Z, 04:46:49Z and 05:09:32Z. The coordinating agent had
      been estimating elapsed time between tool calls, and the estimates ran about four
      times fast.'
    - >-
      'The worse half. The misreading supplied a reason for a scheduling decision: BC-055
      was recorded stopped because "blocks 2 and 3 overran into this cell''s slack", and
      nothing had overrun -- the run stopped with most of its budget unspent. That reads as
      a constraint the run met and was a mistake the run made, which is the flattering
      direction. Recorded as D-358 and the reason replaced with what happened.'
    - >-
      Clocks in session-036, session-037, session-038 and run-002 are now the measured
      windows, rounded to the minute; the per-phase boundaries inside them were never
      timestamped and are apportioned, which is why they are round. run-002 returns to
      `stopped` because the run is resuming rather than finished.
    - >-
      The practice change is mechanical rather than a resolution to be more careful: read
      `date -u` at each block boundary and record it. This session's own phases are
      clocked that way.
    stop_reason: criterion
    next_action: >-
      Enter phase 2 and widen the witness contract so the certificate can be written down.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-057
    bead: think-pfwx
    objective: >-
      Give the witness contract a scalar kind that can express an enclosure, build the
      `exact_verify` branch that replays one, emit the n = 29 witness, and record it as
      evidence with its assurance stated.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The record now says what the run did; the objective changes from correcting history
      to closing the socket the witness contract left open.
    budget_minutes: 27
    started_at: '2026-08-28T22:52:00-07:00'
    deadline_at: '2026-08-28T23:19:00-07:00'
    expected_output: >-
      `packing-witness verify` replaying the n = 29 certificate, an evidence entry, and
      controls proving each new refusal fires.
    validation_command: >-
      uv run --frozen packing-witness verify witnesses/kingbird-n029-2026-interval.yaml
    kill_condition: >-
      Stop if `verified_upper_bound` is moved, which is a human decision; stop if a claim
      is recorded without its relaxation, which would make an upper bound at an opened
      configuration indistinguishable from a claim about the optimum.
    fallback: >-
      Retain the schema widening and a typed statement of what the checker cannot replay,
      rather than a witness that passes because the checker is lenient.
    outcome: >-
      Built and replayed. `exact_verify` no longer raises `checker-not-built`; the n = 29
      certificate verifies through the public tool at 406 of 406 pairs strictly separated.
      Two refusals from the existing contract fired on the way and both were right.
    evidence:
    - >-
      '`scalar.kind` gains `interval-enclosure` as a fourth value rather than forcing a new
      contract version: no existing file changes meaning, and readers that switch on kind
      already fail closed on one they do not know -- `_exact_materialize` raises
      `formal-certificate-missing`. The kind carries the operator verdict, the certified
      pose box, the contact system and the declared relaxation.'
    - >-
      'A bug worth the file it is tested in. The first replay reported exactly 52 undecided
      pairs -- the packing''s contact count -- because the checker parsed 40-digit
      enclosures at mpmath''s ambient default of 15, widening them by about `1e-14` and
      swamping a relaxation of `1e-20`. Precision is now pinned from the witness''s own
      recorded digits. A replay whose verdict depends on the caller''s precision is not a
      replay, and the test asserts the witness verifies from ambient 15, 30 and 200.'
    - >-
      'Two existing contract refusals fired before the witness was accepted, and both were
      correct: a file without the softschema envelope, and a `verified` claim without a
      replayable certificate record. The certificate block now carries the operator, the
      box radius, the residual bound, the relaxation, the pair counts, the layout
      equivalence statement and both a replay and a rebuild command.'
    - >-
      'The witness stores the *relaxed* corners, because those are what was verified.
      Storing the unrelaxed ones and the relaxation separately would leave a reader to redo
      the shift and hope they did it the same way.'
    - >-
      'Evidence entry `E-n029-interval-certified-upper`, assurance `verified`, method
      `interval-certified`, replay passed. Its limitations say what the bound is not: not
      the optimum, not an optimality result, not the value the enclosures surround, and
      below exact-algebraic because soundness rests on the interval library''s directed
      rounding. `verified_upper_bound` is untouched.'
    stop_reason: criterion
    next_action: >-
      Register controls, run the gate, and close the block.
  - workflow: process-review
    recording: contemporaneous
    clock_role: finalization
    focus: process
    commitment: BC-057
    bead: think-pfwx
    objective: >-
      Register the block's controls, reconcile the synopsis with the built checker, and
      leave the checkpoint pushed.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: The scientific phases reached their criteria.
    budget_minutes: 6
    started_at: '2026-08-28T23:19:00-07:00'
    deadline_at: '2026-08-28T23:25:00-07:00'
    expected_output: Controls that fire, a green gate, and a pushed checkpoint.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: Stop if a control is registered without having been watched to fire.
    fallback: Push with the failing step named.
    outcome: >-
      Closed. Controls rise from 97 to 100 and all 100 fire. Two of the three needed their
      expectations corrected against what the mutation actually reports, which is the
      reason each is watched rather than assumed.
    evidence:
    - >-
      'Three controls registered: a replay that inherits the caller''s precision instead of
      the witness''s, a root that is not unique replayed anyway, and an enclosure written
      backwards accepted. The first reproduces the bug found in phase 2; the third is
      caught by `mpmath` itself refusing an inverted enclosure.'
    - >-
      Two stale claims in the synopsis are corrected: it said the interval checker was
      missing and that the strategy returns `checker-not-built`. Both were true when
      written and are not now.
    stop_reason: criterion
    next_action: >-
      Open block 6 as session-040 under BC-058 and `think-km5r`: give the pose model a
      chirality so the reflected n = 29 squares can be assembled.
  primary_bead: think-qs6k
  status: completed
  budget:
    wall_minutes: 45
    orientation_minutes: 3
    checkpoint_minutes: 10
    slice_minutes: 30
    finalization_minutes: 6
  stop_conditions:
  - The block deadline at 2026-08-28T23:25:00-07:00
  - Any move of verified_upper_bound, which is a human decision
  - A recorded claim whose relaxation is not stated alongside it
  - A correction that cannot itself be checked against the commit timestamps
  progress:
    metric: >-
      Whether an interval certificate can be reviewed by someone who did not produce it
    before: >-
      No. The result was a driver script and a retained JSON; `exact_verify` raised
      `checker-not-built` and the contract had no scalar kind for an enclosure.
    after: >-
      Yes. `packing-witness verify witnesses/kingbird-n029-2026-interval.yaml` replays it
      from the file alone, at any ambient precision, and refuses the three ways it should.
      The bound is recorded as evidence and has not been promoted.
  delegations: []
  outputs:
  - witnesses/witness.schema.yaml
  - witnesses/kingbird-n029-2026-interval.yaml
  - src/sqpack/witness.py
  - cases/kingbird29/certify_interval.py
  - tests/test_witness_interval.py
  - frontier/evidence.yaml
  - defects.yaml
  - devtools/controls.yaml
  checks:
  - 'uv run --frozen packing-witness verify witnesses/kingbird-n029-2026-interval.yaml: VERIFIED, 406 pairs'
  - 'uv run --frozen --group dev python -m devtools.run_negative_controls: 100 of 100 fire'
  - 'uv run --frozen packing-ledger check: OK'
  stop_reason: >-
    Both work phases reached their criteria inside the block clock, which was read from a
    clock this time rather than estimated.
  next_action: >-
    Open block 6 as session-040 under BC-058 and `think-km5r`. Merge origin/main first,
    then give the pose model a chirality so the seven reflected n = 29 squares can be
    assembled, or state what that costs the feature naming. The middle layers run before
    the efficiency and research cells, which are deliberately last.
---
# session-039 — block 5, the certificate enters the record

Block 5 of [agenda-006](../agendas/agenda-006-overnight-research-blocks.md), and the
first of the missing middle layers.

## Two things, and the first was not planned

Reviewing the clock before scheduling the continuation showed that this run had been
wrong about its own history.
It declared blocks of 150, 180, 180 and 40 minutes and took 31, 42, 29 and 23; it
declared a 690-minute target and stopped after 143.

The bookkeeping is the smaller half.
The misreading also supplied a *reason*: `BC-055` was recorded stopped because later
blocks had overrun into its slack, and nothing had overrun — the run stopped with most
of its budget unspent.
A constraint the run claimed to meet was in fact a mistake it made, which is the
flattering direction, and it is [D-358](../../../defects.md).

## What the block was for

The `n = 29` certificate existed as a script and a JSON file.
Nobody else could check it, because the witness contract had no way to say what it was:
`scalar.kind` offered `decimal`, `rational` and `algebraic-number-field`, and an
enclosure is none of those.

It now offers a fourth, and `exact_verify` replays one instead of raising
`checker-not-built`:

```
$ uv run --frozen packing-witness verify witnesses/kingbird-n029-2026-interval.yaml
VERIFIED
  id: W-kingbird-n029-interval
  n: 29
  method: interval-certified
  pairs tested: 406
```

The kind was added rather than a new contract version opened.
No existing file changes meaning, and readers that switch on `kind` already fail closed
on one they do not know.

## The bug the replay found

The first replay reported exactly 52 undecided pairs — the packing’s contact count — and
the packing had not changed.
The checker was parsing 40-digit enclosures at mpmath’s ambient default of 15, widening
them by about `1e-14` and swamping a relaxation of `1e-20`.

Precision is now pinned from the witness’s own recorded digits, and the test asserts the
witness verifies from ambient 15, 30 and 200. A replay whose verdict depends on the
caller’s precision is not a replay.

## What is recorded, and what is not

`E-n029-interval-certified-upper` carries assurance `verified`, method
`interval-certified`, and a replay that passes.
Its limitations say what the bound is not: not the optimum, not an optimality result,
not the value the enclosures surround, and below `exact-algebraic` because soundness
rests on the interval library’s directed rounding rather than on exact predicates.

`verified_upper_bound` has not moved.
Recording a certificate and promoting it are different acts, and only the first is a
runner’s to make.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
