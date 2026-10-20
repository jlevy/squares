---
type: is
id: is-01m4wzs72rh8db5f4mp5y8w4wr
title: Keep shared atlas construction within measured test calls
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-14T10:36:58.839Z
updated_at: 2026-10-14T10:37:16.675Z
started_at: 2026-10-14T10:37:16.673Z
---
PR599 performance review B1: eager module fixture places both atlas renders in unmeasured setup. Keep genuine shared immutable outputs but return a bounded lazy memoized callable invoked by test bodies, preserving call-phase cost signals, all assertions and unchanged ceilings.
