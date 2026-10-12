---
type: is
id: is-01m4pvcf4yd0f460f4xyxxx80m
title: "PR #512 B3: pose binary identity with T-145's CI binary is two equal literals compared nowhere"
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
created_at: 2026-10-12T01:24:40.221Z
updated_at: 2026-10-12T01:33:18.646Z
started_at: 2026-10-12T01:33:18.646Z
---
Low. packing/devtools/audit_n40_new_supports.py:151-154; integrity-ceremony.yaml. CI_BINARIES['pose'] equals audit_continuous_pose.CI_BINARIES['pose'] but nothing compares them. Fix: a check in kernel_checks reading both from their records, or a test. Review: https://github.com/jlevy/squares/pull/512#pullrequestreview-5485844215
