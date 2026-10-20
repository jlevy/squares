---
type: is
id: is-01m4xk1h2skppdp58y4zr0kvph
title: Remove repeated work in real atlas pool-worker byte comparison
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-14T16:13:34.167Z
updated_at: 2026-10-14T16:14:48.216Z
started_at: 2026-10-14T16:14:48.214Z
---
Actual required-browser checkpoint 38594336170 at 58b6a868 fails test_known_best_atlas::test_a_pool_worker_builds_the_same_bytes_as_this_process at 14.45 seconds CALL against the unchanged 12-second limit. Preserve the real multiprocessing comparison and all assertions; optimize measured repeated work and rerun strict current-head proof.
