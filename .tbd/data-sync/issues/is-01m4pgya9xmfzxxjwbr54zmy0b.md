---
type: is
id: is-01m4pgya9xmfzxxjwbr54zmy0b
title: "PR #512 A3: audit_n40_new_supports copies T-145 checks and lost the empty-stderr and tau-bounds guards"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4pgxrs8s333vbdgpxw6c1w7
hold: null
hold_until: null
created_at: 2026-10-11T22:22:10.748Z
updated_at: 2026-10-11T23:24:05.169Z
started_at: 2026-10-11T22:23:17.573Z
closed_at: 2026-10-11T23:24:05.168Z
close_reason: "fixed in 286326fd9 (option a: T-145 finite checks take a Release; both guards restored; T-145 receipts byte-identical); https://github.com/jlevy/squares/pull/512#issuecomment-6115070910"
resolution: null
duplicate_of: null
---
Medium. packing/devtools/audit_n40_new_supports.py:652-682,600-604 vs packing/devtools/audit_continuous_pose.py:828,705-708. Reuse the T-145 functions. PR #512, review https://github.com/jlevy/squares/pull/512#pullrequestreview-5485248489
