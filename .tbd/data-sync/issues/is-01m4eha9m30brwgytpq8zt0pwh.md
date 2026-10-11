---
type: is
id: is-01m4eha9m30brwgytpq8zt0pwh
title: "PR #456 review E1: correct stale artifact-waiter overlap documentation"
kind: bug
status: closed
priority: 3
version: 3
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4edxmfwe4ey36yag3yg9zz6
hold: null
hold_until: null
created_at: 2026-10-08T19:54:47.808Z
updated_at: 2026-10-08T21:37:25.543Z
started_at: 2026-10-08T19:59:11.810Z
closed_at: 2026-10-08T21:37:25.542Z
close_reason: Fixed in e047331e5ef17d6590ebd36d7c1b8aa4e0441372. Waiter introduction matches seven successful-producer dependencies and exact-attempt visibility semantics; strict600s acceptance deadline unchanged.23 author and23 independent waiter controls pass; final source independently reviewed in ReviewE5463107477 with marked disposition6069502067.
resolution: null
duplicate_of: null
---
Fresh independent Astra MAX follow-up E1 Low: wait_for_run_artifact.py module introduction still describes setup overlap removed by the seven native prepare dependencies. Correct the introduction to describe a post-producer exact-attempt visibility join, bounded polling and unchanged strict600s acceptance deadline. Patch prepared outside source pending completion of active push-floor snapshot, then focused23 waiter tests/lint and reviewer readback. No timeout or workflow guard change.
