---
type: is
id: is-01m5mwbn450xgwq4mgjnrpn0jm
title: Plan the News page toggle (notable stories / all changes by PR), the merged-PR record and the S3+ News process
kind: task
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-23-news-pr-feed.md
delegate: c-news-plan-1023
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T17:18:55.109Z
updated_at: 2026-10-23T18:09:54.007Z
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
