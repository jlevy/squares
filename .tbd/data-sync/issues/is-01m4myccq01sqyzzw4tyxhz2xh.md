---
type: is
id: is-01m4myccq01sqyzzw4tyxhz2xh
title: "PR #406 A4: production failure path (exit 1 at real ceilings) never exercised by a test"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mybh5kcffr8zqzm2ajg86e
hold: null
hold_until: null
created_at: 2026-10-11T07:38:34.591Z
updated_at: 2026-10-11T18:58:29.070Z
started_at: 2026-10-11T07:39:11.063Z
closed_at: 2026-10-11T18:58:29.068Z
close_reason: "fixed in 0a4a69d5e: test_production_ceiling_rejects_one_byte_over_through_the_cli. Disposition: https://github.com/jlevy/squares/pull/406#issuecomment-6112530517"
resolution: null
duplicate_of: null
---
Medium. packing/tests/test_added_blob_guard.py:195-218 only tests tiny ceilings and a monkeypatched refusal. Review A: https://github.com/jlevy/squares/pull/406#pullrequestreview-5482287656 (PR #406).
