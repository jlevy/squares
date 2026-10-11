# Feature: Recent Results by Week on the Results Page

**Date:** 2026-10-11

**Author:** Claude (Opus 5.5), lane W of the 2026-10-11 intake pass, bead `think-2z22`

**Status:** Prototype on a lane branch, for the owner to judge; no pull request yet

## Overview

The owner asked on 2026-10-11 “whether we could do a rollup of results by day or week on
the results page for S3+ values”, and then: “It shouldn’t replace the table, but it
would be nice to have a brief overview with credits/links to those who have new
results.”

The prototype adds a section, **Recent Results by Week**, to `results.html` (which
`all-results.html` forwards to) under the page’s hero and above everything else.
The table, its filters and its row addresses are unchanged.
The section is generated from `packing/frontier/results.yaml` at render time by
`overview_sections.recent_rollup`; nothing in it is typed into the template.

Each of the last four calendar weeks is a native disclosure whose summary names the week
and its count (`5–11 October 2026 · 40 results`). Inside, there is one line per finder:
the finder’s name, linked to their project, then what kinds of result and how many, then
each result’s id as a link to its row.
The newest week with a result starts open and the earlier weeks start closed, so the
page opens on about ten lines.

## Decisions

### The date that places a result in a week

A result is placed by **the date its row already shows** (`Result.dated`): the
`attribution.published` of a result by others, and the `established` date of this
project’s own. This is the claim’s own date, the one the record chose for credit.
It is also the date the table’s Date column and its Max age filter use, so the overview
is a view of the table rather than a second clock.

Registration was rejected.
It records when this repository took a result in, which follows the intake schedule
rather than the finder’s work.
It would show T-087, published in 2018 and registered on 3 October 2026, as a new
result.
Confirmation was rejected too: it carries no date of its own, and it would credit
the review queue here rather than the finder.

The consequence is that weeks are not append-only.
A result registered late appears in the week it was published, so an earlier week can
gain a line. That is correct for credit, which is the overview’s purpose.

### Weeks, and days inside them

The overview uses **ISO weeks (Monday to Sunday), the last four, with one line per
finder**. It does not group by day.

In the four weeks to 11 October, 91 results are at S3 or above.
The weeks hold 6, 19, 26 and 40 results on 3, 7, 7 and 11 finder lines.
Grouping the current week by day would give 6 day groups with 2 to 5 finders each, about
18 lines against the 11 lines by finder, and a reader looking for who has new results
would find the same name under several days.
The day stays one press away: an id opens the row, whose first column is the date.

**For the owner:** keep weeks only, or add a quiet day range to each line (about 40
bytes a line).

### What a line says

- **Finder.** The finder is the credit line before any “after …” (`credit_finder`), the
  same split the table’s Credit cell makes.
  The name is the register’s own (`Couzo`, `ry-xu`, `Levy`). The “after” lineage stays
  in the row.
- **Order.** A week’s lines run from the most significant result: highest S rung, then
  the number of results, then the newest, then the name.
  This is the order the owner set for the project cards on 2026-10-01 (`project_order`).
- **Kinds.** Kinds are counted in words: `19 lower bounds`, `1 lower bound and 1 upper
  bound`, `3 optimality results`.
- **Ids.** Each id links to `#t-NNN` on the same page, the row’s own address, which the
  table highlights as the target.
  A result above the floor carries its rung after its id in the significance ink
  (`T-060S5`); there are 8 such results today.

### Credit links

The finder’s name links to **the listed project the record attributes most of that
line’s results to**. That is `result_projects`, which reads the source-coverage register
and the project lists behind the overview’s Other Square Packing Projects cards.
Ties go to the project listed first, and the link is the card’s own address.
A finder whose results no listed project holds, such as this project (`Levy`) or
Karakuş, is named without a link.

The cards on `index.html` have no per-card anchors, so the link goes to the project
itself rather than to its card.

Draft PR #490 adds contributor profiles and `Result.credit_html`. When it lands, the
name should link to the person’s profile instead.
That is a one-function change in `rollup_who`. The prototype changes no credit rendering
that #490 changes. Its edits to `overview_sections.py`, `render_overview.py` and the
document map are new blocks or lines away from #490’s hunks.

### What counts

- **The floor is S3 by the recorded score**, `significance.score >= 3`, the rubric’s “a
  substantive case result or machine audit”.
  The template takes `S3` and “four weeks” from `ROLLUP_FLOOR` and `ROLLUP_WEEKS`.
