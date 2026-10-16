---
type: is
id: is-01m51bfrmwpzgxr6ff30v29wr2
title: "PR #637 A4: the holds on #570 and #574 are not recorded where the PR says"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: ecstatic-edison-replies-stack
labels: []
dependencies: []
parent_id: is-01m51bf8swfxxv0hbffaxdzk0r
hold: null
hold_until: null
created_at: 2026-10-16T03:18:29.788Z
updated_at: 2026-10-16T03:18:35.869Z
started_at: 2026-10-16T03:18:35.869Z
---
Low. result-requests.yaml:7900 (#570), :8060 (#574). The PR description gives defer-dependency owner (think-rfce, think-9v2k) but neither bead nor entry records the hold; --report shows both reply due, so the next pass would post them. Record each hold and what releases it on the beads and in the entries' notes, or post the due replies. https://github.com/jlevy/squares/pull/637#pullrequestreview-5542558537
