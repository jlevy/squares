# Postmortem: Three Catalogue Intakes Nobody Owned

**Date:** 2026-10-05

**Author:** Claude (agent), for the project owner

**Status:** Complete

**Scope:** the Kingbird catalogue’s September 2026 improvements at $n = 69, 83, 87$,
held as `pending_catalogue_intake` from 2026-09-30 until the owner asked about them on
2026-10-05 ([D-519](../../../defects.md)); two more instances found the same day, an
import held past the pull request it waited for and two evidence updates a packet named
and did not retain; and the intake process that let all three wait with no owner.

## What happened

On 2026-09-30 a refresh captured the Kingbird catalogue again and compared it with the
capture of 2026-08-22 (`1d4020e9f`). `devtools.diff_kingbird_catalogue` found 41 counts
at $n \le 324$ printing a lower side.
At 36 of them a certified packet already reported a smaller side.
$n = 126$ and $179$ took the new sides, because their results were published before 22
August. Three counts were left: $n = 69$ (David Ellsworth, September 2026), and $n = 83$
and $87$ (Allen Chang, September 2026).

Each was a result by others published after the register’s cutoff, so
[epistemics.md](../../../epistemics.md#results-by-others) requires the register to hold
it before the record takes it.
The refresh handled that correctly.
It declared the three under `pending_catalogue_intake` (`a897e4031`), gave each case
record a `source-evidence` blocker that `STATUS.md` shows as “catalogue ahead, intake
pending” (`b8502282d`), and documented the state in the frontier README (`5358bfbba`).

Then nothing happened for five days.
The frontier went on reporting the older sides as each count’s best known upper bound,
and on 2026-10-05 the owner noticed that $n = 83$ was stale and asked how the intake had
been missed.

## Timeline

| Date | Event |
| --- | --- |
| 2026-08-22 | The catalogue is captured; the UnitSquare and certified-packet intakes read this capture |
| 2026-09-24 | The catalogue’s server dates the page that carries the September improvements |
| 2026-09-29 | The Couzo intake compares its packings with the live catalogue; the record’s capture is not refreshed |
| 2026-09-30 | The catalogue is captured again; the three counts are declared pending, their records carry the blocker, and the guide describes it. No commit names a bead for registering them |
| 2026-10-01 | `plan-2026-10-01-result-status.md` lists “Register the three catalogue intakes” under Follow-Up Work. The other two items in that list name their beads; this one names none, and no bead is opened |
| 2026-10-01 to 10-04 | Import work follows the GitHub issues. `check_requests --backlog` never lists the three, and every gate run passes `check_source_coverage` |
| 2026-10-05 | The owner reports $n = 83$; `think-s1xt` (the import) and `think-ywso` (this defect) are opened |

## Root cause

The deferral was correct and recorded, but nothing owned it: no open bead tracked
registering the three results, and the plan line that named the work named no bead.
Every tool that lists import work reads GitHub issues (`check_requests --github`,
`--report`) or register entries (`--backlog`), a count pending catalogue intake is
neither, and `check_source_coverage` accepted the declaration however long it stood.
The runbook began an import from “a GitHub issue, or a link”, so an input that arrived
through the catalogue had no step that would come back to it.

The catalogue refresh contributed: it was a hand-run `curl` and `html2text`, described
as a dated research survey, with no command anyone would run to ask whether the
catalogue had moved again.

## Two more of the same, found the same day

The coordinator of the 2026-10-05 follow-up found the gap twice more while this
postmortem was being written.

**A wait that outlived its blocker.** `think-e6ss` imported wand125’s 16 mixed
certificates of 4 October as far as a packet (`wand125-mixed-bounds-2026-10-04`, merged
in PR #339) and held stage 3 “until jlevy/squares#305 merges”.
#305 merged at 23:00 UTC that evening, and nothing resumed the import: #282’s
`oct3-oct4-mixed-14` stayed `queued: true`, owned by no bead of its own, since the
issue’s answer bead owns the reply and its `beads` list did not name `think-e6ss`.

**Evidence a packet named and nobody took in.** The same packet’s README says wand125’s
`c56b9b7` and `1ebd484`, evidence updates to the $s(59) = 8$ and $s(45) = 7$ covers, are
not retained by it. Both commits are ancestors of its pin, so no count of commits past
the pin could see them, and no bead was opened for either.
`3f063bd` and `781afb3`, later updates to $s(77)$ and $s(21)$, came after the pin and
went unread as well.

All three have one shape: the record could hold work back and had no place that listed
what it held.

## What has changed

| Change | Guards against |
| --- | --- |
| `pending_catalogue_intake` requires `bead` and `recorded` in its schema, and `check_source_coverage` refuses an entry without them; a `deferred-conflict` beyond-horizon claim requires a `bead` | A deferral with no owner |
| `check_bead_tree` fails every deferral whose bead is closed or missing: pending intakes, deferred conflicts, repository reads that name a bead, and the `answer_bead` of every open issue | An owner closed while its deferral stands |
| [`devtools.intake_sweep`](../../../packing/devtools/intake_sweep.py), run by `make intake`, reads GitHub, every watched repository, the newest catalogue capture, the other catalogues and the record’s own queues, and exits 1 while any item has no open bead | An input that no tool lists |
| [`devtools.capture_kingbird_catalogue`](../../../packing/devtools/capture_kingbird_catalogue.py) captures the page into `attic/intake/`; given either retained HTML file, it reproduces that capture’s transcription body byte for byte | A capture that only a by-hand command could make |
| [`intake-watch.yaml`](../../../packing/campaign/intake-watch.yaml) records a repository read past its packets, with the bead that owns what it holds or a note that nothing does | A repository read and found empty looking the same as one never read |
| [result-import.md](../../../packing/campaign/result-import.md) gains Running an Intake Pass, Intake Sources and Stage 0: Sweep | A process that started only from an issue or a link |
| A queued result or ask in `result-requests.yaml` takes its own `bead` and a `blocked_on`; `check_bead_tree` fails a named bead that has closed, and the sweep reports a queued item with no bead of its own | An import that only an issue’s answer bead was said to own |
| The sweep reports an open import bead, or a queued item, whose stated blocker has merged or closed: `blocked_on`, a sentence such as “waits for jlevy/squares#305”, or a `blocks` dependency once all have closed | A wait that outlives its blocker |
| A pin is structured, an acquisition record’s commit or a revision in a register source’s address; the sweep reads trees as well as commits and reports commits a pin contains whose changed paths no packet at or after them retains | Evidence a packet names in prose and does not retain |

Three repairs were needed to make the sweep run.
`check_requests --github` paged with `gh api --paginate`, which follows GitHub’s
`repositories/{id}` links; the agent session’s proxy refuses those, so the comparison
failed on its second page.
It now asks for pages by number.
The bead-alias reader kept the quotes `tbd` writes around a numeric-looking alias such
as `"48e1"`, so 26 beads could not be named as owners.
And in a linked worktree `check_bead_tree` read the bead store blob by blob from the
sync branch, 17 s, where the shared sync worktree takes 0.6 s.

## The other lists that hold work back

Every list in the records that holds work back for later was checked for the same gap:

- **An open issue’s queued results and asks** were taken to be owned by its
  `answer_bead`, which the schema requires and nobody checked.
  `check_bead_tree` now checks every open issue’s answer bead, and every one passed on
  2026-10-05. The answer bead owns the reply, not the import, so a queued item now names
  its own `bead`. The schema leaves it optional until the three queued items open on
  2026-10-05, which other lanes are importing, carry one; the sweep reports each until
  then. *Note, 2026-10-23:* the schema now requires it, and `check_bead_tree` fails a
  queued item that names none (`think-du1e`).
- **A register entry’s `activity`** expires: `check_results` refuses one more than 30
  days older than `last_reviewed`. It may link a branch or a file rather than a bead, so
  it is left to that rule.
- **The validation backlog**, entries below `V3` or `C3`, says what is queued in
  `next_rung`. Six of the ten name no bead.
  An entry with nothing in hand legitimately waits, so the sweep lists them and does not
  fail on them.
- **A stopped session’s `certification_pending`** already requires its follow-up bead
  (`OR-13`).
- **Superseded reports** and **superseded-covered sources** are settled states, not
  deferrals.

## The first sweep

The sweep, run on 2026-10-05 before that day’s intake lanes merged, found 29 items with
no owner besides the three counts: 15 comments on #282 and #281 after their entries’
`read_through`, 11 watched-repository items (heads past every pin, and wand125’s two
unretained commits), and the 3 queued items with no bead of their own.
It found 8 open import beads waiting on a pull request or bead that had already merged
or closed, `think-e6ss` among them.
The other channels had the same gap; the catalogue was only where it showed first.

## The rules this yields

**R1. A deferral names an open bead, and the gate checks the bead.** A name the gate
cannot resolve is the same orphan as no name.

**R2. One command reads every source, and says which it could not read.** A quiet report
from a sweep that skipped a source is not a clean one, so the source is listed as not
checked rather than left out.

**R3. A wait names what it waits on, and something reads it.** A blocker written only in
prose resolves silently; the sweep reads the prose, and `blocked_on` saves it the
guessing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
