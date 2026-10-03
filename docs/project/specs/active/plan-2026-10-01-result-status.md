# Plan: A Workflow Status for Every Result, and No Separate Block for Reported Ones

**Date:** 2026-10-01

**Author:** Claude (agent), for the repository owner

**Status:** Proposal for the owner’s confirmation.
It is applied on the branch `claude/awaiting-replay` so it can be read as a diff and
looked at on the built site.
The status vocabulary, the rung at which a result is confirmed and the shape of the
activity mark are provisional; each is one small edit.

**Workflow:** W7 pipeline improvement

**Beads:** `think-d04u`, `think-ai94`

## Summary

The homepage carried a block under its results table, “Reported, awaiting replay: 48
cases, $n = 18$ to $95$”. The owner asked where it came from, why it was separate, and
that those results sit with the main results, each with its current status.

The 48 rows were not 48 results.
They were two register entries, T-046 and T-048, both already rows of the results table,
written out case by case.
The block was a port of a README table that listed cases, placed under a table that
lists results. Nothing in the record required a second listing.
The block is removed.
The two entries, and every other result this project has not replayed, are rows of the
one table, and what the block said about them is now a value of a status every row
carries.

The owner then asked for the table’s *Standing* to be reviewed, and proposed a status
that follows the project’s workflow: recorded, reviewed, confirmed, incomplete.
This plan defines those four as predicates over the record, derives them, and shows them
in place of the standing.
Whether a result is superseded stays as its own mark.
A second mark says who has the next move on a result, this project or someone else,
which the owner asked for as a way to tell results in analysis from results waiting on
others.

The record was also behind the work.
Complete replays of T-048, of T-055 and of 21 of T-046’s certificates passed on 29
September and sit on unmerged transfer branches.
The site said “awaiting replay” for results that had been replayed two days earlier.
That integration is its own piece of work and is not done here; the three entries now
say so.

## Where the Block Came From

| Step | When | What |
| --- | --- | --- |
| README’s table | 2026-09-29, `8b4488561`, `think-ti71` | `devtools.render_recent_results` generated “Recent Results, All Sources” in README: one row for each case $n \le 100$ with a recent lower bound, showing the verified bound and “the reported one where it differs”. It replaced a listing kept by hand that had drifted three times. |
| The homepage port | 2026-09-30, `886d4b583`, `think-yy2c` | The homepage took over what README’s generated tables showed. The rows whose reported lane differs (`Row.shows_reported`) became a disclosure under the recent list, grouped by holder. The bead was created after the fact and says so: “No bead was ever created.” |
| The $n = 11$ fix | 2026-09-30, `febdbe249`, `think-pd2g` | The block listed $n = 11$ as awaiting a replay that had happened, because a rounded reported value was compared as a number with the verified one. The comparison was fixed; the block went from 49 cases to 48. |
| README’s trim | 2026-09-30, `e4ad5cedd`, `think-f7ig` | README’s tables were removed in favour of the site. The block was then the only place the per-case listing survived. |

The spec for the site, [the overview plan](plan-2026-09-29-github-pages-overview.md),
recorded the block as built and gave no reason for it beyond the port.
The owner’s earlier question about it left no bead: a search of the tracker finds only
`think-yy2c` and `think-pd2g`.

## What the Block Listed

Every row came from a case record’s `reported_lower_bound`, and every one of those is
carried by a register entry: `check_results` fails when a recent reported lower bound
has none.

| Entry | Cases in the block | Claim | Source and date | Rungs | Standing | Replayed since? |
| --- | --- | --- | --- | --- | --- | --- |
| T-046 | 47: $n = 18, 19, 20$; $26$; $28$ to $31$; $37$ to $44$; $51$ to $61$; $66$ to $78$; $86$; $88$ to $91$; $94$ and $95$ | One rectangle-density lower bound a case, from $s(18) \ge 939/200$ to $s(95) \ge 49209/5000$ | wand125, 27 and 28 September 2026 | `V0/C0`, `S3` | current best, reported | In part, and not in the record. See below. |
| T-048 | 1: $n = 50$ | $s(50) \ge 37/5$ | wand125, 28 September 2026 | `V0/C0`, `S3` | current best, reported | Yes, in full, and not in the record. |

