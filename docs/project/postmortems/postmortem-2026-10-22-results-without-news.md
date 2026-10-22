# Postmortem: Results That Landed Without News

**Date:** 2026-10-22

**Author:** Claude (agent, lane `c-rootcause-announce-1022`), for the project owner

**Status:** Complete.
The fixes are open under epic `think-s38d`.

**Scope:** T-194, Fitzharding’s Lean proof that Wainwright’s packing of 19 squares is
optimal, scored S5, which landed on 16 October 2026 in PR #651 with no News article; the
25 other S3+ results that landed on 16 to 21 October without one; the 15 S4/S5 results
from before the News archive existed; and the process that let a result reach the
register, the case page and the results table while News showed nothing new for a week.
Every count is taken at `main` `e44a51f44` unless another revision is named.

## What happened

News was built on 13 to 16 October, and announcing results on it was never made anyone’s
job.

The News record, [`site-changelog.yaml`](../../../packing/site-changelog.yaml), was
designed so that an article cites a merged pull request and takes its date from that
merge. The article therefore cannot be written in the pull request that registers the
result. The runbook accepts this: draft the article’s text in the pull request’s
description before merge, then “complete the prepared News/changelog disposition in the
next change”. No bead, no step of the intake pass and no tool owns that next change, and
no check compares News with the register.

