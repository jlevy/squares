---
type: is
id: is-01m5kj4xmqyc7tkp4vb2w434mt
title: "PR #736 A10: an unstamped row source crashes the overview render; an unstamped house is silently skipped"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: c-addr-736-1023
labels: []
dependencies: []
parent_id: is-01m5khvkc9y6prw31wexsamsc4
hold: null
hold_until: null
created_at: 2026-10-23T05:01:14.263Z
updated_at: 2026-10-23T05:01:19.284Z
started_at: 2026-10-23T05:01:19.284Z
---
Medium. packing/devtools/overview_sections.py beyond_rows read landed[source['id']] for every source with rows (KeyError on a source with no landing); house_moves iterates the landing record so a missing house is left out. Review A round 2 of PR #736: https://github.com/jlevy/squares/pull/736#issuecomment-6356372182