T-046’s 47 cases rest on 45 certificates; $n = 77$ and $n = 90$ take the certificates of
$n = 76$ and $n = 89$. Its 48th count, $n = 27$, was replayed on 27 September and is
T-045’s.

**The replays exist and are not integrated.** Ten replay batches were launched on 29
September (`think-20mv`). Five pushed receipts to transfer branches; each certificate in
them reports `VERIFIED` at all 201 directions.

| Where | What passed | Branch |
| --- | --- | --- |
| T-046, 21 certificates | $n = 18, 19, 20, 26, 29, 30, 38, 39, 40, 41, 52, 53, 59, 61, 67, 69, 71, 75, 78, 86, 95$ | `claude/replay-wand125-rect-b02`, `-b04`, `-b07`, `-b08`, `-b09` |
| T-046, 24 certificates | No receipt: $n = 28, 31, 37, 42, 43, 44, 51, 54, 55, 56, 57, 58, 60, 66, 68, 70, 72, 73, 74, 76, 88, 89, 91, 94$ (batches b01, b03, b05, b06 and b10 pushed nothing) | None |
| T-048 | The complete L740 replay: `ALL_ANGLES_VERIFIED_AND_REPLAYED`, 201 of 201 (`think-nnlg`) | `claude/replay-wand125-n50-l740-local` |
| T-055 | The complete point-only replay of $s(21) = 5$: `FRESH_ALL_DOMAIN_REPLAY_VERIFIED` (`think-ifsv`). Not in the block; it is the third `V0/C0` entry. | `claude/replay-wand125-n21-point` |

None of this is on `main`. Until the receipts are merged into their packets and entered
as evidence, the three entries stay at `V0/C0` by the checker’s derivation, which is
correct: a rung is earned by retained evidence.
What the site can say truthfully today is that they are recorded and in analysis here.

## Why It Was Separate

There was no distinction in the record that needed a second listing.
The block and the table read different files.
The table lists register entries.
The block listed cases, from the case records’ reported lane, because README’s table had
listed cases. One entry covering 47 cases was therefore one row of the table and 47 rows
of the block.

The table did show both entries, as *current best, reported*, at `V0/C0`. Its filters
start at `S4` and up on the homepage, and both entries are `S3`, so neither showed until
a reader changed the filter.
The block was, in effect, a way round that default.

Every other part of the site already treats these cases through one mechanism.
The frontier atlas has a reported lane beside the verified one for each case; the case
pages carry both; the star marks a case by its verified bound, so a reported bound stars
nothing; and the results page lists both entries.

## What Standing Was

Standing is derived by `render_recent_results.standing` from which evidence the case
records cite, and `devtools.check_standing` holds it to the numbers.
It is sound. It answered one question well and was being asked three.
The counts are of the 61 results the register held when the owner asked; four more
arrived the same day (T-062 to T-065).

| Standing | Results | What it says |
| --- | ---: | --- |
| superseded | 27 | It claims a bound, and no case bound rests on it now |
| current best | 21 | A verified case bound rests on it |
| none, shown as “not a bound” until the kinds landed | 9 | Its evidence claims no bound: a rigidity, a case exclusion, an audit |
| current best, reported | 2 | Only a reported case bound rests on it |
| second certificate | 1 | It proves a value another result holds |
| second certificate, reported | 1 | The same, and not replayed here |

It mixed three things.

- **Position on the frontier.** *Current best* and *superseded* say whether a case bound
  rests on the result.
  This is what the derivation is for.
- **Whether the bound has been replayed.** The suffix *reported* repeats the
  confirmation rung. T-046 is `C0` and *reported*; no result can be one without the
  other.
- **What kind of result it is.** *Second certificate* and *not a bound* say what the
  entry is, which no bound can change.
  [The result-kinds plan](plan-2026-10-01-result-kinds.md) took *not a bound* out on the
  same day and gave every result a kind.
  It left five results of a kind that is no bound still carrying a standing, because
  each cites a bound’s evidence: T-003, a method limit, *superseded*; T-004, an audit,
  and T-005, a correction, *current best*; T-054 and T-055, simplifications, *second
  certificate*. This plan settles them.