For three days the News feature’s own build-out covered the gap.
Its pull requests (on `codex/*` branches) backfilled the S3+ intake results inside their
windows, so T-153 and T-154 have articles.
The build-out’s last result article merged at 03:20Z on 16 October (#638). T-194 merged
at 17:49Z the same day.

PR #651 did everything the checklist asked.
It carried the `S5` label, a News line (“draft entry before merge … dated by the
merge”), an **Announcement** block for the owner’s X post, and a ticked box saying it
had its News disposition.
Three later pull requests touched T-194 (#655, #658, #690), and each said its News
belonged elsewhere. Nobody wrote the article.

The 13 S3+ pull requests merged after #651 went the same way.
Each described an article, most of them “for post-merge authoring”.
Three articles were written, by later pull requests that took them on by name: #700 for
#687, and #716, on the coordinator’s word, for #704 and #706.

## Timeline

All times are UTC.

| When | Event |
| --- | --- |
| 11 Oct | The owner asks for a short announcement, one line per result, “for the owner to announce from”. `render_announcement` is built, and the intake pass gains step 6, “Render the announcement … for the owner to post; an agent never posts it” (`01021d703`) |
| 13 Oct 17:07, 22:04 | #560 (T-153, S5) and #588 (T-154, S5) merge. News does not exist yet, and neither description mentions it |
| 14 Oct 10:46–10:47 | Two separate work streams merge 44 seconds apart: #563, the intake stream’s announcement renderer, and #590, the News stream’s `site-changelog.yaml`. #590 backfills the 36 PRs #479 to #588, so T-153 and T-154 get articles |
| 14 Oct 20:54 | #604 publishes the News articles. At the owner’s request (`think-rpda`) the home page box shows the three newest S5 articles, and the archive defaults to S4/S5 |
| 14 Oct 23:39 | #608, an intake records PR, writes articles for #602 and #605, because its bead (`think-3aum`) names them |
| 15 Oct 18:30 | #621 audits 94 PRs, adds the S labels, the PR template’s News checkbox and the runbook’s [Label the PR and Prepare News](../../../packing/campaign/result-import.md#label-the-pr-and-prepare-news): draft before merge, write the YAML entry “in the next change” |
| 16 Oct 02:16, 03:20 | #633 writes the T-191 and T-192 articles. #638 backfills T-060 (30 September) as the home box’s third S5 article, because “only two canonical S5 articles existed”. These are the build-out’s last result articles |
| 16 Oct 03:27 | Fitzharding announces sq19 on X, and issue #640 asks for it to be registered |
| 16 Oct 05:00–14:30 | The overnight intake coordinator prepares #642, #651, #655 and #658. Its handoff gives the steps after each merge: retarget, re-cut the site edition, re-pin, wait for CI. News is not among them (`think-hg5s`) |
| 16 Oct 17:49 | **#651 merges, and T-194 lands.** No article follows |
| 16 Oct 19:28 | #655, the review of the proof, merges: “the News item, if any, belongs to the result’s own entry, so this PR has none” |
| 17 Oct 01:42 | #657 raises T-189 from S2 to S3: “a short entry … may be drafted at merge” |
| 19 Oct | #676 and #671 merge with articles drafted “for post-merge authoring”. #658 (T-194 to C1) merges: “News: none beyond the site edition’s entry”. The stage 7 reply on #640 is posted |
| 20 Oct | #688, #692, #687 and #699 merge, each with an article drafted. At 21:05 #700 writes #687’s T-220 article, the first result article since #638 |
| 21 Oct | #708 (T-224), #704 (T-196) and #706 (T-223) merge |
| 22 Oct 00:31 | #716 writes the T-196 and T-223 articles “on the coordinator’s word” (`think-ql4v`) |
| 22 Oct 20:33 | The owner calls it “a serious failure in the process”. Epic `think-s38d` opens |

## Impact

**What a visitor did not see.**

- **News has no article for T-194.** On the live site (v0.9.2, fetched on 22 October),
  `news.html` never mentions T-194 or 19 squares.
  The archive opens filtered to S4/S5, and the newest article in that view was dated 14
  October, eight days old.
- **The home page’s News box did not change after 16 October.** It shows Fitzharding’s
  proof for 17 squares (13 October), Overbeck’s candidate proof for 17 squares (13
  October) and Ahmed’s proof for 11 squares (30 September).
- **`CHANGELOG.md` on GitHub**, generated from the same YAML, leaves it out too.
- **Of the 31 S3+ results that landed from 16 October, 5 have an article**: T-191,
  T-192, T-196, T-220 and T-223. Each of the other 26 is a new or confirmed bound,
  adopted packing or proof by someone outside the project, and none was credited in
  News.

**What a visitor did see.** T-194 was published as a result: it was a row scored S5 in
the home page’s results table, which reads the register directly, an entry at
`results.html#t-194`, and a link on the case page for 19 squares.
Fitzharding was answered on #640 on 19 October.
So the record was right, and its announcement on the site was missing.

**What is not known.** Whether the owner posted #651’s Announcement block on X is not
recorded in the repository.
Fitzharding announced the proof himself.

## Root cause

**A result’s News article cannot be written in the pull request that registers the
result, and the step that writes it afterwards has no owner and no check.**

1. **The article has to come after the merge.** `render_changelog.validate` refuses an
   entry whose pull request has “no retained merged main delivery”, and requires the
   entry’s date to be that merge’s date
   ([`render_changelog.py`](../../../packing/devtools/render_changelog.py), the delivery
   loop in `validate`).
   [`import_changelog`](../../../packing/devtools/import_changelog.py) builds the
   delivery from the merged PR’s metadata and checks that `main` contains it.
   The plan behind News says the same: “a subsequent changelog-update PR or
   documentation batch can publish those entries”
   ([plan](../specs/active/plan-2026-10-13-site-changelog.md), Ongoing authoring).
2. **The runbook defers it to “the next change”.** Stage 5 says to draft the article
   before merge (line 1014 of `result-import.md` at `e44a51f44`), then lists after the
   merge: “Complete the prepared News/changelog disposition in the next change” (line
   1106).
3. **Nobody owns the next change.** Steps 1 to 8 of
   [Running an Intake Pass](../../../packing/campaign/result-import.md#running-an-intake-pass)
   (lines 25 to 98), which a pass follows, never mention News.
   The pass “is done when … every count it re-housed is regularized … and every reply it
   owes is posted and recorded” (lines 95 to 98), with no word about News.
   No bead is opened for an article.
   `make intake` lists `#N owes a reply` until a reply is recorded, and lists nothing
   for an article that is owed.
4. **No check compares News with the register.** The changelog’s coverage check compares
   coverage with the deliveries someone already imported, so a PR nobody imported is
   invisible to it: the 70 PRs merged after #627 through `e44a51f44` include 4 retained
   deliveries, and the check passes.
   `check_published_site` compares `news.html` with the YAML, and `news_highlights`
   filters the YAML. Each check confirms that a view agrees with its own source, and no
   check reads `results.yaml`.

From 13 to 16 October this did not show, because the News build-out did the work.
Of the 22 result articles at `e44a51f44`, 18 were written by its PRs (#590, #604, #617,
#621, #633, #638), and 4 by intake PRs (#608, #700, and two in #716).

## Contributing factors

**Two things are called the announcement.** Step 6 of the intake pass renders the
owner’s X post into the PR under **Announcement**, and the runbook says three times that
an agent never posts it.
The News article is a separate record, which nothing assigns to the owner.
The two came from separate streams, merged 44 seconds apart on 14 October (#563 and
#590), and the intake pass took in only the first.
Lanes wrote the X block, which has a step, and drafted the article, which has none.
#671 holds a “draft for the owner to post after merge” beside a News draft “after
merge”: both wait for the merge, and only the first names who acts on it.

**The checkbox is ticked by the author.** Of the 14 S3+ PRs merged from #651 on, 9
ticked “PR has … its News/changelog disposition”; 6 of those 9 never got an article
(#651, #644, #657, #645, #688 and #692). Every one of the 14 described an article, and 3
got one.

**A step that a tool lists gets done, and a step that no tool lists does not.**
`check_release_impact` refuses a PR without a reviewed release disposition, and all 17
PRs from #651 to #718 that registered, reviewed, confirmed or announced a result changed
`release.py`. Three changed `site-changelog.yaml`. The sweep lists replies that are
owed, and T-194’s reply was posted.
The one article written from its own PR’s deferral, T-220, is the one whose “Selected
next entry” put the article beside the tracked reply: “the stage 7 reply on #680,
recorded in the next records change, and the News entry through `import_changelog`”. Of
the eleven result PRs from #651 to #708, #687 is the only one whose next entry names an
article.

**The release ceremony took the place of a record of what changed.** #658 disposed of
News as “none beyond the site edition’s entry”, and the site’s edition history does
record “the site cut v0.7.15 for T-193 and T-194”. That history is internal bookkeeping
and is not News. The handoff of 16 October lists the re-cut and the re-pin after each
merge, and leaves News out.
`think-wdqo` records that site editions took 85 of 210 commits across 11 PRs before the
owner dropped them on 22 October.

**Handoffs and parallel lanes split T-194 four ways.** #651 was prepared by the
overnight coordinator, whose handoff says “nothing is merged”.
#655 deferred News to “the result’s own entry”, #658 to the site edition, and #690 said
“News: none”.
Each PR disposed of its own News correctly and assumed someone else had the
result’s.

**Deferring News until a result is confirmed can defer it indefinitely.** #701 omitted
T-223’s article as “an intermediate registration; it belongs to the stage 4 PR that
confirms and adopts”, which the runbook allows for “an intermediate research
checkpoint”. T-194 is reported at V0/C1, and its confirmation waits on a full build of
190 to 380 CPU-hours that the owner holds.
#651 did intend to announce it as reported, as T-153 and T-154 had been, so this factor
did not cause T-194’s miss.
It is a hazard for the gate.

**Raising a result’s score does not prompt an article.** T-189 was S2 when #627
registered it, so #633 correctly left it out.
#657 raised it to S3, and said only that an article “may be drafted”.

**The pages that would have shown the gap did not show it.** The home box shows S5
articles only, and from 16 to 22 October the record held exactly three.
So the box looked the same whether or not an S5 result had landed.
The archive’s default S4/S5 view hides every S3 article, so the 25 missing S3 articles
would not have shown by default either.
T-194 itself did appear on the home page, in the results table, so a deployed-site check
for the result found it published.

**S labels are missing too.** 9 of the 70 PRs merged after #627 carry no S label, among
them #701, which registered T-223. The importer reads the score from that label.

## Why T-153 and T-154 have articles and T-194 does not

|  | #560 (T-153) and #588 (T-154) | #651 (T-194) |
| --- | --- | --- |
| Merged | 13 October | 16 October |
| S label | none at merge; `S5` applied on 15 October by #621’s audit | `S5` |
| News line in the description | none: the template had no News item yet | “draft entry before merge … dated by the merge” |
| Announcement block | none | yes, for the owner to post |
| News checkbox | not in the template yet | ticked |
| Article | written by #590, the News build-out’s first backfill | none |

The PRs that did no News paperwork got articles, and the PR that did all of it got none.
What decided it was the merge date: #560 and #588 fell inside the window #590
backfilled, and #651 merged 14.5 hours after the build-out’s last result article.

## The S3 batches

| Results | PRs | What the PR said | Article | Why |
| --- | --- | --- | --- | --- |
| T-189 | #627 registered it at S2; #657 raised it to S3 | “may be drafted at merge” | none | No step |
| T-197, T-218, T-219 | #676, #692 | “News draft for post-merge authoring” | none | No step |
| T-200 to T-217 | #671; #688 confirmed T-205 to T-207 | “News draft after merge”; “in the next records change” | none | No step |
| T-220 | #687 | an article “is warranted after merge”, named as the next entry beside the reply | #700 | The lane named it; #700 “brings in the News entry #687 deferred to it” |
| T-221, T-222 | #699 | “News draft for post-merge authoring” | none | No step |
| T-196 | #676, #704 | “News draft for post-merge authoring” | #716 | The coordinator’s word |
| T-223 | #701, #706 | omitted at registration; “one entry … after the deployed-site check” | #716 | The coordinator’s word |
| T-224 | #708 | “News: one entry” | none | No step |

No lane decided to leave an article out, and no owner decision to omit one is on record.
Every PR planned an article, and the three that were written were the ones a later PR
took on by name. The S3 PRs that are not results, #644, #645 and #578, also drafted
articles that were never written.

## The September results

News began with #590, merged on 14 October (`site-changelog.yaml` was first committed in
`6279bd0e6`, on 13 October local time).
Its backfill covered #479 to #588 (10 to 13 October), and #621 extended it to the week
from 8 October. T-060 (30 September) was added by #638 to fill the home box.
So the 13 S4/S5 results of 1 to 29 September were never inside any backfill window.
That was a scoping decision, not a step someone missed.
T-064 and T-081 (1 and 3 October) appear only in an S2 attribution entry, which is not
News, so 15 S4/S5 results predate News without an article.
`think-gq0l` asks the owner whether to backfill them under their original dates.

## What is being fixed

| Bead | Change | Guards against |
| --- | --- | --- |
| `think-9wxc` | A records-tier and CI gate: every registered S4 or S5 result has a News article that News shows, at its own score. The result’s own PR drafts the article, and a named stage 7 step lands it right after the verified deploy; until it does, the gate fails the next change to the register or News, and warns on any other. T-194 gets its article | An S4/S5 result landing unannounced; an article left to “the next change” |
| `think-gq0l` | The owner decides whether the 15 S4/S5 results from before News get articles dated to their merges; until then the gate exempts them | A gap the archive inherited when it was created |
| `think-aqv8` | A discreet significance filter at the top right of the home box, S5 by default when there are enough S5 articles, otherwise S4+S5 | A box that stays the same for a week without anyone noticing |
| `think-2252` | An audit of the 26 S3+ results without articles; S3 articles stay optional, by the owner’s decision | The S3 backlog this incident left |
| `think-jlra` | This postmortem |  |

## What else should change

1. **The gate should count articles News shows.** It should require an entry scored 3 or
   more, without `news_exclusion`, that lists the result.
   Presence in `result_ids` is not enough: T-064 and T-081 sit in an S2 entry that News
   never shows. **Done in #735**: the gate reads the entries News renders, at the
   result’s own score.
2. **The gate needs the ordering problem solved, not only described.** While the
   validator requires a merged delivery, a PR cannot carry its own article.
   A gate on that rule alone would turn `main` red at the next merge after every S4/S5
   merge, and the next PR, whatever it is, would inherit the duty.
   #735 handles it narrowly: an article owed on `main` fails only a change that edits
   `results.yaml` or `site-changelog.yaml`, the change that can settle it, and every
   other change, `main`’s pushes and scheduled runs included, gets a warning and passes.
   The real fix is still open as `think-n51k`: let a branch’s article name its own PR as
   pending, accepted only for that PR, with its date set at merge by the same stamp that
   sets `landed` in `devtools.stamp_landed`, and its delivery row added by the importer
   afterwards.
3. **Run the gate when a score rises, not only at registration.** T-189 rose from S2 to
   S3 and nothing asked for an article.
   **Done in #735** for S4 and S5: a raise is owed exactly as a registration is.
   S3 stays optional (item 4).
4. **Make S3 a decision.** Give each S3 result an article or a recorded omission with
   its reason, as each PR has a coverage omission now, and have the sweep list
   `T-NNN owes News or an omission`, as it lists replies.
5. **Rename the PR’s Announcement section to say what it is, the owner’s X post**, and
   generate the PR’s News line from the YAML diff rather than typing it.
   Replace the ticked box with a check that fails.
6. **Have `check_published_site` check the deployed `news.html` against the register,
   not only against the YAML.**
7. **Fix the coverage claim or stop making it.** The audit is complete only over
   imported deliveries, 4 of 70. The sweep could list merged PRs with no delivery or
   omission, and the 9 with no S label, as a report rather than a gate.
8. **Put News in the after-merge list coordinators hand off.** With site editions gone
   (`think-wdqo`), that list is: the News article, the replies, and the deployed-site
   check.
9. **Turn the measurement into a tool (OR-1).** These counts came from a one-off script
   over `results.yaml` and `site-changelog.yaml`. `think-9wxc`’s gate, or a report mode
   of it, should print them.
   **Done in #735** for S4 and S5: every run of the gate prints the registered, exempt,
   owed and failing counts.

## The rules this yields

**R1. A record the change requires is written in the change, or a tool lists it as owed
until it is.** “In the next change” with nothing to list it is how this was lost.
It is R3 of the
[5 October postmortem](postmortem-2026-10-05-orphaned-catalogue-intake.md) (“a wait
names what it waits on, and something reads it”), which was applied to replies and
pending intakes and not to News.

**R2. Check a view against the source of truth, not against itself.** News was checked
against its own YAML and coverage against its own deliveries.
Neither was checked against the register or against `main`.

**R3. A box the author ticks is a reminder, not a control.** A check that fails is the
control. The ceremony that had one was done every time, and the step that had a checkbox
was missed.

**R4. A new surface comes with an owner who keeps it current.** News was fed by the work
that built it. When that work ended, no person and no step took it over.

## Evidence

**Proved**, read from the code or from quoted primary records at `e44a51f44`: `validate`
requires a merged delivery and its date; the runbook’s draft-then-next-change wording
and the absence of News from the intake pass’s steps and done criteria; the coverage
check’s closed set; the home box’s S5 filter (`news_highlights.py`) and the archive’s
S4/S5 default (`render_changelog.py`, `aria-pressed` for scores of 4 and above); every
PR quotation above; `think-ql4v`’s “on the coordinator’s word”; T-189’s scores at #627
and at `e44a51f44`.

**Measured** at `e44a51f44`, or on GitHub on 22 October: 21 S4/S5 results, 16 with no
article News shows; 31 S3+ results landed from 16 October, 5 with articles; 22 result
articles, 18 written by the News build-out; 70 PRs merged after #627, 4 retained as
deliveries and 9 without an S label; 14 S3+ PRs from #651 on, with 9 boxes ticked and 3
articles written; `release.py` changed in 17 of 17 result PRs and `site-changelog.yaml`
in 3; the live `news.html` without T-194, and the live home box’s three headings.
`think-wdqo`’s 85 of 210 commits is the coordinator’s measurement, not repeated here.

**Inferred**: that lanes did the X block because it had a step and left the article
because it had none; that T-220’s article was written because #687 named it beside a
tracked reply; that the release ceremony displaced News rather than merely sitting
beside it; that the box’s unchanging state hid the gap from the owner and the agents.
Each fits the evidence, and none is established by it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