- **Draft scores are included.** A score the registering lane set is the record’s score
  until a review changes it, and the table shows it the same way.
  Excluding drafts would delay credit by the review.
  On this branch’s base, 22 of the 91 listed entries still have a `significance.by`
  ending “(repository; draft)”, 15 of them session 161’s (T-037 to T-053). The draft
  state is written only in the prose of `by`, and “confirming the draft of …” also
  contains the word, so the renderer cannot tell drafts apart without guessing.
  **For the owner:** if drafts should be marked or excluded, add a structured field (for
  example `significance.draft: true`, which the reviewing lane removes) rather than
  parse `by`.
- **Superseded results are included, muted, and titled “Superseded”.** A result
  superseded since was still new in its week, and dropping it would take credit away
  after the fact: wand125’s line for the week of 21 September (T-044 to T-046) would
  disappear. This is common: 31 of today’s 91 are superseded.
  **For the owner:** if muted ids read as noise, the alternative is the homepage’s rule,
  which hides superseded results.
- **Pending adoption, recorded-only and incomplete results count** as the table shows
  them. The overview reports what is new, and the status is in the row.
- **Regularizations** are not register rows.
  A result that carries `regularizations` counts once, by its own S rung.
  T-146, the regularized-certificates entry, is S2 and is not listed.
- **Simplifications** count by their S rung like any other kind; both today are S2.
- **Claims beyond the horizon** never appear.
  The 52 `beyond_horizon_claims` rows (n > 324) live in `source-coverage.yaml`, not in
  the register. A register entry beyond 324 would count like any other; none exists.
- **Withdrawn results** have left the register and are not listed.

### The week the overview ends on

The newest week is the one holding the record’s newest date: the latest `registered`, or
any later date a row shows (`rollup_reference`). It is never the build clock, so one
tree renders the same bytes on any day, as `reference_date` already ensures for the
tables. The summaries name dates, never “this week”, so a page that has not been rebuilt
is not wrong.

### Placement

The section is at the top of the page, under the hero, so a returning reader sees what
is new before the rating ladders.
The deep links `results.html#all-results`, `#verification-ladders` and `#t-NNN` are
unchanged. **For the owner:** top of the page, or directly above “All Results”.

## Byte Cost

| Measure | Bytes |
| --- | ---: |
| `results.html` before (3a5a91a90, 146 results) | 842,932 |
| `results.html` with the overview | 854,905 |
| The overview’s block | 11,605 |
| Ceiling (`site_urls.PAGE_BUDGET_EXCEPTIONS`, `test_overview.PAGE_CEILINGS`) | 950,000 |

The block costs about 30 bytes an id (80 for a superseded one) and about 250 a line.
`tests/test_results_rollup.py` holds it under 24,000 bytes, about twice today’s, as a
signal that it has become a second table.
The new stylesheet, `devtools/overview/results.css`, is a 1,628-byte shared asset, which
means one more cached request.
The homepage is not touched.

## Validation

- `tests/test_results_rollup.py` checks the rendered page against the register.
  It recomputes each week from the YAML: the right entries, each once, on the right
  lines, with the right finder and project link, superseded marks, rungs and open state.
  It also tests the grouping rules on entries made for the purpose.
- `tests/test_overview.py` with the new tests: 316 passed, including the page ceilings
  and the deterministic render.
- `packing-validate --only "browser floor"`: both steps passed (Biome, ESLint, `tsc`,
  122 Node tests, 56 liveness tests), the new stylesheet included.
- Adding the note to the document map regenerates one row of `SYNOPSIS.md`’s generated
  document table (`devtools.render_document_map`).
- Screenshots of the section in Chromium at 1280 and 390 px, light and dark, show no
  horizontal overflow (`scrollWidth − innerWidth = 0`).

## Not Done

- No layout test in the Chromium lane (`SITE_LAYOUT_TESTS`); the screenshots are the
  evidence for this prototype.
- No day view, no feed, and no copy of the overview on the homepage.
- Contributor-profile links wait for PR #490.

## References

- Bead `think-2z22`; epic `think-mq0k`
- [epistemics.md, Significance and Novelty](../../../../epistemics.md#significance-and-novelty)
- [Website implementation plan](plan-2026-10-08-site-layout-and-navigation.md)
- Draft PR #490, “add person profiles, linked credits and attribution policy”

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
