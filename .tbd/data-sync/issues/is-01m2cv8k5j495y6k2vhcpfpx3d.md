---
type: is
id: is-01m2cv8k5j495y6k2vhcpfpx3d
title: "PR #157 review READ-03: explicit empty counts erase the weighted declaration"
kind: bug
status: open
priority: 2
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:45.298Z
updated_at: 2026-09-13T07:38:45.298Z
---
threshold.py:300-302, packing/devtools/decide_threshold_certificate.py:123-127 and the orbit parser all turn 'multiplicities: []' into the constructor's omitted-count sentinel, so a tagged T025 atom becomes all ones and passes the strict reader's unweighted check. Fix: distinguish MISSING legacy data from MALFORMED declared weighted data; refuse weighted declarations at unweighted-only admission boundaries before normalization; reject null, unknown, mixed, empty and incomplete shapes through the documented error path.
