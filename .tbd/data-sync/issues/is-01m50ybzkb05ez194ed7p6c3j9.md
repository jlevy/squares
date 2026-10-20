---
type: is
id: is-01m50ybzkb05ez194ed7p6c3j9
title: "PR #625 A3: release.py RELEASE_NO_PUBLIC_CHANGES head-entry conflict with #630"
kind: bug
status: closed
priority: 3
version: 6
delegate: tbd-moderate-addresser-ee8en33t
labels: []
dependencies: []
parent_id: is-01m50wdx4ytqyqrhnqsebt2mbq
hold: null
hold_until: null
created_at: 2026-10-15T23:29:14.347Z
updated_at: 2026-10-16T02:09:29.481Z
started_at: 2026-10-15T23:29:47.458Z
closed_at: 2026-10-16T02:09:29.481Z
close_reason: "Resolved at merge time: #626 merged at 22c0ebf0d and #625 at ee9cec6ea; main ee9cec6ea was merged into #630 at de19ec62a, where the RELEASE_NO_PUBLIC_CHANGES head-entry conflict was resolved by keeping both entries (#630's first, #625's after it). #630's survey entry was restated over ee9cec6e at 9fdb59ff8 after a fresh render (42/42 files byte-identical); check_release_impact --baseline-ref origin/main, release_pin --check, check_requests, packing-validate --records and the release/requests tests pass, and hosted CI on #630 at 9fdb59ff8 is green (pass=31, skipping=28). Neither branch was merged into the other."
resolution: null
duplicate_of: null
---
Low. Both #625 and #630 add an entry at the head of RELEASE_NO_PUBLIC_CHANGES (packing/src/sqpack/release.py:987); git merge-tree reports a content conflict. Coordinator: merge order #626, #625, #630; resolved at merge time by merging main and keeping both entries. Review: https://github.com/jlevy/squares/pull/625#pullrequestreview-5541122607

## Notes

Deferred (PR #625 review A, A3): resolved at merge time by merging main and keeping both entries. Planned merge order #626, #625, #630, so the conflict lands on #630 (think-2878, PR #630 A1): the coordinator merges main into #630 after #625 lands, keeps both RELEASE_NO_PUBLIC_CHANGES head entries, and re-runs check_release_impact --baseline-ref origin/main. Close both when that merge is pushed. Neither branch was merged into the other.
