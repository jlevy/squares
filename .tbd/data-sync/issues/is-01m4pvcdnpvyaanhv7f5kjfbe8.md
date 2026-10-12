---
type: is
id: is-01m4pvcdnpvyaanhv7f5kjfbe8
title: "PR #512 B2: kernel_checks holds for a shared path absent from both manifests"
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
created_at: 2026-10-12T01:24:38.709Z
updated_at: 2026-10-12T02:48:42.548Z
started_at: 2026-10-12T01:33:17.118Z
closed_at: 2026-10-12T02:48:42.548Z
close_reason: "Fixed in 68aef9be6/bde21d708 on PR #512; dispositions https://github.com/jlevy/squares/pull/512#issuecomment-6116848163"
resolution: null
duplicate_of: null
---
Low. packing/devtools/audit_n40_new_supports.py:403. ours.get(path) == theirs.get(path) is None == None for a path in neither manifest. Fix: path in ours and ours[path] == theirs.get(path). Review: https://github.com/jlevy/squares/pull/512#pullrequestreview-5485844215
