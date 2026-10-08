---
type: is
id: is-01m4eha9m30brwgytpq8zt0pwh
title: "PR #456 review E1: correct stale artifact-waiter overlap documentation"
kind: bug
status: in_progress
priority: 3
version: 2
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4edxmfwe4ey36yag3yg9zz6
hold: null
hold_until: null
created_at: 2026-10-08T19:54:47.808Z
updated_at: 2026-10-08T19:59:11.812Z
started_at: 2026-10-08T19:59:11.810Z
---
Fresh independent Astra MAX follow-up E1 Low: wait_for_run_artifact.py module introduction still describes setup overlap removed by the seven native prepare dependencies. Correct the introduction to describe a post-producer exact-attempt visibility join, bounded polling and unchanged strict600s acceptance deadline. Patch prepared outside source pending completion of active push-floor snapshot, then focused23 waiter tests/lint and reviewer readback. No timeout or workflow guard change.
