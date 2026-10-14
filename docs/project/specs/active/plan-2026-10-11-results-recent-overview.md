# Feature: Recent Results on the Results Page

**Date:** 2026-10-11, revised 2026-10-12 and 2026-10-14 (twice)

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

`landed` is recorded, not derived: a page never reads Git (OR-18).
`devtools.stamp_landed` writes it.
The entries already on `main` were dated once from its first-parent history
(`--backfill`), each by the first commit whose register holds it, which for a merged
pull request is the merge.
From now on the merge step stamps a records pull request’s new entries with the day it
merges (`--apply`, in [result-import.md](../../../packing/campaign/result-import.md)),
and `tests/test_stamp_landed.py` fails on `main` if any entry there has none.
An entry a branch adds carries no `landed` until it is stamped, and a render of the
branch places it by `registered`.

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
day” links `?added-age=1`, which counts from the reader’s day: on the day of the newest
arrival it lists the two newest blocks.

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
It uses the same mechanism as Max age: an age measured from the reader’s day by
`overview/table.js` (`ageCutoff`). `?added-age=1` shows the results that reached the
site on the reader’s day or the day before.

`controlParam` gave every age control the one parameter `age`. Two age controls would
then answer to one parameter, so an age now takes its key, as the bounds do
(`added-age`). Max age keeps `age`, which the links in use already carry.

A preset-only select, **Added on** (`data-filter="added"`, `data-preset`), holds a row
to one day. It offers every day something reached the site, newest first, and is hidden
until a link sets it, as Project and At significance are.
A preset-only date input, **Added since** (`data-bound="since"`, `?added-since=`), holds
a row to a day or later; the section’s heading sets it.
A preset value no option offers, such as `?added=` on a day nothing arrived, is added to
its select as a disabled option and applied, so the table shows no row and the bar names
the day, rather than quietly showing every row (#514’s review A, finding A5). The
homepage’s link to the complete table forwards all three parameters.

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

Measured on the register at the merge with `main` (`37e6757ed`), 160 results:

| Measure | Bytes |
| --- | ---: |
| The seven days, 48 results over 7 to 14 October | 15,452 |
| The weekly rollup, 68 results in the four weeks before | 10,439 |
| Both sections | 25,891 |
| Ceiling for both (`tests/test_results_rollup.py`, `ROLLUP_BYTES`) | 48,000 |
| `results.html` on this branch | 924,981 |
| Page ceiling (`site_urls.PAGE_BUDGET_EXCEPTIONS`, `test_overview.PAGE_CEILINGS`) | 1,150,000 |

An entry of the seven days costs about 320 bytes: its id link, headline, cases, rungs
and a linked credit.
The weekly rollup costs about 30 bytes an id and 250 a line, as before.
The busiest eight days so far, to 6 October, took in 76 results, about 24,300 bytes at
that rate, so the sections’ ceiling of 48,000 is about 1.3 times the largest the record
has given and 1.9 times the current size.

The page’s ceiling was 950,000, set on 11 October at 146 results.
At 160 results the page sat about 25,000 bytes under it, room for six more, while the 14
October intake registers about thirty (#514’s review A, finding A2). A row of the table
is most of a result’s cost: 3,447 bytes on average and 4,660 at the 90th percentile,
against about 320 for its entry in the seven days, which only a recent result has.
The new sections are 26 KB, about 3% of the page, so trimming them could not buy the
room; the ceiling is raised to 1,150,000 instead, below the 2,000,000 hard limit every
page is held to. `test_the_results_page_has_room_for_forty_more_results` holds room for
40 more results at the 90th-percentile row and an average entry: 924,981 + 40 × (4,660 +
281\) = 1,122,621 bytes.
At the average row the ceiling holds 59 more.
Past it, the remedy is a lighter table row, which every result pays for.

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
  day it landed, and a branch’s new entry with no `landed`, placed by its registration.
- `tests/test_stamp_landed.py` holds the stamp, the backfill on a scratch repository (a
  branch’s entry lands with its merge, and on the merge’s UTC day), the check’s rules,
  and the live register: every entry on `origin/main` carries `landed`, none before its
  registration.
- `tests/test_overview.py` and `tests/test_site_project_tallies.py` hold the bar’s
  controls and every row’s facets, `added` included, and the page’s room for 40 more
  results.
- `tests/node/overview_table/` tests the `added-age`, `added` and `added-since` presets,
  their composition with Max age, the reader’s-day measurement, and the homepage link’s
  forwarding.
- `tests/test_site_result_filters.py` runs the filter in Chromium, its clock on the day
  of the newest arrival.
  It checks that `?added-age=1` shows exactly the results that arrived that day or the
  day before, some of them registered earlier; that the heading’s `?added-since=` shows
  the section’s results with Added since in the bar; that a day’s link shows that day’s
  results; and that a day nothing arrived on shows no row and is named in the bar.
- `tests/test_site_rendering.py` serves the page with both sections taken out for the
  font-arrival negative control.
- Screenshots in Chromium at 1280 and 390 px, light and dark, show no horizontal
  overflow.

## Not Done

- No layout test in the Chromium lane (`SITE_LAYOUT_TESTS`) for the sections; the
  screenshots are the layout evidence (`think-w5eo`).
- Contributor-profile links wait for PR #490 (`think-pose`).
- No copy of the overview on the homepage (`think-d1ip`), and no feed.
- The site’s release edition for this change is the owner’s to cut
  (`check_release_impact` names `site`).

## References

- Bead `think-2z22`; epic `think-mq0k`
- [epistemics.md, Significance and Novelty](../../../../epistemics.md#significance-and-novelty)
- [Website implementation plan](plan-2026-10-08-site-layout-and-navigation.md)
- Draft PR #490, “add person profiles, linked credits and attribution policy”

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
