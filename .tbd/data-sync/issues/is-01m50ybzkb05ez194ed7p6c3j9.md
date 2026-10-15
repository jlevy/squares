---
type: is
id: is-01m50ybzkb05ez194ed7p6c3j9
title: "PR #625 A3: release.py RELEASE_NO_PUBLIC_CHANGES head-entry conflict with #630"
kind: bug
status: open
priority: 3
version: 4
delegate: tbd-moderate-addresser-ee8en33t
labels: []
dependencies: []
parent_id: is-01m50ybhb03wd555pnyjhsx1e8
hold: null
hold_until: null
created_at: 2026-10-15T23:29:14.347Z
updated_at: 2026-10-15T23:41:51.225Z
started_at: 2026-10-15T23:29:47.458Z
---
Low. Both #625 and #630 add an entry at the head of RELEASE_NO_PUBLIC_CHANGES (packing/src/sqpack/release.py:987); git merge-tree reports a content conflict. Coordinator: merge order #626, #625, #630; resolved at merge time by merging main and keeping both entries. Review: https://github.com/jlevy/squares/pull/625#pullrequestreview-5541122607

## Notes

Deferred (PR #625 review A, A3): resolved at merge time by merging main and keeping both entries. Planned merge order #626, #625, #630, so the conflict lands on #630 (think-2878, PR #630 A1): the coordinator merges main into #630 after #625 lands, keeps both RELEASE_NO_PUBLIC_CHANGES head entries, and re-runs check_release_impact --baseline-ref origin/main. Close both when that merge is pushed. Neither branch was merged into the other.
