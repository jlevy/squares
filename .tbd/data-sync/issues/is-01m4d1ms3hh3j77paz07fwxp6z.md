---
type: is
id: is-01m4d1ms3hh3j77paz07fwxp6z
title: C9 Preserve legacy result fragments through the homepage filter link
kind: bug
status: in_progress
priority: 1
version: 2
assignee: codex
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
hold: null
hold_until: null
created_at: 2026-10-08T06:01:39.696Z
updated_at: 2026-10-08T06:01:51.746Z
started_at: 2026-10-08T06:01:51.745Z
---
The static homepage copies supported filter query keys into its All Results link but drops the result-row hash. Preserve known result fragments through a real click, keep unsupported query keys out, and verify that the destination reveals the requested row even when filters exclude it. Retain complete-results default, keyboard, count, and layout checks; move browser coverage into the installed Chromium frontend lane.
