---
type: is
id: is-01m5kj4xmqyc7tkp4vb2w434mt
title: "PR #736 A10: an unstamped row source crashes the overview render; an unstamped house is silently skipped"
kind: bug
status: closed
priority: 2
version: 3
delegate: c-addr-736-1023
labels: []
dependencies: []
parent_id: is-01m5khvkc9y6prw31wexsamsc4
hold: null
hold_until: null
created_at: 2026-10-23T05:01:14.263Z
updated_at: 2026-10-23T06:11:33.175Z
started_at: 2026-10-23T05:01:19.284Z
closed_at: 2026-10-23T06:11:33.175Z
close_reason: "Fixed in 79abd064d (option 1): beyond_rows skips a source with no landing, as house_moves skips a house; the landing test stays the CI gate. test_an_unstamped_house_or_source_is_left_out_and_the_render_carries_on fails with KeyError 'couzo-index-2026-10-15' with the fix reverted, passes with it."
resolution: null
duplicate_of: null
---
Medium. packing/devtools/overview_sections.py beyond_rows read landed[source['id']] for every source with rows (KeyError on a source with no landing); house_moves iterates the landing record so a missing house is left out. Review A round 2 of PR #736: https://github.com/jlevy/squares/pull/736#issuecomment-6356372182
