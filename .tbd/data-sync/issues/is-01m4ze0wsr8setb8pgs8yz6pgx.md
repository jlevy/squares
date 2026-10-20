---
type: is
id: is-01m4ze0wsr8setb8pgs8yz6pgx
title: "PR 614 B9: test comment at test_house_adoption.py:281 contradicts its assertion"
kind: chore
status: closed
priority: 3
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4yz7whq6kvpef88k4dwj8z5
hold: null
hold_until: null
created_at: 2026-10-15T09:24:19.384Z
updated_at: 2026-10-15T09:46:35.610Z
started_at: 2026-10-15T09:24:25.197Z
closed_at: 2026-10-15T09:46:35.610Z
close_reason: "Fixed in 6133c4877: comment reworded to match unread == []."
resolution: null
duplicate_of: null
---
The comment says the entry is named unread; the assertion checks unread == []. Reword.
