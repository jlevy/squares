---
type: is
id: is-01m5pb37gxb706v3jpwqntg4k9
title: "Decision: news.html byte budget, no measured size passes the load checks, today's page included (think-3oxz)"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-23-news-pr-feed.md
labels:
  - decision
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T06:55:42.109Z
updated_at: 2026-10-24T06:55:42.109Z
---
The owner's decision is needed: the measurement that was to confirm a larger byte budget for news.html (plan #759, "Before Phase 1: The Budget Raise"; think-3oxz) found no size that passes the site's own load checks, and today's page fails one of them too. The budget stays at 600,000 bytes until the owner picks a step.

WHAT WAS ASKED. The owner chose "Keep all, raise the limit" on 23 October 2026: every story stays on news.html. The plan proposed raising the page's byte budget from 600,000 to 1,300,000 bytes, but only if a page that size passes every check_site_rendering limit unchanged on the median of three runs (layout shift CLS at most 0.1, largest paint LCP at most 4,000 ms, longest task at most 300 ms, blocking time at most 600 ms), with the page readable without scripts. If 1,300,000 failed, try 1,000,000; if that failed too, stop and ask.

WHAT WAS MEASURED. On 24 October 2026, 06:22 to 06:30 UTC, on the shared 4-core host (node "vm", load average 2.4 to 9.6 during the runs), Chromium 151.0.7922.34, with the new retained tool devtools.measure_news_page (branch claude/intake-2026-10-24-news-budget). Two complete runs, each with three runs per scenario at 1280 and 390 px, light and dark:
- Today's page as main renders it: 318,950 bytes, 50 stories, 42,027 bytes gzipped (level 6), 31,031 brotli. Layout shift above 0.1 on the median in 1 of 4 scenarios in run 1 (390 dark 0.399) and 2 of 4 in run 2 (1280 light 0.119, 390 dark 0.399). Longest task at most 100 ms.
- Projected to 1,304,794 bytes (215 stories, today's cards repeated; 153,093 gzipped): layout shift fails all 4 scenarios in both runs (0.119 to 0.410), and the longest task fails all 4 in both runs (332 to 454 ms).
- Projected to 1,005,302 bytes (163 stories; 118,948 gzipped): layout shift fails 2 of 4 scenarios in both runs; in run 2 also longest task 578 ms and blocking 1,071 ms at 390 dark, with the host's load average at 9.6.
- Readable without scripts at every size.

WHY. The layout shift is the News cards' script (overview/news-cards.js) shrinking the first visible story card to ten lines after the browser has already drawn it at full height, so everything below it jumps up: 0.35 of the screen at 390 px, 0.09 at 1280. On today's page it is a race the script sometimes wins (some runs score 0). On a larger page the browser draws before it reaches the script at the end of the page every time, so the shift happens every time. The long task grows with the page: Chromium's style work at load goes from about 80 ms of thread time at 319 KB to 250 to 355 ms at 1.0 MB and 420 to 475 ms at 1.3 MB.

WHAT IT MEANS. No raise can be confirmed by this measurement, so the 600,000-byte budget stands, and check_published_site will refuse to deploy a news.html above it. At the last 28 days' pace (10,151 bytes a day, from the page's own dated cards), today's page reaches 450,000 bytes, the plan's watch point, in about 13 days and 600,000 in about 28 (measure_news_page bytes, 24 October).

OPTIONS (none runs automatically):
1. Have the site agent make the card collapse happen before the first paint (for example, the collapsed height set by a style that applies when scripts run, with the script only measuring), then re-run the measurement. This changes news-cards.js and site.css, which the raise was not allowed to touch.
2. Raise the budget anyway on the owner's judgement, treating the shared host's numbers as advisory. The layout shift is not a timing figure, and check_site_rendering enforces it even in its report-only mode.
3. Keep 600,000 bytes and move older stories to dated archive pages (the plan's earlier design), or shorten the cards on news.html.
4. Another step the owner names.

Also reported, outside the budget's conditions: with scripts on, check_site_rendering counts 73 of the page's 90 formulas as unreadable because they sit in S3 cards the default S4 and S5 filter hides; it reports that at every size, today's page included.

The pages measured were rendered at main c5697c2f2. At main 34eb8bb75 (#769) the page is 319,181 bytes over the same 50 stories, with the same room figures.

Evidence: the tool and its tests are commit 9d566b859 on branch claude/intake-2026-10-24-news-budget (pushed; no pull request opened, since the raise stopped). The two load reports are summarised in think-3oxz's notes. Re-run from packing/ with `python -m devtools.measure_news_page project 0 --out DIR0`, `project 1300000 --out DIR1`, `project 1000000 --out DIR2`, then `load DIR0 DIR1 DIR2 --markdown`, about 3 to 4 minutes of wall time and 105 navigations.
