# Bead and Plan Reconciliation, Round 2, 12 October 2026

**Status:** Reviewed and applied under `think-va12`; the questions under
[Owner Decisions](#owner-decisions) remain open on their beads.

## Scope and Ownership

This round continues the
[10 October reconciliation](review-2026-10-10-tbd-coordination.md) on the same branch,
after `main` at `e96e9ea95` was merged in.
The snapshot of 12 October holds 4,976 beads: 3,853 closed, 848 open, 270 in progress
and five deferred. The review covers every one of the 1,123 nonclosed beads and all 55
plan specifications, as the
[retained baseline](review-2026-10-12-bead-reconciliation-baseline.json) records.
Of those beads, 157 were created after the first round’s baseline, and 236 of the first
round’s 245 `needs_evidence` beads were still open.

The workflow entry is `general-improvement`; no research work was launched.
The coordinator owns the epic `think-va12`, every tracker mutation, the records and the
commits. Five read-only lanes, one bead each (`think-du14`, `think-cxpm`, `think-5i2o`,
`think-m2k7`, `think-njpv`), ran on Opus at high effort, the
[OR-2](../../../operating-rules.md#or-2-run-three-to-five-sub-agents-at-a-model-and-thinking-level-matched-to-the-task)
row for record bookkeeping.
Each lane received a queue in which every spec travels with the beads its `spec_path`
names, so one reviewer decided a plan’s folder together with the work it governs.
Each returned an evidence-bearing disposition per item, in
`review-2026-10-12-bead-reconciliation-lane-N.json`.

## Results

The coordinator verified the lane proposals, changed three bead dispositions, added five
re-homes the lanes named only in prose, reworded five status lines, and applied the
result. The [applied record](review-2026-10-12-bead-reconciliation-applied.json) holds
the final disposition for every bead and spec and a receipt of what changed.

| Bead disposition | Count | Notes |
| --- | --- | --- |
| Close | 101 | 95 completed, 4 duplicates, 2 canceled; 62 were in progress |
| Update | 57 | 41 governing-document re-homes, 13 dated notes, 6 `blocked` holds |
| Retain | 943 | Live and correctly described; the reason names what is still open |
| Needs evidence | 22 | Each names the missing fact or owner decision |

Of the 236 beads the first round left at `needs_evidence`, nine closed, seventeen were
updated, 200 were found live and retained, and ten still need a decision.
Of the 157 new beads, 35 closed.

Every commit of this repository that a close cites is on `origin/main`, and every pull
request a close cites as merged is merged.
No close leaves an open child under a closed parent.

Twenty plans changed lifecycle folder, and six active plans got corrected status lines.

| Folder | Before | After | Plans moved in |
| --- | --- | --- | --- |
| `active/` | 42 | 23 | — |
| `done/` | 8 | 23 | fifteen: four completed session plans (n17 overnight, ten-hour, four-hour, six-hour), post-optimality W3, constructive enumeration, symbolic promotion, gate validation speed, post-3.81 sequence, video delivery, epistemics ladder, result status, the n = 11 explainer series, Fibonacci torus, and interval certification |
| `paused/` | 1 | 3 | the minimal packing toolkit, idle since 23 August with 43 untouched beads; the promotion pipeline, held since 27 August on its n = 29 preconditions |
| `archive/` | 2 | 4 | the after-R052 plan and its successor, the after-4640020 overnight queue, which never ran; both defer to agenda-042’s cells |
| `future/` | 0 | 1 | the n17 eight-hour proof block, prepared and held under paused agenda-046 |
| `draft/` | 2 | 1 | — |

The interval-certification plan moves from `draft/` to `done/`, reversing the first
round. All four of its phases were built on 29 August under agenda-006, so its fifteen
boxes are now ticked.

Each move took its incoming links with it: 92 files across specs, agendas, sessions,
hypotheses, templates, the document map, `math-markup.yaml`, `defects.yaml`, and one
consumer test. The beads followed too: 29 open beads named on a moved plan were re-homed
to the agenda, exploration or review that now governs them, and the other 150 beads
naming a moved plan, 99 of them closed, were repointed to its new path.
Done and archived plans are marked as records in the document map.

## Coordinator Amendments

- **`think-vore` stays open:** Lane 3 proposed closing it as canceled, but the decision
  is recorded only in the exact-side-values plan on the unmerged PR #435 branch, and the
  bead is a live claim of that workstream’s agent.
- **`think-om5l` and `think-ga3m` stay in progress:** Their imports are complete.
  But `packing/campaign/intake-watch.yaml` still names them as owners of two
  repositories’ read-throughs, and `check_bead_tree` requires every deferral a record
  declares to name an open bead.
  They were closed, then reopened and restored to their prior claim when the local check
  failed. Each should close in the change where an intake pass updates its entry.
- **Two lanes disagreed about agenda-042’s beads:** Lane 5 re-homed four beads to the
  after-4640020 plan, which lane 1 archived; all seven beads now point at agenda-042.
- **Five lane status lines were reworded:** each cited a plan this round also moved, or
  said “governed elsewhere” without naming where.

The gate-validation-speed plan’s one unchecked item, an agent-log rollup, is recorded as
not done. The question it served passes to the validation-efficiency plan.
`development.md` now gives the measure-verifier tier’s recorded 72.83 s cohort, which
was still described as pending under the now-closed `think-th8p`.

## Discovered Work

Two follow-ups had no bead:

- `think-ni9u`: BuddenPing posted refined certificates on #503 (N207, T-147) and #504
  (N153, T-148) after both issues closed.
- `think-6l0e`: exp-046 names one preregistered re-run of the H-044 chunk census with
  the contact-relaxed universe as the follow-on to `think-l48p`, which this round
  closed.

## Owner Decisions

These are recorded on their beads.
None blocks the reconciliation.

- **Scope:**
  - `think-vb7g`: should the atlas stop at 324, or build the caveated 325 to 400 form?
  - `think-91yk`, `think-nho8`, `think-7c17`: BC-388 to BC-390 are n = 11 settlement
    work still marked ready, although T-060 settles s(11). Retire them?
  - `think-q6vy`: should its SYNOPSIS follow-ons be retired or re-homed so the bead can
    close?
- **Claims:**
  - `think-vtc1`, `think-t7a9`, `think-nymu`: the exact-side-values plan says
    `think-wgo1` has taken over their work.
    Release the old claims?
  - `think-wklm`, `think-ic0g`, `think-j30w`, `think-tswc`: are these v2-transitions
    spike claims superseded by the workbench package beads?
- **Lifecycle:**
  - Confirm that the minimal packing toolkit belongs in `paused/`.
  - Confirm that the eight-hour proof block belongs in `future/` until a launch
    instruction.
- **Unmerged agenda:** `think-d3z8`, `think-du2j` and `think-oc16` are governed by an
  agenda that exists only on the unmerged branch `claude/nice-fermi-v8fhi2`. Its BC-376
  to BC-378 numbers collide with agenda-042’s.
- **Closes awaiting a decision:**
  - `think-dc0p`: duplicate of `think-ndvg`?
  - `think-fh5n`: close draft PR #407?
  - `think-geid`: accept a retire-negative?
  - `think-98mg`: does BC-451’s retire-negative discharge the bead’s own “keep open”
    note?

## Repeating the Review

From `packing/`, with the project Python environment:

```bash
tbd list --all --json > SNAPSHOT.json
python -m devtools.reconcile_work SNAPSHOT.json --split 5 \
  --prior ../docs/project/reviews/review-2026-10-12-bead-reconciliation-applied.json
python -m devtools.reconcile_work SNAPSHOT.json --split 5 --baseline
python -m devtools.reconcile_work BASELINE.json --reviews LANE-1.json ... LANE-5.json
git fetch origin main
python -m devtools.reconcile_work --check-commits FINAL.json   # --strict: fail on unresolved
python -m devtools.move_documents OLD=NEW ...          # dry run; --apply git-mvs and writes
python -m devtools.reconcile_work FRESH-SNAPSHOT.json --verify EARLIER.json ... FINAL.json
python -m devtools.check_bead_tree
python -m devtools.check_math_markup     # move_documents keeps `migrated` sorted
```

`--split` keeps each spec with the beads it governs, and `--prior` carries the last
round’s dispositions forward as context.
Each spec now reports its folder and whole status line.
`--check-commits` refuses a close that cites a commit missing from `--base`
(`origin/main`, fetched first), and a base that does not resolve.
`move_documents` repoints bare, `./`, `../` and repository-relative references, leaves
frozen records alone (every reconciliation record here among them), and reports a moved
path it leaves in fenced code.
`--verify` checks a fresh snapshot, each bead’s `tbd show` record and the tree against
what was applied; give it every round’s records, oldest first, so that a later repair
supersedes an earlier one and a plan moved twice is found at its last place.
Run `check_bead_tree` before `tbd sync`, since CI reads the synced store and a close
that breaks an invariant turns every pull request red.

A `spec_path` repair that follows a file move reaches the shared tracker at once, while
the move reaches `main` only when its pull request merges.
Apply such repairs after the move merges.
When they are applied earlier, as rounds 1 to 3 were, run
`reconcile_work --branch-only-paths` before merging and keep its listing, so that a
declined move can be undone bead by bead.
`--needs-evidence` lists what every round so far left waiting on a named fact;
`think-bx03` owns that list.

## Validation and Limits

Hosted CI runs on the pushed head.
The tool changes pass 29 focused tests, Ruff and BasedPyright.
The coverage check accepts exactly 1,123 bead and 55 spec dispositions, for the lanes
together and for the applied record.
Documentation validation covers the moved plans’ links.
`--verify` reports 162 checks with no problems; holds and notes are not in a list
snapshot and are counted rather than checked.

The local pre-push run’s three behavioral failures are environmental.
Two process-group reaping tests fail in this container even in isolation.
A third passed when re-run alone, after commits made during the run disturbed it.

The review rests on recorded evidence and does not re-verify the scientific results
behind any close. A version check before each mutation cannot exclude a concurrent write
between check and update; three beads created by other agents during the round are
outside its baseline.

## Status Addendum, 13 October: A Move Without a Record, and a Stronger `--verify`

Under review A on [#493](https://github.com/jlevy/squares/pull/493) (finding A2, fixed
in `c60db5740` on its branch), the numeric-symbolic round-trip plan moved from `draft/`,
where this round retained it, to `archive/`: the promotion-pipeline plan superseded it,
and agenda-005 built the round trip.
No round’s record carried that move.
The [addendum record](review-2026-10-12-bead-reconciliation-addendum.json) now does,
read after this round’s applied record; the applied records themselves are unchanged.
[#579](https://github.com/jlevy/squares/pull/579), which replaced #493, carries the move
in `2a8ce4aea`.

Reviews B and C on #579 found that `--verify` skipped round 1’s past-tense actions
without a word, saw only `status` and `spec_path`, and judged each record alone.
It now reads round 1’s receipt and its `path_repairs`, and the `path_repoints` that
rounds 2 and 3 recorded in their receipts (after review D on #579), checks resolution,
`duplicate_of`, `close_reason`, holds, appended notes and the version guard through
`tbd show`, follows a plan moved twice, lets a later record supersede an earlier one,
counts what it cannot check by field, and fails when it recognizes nothing.
On 13 October, lanes A and B, the three applied records and the addendum, read oldest
first, gave 2,161 checks and no problems; the three applied records and the addendum
alone gave 2,150. Thirty-seven targets stayed unchecked: 28 plans’ `new_status` lines,
which the formatter rewraps and retypes, and eight close reasons and one note that round
1 did not record. The procedure above was updated the same day to match.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
