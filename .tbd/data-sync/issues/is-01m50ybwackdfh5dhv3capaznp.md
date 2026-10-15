---
type: is
id: is-01m50ybwackdfh5dhv3capaznp
title: "PR #625 A1: #534 reply says replays took 3.3 to 6.1 CPU-hours though none ran"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: tbd-moderate-addresser-ee8en33t
labels: []
dependencies: []
parent_id: is-01m50ybhb03wd555pnyjhsx1e8
hold: null
hold_until: null
created_at: 2026-10-15T23:29:10.987Z
updated_at: 2026-10-15T23:29:47.449Z
started_at: 2026-10-15T23:29:47.449Z
---
Medium. packing/campaign/result-requests.yaml:6690 records https://github.com/jlevy/squares/issues/534#issuecomment-6200836218, which says replays of this kind 'took 3.3 to 6.1 CPU-hours by the T-142 and T-143 measurements'. None ran; those are the 11 October prep lane's prices from smoke runs (think-i85v). Review: https://github.com/jlevy/squares/pull/625#pullrequestreview-5541122607. Coordinator chose fix (a): edit the comment under github-editing and record the in-place correction on the #534 entry.
