---
type: is
id: is-01m4qbx7ecz4v9s7rhkaw3kvgp
title: "PR #512 C2: manifest-hash clause of retained_alike survives mutation"
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
created_at: 2026-10-12T06:13:26.603Z
updated_at: 2026-10-12T06:28:17.708Z
started_at: 2026-10-12T06:13:36.654Z
closed_at: 2026-10-12T06:28:17.707Z
close_reason: "fixed in ef244c575: both-copies KERNEL_CHANGES case; drop-manifest-hash mutant killed"
resolution: null
duplicate_of: null
---
Low. packing/devtools/audit_n40_new_supports.py:403-407 (retained_alike); packing/tests/test_audit_n40_new_supports.py:407. Add a KERNEL_CHANGES case changing both packets' copies of one shared file the same way. PR #512, https://github.com/jlevy/squares/pull/512#pullrequestreview-5487045374
