---
type: is
id: is-01m5mvsbaz9gdq14qb1t8x8fj1
title: News for every landed S3+ result and S3+-labelled PR, clearly labelled with its significance (owner, 23 October)
kind: task
status: closed
priority: 1
version: 5
delegate: c-news-1023
labels:
  - process
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T17:08:55.263Z
updated_at: 2026-10-24T01:53:15.416Z
started_at: 2026-10-23T17:08:57.017Z
closed_at: 2026-10-24T01:53:15.415Z
close_reason: "#758 merged at 5664ac1e8 (head c4fe4312a; reviews A 6372329921 and B 6378129147 with dispositions 6376713694 and 6378406397; CI green 40050494138, 40050494149, 40050490671): the 16 merged S3 PRs that had no News now have stories (14 entries). The process and the page design (S3+ News for every landed PR, the PR feed, the tabs) continue in think-vph5 and PR #759."
resolution: null
duplicate_of: null
---
Owner, 23 October 2026 (in conversation): 'can we in parallel make sure that every time we have a PR land, it's clearly reflected in the news for all with significance S3+ And that's labeled in a clear way. Should be part of our process and the design.' Supersedes the 22 October decision ('Let's have it do S4 and S5 then'; render_changelog.ANNOUNCED_FROM = 4). Scope: the runbook rule, the records-tier gate (offline: registered results at S3+), the intake sweep (online: merged PRs labelled S3+ with no News entry naming them), the News data (each entry's significance score and PR numbers), backfill of what landed without an item, and a site bead for any visual label the cards lack (visuals are the site agent's).

## Notes

Stories for the 16 outstanding S3 PRs only; the toggle and feed design moved to a separate plan.
