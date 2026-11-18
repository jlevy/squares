---
type: is
id: is-01m7nyxcvzfqbte9ch3r6q7q6y
title: "PR #909 A1: main moved twice; the head no longer merges"
kind: bug
status: closed
priority: 3
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m7nyxbsr24nq3xkfk7djkx9d
hold: null
hold_until: null
created_at: 2026-11-17T23:54:11.711Z
updated_at: 2026-11-18T02:42:34.603Z
started_at: 2026-11-18T00:44:56.727Z
closed_at: 2026-11-18T02:42:34.603Z
close_reason: "Fixed: main merged four times (249d11db8, 27f56bcff, dd5f1affd, eda3ee5cd), no-change records against each main, re-pinned last 5d931e1a0; dispositions https://github.com/jlevy/squares/pull/909#issuecomment-6966950958; #909 merged a1a8d0aae."
resolution: null
duplicate_of: null
---
High. release.py:802, test_check_requests.py:2096-2122; fresh no-change record after #908 merges. Review A (senior, round 1) of PR #909 at 03dce2355: https://github.com/jlevy/squares/pull/909#issuecomment-6964495841
