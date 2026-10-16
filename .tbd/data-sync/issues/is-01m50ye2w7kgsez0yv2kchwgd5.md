---
type: is
id: is-01m50ye2w7kgsez0yv2kchwgd5
title: "PR #627 B4: the stack must land and take main by merge commits; nothing on the stack says so"
kind: bug
status: closed
priority: 2
version: 3
delegate: ecstatic-edison-address-627
labels: []
dependencies: []
parent_id: is-01m50yc0efcxyyh72mesjv7t15
hold: null
hold_until: null
created_at: 2026-10-15T23:30:23.239Z
updated_at: 2026-10-16T00:13:37.051Z
started_at: 2026-10-15T23:30:49.193Z
closed_at: 2026-10-16T00:13:37.051Z
close_reason: "fixed in the PR #627 description (Landing) and the review B reply"
resolution: null
duplicate_of: null
---
Low. PR #627, review B (https://github.com/jlevy/squares/pull/627#pullrequestreview-5541117145). PUBLICATION_REVISION 5791b79b and DATA_REVISION are branch commits. Fix: state on #627 that the stack lands with gh stack merge 631 --merge --yes and takes main by merge commits, never gh stack sync.
