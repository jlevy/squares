---
type: is
id: is-01m4qbx8kyas0phptqrhgx623j
title: "PR #512 C3: check-axis does not hold the candidate to CANDIDATE_SHA256"
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
created_at: 2026-10-12T06:13:27.806Z
updated_at: 2026-10-12T06:28:18.580Z
started_at: 2026-10-12T06:13:37.397Z
closed_at: 2026-10-12T06:28:18.580Z
close_reason: "fixed in ef244c575: density.sha256 == CANDIDATE_SHA256 in CRATE_DECISION; P2 test"
resolution: null
duplicate_of: null
---
Low. packing/devtools/audit_n40_new_supports.py:848, :891-893. Probe P2: candidate replaced by D3 with matching crate block holds. Add density.sha256 == CANDIDATE_SHA256 to CRATE_DECISION with a test from P2. PR #512, https://github.com/jlevy/squares/pull/512#pullrequestreview-5487045374
