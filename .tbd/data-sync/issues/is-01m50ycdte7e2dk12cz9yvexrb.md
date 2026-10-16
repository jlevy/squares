---
type: is
id: is-01m50ycdte7e2dk12cz9yvexrb
title: "PR #626 A1: #523 ask blocked_on lacks think-kok7 for the n = 19 part"
kind: bug
status: closed
priority: 3
version: 3
delegate: tbd-moderate-addresser-ee8en33t
labels: []
dependencies: []
parent_id: is-01m50yc6hrcb9bzwnns4yh4a7k
hold: null
hold_until: null
created_at: 2026-10-15T23:29:28.910Z
updated_at: 2026-10-15T23:41:23.030Z
started_at: 2026-10-15T23:29:47.477Z
closed_at: 2026-10-15T23:41:23.030Z
close_reason: "fixed in 836c95d36 on PR #626: #523 ask blocked_on is [think-x4v4, think-kok7]. Confirmed: check_requests gate 0, --report #523 reply due no, packing-validate --records exit 0."
resolution: null
duplicate_of: null
---
Low. The ask note at packing/campaign/result-requests.yaml:6285 says the n = 19 part waits on a budget and the leaf-rule review (think-kok7); blocked_on (:6288) names only think-x4v4. Fix (pick one): add think-kok7 to blocked_on, or split the ask. Review: https://github.com/jlevy/squares/pull/626#pullrequestreview-5541123578
