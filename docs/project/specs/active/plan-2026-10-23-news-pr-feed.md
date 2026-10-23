---
title: News Feed of Every Merged Pull Request
description: A committed record of every merged pull request, the tool and gate that keep it, and an in-place News toggle between notable stories and all changes by PR
author: Intake lane c-news-plan-1023, for the repository owner
---
# Feature: News Feed of Every Merged Pull Request

**Date:** 2026-10-23 (last updated 2026-10-23)

**Author:** intake lane `c-news-plan-1023` under coordinator `coord-intake-1023`, for
the repository owner

**Status:** Approved in outline.
The owner answered every open question on 23 October 2026 ([Decisions](#decisions)).

**Tracking:** `think-vph5` (this plan); `think-4oj0` (News stories for the 16 merged S3
pull requests that have none); `think-n51k` (a pull request carrying its own News entry,
which this plan does not do)

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

The plan has two phases, each one pull request that can land on its own: the record, its
tool, the one-time backfill and the gate; then the page, its budget and the profile
lists.

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

4. Asked where the feed starts: “All merged PRs”, from the repository’s start,
   backfilled once. Asked who builds the page part: “Me, with the records”, meaning the
   intake session builds it along with the records.

5. “Let’s plan this out separately and make sure that you have landed the news items in
   parallel that are outstanding first, before we tackle the bigger design problem.
   I don’t want this larger effort to derail anything else that’s able to be landed
   right now.”

6. On the toggle, after reading this plan’s first draft: “We should use a toggle at the
   top of the page, much like we had a while back in the history, where there was a Film
   | Workbench toggle”.

The owner’s answers to the plan’s questions are under [Decisions](#decisions).

Point 5 is why this is a plan.
Two things proceed without it and the plan takes both as given: `think-4oj0` lands News
stories for the 16 merged S3 pull requests that have none, and live intake lanes draft a
News entry in the description of every S3+ pull request they open, which the coordinator
lands after the merge.

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
  `test_overview.py` repeats the two largest page ceilings in `PAGE_CEILINGS` and gives
  `results.html` a fixed runway, `RESULTS_ROOM_THROUGH`.
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
  the answer into a record: it dates each register entry’s `landed`, and its `--audit`
  compares the record with `main`’s first-parent history and gates nothing.
  [OR-18](../../../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob)
  is why: no program depends on Git history to produce its answer.

### Measured on 23 October 2026

The coordinator’s first figures were taken at 05e95db36. Every figure below was re-taken
at 769e441e1 and the record counts again at cc91ee1b8, where they are unchanged; GitHub
and the deployed site were read the same day.
The pace, budget, bytes-sent and timing rows were re-taken at 64b316b6c, with GitHub and
the deployed site read at about 23:00Z.

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
| Changelog entries | 48: S5 4, S4 8, S3 24, S2 12; News shows 36, 35 of them dated October | `site-changelog.yaml` |
| Deliveries, coverage, omissions | 103, 103, 42; 3 formal stacks | `site-changelog.yaml` |
| S3+ pull requests with a story | 41 of 57; the 16 without are #731, #725, #708, #699, #692, #688, #676, #671, #657, #645, #644, #621, #620, #578, #469, #460, all S3 and all merged in October | labels joined to entries’ `pull_requests` |
| Register | 230 results; 177 at S3+ (S5 10, S4 11, S3 156) | `frontier/results.yaml` |
| S3+ results with no story at their own score | 124: the 15 exempt S4 and S5 results and 109 S3 results | the gate’s rule, `news_announced_scores` |
| S3+ results named by no entry at all | 121; T-062, T-064 and T-081 are named only by S2 entries, which News does not show | the coordinator’s first figure of 121 counts this way |
| The 109 unannounced S3 results by `landed` | 81 before 13 October, when the News archive began; 27 on 13–22 October; 1 on 23 October | `landed` |
| Deployed News page | 223,432 bytes: 36 cards averaging 5,264 bytes (2,867 to 11,846), and 33,910 bytes outside them; one significance meter paragraph averages 628 bytes | `https://squaremath.org/news.html`, fetched twice that day (223,194 bytes at the first fetch) |
| Page budget | 600,000 bytes for a `page`, and 2,000,000 for every HTML file; News has no exception; the largest exceptions are 1,500,000 (`papers/n11-lower-bounds-explainer.html`), 1,400,000 (`results.html`) and 1,300,000 (`index.html`) | `site_urls.PAGE_BUDGETS`, `PAGE_BUDGET_EXCEPTIONS` and `HARD_HTML_LIMIT` at 64b316b6c, unchanged since 769e441e1 |
| Bytes sent | `news.html` 223,432 bytes, sent as 32,172 gzipped (6.9 to 1); `results.html` 1,303,283 as 86,414 (15 to 1); `index.html` 483,093 as 45,445; a request accepting only brotli got `news.html` uncompressed, and one accepting brotli or gzip got gzip | `curl` with each `Accept-Encoding` against `https://squaremath.org` |
| Load timings on record | `results.html` at 1,324,108 bytes passed three runs at desktop and phone widths, light and dark, and with scripts off: CLS 0, LCP at most 444 ms, longest task 197 ms, blocking 155 ms; News has none | the reason in `PAGE_BUDGET_EXCEPTIONS["results.html"]`, recorded on 22 October and not re-run |
| A large profile | 123,797 bytes (`profiles/evan-daniel.html`) | the deployed site |

## Design

### The merged-pull-request record

**A separate file, which absorbs `deliveries` and `stacks`.** The record is
`packing/pull-requests.yaml`, schema `packing/pull-requests.schema.yaml`, contract
`packing.squares:PullRequests/v1`, status `enforced`. It becomes the one home of every
merge fact. The 103 `deliveries` rows and the 3 `stacks` move into it in Phase 1, and
`site-changelog.yaml` keeps only editorial content: `entries`, `coverage` and
`frozen_entries`, under contract `SiteChangelog/v2`. An entry’s pull requests are looked
up in the new record, where the old rule looked them up in `deliveries`.

Extending `deliveries` in place to all 537 pull requests was the alternative.
It loses on four counts:

- **The coverage rule.** Every delivery needs an entry or exactly one omission, so 434
  new deliveries would need 434 written omissions, or the rule would have to change
  anyway.
- **Authorship.** `site-changelog.yaml` is hand-edited prose under review; the record is
  written by a tool and can be regenerated from GitHub.
  Mixing them puts several thousand machine-written lines in the file editors work in,
  and a tool rewriting part of it on every merge.
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
      - {id: T-223, change: raised}
      - {id: T-223, change: adopted, n: [204, 260]}
stacks: []          # moved unchanged from site-changelog.yaml
story_exempt: []    # S3+ pull requests allowed no story; may only shrink
```

| Field | Required | Meaning |
| --- | --- | --- |
| `number`, `title`, `merged_at`, `base_ref`, `merge_commit` | yes | GitHub’s facts at the latest read, as `deliveries` holds them today |
| `author` | yes | the GitHub login that opened the pull request; provenance, not credit |
| `labels` | yes, may be empty | every GitHub label; the significance label is the one `S1`–`S5` label, at most one |
| `delivery_to_main` | when the base is not `main` or the merge commit is off `main`’s first-parent line | `{commit, evidence}`: the first-parent commit of `main` whose history first holds the merge, and its commit URL; `via` names the carrying pull request when there is one |
| `stack_id` | no | formal stack membership, as today |
| `results` | no | each result the merge changed: `registered` (a new id), `raised` (a higher verification or confirmation rung, or a higher significance), or `adopted` with the counts `n` it became the house best packing at |
| `summary` | no | one plain sentence for a feed reader, for a title worth replacing ([Decision 4](#decisions)) |

Three fields the coordinator proposed are derived at render time rather than stored,
each because storing it would give a fact a second home:

- **Significance** is the S label.
  A pull request with no S label takes the score of the strongest result it `registered`
  or `raised`, read from the register, and is marked as scored from its results
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
  `gh pr list --repo jlevy/squares --state merged --limit 2000 --json number,title,mergedAt,mergeCommit,baseRefName,labels,author`.
  On 23 October it returned 537 rows in 3.6 s. The tool refuses a result whose length
  equals the limit, which could be a truncated list.
- **Verify.** Each merge commit must reach local `origin/main` (fetch it first), the
  check `import_changelog.verify_main_delivery` makes today.
  For a merge commit off the first-parent line, the tool finds the first first-parent
  commit of `main` that holds it, by ancestry tests along
  `git rev-list --first-parent origin/main`, and records it as `delivery_to_main`. A
  pull request that never reached `main` is refused by name.
- **Results.** For a merge whose first-parent diff touches `frontier/results.yaml`, the
  tool compares the register at the merge’s first parent and at the delivering commit:
  new ids are `registered`, and an id whose rung or significance rose is `raised`. It
  reads the house table `upper_bound_houses.ADOPTED` at the same two commits for
  `adopted`. It reads each entry’s id, rungs and score with a line scanner of the kind
  `render_changelog.register_score` is, so it need not parse a 1.98 MB register per
  commit. 122 first-parent commits on `main` have changed the register.
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
- **The backfill** is the first `--apply`: about 540 rows, the 103 migrated `deliveries`
  among them, whose `merged_at`, `base_ref`, `merge_commit` and `delivery_to_main` must
  agree with what GitHub and Git return (a title edited since is refreshed and listed),
  and the `results` of the 122 register-changing merges.
  Its cost is estimated, not measured, at under five CPU-minutes: one GitHub call, and
  at most 244 `git show` reads of the register (two for each of the 122 merges) and as
  many of `upper_bound_houses.py`.

`import_changelog` changes in two ways.
It reads merge facts from the record rather than writing `deliveries`, so drafting a
story is offline once the merge is recorded.
It also takes a drafted entry from the pull request’s description.
Live lanes already draft the entry under a **News** heading; this plan fixes its form as
one fenced `yaml` block under `## News`, which becomes the candidate in place of
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

**The page’s room.** Once the budget raise has landed, step 3 also runs
`python -m devtools.measure_news_page bytes` on the rendered page.
When fewer than 30 days of room remain before the trip point, the coordinator opens a
`decision` bead for the owner then, before the check fails
([The page budget](#the-page-budget)).

**Who runs it.** The intake pass’s runner, its coordinator, which merges under the
`github-merge: autonomous` grant ([Decision 5](#decisions)). When the owner merges by
hand, the next pass’s sweep lists the pull request and that pass records it.

**Each follow-up is recorded by the next.** The follow-up is a merged pull request too,
so the record always trails `main` by the latest follow-up and by anything merged after
it. The sweep tells that tail apart from a gap (below).

**The runbook and the comments change to the 23 October rule** in Phase 1:

- [Label the PR and Prepare News](../../../../packing/campaign/result-import.md#label-the-pr-and-prepare-news):
  “For other S3–S5 work, S3 results included, News stays optional” becomes: every pull
  request labelled S3, S4 or S5 has a story naming each S3+ result it registers or
  raises, drafted under **News** in its description as a fenced `yaml` entry and landed
  in the first change after its merge (the owner, 23 October 2026, point 1 above and
  [Decision 1](#decisions)).
- [Announce a Significant Result](../../../../packing/campaign/result-import.md#announce-a-significant-result)
  keeps the 22 October rule for results and adds the pull-request rule and its gate.
- Stage 7’s bullet list gains the record step, and
  [Maintaining the project changelog](../../../../development.md#maintaining-the-project-changelog)
  says where merge facts now live.
- The `ANNOUNCED_FROM` comment cites both decisions: 22 October (“Let’s have it do S4
  and S5 then”) for registered results, and 23 October (“Via each PR’s story”) for S3
  results, which reach News through the story of the pull request that registers or
  raises them. Its value stays 4.
- `.github/PULL_REQUEST_TEMPLATE.md`’s opening comment names the `## News` block form.

### Gates

**What catches an S3+ story left out.** The story gate runs inside
`render_changelog --check` in the records tier, in the step that already runs the
announcement gate. It reads only the tree:

- every pull request an entry names is a row of the record, and an entry’s date is the
  latest merge day of its pull requests (the rule today, moved to the record);
- every row whose S label is S*k*, with *k* at least 3 and the row not in
  `story_exempt`, is named by a News-shown entry scored *k* or higher, so an S4 pull
  request named only by an S3 entry fails, as a result announced below its score does
  today;
- for rows numbered above Phase 1’s own pull request (a constant set when that pull
  request is opened), that entry also lists in `result_ids` every S3+ result the row
  `registered` or `raised` ([Decision 1](#decisions)); earlier rows are reported, not
  failed;
- a score taken from results ([Decision 2](#decisions)) owes no story;
- a `story_exempt` entry that now has its story, or names a row that is not S3+, fails
  until it is removed, the same rule `ANNOUNCEMENT_EXEMPT` follows.

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
current `validate` code.
From Phase 1 on it validates a `SiteChangelog/v1` document from `main` against that
document’s own schema, then compares entry ids, dates and pull request membership, which
is all the freeze needs.

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
  Only the selected tab is in the tab order.
  The Left and Right arrows (wrapping), Home and End move between the tabs and select,
  as `atlas-view.js` does, and a click or Enter selects.
  The style is unchanged, because `site-nav.css` gives
  `[role="tab"][aria-selected="true"]` the same fill as `a[aria-current="page"]`. This
  plan has not checked that ARIA in HTML allows `role="tablist"` on a `nav` element; if
  it does not, Phase 2 puts the role on an inner element with `display: contents`, which
  keeps the strip’s layout.
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

**How this fits with #736.** #736 (open, the site agent’s) makes these changes:

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

Phase 1 changes no page.
Its edits to `render_changelog.py` (`validate`, the gates, `load`) and to
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

**Expected size**, estimated from the averages measured on 23 October: 5,264 bytes a
story; a shell of about 38,000 bytes (33,910 today, plus the strip, the feed’s filter
and the archive links); the feed’s 200,000-byte cap; and October’s 2.4 S3+ merges a day,
one story each, about 12,600 bytes a day.

| When | `news.html` | What it shows |
| --- | --- | --- |
| Today | 223,432 bytes | 36 stories |
| After `think-4oj0` | about 307,700 | 52 stories |
| Phase 2 lands | about 512,000 | 52 stories, and about 420 rows filling the feed’s cap at once |
| About 7 days after Phase 2 | 600,000 | today’s `page` budget |
| About 50 days after | 1,150,000 | the trip point below: about 173 stories |
| About 62 days after | 1,300,000 | the proposed budget: about 200 stories |

At the last seven days’ pace, 2.0 a day, the trip point comes about 61 days after Phase
2 and the budget about 75.

**The measurement, before the budget moves.** One retained tool,
`devtools.measure_news_page`, takes the measurement, as
[OR-1](../../../../operating-rules.md#or-1-build-the-tool-never-leave-a-measurement-in-one-off-code)
requires. Its report goes into the pull request that raises the budget, and its figures
into the exception’s reason.
It measures two pages, both built by the site’s own renderer:

- **today’s `news.html`**, as `main` renders it when the raise is made;
- **a projected `news.html` at the proposed budget**, 1,300,000 bytes: the real stories
  repeated in date order under new ids and anchors until the page reaches that size,
  with the feed at its full cap.
  Built from the page’s own cards, the projection carries the markup readers will get.

Its modes, from `packing/`:

- **`bytes PAGE...`** needs no browser.
  For each page it reports:
  - the raw bytes;
  - the gzip bytes at level 6, the level `preview_site.serve` uses; GitHub Pages sent
    gzip on 23 October;
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
  and at the projected size: five runs of each switch, to the feed and back, by click
  and by arrow key, at 1280 and 390 px.
  For each it reports the handler’s time, the time to the next frame, any long task, and
  the same counters over the change.
  Its page code is a probe file under `probes/measure_news_page/`, loaded with
  `sqpack.probes.probe`.

The budget may move when both pages pass:

- every `check_site_rendering` limit, unchanged (CLS 0.1, LCP 4,000 ms, longest task 300
  ms, blocking 600 ms), on the median of three runs, with the no-JS page readable;
- a tab switch that paints its next frame within 200 ms of the press, the median of five
  runs at 390 px, with no long task above the site’s 300 ms limit; 200 ms is the “good”
  bound of the web’s Interaction to Next Paint measure.

Transfer size has no limit of its own; the measured gzip and brotli bytes go into the
exception’s reason. Timings taken on the shared host are advisory, as `results.html`’s
exception says of its own, and shared CI keeps timing report-only
(`--timing-mode report-only`, `think-9dhb`). The report names the host, the Chromium
version and the runs.
The run is estimated, not measured, at a few CPU-minutes: about 80 navigations.

If the projected page fails a limit, the tool measures a projection at 1,000,000 bytes,
and the budget is the larger size that passes, with its trip point 150,000 bytes below
it. If 1,000,000 fails too, the raise stops and the report goes to the owner.

**The budget: 1,300,000 bytes**, if the measurement passes, for four reasons:

- It is the size the owner’s question named ([Decision 6](#decisions)).
- The site already serves a page that size.
  `results.html` is 1,303,283 bytes deployed, and its exception records three-run checks
  passing at 1,324,108. News prose compresses less than that table did on 23 October,
  6.9 to 1 against 15 to 1. If that ratio holds, News at 1,300,000 bytes sends about
  187,000 gzipped bytes, about twice what `results.html` sends, so the measurement
  settles the budget and the precedent only suggests it.
- It leaves 700,000 bytes under the 2,000,000-byte hard limit every HTML file has, room
  for one more measured raise if the owner chooses one later.
- At October’s pace it lasts about 62 days after Phase 2 lands, and the check below
  trips about 50 days in.

**Where it is set.**

- `site_urls.PAGE_BUDGET_EXCEPTIONS["news.html"] = (1_300_000, reason)`. The reason
  states the measured raw, gzip and brotli bytes, the timings at both sizes and their
  date, the trip point, and the bead that owns the runway.
  `validate_registry` already requires an exception to sit within the hard limit and to
  give a reason.
- `docs/project/site-urls.md`, re-rendered by `python -m devtools.site_urls --write`,
  lists it under Measured exceptions.
- `test_changelog_publication.py` holds it.
  `NEWS_CEILING = 1_300_000` and `NEWS_TRIP_BYTES = 1_150_000` sit beside the News page
  tests, and a test requires the exception to equal `NEWS_CEILING`, as
  `test_overview.py`’s `PAGE_CEILINGS` does for `index.html` and `results.html`.
- `check_published_site` needs no change.
  It reads `page_budget(row)`, so the Pages workflow refuses to deploy a `news.html`
  above 1,300,000 bytes, and the check of the deployed site reports one.
- The archive pages are ordinary `page` rows under the 600,000-byte default, with no
  exception.

**The check that trips first.** `test_news_page_stops_short_of_its_budget` runs in the
quick lane every pull request runs.
It renders `news.html` and fails when the page reaches `NEWS_TRIP_BYTES`, 150,000 bytes
under the budget, about 12 days of stories at October’s pace.
It prints the page’s bytes, the trip point, the budget and the days of room left at the
last 28 days’ pace, as the results page’s runway test prints its projection.
The change that would carry the page past the trip point is the change that fails, so no
story lands past it until the owner has chosen the next step.
This is the shape
[OR-17](../../../../operating-rules.md#or-17-every-routine-gate-has-a-wall-ceiling-and-anything-above-it-is-selected-on-purpose)
gives a gate’s wall time: a ceiling, and anything above it selected on purpose, with the
record saying who selected it.
The coordinator’s 30-day notice ([Process](#process)) gives the owner time to answer
before the check fails.

**When the page reaches its trip point.** The plan builds nothing for that day.
The next step is the owner’s decision, made then.
The coordinator’s `decision` bead puts these options to the owner, and none of them runs
automatically:

- raise the budget again, after the same measurement at the new size, up to the
  2,000,000-byte hard limit;
- shrink the feed’s cap on `news.html`, whose 200,000 bytes are about 16 days of
  stories;
- move older stories to dated archive pages, the design this plan drafted and the owner
  did not take on 23 October;
- shorten the cards on `news.html`, a card design the site agent owns;
- another step the owner names.

**What keeps the page cheap to load at that size.**

- **Static stories.** The renderer writes every story as HTML at build time.
  No script builds, fetches or re-renders a card, so a reader without scripts gets the
  whole page, which the no-JS check holds.
  Formulas arrive as prepared MathML (58 `<math>` elements on 23 October), and the page
  loads no math script.
- **Small scripts that only switch state.** `news-filters.js` (164 lines) sets `hidden`
  on cards and rows. `news-views.js` sets one attribute on the root and the tablist’s
  ARIA states, and `site.css` hides the other view.
  Neither creates, moves or re-renders markup, so a switch costs a style change and no
  parsing.
- **Cached shared files.** Styles, scripts and fonts are content-hashed files under
  `assets/`, cached across pages, so only the HTML grows.
- **Lazy images.** News has none today (no `<img>` on 23 October).
  A story that adds one sets `loading="lazy"`, `decoding="async"` and its `width` and
  `height`, so the image loads near the viewport and holds its box, and a renderer test
  holds every `<img>` on a News page to that.
- **A capped feed.** Rows past 200,000 bytes go to the archive pages, so the feed’s
  share stays fixed while the stories grow.
- **One cost to watch, read from the code and not measured.** At load, `news-cards.js`
  collapses each card and then reads its `scrollHeight`, one card at a time, so each
  card can force a layout before the next.
  The `load` mode’s `LayoutCount` and longest task show whether that cost grows with the
  story count. If it does, Phase 2 reads every card’s height before collapsing any.

**When the raise lands.** In Phase 2, measured on Phase 2’s own page, which launches at
about 512,000 bytes, about 7 days of stories under today’s budget.
Before Phase 2, the stories alone pass 600,000 bytes about 23 days after `think-4oj0`
lands. If Phase 2 has not merged two weeks after `think-4oj0` lands, the raise lands
ahead of it on its own: the tool, the measurement at both sizes without the switch, the
exception and the trip check.
Phase 2 then adds the switch’s measurement.

### Profiles

Each profile gains a **Pull Requests** section after Related News: newest first, one
line per pull request whose feed row names the person, with the date, the badge, the
story’s title (or the pull request’s title) linked, the role (“results”, “credited”,
“reported” or “pull request by”), and a link to the row on its archive page.
It uses the same `result_people` derivation as the feed, so a profile and the feed
cannot disagree, and the folding `_work_listing` already applies to long lists.

## Implementation Plan

### Phase 1: The Record, Its Tool, the Backfill and the Gate

One pull request. It starts after `think-4oj0`’s stories merge, so `story_exempt` starts
empty; if any of the 16 are still missing then, they go into `story_exempt` with a
reason, and that list may only shrink.

- [ ] `packing/pull-requests.schema.yaml` and the offline module
  `devtools.pull_request_record`: load, validate, and the derivations the gates need,
  scores from results among them.
- [ ] `devtools.record_pull_requests`, with its listing, `--apply`, `--pr` and `--audit`
  modes.
- [ ] Run the backfill: `--apply` over every merged pull request.
  Move the 103 `deliveries` and 3 `stacks` out of `site-changelog.yaml` and check that
  they agree with their rows.
- [ ] `render_changelog`: `SiteChangelog/v2`; entries checked against the record; the
  story gate, with its `result_ids` rule for rows numbered above this pull request; the
  freeze check reading v1 from `main`; `CHANGELOG.md` re-rendered and unchanged.
- [ ] `import_changelog`: merge facts from the record; the drafted `## News` entry from
  the description.
- [ ] `intake_sweep`: the Merged pull requests section, and the audit in `--offline`.
- [ ] `validate_schemas`’ corpus, the two steps’ `known_inputs`, and
  `release.validate_release_impacts` with whatever `check_release_impact` asks.
- [ ] The runbook, `development.md`, the `ANNOUNCED_FROM` comment and the template
  comment, as Process says.
- [ ] Tests, as the Testing Strategy says.

### Phase 2: The Toggle, the Feed, the Archives, the Budget and the Profile Lists

One pull request, after #736 and Phase 1 merge.
The intake session builds it, as the owner said (point 4). The budget raise lands ahead
of it on its own if Phase 2 is late ([When the raise lands](#the-page-budget)).

- [ ] `site_tallies.result_people(record)`, public, shared by the feed and the profiles.
- [ ] The feed view and its cap in `render_news`, through a feed renderer
  `devtools.render_pr_feed`; `row_location`; the half-month archive pages of rows in
  `render_overview`’s page table and `site-urls.yaml`; the archive links; and
  `news/anchors.json`.
- [ ] The budget raise, as [The page budget](#the-page-budget) says:
  `devtools.measure_news_page` and its probe; its report at today’s and the projected
  size; `PAGE_BUDGET_EXCEPTIONS["news.html"]` with its measured reason, and
  `docs/project/site-urls.md` re-rendered; `NEWS_CEILING`, `NEWS_TRIP_BYTES` and the
  trip check; the room report in Record the merge.
- [ ] `news-cards.js`: every card’s height read before any card collapses, if the
  measurement shows its load work growing with the story count.
- [ ] `news_view_tabs()`, passed to `kpress_page(tabs=…)` for `news.html` and every
  archive page; `news_significance_filter(levels)`.
- [ ] `overview/news-views.js` (new): the tablist, the `news-view` address and history.
- [ ] `overview/embed.js`: `data-site-news-view` from `news-view` or a `#pr-` fragment.
- [ ] `news-filters.js`: one instance per view, the **All** button and “Not scored”.
- [ ] `news-forward.js`: the `news/anchors.json` lookup on a missed fragment.
- [ ] `site.css`: the feed row, hiding the unselected view under `data-site-news-view`,
  and the `scripting: none` rule for rows.
- [ ] The header probe’s `[aria-selected="true"]`, and `news.html` and an archive page
  in `test_site_wide_blocks.py`.
- [ ] The profiles’ Pull Requests section.
- [ ] Tests and browser probes, as the Testing Strategy says.
- [ ] If Phase 2 is labelled S3 or higher, as a new public capability is likely to be,
  its own story lands in the follow-up after its merge, through the step Phase 1 adds.

## Testing Strategy

**Phase 1**, from `packing/`:

- A new `tests/test_pull_requests.py`:
  - the schema accepts the example and refuses each malformed field;
  - a second `--apply` over the same GitHub JSON fixture writes identical bytes;
  - a relabel refreshes `labels`, and a changed merge commit is refused;
  - a fixture repository in the style of `test_changelog.py`’s delivery tests: a merge
    commit off the first-parent line gets the right carrying commit, and a commit that
    never reached `main` is refused;
  - a two-commit fixture register yields `registered` and `raised`, and a two-commit
    `ADOPTED` table yields `adopted` with its counts;
  - an unlabelled row takes the score of its strongest registered or raised result;
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
  - a stale `story_exempt` entry fails;
  - main’s v1 document still freezes entries;
  - the migrated `CHANGELOG.md` renders identically.
- `test_intake_sweep.py`: a gap and an S3+ pull request need action, the trailing S1 is
  listed, and label drift needs action.
- `packing-validate --records`, then `--fast` in CI.
- The backfill’s evidence in the pull request: the row count equals the GitHub count at
  the run, `record_pull_requests --audit` reports nothing, and the 103 migrated rows
  match.

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
- The budget, in `test_changelog_publication.py` and a new
  `tests/test_measure_news_page.py`:
  - `PAGE_BUDGET_EXCEPTIONS["news.html"]` equals `NEWS_CEILING`, and `NEWS_TRIP_BYTES`
    is below it;
  - `news.html` under `NEWS_TRIP_BYTES`, which is the trip check itself;
  - `measure_news_page bytes` on a fixture page reports the gzip and brotli sizes the
    libraries give, and the days of room that follow from a fixture pace;
  - `measure_news_page project` reaches its target within one story’s bytes, from the
    page’s own cards only, with every id and anchor unique.
- Browser tests in `test_site_homepage.py`’s style:
  - the strip’s roles once enhanced: `tablist`, `tab`, `aria-selected`, `aria-controls`
    and `tabpanel`;
  - only the selected tab is in the tab order, and the arrows, Home and End move and
    select;
  - `news-view=changes` opens on the feed with no layout shift, switching pushes the
    address, and Back restores it;
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

1. Phase 1 merges. From then on the intake runner runs Record the merge after every
   merge, and the sweep reports anything missed.
2. Phase 2 merges and deploys.
   `check_published_site` and a look at `news.html` in both views, at its stacked form
   with scripts off, and at one archive page on the deployed site confirm it.
   `measure_news_page bytes` run against the deployed page agrees with the raw and gzip
   bytes in the exception’s reason.
3. The next follow-up records Phase 2 and lands its story, the first story the new step
   carries.

The News address and its bookmarks keep working: stories never leave `news.html`, a row
that leaves it is forwarded to its archive page, and the archive pages are new.

## Decisions

The owner answered the plan’s questions in conversation on 23 October 2026, and the
coordinator relayed the answers with the option labels quoted below.

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
   result it registered or raised, is marked as scored from its results, and owes no
   story, since it predates the rule.
   One with no label and no result stays “Not scored”.
   Hand-labelling the 352 on GitHub, and leaving them all unscored, were not taken.
3. **One page, switched in place.** The owner chose “One page, switched in place”, not
   the first draft’s two pages joined by links.
   On the toggle’s look the owner added: “We should use a toggle at the top of the page,
   much like we had a while back in the history, where there was a Film | Workbench
   toggle”. [The page](#the-page) follows both: the Film | Workbench strip’s element,
   look and place, switched in place as a tablist.
4. **Routine rows show the GitHub title.** This was not put to the owner, and the first
   draft’s recommendation stands.
   The optional `summary` remains for a title worth replacing.
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
   [The page budget](#the-page-budget) follows the answer: half-month archive pages hold
   feed rows only, the budget moves to 1,300,000 bytes on a measured load check, and a
   check trips 150,000 bytes short of it, leaving the next step to the owner.
   Half-month archive pages for stories, which the plan recommended, and shorter cards
   on `news.html` were not taken.
   Two figures in the question text were off, and the plan uses corrected ones:
   - `index.html`’s 1,300,000 bytes is the third-largest exception, after
     `results.html`’s 1,400,000 and the lower-bounds explainer’s 1,500,000.
   - The 86 days counted the stories alone at 2.2 a day.
     With the feed and the shell on the page, at October’s 2.4 a day, 1,300,000 bytes
     lasts about 62 days after Phase 2 lands.

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
