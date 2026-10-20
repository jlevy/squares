---
type: is
id: is-01m4mnfzymh73a49sb5qp6n7ab
title: "PR #496 F2: fetch_once lets TimeoutError and other connection errors escape unretried"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mneswbxt0m4w1caxy0x320
hold: null
hold_until: null
created_at: 2026-10-11T05:03:15.412Z
updated_at: 2026-10-12T23:39:05.584Z
started_at: 2026-10-11T05:03:47.515Z
closed_at: 2026-10-12T23:39:05.584Z
close_reason: "Completed: PR #496 review finding F2 fixed in PR #507 (merged, e96e9ea95)."
resolution: null
duplicate_of: null
---
Medium, pre-existing. packing/devtools/check_published_site.py:1249-1262 (fetch_once), 1265-1287 (fetch). A header timeout raises TimeoutError, a dropped connection ConnectionResetError or http.client.HTTPException; nothing catches them and the audit crashes. Fix: map them to status 0 (transient, retried); controlled test with a server that delays its headers. PR #496, review F: https://github.com/jlevy/squares/pull/496#pullrequestreview-5481911429