A reader got little from it.
On the page, *current best* drew no chip, so 21 rows showed nothing; 27 rows said
*superseded*; 9 said *not a bound*, and then nothing; and 4 rows carried any other word.
As a filter it separated superseded results from the rest, which the “Hide superseded”
checkbox beside it already did.
It did not say where a result stands in this project’s work on it: taken in, read,
replayed, or stuck.

## The Proposal: Status

One field, named **status**, with a closed vocabulary.
It is derived by `devtools.result_status` from the register and the evidence a result
cites. It is never stored, so it cannot be set by hand or drift from the rungs.

| Status | Meaning | Predicate | Results |
| --- | --- | --- | ---: |
| recorded | Registered here from its source; nothing here has read or replayed it | `C0` | 3 |
| reviewed | Its argument has been read here and the read is on file; no replay has passed | `C1` | 4 |
| confirmed | A confirming replay has passed, here or by a third party whose replay is retained | `C2` and up | 56 |
| incomplete | The record holds an open defect against it | See below; it wins over the other three | 2 |

A result is **incomplete** while any of these holds:

1. A read found a defect and nothing here has replayed past it: a cited evidence entry’s
   `external_review.state` is `defect-found`, and the result stands below `C2`.
2. The latest review in the result’s `reviews` ends `defect-open` or `refuted`.
3. A cited replay ran and failed (`replay_status: failed`).

Exactly one status holds for each result: the three rung statuses partition the
confirmation ladder, and incomplete overrides them.

### How Status Differs From the Rungs

`V` says what the result’s own source certifies, anywhere.
`C` says how far that has been independently confirmed, rung by rung.
Status is the confirmation ladder read in three words, and it adds the one thing the
ladder cannot say, that a defect is open.

*Confirmed* is exactly `C2` and up.
It earns its place as the word a reader scans for and filters by, and as the one schema
every row shares; it adds no judgment of its own.
`C2` is the threshold because it is where the ladder itself changes kind: `C0` is
recorded, `C1` is read, and from `C2` a replay has passed, which is why the checker
refuses a `C` above `V` from `C2` up.

### Incomplete Today

| Entry | Why |
| --- | --- |
| T-058 | wand125’s $B \cdot \mathit{UB}(n)$ ceiling. The read of 29 September found a missing premise (`E-wand125-tools-ceiling-report`, `defect-found`), and nothing here has replayed past it. `think-xgjo` is open. |
| T-059 | wand125’s equality of 12,028 $n = 11$ row minima. The read of 29 September found journal-admission defects (`E-wand125-tools-n11-row-report`, `defect-found`); three sample rows were replayed and the complete replay is queued (`think-11z6`). Update, 2 October: the complete replay passed, 12,028 of 12,028 rows equal (`E-wand125-tools-n11-row-replay`), and T-059 is at `V3`/`C3`, confirmed and no longer incomplete. |

Five results cite a read that found a defect and are not incomplete: T-004, T-005, T-006
and T-008 cite the defect in Bentz’s Lemma 10, which T-005 corrects, and T-060 cites the
publisher’s stale digest bindings.
Each has a passing replay here past the defect.

**Omissions the record states only in prose.** These do not make an entry incomplete,
because no field holds them.
The owner may want some of them to.

| Omission | Entries | Where it is written |
| --- | --- | --- |
| A review exists and is not recorded as an `external_review`, so the entry derives `C0` and not `C1` | T-046, T-048, T-055 | Each entry’s `next_rung` and `notes`; `think-wcex` is open. Doing it makes all three *reviewed*. |
| The significance score is a draft | 19: T-037 to T-055 | `significance.by: session-161 (repository; draft)` |
| A passed replay is not in the record | T-046, T-048, T-055 | Transfer branches; now each entry’s `activity` |
| The read names unverified items | T-007 | `next_rung`: four named items |

If the owner wants a recorded omission to count, the smallest addition is one optional
list on a result, `omissions`, each item a sentence, a date and a link, with
*incomplete* derived from a non-empty list.
It is not added here: the register has no placeholder entry today, since the schema
requires every field.

### Kind, Status and the Superseded Mark

Three things now sit under a result’s rungs, each answering one question.

