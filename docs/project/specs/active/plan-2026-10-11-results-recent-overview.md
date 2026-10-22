# Feature: Recent Results on the Results Page

**Date:** 2026-10-11, revised 2026-10-12, 2026-10-14 (three times) and 2026-10-20

**Author:** Claude, lane W of the 2026-10-11 intake pass, bead `think-2z22`

**Status:** Ready for review in pull request #514; the owner’s presentation choices are
answered below

## Overview

The owner asked on 2026-10-11 “whether we could do a rollup of results by day or week on
the results page for S3+ values”, and then: “It shouldn’t replace the table, but it
would be nice to have a brief overview with credits/links to those who have new
results.” On 2026-10-12 they added: “I’d like to be able to easily see which items have
been imported in the last day.”

`results.html` (which `all-results.html` forwards to) now opens, under its hero and
above everything else, on two sections generated from `packing/frontier/results.yaml` at
render time. Nothing in either is typed into the template.

- **Added in the Last Seven Days** (`overview_sections.recent_added`): every result that
  reached the site over the newest day one did and the seven before it, one native
  disclosure a day, newest first, at every significance.
  Each entry gives its id (a link to its row), its headline, its cases, its V and C
  rungs and S score, and its credit.
  The two newest days start open.
- **Earlier Results by Week Published** (`overview_sections.recent_rollup`): the weekly
  rollup of S3 and above, one line per finder, for the four calendar weeks before those
  days. Every week starts closed.

The table, its rows and their addresses are unchanged.
Its filter bar gains one filter on the day a result reached the site, **Added**
(`results.html?added-age=1`, `?added=2026-10-12` for one day, and
`?added-since=2026-10-07` from one day on).

## Decisions

### Two questions, two dates

Each section uses the date that answers its question.

- **What came in** uses `landed`, the UTC day the entry first reached `main`, and with
  it the site. That is the owner’s “imported in the last day”: the day a reader could
  first see the result here.
  It is not `registered`, the day a lane wrote the entry, which runs ahead of arrival
  while its pull request waits to merge.
  On the register of 14 October, 67 of 160 entries reached `main` the day they were
  registered, 69 a day later and 24 two days later (#514’s review A, finding A1, which
  first measured this).
  Grouped by registration, the page read on 14 October missed T-153 and T-155 from the
  last day, though both had landed within 19 hours.
- **Whose results are new** uses the date the row shows (`Result.dated`): the
  `attribution.published` date of a result by others, and the `established` date of this
  project’s own. This is the claim’s own date, the one the record chose for credit, and
  it is what the table’s Date column and its Max age filter use.
  The weekly rollup’s heading says “by Week Published”.

`landed` is recorded, not derived: no page and no gate reads Git (OR-18; #514’s review
B, finding B3). The schema requires it on every entry, and a lane writes it with each
new entry, as the day it registers it.
The merge step re-dates a records pull request’s new entries, those `origin/main` lacks,
to the day of the stamp (`devtools.stamp_landed --apply`, with its re-pin, as the last
commits before the merge; Stage 5 of
[result-import.md](../../../../packing/campaign/result-import.md)). That is the merge
day when the stamp is the last step before the merge, and running it again after a
re-merge or a slip past midnight UTC re-dates them again (review B, finding B2). A
forgotten re-date leaves those entries a day or two early, the lag A1 measured, and
turns nothing red. The entries on `main` before the field existed were dated once from
its first-parent history (`--backfill`), each by the first commit whose register holds
it, which for a merged pull request is the merge.
`--audit` compares every entry on `main` with that history after a merge and gates
nothing; its corrections ride the next records pull request.

A result published before the seven days and arriving in them appears in both sections
if it is at S3 or above, under the day it arrived and the week it was published.
On the register at the merge with `main` (`37e6757ed`) no result is placed so; on 12
October the same rule put T-090, T-091 and T-092 in both sections.
No row shows a day after its registration, and none was registered after it landed (the
tests hold the register to both), so a result at the floor shown on any day from the
rollup’s first Monday on is in at least one of the two sections.

### The seven days

