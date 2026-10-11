---
type: is
id: is-01m4mycs5gyh74ystfyt32wy3j
title: "PR #406 A7: an LFS pointer is a one-line bypass of the gate"
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
created_at: 2026-10-11T07:38:47.339Z
updated_at: 2026-10-11T18:58:30.569Z
started_at: 2026-10-11T07:39:16.163Z
closed_at: 2026-10-11T18:58:30.564Z
close_reason: "fixed in 0a4a69d5e: LFS pointers refused. Disposition: https://github.com/jlevy/squares/pull/406#issuecomment-6112530517"
resolution: null
duplicate_of: null
---
Low. packing/tests/test_added_blob_guard.py:146-157 pins that a pointer declaring size 999999999 passes; development.md:1853. Review A: https://github.com/jlevy/squares/pull/406#pullrequestreview-5482287656 (PR #406).
