---
type: is
id: is-01m5x4cnp25xx07kzyyrhfxxs7
title: The Changelog page shows the day rollup, not a News-like story per entry
kind: task
status: closed
priority: 1
version: 3
delegate: claude-session-01mfvb
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-26T22:13:12.514Z
updated_at: 2026-10-26T23:55:38.295Z
started_at: 2026-10-26T22:14:36.127Z
closed_at: 2026-10-26T23:55:38.293Z
close_reason: null
resolution: null
duplicate_of: null
---
The owner, 26 October 2026, on the Changelog page shipped by #837: "you previously had a
nice togglable brief tabular summary for the changelog. you've replaced it with something
far too verbose... we don't need a full duplication of news-like stories for every tiny
change to the site that is excessive", and then: "the Recently Added section is closer to
what the changelog should look like and we should move that to changelog not put it on the
homepage", and "it should have a button to take you."

So the Changelog page keeps its address and loses its presentation. What it holds instead
is the day rollup the home page calls Recently Added.

## What moves

- `overview_sections.recently_added` draws `div.site-rollup.site-added`: one `<details>` a
  day, newest first, its summary the date and its tally, its body one brief line an item.
  That block moves from the home page to `changelog.html` and covers the whole history
  rather than `ADDED_DAYS`.
- The home page loses the `Recently Added` heading, its introduction and the block, and
  gains a `Changelog` action beside `All News`, which is where the two history surfaces
  belong together under the Project menu.
- The per-entry prose `render_changelog.render_markdown(destination="site")` writes stops
  being the Changelog page's body. The GitHub action row stays.

## Measured before starting

The full history is **35 day blocks and 2,332 line items**, oldest 1 September 2026, so
one page holds it. The seven-day window already carries 1,784 of those items, so the page
is about a third larger than the block the home page draws today, not an order more.

## The constraint that is easy to miss

`render_changelog.archived_news_targets` forwards a bookmark for every below-floor entry
to `changelog.html#<entry anchor>`, and News and About both carry those links;
`test_changelog_publication.py` asserts the anchor is on the page. Dropping the per-entry
prose would strand them. So each site or project change keeps a brief line of its own in
its day's rollup, carrying its anchor and linking out to its pull request, its issues, or
its News card where it has one. That is also what the owner asked for in "links to expand
to details if necessary": the line is the summary, the link is the detail.
