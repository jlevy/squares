---
type: is
id: is-01m4eehxmyz5pmqam04xs0fw2q
title: "Fix CI and verify mergeability for packing-methods PR #458"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-08T19:06:31.965Z
updated_at: 2026-10-08T19:08:39.295Z
started_at: 2026-10-08T19:08:39.292Z
---
User request: fix CI and make sure it is mergeable. Continue W8 documentation repair on codex/packing-methods. CI suite-a reports README.md missing packing-methods.md from its layout tree, although the navigation link is present. Restore the documented layout contract, reproduce and pass the failed checker/control, review the change, push, and wait for applicable CI to pass at the exact final head. Verify clean mergeability into main without merging. Preserve the original research checkout and unrelated work.
