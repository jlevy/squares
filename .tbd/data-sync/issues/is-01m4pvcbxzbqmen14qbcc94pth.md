---
type: is
id: is-01m4pvcbxzbqmen14qbcc94pth
title: "PR #512 B1: check-axis does not bind the crate's decision to the density"
kind: bug
status: closed
priority: 1
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4pvbzwtey75pwyt8pwk5pzr
hold: null
hold_until: null
created_at: 2026-10-12T01:24:36.927Z
updated_at: 2026-10-12T02:48:41.791Z
started_at: 2026-10-12T01:33:14.432Z
closed_at: 2026-10-12T02:48:41.790Z
close_reason: "Fixed in 68aef9be6/bde21d708 on PR #512; dispositions https://github.com/jlevy/squares/pull/512#issuecomment-6116848163"
resolution: null
duplicate_of: null
---
Medium. packing/devtools/audit_n40_new_supports.py:793-821 (axis_stage_checks); compare packing/devtools/audit_continuous_pose.py:2020-2033 (crate_premises). CRATE_DECISION reads neither crate.input_sha256 nor premises.input_sha256, nor L, n, expanded_rectangles. Fix: require both digests equal facts().crate_sha256['axis-A'], premises L == text(CLAIM.L), n == CLAIM.n, expanded_rectangles == f.distinct; mutant test (foreign digests, L=1, n=1, one expanded rectangle must fail); regenerate receipts/axis-check.json only if detail changes; extend the integrity-ceremony boundary text. Review: https://github.com/jlevy/squares/pull/512#pullrequestreview-5485844215
