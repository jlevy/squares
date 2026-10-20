---
type: is
id: is-01m50ybwackdfh5dhv3capaznp
title: "PR #625 A1: #534 reply says replays took 3.3 to 6.1 CPU-hours though none ran"
kind: bug
status: closed
priority: 1
version: 3
delegate: tbd-moderate-addresser-ee8en33t
labels: []
dependencies: []
parent_id: is-01m50ybhb03wd555pnyjhsx1e8
hold: null
hold_until: null
created_at: 2026-10-15T23:29:10.987Z
updated_at: 2026-10-15T23:41:22.143Z
started_at: 2026-10-15T23:29:47.449Z
closed_at: 2026-10-15T23:41:22.143Z
close_reason: "fixed in 2e7f0de03 on PR #625 (fix a): #534 comment 6200836218 edited in place at 2026-10-15T23:30:26Z to 'were priced at 3.3 to 6.1 CPU-hours from the T-142 and T-143 smoke runs; none has run yet' with a visible Edited note; #534 entry notes record the edit; release reason counts five notes. Confirmed: API read-back of the comment, check_requests gate 0, --report #534 reply due no, survey render byte-identical (42 files), packing-validate --records exit 0."
resolution: null
duplicate_of: null
---
Medium. packing/campaign/result-requests.yaml:6690 records https://github.com/jlevy/squares/issues/534#issuecomment-6200836218, which says replays of this kind 'took 3.3 to 6.1 CPU-hours by the T-142 and T-143 measurements'. None ran; those are the 11 October prep lane's prices from smoke runs (think-i85v). Review: https://github.com/jlevy/squares/pull/625#pullrequestreview-5541122607. Coordinator chose fix (a): edit the comment under github-editing and record the in-place correction on the #534 entry.