|  | Question | Values | Where it comes from |
| --- | --- | --- | --- |
| Kind | What is the result? | lower bound, upper bound, optimality, simplification and six others | Declared in the register, checked against the claim and the evidence |
| Status | How far has the work on it here gone? | recorded, reviewed, confirmed, incomplete; and beside it, who has the next move | Derived from the rungs and the defects on record; the activity is recorded and dated |
| Superseded | Does a case bound still rest on it? | marked, or not | Derived from the case records |

- **Superseded** stays, as its own mark and its own filter, and it is asked only of a
  bound: a result whose kind is lower bound, upper bound or optimality.
  26 results are marked, every one a confirmed lower bound.
  The “Hide superseded” checkbox is unchanged.
  *Current best* is not drawn.
- **A result of another kind is never marked superseded.** This settles T-003: it is the
  limit of a method, it cites the evidence of the bound it measures, and so its standing
  derives as *superseded*, though no later bound supersedes a method’s limit.
  It draws its kind and its status, it is not hidden by “Hide superseded”, and
  `render_recent_results.superseded` is the one rule.
  T-004 and T-005 derive *current best*, which was never drawn, so nothing changes for
  them. **Update, 2026-10-03.** Still true of a standing, which marks only a bound; T-003
  stays unmarked. A result of another kind is now marked where its entry declares a later
  result that implies it (`superseded_by`): *superseded* for the whole, *superseded in
  part* for some, as T-060 is of T-036’s bound (think-xm4t). Every mark also names what
  supersedes it, a bound’s derived from its cases (*superseded by T-060*).
- **Second certificate** is the kind *simplification*, which T-054 and T-055 carry.
  The mark is gone from the tables.
- **Reported** is gone as a word.
  *Current best, reported* is the status *recorded* at `V0/C0`.

The derivation of standing is untouched: `render_recent_results.standing` and
`devtools.check_standing` work as they did, and the chain of results on a case, inside a
result’s overview, still says which result holds the case and which are superseded
there. What changed is what a table of results shows of it: one mark.

The field is named *status* on the site, in `RESULTS.md` and in the filter bar.

## Who Has the Next Move

The owner asked for a way to tell results this project is actively analysing from
results waiting on others to respond or clarify.

No field in the record says either.
`next_rung` is prose and describes what is queued.
Beads, issues and branches hold the facts, outside the register.
So this is the one place a hand-recorded field is needed, and it is built to expire.

```yaml
activity:
  state: in-analysis        # or: waiting
  party: source             # waiting only: source, owner or third-party
  what: >-
    The complete L740 replay passed here on 2026-09-29 …
  since: '2026-09-29'
  link: think-nnlg          # a bead, an issue, a pull request, a branch or a file
```

- **In analysis** means a replay, a review or an audit of the result is under way here.
  Work that is queued and not begun stays in `next_rung`.
- **Waiting** means a question, a request or a missing artifact is with another party,
  and `party` says who.
- `devtools.check_results` requires the fields, a link that is a bead, a GitHub address
  or a file that exists, and a date no later than the register’s `last_reviewed`.
- **It expires.** The checker refuses an activity dated more than 30 days before
  `last_reviewed`. It is then re-dated with what happened since, or removed.
  The check reads the register’s own date and never the clock, so the gate is
  deterministic; the cost is that a register nobody touches cannot flag a stale entry.
  A session-close check against the clock would close that gap, and is not built here.
- The checker cannot see whether a linked bead or issue is closed.
  That needs `tbd` or the network, neither of which the records gate may use.

### Two Shapes, and the Recommendation

|  | A: a mark beside the status (built) | B: statuses of their own |
| --- | --- | --- |
| Vocabulary | recorded, reviewed, confirmed, incomplete; plus a second chip, *in analysis* or *waiting on source* | recorded, in analysis, waiting, reviewed, confirmed, incomplete |
| A result confirmed and waiting on its source | *confirmed*, *waiting on source* | *confirmed*; the wait is not shown |
| A result recorded and in analysis | *recorded*, *in analysis* | *in analysis*; that it has not been read is not shown |
| Counts today | 3 recorded, 4 reviewed, 56 confirmed, 2 incomplete; 3 of them in analysis | 0 recorded, 3 in analysis, 0 waiting, 4 reviewed, 56 confirmed, 2 incomplete |
| What decides it | The rung, and separately the dated activity | The activity where one is recorded, else the rung |

