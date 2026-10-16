---
type: is
id: is-01m51bfrmwpzgxr6ff30v29wr2
title: "PR #637 A4: the holds on #570 and #574 are not recorded where the PR says"
kind: bug
status: closed
priority: 2
version: 3
delegate: ecstatic-edison-replies-stack
labels: []
dependencies: []
parent_id: is-01m51bf8swfxxv0hbffaxdzk0r
hold: null
hold_until: null
created_at: 2026-10-16T03:18:29.788Z
updated_at: 2026-10-16T04:03:56.690Z
started_at: 2026-10-16T03:18:35.869Z
closed_at: 2026-10-16T04:03:56.690Z
close_reason: "fixed in 66e8be69e: holds on #570 and #574 and what releases them noted in both entries and on think-rfce and think-9v2k. Dispositions: https://github.com/jlevy/squares/pull/637#issuecomment-6207805231"
resolution: null
duplicate_of: null
---
Low. result-requests.yaml:7900 (#570), :8060 (#574). The PR description gives defer-dependency owner (think-rfce, think-9v2k) but neither bead nor entry records the hold; --report shows both reply due, so the next pass would post them. Record each hold and what releases it on the beads and in the entries' notes, or post the due replies. https://github.com/jlevy/squares/pull/637#pullrequestreview-5542558537
