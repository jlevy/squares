---
type: is
id: is-01m4qbx67ejh3p3pjg5ar2dkyj
title: "PR #512 C1: no test holds the crate decision to the derived input (== derived mutant survives)"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4qbwvsj8cz41qmdkx6gxykx
hold: null
hold_until: null
created_at: 2026-10-12T06:13:25.358Z
updated_at: 2026-10-12T06:28:16.699Z
started_at: 2026-10-12T06:13:35.988Z
closed_at: 2026-10-12T06:28:16.698Z
close_reason: "fixed in ef244c575: P1 test; drop-derived mutant killed"
resolution: null
duplicate_of: null
---
Medium. packing/devtools/audit_n40_new_supports.py:859; packing/tests/test_audit_n40_new_supports.py:324-363. Removing == derived passes all 99 tests and probe P1 (D3's density, same counts/expansion/mass, self-consistent digests) gives AXIS_STAGE_HOLDS. Add P1 as a test failing CRATE_DECISION. PR #512, https://github.com/jlevy/squares/pull/512#pullrequestreview-5487045374
