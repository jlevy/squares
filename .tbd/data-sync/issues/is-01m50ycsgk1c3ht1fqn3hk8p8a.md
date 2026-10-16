---
type: is
id: is-01m50ycsgk1c3ht1fqn3hk8p8a
title: "PR #630 A1: release.py RELEASE_NO_PUBLIC_CHANGES head-entry conflict with #625"
kind: bug
status: open
priority: 3
version: 5
delegate: tbd-moderate-addresser-ee8en33t
labels: []
dependencies: []
parent_id: is-01m50wdx4ytqyqrhnqsebt2mbq
hold: null
hold_until: null
created_at: 2026-10-15T23:29:40.883Z
updated_at: 2026-10-16T00:02:17.847Z
started_at: 2026-10-15T23:29:47.493Z
---
Low. Both #625 and #630 add an entry at the head of RELEASE_NO_PUBLIC_CHANGES (packing/src/sqpack/release.py:987); git merge-tree reports a content conflict. Coordinator: merge order #626, #625, #630; resolved at merge time by merging main and keeping both entries. Review: https://github.com/jlevy/squares/pull/630#pullrequestreview-5541123708

## Notes

Deferred (PR #630 review A, A1): resolved at merge time by merging main and keeping both entries. After #626 and #625 land, the coordinator merges main into #630, keeps both RELEASE_NO_PUBLIC_CHANGES head entries (each a distinct fresh record with its own reason), and re-runs check_release_impact --baseline-ref origin/main. Same conflict as think-eiu9 (PR #625 A3).
