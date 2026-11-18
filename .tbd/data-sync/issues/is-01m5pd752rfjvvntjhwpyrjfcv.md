---
type: is
id: is-01m5pd752rfjvvntjhwpyrjfcv
title: "PR #788 (merge): senior review of devtools.measure_news_page and the News load measurement"
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-23-news-pr-feed.md
delegate: c-review-788-a
labels: []
dependencies: []
parent_id: is-01m5mwbn450xgwq4mgjnrpn0jm
hold: null
hold_until: null
created_at: 2026-10-24T07:32:47.832Z
updated_at: 2026-10-24T07:53:30.977Z
started_at: 2026-10-24T07:33:03.816Z
---

## Notes

Review A (senior, round 1) of PR #788 at head 463f78d3f9219090dbc34b9794802099c2870d96, base 34eb8bb75b3ce6fff9c04bcfce0eb8f8d1e1bf9a, published as a PR comment: https://github.com/jlevy/squares/pull/788#issuecomment-6381675002

Verdict: approve once A1 is fixed. A1's fix is to the PR body and the plan's dated line; no code change is needed to merge.
Findings: A1 High, A2-A4 Medium, A5-A9 Low, A10 suggestion. Blocker/High: A1.
- A1 (High): the longest task's cause is news-cards.js's per-card forced layout (LayoutCount 31/81-82/105-108 = 2 per visible card 12/37/49, plus about 7), not page size. Without news-cards.js the 1,305,949-byte page passes all four check_site_rendering limits (runs 3, load average 8.7-9.7: CLS <= 0.061, longest task <= 234 ms). The PR's Why it fails and the plan's dated line (plan:1324) say otherwise; think-lsam repeats it.
- A2 (Medium): a second shift (0.0606 at 390, 0.0226 at 1280, source div.site-news, consistent with news-filters.js:160 revealing the filter bar) tips desktop over 0.1; the fold alone is 0.092-0.098 there.
- A3 (Medium): the 28-day window's first 12 days hold one story; the runway to 600,000 is 18-22 days at the plan's pace and at the 7/14/21-day paces, 28 only at the 28-day pace.
- A4 (Medium): the report box is ticked but the tool's load --markdown tables (DCL/FCP unthrottled and slow-4g, counters, ParseHTML) are not in the PR.
- A5-A9 (Low): projected brotli is a repetition artifact; verdict passes when native timing is unavailable or errors occur; p90 rank; bytes --markdown help; 1,005,302 row lacks a fail mark.
Outside the diff: think-lsam says "no pull request opened" (stale) and carries A1-A3.
Dedicated reviews: none warranted.
Tests: pytest tests/test_measure_news_page.py under unshare -n, 10 passed; ruff clean; flowmark stable; bytes/project at head and on main 11d0ab06b reproduce, independently re-measured; reviewer counters and one check_site_rendering --runs 3 on a scratch copy without news-cards.js.
