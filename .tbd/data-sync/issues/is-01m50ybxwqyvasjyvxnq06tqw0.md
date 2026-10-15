---
type: is
id: is-01m50ybxwqyvasjyvxnq06tqw0
title: "PR #625 A2: description render and hosted-check lines predate head 6b27985 over main 22a67ce4"
kind: bug
status: closed
priority: 3
version: 3
delegate: tbd-moderate-addresser-ee8en33t
labels: []
dependencies: []
parent_id: is-01m50ybhb03wd555pnyjhsx1e8
hold: null
hold_until: null
created_at: 2026-10-15T23:29:12.599Z
updated_at: 2026-10-15T23:44:23.103Z
started_at: 2026-10-15T23:29:47.454Z
closed_at: 2026-10-15T23:44:23.103Z
close_reason: "fixed in the PR #625 description: Validation records the render at 2e7f0de03 over main 22a67ce4 (42 files byte-identical, HTML b5b2222d, Markdown 06d4338c) and hosted checks at 2e7f0de03 (31 pass, 28 skipped, 0 fail; runs 38824459029, 38824459048, 38824453787). check_pr_description ok."
resolution: null
duplicate_of: null
---
Low. packing/src/sqpack/release.py:996 says 'Rendered on this branch over main 22a67ce4'; the PR description's render and hosted-check lines are at e93f6a804 over main 6e73ef1c2. Fix: record render at current head over 22a67ce4 and hosted checks at the current head. Review: https://github.com/jlevy/squares/pull/625#pullrequestreview-5541122607
