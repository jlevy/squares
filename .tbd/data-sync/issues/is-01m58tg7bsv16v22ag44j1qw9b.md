---
type: is
id: is-01m58tg7bsv16v22ag44j1qw9b
title: "PR #676: synchronize POSIX TERM-ignore timeout control with child readiness"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m578snhcmb9xf25bnb3atvy8
hold: null
hold_until: null
created_at: 2026-10-19T00:55:34.520Z
updated_at: 2026-10-19T00:55:43.671Z
started_at: 2026-10-19T00:55:43.670Z
---
The 19 October isolated --push gate reached the pool-heavy lane after 18,977 normal tests passed. test_timeout_kills_term_ignoring_group then received -SIGTERM instead of -SIGKILL: the child had not printed its ready marker or installed SIG_IGN before the 0.2-second wall timer began. A test-only readiness handshake and a 0.3-second startup regression are prepared in packing/tests/test_supervise_posix.py; the production timeout and signal behavior remain unchanged. Re-run focused controls and the complete exact-head push gate before claiming qualification. Failed gate log retained at agent-source/squares-pr676-qualification-20261019/push-gate-failed.log.
