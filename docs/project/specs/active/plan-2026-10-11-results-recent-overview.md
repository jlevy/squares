# Feature: Recent Results on the Results Page

**Date:** 2026-10-11, revised 2026-10-12

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

- **Added in the Last Seven Days** (`overview_sections.recent_added`): every result the
  register took in over its newest day and the seven before it, one native disclosure a
  day, newest first, at every significance.
  Each entry gives its id (a link to its row), its headline, its cases, its V and C
  rungs and S score, and its credit.
  The two newest days start open.
- **Earlier Results by Week Published** (`overview_sections.recent_rollup`): the weekly
  rollup of S3 and above, one line per finder, for the four calendar weeks before those
  days. Every week starts closed.

The table, its rows and their addresses are unchanged.
Its filter bar gains one filter on the day a result was registered, **Added**
(`results.html?added-age=1`, and `?added=2026-10-12` for one day).

## Decisions

### Two dates, one per question

The register has two dates for a result, and each section uses the one that answers its
question.

- **What came in** uses `registered`, the day this repository took the result in.
  That is the owner’s “imported in the last day”.
  T-087, published in 2018 and registered on 3 October 2026, was new to the register
  that day, and by registration it belongs to 3 October.
- **Whose results are new** uses the date the row shows (`Result.dated`): the
  `attribution.published` date of a result by others, and the `established` date of this
  project’s own. This is the claim’s own date, the one the record chose for credit, and
  it is what the table’s Date column and its Max age filter use.
  The weekly rollup’s heading says “by Week Published”.

A result published before the seven days and registered in them appears in both
sections, under the day it was added and the week it was published.
On 12 October that is T-090, T-091 and T-092. No row shows a day after its registration
(the tests hold the register to this), so a result shown on any day from the rollup’s
first Monday on is in at least one of the two sections.

### The seven days

The window is the register’s newest `registered` date, `reference_date`, and the seven
days before it: 5 to 12 October 2026 on this branch.
That is the cutoff `?added-age=7` holds a row to on that day (`age_cutoff`, the function
Max age already uses), so the section and its heading’s link list the same results when
read on the day of the last registration.
The page names dates, never “today”: it is static and rebuilt on merge, and a render of
one tree is the same bytes on any day.

A day the register took nothing in has no block.
Within a day, entries run from the highest S rung, then by id.
An entry has two lines: the id and the register’s headline as plain text, with its math
as written; then, quieter, its cases, `V3 C3 S3`, and its credit.
A list of cases longer than 40 characters is written as its count and its ends (`178
counts from 1 to 324`).

- **S4 and S5** are set in bold in the significance ink.
- **Superseded entries** are muted and their id is titled “Superseded”, as in the weekly
  lines.
- **The two newest days start open**, and every older day and every week starts closed.
- **Each day ends with a link** to its own rows,
  `results.html?added=2026-10-12#all-results`. An exact day keeps that link correct
  however long after the build it is followed.
  The heading links to `results.html?added-age=7#all-results`, which counts from the
  reader’s day.

### The Added filter

The rows carry `data-added`, the `registered` date.
The bar has a visible control, **Added within *n* days**, with `data-filter="added"` and
`data-bound="age"`. It uses the same mechanism as Max age: an age measured from the
reader’s day by `overview/table.js` (`ageCutoff`). `?added-age=1` shows the results
registered on the reader’s day or the day before.

`controlParam` gave every age control the one parameter `age`. Two age controls would
then answer to one parameter, so an age now takes its key, as the bounds do
(`added-age`). Max age keeps `age`, which the links in use already carry.

A preset-only select, **Added on** (`data-filter="added"`, `data-preset`), holds a row
to one day. It offers every day the register took something in, newest first, and is
hidden until a link sets it, as Project and At significance are.
The homepage’s link to the complete table forwards both parameters.

### Weeks before the seven days

The weekly rollup covers the four ISO weeks (Monday to Sunday) up to the day before the
seven days begin. If they begin mid-week, the newest week is cut at that day and its
summary names the days it covers (`span_label`). On this branch they begin on a Monday,
so the weeks are 7 September to 4 October.

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
- **Draft scores count as recorded.** The intake stack’s significance review (layer 5)
  confirms every draft, so the question does not block this work.
- **Superseded results are included, muted, and titled “Superseded”** in both sections:
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
| 1. Weeks only, or days | Days for the last seven days, by registration; weeks before them, by publication |
| 2. Draft significance scores | Counted as recorded; layer 5 confirms every draft, so it does not block |
| 3. Superseded results | Muted, as prototyped |
| 4. Placement | Top of the page, as prototyped |

## Byte Cost

| Measure | Bytes |
| --- | ---: |
| The seven days, 65 results over 5 to 12 October | 20,013 |
| The weekly rollup, 55 results in the four weeks before | 8,174 |
| Both sections | 28,187 |
| Ceiling for both (`tests/test_results_rollup.py`, `ROLLUP_BYTES`) | 48,000 |
| `results.html` on this branch | 896,074 |
| Page ceiling (`site_urls.PAGE_BUDGET_EXCEPTIONS`, `test_overview.PAGE_CEILINGS`) | 950,000 |

An entry of the seven days costs about 308 bytes: its id link, headline, cases, rungs
and a linked credit.
The weekly rollup costs about 30 bytes an id and 250 a line, as before.
The prototype’s ceiling of 24,000 held the weekly rollup alone.
The busiest eight days so far, to 6 October, registered 76 results, about 23,400 bytes
at that rate, so the ceiling is 48,000, about 1.4 times the largest the record has given
and 1.7 times the current size.
Past it the remedy is a shorter entry, not a higher number, because the page’s own
ceiling is shared with every row of the table.

The filter adds `data-added` to each row (about 25 bytes) and one option to Added on for
each day the register took something in.
`devtools/overview/results.css` is a shared asset, cached once.

## Validation

- `tests/test_results_rollup.py` checks the rendered page against the register.
  It recomputes each day and week from the YAML, checking: the right entries, each once;
  their headline, cases, rungs, score and credit link; superseded marks; open state; and
  the links to the filter.
  It also checks that no result at the floor falls between the two sections.
  It tests the grouping rules on entries made for the purpose, including one published
  in 2018 and registered in the window.
- `tests/test_overview.py` and `tests/test_site_project_tallies.py` hold the bar’s
  controls and every row’s facets, `added` included.
- `tests/node/overview_table/` tests `added-age` and `added` presets, their composition
  with Max age, the reader’s-day measurement, and the homepage link’s forwarding.
- `tests/test_site_result_filters.py` runs the filter in Chromium.
  It checks that `?added-age=1` shows exactly the results registered on the register’s
  newest day or the day before, that the heading’s link shows the section’s results, and
  that a day’s link shows that day’s results.
- `tests/test_site_rendering.py` serves the page with both sections taken out for the
  font-arrival negative control.
- Screenshots in Chromium at 1280 and 390 px, light and dark, show no horizontal
  overflow.

## Not Done

- No layout test in the Chromium lane (`SITE_LAYOUT_TESTS`) for the sections; the
  screenshots are the layout evidence.
- No feed, and no copy of the overview on the homepage.
- Contributor-profile links wait for PR #490.

## References

- Bead `think-2z22`; epic `think-mq0k`
- [epistemics.md, Significance and Novelty](../../../../epistemics.md#significance-and-novelty)
- [Website implementation plan](plan-2026-10-08-site-layout-and-navigation.md)
- Draft PR #490, “add person profiles, linked credits and attribution policy”

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