**A is recommended.** The status stays a pure function of the rungs and the defects on
record, so it never needs a hand to keep it true.
Who has the next move is a different question with a different lifetime: it is dated and
expires, and it applies to confirmed results as well.
Under B, three of the six statuses would be hand-recorded and could go stale, and the
status of T-046 would stop saying that it has not been read.

### What the Record Shows Today

Entered in the register on this branch, each from a bead that is in progress and a
transfer branch that holds the receipts:

| Entry | Activity | What | Since | Evidence |
| --- | --- | --- | --- | --- |
| T-046 | in analysis | 21 of 45 certificates replayed in full; receipts unmerged; 24 without a receipt | 2026-09-29 | `think-20mv`, in progress; five transfer branches |
| T-048 | in analysis | Complete replay passed; evidence entry and verified lane not yet written | 2026-09-29 | `think-nnlg`, in progress; its note records the pass |
| T-055 | in analysis | Complete replay passed; comparison and evidence entry not yet written | 2026-09-29 | `think-ifsv`, in progress; the transfer commit |

Plausible from the record and **not entered**, because each is inferred from prose or
blocks nothing. The owner may want some of them.

| Entry | Would be | For what | Since | Evidence, and why it was left out |
| --- | --- | --- | --- | --- |
| T-059 | in analysis | The replay of all 12,028 rows | 2026-09-29 | `think-190a` is in progress and `think-11z6`, the replay itself, is open. Inferred: queued, not shown to have begun. Update, 2 October: the replay ran and passed, so the row is moot. |
| T-058 | in analysis | Discharging the missing premises, or replacing the ceiling | 2026-09-29 | `think-xgjo` is open. Inferred: queued. |
| T-052, T-053 | in analysis | The `zm_mixed.py` re-sweeps | 2026-09-29 | Issue 238 says they “were started here and have not finished”. Inferred from the issue; no receipt or bead says they are running. |
| T-060 | waiting on owner | The oversight record that rung 4 needs | 2026-09-30 | Its `notes`. Left out: all 54 results at `C3` wait on the same record, which is what “review record pending” in the rung’s name already says. |
| T-061 | waiting on source | A revised Zenodo release | 2026-09-30 | Issue 247, this project’s last comment. A recorded request; left out because nothing here depends on it. |
| T-057 | waiting on source | The boxes or checker of the source’s own interval run | 2026-09-29 | `replay_status: public-certificate-missing` on its report evidence. Inferred: no request is on record, and the result no longer depends on it. |
| T-056 | waiting on source | Coordinates at higher precision for $n = 206, 259, 305$ | 2026-09-29 | Its `next_rung`. Inferred: issue 227 states the finding and asks for nothing. |

Nothing registered is waiting on its source with a recorded request that blocks work
here. Two issue threads have the next move on this side: issue 238, where Evan Daniel
answered this project’s three questions on 1 October, and issue 256, his registration
request for $s(60) = 8$, which pull request 267 answers.

## Every Result

The table is `python -m devtools.result_status --list` with notes added.
“Mark” is *superseded*, drawn on a bound that no case bound rests on now.

