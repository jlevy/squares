---
type: is
id: is-01m2cm9t0y38gyjk0saamcf6jm
title: Reject malformed numeric suffixes in synopsis lower-bound validation
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2cge1zdgenaswpf8nmd9fmv
created_at: 2026-09-13T05:37:05.053Z
updated_at: 2026-09-13T05:46:26.256Z
closed_at: 2026-09-13T05:46:26.255Z
close_reason: Fixed in b43d3011 and propagated through PR149 236132e7 and PR156 0aa5abfc. Four malformed suffix controls failed before the repair and now pass; ordinary decimals and both ellipsis forms remain accepted. Independent root review accepted the two-file change. All 30 focused synopsis tests pass; final pre-push gate passed all 46 steps and 795 reachable tests in 312.63 seconds. All branches are pushed with correct native stack bases.
resolution: null
duplicate_of: null
---
A final Astra Max review of PR148 found the new shown_lower regex in packing/devtools/check_synopsis.py lacks a numeric token end boundary. It accepts false lower cells such as 381/100 = 3.81e99 and 381/100 = 3.81/100 by reading only the 3.81 prefix. Restore boundary validation with negative regression controls and preserve valid decimal and ellipsis forms; propagate the fix through the reviewed stack.
