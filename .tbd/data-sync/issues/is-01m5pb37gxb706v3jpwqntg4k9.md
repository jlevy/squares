---
type: is
id: is-01m5pb37gxb706v3jpwqntg4k9
title: "Decision: news.html byte budget, no measured size passes the load checks, today's page included (think-3oxz)"
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-23-news-pr-feed.md
labels:
  - decision
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T06:55:42.109Z
updated_at: 2026-10-24T08:42:49.754Z
---
The owner's decision is needed: the measurement that was to confirm a larger byte budget for news.html (plan #759, "Before Phase 1: The Budget Raise"; think-3oxz) found no size that passes the site's own load checks, and today's page fails one of them too. The budget stays at 600,000 bytes until the owner picks a step.

WHAT WAS ASKED. The owner chose "Keep all, raise the limit" on 23 October 2026: every story stays on news.html. The plan proposed raising the page's byte budget from 600,000 to 1,300,000 bytes, but only if a page that size passes every check_site_rendering limit unchanged on the median of three runs (layout shift CLS at most 0.1, largest paint LCP at most 4,000 ms, longest task at most 300 ms, blocking time at most 600 ms), with the page readable without scripts. If 1,300,000 failed, try 1,000,000; if that failed too, stop and ask.

WHAT WAS MEASURED. On 24 October 2026, 06:22 to 06:30 UTC, on the shared 4-core host (node "vm", load average 2.4 to 9.6 during the runs), Chromium 151.0.7922.34, with the new retained tool devtools.measure_news_page (branch claude/intake-2026-10-24-news-budget). Two complete runs, each with three runs per scenario at 1280 and 390 px, light and dark:
- Today's page as main renders it: 318,950 bytes, 50 stories, 42,027 bytes gzipped (level 6), 31,031 brotli. Layout shift above 0.1 on the median in 1 of 4 scenarios in run 1 (390 dark 0.399) and 2 of 4 in run 2 (1280 light 0.119, 390 dark 0.399). Longest task at most 100 ms.
- Projected to 1,304,794 bytes (215 stories, today's cards repeated; 153,093 gzipped): layout shift fails all 4 scenarios in both runs (0.119 to 0.410), and the longest task fails all 4 in both runs (332 to 454 ms).
- Projected to 1,005,302 bytes (163 stories; 118,948 gzipped): layout shift fails 2 of 4 scenarios in both runs; in run 2 also longest task 578 ms and blocking 1,071 ms at 390 dark, with the host's load average at 9.6.
- Readable without scripts at every size.
- A third run (24 October 08:33-08:38Z, main e5c1c64e3, load average 3.4 to 6.1, same Chromium), taken for review A on PR #788, gave the same verdicts: today's 319,181-byte page fails the layout shift in 2 of 4 scenarios (1280 px, 0.121); 1,006,226 bytes fails it in 3 of 4; 1,305,949 bytes fails it and the longest task (339 to 400 ms) in 4 of 4.

WHY (corrected 24 October after review A on PR #788; a third run with two controls confirms it). Both failures come from the News scripts' work at load, not from the page's bytes alone.
- The layout shift is the News cards' script (overview/news-cards.js) shrinking the first visible story card to ten lines after the browser has already drawn it at full height, so everything below it jumps up: 0.34 to 0.35 of the screen at 390 px, 0.09 at 1280. Then news-filters.js reveals the filter bar above the stories (news-filters.js:160, controls.hidden = false), and they move again: 0.06 at 390 px, 0.02 at 1280. At 1280 px each shift alone is under 0.1; together (0.119 to 0.121) they fail it. On today's page the fold is a race the script sometimes wins (some runs score 0). On a larger page the browser draws before it reaches the script at the end of the page every time, so the shift happens every time.
- The longest task is news-cards.js's refresh, not the page's size. At load it folds each card, reads its line height and height, writes, and then reads its width, card after card (news-cards.js:47-66 and :95), so each card forces two layouts and two style recalculations: 31 layouts today, 81 at about 1.0 MB and 106 at about 1.3 MB (12, 37 and 49 visible cards). Style work grows with them, from about 85 ms to 470 to 480 ms of thread time.
- Controls (measure_news_page project 1300000 --without SCRIPT, then load, 24 October 08:33-08:38Z): the 1,305,949-byte page without news-cards.js passes every limit (CLS at most 0.061, longest task at most 144 ms, blocking at most 103, LCP at most 1,064; 6 to 8 layouts), with the cards left at full height. Without news-filters.js it still fails the longest task (432 ms, 106 layouts) and the shift at 390 px (0.35), while its 1280 px shift drops to 0.097.

WHAT IT MEANS. No raise can be confirmed by this measurement, so the 600,000-byte budget stands, and check_published_site will refuse to deploy a news.html above it. Today's page (319,181 bytes) reaches 600,000 in about 18 to 28 days and the plan's 450,000-byte watch point in about 9 to 13, depending on the window the pace is read over (measure_news_page bytes --pace-days N, 24 October): last 28 days 10,160 bytes a day, 12.9 and 27.6 days; last 21 days 13,217, 9.9 and 21.2; last 14 days 15,230, 8.6 and 18.4; last 7 days 12,947, 10.1 and 21.7; the plan's 14,400, 9.1 and 19.5. The 28-day figure is the long end: the window starts on 27 September, and the page's stories are one on 30 September and 49 from 9 October. The decision needs to land before the short end, about 18 days from 24 October.

OPTIONS (none runs automatically):
1. Have the site agent change news-cards.js and site.css so the cards are folded before the first paint (for example, the collapsed height set by a style that applies when scripts run, with the script only measuring), the filter bar's space is reserved before it is revealed, and the script reads every card's height before it writes any (the plan's batching remedy); then re-run the measurement. On the controls' evidence this one change addresses both failing limits; what a batched script costs is what the re-measurement settles. This changes news-cards.js and site.css (and news-filters.js or the filter bar's style), which the raise was not allowed to touch.
2. Raise the budget anyway on the owner's judgement, treating the shared host's numbers as advisory. The layout shift is not a timing figure, and check_site_rendering enforces it even in its report-only mode.
3. Keep 600,000 bytes and move older stories to dated archive pages (the plan's earlier design), or shorten the cards on news.html. On the controls' evidence this is not needed for the longest task.
4. Another step the owner names.

Also reported, outside the budget's conditions: with scripts on, check_site_rendering counts 73 of the page's 90 formulas as unreadable because they sit in S3 cards the default S4 and S5 filter hides; it reports that at every size, today's page included.

The pages measured were rendered at main c5697c2f2. At main 34eb8bb75 (#769) the page is 319,181 bytes over the same 50 stories, with the same room figures.

Evidence: the tool and its tests are on branch claude/intake-2026-10-24-news-budget, draft PR #788 (https://github.com/jlevy/squares/pull/788), which carries the tool alone, the third run's full load --markdown tables and review A's dispositions. The first two load reports are summarised in think-3oxz's notes; their JSON was not retained. Re-run from packing/ with `python -m devtools.measure_news_page project 0 --out DIR0`, `project 1300000 --out DIR1`, `project 1000000 --out DIR2`, then `load DIR0 DIR1 DIR2 --markdown`, about 3 to 4 minutes of wall time and 105 navigations; add `project 1300000 --out DIR3 --without news-cards.js` for the control, 35 navigations more.

## Notes

2026-10-24 c-fix-788-1024 (review A on PR #788, https://github.com/jlevy/squares/pull/788#issuecomment-6381675002): description corrected in place. WHY now names news-cards.js refresh's two forced layouts per visible card as the longest task's cause (A1) and the news-filters.js filter-bar reveal as the second layout shift (A2), with the retained tool's controls (project --without news-cards.js passes every limit at 1,305,949 bytes; without news-filters.js it still fails the longest task). WHAT IT MEANS gives the runway as 18 to 28 days to 600,000 and 9 to 13 to 450,000 by pace window (A3). Option 1 widened to fold before first paint, reserve the filter bar and batch reads before writes; option 3 notes it is not needed for the longest task. The stale 'no pull request opened' evidence line now points at #788. Before the edit the description said the long task grows with the page and gave about 28 days as the runway.