| id | kind | standing until now | status | decided by | mark | activity | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-002 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-003 | method limit | superseded | confirmed | `C3` |  |  | Its evidence gives it the standing *superseded*; it is a method’s limit, so it is not marked. |
| T-004 | audit | current best | confirmed | `C3` |  |  |  |
| T-005 | correction | current best | confirmed | `C3` |  |  |  |
| T-006 | optimality | current best | confirmed | `C3` |  |  |  |
| T-007 | lower bound | current best | reviewed | `C1` |  |  | The read names four unverified items; `C3` needs Theorem 1 machine-checked. |
| T-008 | optimality | current best | confirmed | `C3` |  |  |  |
| T-009 | upper bound | current best | confirmed | `C3` |  |  |  |
| T-010 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-011 | upper bound | current best | confirmed | `C3` |  |  |  |
| T-012 | rigidity | none | confirmed | `C3` |  |  |  |
| T-013 | rigidity | none | confirmed | `C3` |  |  |  |
| T-014 | rigidity | none | confirmed | `C3` |  |  |  |
| T-015 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-016 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-017 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-018 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-019 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-020 | lower bound | current best | confirmed | `C3` |  |  |  |
| T-021 | lower bound | current best | confirmed | `C3` |  |  |  |
| T-022 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-023 | case exclusion | none | confirmed | `C3` |  |  |  |
| T-024 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-025 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-026 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-027 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-028 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-029 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-030 | lower bound | current best | confirmed | `C3` |  |  |  |
| T-031 | case exclusion | none | confirmed | `C3` |  |  |  |
| T-032 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-033 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-034 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-035 | case exclusion | none | confirmed | `C3` |  |  |  |
| T-036 | restricted optimality | none | confirmed | `C2` |  |  | `C2`: replayed without a machine certificate; `C3` waits on a replay mode for the isolation radius. |
| T-037 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-038 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-039 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-040 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-041 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-042 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-043 | lower bound | current best | confirmed | `C3` |  |  |  |
| T-044 | lower bound | current best | confirmed | `C3` |  |  |  |
| T-045 | lower bound | current best | confirmed | `C3` |  |  |  |
| T-046 | lower bound | current best, reported | recorded | `C0` |  | in analysis | 47 cases of the old block. 21 of its 45 unreplayed certificates passed a full replay on 2026-09-29; the receipts are on transfer branches, not in the record. |
| T-047 | lower bound | current best | confirmed | `C3` |  |  |  |
| T-048 | lower bound | current best, reported | recorded | `C0` |  | in analysis | $n = 50$ of the old block. The complete replay passed on 2026-09-29; the receipts are on a transfer branch, not in the record. |
| T-049 | lower bound | current best | confirmed | `C3` |  |  |  |
| T-050 | lower bound | superseded | confirmed | `C3` | superseded |  |  |
| T-051 | optimality | current best | confirmed | `C3` |  |  |  |
| T-052 | optimality | current best | confirmed | `C3` |  |  | A second, `zm_mixed.py` re-sweep was started here (issue 238) and is not in the record. |
| T-053 | optimality | current best | confirmed | `C3` |  |  | A second, `zm_mixed.py` re-sweep was started here (issue 238) and is not in the record. |
| T-054 | simplification | second certificate | confirmed | `C3` |  |  |  |
| T-055 | simplification | second certificate, reported | recorded | `C0` |  | in analysis | The complete replay passed on 2026-09-29; the receipts are on a transfer branch, not in the record. |
| T-056 | upper bound | current best | confirmed | `C3` |  |  | At $n = 206, 259, 305$ the printed side needs coordinates at higher precision from the source. |
| T-057 | upper bound | current best | confirmed | `C3` |  |  | The source’s own interval run cannot be replayed until it publishes its boxes; the result no longer depends on it. |
| T-058 | method limit | none | incomplete | `C1`, and a read that found a defect |  |  | The read found a missing premise in the source’s ceiling; `think-xgjo` is open. |
| T-059 | audit | none | incomplete | `C1`, and a read that found a defect |  |  | The read found journal-admission defects; the replay of all 12,028 rows is queued (`think-11z6`). Update, 2 October: it passed, and T-059 is `V3`/`C3`, confirmed. |
| T-060 | optimality | current best | confirmed | `C3` |  |  | Rung 4 waits on the owner’s oversight record and a second adversarial review. |
| T-061 | lower bound | superseded | confirmed | `C3` | superseded |  | A revised Zenodo release was asked for on issue 247; nothing here depends on it. |
| T-062 | optimality | current best, reported | reviewed | `C1` |  |  |  |
| T-063 | optimality | current best, reported | reviewed | `C1` |  |  |  |
| T-064 | optimality | current best, reported | reviewed | `C1` |  |  |  |
| T-065 | upper bound | current best | confirmed | `C3` |  |  |  |

Counts, of 65: 56 confirmed, 4 reviewed, 3 recorded, 2 incomplete; 26 marked superseded,
all of them confirmed lower bounds.
Every result of this project is confirmed: its certificate is replayed from the
repository before it is registered.

## Reports That Are Not Register Entries

The owner asked that results not fully assessed be in the register and the table, with a
tag, so the table reflects the state of the work.
The count of such results is small, and the tag exists: it is the status.

