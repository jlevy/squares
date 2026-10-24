---
title: News Feed of Every Merged Pull Request
description: A committed record of every merged pull request, the tool and gate that keep it, and an in-place News toggle between notable stories and all changes by PR
author: Intake lane c-news-plan-1023, for the repository owner
---
# Feature: News Feed of Every Merged Pull Request

**Date:** 2026-10-23 (last updated 2026-10-24)

**Author:** intake lane `c-news-plan-1023` under coordinator `coord-intake-1023`, for
the repository owner

**Status:** Owner’s questions answered.
The owner answered every open question on 23 October 2026 ([Decisions](#decisions)).
Nobody has approved the plan itself.

**Tracking:** `think-vph5` (this plan); `think-4oj0` (News stories for the 16 merged S3
pull requests that had none, landed with #758 on 24 October); `think-n51k` (a pull
request carrying its own News entry, which this plan does not do)

## Overview

News today shows hand-written stories, and only some merged pull requests get one.
This plan adds:

- a committed record of every merged pull request, and a tool that writes it after each
  merge;
- a records-tier gate that fails when a pull request labelled S3 or higher has no News
  story, or when its story leaves out an S3+ result the pull request registered or
  raised;
- a toggle at the top of the News page, switched in place, between **Notable stories**
  (the stories, as now) and **All changes by PR** (one generated row per merged pull
  request, with its significance, the results it carries and the people those results
  credit);
- a raised byte budget for `news.html`, set on measured load checks, so the page keeps
  every story, with a check that fails while the page still has room;
- on each contributor profile, the list of pull requests that carry that person’s
  results.

The plan has three pull requests, each able to land on its own: first the page budget’s
raise, then Phase 1 (the record, its tool, the one-time backfill and the gate), then
Phase 2 (the page and the profile lists).

## The Owner’s Words

The owner, in conversation on 23 October 2026:

1. “Also, to confirm, can we in parallel make sure that every time we have a PR land,
   it’s clearly reflected in the news for all with significance S3+ And that’s labeled
   in a clear way. Should be part of our process and the design”

2. “You should be able to get the important things that have happened from every
   person’s contributions and so on.
   Let’s review how to best do this.
   And whether it should go in as part of the news stories or perhaps be a separate feed
   at the bottom of the news page”

3. “Maybe the best design would be to have a toggle at the top of the news page that
   shows either just the notable news stories or a feed of all changes by PR.”

4. Asked where the feed starts, the owner chose “All merged PRs (Recommended)”. Asked
   who builds the page part, the owner chose “Me, with the records (Recommended)”.
   [Decision 4](#decisions) gives both answers and who wrote each reading of them.

5. “Let’s plan this out separately and make sure that you have landed the news items in
   parallel that are outstanding first, before we tackle the bigger design problem.
   I don’t want this larger effort to derail anything else that’s able to be landed
   right now.”

6. On the toggle, after reading this plan’s first draft: “We should use a toggle at the
   top of the page, much like we had a while back in the history, where there was a Film
   | Workbench toggle”.

The owner’s answers to the plan’s questions are under [Decisions](#decisions).

Point 5 is why this is a plan.
Two things proceeded without it and the plan takes both as given: `think-4oj0` landed
News stories for the 16 merged S3 pull requests that had none (#758, merged at 5664ac1e8
on 24 October), and live intake lanes draft a News entry in the description of every S3+
pull request they open, which the coordinator lands after the merge.

## Goals

- Every merged pull request, from #1 on, appears once in a generated feed with its merge
  date, a clear S1–S5 badge (or a plain “not scored” mark), its title, the results it
  registered, raised or adopted, and the people those results credit, linked to their
  profiles.
- Every pull request labelled S3, S4 or S5 has a News story naming each S3+ result it
  registered or raised, and a gate fails the change that records the pull request
  without one.
- Landing a story after the merge is a named runbook step with a tool behind it, run in
  the same follow-up that records the merge.
- `news.html` carries both views and every story, under a byte budget raised on measured
  load checks, and a check fails while the page still has room, so the step after it is
  chosen on purpose.
- Rendering and validation stay offline: GitHub is read only by a tool at authoring
  time, as `site-changelog.yaml`’s header already requires.
- Each contributor profile lists the pull requests that carry the person’s results.

## Non-Goals

- No change to the home page’s News box, which PR #736 redesigns: its stories stay on
  `news.html`, so its links keep their targets.
  None to the atlas pages of #744 and #746.
- No story is written automatically.
  The feed row is generated; a story stays edited prose.
- No same-PR stories. An entry still needs its pull request’s merge facts, so it lands
  after the merge; letting a pull request carry its own entry, stamped at merge, is
  `think-n51k`.
- No retroactive GitHub labels on the 352 unlabelled pull requests; the feed scores them
  from their results ([Decision 2](#decisions)).
- No backfilled stories for the 109 S3 results or the 15 exempt S4 and S5 results that
  already lack one ([Decision 1](#decisions)); the 15 stay the separate decision
  `render_changelog.ANNOUNCEMENT_EXEMPT` names.
- No second address for the toggle ([Decision 3](#decisions)).
- No archive pages for stories ([Decision 6](#decisions)). Only feed rows leave
  `news.html`.
- Nothing automatic when the raised budget runs out.
  The step after it is the owner’s decision at that time.
- No person or topic filters on the feed beyond significance.

## Background

### What exists

- **`packing/site-changelog.yaml`** is the editorial record behind News and
  `CHANGELOG.md`, contract `packing.squares:SiteChangelog/v1`. Beside its `entries` it
  keeps one `deliveries` row per pull request an entry names (number, title,
  `merged_at`, `base_ref`, `merge_commit`, and `delivery_to_main` and `stack_id` for
  stack layers), the formal `stacks`, and `coverage`, which gives each delivery an entry
  or exactly one written omission.
  `render_changelog.validate` refuses an entry whose pull request has no delivery (“no
  retained merged main delivery”) and dates an entry by the latest merge day of its pull
  requests. A delivery exists only after the merge, so a story cannot land in the pull
  request it announces.
- **`devtools.import_changelog`** fetches merged pull requests with `gh pr view`, checks
  that each merge commit reaches local `origin/main`, takes the score from the single S
  label, and writes a candidate entry with placeholder prose and a coverage audit for
  review.
- **`devtools.render_changelog`** renders News.
  `news_entries` shows entries at S3 or higher without `news_exclusion`. The
  announcement gate (`--announcement-base`, in the records tier’s “synopsis agrees with
  the artifacts” step) requires a News item for every registered result at
  `ANNOUNCED_FROM = 4` or above, outside the 15 results in `ANNOUNCEMENT_EXEMPT`. It
  fails a pull request that edits the register or the News record while the debt stands,
  warns any other, and only warns on `main`.
- **The News page** (`render_overview.news_page`, template `news-article.md`) draws the
  significance filter (`news-significance-label`, buttons `data-news-score` for S3 to
  S5) and the topic menu above one card per story.
  `overview/news-filters.js` keeps the choice in the `news-s` and `news-topics` query
  parameters and opens on S4 and S5. S3 cards are rendered `hidden`, and
  `@media (scripting: none)` in `site.css` shows every card to readers without scripts.
- **The Film | Workbench tabs.** d73244ff4 (30 September, “Visualize: the film at full
  size, with a Workbench tab beside it”) added the Visualize section’s tabs:
  `render_overview.visualize_tabs` drew a `<nav class="site-tabs" aria-label="Visuals">`
  of two links, styled in `site-nav.css` by `nav.site-tabs a`, `a + a` and
  `a[aria-current="page"]`. 12a0a8438 (1 October, “the Film | Workbench tabs sit below
  the bar’s rule”) moved them into the header slot under the bar’s rule: a header that
  holds tabs hands its rule to the bar (`.kpress-site-header:has(> .site-tabs)`), the
  tabs stand `--site-tabs-space` (0.7rem) under the rule, and the page’s first block
  starts `--site-page-top` under the tabs.
  The same commit added the `preview_site/header` probe, `preview_site.tabs_problems`,
  `measure_site_pages header` and the Chromium test in `test_site_wide_blocks.py`. Those
  tabs were links between two pages.
  dd9bfa063 (22 October) retired them with the Film | Workbench switcher, but
  `kpress_page`’s `tabs` argument, the styles, the probe and `tabs_problems` remain, and
  `site-nav.css` already gives an in-place tab (`[role="tab"][aria-selected="true"]`)
  the current link’s fill.
- **An in-place tablist on the same strip.** The atlas’s Grid | Triangle view
  (`overview_sections.atlas_view_tabs`, `overview/atlas-view.js`) is a
  `site-tabs site-chooser-small` tablist of two buttons: `role="tablist"`,
  `aria-selected`, only the selected tab in the tab order, and the arrow keys, Home and
  End moving between them and selecting.
  `overview/embed.js`, which runs in the head of every page, sets `data-site-atlas-view`
  from `?atlas=` before first paint, and reads `?view=embed` for pages framed in a
  popover.
- **Page budgets.** `site_urls.PAGE_BUDGETS` gives a `page` 600,000 bytes, and
  `PAGE_BUDGET_EXCEPTIONS` raises that for named pages, each with a measured reason and
  under `HARD_HTML_LIMIT`, 2,000,000 bytes for every HTML file.
  `docs/project/site-urls.md` renders both.
  `check_published_site` holds every registered page to `page_budget(row)`: in the Pages
  workflow before a deploy (`--local site`), and on the deployed site after it.
  `test_overview.py` repeats two of the largest page ceilings in `PAGE_CEILINGS` and
  gives `results.html` a fixed runway, `RESULTS_ROOM_THROUGH`.
- **Load checks in Chromium**, through Playwright, in three retained tools:
  - `check_site_rendering`: CLS, LCP, longest task and blocking time at 1280 and 390 px,
    light and dark, served gzipped from a local server, with a separate no-JS
    readability context;
  - `measure_site_pages load`: DOMContentLoaded, load, first contentful paint and the
    bytes a load moves, optionally over a throttled network (`NETWORKS`);
  - `measure_atlas_views move`: what an in-place view change costs, with Chromium’s own
    main-thread counters (`Performance.getMetrics`).
- **Profiles** (`devtools.render_contributors`) list a person’s Records, Results and
  Credited Work from the reviewed credit manifest (`contributors/occurrences.yaml`)
  through `site_tallies.person_credit_stats`, and Related News from profile links in
  story prose (`news_by_profile`).
- **`devtools.stamp_landed`** is the precedent for a tool that reads history and writes
  the answer into a record.
  Its `--backfill` and `--audit` modes read the register at each first-parent commit of
  `main` (`git show COMMIT:packing/frontier/results.yaml`) to date each entry’s
  `landed`, and `--audit --apply` writes the corrections; its default `--apply` compares
  only with `origin/main`’s copy.
  Nothing that renders a page or gates a change reads Git, which is the rule
  [OR-18](../../../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob)
  sets: no program depends on Git history to produce its answer.

### Measured on 23 October 2026

The coordinator’s first figures were taken at 05e95db36. Every figure below was re-taken
at 769e441e1 and the record counts again at cc91ee1b8, where they are unchanged; GitHub
and the deployed site were read the same day.
The pace, budget, bytes-sent and timing rows were re-taken at 64b316b6c, with GitHub and
the deployed site read at about 23:00Z. Rows marked **24 October** were re-taken after
#758 merged: the record counts at da117ad0b, and the deployed News page as review A of
#759 measured it. The changelog’s counts were taken again at 14b14f2d1, after #765 added
three deliveries.

| Fact | Value | How measured |
| --- | --- | --- |
| Merged pull requests | 537, #1 to #752, merged 22 August 18:33Z to 23 October 17:20Z | `gh pr list --state merged --limit 2000 --json …` (3.6 s) |
| By S label | S1 34, S2 94, S3 45, S4 8, S5 4; none 352 | the same listing; no pull request has two S labels |
| Unlabelled pull requests | 352, all #711 or earlier; the first labelled is #246, and 8 since #600 have none (#681, #685, #691, #693, #696, #701, #710, #711) | the same listing |
| GitHub authors | `jlevy` 528, `Guzhou0806` 7, `wand125` 2 | the same listing |
| Reaching `main` | all 537; 521 merge commits on `main`’s first-parent line; 16 arrived inside a later merge (12 based on another branch, and #55, #122, #123, #336 based on `main`) | `git merge-base --is-ancestor` and `git rev-list --first-parent` |
| Bases other than `main` | 73 | the same listing |
| Merge pace | August 61, September 162, October to the 23rd 314; 95 in the last 7 days | the same listing |
| S3+ merge pace | 56 in October to the 23rd, 2.4 a day, and 1 before; 14 in the 7 days to 23 October 23:00Z, 2.0 a day | the same listing, re-read at 23:00Z, when it held 541 merged pull requests |
| Changelog entries, **24 October** | 63 at 14b14f2d1: S5 4, S4 8, S3 38, S2 13; News shows 50 (62 at da117ad0b; 48 entries and 36 on News on 23 October) | `site-changelog.yaml` |
| Deliveries, coverage, omissions, **24 October** | 120, 120, 42 at 14b14f2d1 (117, 117 and 40 at da117ad0b); 3 formal stacks (103, 103 and 42 on 23 October) | `site-changelog.yaml` |
| S3+ pull requests with a story, **24 October** | all 57; on 23 October 41, and the 16 without were #731, #725, #708, #699, #692, #688, #676, #671, #657, #645, #644, #621, #620, #578, #469, #460, all S3 and all merged in October, which #758 gave stories | labels from a fresh listing of 546 merged pull requests joined to entries’ `pull_requests`; the story gate as specified below fails none |
| Shared merge commits, **24 October** | 28 commits are GitHub’s `mergeCommit` for more than one pull request, 89 pull requests in all; 16 of the 28 register or raise a result, and one of them, d167d4b86, adopts | review A of #759, and a scratch read of the same listing with each pull request’s `headRefName` and `headRefOid` |
| Carried pull requests, **24 October** | 16, by the shape of their merge commit: 13 merge into their base; for 2 (#258, #298) it is their own head, their base branch fast-forwarded to it; for 1 (#336) it merges `main` into their branch | review B of #759, from a listing of 549 merged pull requests that adds `baseRefOid` |
| Register-changing merges, **24 October** | 125 first-parent commits of `main` change `frontier/results.yaml` | `git rev-list --first-parent origin/main -- packing/frontier/results.yaml` at da117ad0b |
| Register | 230 results; 177 at S3+ (S5 10, S4 11, S3 156) | `frontier/results.yaml` |
| S3+ results with no story at their own score | 124: the 15 exempt S4 and S5 results and 109 S3 results | the gate’s rule, `news_announced_scores` |
| S3+ results named by no entry at all | 121; T-062, T-064 and T-081 are named only by S2 entries, which News does not show | the coordinator’s first figure of 121 counts this way |
| The 109 unannounced S3 results by `landed` | 81 before 13 October, when the News archive began; 27 on 13–22 October; 1 on 23 October | `landed` |
| Deployed News page | 223,432 bytes: 36 cards averaging 5,264 bytes (2,867 to 11,846), and 33,910 bytes outside them; one significance meter paragraph averages 628 bytes | `https://squaremath.org/news.html`, fetched twice that day (223,194 bytes at the first fetch) |
| Deployed News page, **24 October** | 318,655 bytes: 50 cards averaging 5,685 bytes (90th percentile 8,479), the 14 cards added since 23 October averaging about 6,800, and 34,414 bytes outside the cards; sent as 43,345 gzipped bytes (7.4 to 1), where zlib at level 6 gives 41,988; 90 `<math>` elements | review A of #759 (`curl` with each `Accept-Encoding`); the card split re-counted from its copy of the page |
| Page budget | 600,000 bytes for a `page`, and 2,000,000 for every HTML file; News has no exception; the largest exceptions are 1,500,000 (`papers/n11-lower-bounds-explainer.html`), 1,400,000 (`results.html`) and 1,300,000 (`index.html`) | `site_urls.PAGE_BUDGETS`, `PAGE_BUDGET_EXCEPTIONS` and `HARD_HTML_LIMIT` at 64b316b6c, unchanged since 769e441e1 |
| Bytes sent | `news.html` 223,432 bytes, sent as 32,172 gzipped (6.9 to 1); `results.html` 1,303,283 as 86,414 (15 to 1); `index.html` 483,093 as 45,445; a request accepting only brotli got `news.html` uncompressed, and one accepting brotli or gzip got gzip | `curl` with each `Accept-Encoding` against `https://squaremath.org` |
| Load timings on record | `results.html` at 1,324,108 bytes passed three runs at desktop and phone widths, light and dark, and with scripts off: CLS 0, LCP at most 444 ms, longest task 197 ms, blocking 155 ms; News has none | the reason in `PAGE_BUDGET_EXCEPTIONS["results.html"]`, recorded on 22 October and not re-run |
| A large profile | 123,797 bytes (`profiles/evan-daniel.html`) | the deployed site |

## Design

### The merged-pull-request record

**A separate file, which absorbs `deliveries` and `stacks`.** The record is
`packing/pull-requests.yaml`, schema `packing/pull-requests.schema.yaml`, contract
`packing.squares:PullRequests/v1`, status `enforced`. It becomes the one home of every
merge fact. Every `deliveries` row (120 at 14b14f2d1) and the 3 `stacks` move into it in
Phase 1, and `site-changelog.yaml` keeps only editorial content: `entries`, `coverage`,
`frozen_entries` and the optional feed summaries, under contract `SiteChangelog/v2`. An
entry’s pull requests are looked up in the new record, where the old rule looked them up
in `deliveries`.

**The coverage rule under v2.** Today `validate` requires `coverage.pull_requests` to
equal both the set of `deliveries` and the pull requests entries represent together with
those omitted (`render_changelog.py:682`), and the runbook asks for an entry or an
omission for each S1 or S2 pull request
([`result-import.md`](../../../../packing/campaign/result-import.md#label-the-pr-and-prepare-news),
“For S1/S2, record a coverage omission or retain an entry in the full changelog”). Under
v2:

- `coverage.pull_requests` is a subset of the record’s numbers, and equals the pull
  requests the entries represent together with those omitted, each omitted at most once
  and never also represented;
- a row of the record owes `coverage` nothing: an S1, S2 or unscored row needs neither
  an entry nor an omission, so the about 430 rows the backfill adds need no written
  omission;
- an omission does not excuse an S3+ row, which the story gate holds to its story
  ([Gates](#gates)).

Every covered pull request and omission carries over unchanged (120 and 42 at
14b14f2d1). The runbook’s S1/S2 sentence changes to match in Phase 1
([Process](#process)), and `test_changelog.py` holds the rule: a coverage number the
record lacks fails, a coverage list that differs from the represented and omitted pull
requests fails, an S2 row with neither an entry nor an omission passes, and an S3 row
with only an omission fails the story gate.

Extending `deliveries` in place to all 537 pull requests was the alternative.
It loses on four counts:

- **The coverage rule.** Every delivery needs an entry or exactly one omission, so the
  about 430 new deliveries would need as many written omissions, or the rule would have
  to change anyway.
- **Authorship.** `site-changelog.yaml` is hand-edited prose under review; the record is
  written by a tool, apart from the curated stacks it keeps, and can be rewritten from
  GitHub and Git. Mixing them puts several thousand machine-written lines in the file
  editors work in, and a tool rewriting part of it on every merge.
- **Shape.** `deliveries` cannot say that a pull request reached `main` inside another
  merge: `validate` requires `delivery_to_main.commit` to equal the merge commit, and
  `import_changelog` refuses a merge commit off the first-parent line.
  Sixteen of the 537 are such pull requests.
- **Readers.** The feed and the profiles need merge facts for every pull request; they
  should not read the editorial record to get them.

Keeping `deliveries` and adding a superset beside it would hold each merge fact twice
and need a check that the two agree.
Moving them costs one migration and leaves one home for each fact.

**Fields.** One row per merged pull request, newest number first:

```yaml
softschema:
  contract: packing.squares:PullRequests/v1
  schema: pull-requests.schema.yaml
  status: enforced
repository: https://github.com/jlevy/squares
pull_requests:
  - number: 706
    title: 'records(#678): stage 4 raises T-223 to V3/C3 and adopts it at 204 and 260'
    merged_at: '2026-10-21T22:19:02Z'
    base_ref: main
    merge_commit: bb0c24e9f5125546316be2860bce295149ac299c
    author: jlevy
    labels: [S3, intake]
    results:
      - {id: T-223, change: raised, score: 3}
      - {id: T-223, change: adopted, n: [204, 260]}
stacks: []          # moved unchanged from site-changelog.yaml
```

| Field | Required | Meaning |
| --- | --- | --- |
| `number`, `title`, `merged_at`, `base_ref`, `merge_commit` | yes | GitHub’s facts at the latest read, as `deliveries` holds them today |
| `author` | yes | the GitHub login that opened the pull request; provenance, not credit |
| `labels` | yes, may be empty | every GitHub label; the significance label is the one `S1`–`S5` label, at most one |
| `delivery_to_main` | when the base is not `main` or the merge commit is off `main`’s first-parent line | `{commit, evidence}`: the first-parent commit of `main` whose history first holds the merge, and its commit URL; `via` names the carrying pull request when there is one |
| `stack_id` | no | formal stack membership, as today; curated, and kept by the tool |
| `results` | no | each result this pull request’s own change delivered ([the tool](#the-tool-devtoolsrecord_pull_requests) says how a shared or carried merge is split): `registered` (a new id), `raised` (a higher verification or confirmation rung, or a higher significance), or `adopted` with the counts `n` it became the house best packing at; a `registered` or `raised` item carries `score`, the result’s significance at the pull request’s own head |

Everything in the record but the formal stacks is written by the tool.
The `stacks` list and each row’s `stack_id` are curated, as they are in
`site-changelog.yaml` today: the fetch reads no stack field, and two of the three stacks
give a pull request page as their evidence.
The tool keeps both as it finds them on every rewrite, and `test_pull_requests.py` holds
that a rewrite keeps them.
The two hand-edited fields the first draft put here live with the other editorial
content instead:

- **Pull requests allowed no story** are `render_changelog.STORY_EXEMPT`, a constant
  beside `ANNOUNCEMENT_EXEMPT`, mapping each number to its reason.
  It starts empty and may only shrink ([Gates](#gates)).
- **A feed summary**, one plain sentence for a title worth replacing
  ([Coordinator Defaults](#coordinator-defaults)), is an entry of the optional
  `pull_request_summaries` mapping in `site-changelog.yaml`, keyed by number, each
  number a row of the record.

So the tool’s rewrite carries over the curated stacks and no other hand-edited field,
and rewriting the rows from GitHub and Git loses no edit.

**Why each item keeps its score.** `score` on a `registered` or `raised` item is the
result’s significance when this pull request delivered it, a fact of that delivery.
The register keeps the result’s current score, and a later rescoring there is the
`raised` item of the pull request that made it.
The label floor, the story gate’s result rule and the score taken from results
([Gates](#gates), [Decision 2](#decisions)) read the item’s `score`, so a later raise is
not charged to an earlier pull request.

Three fields the coordinator proposed are derived at render time rather than stored,
each because storing it would give a fact a second home:

- **Significance** is the S label.
  A pull request with no S label takes the highest `score` among the results it
  `registered` or `raised`, and is marked as scored from its results
  ([Decision 2](#decisions)). A pull request with neither is “Not scored”.
  The label can change after a merge, and the tool’s next run refreshes `labels`.
- **News entry ids** are the entries whose `pull_requests` name the number;
  `site-changelog.yaml` is their one home.
- **Credited people** are derived from `results` through the reviewed credit records,
  below. A credit correction there then reaches the feed and the profiles without editing
  this record.

**How credited people are derived.** Most pull requests are opened by the owner’s
account on behalf of agents (528 of 537), so the GitHub author says nothing about
credit. The people a row names come from the records, in this order:

1. **The results’ authors and credits.** For each id in `results`, the primary authors
   and the people credited in other roles, exactly as profiles count them:
   `site_tallies` joins the reviewed spans in `contributors/occurrences.yaml` to the
   result’s `attribution.source_keys` in `results.yaml` and the sources’ `credit` text
   in `resources/bibliography.yaml`, and a first-party result credits `Levy` through
   `result_credit.PROJECT_AUTHOR`. [`attribution.md`](../../../../attribution.md) owns
   the rules: Results and Credits are disjoint, and an `after` credit is not authorship.
   Phase 2 makes the private joins in `site_tallies` a public function,
   `result_people(record)`, so the feed and the profiles share them.
2. **The reporter.** For each result, the issues in `campaign/result-requests.yaml`
   whose `results[].register` lists it give the issue `author`, a GitHub login, which
   resolves to a profile through the profile’s `links` entry of kind `github`. The
   reporter is named as “reported by” unless already named under 1.
3. **An outside author.** The pull request’s `author` is named as “pull request by” when
   it resolves to a profile and is not the project account `jlevy`: today `Guzhou0806`’s
   7 pull requests and `wand125`’s 2.

A login that resolves to no profile is not shown, because the attribution policy does
not turn an unreviewed handle into a credit.
A row with no results and no outside author names nobody.
The project account is never shown as a pull request’s author: agents open those pull
requests, and attribution.md credits no agent and treats project ownership as different
from authorship.

### The tool: `devtools.record_pull_requests`

`devtools.record_pull_requests` reads GitHub and Git at authoring time and writes the
record. A separate offline module, `devtools.pull_request_record`, loads, validates and
derives from it for every renderer and gate, as `render_changelog` and
`import_changelog` divide the same work today.

- **Fetch.** One call:
  `gh pr list --repo jlevy/squares --state merged --limit 2000 --json number,title,mergedAt,mergeCommit,baseRefName,baseRefOid,headRefName,headRefOid,labels,author`.
  On 23 October it returned 537 rows in 3.6 s, and on 24 October, with the two head
  fields and `baseRefOid`, which rules 3 and 4 below read, 549 rows in 3.9 s. The tool
  refuses a result whose length equals the limit, which could be a truncated list.
- **Verify.** Each merge commit must reach local `origin/main` (fetch it first), the
  check `import_changelog.verify_main_delivery` makes today.
  For a merge commit off the first-parent line, the tool finds the first first-parent
  commit of `main` that holds it, by ancestry tests along
  `git rev-list --first-parent origin/main`, and records it as `delivery_to_main`. A
  pull request that never reached `main` is refused by name.
- **Results.** Each row’s `results` are the change its own pull request delivered, not
  the whole of the merge that brought it to `main` (How results are attributed, below).
  The tool reads each entry’s id, rungs and score with a line scanner of the kind
  `render_changelog.register_score` is, so it need not parse a 1.99 MB register per
  commit. 125 first-parent commits on `main` had changed the register on 24 October.
- **Idempotent.** Rows are sorted by number and written atomically with a fixed YAML
  layout. A run with nothing new writes nothing, and a second run of the same input is
  byte-identical. A row already recorded is refreshed only in `title` and `labels`, which
  GitHub lets change after a merge, and the tool prints each refresh.
  It refuses to change a recorded `merged_at`, `merge_commit` or `delivery_to_main`, as
  `import_changelog.draft` refuses today.
- **Modes**, from `packing/`, with the `NO_PROXY` settings
  [Publishing Hosted Data](../../../../development.md#publishing-hosted-data) gives for
  running `gh`:
  - `python -m devtools.record_pull_requests` lists the merged pull requests the record
    lacks and the label or title changes, and writes nothing.
  - `--apply` writes them.
    Its first run is the backfill of every merged pull request.
  - `--pr N` limits a run to one pull request.
  - `--audit` reads only local Git: every first-parent `Merge pull request #N` commit on
    `origin/main` has a row, and every row’s merge commit is reachable.
    It gates nothing, like `stamp_landed --audit`.
- **The backfill** is the first `--apply`: about 550 rows, every migrated `deliveries`
  row among them, whose `merged_at`, `base_ref`, `merge_commit` and `delivery_to_main`
  must agree with what GitHub and Git return (a title edited since is refreshed and
  listed), and the `results` of the register-changing merges, 125 on 24 October.
  Its evidence lists each shared-merge group and carried pull request with the results
  each row took, and any group it refused.
  Its cost is estimated, not measured, at under five CPU-minutes: one GitHub call, two
  `git show` reads of the register for each register-changing merge, one for each layer
  head of a shared group and two for each carried pull request, about 370 in all, and as
  many of `upper_bound_houses.py`. The scratch read of the 28 shared groups took 9 s,
  and the re-run of the corrected rule over all 39 delivering commits that more than one
  pull request reaches took 20 s on the shared host.
- **Its standing under OR-18.** The tool reads `git show REV:path` at historical
  commits, which OR-18 rules out for a program that produces an answer.
  It is an authoring-time acquisition: it reads history once, writes the facts into a
  reviewed record, and nothing re-derives them later.
  The precedents are `stamp_landed --backfill` and `--audit --apply`, which read the
  register at first-parent commits and write `landed`, and
  `import_changelog.verify_main_delivery`, which checks a merge’s ancestry while an
  entry is drafted. No gate, renderer or test reads `results` from Git: the gates read
  the committed record and register, and the tests build their own fixture repositories.

**How results are attributed.** GitHub can give one `mergeCommit` to several pull
requests: every layer of a formal stack or chain that lands together gets the commit
that delivered the whole group.
On 24 October 28 commits were the `mergeCommit` of more than one pull request, 89 in
all. A merge’s first-parent diff therefore cannot be a row’s `results`, or each layer
would show every other layer’s results, credits and story debt.
The tool works per delivering commit *D*, a first-parent commit of `main`: a row’s merge
commit when that is on the first-parent line, otherwise its `delivery_to_main.commit`.

1. **The group’s change.** The register at *D*’s first parent against the register at
   *D*: new ids are registered, and an id whose rung or significance rose is raised.
   The house table `upper_bound_houses.ADOPTED` at the same two commits gives the
   adoptions: each count whose entry is new or names another id.

2. **One pull request.** When *D* delivers one pull request, as for most merges, that
   row takes the whole change, less what a pull request carried into *D* takes (rule 4).

3. **Layers that share *D* as their `mergeCommit`.** The tool orders them into one chain
   by their refs: exactly one is based on `main`; each other’s `baseRefName` is another
   layer’s `headRefName`, and its `baseRefOid` that layer’s `headRefOid`; and each
   layer’s `headRefOid` is an ancestor of *D* and of the head of every layer above it.
   On 24 October each of the 61 layers not based on `main` had the head of the layer
   below as its `baseRefOid`. A layer’s own change is the register and `ADOPTED` at the
   head of the layer below it (for the layer based on `main`, *D*’s first parent)
   against both at its own head.

4. **A pull request carried into *D*** by a merge into another branch, one whose merge
   commit *M* is off the first-parent line, has its own change measured from the base
   side of *M*, by *M*’s shape:
   - when *M*’s second parent is the pull request’s head, *M* merged it into its base,
     and its change is *M*’s first parent against *M*, as for 13 of the 16 carried pull
     requests on 24 October;
   - when *M* is its head, because the base branch was fast-forwarded to it (#258,
     #298), or *M*’s first parent is its head, because *M* merges the base into its
     branch (#336), its change is GitHub’s `baseRefOid` against its head;
   - any other shape is refused by name.

   The row whose own change holds *M*, the pull request that carried it, takes none of
   its registrations, raises or adoptions.

5. **What a row keeps.** A row keeps only what is part of the group’s change: an id the
   group registers, an adoption the group makes, and a raise of an id the group raises
   or registers. So a later layer’s raise of an id an earlier layer registered is kept,
   though the id is new against *D*’s first parent: #459 raises T-127, which #448
   registered. An id that a layer’s branch took from `main`, merging it in after `main`
   registered the id, is not part of the group’s change and is dropped.

6. **Everything accounted for once.** Every id the group registers, and every adoption
   it makes, goes to exactly one row.
   Every rise it makes goes to at least one, and a rise of an id the group registers
   goes to the row that raised it, while the row that registered the id keeps the
   registration. The tool refuses these by name, and records such a group only when the
   reviewed backfill says which pull request delivered each id:
   - a group whose layers cannot be ordered;
   - a head that is not an ancestor of *D*;
   - two rows with the same head, whose changes overlap, as #249 and #258 do
     (b2f622f17);
   - a carried merge commit of another shape;
   - a change no row accounts for.

The review’s example is d3860c97a, “Merge pull request #469”, GitHub’s `mergeCommit` for
11 pull requests. Its first-parent change registers T-125 to T-130. By the rule above,
read from the 11 layer heads on 24 October:

- #442, the layer based on `main`, registered T-125 and T-126;
- #448 registered T-127, and #459 raised it;
- #460 registered T-128, #463 T-129 and #469 T-130;
- #443, #449, #450, #466 and #468 registered and raised nothing.

The first-parent diff alone would have given all six ids to all 11 rows.
The same read ordered all 28 shared groups by their refs, and in each one the layers’
own changes added up to the merge’s change, every registered id claimed once.
One of the 28 adopts: d167d4b86, which delivers #661 and #676 and carries #662, sets
`ADOPTED[29]` to T-195. #661’s head already holds that entry, so #661 takes T-195 and
its adoption at 29, #676 takes T-196 to T-199, and #662 takes nothing.

Of the 16 pull requests carried by a later merge, three have a merge commit that does
not merge them into their base, and rule 4 measures them from their `baseRefOid`:

- **#298**, carried into #292’s merge 47569ad50. GitHub’s `mergeCommit` for it is its
  own head, 944d2d39f, which merges #292’s branch at c307f646f, its `baseRefOid`. From
  there #298 registered T-070 to T-079 and raised T-048, T-055, T-058, T-059, T-062,
  T-063 and T-064, and also T-066 to T-069, which #292 registered.
  #292 takes T-066 to T-069 and no raise.
  Measured from its merge commit’s first parent, #298 would have taken nothing, and #292
  all 14 ids, the 7 raises and the people credited for #298’s results.
- **#336**, carried into #383’s merge 00f320296. Its merge commit, 0d4442a0e, merges
  `main` into its branch, and from its `baseRefOid`, 62f81e3a6, to its head it
  registered nothing. The seven ids that merge commit’s first-parent diff shows were
  `main`’s: T-094 from #362, T-095 to T-098 from #369, and T-099 and T-100 from #381.
- **#258**, carried into #249’s merge 306ae9fab. Its merge commit is its head,
  b2f622f17, which is also #249’s head, so rule 6 refuses the group.
  T-061 comes from #258’s first commit, 818d6cf3f, a merge of `main` that renumbers the
  result #249 registered as T-058 (73d5a98af), and the reviewed backfill names the row
  that takes it.

The other 13 carried pull requests, measured from their merge commit’s first parent,
registered, raised and adopted nothing.
Review B of #759 checked the rule with its own script, which reads the register as YAML
and `ADOPTED` at the same commits.
Adapted to the rule as corrected here and re-run read-only on its 549-row listing and
local Git at 14b14f2d1, the script covers the 39 delivering commits that more than one
pull request reaches, 18 of which register, raise or adopt.
38 pass: each of the 75 ids they register is claimed by exactly one row, every rise by
at least one, and the one adoption by #661. 306ae9fab is refused for its equal heads.
These figures come from scratch reads of the GitHub listing and local Git; the tool and
its backfill evidence re-derive them.
Because each row holds only its own results, the credited people derived from it and the
story it owes follow the pull request that delivered them.

`import_changelog` changes in two ways.
It reads merge facts from the record rather than writing `deliveries`. It also takes a
drafted entry from the pull request’s description, which it still reads from GitHub
(`gh pr view`, its `body` field) at authoring time; rendering and every gate stay
offline.
Live lanes already draft the entry under a **News** heading; this plan fixes its
form as one fenced `yaml` block under `## News`, which becomes the candidate in place of
placeholder prose, with the merge day as its `date`. The candidate is still reviewed
before it lands.

### Process

**Where the step goes.** Stage 7’s
[After the Merge](../../../../packing/campaign/result-import.md#after-the-merge) gains a
first step, **Record the merge**, ahead of the replies.
Once the deploy of a merge is verified, the intake pass’s runner:

1. fetches `origin/main` and runs `python -m devtools.record_pull_requests --apply`;
2. for each newly recorded pull request labelled S3 or higher, runs
   `python -m devtools.import_changelog --pr N --output "$TMPDIR/changelog-candidate.yaml"`,
   reviews the candidate it takes from the description, checks that its `result_ids`
   name every S3+ result the row `registered` or `raised`, and brings the entry into
   `site-changelog.yaml` with its coverage number;
3. renders with `python -m devtools.render_changelog`, runs
   `packing-validate --records`, and lands the change as the first change after the
   merge, the same follow-up that records the replies.

**The page’s room.** Once the budget raise has landed, the follow-up that lands a story
runs `python -m devtools.measure_news_page bytes` on the rendered page; from Phase 1 on
that is step 3. When the page it reports comes within 432,000 bytes of the trip point,
past about 718,000 bytes at the proposed trip point of 1,150,000, the coordinator opens
a `decision` bead for the owner in that follow-up, before the check fails.
At this plan’s pace of 14,400 bytes a day, 432,000 bytes is about 30 days of stories;
the report prints its own count of days left as a figure, not as the trigger.
The bead says that at the trip point no S3+ merge can be recorded, and that once
`main`’s page is at or over the point no change in the trip check’s failing scope can
merge, S1 and S2 recording included.
It asks the owner to choose the next step before the page gets there
([The page budget](#the-page-budget)).

**Who runs it.** The intake pass’s runner, its coordinator, which merges under the
`github-merge: autonomous` grant ([Decision 5](#decisions)). When the owner merges by
hand, the next pass’s sweep lists the pull request and that pass records it.

**Each follow-up is recorded by the next.** The follow-up is a merged pull request too,
so the record always trails `main` by the latest follow-up and by anything merged after
it. The sweep tells that tail apart from a gap (below).

**The runbook and the comments change to the 23 October rule** in Phase 1. Each passage
below stops being true then, and Phase 1’s checklist item rewrites every one.
Line numbers are `main`’s at 14b14f2d1.

- [Label the PR and Prepare News](../../../../packing/campaign/result-import.md#label-the-pr-and-prepare-news):
  - `result-import.md:1128-1131`, “For other S3–S5 work, S3 results included, News stays
    optional, as before: draft a concise News entry before merge, or record an editorial
    omission when the PR is an intermediate research checkpoint without a distinct
    reader-facing development.”
    It becomes: every pull request labelled S3, S4 or S5 has a story naming each S3+
    result it registers or raises (the owner, 23 October 2026, point 1 above and
    [Decision 1](#decisions)). This plan adds the form and the landing step: the story
    is drafted under **News** in the pull request’s description as a fenced `yaml` entry
    and landed in the first change after its merge.
    The omission clause goes: an S3+ pull request cannot be omitted, since
    `STORY_EXEMPT` may only shrink, so a pull request that is an intermediate checkpoint
    with no reader-facing development is labelled S1 or S2 by the rubric instead.
  - `:1142-1143`, “For S1/S2, record a coverage omission or retain an entry in the full
    changelog; these scores stay out of News.”
    It becomes the v2 coverage rule: an S1 or S2 pull request’s row is its record, and
    an entry or an omission is optional.
  - `:1148-1166`, the import paragraph (“After the source PR merges and its commit
    reaches local main, use the existing authoring command”, through “bring the approved
    entry into `site-changelog.yaml`”). Its candidate brings a delivery row; it becomes:
    once Record the merge has written the row, `import_changelog` reads the merge facts
    from `pull-requests.yaml`, takes the drafted `## News` block from the description,
    and the candidate carries the entry and its coverage number, with no delivery row.
- [Stage 7](../../../../packing/campaign/result-import.md#stage-7-answer): `:1292-1294`,
  “Every S4 or S5 result gets a News item in the first change after the merge that
  registered or raised it”.
  It gains the pull-request rule (every S3+ pull request gets its story in that change)
  and Record the merge as the change’s first step.
- [Announce a Significant Result](../../../../packing/campaign/result-import.md#announce-a-significant-result):
  - `:1357-1358`, “S3 News stays optional, as Label the PR and Prepare News says.”
    It becomes: S3 results reach News through the story of the pull request that
    registers or raises them (the owner, 23 October, [Decision 1](#decisions)), and that
    story is held by the story gate.
    The section keeps the 22 October rule for registered results and adds the
    pull-request rule and its gate.
  - `:1372-1374`, step 2’s “Bring its delivery row, its coverage number and the reviewed
    entry into `site-changelog.yaml`”. The delivery row is now the record’s, written by
    Record the merge, so the step brings the coverage number and the entry.
- [After the Merge](../../../../packing/campaign/result-import.md#after-the-merge)
  (`:1509`) gains Record the merge as its first step.
- [Maintaining the project changelog](../../../../development.md#maintaining-the-project-changelog):
  `development.md:2128-2130`, “One merged PR may support separate articles for distinct
  contributions, with one retained delivery row and all article IDs listed in its
  coverage audit”, and the section says where merge facts now live.
- The `ANNOUNCED_FROM` comment (`render_changelog.py:708-711`), which ends “S3 News
  stays optional.” It cites both decisions instead: 22 October (“Let’s have it do S4 and
  S5 then”) for registered results, and 23 October (“Via each PR’s story (Recommended)”)
  for S3 results, which reach News through the story of the pull request that registers
  or raises them. Its value stays 4.
- `.github/PULL_REQUEST_TEMPLATE.md`’s opening comment, “Prepare appropriate News
  wording or an explicit editorial omission under that policy”, names the `## News`
  block form and drops the omission for S3+.

### Gates

**What catches an S3+ story left out.** The story gate runs inside
`render_changelog --check` in the records tier, in the step that already runs the
announcement gate. It reads only the tree:

- every pull request an entry names is a row of the record, and an entry’s date is the
  latest merge day of its pull requests (the rule today, moved to the record);
- every row whose S label is S*k*, with *k* at least 3 and the row not in
  `STORY_EXEMPT`, is named by a News-shown entry scored *k* or higher, so an S4 pull
  request named only by an S3 entry fails, as a result announced below its score does
  today;
- for rows numbered above Phase 1’s own pull request (a constant set when that pull
  request is opened), that entry also lists in `result_ids` every result the row
  `registered` or `raised` with a `score` of 3 or more ([Decision 1](#decisions));
  earlier rows are reported, not failed;
- a score taken from results ([Decision 2](#decisions)) owes no story;
- a `STORY_EXEMPT` entry that now has its story, or names a row that is not S3+, fails
  until it is removed, the same rule `ANNOUNCEMENT_EXEMPT` follows.

**The label floor.** A row’s S label, when it has one, is at least the `score` of every
result it `registered`, since the rubric gives a registered result’s pull request that
result’s score (“A new registered result and its announcement inherit that result’s
actual S score”,
[Label the PR and Prepare News](../../../../packing/campaign/result-import.md#label-the-pr-and-prepare-news)).
Under Decision 1 an S3 result reaches News only through its pull request’s story, so an
S2 label on that pull request would keep the result off News with nothing to catch it.
The check reads only the record, runs in the same step with the same scopes as the story
gate, and lists each row it fails with the result and its score.
A raise is left to the rubric, since raising a rung is not always new significance, and
the story gate already requires an S3+ row’s story to name the S3+ results it raised.
Review A of #759 scanned the 125 register-changing merges and found none labelled below
a result it registers, and the scratch read of the 28 shared groups found no layer below
one (#463, labelled S1, registered T-129 at score 1), so the floor starts with no
exemptions.

A row and its story arrive in the same follow-up, so the change that records an S3+ pull
request without its story is the change that fails.
The gate follows the announcement gate’s scopes: it fails a pull request that edits
`pull-requests.yaml` or `site-changelog.yaml`, warns on any other, and only warns on
`main` (`--announcement-base HEAD^1`), where a merged change can no longer act.

**What catches a merge never recorded.** No offline gate can, because the tree does not
know what GitHub merged, and OR-18 rules out deciding it from Git history.
Three things cover it:

- `make intake` (`intake_sweep`) gains a **Merged pull requests** section from the same
  GitHub listing. A merged pull request missing from the record **needs action** when it
  is labelled S3 or higher, or merged before the newest recorded one (a gap).
  It is **listed** when it is an S1, S2 or unlabelled pull request merged after the
  newest recorded one, the trailing follow-up.
  A row whose labels differ from GitHub’s needs action, since a relabel can create or
  remove a story debt.
  `--offline` runs `record_pull_requests --audit` instead.
- The record step’s own listing, run before every follow-up.
- The feed states the newest pull request it covers, “Changes recorded through #N,
  merged on D”, so a reader can see the tail.

**Other checks on the record**: the enforced schema in the soft-schema step, with the
record added to `validate_schemas`’ corpus and to the `known_inputs` of the two
validation steps that list `site-changelog.yaml`; unique numbers in descending order; at
most one S label a row; `merged_at` timestamps that parse; `delivery_to_main` evidence
that matches its commit; stack membership as today; every result id in the register.

**The freeze check.** `validate_previous_ref` validates `main`’s changelog with the
current `validate` code, then compares entry ids, dates and pull request membership,
which is all the freeze needs.
From Phase 1 on it accepts either contract from the base:

- **a `SiteChangelog/v1` document**, which only Phase 1’s own pull request sees on
  `main`, is validated against its own schema, and its entries’ dates come from its own
  `deliveries`;
- **a `SiteChangelog/v2` document**, what `main` holds once Phase 1 merges, takes its
  entries’ dates from the base’s `pull-requests.yaml`, read at the same merge base.

Phase 2, which starts from a `main` that holds v2, removes the v1 path, and a test then
requires the base to be v2.

### The page

**One page, two views** ([Decision 3](#decisions)). `news.html` carries **Notable
stories**, the stories as now, and **All changes by PR**, the feed.
A toggle at the top switches between them in place.

**The toggle’s look and position: the Film | Workbench tabs.** The owner asked for the
toggle “much like we had a while back in the history, where there was a Film | Workbench
toggle” (point 6). It takes that strip’s element, look and place:

- `news_page` passes `tabs=news_view_tabs()` to `kpress_page`, which puts the strip
  after the navigation bar in the header slot, where `visualize_tabs` put the Film |
  Workbench strip (d73244ff4).
- The strip is the same element, a `<nav class="site-tabs" aria-label="News views">` of
  two links, “Notable stories” and “All changes by PR”. `site-nav.css` therefore draws
  it as it drew Film | Workbench: `nav.site-tabs a` for each tab, `a + a` for the
  divider, and the tinted fill for the current tab.
- The header hands its rule to the bar, the strip stands `--site-tabs-space` (0.7rem)
  under the rule, and the page’s title starts `--site-page-top` under the strip, all by
  the rules 12a0a8438 added.
  None of those rules changes, and print and the embed view still hide the strip.

**The toggle’s behaviour: a tablist that switches in place**, as the atlas’s Grid |
Triangle tablist does:

- **In the first response**, the two links point at the two views’ sections on the same
  page, `#news-stories` and `#news-changes`, with “Notable stories” marked
  `aria-current="page"`.
- **A new script, `overview/news-views.js`, turns the strip into a tablist.** It sets
  `role="tablist"` on the strip, `role="tab"`, `aria-selected` and `aria-controls` on
  each link, and `role="tabpanel"` with `aria-labelledby` on each view’s section.
  ARIA in HTML allows `tablist` on `nav` and `tab` on `a[href]`, as review A of #759
  checked. Only the selected tab is in the tab order.
  The Left and Right arrows (wrapping), Home and End move between the tabs and select,
  as `atlas-view.js` does, and a click or Enter selects.
  The style is unchanged, because `site-nav.css` gives
  `[role="tab"][aria-selected="true"]` the same fill as `a[aria-current="page"]`. The
  script removes `aria-current` from the strip’s links when it enhances them: left on
  “Notable stories”, it would keep that tab filled by `site-nav.css:493` while the feed
  is selected, and both tabs would show the fill.
- **Each tab’s `href` becomes its view’s own address**, so opening a tab in a new window
  or copying its link gives that view.
  The view can be bookmarked and shared, as Film and Workbench could.

**The view in the URL.** `news-view=changes` selects the feed; no parameter means the
stories.

- **Not `view`:** `overview/embed.js` already reads `?view=embed`. The atlas keeps its
  own parameter, `?atlas=grid`, in the same way.
- **Not a fragment:** fragments already address stories (each card’s anchor), legacy
  bookmarks (`news-forward.js`) and now rows (`#pr-706`). A fragment that names a row
  selects the feed, as a bookmarked card widens News’s filters today.
- **History:** switching views pushes a history entry, and Back restores the view.
- **No flash on load:** when an address opens on the feed, `embed.js`, the head
  bootstrap every page carries, which already sets `data-site-atlas-view` from `?atlas=`
  on `atlas.html`, sets `data-site-news-view` from `news-view` or a `#pr-` fragment on
  the News pages. `site.css` hides the other view under that attribute before first
  paint, so the page neither flashes the stories nor shifts.

**Filters and `news-s`.** Each view keeps its own filter:

- **The stories:** their significance buttons (S3 to S5, opening on S4 and S5) and
  topics.
- **The feed:** S1 to S5, “Not scored” and an **All** button, opening on S3, S4 and S5.

`news-s` in the address is the selected view’s choice, as it is News’s today, and no
`news-s` means that view’s default.
Each view remembers its choice during the visit, and switching views writes the newly
selected view’s choice into the address.

`news-filters.js` today binds one filter block to one list through `querySelector`.
Phase 2 runs it once per view, scoped to that view’s panel, and only the selected view’s
instance writes the address.
#736’s change, opening on the levels the markup presses, gives each instance its own
default.

**Without JavaScript**, both views show, stacked:

- the stories first, then the feed under its heading;
- every card and row visible, by the `@media (scripting: none)` rule News uses for its
  cards, extended to the rows;
- the filter bars hidden;
- the strip working as in-page links that jump to the two sections, the second being the
  link to the feed.

`news-view` cannot act without scripts, so a shared feed address opens on the stories,
with the strip’s second link one step away.

**Accessibility.**

- The tablist pattern above, with each panel labelled by its tab.
- The filters are the existing fieldsets with their hidden legends and `aria-pressed`
  buttons, and each view’s live count keeps `role="status"`.
- Hidden rows and the unselected panel use `hidden` or `display: none`, so assistive
  technology skips them as sighted readers do.
- Each badge carries `aria-label="Significance S3 of 5"`, “Significance S3 of 5, scored
  from its results”, or “Not scored”.
- Each row is an `<li id="pr-706">` in an `<ol>`, so a story, a profile or a reader can
  link a row.

**A feed row, in words.** Rows are grouped under date headings, newest first.

- **An S3+ row** shows, in order:
  - the merge date;
  - the significance meter News cards and results use
    (`overview_sections.significance_mark`: the “S3” text beside five bars, with the
    rubric’s short meaning as its tooltip);
  - the story’s title, linked to the story, or the pull request’s title for a row scored
    from its results, which owes no story;
  - under it, in the quieter `site-news-records sans-text` style, “#706” linked to the
    pull request on GitHub, then the pull request’s title;
  - the results, as “Raises T-223 · Adopts T-223 at 204 and 260”, each id linked to its
    result page;
  - the people, as “Couzo · reported by Couzo”, deduplicated, each linked to the
    profile.
- **An S1, S2 or unscored row** is one line: the date, the compact badge (the meter’s
  “S2” text without the bars), the pull request’s title linked to GitHub, and any
  results and people, in the quieter style.
  A row scored from its results says so in the quieter line, as “scored from T-019”.

**The clear label.** The badge is the one significance mark the site already uses on
stories and results, so an S3 change looks the same everywhere.
Its text names the level for readers who do not read bars, and the filter buttons carry
the rubric’s meanings (`render_changelog.news_significance_meanings`). The meter’s bars
cost about 500 bytes, so routine rows get the text alone.

**The feed’s cap.** `news.html` carries the newest feed rows up to 200,000 bytes, whole
rows only, newest first: about 420 rows, or about a month at October’s 13.7 merges a
day. Stories have no cap ([Decision 6](#decisions)); the whole page’s budget is under
[The page budget](#the-page-budget).
Feed rows are not yet rendered, so they are taken as about 1,600 bytes for an S3+ row
and 350 for a routine row, about 475 on average.

**Older rows go to half-month archive pages.** `news/YYYY-MM-01.html` holds the rows
merged on days 1 to 15, and `news/YYYY-MM-16.html` the rows merged from the 16th to the
month’s end.

- **The feed only.** An archive page carries the header strip, the feed’s filter and
  every row of its half month, including rows still on `news.html`. On it, “All changes
  by PR” is the current tab and “Notable stories” is a link to `news.html`, as the Film
  and Workbench tabs linked two pages.
- **Stable addresses.** A merge date alone decides a row’s archive page, so the address
  never changes.
- **Sizes**, estimated with the row figures above: 1 to 15 October, the busiest half
  month so far, holds 219 rows, about 142,000 bytes with the shell, under the
  600,000-byte `page` budget.
- **Headroom.** A test fails any archive page above 560,000 bytes, which a half month
  reaches at about five times October’s pace, and the failing test names the follow-up:
  weekly pages.
- **Navigation.** The feed on `news.html` ends with links to the archive pages (“Earlier
  changes: 1–15 October 2026 · 16–30 September 2026 · …”). Each archive page is a row of
  `site-urls.yaml`, derived from the pages the renderer declares and written by
  `python -m devtools.site_urls --write`, as every generated page is.

**Links that outlive the cap.** Stories never move, so every link to a story keeps its
`news.html` address: the home page’s News box, Related News on profiles, replies posted
on issues and readers’ bookmarks.
Rows move, and one function, `row_location(row)`, gives each row its page:

- **Profiles’ Pull Requests lists** link a row’s archive page, which never moves.
- **Old links to a row** that has left `news.html`, such as `news.html#pr-706`, are
  forwarded by `news-forward.js` when the fragment is not on the page.
  It reads a static map, `news/anchors.json`, from each such row anchor to its archive
  page, about 50 bytes a row and fetched only on such a miss.
  Without scripts such a link opens `news.html` at the top.

**Why not the alternatives.**

- **A static data file for older rows** needs a second renderer in the browser that
  matches the Python one, and readers without scripts and search engines would not see
  older rows.
- **Archive pages for stories too**, which this plan recommended, would keep `news.html`
  under today’s budget.
  The owner chose to keep every story on the page ([Decision 6](#decisions)).

**The header checks cover the strip.** The strip is a `nav.site-tabs` child of the
header slot, the element `preview_site/header` already finds
(`header?.querySelector("nav.site-tabs")`), so the existing checks apply unchanged:

- `tabs_problems` holds it below the rule: the tabs start at or below the rule’s foot,
  and the content starts at or below the tabs’ foot.
- `measure_site_pages header` reports it.
- `preview_site --shots` fails a page whose tabs start over the rule.

Phase 2 makes two small changes:

- The probe reads the current tab from `[aria-current="page"]` only, so it also reads
  `[aria-selected="true"]`, for a strip the script has enhanced.
- `test_site_wide_blocks.py` adds `news.html` and one archive page to the pages it holds
  to the rule in Chromium at 1280 and 390: “Notable stories” current on `news.html` and
  “All changes by PR” on the archive page, the strip `--site-tabs-space` under the rule,
  and the title `--site-page-top` under the strip.

**How this fits with #736.** #736 is open.
Asked whether to take it over, the owner selected “Take it over (Recommended)” and
added: “Review carefully and make sure it’s a strict improvement that we can land.
And that it’s compatible with the other design choices we’ve made”.
On that answer another lane is taking #736 over from the site agent and bringing it up
to current `main`; Phase 2 still waits for it to merge.
#736 makes these changes:

- it adds `NEWS_FLOOR` and `NEWS_LEVELS`;
- it moves the significance buttons into `news_significance_filter(selected)`;
- it adds the home box’s compact filter and `data-news-limit`;
- it makes `news-filters.js` open on the levels its markup presses;
- it adds `stamp_landed`’s `landings.yaml`.

Phase 2 starts from `main` after #736 merges and builds on it:

- `news_significance_filter` gains a `levels` argument that defaults to
  `range(NEWS_FLOOR, 6)`, so the stories and the home box render as #736 leaves them,
  and the feed passes S1 to S5.
- The feed’s S3+ default is pressed in markup, which #736’s script already honours; the
  script gains per-view instances, the **All** button and “Not scored”.
- The strip is drawn only on `news.html` and its archive pages, never in the home box.
- The home box does not change: its stories stay on `news.html`.
- `news_highlights.py`’s selection, the compact filter, `stamp_landed.py` and
  `landings.yaml` are untouched.

The budget raise and Phase 1 change no page.
Their edits to `render_changelog.py` (`validate`, the gates, `load`) and to
`result-import.md` meet #736’s only as text merges, and whichever lands second merges
`main`.

**Checks that stay green**, run in Phase 2:

- the browser floor (`packing-validate --only "browser floor"`: Biome, `tsc` and the
  type-aware ESLint rules) for `news-views.js`, `news-filters.js`, `news-forward.js`,
  `embed.js` and any probe;
- `packing-validate --only "browser code lives in files"`;
- `site_urls --check --history-ref origin/main`, for the new rows and every page budget;
- `test_changelog.py`, `test_changelog_publication.py`, `test_news_highlights.py`,
  `test_site_homepage.py` (its News facet tests drive Chromium),
  `test_site_wide_blocks.py`, `test_site_preview_checks.py`,
  `test_render_contributors.py`, `test_overview.py` and `test_site_navigation.py`;
- `check_published_site` after the deploy.

`workbench_tools.check_frontend` builds and drives the workbench page only, so it is
unaffected; it runs in the full gate as always.

### The page budget

**Every story stays on `news.html`** ([Decision 6](#decisions)), so the page outgrows
the 600,000-byte `page` budget and needs a measured exception of its own.
Only feed rows leave it, for the archive pages above.

**Expected size**, re-taken from the deployed page on 24 October: 318,655 bytes over 50
stories, 34,414 of them outside the cards.
The 14 cards added since 23 October average about 6,800 bytes against 5,685 for all 50,
so the projection takes about 6,000 bytes a story.
At October’s 2.4 S3+ merges a day, one story each, the page gains about 14,400 bytes a
day. Phase 2 adds about 204,000 bytes at once: the feed’s 200,000-byte cap and about
4,000 for the strip, the feed’s filter and the archive links.

| `news.html` | Days from 24 October, stories only | With Phase 2’s feed | What it is |
| --- | --- | --- | --- |
| 318,655 bytes | today |  | 50 stories, deployed |
| 450,000 | about 9 |  | the raise must have merged by then ([When the raise lands](#the-page-budget)) |
| 600,000 | about 19 |  | today’s `page` budget; `check_published_site` fails each follow-up that adds a story past it |
| 1,150,000 | about 58 | about 44 | the trip point below: about 189 stories, or about 155 beside the feed |
| 1,300,000 | about 68 | about 54 | the proposed budget: about 214 stories, or about 180 beside the feed |

At 6,800 bytes a story, the pace of the newest cards, each day count is about an eighth
shorter: `page`’s 600,000 bytes about 17 days away and the trip point about 51.

**The measurement, before the budget moves.** One retained tool,
`devtools.measure_news_page`, takes the measurement, as
[OR-1](../../../../operating-rules.md#or-1-build-the-tool-never-leave-a-measurement-in-one-off-code)
requires. Its report goes into the pull request that raises the budget, and its figures
into the exception’s reason.
It measures two pages, both built by the site’s own renderer:

- **today’s `news.html`**, as `main` renders it when the raise is made;
- **a projected `news.html` at the proposed budget**, 1,300,000 bytes: the real stories
  repeated in date order under new ids and anchors until the page reaches that size,
  with the feed at its full cap once Phase 2 has a feed.
  Built from the page’s own cards, the projection carries the markup readers will get.

Its modes, from `packing/`:
- **`bytes PAGE...`** needs no browser.
  For each page it reports:
  - the raw bytes;
  - the gzip bytes at level 6, the level `preview_site.serve` uses; GitHub Pages sent
    gzip on 23 and 24 October, though not at level 6 (43,345 bytes on 24 October for a
    page level 6 compresses to 41,988);
  - given a deployed address, the raw bytes and the gzip transfer size the site sends;
  - the brotli bytes at quality 11, through the `brotli` module the environment already
    has from `fonttools[woff]`, for reference only, since GitHub Pages answered a
    brotli-only request with the uncompressed page;
  - the stories’, rows’ and shell’s shares, and the 90th-percentile story;
  - the days of room left before the trip point, at the last 28 days’ story pace.
- **`project BYTES --out DIR`** writes the projected page into a built site directory,
  beside its shared assets.
- **`load DIR`** measures each page’s load in Chromium:
  - `check_site_rendering DIR --page news.html --runs 3`, its protocol unchanged: a
    fresh context at 1280 and 390 px, light and dark, served gzipped from a local
    server; CLS, LCP, longest task and blocking time, and the separate no-JS readability
    context;
  - `measure_site_pages load DIR --page news.html --runs 3`, its protocol unchanged,
    unthrottled and with `--network slow-4g`: DOMContentLoaded, load, first contentful
    paint, and the bytes the load moved;
  - parse and render time: Chromium’s main-thread counters at load, through the DevTools
    protocol’s `Performance.getMetrics` (`ScriptDuration`, `LayoutDuration`,
    `RecalcStyleDuration` and `LayoutCount`), read as `measure_atlas_views move` reads
    them, and the `ParseHTML` total from one `check_site_rendering --trace` navigation,
    recorded as a diagnostic with no gate credit.
- **`switch DIR`** times the in-place tab switch on Phase 2’s page, at its launch size
  and at the projected size, at 1280 and 390 px, by click and by arrow key, five runs of
  each path. For each it reports the handler’s time, the time to the next frame, any long
  task, the same counters over the change (`LayoutCount` among them), and the
  long-animation-frame `forcedStyleAndLayoutDuration` of each script, which
  `check_site_rendering`’s probe already records
  (`probes/check_site_rendering/instrument.js:126-137`). Its page code is a probe file
  under `probes/measure_news_page/`, loaded with `sqpack.probes.probe`. The paths:
  - from the default view to the feed and back;
  - **an address that opens on the feed (`news-view=changes`), then a switch to the
    stories.** This is the expensive path.
    The stories’ panel is hidden before first paint, so `news-cards.js` enhances none of
    its cards at load: `refresh` returns while a card has no box (`news-cards.js:48`),
    and each card’s `previousWidth` is recorded as 0 (`:95`). On the first switch to the
    stories every card’s `ResizeObserver` sees its width change and runs `refresh`
    (`:96-100`), which collapses the card and reads `getComputedStyle(body).lineHeight`
    and `body.scrollHeight`, one card after another.

The budget may move when both pages pass:

- every `check_site_rendering` limit, unchanged (CLS 0.1, LCP 4,000 ms, longest task 300
  ms, blocking 600 ms), on the median of three runs, with the no-JS page readable;
- a tab switch that paints its next frame within 200 ms of the press, the median of five
  runs at 390 px on each path above, the first reveal of the stories included, with no
  long task above the site’s 300 ms limit; 200 ms is the “good” bound of the web’s
  Interaction to Next Paint measure.

The raise lands before Phase 2 has a switch, so it is held to the load limits alone;
Phase 2 adds the switch limit and re-runs `load` on its page with the feed.

Transfer size has no limit of its own; the measured gzip and brotli bytes go into the
exception’s reason. Timings taken on the shared host are advisory, as `results.html`’s
exception says of its own, and shared CI keeps timing report-only
(`--timing-mode report-only`, `think-9dhb`). The report names the host, the Chromium
version and the runs.
The run is estimated, not measured, at a few CPU-minutes: about 80 navigations.

If the projected page fails a limit, the tool measures a projection at 1,000,000 bytes,
and the budget is the larger size that passes, with its trip point 150,000 bytes below
it. If 1,000,000 fails too, the raise stops and the report goes to the owner.

**The proposed budget: 1,300,000 bytes.** The budget, the 150,000-byte trip margin, the
feed’s 200,000-byte cap and the half-month split of rows are this plan’s proposals, not
the owner’s choices.
The owner chose only “Keep all, raise the limit” ([Decision 6](#decisions)); the
measurement confirms the budget, and all four stay proposals until the owner confirms
them. 1,300,000 bytes is proposed, if the measurement passes, for four reasons:

- The site already serves a page that size.
  `results.html` is 1,303,283 bytes deployed, and its exception records three-run checks
  passing at 1,324,108. News prose compresses less than that table does: 7.4 to 1 on 24
  October against 15 to 1. If that ratio holds, News at 1,300,000 bytes sends about
  177,000 gzipped bytes, about twice what `results.html` sends, so the measurement
  settles the budget and the precedent only suggests it.
- It is the size the coordinator’s option text gave as an illustration of runway (“even
  1.3 MB, the largest exception any page has, would last about 86 days”), not as a
  proposed budget, and the plan keeps it because the first reason holds.
- It leaves 700,000 bytes under the 2,000,000-byte hard limit every HTML file has, room
  for one more measured raise if the owner chooses one later.
- From today’s page, at October’s pace, it lasts about 68 days, or about 54 once Phase
  2’s feed is on the page, and the check below trips about 10 days before it.

**Where it is set.**

- `site_urls.PAGE_BUDGET_EXCEPTIONS["news.html"] = (1_300_000, reason)`. The reason
  states the measured raw, gzip and brotli bytes, the timings at both sizes and their
  date, the trip point, and the bead that owns the runway.
  `validate_registry` already requires an exception to sit within the hard limit and to
  give a reason.
- `docs/project/site-urls.md`, re-rendered by `python -m devtools.site_urls --write`,
  lists it under Measured exceptions.
- `render_changelog` holds the two figures, `NEWS_CEILING = 1_300_000` and
  `NEWS_TRIP_BYTES = 1_150_000`, beside the announcement gate, and a test in
  `test_changelog_publication.py` requires the exception to equal `NEWS_CEILING`, as
  `test_overview.py`’s `PAGE_CEILINGS` does for `index.html` and `results.html`.
- `check_published_site` needs no change.
  It reads `page_budget(row)`, so the Pages workflow refuses to deploy a `news.html`
  above 1,300,000 bytes, and the check of the deployed site reports one.
- The archive pages are ordinary `page` rows under the 600,000-byte default, with no
  exception.

**The check that trips first.** The trip check renders `news.html` through
`render_overview.news_page` and compares its bytes with `NEWS_TRIP_BYTES`, 150,000 bytes
under the budget, about 10 days of stories at October’s pace.
It prints the page’s bytes, the trip point, the budget and the days of room left at the
last 28 days’ pace, as the results page’s runway test prints its projection.
This is the shape
[OR-17](../../../../operating-rules.md#or-17-every-routine-gate-has-a-wall-ceiling-and-anything-above-it-is-selected-on-purpose)
gives a gate’s wall time: a ceiling, and anything above it selected on purpose, with the
record saying who selected it.

- **Where it runs, and its scope.** It runs inside `render_changelog --check`, in the
  records-tier step that runs the announcement gate, and takes that gate’s
  `--announcement-base`. Its scope is decided by file path, as that gate’s is:
  `edits_announcement_records` runs `git diff --name-only BASE -- PATHS` against the
  merge base (`render_changelog.py:973-975`), and the trip check runs the same diff over
  its own list. It fails a change that edits one of these files:
  - `packing/site-changelog.yaml`;
  - `packing/pull-requests.yaml`, once Phase 1 adds it;
  - `packing/devtools/render_changelog.py`, which renders the stories;
  - `packing/devtools/templates/news-article.md`, the News page’s template;
  - `packing/devtools/render_pr_feed.py`, the feed renderer, once Phase 2 adds it.

  `packing/devtools/render_overview.py` is outside the failing scope.
  `news_page` is one function in it, and the module renders every other page as well, so
  a scope that held it would fail every change to an overview page once `main` is past
  the point. A change to `news_page` gets the warning, as a header change does.
  The check warns on any other change, and only warns on `main` (`--announcement-base
  HEAD^1`), where a merged change can no longer act.
  A pull request that cannot change the page’s stories does not go red because `main`
  crossed. Its fail, warn and main-only-warn cases are tested in the quick lane on
  fixture pages.

- **It holds against `main` plus the change.** For a pull request, CI checks out
  GitHub’s merge of the branch onto `main` (`refs/pull/N/merge`), so the page it
  measures is `main`’s stories with the change’s added.
  That still leaves a race: two follow-ups can each pass against a `main` that lacks the
  other, and together cross the trip point once both merge.
  So a change in the failing scope merges only on a check run against the `main` it
  merges into: when `main` has moved since the run, the branch merges `main` and the
  check runs again before the merge.
  The coordinator, who merges every follow-up, applies this at Record the merge and at
  the merge step, and the runbook says so.

- **Anything else that grows the page.** A change outside the scope can still add bytes,
  a header change on every page for example.
  It gets the warning, and the hard limit stays where it is: `check_published_site`
  refuses to deploy a `news.html` above the budget.

**At the trip point, recording S3+ merges stops.** There the story gate and the trip
check conflict. The follow-up that records an S3+ merge must carry its story, and the
story is what carries the page past the trip point, so the check refuses it;
`STORY_EXEMPT` may only shrink, so it offers no way round.
No S3+ row can be recorded, and the sweep lists each such merge as needing action.

**Past the trip point, every change in the failing scope fails.** While `main`’s page is
under the point, an S1 or S2 merge is still recorded, since its row enters a feed whose
cap is fixed. But the check fails a change in its scope whenever the page it renders is
at or over the point, whatever the change did to the page, and `main` can pass the point
without the check refusing anything: through a change outside the scope, which only
warns, or through a hand merge, which the re-run rule does not reach.
From then on every follow-up fails, since from Phase 1 on each one edits
`pull-requests.yaml`. Recording S1 and S2 merges stops too, and so does a story edit
that shrinks the page but leaves it over the point.
A change in the scope passes again only when the page it renders is under the point, as
after a raise of the budget or a smaller feed cap.

**The owner chooses what happens before the page gets there.** The plan builds nothing
for the trip point itself.
When the page comes within 432,000 bytes of the trip point, the coordinator’s `decision`
bead ([Process](#process)) states that recording S3+ merges stops at the trip point and
that past it every change in the failing scope fails, S1 and S2 recording included.
It puts these options to the owner; none of them runs automatically:

- raise the budget again, after the same measurement at the new size, up to the
  2,000,000-byte hard limit;
- shrink the feed’s cap on `news.html`, whose 200,000 bytes are about 14 days of
  stories;
- move older stories to dated archive pages, the design this plan drafted and the owner
  did not take on 23 October;
- shorten the cards on `news.html`, a card design the site agent owns;
- let recording S3+ merges pause at the trip point until a later step lands, with each
  paused merge listed by the sweep;
- another step the owner names.

The step the owner chooses lands before the page reaches the trip point, so recording
does not stop unless the owner chose that.

**What keeps the page cheap to load at that size.**

- **Static stories.** The renderer writes every story as HTML at build time.
  No script builds, fetches or re-renders a card, so a reader without scripts gets the
  whole page, which the no-JS check holds.
  Formulas arrive as prepared MathML (90 `<math>` elements on 24 October), and the page
  loads no math script.
- **Small scripts that only switch state.** `news-filters.js` (164 lines) sets `hidden`
  on cards and rows. `news-views.js` sets one attribute on the root and the tablist’s
  ARIA states, and `site.css` hides the other view.
  Neither creates, moves or re-renders markup, so a switch parses nothing.
  The first reveal of the stories on a page opened on the feed costs more than a style
  change: it runs `news-cards.js`’s `refresh` on every card (below).
- **Cached shared files.** Styles, scripts and fonts are content-hashed files under
  `assets/`, cached across pages, so only the HTML grows.
- **Lazy images.** News has none today (no `<img>` on 23 October).
  A story that adds one sets `loading="lazy"`, `decoding="async"` and its `width` and
  `height`, so the image loads near the viewport and holds its box, and a renderer test
  holds every `<img>` on a News page to that.
- **A capped feed.** Rows past 200,000 bytes go to the archive pages, so the feed’s
  share stays fixed while the stories grow.
- **One cost to watch, read from the code and not measured.** `news-cards.js` collapses
  each card and then reads its `scrollHeight`, one card at a time, so each card can
  force a layout before the next.
  It does so on three paths: at load (`news-cards.js:94`), from each card’s
  `ResizeObserver` when its width changes (`:96-100`), which on a page opened on the
  feed is every card at the first switch to the stories, and on every `news:filter`
  event (`:117-122`). The `load` and `switch` modes’ `LayoutCount`,
  `forcedStyleAndLayoutDuration` and longest task show whether that cost grows with the
  story count. If it does, Phase 2 batches all three paths: every card’s height is read
  before any card collapses, and the observers’ callbacks are gathered into one such
  pass per frame.

**When the raise lands: before Phase 1, as its own pull request.** On 24 October the
deployed `news.html` was 318,655 bytes over 50 stories, and at about 14,400 bytes a day
it reaches the 600,000-byte `page` budget in about 19 days.
Then `check_published_site` fails each follow-up that adds a story.
Phase 1 is a larger change, a record migration and a gate, and needs its own correctness
review, so the raise does not wait for it.

- **Its trigger is a size, not a date.** The raise is the next News work after this plan
  merges, and it must merge before `main`’s `news.html` passes 450,000 bytes, about 9
  days away at that pace and about 10 days short of the `page` budget.
- **Who watches it.** Until the raise merges, the coordinator reads the rendered page’s
  bytes in each follow-up that lands a story.
  If `main`’s page passes 450,000 bytes with the raise unmerged, the coordinator opens a
  `decision` bead for the owner in the follow-up that reads it, ahead of the
  600,000-byte failure.
- **What it carries.** `devtools.measure_news_page` with its `bytes`, `project` and
  `load` modes; the measurement at today’s size and at the projected size, stories only;
  the exception and its reason; `NEWS_CEILING`, `NEWS_TRIP_BYTES` and the trip check;
  and the room report in the follow-up that lands a story.
- **What Phase 2 adds.** The `switch` mode and its probe, and the `load` and `switch`
  measurements of its own page with the feed at its cap, at launch size and at the
  projected size. Phase 2 does not merge if its page fails the limits the raise was set
  on.

The raise changes no visual, site template, style or browser script.

### Profiles

Each profile gains a **Pull Requests** section after Related News: newest first, one
line per pull request whose feed row names the person, with the date, the badge, the
story’s title (or the pull request’s title) linked, the role (“results”, “credited”,
“reported” or “pull request by”), and a link to the row on its archive page.
It uses the same `result_people` derivation as the feed, so a profile and the feed
cannot disagree, and the folding `_work_listing` already applies to long lists.

## Implementation Plan

### Before Phase 1: The Budget Raise

One pull request, the next News work after this plan merges, and merged before `main`’s
`news.html` passes 450,000 bytes ([When the raise lands](#the-page-budget)).

- [x] `devtools.measure_news_page`, with its `bytes`, `project` and `load` modes.
- [x] Its report at today’s size and at the projected 1,300,000 bytes, stories only, in
  the pull request.
- [ ] `PAGE_BUDGET_EXCEPTIONS["news.html"]` with its measured reason, and
  `docs/project/site-urls.md` re-rendered.
- [ ] `NEWS_CEILING`, `NEWS_TRIP_BYTES` and the trip check in
  `render_changelog --check`, with its scopes.
- [ ] The room report in the follow-up that lands a story, and the merge-step rule that
  a change in the trip check’s failing scope is checked against the `main` it merges
  into, in the runbook.
- [ ] Tests, as the Testing Strategy says.

**24 October 2026:** the tool and its report landed on their own, with the budget
unchanged. The measurement failed `check_site_rendering`’s load limits at all three
sizes, today’s 318,950 bytes, about 1,000,000 and about 1,300,000. Both failures come
from the News scripts’ work at load, not from the page’s bytes alone:

- **A layout shift above 0.1, present at today’s size.** `news-cards.js` folds the first
  visible card after the first paint, a shift of about 0.09 at 1280 px and 0.34 to 0.35
  at 390 px. When `news-filters.js` then reveals the filter bar (`news-filters.js:160`),
  the stories move again, by 0.02 at 1280 px and 0.06 at 390 px.
  At 1280 px each shift alone stays under 0.1, and together they pass it.
- **A longest task past 300 ms at about 1,300,000 bytes.** `news-cards.js`’s `refresh`
  forces two layouts for each visible card, one card after another: 31 layouts at load
  today, 81 at about 1,000,000 bytes and 106 at about 1,300,000. This is the One cost to
  watch above, and it grows with the story count.
  The 1,305,949-byte page without `news-cards.js` passed every limit, its longest task
  at most 144 ms, and without `news-filters.js` it still failed the longest task
  (`measure_news_page project --without`, #788).

The raise waits on the owner’s decision `think-lsam`. Its first option is to fold the
cards before the first paint and read every card’s height before writing any, then
measure again.

### Phase 1: The Record, Its Tool, the Backfill and the Gate

One pull request. `think-4oj0`’s stories merged with #758 on 24 October, and every S3+
pull request then had a story, so `STORY_EXEMPT` starts empty.

- [ ] `packing/pull-requests.schema.yaml` and the offline module
  `devtools.pull_request_record`: load, validate, and the derivations the gates need,
  scores from results among them.
- [ ] `devtools.record_pull_requests`, with its listing, `--apply`, `--pr` and `--audit`
  modes, and its per-pull-request split of a shared or carried merge’s registrations,
  raises and adoptions, a carried pull request measured from the base side.
- [ ] Run the backfill: `--apply` over every merged pull request.
  Move every `deliveries` row and the 3 `stacks` out of `site-changelog.yaml` and check
  that they agree with their rows.
  List each shared-merge group and carried pull request in the evidence, with the
  results each row took, and for each refused group, 306ae9fab among them, the reviewed
  owner of each id.
- [ ] `render_changelog`: `SiteChangelog/v2`, with its coverage rule and the optional
  `pull_request_summaries`; entries checked against the record; `STORY_EXEMPT`; the
  story gate, with its `result_ids` rule for rows numbered above this pull request; the
  label floor; the freeze check accepting v1 or v2 from the base; `CHANGELOG.md`
  re-rendered and unchanged.
- [ ] `import_changelog`: merge facts from the record; the drafted `## News` entry from
  the description.
- [ ] `intake_sweep`: the Merged pull requests section, and the audit in `--offline`.
- [ ] `validate_schemas`’ corpus, the two steps’ `known_inputs`, and
  `release.validate_release_impacts` with whatever `check_release_impact` asks.
- [ ] Every runbook, `development.md`, `ANNOUNCED_FROM` and template passage that
  [Process](#process) lists.
- [ ] Tests, as the Testing Strategy says.

### Phase 2: The Toggle, the Feed, the Archives and the Profile Lists

One pull request, after #736 and Phase 1 merge.
The intake session builds it, as the coordinator reads the owner’s answer
([Decision 4](#decisions)). Phase 2 changes templates, styles and browser scripts, work
the owner’s 23 October scope rule kept out of that intake pass: “The scope of all of
your work is intake only.
Don’t change things on the site that are unrelated visuals.
Those are handled by the other agent.”
The owner’s answer to who builds the page part, “Me, with the records (Recommended)”
(point 4), is what places Phase 2 with the intake session despite that rule.

- [ ] `site_tallies.result_people(record)`, public, shared by the feed and the profiles.
- [ ] The feed view and its cap in `render_news`, through a feed renderer
  `devtools.render_pr_feed`; `row_location`; the half-month archive pages of rows in
  `render_overview`’s page table and `site-urls.yaml`; the archive links; and
  `news/anchors.json`, with its own `site-urls.yaml` row, since `check_published_site`
  fails a file it does not expect.
  The trip check’s failing scope gains `render_pr_feed.py`.
- [ ] The switch measurement, as [The page budget](#the-page-budget) says:
  `measure_news_page switch` and its probe, and the `load` and `switch` report on this
  pull request’s page with the feed at its cap, at launch size and at the projected
  size.
- [ ] `news-cards.js`: every card’s height read before any card collapses, on load, on
  the `ResizeObserver` path and on `news:filter`, if the measurement shows that work
  growing with the story count or the first reveal of the stories missing the switch
  limit.
- [ ] `news_view_tabs()`, passed to `kpress_page(tabs=…)` for `news.html` and every
  archive page; `news_significance_filter(levels)`.
- [ ] `overview/news-views.js` (new): the tablist, `aria-current` removed from the
  enhanced strip, the `news-view` address and history.
- [ ] `overview/embed.js`: `data-site-news-view` from `news-view` or a `#pr-` fragment.
- [ ] `news-filters.js`: one instance per view, the **All** button and “Not scored”.
- [ ] `news-forward.js`: the `news/anchors.json` lookup on a missed fragment.
- [ ] `devtools.check_site_scripts`’ inventory: an entry for `news-views.js`, and
  `news-forward.js`’s entry, today “registered-forwarder: Forward only retained About
  history anchors…” (`check_site_scripts.py:54`), rewritten for a script that also
  fetches `news/anchors.json`.
- [ ] `site.css`: the feed row, hiding the unselected view under `data-site-news-view`,
  and the `scripting: none` rule for rows.
- [ ] The header probe’s `[aria-selected="true"]`, and `news.html` and an archive page
  in `test_site_wide_blocks.py`.
- [ ] The profiles’ Pull Requests section.
- [ ] `validate_previous_ref`’s v1 path removed.
- [ ] Tests and browser probes, as the Testing Strategy says.
- [ ] If Phase 2 is labelled S3 or higher, as a new public capability is likely to be,
  its own story lands in the follow-up after its merge, through the step Phase 1 adds.

## Testing Strategy

**The budget raise**, from `packing/`, in `test_changelog_publication.py`,
`test_changelog.py` and a new `tests/test_measure_news_page.py`:

- `PAGE_BUDGET_EXCEPTIONS["news.html"]` equals `NEWS_CEILING`, and `NEWS_TRIP_BYTES` is
  below it;
- the trip check on fixture pages: a page at the trip point fails a change that edits
  `site-changelog.yaml`, `render_changelog.py` or `news-article.md`, warns a change to
  `render_overview.py` or another file, and only warns on `main`; a page under it passes
  in every case;
- past the trip point: a change that edits `site-changelog.yaml` without adding a story
  fails, and so does one that shortens a story but leaves the page over the point; one
  that brings the page under it passes;
- `measure_news_page bytes` on a fixture page reports the gzip and brotli sizes the
  libraries give, and the days of room that follow from a fixture pace;
- `measure_news_page project` reaches its target within one story’s bytes, from the
  page’s own cards only, with every id and anchor unique.

**Phase 1**, from `packing/`:

- A new `tests/test_pull_requests.py`:
  - the schema accepts the example and refuses each malformed field;
  - a second `--apply` over the same GitHub JSON fixture writes identical bytes;
  - a relabel refreshes `labels`, and a changed merge commit is refused;
  - a fixture repository in the style of `test_changelog.py`’s delivery tests: a merge
    commit off the first-parent line gets the right carrying commit, and a commit that
    never reached `main` is refused;
  - a two-commit fixture register yields `registered` and `raised`, each with its
    `score`, and a two-commit `ADOPTED` table yields `adopted` with its counts;
  - **no row shows another layer’s results**, in
    `test_a_shared_merge_commit_gives_each_layer_only_its_own_results`: a fixture
    repository in which layer 1, based on `main`, registers T-001 and adopts it at a
    count in `ADOPTED`, and layer 2, based on layer 1’s branch, registers T-002 and
    raises T-001; one merge commit on `main` delivers both, and the GitHub fixture gives
    both pull requests that commit as their `mergeCommit`, as GitHub gave d3860c97a to
    11 pull requests. Layer 1’s row holds only T-001 registered and adopted, and layer
    2’s only T-002 registered and T-001 raised, a raise kept although T-001 is new
    against the merge’s first parent;
  - an upper layer that merges `main` after `main` registered an id does not take that
    id, which is not part of the group’s change (rule 5);
  - a pull request merged into its base branch by a merge commit, the shape of 13 of the
    16 carried pull requests on 24 October, keeps the id its own merge registered, and
    the pull request that carried it to `main` does not take that id;
  - #298’s shape: a pull request whose head merges its base branch, which is then
    fast-forwarded to that head, so that GitHub gives the head as its `mergeCommit`, and
    which registered one id and raised another before that merge.
    Its row takes both, measured from its `baseRefOid`, and the pull request that
    carried it takes neither;
  - #336’s shape: a `mergeCommit` that merges the base into the pull request’s branch,
    on a branch that registered an id.
    The row takes that id and none of the ids the merged base brought;
  - a layer that carries a merged pull request, as #661’s branch carries #662 into
    d167d4b86: the carried pull request’s id is its own, and the layer does not take it;
  - refused by name: two pull requests based on `main` that share one merge commit,
    which cannot be ordered; two rows with the same head, as #249 and #258 have; a
    carried merge commit of another shape; and a group whose rows leave an id or an
    adoption of the merge’s change unclaimed;
  - `pull_request_record.validate` fails a record in which two rows register the same id
    or make the same adoption, the invariant that holds the property on the real record
    after the backfill;
  - an unlabelled row takes the highest `score` among its registered or raised results;
  - a listing as long as the limit is refused.
- `test_changelog.py`, extended:
  - an entry naming a pull request the record lacks fails, and an entry’s date comes
    from the record;
  - an S3 row with no story fails a change that edits either record, warns another, and
    warns on `main`;
  - an S4 row named only by an S3 entry fails;
  - a row above the cut-over whose story leaves out an S3+ result it registered fails,
    and a row below it is reported;
  - a row scored from its results owes no story;
  - a stale `STORY_EXEMPT` entry fails;
  - a row labelled S2 that registered a result with `score: 3` fails the label floor,
    and a row labelled S3 that registered it passes;
  - the v2 coverage rule: a coverage number the record lacks fails, a coverage list that
    differs from the represented and omitted pull requests fails, an S2 row with neither
    an entry nor an omission passes, and an S3 row with only an omission fails the story
    gate;
  - a `pull_request_summaries` key the record lacks fails;
  - past the trip point, a change that records only an S2 row fails;
  - the freeze check: a v1 document from the base and a v2 document from the base each
    still freeze entries, the v2 one dated from the base’s `pull-requests.yaml`;
  - the migrated `CHANGELOG.md` renders identically.
- `test_intake_sweep.py`: a gap and an S3+ pull request need action, the trailing S1 is
  listed, and label drift needs action.
- `packing-validate --records`, then `--fast` in CI.
- The backfill’s evidence in the pull request: the row count equals the GitHub count at
  the run, `record_pull_requests --audit` reports nothing, every migrated `deliveries`
  row matches, and each shared-merge group and carried pull request is listed with the
  results each row took.
  For d3860c97a that is #442 T-125 and T-126, #448 T-127, #459 a raise of T-127, #460
  T-128, #463 T-129 and #469 T-130. For 47569ad50 it is #292 T-066 to T-069, and #298
  T-070 to T-079 with its raises of T-048, T-055, T-058, T-059, T-062, T-063, T-064 and
  T-066 to T-069. For d167d4b86 it is #661 T-195 and its adoption at 29, and #676 T-196
  to T-199. 306ae9fab is refused for its equal heads, and the evidence names the row
  that takes T-061.

**Phase 2**:

- Renderer tests:
  - one row per record row, newest first;
  - the feed’s cap keeps whole rows, newest first, within 200,000 bytes, and every
    News-shown story is on `news.html`;
  - the archive pages partition every row by half month, hold no story, and take their
    names from dates alone;
  - `row_location` points at `news.html` within the cap and at the archive page
    otherwise, and `news/anchors.json` holds every row that is off `news.html` and no
    story;
  - every archive page under 560,000 bytes;
  - every `<img>` on a News page lazy, asynchronous and sized;
  - S1, S2 and unscored rows rendered `hidden`, and S3+ rows visible;
  - each badge’s `aria-label`, “scored from its results” included;
  - every story, result and profile link resolving to a page and anchor that exist;
  - the “recorded through” line.
- The switch measurement, in `tests/test_measure_news_page.py`: `measure_news_page
  switch` on a fixture page covers both paths, the first reveal of the stories from an
  address opened on the feed among them, and reports `forcedStyleAndLayoutDuration`.
- Browser tests in `test_site_homepage.py`’s style:
  - the strip’s roles once enhanced: `tablist`, `tab`, `aria-selected`, `aria-controls`
    and `tabpanel`, and no link left with `aria-current`, so only the selected tab is
    filled;
  - only the selected tab is in the tab order, and the arrows, Home and End move and
    select;
  - `news-view=changes` opens on the feed with no layout shift, switching pushes the
    address, and Back restores it;
  - after a page opens on the feed and switches to the stories, each card is collapsed
    or short as on a page opened on the stories;
  - a `#pr-N` fragment selects the feed and reveals its row;
  - `news-s` is kept per view, and **All** selects every level;
  - a link to a row that left `news.html` forwards to its archive page, and a link to
    any story lands on `news.html`;
  - with scripting disabled, both views show, stacked, and the strip’s links jump to
    them.
- The header: `test_site_wide_blocks.py` holds `news.html` and an archive page to
  `tabs_problems` at 1280 and 390, with “Notable stories” current on `news.html` and
  “All changes by PR” on the archive page.
- `test_render_contributors.py`: Evan Daniel’s profile lists #687 for T-220, and a
  person with no result lists none.
- The checks named under The page, `measure_news_page`’s report for the budget, and
  `packing-validate --edit` while editing.

## Rollout Plan

1. The budget raise merges and deploys.
   `measure_news_page bytes`, given the deployed address, reports the deployed page’s
   raw bytes, which equal those of the page `main` rendered at the merge, and its gzip
   transfer size. GitHub Pages’ gzip is not zlib’s level 6: on 24 October it sent 43,345
   bytes for a page level 6 compresses to 41,988, 3.2% more.
   So the transfer size is compared with the level-6 figure in the exception’s reason
   within 5%, and the next follow-up records the deployed figure in the reason beside
   it.
2. Phase 1 merges. From then on the intake runner runs Record the merge after every
   merge, and the sweep reports anything missed.
3. Phase 2 merges and deploys.
   `check_published_site` and a look at `news.html` in both views, at its stacked form
   with scripts off, and at one archive page on the deployed site confirm it.
   The deployed page’s bytes are checked as in step 1.
4. The next follow-up records Phase 2 and lands its story, the first story the new step
   carries.

The News address and its bookmarks keep working: stories never leave `news.html`, a row
that leaves it is forwarded to its archive page, and the archive pages are new.

## Decisions

The owner answered the plan’s questions in conversation on 23 October 2026, and the
coordinator relayed the answers with the option labels quoted below, each exactly as
selected. The text after each label says how the plan follows the answer; it is this
plan’s, except where it names the coordinator or quotes the option text.

1. **S3 results reach News through each pull request’s story.** The owner chose “Via
   each PR’s story (Recommended)”. `ANNOUNCED_FROM` stays 4. From Phase 1 on, every S3+
   pull request’s story names in `result_ids` each S3+ result the pull request registers
   or raises, and the story gate enforces it.
   The 109 S3 results already without a story stay without one, and each appears in the
   feed under its pull request.
   Lowering the result gate to 3, with an exemption list growing from 15 results to 124
   or with 109 stories to write, was not taken.
2. **Pull requests with no S label are scored from their results.** The owner chose
   “Score from their results (Recommended)”. Each takes the score of the strongest
   result it registered or raised, as its row records that score, is marked as scored
   from its results, and owes no story, since it predates the rule.
   One with no label and no result stays “Not scored”.
   Hand-labelling the 352 on GitHub, and leaving them all unscored, were not taken.
3. **One page, switched in place.** The owner chose “One page, switched in place”, not
   the first draft’s two pages joined by links.
   On the toggle’s look the owner added: “We should use a toggle at the top of the page,
   much like we had a while back in the history, where there was a Film | Workbench
   toggle”. [The page](#the-page) follows both: the Film | Workbench strip’s element,
   look and place, switched in place as a tablist.
4. **The feed covers every merged pull request, and the intake session builds the page
   part.** Asked where the feed starts, the owner chose “All merged PRs (Recommended)”.
   This plan reads that as every merged pull request from #1 on, backfilled once, which
   is the tool’s first `--apply`. Asked who builds the page part, the owner chose “Me,
   with the records (Recommended)”. The reading is the coordinator’s, restated on 24
   October: the owner chose that the intake session build the page part along with the
   records. Phase 2 follows it.
5. **The intake runner records each merge.** The owner chose “Intake runner
   (Recommended)”: the intake pass’s runner, its coordinator, records each merge in the
   follow-up it opens for the replies, and the sweep is the backstop.
   The coordinator confirmed the mapping on 23 October: the intake pass’s coordinator
   records each merge in the follow-up it opens for replies.
   A GitHub workflow that opens a pull request for every merge was not taken.
6. **Every story stays on `news.html`, and the page’s budget is raised.** Asked how
   older material should leave the page, the owner chose “Keep all, raise the limit”.
   The option’s description was the coordinator’s question text, not the owner’s words.
   It said that every story stays on `news.html`, that only old feed rows are archived,
   that raising the size limit needs measured load-time checks, and that even 1.3 MB,
   the largest exception any page has, would last about 86 days.
   The 1.3 MB was the option text’s illustration of runway, not a budget the owner set.
   The owner chose only that option.
   The 1,300,000-byte budget, the 150,000-byte trip margin, the feed’s 200,000-byte cap
   and the half-month split of feed rows are this plan’s proposals
   ([The page budget](#the-page-budget)): the measurement confirms the budget, and all
   four stay proposals until the owner confirms them.
   Half-month archive pages for stories, which the plan recommended, and shorter cards
   on `news.html` were not taken.
   Two figures in the question text were off, and the plan uses corrected ones:
   - `index.html`’s 1,300,000 bytes is the third-largest exception, after
     `results.html`’s 1,400,000 and the lower-bounds explainer’s 1,500,000.
   - The 86 days counted the stories alone at 2.2 a day.
     From the page as deployed on 24 October, at October’s 2.4 stories a day of about
     6,000 bytes, 1,300,000 bytes lasts about 68 days, or about 54 with Phase 2’s feed
     on the page.

## Coordinator Defaults

This was not put to the owner.
The coordinator set it, and the owner can overturn it.

- **Routine rows show the GitHub title.** The first draft’s recommendation stands, as
  the coordinator’s default of 23 October.
  An optional feed summary, kept in `site-changelog.yaml`’s `pull_request_summaries`,
  remains for a title worth replacing.

## Open Questions

None. The last one, on the page budget, is [Decision 6](#decisions).

## References

- [`packing/site-changelog.yaml`](../../../../packing/site-changelog.yaml) and
  [`packing/site-changelog.schema.yaml`](../../../../packing/site-changelog.schema.yaml)
- [`packing/devtools/render_changelog.py`](../../../../packing/devtools/render_changelog.py),
  [`packing/devtools/import_changelog.py`](../../../../packing/devtools/import_changelog.py),
  [`packing/devtools/overview/news-filters.js`](../../../../packing/devtools/overview/news-filters.js),
  [`packing/devtools/overview/embed.js`](../../../../packing/devtools/overview/embed.js),
  [`packing/devtools/overview/atlas-view.js`](../../../../packing/devtools/overview/atlas-view.js),
  [`packing/devtools/render_contributors.py`](../../../../packing/devtools/render_contributors.py),
  [`packing/devtools/site_tallies.py`](../../../../packing/devtools/site_tallies.py),
  [`packing/devtools/intake_sweep.py`](../../../../packing/devtools/intake_sweep.py),
  [`packing/devtools/stamp_landed.py`](../../../../packing/devtools/stamp_landed.py),
  [`packing/devtools/site_urls.py`](../../../../packing/devtools/site_urls.py),
  [`packing/devtools/preview_site.py`](../../../../packing/devtools/preview_site.py)
  (`tabs_problems`) and
  [`packing/devtools/probes/preview_site/header.js`](../../../../packing/devtools/probes/preview_site/header.js)
- [`packing/devtools/templates/site-nav.css`](../../../../packing/devtools/templates/site-nav.css)
  (`.site-tabs`)
- The budget and the load checks:
  [`packing/devtools/site_urls.py`](../../../../packing/devtools/site_urls.py)
  (`PAGE_BUDGETS`, `PAGE_BUDGET_EXCEPTIONS`, `HARD_HTML_LIMIT`),
  [`packing/devtools/check_site_rendering.py`](../../../../packing/devtools/check_site_rendering.py),
  [`packing/devtools/measure_site_pages.py`](../../../../packing/devtools/measure_site_pages.py)
  (`load`),
  [`packing/devtools/measure_atlas_views.py`](../../../../packing/devtools/measure_atlas_views.py)
  (`move`),
  [`packing/devtools/overview/news-cards.js`](../../../../packing/devtools/overview/news-cards.js)
  and [`packing/tests/test_overview.py`](../../../../packing/tests/test_overview.py)
  (`PAGE_CEILINGS`, `RESULTS_ROOM_THROUGH`)
- Commits d73244ff4 (30 September 2026, the Film | Workbench tabs), 12a0a8438 (1
  October, the tabs below the bar’s rule) and dd9bfa063 (22 October, the switcher
  retired)
- [The runbook](../../../../packing/campaign/result-import.md): Label the PR and Prepare
  News, Announce a Significant Result, and After the Merge
- [`attribution.md`](../../../../attribution.md) and
  [`packing/campaign/result-requests.yaml`](../../../../packing/campaign/result-requests.yaml)
- [The changelog plan](plan-2026-10-13-site-changelog.md) and
  [the contributor profiles plan](plan-2026-10-10-contributor-profiles.md)
- [The postmortem of 22 October](../../postmortems/postmortem-2026-10-22-results-without-news.md)
- Pull requests [#736](https://github.com/jlevy/squares/pull/736) (home page News box),
  [#744](https://github.com/jlevy/squares/pull/744) and
  [#746](https://github.com/jlevy/squares/pull/746) (atlas)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
