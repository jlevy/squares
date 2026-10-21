---
type: is
id: is-01m5g5gnq2essjemgdmkm4rxzh
title: Update T-196 resource description after upstream adoption
kind: bug
status: closed
priority: 2
version: 3
delegate: profiles-pr-coordinator
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T21:22:44.577Z
updated_at: 2026-10-21T21:38:41.968Z
started_at: 2026-10-21T21:22:54.231Z
closed_at: 2026-10-21T21:38:41.967Z
close_reason: Shared T-196 resource description now reflects independently replayed certificates and adoption at 227/260. Commit e3e33171b; final selected push gate 25/25 passed, full rebuild 7298 checks passed, and live homepage/profile copy verified.
resolution: null
duplicate_of: null
---
The shared resource card still describes T-196 as pending adoption after origin/main adopted verified results at 227 and 260. Correct only the description against current evidence; preserve the distinction from stronger reported n260 bounds.
