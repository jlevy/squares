---
type: is
id: is-01m44q9r9vg4qqmt52v1s63kqt
title: "PR #325 A5 (Low): hard-coded bin count."
kind: task
status: closed
priority: 2
version: 3
delegate: graph_gate
labels: []
dependencies: []
parent_id: is-01m44q74w8x5z0b69hev8yr4d7
hold: null
hold_until: null
created_at: 2026-10-05T00:26:57.210Z
updated_at: 2026-10-05T00:53:37.143Z
started_at: 2026-10-05T00:27:47.066Z
closed_at: 2026-10-05T00:53:37.142Z
close_reason: A5 fixed in17d43/56d5;11focusedtests+lint/types/recordchecks pass. HostedCI terminal blockedby inheritedparentdrift, explicitreceipt.
resolution: null
duplicate_of: null
---
https://github.com/jlevy/squares/pull/325#pullrequestreview-5408660666

**A5 (Low): hard-coded bin count.**
- `packing/tests/test_hull_kernel_caches.py:177-178` hard-codes 8 instead of reading `bins=8` from line 174.

Authorized maintenance only. Disposition requires evidence and exact-head CI; no research follow-up reserved.
