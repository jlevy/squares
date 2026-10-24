---
type: is
id: is-01m5p8babk5xj1t2jtfgv1qy88
title: "News page budget raise: measure_news_page, the news.html exception and the trip check (plan #759, before Phase 1)"
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-23-news-pr-feed.md
delegate: c-news-budget-1024
labels: []
dependencies: []
parent_id: is-01m5mwbn450xgwq4mgjnrpn0jm
hold: null
hold_until: null
created_at: 2026-10-24T06:07:41.427Z
updated_at: 2026-10-24T07:17:08.642Z
started_at: 2026-10-24T06:08:00.514Z
---
The plan docs/project/specs/active/plan-2026-10-23-news-pr-feed.md, section 'Before Phase 1: The Budget Raise' and 'The page budget'. One PR: devtools.measure_news_page (bytes, project, load), its report at today's size and the projected 1,300,000 bytes, PAGE_BUDGET_EXCEPTIONS['news.html'] with a measured reason, docs/project/site-urls.md re-rendered, NEWS_CEILING and NEWS_TRIP_BYTES and the trip check in render_changelog --check with its scopes, the room report and merge-step rule in the runbook, and the tests from the Testing Strategy. Must merge before main's news.html passes 450,000 bytes (318,655 on 24 Oct; about 9 days). Owner's answer: 'Keep all, raise the limit'.

## Notes

2026-10-24 c-news-budget-1024: RAISE STOPPED at the plan's fallback rule; owner decision opened as think-lsam (label decision, under think-ezt8). No pull request opened.

Delivered: devtools.measure_news_page (bytes, project, load; no page code, so no probe) and tests/test_measure_news_page.py (10 tests), commit 9d566b859 on branch claude/intake-2026-10-24-news-budget, pushed (git ls-remote agrees), based on main 34eb8bb75. Not done, since each depends on a confirmed budget: PAGE_BUDGET_EXCEPTIONS["news.html"], site-urls.md, NEWS_CEILING and NEWS_TRIP_BYTES, the trip check, the runbook rules, the plan's ticks.

Measured 24 Oct 06:22-06:30Z, host "vm" (4 cpus, load average 2.4-9.6), Chromium 151.0.7922.34, under nice, two full runs of `load --runs 3` (105 navigations each, 3m08s and 3m41s wall). Pages rendered at main c5697c2f2:
- today: 318,950 raw, 42,027 gzip-6, 31,031 brotli-11; 50 stories (mean 5,685, p90 8,727), shell 34,709. Worst CLS median 0.399 in both runs (run 1 fails 390 dark; run 2 fails 1280 light 0.119 and 390 dark 0.399). LCP <=380, longest task <=100, blocking <=86 ms. No-JS readable.
- 1,304,794 raw (215 stories), 153,093 gzip: CLS fails 4/4 in both runs (0.119-0.410); longest task fails 4/4 (395-454 run 1, 332-423 run 2); LCP <=1,392; blocking <=529. No-JS readable.
- 1,005,302 raw (163 stories), 118,948 gzip: CLS fails 2/4 in both runs (0.119-0.400); run 2 also longest task 578 and blocking 1,071 at 390 dark (load average 9.6). No-JS readable.
Cause of the shift: news-cards.js collapses the first visible card (basic-and-advanced-tutorials) to 10 lines after first paint (0.35 of the viewport at 390 px, 0.09 at 1280). Load counters: style 77-99 ms at 319 KB, 253-355 at 1.0 MB, 420-475 at 1.3 MB; layouts 31 / 82 / 106. With scripts on, check_site_rendering also counts 73 of 90 formulas unreadable at every size (S3 cards hidden by the default filter); reported, outside the budget's conditions.
Room now (bytes mode, main 34eb8bb75): 319,181 bytes; at the last 28 days' pace (10,160 bytes a day) about 13 days to the plan's 450,000 watch point and 28 to the 600,000 budget.
Validation: test_measure_news_page 10 passed; ruff and basedpyright clean on both files; check_no_embedded_js, check_probes, site_urls --check and check_release_impact pass. packing-validate --edit: the whole-repo type floor timed out at 900 s on the loaded host (load average 11-13), and site_urls failed only because origin/main moved (#769) mid-run, passing after the branch moved to 34eb8bb75.

2026-10-24 c-news-budget-1024 (on coord-intake-1023's instruction): draft PR #788 opened for the tool alone, https://github.com/jlevy/squares/pull/788, labels S1 and project, head 463f78d3f (commits 9d566b859, the tool and tests; 463f78d3f, the plan's tool and report items ticked and one dated line saying the raise waits on think-lsam). No exception, trip check or runbook change. Branch on main 34eb8bb75; no merge needed. Hosted CI is the full type check (local one timed out under load).
