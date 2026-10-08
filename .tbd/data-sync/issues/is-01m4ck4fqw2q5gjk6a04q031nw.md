---
type: is
id: is-01m4ck4fqw2q5gjk6a04q031nw
title: "D1: validate Host and Origin on the local browser-test server"
kind: bug
status: in_progress
priority: 2
version: 3
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
hold: null
hold_until: null
created_at: 2026-10-08T01:48:05.755Z
updated_at: 2026-10-08T11:19:55.182Z
started_at: 2026-10-08T01:49:34.673Z
---
Independent security review confirmed arbitrary Host and Origin headers are accepted by the new loopback server. Require the actual loopback authority and reject foreign origins before serving GET or HEAD; retain same-origin browser tests.
