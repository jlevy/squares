---
type: is
id: is-01m5mwbn450xgwq4mgjnrpn0jm
title: Plan the News page toggle (notable stories / all changes by PR), the merged-PR record and the S3+ News process
kind: task
status: in_progress
priority: 2
version: 9
spec_path: docs/project/specs/active/plan-2026-10-23-news-pr-feed.md
delegate: c-news-plan-1023b
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T17:18:55.109Z
updated_at: 2026-10-23T23:14:13.837Z
started_at: 2026-10-23T17:19:23.812Z
---

## Notes

2026-10-23 c-news-plan-1023: plan written and opened as draft PR #759 (https://github.com/jlevy/squares/pull/759), branch claude/intake-2026-10-23-news-feed-plan, head cd1c8eb67 (S1, project). Spec: docs/project/specs/active/plan-2026-10-23-news-pr-feed.md. Design: a separate packing/pull-requests.yaml absorbs site-changelog.yaml's deliveries and stacks; devtools.record_pull_requests writes it after each merge (first run = backfill of all 537 merged PRs); an offline story gate in render_changelog --check fails the change that records an S3+ PR without a News story; intake_sweep lists merges never recorded; stage 7 gains "Record the merge". Phase 2: news.html / changes.html toggle, month archives, profile PR lists, after #736 and Phase 1. Five owner questions in the spec's Open Questions (ANNOUNCED_FROM at 3; scores for the 352 unlabelled PRs; separate feed address; routine-row text; who records merges).

2026-10-23 coord-intake-1023: OWNER ANSWERS (in conversation, 23 October, on the plan in PR #759):
- Q1 S3 results: "Via each PR's story (Recommended)". Keep ANNOUNCED_FROM = 4 for results. From Phase 1 on, every S3+ PR's story names each S3+ result the PR registers or raises. The 109 older S3 results appear in the feed under their PR.
- Q2 old PRs: "Score from their results (Recommended)". An unlabelled PR takes the score of the strongest result it delivered, computed and marked as such, and owes no story.
- Q3 toggle: "One page, switched in place". This is not the plan's recommended two pages; the spec must be redesigned for one page within the page budget.
- Q5 recording: "Intake runner (Recommended)". The intake runner records each merge at stage 7, and the sweep is the backstop.
- Q4 (feed row text) was not asked. The coordinator's default is the GitHub title, as the plan recommends.
- OWNER, same conversation: "We should use a toggle at the top of the page, much like we had a while back in the history, where there was a Film | Workbench toggle". That toggle was `.site-tabs` (d73244ff4, 30 September; moved under the bar's rule in 12a0a8438, 1 October). The spec takes its look and position (header slot, under the rule, `--site-tabs-space`), with in-place switching per Q3.

2026-10-23 c-news-plan-1023: revised to the owner's answers (relayed by coord-intake-1023) and pushed: head 42582e6a7 on PR #759, after merging main cc91ee1b8. Decisions recorded with option labels: Q1 "Via each PR's story (Recommended)" (ANNOUNCED_FROM stays 4; the story gate requires each S3+ result a PR registers or raises, from Phase 1 on); Q2 "Score from their results (Recommended)"; Q3 "One page, switched in place", plus the owner's Film | Workbench toggle instruction (header-slot nav.site-tabs from d73244ff4 / 12a0a8438, enhanced to a tablist, view in news-view); Q4 GitHub title (not asked); Q5 "Intake runner (Recommended)". New finding: with every S3+ PR getting a story (2.2/day last week, 5,264 bytes each), news.html passes its 600,000-byte budget about 25 days after think-4oj0 lands even without the feed, so the plan caps both views (stories 300,000 bytes, rows 200,000) and adds half-month archive pages; one new open question asks the owner to accept that.

2026-10-23 c-news-plan-1023b: revised to the owner's page-budget answer, "Keep all, raise the limit" (relayed by coord-intake-1023), and pushed: head 8dee3896c on PR #759, after merging main 64b316b6c (merge commit 42945ed06). Every story stays on news.html; only feed rows (cap 200,000 bytes) go to half-month archive pages. New section "The page budget": a retained tool devtools.measure_news_page (bytes: raw, gzip level 6, brotli q11; project: real stories repeated to a target size; load: check_site_rendering and measure_site_pages load at 1280/390, light/dark, no-JS, plus Performance.getMetrics counters and a ParseHTML trace diagnostic; switch: the in-place tab switch, 5 runs, <=200 ms to next frame at 390 px), run on today's page and a projected 1,300,000-byte page. Budget: PAGE_BUDGET_EXCEPTIONS["news.html"] = 1,300,000 (fallback 1,000,000, then the owner), held by NEWS_CEILING in test_changelog_publication.py; trip check test_news_page_stops_short_of_its_budget at NEWS_TRIP_BYTES 1,150,000 (OR-17); Record the merge reports days of room and the coordinator opens a decision bead at under 30 days; at the trip point the next step is the owner's (raise again up to HARD_HTML_LIMIT 2,000,000, shrink the feed cap, archive stories, shorter cards). Decision 6 quotes the label and attributes the option text to the coordinator; Decision 5 gains the coordinator's confirmation. Corrections found: the largest exceptions are 1,500,000 (n11 lower-bounds explainer) and 1,400,000 (results.html), not index.html's 1,300,000; the old "17 in 7 days (2.2 a day)" was 2.4 a day; at October's 2.4/day with the feed on the page, 1,300,000 lasts about 62 days after Phase 2, not 86. Measured 23 Oct ~23:00Z: deployed news.html 223,432 bytes sent as 32,172 gzip; results.html 1,303,283 as 86,414; GitHub Pages served gzip, no brotli. check_documentation, check_synopsis and check_pr_description passed.
