# Bead and Plan Reconciliation, 10 October 2026

Status: reviewed and reconciled under `think-p2z4`.

## Scope and Ownership

The baseline contains 4,681 beads: 3,683 closed, 799 open, 194 in progress, and five
deferred. The review covers every one of the 998 non-closed beads and all 53 plan
specifications. Closed beads supply dependency and completion context; their underlying
deliverables are not independently reverified by this administrative review.

Two Sol agents review disjoint bead and spec queues under `think-1a9o` and `think-sjz7`.
A third prepares optional upstream tbd coordination guidance under `think-nx5z`. The
coordinator owns shared tracker updates, integration, and commits.
The workflow entry is `general-improvement`; this pass launches no research work.

The retained [coverage baseline](review-2026-10-10-bead-reconciliation-baseline.json)
records the exact review scope.
The lane reports carry each proposed disposition and its evidence.
A retained disposition means the current review did not justify changing the status; it
is not a new certification that the work is actively executing.

## Coordination Policy

[OR-19](../../../operating-rules.md#or-19-confirm-one-bead-owner-before-work-sync-at-session-start-after-commits-and-at-handoff-or-end)
requires identifiable ownership, accepted claims before execution, disjoint delegation,
and verified sync at session start, after each commit, and before handoff or end.
The generated `AGENTS.md` summary exposes the rule at session entry.
Administrative reconciliation owns a review bead and does not take over the
implementation beads it inspects.

These are Squares requirements.
Upstream tbd retains lightweight use and offers an explicit coordination workflow for
collaborators. The existing `start` JSON result, including skipped claims, is sufficient
to check local ownership without changing exit codes or claiming a distributed lock
across independent clones.

## Repeating the Review

The inventory command reads a full `tbd list --all --json` export and emits disjoint
review queues. It includes closed children, recognizes exact former-root path moves, and
distinguishes missing ownership data from metadata omitted by the list command.
It never changes beads.

From `packing/`, with the project Python environment:

```bash
python -m devtools.reconcile_work SNAPSHOT.json
python -m devtools.reconcile_work SNAPSHOT.json --baseline
python -m devtools.reconcile_work \
  ../docs/project/reviews/review-2026-10-10-bead-reconciliation-baseline.json \
  --reviews \
  ../docs/project/reviews/review-2026-10-10-bead-reconciliation-a.json \
  ../docs/project/reviews/review-2026-10-10-bead-reconciliation-b.json
```

The coverage check rejects missing or duplicate dispositions and proposed mutations
without cited evidence.
It establishes review coverage, not the truth of each proposed completion.
The coordinator must inspect the supporting evidence and re-read current bead versions
before applying changes.

## Reconciliation Decisions

The [lane A review](review-2026-10-10-bead-reconciliation-a.md) and
[lane B review](review-2026-10-10-bead-reconciliation-b.md) cover all 998 beads and 53
specifications without overlap.
Their final bead dispositions are seven closures, 100 updates, 646 retained, and 245
needing further evidence.
The updates comprise 99 exact governing-path repairs and two explicit paused holds, with
one overlap.

The seven verified closures are `think-5o8i`, `think-6l39`, `think-ele8`, `think-giqi`,
`think-rs0t`, `think-r7yt`, and `think-ny3r`. `think-23td` and `think-lhyk` retain their
unfinished scope with paused holds.
The earlier instruction proposal `think-gc95` is consolidated as a duplicate of the
assigned upstream lane `think-nx5z`; `think-kc9d` now names only the remaining
execution-order evaluation work.
Existing blocked and paused holds remain intact; historical network failures and old
prerequisite notes do not justify new deferrals.

Thirteen specifications leave `active/`: eight completed plans move to `done/`, two
unlaunched plans to `draft/`, the generalized Motion Lab plan to `paused/`, and two
historical or superseded plans to `archive/`. Three active plans get corrected status
text. Incoming and outgoing links, the document map, its rendered SYNOPSIS, math-markup
paths, and the affected consumer test follow the moves.

The [applied receipt](review-2026-10-10-bead-reconciliation-applied.json) distinguishes
tracker changes from the lane proposals.
Path repair also covers closed beads whose former-root links obscure a plan’s
decomposition. This is metadata repair, not a new verification of their completed work.
Native `tbd update --spec` can propagate to children.
A fresh tracker inventory verifies all 526 intended path repairs, with no mismatches.
The bead-tree check reports no problems or warnings after reconciliation.

The review retains all uncertain work.
In particular, a delivered draft is not accepted production work, a proposed negative
retirement still needs its named owner review, and an optional replay remains unfinished
after it stops gating promotion.
Existing beads remain the owners of those decisions; the review creates no duplicate
implementation queue.

## Evaluating the Next Sessions

At the next coordination review, sample ten completed delegated slices from their beads
and session transcripts.
Record the numerator and denominator for each check:

- The dispatch names a bead, unique acting owner, and disjoint write scope; the worker
  acknowledges that assignment before editing.
- The claim result is accepted and its sync succeeds before execution.
  A skipped claim followed by work is a failure even if the command exits zero.
- Every commit has a progress update and successful sync from the tracker owner,
  including commits whose CI is still pending.
- Completion or handoff carries evidence, an accurate remaining-work status, and a
  successful final sync; a transferred owner acknowledges before continuing.

Report unavailable transcript evidence separately from confirmed failures.
Count actual overlapping execution and preventable duplicate beads as outcomes, rather
than treating generic delegate names as proof.
Compare this sample with the next ten slices before adding stricter enforcement.
Lightweight projects can omit this review entirely.

The retained inventory and coverage check support periodic queue reconciliation.
They do not observe execution order; automatic checkpoint verification would require
explicit event receipts or session-log integration and is a separate upstream proposal
under `think-kc9d`.

## Validation and Upstream Follow-up

The audit tool passes 16 focused tests, Ruff, and BasedPyright.
Its coverage check accepts exactly 998 bead and 53 spec dispositions.
Documentation validation covers 1,996 documents; the moved-path math-markup inventory
also passes. Independent review caught and resolved malformed mutation-field acceptance,
unsupported baseline options, and the sorted inventory requirement.

The pre-push run passed 65 structural, type, browser, and record checks.
Its behavioral step completed 4,211 tests with 29 skips, then reported 33 failures and
1,321 setup errors amid external-volume exhaustion (`ENOSPC`). The run took 1,063.58
seconds. Completed disposable fixtures were removed; only 2.8 GiB remained on the shared
volume, so the broad suite was not repeated locally.
Hosted PR checks supply the remaining validation; this run is not recorded as a passing
pre-push tier.

The optional upstream shortcut is proposed in
[tbd PR #324](https://github.com/jlevy/tbd/pull/324), tracked by `tbd-9fvc`. Separate
upstream follow-ups record the close-with-hold failure (`tbd-hqte`) and bulk spec-update
limitation and help mismatch (`tbd-3vuh`). They are outside the instruction-only
coordination proposal.

## Limits

Age, a generic delegate, and all children being closed are triage signals.
None proves that a workstream is finished or that its owner has stopped.
Missing completion evidence leaves the work open; a missing governing document needs
investigation rather than a guessed replacement.
A specification with unchecked scope is not completed merely because its current
decomposition is closed.

Snapshot metadata cannot prove whether claims were published before execution or whether
two agents performed the same work.
The earlier audit `think-qpm4` found that installed tbd v0.10.0 can update
`last_sync_at` during search without performing a Git sync, so that timestamp is not a
compliance receipt.

## Status Addendum, 13 October: What Merging Decides

Senior review A on PR #493 (A1) found that the tracker changes are already applied:
`tbd-sync` carries them whether or not the PR merges.
Merging adopts the file moves, OR-19 and its `AGENTS.md` summary, the tools and the
records. It does not decide the bead closures, holds, notes and `spec_path` repairs of
this round, [round 2](review-2026-10-12-bead-reconciliation-round-2.md) or the
[owner decisions of 13 October](review-2026-10-13-owner-decisions.md); those were
applied when each round ran.
The owner accepted this round’s applied set on 11 October.

Some repairs depend on a move: on 13 October, 453 beads (62 not closed) named a plan
path that exists on this branch and not on `main`, across 22 plans.
`reconcile_work SNAPSHOT.json --branch-only-paths` lists them.
Every one of those 22 files came from `docs/project/specs/active/` under the same name,
so a declined move is undone with
`tbd update <id> --spec docs/project/specs/active/<file>` for each bead the listing
names. The applied records also keep each repair’s `from` and `to`.

Neither plan this round filed in `draft/` stayed there.
[Round 2](review-2026-10-12-bead-reconciliation-round-2.md) moved interval certification
to `done/`, since it had been built the day after it was written, and review A on #493
(finding A2) moved the numeric-symbolic round trip to `archive/`, as round 2’s addendum
records. `draft/` is empty.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
