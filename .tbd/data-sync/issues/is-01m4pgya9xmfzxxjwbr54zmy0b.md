---
type: is
id: is-01m4pgya9xmfzxxjwbr54zmy0b
title: "PR #512 A3: audit_n40_new_supports copies T-145 checks and lost the empty-stderr and tau-bounds guards"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4pgxrs8s333vbdgpxw6c1w7
hold: null
hold_until: null
created_at: 2026-10-11T22:22:10.748Z
updated_at: 2026-10-11T22:23:17.573Z
started_at: 2026-10-11T22:23:17.573Z
---
Medium. packing/devtools/audit_n40_new_supports.py:652-682,600-604 vs packing/devtools/audit_continuous_pose.py:828,705-708. Reuse the T-145 functions. PR #512, review https://github.com/jlevy/squares/pull/512#pullrequestreview-5485248489
