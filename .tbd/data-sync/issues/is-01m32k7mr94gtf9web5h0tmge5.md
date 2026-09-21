---
type: is
id: is-01m32k7mr94gtf9web5h0tmge5
title: check_session_gate cannot bootstrap a record authored terminal
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m32dvmtc77znp14556p7c5w2
created_at: 2026-09-21T18:21:43.048Z
updated_at: 2026-09-21T18:21:43.048Z
---
A session record authored `status: completed` in its first commit has no commit at
which its gate can pass, so it can never earn its own first receipt. Found on PR 211
(branch claude/n17-mira-guzhou-4613-intake), where it was the last blocker.

## The constraint, as measured

1. `check_session_gate` demands a passing `full gate:` declaration at every commit where
   the record is terminal (`completed` or `stopped`) and numbered at or above
   `GATE_DECLARED_FROM`. So every hosted run on such a branch fails that one step, and
   the record can never cite a green run naming its own tree.
2. `certification_pending` is refused for `completed`: `check_session_gate.py:377`,
   "certification_pending is allowed only when stopped".
3. The working route every recent session used is invisible in the code and unstated in
   the docs: the record sits `status: in_progress` at the commit the gate runs on, so the
   check demands nothing, and the closeout commit makes the record terminal AND supplies
   the receipt in one act. Verified: session-147 declares `e2721b68` and its closeout
   `bfeba117` is that commit's direct child; at `e2721b68` the record read
   `status: in_progress`. Same shape for session-148 at `e2530693`.

## Why the in_progress route cannot be applied retroactively

Recreating that state on a record whose session ended earlier is refused by
`sqpack/campaign/ledger.py`, three ways, and each refusal is correct:

- `in-progress session deadline_at has passed` (line 1009), and removing the field gives
  `in-progress session needs an offset-aware deadline_at`. A future deadline also needs
  `budget.wall_minutes` inflated, since `deadline_at - started_at` is bounded by it.
- `session status does not match final workflow phase` (line 1178): the final phase must
  also be `in_progress`, which is false of a phase that completed with its own outcome
  and evidence.
- `in-progress workflow phase N deadline_at has passed`, for the phase clock.

Those rules exist because of `D-358`. So the ordering constraint is load-bearing: a
record must be authored non-terminal, gated, and only then closed. Nothing says so.

## What would close this

Either state the ordering constraint where a session author will read it
(`campaign/agent-sessions/README.md`, beside the `certification_pending` paragraph at
lines 187-193, and in `check_session_gate`'s module docstring), or give the checker a
bootstrap: for instance allow `certification_pending` on a `completed` record, or accept
a terminal record whose only missing receipt is its first.

PR 211 was unblocked by the documented alternative rather than by a code change:
session-149 is `stopped` with `certification_pending: think-pcd0` and two real `failed`
declarations, which is what `agent-sessions/README.md:187-193` prescribes for work that
stops before its validation succeeds.

Adjacent, and about readings of this same checker: `think-qsn2` (ancestry verdicts
depend on which refs a clone holds, so sessions 087-090 and 112-113 fail on a full clone
and pass in CI) and `think-fqut` (stacked-PR merges rebase child branches and orphan the
commits their `checks:` declare).
