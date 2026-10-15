---
type: is
id: is-01m50ycsgk1c3ht1fqn3hk8p8a
title: "PR #630 A1: release.py RELEASE_NO_PUBLIC_CHANGES head-entry conflict with #625"
kind: bug
status: in_progress
priority: 3
version: 2
delegate: tbd-moderate-addresser-ee8en33t
labels: []
dependencies: []
parent_id: is-01m50ycgh45vrr9zhdqy32kexy
hold: null
hold_until: null
created_at: 2026-10-15T23:29:40.883Z
updated_at: 2026-10-15T23:29:47.493Z
started_at: 2026-10-15T23:29:47.493Z
---
Low. Both #625 and #630 add an entry at the head of RELEASE_NO_PUBLIC_CHANGES (packing/src/sqpack/release.py:987); git merge-tree reports a content conflict. Coordinator: merge order #626, #625, #630; resolved at merge time by merging main and keeping both entries. Review: https://github.com/jlevy/squares/pull/630#pullrequestreview-5541123708
