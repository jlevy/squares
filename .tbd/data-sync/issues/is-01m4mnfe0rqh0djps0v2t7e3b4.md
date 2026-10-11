---
type: is
id: is-01m4mnfe0rqh0djps0v2t7e3b4
title: "PR #496 E2: progress-conditional fetch call shaped by test doubles"
kind: bug
status: in_progress
priority: 3
version: 2
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mneswbxt0m4w1caxy0x320
hold: null
hold_until: null
created_at: 2026-10-11T05:02:57.046Z
updated_at: 2026-10-11T05:03:50.164Z
started_at: 2026-10-11T05:03:50.163Z
---
Low. packing/devtools/check_published_site.py:1569-1573 branches on progress only because test doubles (tests/test_check_published_site.py:355 fake_site.fetch and the double at :728) do not accept on_retry. Fix: always pass on_retry and widen the doubles' signatures. PR #496, review E: https://github.com/jlevy/squares/pull/496#pullrequestreview-5481683586
