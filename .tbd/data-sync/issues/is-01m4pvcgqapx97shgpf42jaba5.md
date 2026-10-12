---
type: is
id: is-01m4pvcgqapx97shgpf42jaba5
title: "PR #512 B4: 41 of 67 finite checks are failed by no control and named in no test"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4pvbzwtey75pwyt8pwk5pzr
hold: null
hold_until: null
created_at: 2026-10-12T01:24:41.833Z
updated_at: 2026-10-12T02:48:44.066Z
started_at: 2026-10-12T01:33:20.423Z
closed_at: 2026-10-12T02:48:44.066Z
close_reason: "Fixed in 68aef9be6/bde21d708 on PR #512; dispositions https://github.com/jlevy/squares/pull/512#issuecomment-6116848163"
resolution: null
duplicate_of: null
---
Low. packing/devtools/audit_n40_new_supports.py:417-497; packing/tests/test_audit_n40_new_supports.py. Fix: parametrized receipt-mutant test per top-level block of verification.json and per slab-row field, each expecting its named check to fail; one in-K density mutant (box past L) expecting 'every box is a proper rectangle in K'. Review: https://github.com/jlevy/squares/pull/512#pullrequestreview-5485844215
