---
title: News Feed of Every Merged Pull Request
description: A committed record of every merged pull request, the tool and gate that keep it, and a News toggle between notable stories and all changes by PR
author: Intake lane c-news-plan-1023, for the repository owner
---
# Feature: News Feed of Every Merged Pull Request

**Date:** 2026-10-23 (last updated 2026-10-23)

**Author:** intake lane `c-news-plan-1023` under coordinator `coord-intake-1023`, for
the repository owner

**Status:** Draft

**Tracking:** `think-vph5` (this plan); `think-4oj0` (News stories for the 16 merged S3
pull requests that have none); `think-n51k` (a pull request carrying its own News entry,
which this plan does not do)

## Overview

News today shows hand-written stories, and only some merged pull requests get one.
This plan adds a committed record of every merged pull request, a tool that writes it
after each merge, a records-tier gate that fails when a pull request labelled S3 or
higher has no News story, and a toggle at the top of News between **Notable stories**
(the stories, as now) and **All changes by PR** (one generated row per merged pull
request, with its significance, the results it carries and the people credited for
them). Each contributor profile gains the list of pull requests that carry that person’s
results.

The plan has two phases, each one pull request that can land on its own: the record, its
tool, the one-time backfill and the gate; then the pages and the profile lists.

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
- Every pull request labelled S3, S4 or S5 has a News story, and a gate fails the change
  that records the pull request without one.
- Landing a story after the merge is a named runbook step with a tool behind it, run in
  the same follow-up that records the merge.
- Rendering and validation stay offline: GitHub is read only by a tool at authoring
  time, as `site-changelog.yaml`’s header already requires.
- Each contributor profile lists the pull requests that carry the person’s results.

## Non-Goals

- No change to the home page’s News box, which PR #736 redesigns, or to the atlas pages
  of #744 and #746.
- No story is written automatically.
  The feed row is generated; a story stays edited prose.
- No same-PR stories. An entry still needs its pull request’s merge facts, so it lands
  after the merge; letting a pull request carry its own entry, stamped at merge, is
  `think-n51k`.
- No retroactive GitHub labels on the 352 unlabelled pull requests (Owner Question 2).
- No backfilled stories for the 15 S4 and S5 results exempt since 22 October; that stays
  the separate decision `render_changelog.ANNOUNCEMENT_EXEMPT` names.
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
- **Profiles** (`devtools.render_contributors`) list a person’s Records, Results and
  Credited Work from the reviewed credit manifest (`contributors/occurrences.yaml`)
  through `site_tallies.person_credit_stats`, and Related News from profile links in
  story prose (`news_by_profile`).
- **`devtools.stamp_landed`** is the precedent for a tool that reads history and writes
  the answer into a record: it dates each register entry’s `landed`, and its `--audit`
  compares the record with `main`’s first-parent history and gates nothing.
  [OR-18](../../../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob)
  is why: no program depends on Git history to produce its answer.

### Measured on `main` at 769e441e1

The coordinator’s figures for this plan were taken at 05e95db36; #748 merged since, and
every figure below was re-taken at 769e441e1 on 23 October 2026, with GitHub read the
same day.