The window is the newest `landed` date, `added_reference`, and the seven days before it:
7 to 14 October 2026 on the register at the merge with `main` (`37e6757ed`), eight
blocks holding 48 results.
The page names dates, never “today”: it is static and rebuilt on merge, and a render of
one tree is the same bytes on any day.
The heading links to `results.html?added-since=2026-10-07#all-results`, the section’s
own first day, so it lists the section’s results however long after the build it is
followed (#514’s review A, finding A3). The introduction’s “what arrived in the last
day” links `?added-age=1`, which counts whole UTC days, as `landed` is written (review
B, finding B4): on the day of the newest arrival it lists the two newest blocks.

A day nothing arrived on has no block.
Within a day, entries run from the highest S rung, then by id.
An entry has two lines: the id and the register’s headline as plain text, with its math
as written; then, quieter, its cases, `V3 C3 S3`, and its credit.
A list of cases longer than 40 characters is written as its count and its ends (`178
counts from 1 to 324`).

- **S4 and S5** are set in bold in the significance ink.
- **Superseded entries** are muted, their id is titled “Superseded”, and their quiet
  line ends “superseded”, which touch screens and screen readers see too.
  Their links keep their colour.
  In the weekly lines a superseded id is muted and underlined, and says “(superseded)”
  to a screen reader (#514’s review A, finding A4).
- **The two newest days start open**, and every older day and every week starts closed.
- **Each day ends with a link** to its own rows,
  `results.html?added=2026-10-12#all-results`. An exact day keeps that link correct
  however long after the build it is followed.

### The Added filter

The rows carry `data-added`, the `landed` date (`landed_day`). The bar has a visible
control, **Added within *n* days**, with `data-filter="added"` and `data-bound="age"`.
It uses the same mechanism as Max age, an age measured by `overview/table.js`
(`ageCutoff`), but from the day in UTC (`utcDay`), since `landed` is a UTC day; Max age
keeps the reader’s local day.
`?added-age=1` shows the results that reached the site on the UTC day or the day before.

`controlParam` gave every age control the one parameter `age`. Two age controls would
then answer to one parameter, so an age now takes its key, as the bounds do
(`added-age`). Max age keeps `age`, which the links in use already carry.

A preset-only select, **Added on** (`data-filter="added"`, `data-preset`), holds a row
to one day. It offers every day something reached the site, newest first, and is hidden
until a link sets it, as Project and At significance are.
A preset-only date input, **Added since** (`data-bound="since"`, `?added-since=`), holds
a row to a day or later; the section’s heading sets it.
A value the input cannot read, such as `2026-10-6`, is kept, shows no row and keeps the
control in the bar (review B, finding B5). A preset value no option offers, such as
`?added=` on a day nothing arrived, is added to its select as a disabled option and
applied, so the table shows no row and the bar names the day, rather than quietly
showing every row (#514’s review A, finding A5). The homepage’s link to the complete
table forwards all three parameters.

### Weeks before the seven days

The weekly rollup covers the four ISO weeks (Monday to Sunday) up to the day before the
seven days begin. If they begin mid-week, the newest week is cut at that day and its
summary names the days it covers (`span_label`). On the register at the merge with
`main` (`37e6757ed`) they begin on Wednesday 7 October, so the newest week is 5 and 6
October and the others run from 14 September to 4 October.

### What a weekly line says

- **Finder.** The finder is the credit line before any “after …” (`credit_finder`), the
  same split the table’s Credit cell makes.
  The name is the register’s own (`Couzo`, `ry-xu`, `Levy`). The “after” lineage stays
  in the row.
- **Order.** A week’s lines run from the most significant result: highest S rung, then
  the number of results, then the newest, then the name.
  This is the order the owner set for the project cards on 2026-10-01 (`project_order`).
- **Kinds.** Kinds are counted in words: `19 lower bounds`, `1 lower bound and 1 upper
  bound`, `3 optimality results`.
- **Ids.** Each id links to `#t-NNN` on the same page.
  A result above the floor carries its rung after its id in the significance ink
  (`T-060S5`).

### Credit links

A credit links to **the listed project the record attributes the results to**
(`finder_projects`), in a new tab, as a project’s card opens it.
For a weekly line, that is the project holding the most of the line’s results; for one
entry, the first listed project holding it.
This reads `result_projects`, which uses the source-coverage register and the project
lists behind the overview’s Other Square Packing Projects cards.
A finder whose results no listed project holds, such as this project (`Levy`) or
Karakuş, is named without a link.

Draft PR #490 adds contributor profiles and `Result.credit_html`. When it lands, the
name should link to the person’s profile instead.
That is a one-function change in `credit_link`.

### What counts

- **The weekly floor is S3 by the recorded score**, `significance.score >= 3`, the
  rubric’s “a substantive case result or machine audit”.
  The template takes `S3` and “four weeks” from `ROLLUP_FLOOR` and `ROLLUP_WEEKS`, and
  “seven” from `ADDED_DAYS`. The seven days have no floor.
- **Draft scores count as recorded.** On the register at the merge with `main`, three of
  the 160 entries carry a draft score that no review has yet confirmed, kept or changed:
  T-154, T-155 and T-156, all registered after the significance review of 11 October.
  The intake stack’s significance review (layer 5) confirms every draft, so the question
  does not block this work.
- **Superseded results are included, muted, and marked “superseded”** in both sections:
  a result superseded since was still new in its day and its week.
  The owner kept this choice.
- **Pending adoption, recorded-only and incomplete results count** as the table shows
  them. The overview reports what is new, and the status is in the row.
- **Claims beyond the horizon** never appear.
  The `beyond_horizon_claims` rows (n > 324) live in `source-coverage.yaml`, not in the
  register.
- **Withdrawn results** have left the register and are not listed.

### Placement

Both sections are at the top of the page, under the hero, so a returning reader sees
what is new before the rating ladders.
The owner kept this choice.
The deep links `results.html#all-results`, `#verification-ladders` and `#t-NNN` are
unchanged.

## Owner Decisions

| Question | Answer |
| --- | --- |
| 1. Weeks only, or days | Days for the last seven days, by arrival on the site; weeks before them, by publication |
| 2. Draft significance scores | Counted as recorded; layer 5 confirms every draft, so it does not block |
| 3. Superseded results | Muted, as prototyped |
| 4. Placement | Top of the page, as prototyped |

## Byte Cost

Measured on the register at 217 results, after the merge of `main` at `b16ddeb0a` on 19
October (#514’s review D):

| Measure | Bytes |
| --- | ---: |
| The seven days, 71 results over 12 to 19 October | 22,157 |
| The weekly rollup, 97 results in the four weeks before | 15,701 |
| Both sections | 37,858 |
| Ceiling for both (`tests/test_results_rollup.py`, `ROLLUP_BYTES`) | 48,000 |
| `results.html` on `main`, without the sections | 1,157,668 |
| `results.html` on this branch | 1,203,554 |
| Page ceiling (`site_urls.PAGE_BUDGET_EXCEPTIONS`, `test_overview.PAGE_CEILINGS`) | 1,250,000 |

The branch costs 45,886 bytes at 217 results, of which 37,858 are the two sections and
5,208 the rows’ `data-added`. An entry of the seven days costs about 312 bytes with its
share of the day’s heading: its id link, headline, cases, rungs and a linked credit.
A line of the weekly rollup costs about 520 bytes with its ids.

The sections are at 79% of their own ceiling.
About 32 more arrivals in one seven-day window than this one holds would fail
`test_the_overview_stays_brief`; single days have brought 30 (14 October) and 23 (19
October). Past that ceiling the overview is becoming a second table, and the remedy is a
shorter entry, not a higher number.

The page’s ceiling was 950,000, set on 11 October at 146 results.
At 160 results on 14 October the page, then 924,981 bytes, sat about 25,000 under it,
while that day’s intake registered about thirty (#514’s review A, finding A2), and this
branch raised it to 1,150,000. `main` re-selected it at 1,250,000 on 18 October, on
three-run desktop/mobile, light/dark and no-JS checks of the table alone at 212 results
and 1,141,207 bytes.
That timing predates the two sections, and no timing has been measured on the page with
them.

At 217 results the branch halves the page’s headroom, from 92,332 bytes to 46,446. A row
of the table is most of a result’s cost: 3,423 bytes on average and 4,603 at the 90th
percentile, against an average of 291 for its entry in the seven days, which only a
recent result has.
`test_the_results_page_has_room_through_its_room_count` holds the page
through a fixed count, `RESULTS_ROOM_THROUGH = 225`, 217 on 19 October and 8 more: each
result past the register’s count costs the 90th-percentile row and an average entry, so
1,203,554 + 8 × (4,603 + 291) = 1,242,706 bytes, and the room is about 9 results.
The count was 200 on 14 October, under the 1,150,000 ceiling.
The room shrinks as results are registered, and the test fails only when the page could
not reach the count at today’s cost; measured from the page alone it would slide up with
every registration (#514’s review B, finding B1). The intake that passes the count
re-measures the page, its timing included, and either lightens the table or moves the
ceiling as a measured choice (`think-v1qe`). The pending upper bounds of #675 and #678,
up to about 85 and 79 rows, do not fit under 1,250,000 with or without this branch, so
that choice comes with them at the latest.

The filter adds `data-added` to each row (about 25 bytes), one option to Added on for
each day something arrived, and the Added since control.
`devtools/overview/results.css` is a shared asset, cached once.

## Validation

- `tests/test_results_rollup.py` checks the rendered page against the register.
  It recomputes each day and week from the YAML, checking: the right entries, each once;
  their headline, cases, rungs, score and credit link; superseded marks; open state; and
  the links to the filter.
  It also checks that no result at the floor falls between the two sections.
  It tests the grouping rules on entries made for the purpose: one published in 2018 and
  landing in the window, one registered two days before it landed, which goes under the
  day it landed, and a record with no `landed`, which the schema no longer allows in the
  register, placed by its registration.
- `tests/test_stamp_landed.py` holds the merge step’s re-date (a branch’s new entries,
  rewritten in place and re-datable), the history on a scratch repository (a branch’s
  entry lands with its merge, on the merge’s UTC day) and the audit, the ids the parsed
  register and the line scan must agree on, and the live register read from the tree
  alone: every entry carries `landed`, none before its registration.
- `tests/test_overview.py` and `tests/test_site_project_tallies.py` hold the bar’s
  controls and every row’s facets, `added` included, and the page’s room through
  `RESULTS_ROOM_THROUGH`, 225 results until 22 October and 238 since, when the #719
  intake (T-229) passed the count and moved the page’s ceiling to 1,300,000.
- `tests/node/overview_table/` tests the `added-age`, `added` and `added-since` presets,
  their composition with Max age, the reader’s-day and UTC-day measurements, and the
  homepage link’s forwarding.
- `tests/test_site_result_filters.py` runs the filter in Chromium, its clock on the day
  of the newest arrival.
  It checks that `?added-age=1` shows exactly the results that arrived that day or the
  day before, some of them registered earlier; that the heading’s `?added-since=` shows
  the section’s results with Added since in the bar; that a day’s link shows that day’s
  results; and that a day nothing arrived on, or one the date input cannot read, shows
  no row and is named in the bar.
- `tests/test_site_rendering.py` serves the page with both sections taken out for the
  font-arrival negative control.
- Screenshots in Chromium at 1280 and 390 px, light and dark, show no horizontal
  overflow.

## Not Done

- No layout test in the Chromium lane (`SITE_LAYOUT_TESTS`) for the sections; the
  screenshots are the layout evidence (`think-w5eo`).
- Contributor-profile links wait for PR #490 (`think-pose`).
- No copy of the overview on the homepage (`think-d1ip`), and no feed.
- No timing measured on the results page with the two sections, and about 9 results of
  room under its 1,250,000-byte ceiling, with the sections at 79% of their own: both
  wait on `think-v1qe`, which owns the runway.
  On 22 October the #719 intake (T-229) took the page to 1,251,615 bytes at 229 results,
  past that ceiling; it measured the page’s timing and moved the ceiling to 1,300,000
  (`site_urls.PAGE_BUDGET_EXCEPTIONS`), about 9 results of room, and `think-v1qe` keeps
  the durable lightening.
- The site edition is cut on this branch as v0.8.0 (`78c37c335`), dated 20 October; if
  the merge or its deployment slips past that UTC day, a follow-up corrects
  `first_published`.

## References

- Bead `think-2z22`; epic `think-mq0k`
- [epistemics.md, Significance and Novelty](../../../../epistemics.md#significance-and-novelty)
- [Website implementation plan](plan-2026-10-08-site-layout-and-navigation.md)
- Draft PR #490, “add person profiles, linked credits and attribution policy”

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
