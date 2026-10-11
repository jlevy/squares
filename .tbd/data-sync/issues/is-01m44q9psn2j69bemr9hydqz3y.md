---
type: is
id: is-01m44q9psn2j69bemr9hydqz3y
title: "PR #325 A3 (Medium): a shared helper lives in a one-off profiling script."
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
created_at: 2026-10-05T00:26:55.668Z
updated_at: 2026-10-05T00:53:35.782Z
started_at: 2026-10-05T00:27:47.060Z
closed_at: 2026-10-05T00:53:35.781Z
close_reason: A3 fixed in17d43/56d5;11focusedtests+lint/types/recordchecks pass. HostedCI terminal blockedby inheritedparentdrift, explicitreceipt.
resolution: null
duplicate_of: null
---
https://github.com/jlevy/squares/pull/325#pullrequestreview-5408660666

**A3 (Medium): a shared helper lives in a one-off profiling script.**
- `peak_memory_bytes` is in `packing/devtools/profile_n17_partner_memo.py`, and all 8 of #333's probes import it from there.
- **Fix:** move it to a small shared module.

Authorized maintenance only. Disposition requires evidence and exact-head CI; no research follow-up reserved.
