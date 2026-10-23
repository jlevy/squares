---
type: is
id: is-01m5mvsbaz9gdq14qb1t8x8fj1
title: News for every landed S3+ result and S3+-labelled PR, clearly labelled with its significance (owner, 23 October)
kind: task
status: in_progress
priority: 1
version: 3
delegate: c-news-1023
labels:
  - process
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T17:08:55.263Z
updated_at: 2026-10-23T17:11:44.404Z
started_at: 2026-10-23T17:08:57.017Z
---
Owner, 23 October 2026 (in conversation): 'can we in parallel make sure that every time we have a PR land, it's clearly reflected in the news for all with significance S3+ And that's labeled in a clear way. Should be part of our process and the design.' Supersedes the 22 October decision ('Let's have it do S4 and S5 then'; render_changelog.ANNOUNCED_FROM = 4). Scope: the runbook rule, the records-tier gate (offline: registered results at S3+), the intake sweep (online: merged PRs labelled S3+ with no News entry naming them), the News data (each entry's significance score and PR numbers), backfill of what landed without an item, and a site bead for any visual label the cards lack (visuals are the site agent's).

## Notes

2026-10-23 coord-intake-1023: OWNER DESIGN (in conversation, 23 October): "You should be able to get the important things that have happened from every person's contributions and so on ... whether it should go in as part of the news stories or perhaps be a separate feed at the bottom of the news page"; then "Maybe the best design would be to have a toggle at the top of the news page that shows either just the notable news stories or a feed of all changes by PR." Coordinator's proposal, which the owner took: (1) News page toggle: Notable stories (hand-written; required at S4/S5, optional at S3) | All changes by PR (generated feed, one item per merged PR: merge date, S1-S5 badge, title and one-line summary, results registered or adopted, credited people linked to profiles; default filter S3+, show all); (2) each contributor profile lists the PRs carrying their results; (3) a committed PR record written by a tool after each merge (rendering stays offline), the sweep lists merged PRs missing from it, the records tier keeps it consistent. Owner answers: feed covers ALL merged PRs from the repository's start (backfill once); the intake session builds the page part too, in one PR, reusing the News page's significance filter and card styles, no other page changes. Facts at main 05e95db36: News 48 entries (S5 4, S4 8, S3 24, S2 12); register S3+ 177, 121 with no News item; merged S3+ PRs 57, 16 without a story.