**In the register and not confirmed: 9 of 65.** T-046, T-048, T-055 recorded; T-007,
T-062, T-063, T-064 reviewed; T-058, T-059 incomplete.
Five are wand125’s, taken in on 29 September, and three are Evan Daniel’s claims of
$s(60) = 8$, $s(61) = 8$ and $s(k^2 - 3) = k$, registered on 1 October by pull request
267 with a read on file.
T-064 is `S4`, so it is the one unconfirmed result the homepage shows where its filters
start.

**Acted on by the record and not in the register:**

| What | Count | Source | Why it has no entry | What a registration needs |
| --- | ---: | --- | --- | --- |
| Catalogue sides newer than the record | 3: $n = 69, 83, 87$ | David Ellsworth; Allen Chang with Ellsworth; Chang, all September 2026, as the Kingbird catalogue’s capture of 30 September prints them | `source-coverage.yaml` lists them under `pending_catalogue_intake`: “the register holds it before the record takes it” | A bibliography key for each with `dated`, `credit` and `lineage`. The catalogue gives a month, and `attribution.published` takes a day or a year; and the three witnesses have to be taken in. |

**Reported in a case record and outside the register’s scope:**

| What | Cases | Source |
| --- | ---: | --- |
| Reported lower bounds above the verified one | 39, from $n = 65$ to $294$ | Green’s Theorem 9 as Friedman’s survey reports it, a private communication never recovered |
| Reported upper bounds below the verified one | 78 | The catalogue’s best known packings, 77 from Kingbird and 1 from the UnitSquare release, where the verified bound is the grid |
| Superseded reports | 44 | 39 of Griffin Casson’s packings and 5 of UnitSquare’s, each beaten by a certified packing of Francisco Couzo’s |

`epistemics.md` keeps these out on purpose: older results enter the register when they
hold a verified field or are machine audits, and a report below the standing bound that
asks for no work stays in its case record.
The frontier atlas shows every one in its reported lane.

One more gap follows from the same rule and is not closed here.
Fifteen evidence entries hold a verified field, at 25 case fields between them, and are
cited by no register entry: the trivial lower bounds at $n = 1, 2, 3$; the published
proofs at $n = 5, 6, 10, 22, 33$; and the replayed packings of Göbel’s and others at
$n = 5, 10, 18, 19, 26, 27, 38, 40, 52, 65, 66, 67, 82, 84, 85, 86, 89$. All predate the
project. A sixteenth, the upper bound at $n = 17$, was this project’s own and is now
registered.

## The Upper Bound at Seventeen Squares

The case record of $n = 17$ carried a verified upper bound that no register entry
stated: $s(17) \le 4.6755300936045509516342148538535054$, certified on 1 October
(`E-n017-certified-endpoint`). It is registered on this branch as **T-065**, the next
identifier after the three that pull request 267 took.

The rungs are derived: `V3/C3` from its two evidence entries, both exact with a
certificate and a passing replay.
Its kind is *upper bound*, its status *confirmed*, and it is the current best.
`check_results` and `check_standing` pass, the atlas’s citation for the case now reads
“Bidwell 1998, Squares in Squares (confirmed T-065)”, and the shared README and homepage
paragraph says that both ends of the bracket at seventeen squares are machine-checked.

Two things in the entry are judgments, entered as drafts for the owner to confirm.

1. **Whose result it is.** The evidence entry says its novelty is not assessed and that
   no new packing is claimed.
   The packing is John Bidwell’s of 1998, as the atlas credits it.
   Kleddamag’s release of 21 September carries that construction forward as an exact
   rational witness at $4675530093604551/10^{15}$, replayed here.
   This project derived the certified endpoint from that witness, which lowers the
   ceiling in the seventeenth decimal.
   The entry follows T-044 and T-045, where a bound derived here from a source’s files
   is part of the source’s result: it is a result by others, credited to Kleddamag’s
   release, with Bidwell and this project’s part named in the claim.
   The other reading follows T-011, Bidwell’s bound verified here, and needs a
   bibliography key for Bidwell’s packing, which does not exist.
2. **Its significance.** `S3`, the level of T-009 and T-057, the register’s other first
   verified upper bounds, scored as a draft.

## What Is Built on the Branch