| Fact | Value | How measured |
| --- | --- | --- |
| Merged pull requests | 537, #1 to #752, merged 22 August 18:33Z to 23 October 17:20Z | `gh pr list --state merged --limit 2000 --json …` (3.6 s) |
| By S label | S1 34, S2 94, S3 45, S4 8, S5 4; none 352 | the same listing; no pull request has two S labels |
| Unlabelled pull requests | 352, all #711 or earlier; the first labelled is #246, and 8 since #600 have none (#681, #685, #691, #693, #696, #701, #710, #711) | the same listing |
| GitHub authors | `jlevy` 528, `Guzhou0806` 7, `wand125` 2 | the same listing |
| Reaching `main` | all 537; 521 merge commits on `main`’s first-parent line; 16 arrived inside a later merge (12 based on another branch, and #55, #122, #123, #336 based on `main`) | `git merge-base --is-ancestor` and `git rev-list --first-parent` |
| Bases other than `main` | 73 | the same listing |
| Merge pace | August 61, September 162, October to the 23rd 314; 95 in the last 7 days | the same listing |
| Changelog entries | 48: S5 4, S4 8, S3 24, S2 12; News shows 36 | `site-changelog.yaml` |
| Deliveries, coverage, omissions | 103, 103, 42; 3 formal stacks | `site-changelog.yaml` |
| S3+ pull requests with a story | 41 of 57; the 16 without are #731, #725, #708, #699, #692, #688, #676, #671, #657, #645, #644, #621, #620, #578, #469, #460, all S3 | labels joined to entries’ `pull_requests` |
| Register | 230 results; 177 at S3+ (S5 10, S4 11, S3 156) | `frontier/results.yaml` |
| S3+ results with no story at their own score | 124: the 15 exempt S4 and S5 results and 109 S3 results | the gate’s rule, `news_announced_scores` |
| S3+ results named by no entry at all | 121; T-062, T-064 and T-081 are named only by S2 entries, which News does not show | the coordinator’s figure of 121 counts this way |
| The 109 unannounced S3 results by `landed` | 81 before 13 October, when the News archive began; 27 on 13–22 October; 1 on 23 October | `landed` |
| Deployed News page | 223,194 bytes for 36 cards (5,264 bytes each on average, 33,672 bytes outside them); one significance meter paragraph averages 628 bytes | `https://squaremath.org/news.html`, fetched 23 October |
| Page budget | 600,000 bytes for a `page` | `site_urls.PAGE_BUDGETS` |
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
| `labels` | yes, may be empty | every GitHub label; the significance is the one `S1`–`S5` label, at most one |
| `delivery_to_main` | when the base is not `main` or the merge commit is off `main`’s first-parent line | `{commit, evidence}`: the first-parent commit of `main` whose history first holds the merge, and its commit URL; `via` names the carrying pull request when there is one |
| `stack_id` | no | formal stack membership, as today |
| `results` | no | each result the merge changed: `registered` (a new id), `raised` (a higher verification or confirmation rung, or a higher significance), or `adopted` with the counts `n` it became the house best packing at |
| `summary` | no | one plain sentence for a feed reader, used only where Owner Question 4 says |

Three fields the coordinator proposed are derived at render time rather than stored,
each because storing it would give a fact a second home:

- **Significance** is read from the S label.
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

**Pull requests with no S label.** The 352 unlabelled pull requests (all #711 or
earlier) show a “Not scored” mark instead of a badge.
The S3+ default view hides them, **All** shows them, and the story gate ignores them,
since it reads S labels.
Owner Question 2 asks whether they should instead take the score of the strongest result
they registered or raised.

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
- **Modes**, from `packing/`, with the network settings `LANE-RULES.md` gives for `gh`:
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
Once the deploy of a merge is verified, the coordinator:

1. fetches `origin/main` and runs `python -m devtools.record_pull_requests --apply`;
2. for each newly recorded pull request labelled S3 or higher, runs
   `python -m devtools.import_changelog --pr N --output "$TMPDIR/changelog-candidate.yaml"`,
   reviews the candidate it takes from the description, and brings the entry into
   `site-changelog.yaml` with its coverage number;
3. renders with `python -m devtools.render_changelog`, runs
   `packing-validate --records`, and lands the change as the first change after the
   merge, the same follow-up that records the replies.

**Who runs it.** The coordinator of the pass that merged, since the coordinator merges
under the `github-merge: autonomous` grant.
When the owner merges by hand, the next pass’s sweep lists the pull request and that
pass records it. Owner Question 5 asks whether a GitHub workflow should do it instead.

**Each follow-up is recorded by the next.** The follow-up is a merged pull request too,
so the record always trails `main` by the latest follow-up and by anything merged after
it. The sweep tells that tail apart from a gap (below).

**The runbook and the comments change to the 23 October rule** in Phase 1:

- [Label the PR and Prepare News](../../../../packing/campaign/result-import.md#label-the-pr-and-prepare-news):
  “For other S3–S5 work, S3 results included, News stays optional” becomes: every pull
  request labelled S3, S4 or S5 has a story, drafted under **News** in its description
  as a fenced `yaml` entry and landed in the first change after its merge (the owner, 23
  October 2026, point 1 above).
- [Announce a Significant Result](../../../../packing/campaign/result-import.md#announce-a-significant-result)
  keeps the 22 October rule for results and adds the pull-request rule and its gate.
- Stage 7’s bullet list gains the record step, and
  [Maintaining the project changelog](../../../../development.md#maintaining-the-project-changelog)
  says where merge facts now live.
- The `ANNOUNCED_FROM` comment cites both decisions: 22 October (“Let’s have it do S4
  and S5 then”) for registered results, and 23 October for S3+ pull requests, gated
  through the record. Its value changes only if Owner Question 1 says so.
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
  today; under Owner Question 1’s recommended option the entry also lists, in
  `result_ids`, every S3+ result the row `registered` or `raised`, for rows merged after
  Phase 1;
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
- The feed page states the newest pull request it covers, “Changes recorded through #N,
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

**Two addresses, one toggle.** **Notable stories** stays at `news.html`. **All changes
by PR** is a new page, `changes.html`, with month archives under `changes/`. Both pages
open with the same `News` heading and, under it, a two-item control drawn in the
`site-tabs` style: “Notable stories” and “All changes by PR”, links in a
`<nav aria-label="News views">`, the current one marked `aria-current="page"`. Owner
Question 3 asks whether two addresses are acceptable.
They are recommended for three reasons:

- **The budget.** One page holding both views would carry the stories’ 223,194 bytes and
  a feed estimated at about 300,000 bytes today, against a 600,000-byte budget, and the
  feed grows with every merge.
- **No scripts needed.** The toggle works as two links, and each page is complete
  without scripts.
- **One plain address per view**, which readers can share and which search engines
  index.

A `?view=prs` parameter is not needed, because the address is the state.

**Default views and URL state.** News opens on its stories at S4 and S5, as now.
The feed opens at S3, S4 and S5. Both keep the reader’s choice in `news-s`, the
parameter News uses today, so a filter carries across the toggle when the reader changes
it. The feed’s significance group adds S1, S2, “Not scored” and an **All** button, which
selects every level.
The live count says how many of the page’s rows show, as News’s count does for its
cards.

**Without scripts** every row shows and the filter bar does not, by the
`@media (scripting: none)` rule News uses for its cards, extended to the feed’s rows.

**Accessibility.** The toggle is a pair of links, so the keyboard and screen readers
handle it natively. The filter is the existing fieldset with its hidden legend and
`aria-pressed` buttons.
The live count keeps `role="status"`. Hidden rows use `hidden`, so assistive technology
skips them as sighted readers do.
Each badge carries `aria-label="Significance S3 of 5"`, or “Not scored”.
Each row is an `<li id="pr-706">` in an `<ol>`, so a story, a profile or a reader can
link a row.

**A feed row, in words.** Rows are grouped under month headings, newest first.

- **An S3+ row** shows the merge date, then the significance meter News cards and
  results use (`overview_sections.significance_mark`, the “S3” text beside five bars,
  with the rubric’s short meaning as its tooltip), then the story’s title linked to the
  story on `news.html`. Under it, in the quieter `site-news-records sans-text` style:
  “#706”, linked to the pull request on GitHub, with the pull request’s title; then the
  results, as “Raises T-223 · Adopts T-223 at 204 and 260”, each id linked to its result
  page; then the people, as “Couzo · reported by Couzo”, deduplicated, each linked to
  the profile.
- **An S1, S2 or unscored row** is one line: the date, the compact badge (the meter’s
  “S2” text without the bars), the pull request’s title linked to GitHub, and any
  results and people, in the quieter style.

**The clear label.** The badge is the one significance mark the site already uses on
stories and results, so an S3 change looks the same everywhere.
Its text names the level for readers who do not read bars, and the filter buttons carry
the rubric’s meanings (`render_changelog.news_significance_meanings`). The meter’s bars
cost about 500 bytes, so routine rows get the text alone.

**Pages and size.** `changes.html` holds the newest 300 rows, about three weeks at
October’s pace. `changes/YYYY-MM.html` holds every row of one calendar month, from
`changes/2026-08.html`. Rows on the month pages never move, so profiles and stories link
there. Each feed page links every month page below its rows.
Estimates, not measurements: an S3+ row about 1,600 bytes, a routine row about 350, so
`changes.html` comes to about 180,000 bytes and October’s month page about 200,000. A
test holds every feed page under 450,000 bytes, below the 600,000-byte budget.
A month that ever passes it splits into halves, in a follow-up the failing test names.
Each page is a row of `site-urls.yaml`, derived from the pages the renderer declares and
written by `python -m devtools.site_urls --write`, as every generated page is.

**How this fits with #736.** #736 (open, the site agent’s) adds `NEWS_FLOOR` and
`NEWS_LEVELS`, moves the significance buttons into `news_significance_filter(selected)`,
adds the home box’s compact filter and `data-news-limit`, makes `news-filters.js` open
on the levels its markup presses, and adds `stamp_landed`’s `landings.yaml`. Phase 2
starts from `main` after #736 merges and builds on it:

- `news_significance_filter` gains a `levels` argument that defaults to
  `range(NEWS_FLOOR, 6)`, so News and the home box render exactly as #736 leaves them,
  and the feed passes S1 to S5.
- The feed’s S3+ default is pressed in markup, which #736’s script already honours; the
  script gains only the **All** button and “Not scored”.
- The toggle is drawn on the archive path of `render_news` (no `limit`), never on the
  home box.
- `news_highlights.py`, the compact filter, `stamp_landed.py` and `landings.yaml` are
  untouched.

Phase 1 changes no page.
Its edits to `render_changelog.py` (`validate`, the gates, `load`) and to
`result-import.md` meet #736’s only as text merges, and whichever lands second merges
`main`.

**Checks that stay green**, run in Phase 2:

- the browser floor (`packing-validate --only "browser floor"`: Biome, `tsc` and the
  type-aware ESLint rules) for `news-filters.js` and any probe;
- `packing-validate --only "browser code lives in files"`;
- `site_urls --check --history-ref origin/main`, for the new rows and every page budget;
- `test_changelog.py`, `test_changelog_publication.py`, `test_news_highlights.py`,
  `test_site_homepage.py` (its News facet tests drive Chromium),
  `test_render_contributors.py`, `test_overview.py` and `test_site_navigation.py`;
- `check_published_site` after the deploy.

`workbench_tools.check_frontend` builds and drives the workbench page only, so it is
unaffected; it runs in the full gate as always.

### Profiles

Each profile gains a **Pull Requests** section after Related News: newest first, one
line per pull request whose feed row names the person, with the date, the badge, the
story’s title (or the pull request’s title) linked, the role (“results”, “credited”,
“reported” or “pull request by”), and a link to the row on its month page.
It uses the same `result_people` derivation as the feed, so a profile and the feed
cannot disagree, and the folding `_work_listing` already applies to long lists.

## Implementation Plan

### Phase 1: The Record, Its Tool, the Backfill and the Gate

One pull request. It starts after `think-4oj0`’s stories merge, so `story_exempt` starts
empty; if any of the 16 are still missing then, they go into `story_exempt` with a
reason, and that list may only shrink.

- [ ] `packing/pull-requests.schema.yaml` and the offline module
  `devtools.pull_request_record`: load, validate and the derivations the gates need.
- [ ] `devtools.record_pull_requests`, with its listing, `--apply`, `--pr` and `--audit`
  modes.
- [ ] Run the backfill: `--apply` over every merged pull request.
  Move the 103 `deliveries` and 3 `stacks` out of `site-changelog.yaml` and check that
  they agree with their rows.
- [ ] `render_changelog`: `SiteChangelog/v2`; entries checked against the record; the
  story gate; the freeze check reading v1 from `main`; `CHANGELOG.md` re-rendered and
  unchanged.
- [ ] `import_changelog`: merge facts from the record; the drafted `## News` entry from
  the description.
- [ ] `intake_sweep`: the Merged pull requests section, and the audit in `--offline`.
- [ ] `validate_schemas`’ corpus, the two steps’ `known_inputs`, and
  `release.validate_release_impacts` with whatever `check_release_impact` asks.
- [ ] The runbook, `development.md`, the `ANNOUNCED_FROM` comment and the template
  comment, as Process says.
- [ ] Tests, as the Testing Strategy says.

### Phase 2: The Toggle, the Feed Pages and the Profile Lists

One pull request, after #736 and Phase 1 merge.
The intake session builds it, as the owner said (point 4).

- [ ] `site_tallies.result_people(record)`, public, shared by the feed and the profiles.
- [ ] A feed renderer, `devtools.render_pr_feed`: `changes.html` and the month pages,
  registered in `render_overview`’s page table and in `site-urls.yaml`.
- [ ] The toggle on `news.html` and the feed pages; `news_significance_filter(levels)`.
- [ ] `news-filters.js`: the **All** button and “Not scored”.
- [ ] Styles in `site.css`: the feed row, the tab links’ `aria-current` state, and the
  `scripting: none` rule for rows.
- [ ] The profiles’ Pull Requests section.
- [ ] Tests and browser probes, as the Testing Strategy says.
- [ ] If Phase 2 is labelled S3 or higher, as a new public page is likely to be, its own
  story lands in the follow-up after its merge, through the step Phase 1 adds.

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
  - a listing as long as the limit is refused.
- `test_changelog.py`, extended:
  - an entry naming a pull request the record lacks fails, and an entry’s date comes
    from the record;
  - an S3 row with no story fails a change that edits either record, warns another, and
    warns on `main`;
  - an S4 row named only by an S3 entry fails;
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
  - one row per record row, newest first, and month pages that partition the record;
  - S1, S2 and unscored rows rendered `hidden`, and S3+ rows visible;
  - each badge’s `aria-label`;
  - every story, result and profile link resolving to a page and anchor that exist;
  - the “recorded through” line;
  - every feed page under 450,000 bytes.
- Browser tests in `test_site_homepage.py`’s style:
  - the toggle’s links and `aria-current`;
  - `news-s` across the toggle;
  - **All**;
  - the count;
  - a bookmarked `#pr-N` row that the filter would hide is revealed, as News reveals a
    bookmarked card;
  - with scripting disabled, every row shows.
- `test_render_contributors.py`: Evan Daniel’s profile lists #687 for T-220, and a
  person with no result lists none.
- The checks named under The page, and `packing-validate --edit` while editing.

## Rollout Plan

1. Phase 1 merges. From then on the coordinator runs Record the merge after every merge,
   and the sweep reports anything missed.
2. Phase 2 merges and deploys.
   `check_published_site` and a look at `news.html`, `changes.html` and one month page
   on the deployed site confirm it.
3. The next follow-up records Phase 2 and lands its story, the first story the new step
   carries.

Nothing needs a migration on the deployed site: the News address and its bookmarks are
unchanged, and the feed pages are new.

## Open Questions

Each is the owner’s call.
Each is written to be answered without the rest of this plan.

1. **Should every registered S3 result also need a News story?** Today a gate requires a
   story for each registered result scored S4 or S5 (`ANNOUNCED_FROM = 4`, the owner’s
   decision of 22 October).
   The 23 October rule is about pull requests: every S3+ pull request gets a story.
   Every new S3 result arrives in a pull request that is itself S3+, because the rubric
   gives a pull request the score of the strongest result it delivers.
   109 S3 results already on `main` have no story: 81 landed before the News archive
   began on 13 October, 27 between 13 and 22 October, and 1 on 23 October.
   - (a) Keep the result gate at S4 and S5. The new pull-request gate also requires each
     story to list, in `result_ids`, every S3+ result its pull request registered or
     raised, from Phase 1’s merge on.
     New S3 results are then covered, the 109 old ones stay without stories, and each
     still appears in the feed through its pull request’s row.
   - (b) Lower the result gate to S3 and exempt everything that landed before 23
     October. For results registered from then on this is the same as (a), with a second
     gate, and the exemption list grows from 15 results to 124.
   - (c) Lower it to S3 and write the 109 stories, or grouped stories, one per pull
     request. Some of the 27 recent ones will be covered by `think-4oj0`’s 16 stories.
   - **Recommendation: (a).** It meets the 23 October rule without a backlog, and the
     feed already shows every old S3 result with its pull request.
2. **Should the 352 pull requests with no S label get a score?** Labels began with #246
   on 30 September, so nearly every pull request from the project’s first five weeks has
   none, and the feed’s S3+ default would hide them all.
   - (a) Show them as “Not scored”, visible under **All** only.
   - (b) Give each the score of the strongest result it registered or raised, marked
     “scored from its results”, and exempt them from the story gate because they predate
     the rule. The rubric already gives a pull request its result’s score, the tool
     computes these results anyway, and early milestones then appear in the S3+ view.
     The number this would raise to S3+ is not yet measured.
   - (c) Label them by hand on GitHub.
   - **Recommendation: (b)**, since it puts the early milestones in the default view at
     no extra editorial cost and changes no story obligation.
3. **May “All changes by PR” be its own address?** The owner asked for a toggle at the
   top of the News page.
   This plan draws that toggle on two pages, `news.html` and `changes.html`.
   - (a) Two pages, with the toggle as two links: about 300,000 bytes of feed stays off
     the stories page, it works without scripts, and each view has a plain address.
     The toggle navigates to the other page instead of switching in place.
   - (b) One page, switched in place by a script, which would cross the 600,000-byte
     page budget within weeks at the current pace of about 14 merges a day.
   - **Recommendation: (a).**
4. **What one-line text should a routine pull request show?** Rows link the story where
   one exists. For the roughly 480 pull requests without a story, the GitHub title is
   what is available, and agent titles read like commit subjects (“records(#678): stage
   4 raises T-223 …”).
   - (a) Show the GitHub title.
   - (b) Ask every pull request for a one-sentence reader summary in its description,
     which the tool copies into `summary`.
   - (c) Have an agent write summaries for the backfill.
   - **Recommendation: (a)**, adding no step to every pull request.
     `summary` stays available for a title worth replacing.
5. **Who records each merge?** Phase 1 makes it the coordinator’s first step after a
   merge, with the sweep as the backstop.
   - (a) The coordinator, by hand, in the follow-up it already opens for replies.
   - (b) A GitHub workflow that runs on every merge and opens a “record #N” pull
     request. It never forgets, but each such pull request is itself a merge to record
     and needs batching, it needs write permission for workflows, and a story still
     needs an editor.
   - **Recommendation: (a)** now, and (b) if a sweep ever finds a miss.

## References

- [`packing/site-changelog.yaml`](../../../../packing/site-changelog.yaml) and
  [`packing/site-changelog.schema.yaml`](../../../../packing/site-changelog.schema.yaml)
- [`packing/devtools/render_changelog.py`](../../../../packing/devtools/render_changelog.py),
  [`packing/devtools/import_changelog.py`](../../../../packing/devtools/import_changelog.py),
  [`packing/devtools/overview/news-filters.js`](../../../../packing/devtools/overview/news-filters.js),
  [`packing/devtools/render_contributors.py`](../../../../packing/devtools/render_contributors.py),
  [`packing/devtools/site_tallies.py`](../../../../packing/devtools/site_tallies.py),
  [`packing/devtools/intake_sweep.py`](../../../../packing/devtools/intake_sweep.py),
  [`packing/devtools/stamp_landed.py`](../../../../packing/devtools/stamp_landed.py),
  [`packing/devtools/site_urls.py`](../../../../packing/devtools/site_urls.py)
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
