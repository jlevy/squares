---
type: is
id: is-01m4pvcdnpvyaanhv7f5kjfbe8
title: "PR #512 B2: kernel_checks holds for a shared path absent from both manifests"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4pvbzwtey75pwyt8pwk5pzr
hold: null
hold_until: null
created_at: 2026-10-12T01:24:38.709Z
updated_at: 2026-10-12T01:33:17.119Z
started_at: 2026-10-12T01:33:17.118Z
---
Low. packing/devtools/audit_n40_new_supports.py:403. ours.get(path) == theirs.get(path) is None == None for a path in neither manifest. Fix: path in ours and ours[path] == theirs.get(path). Review: https://github.com/jlevy/squares/pull/512#pullrequestreview-5485844215