| Area | Change |
| --- | --- |
| Derivation | `devtools/result_status.py`: `status`, `open_issues`, `status_line`, the activity checks, and `--list`. |
| Schema | `results.schema.yaml`: the optional `activity` object. No stored status. |
| Checker | `check_results` holds each `activity` to its fields, link and age, and prints the count by status. `check_standing` is unchanged; it is what holds the superseded mark to the numbers. `render_recent_results.superseded` says which results are marked. |
| Register | `activity` on T-046, T-048 and T-055; T-065, the upper bound at $n = 17$. No rung of an existing entry changed. |
| Generated views | `RESULTS.md`: a `status` column in both tables, after `kind`, `credit` and the rungs, in place of `standing`. |
| Site | Under the rungs of every row, the kind on its line and then the status line: the status chip, the activity and the superseded mark, each a chip on a line of its own, so the Rungs column is no wider than it was. A Status select in place of Standing, after Kind; “Hide superseded” unchanged; the block, its popovers, its styles and `.site-group-row` removed; a sentence above the homepage table that counts the results not yet confirmed and links each count to those rows. |
| Definitions | `epistemics.md`, Status; the frontier README’s procedure; `paper-design.md`. |

**What each page shows where its filters start.**

| Page | Rows | Of them not confirmed |
| --- | ---: | --- |
| Homepage, at `S4` and up, 180 days, superseded hidden | 7 of 65 | 1 reviewed (T-064) |
| Results page, every result | 65 | 3 recorded, 4 reviewed, 2 incomplete |

The homepage’s defaults are unchanged.
At `S3` and up it would show 26 rows, T-046, T-048 and T-062 among them; at every
significance, 34, with T-055, T-058, T-059 and T-063.

## Decisions for the Owner

1. **The vocabulary.** Recorded, reviewed, confirmed, incomplete, as proposed.
   Recommended as built.
2. **Where *confirmed* begins.** `C2`, where a replay has passed, or `C3`, where a
   machine certificate replays.
   It moves one result, T-036. Recommended: `C2`.
3. **Whether to draw *confirmed*.** It is on 56 of 65 rows.
   Drawing it gives every row the same schema; leaving it undrawn, as *current best* is,
   would mark only the nine that are not.
   Recommended: draw it, and revisit if the column reads as noise.
4. **The activity mark.** Shape A, a mark beside the status, or shape B, statuses of
   their own. Recommended: A, as built.
5. **Which activities to record.** Three are entered.
   Seven more are listed above with the reason each was left out.
6. **Superseded is asked only of a bound.** It leaves T-003, a method limit, unmarked
   and showing under “Hide superseded”.
   Recommended as built; the alternative is to mark any result whose evidence derives
   the standing, as before.
   **Update, 2026-10-03.** Kept for the derived mark; the owner added a declared one for
   other kinds (`superseded_by`, think-xm4t), which leaves T-003 unmarked.
7. **Whether a recorded omission makes a result incomplete.** It would need the
   `omissions` list. Recommended: not until the register admits placeholder entries.
8. **The homepage default.** An unassessed result shows on the homepage only if it is
   `S4` or above; today that is one, T-064. Every one shows on the results page.
   Recommended: keep it.
9. **T-065, the $n = 17$ upper bound.** Its credit and its significance, as set out
   above. Recommended as registered: credited to Kleddamag with Bidwell and this
   project’s part named in the claim, at `S3`.

## Follow-Up Work, Not Done Here

- **Integrate the replays.** Merge the receipts of the six transfer branches into their
  packets, write the evidence entries, move the verified lanes of $n = 50$ and the 21
  rectangle cases, and re-run the 24 certificates that have no receipt (`think-20mv`,
  `think-nnlg`, `think-ifsv`, `think-0rrj`). This is the change that makes most of the
  old block’s rows *confirmed*.
- **Record the reviews that exist** as `external_review` on the three report entries
  (`think-wcex`), which makes T-046, T-048 and T-055 *reviewed* until then.
- **Register the three catalogue intakes**, at $n = 69, 83, 87$.

## References

- [`epistemics.md`](../../../../epistemics.md), Status and Results by Others
- [`packing/devtools/result_status.py`](../../../../packing/devtools/result_status.py)
- [`packing/devtools/render_recent_results.py`](../../../../packing/devtools/render_recent_results.py),
  where standing is derived
- [The overview plan](plan-2026-09-29-github-pages-overview.md)
- [The plan for results by others](plan-2026-09-29-third-party-results-register.md)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
