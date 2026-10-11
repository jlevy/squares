---
type: is
id: is-01m4myd1r991kj66tppaefvaz9
title: "PR #406 A9: derive refusal messages from the constants"
kind: bug
status: closed
priority: 3
version: 3
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mybh5kcffr8zqzm2ajg86e
hold: null
hold_until: null
created_at: 2026-10-11T07:38:56.136Z
updated_at: 2026-10-11T18:58:31.661Z
started_at: 2026-10-11T07:39:19.739Z
closed_at: 2026-10-11T18:58:31.660Z
close_reason: "fixed in 0a4a69d5e: messages formatted from MAX_SECONDS, MAX_QUERY_SECONDS, MAX_METADATA_BYTES. Disposition: https://github.com/jlevy/squares/pull/406#issuecomment-6112530517"
resolution: null
duplicate_of: null
---
Suggestion. check_added_blobs.py:49,81,83 hardcode 30 seconds and 4 MiB. Review A: https://github.com/jlevy/squares/pull/406#pullrequestreview-5482287656 (PR #406).
