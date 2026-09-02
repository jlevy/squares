---
type: is
id: is-01m1hdcwgf5fygt5wsdtx3e47q
title: Make synopsis handoff validation follow terminal session chronology and standalone beads
kind: bug
status: closed
priority: 1
version: 2
spec_path: packing/campaign/agendas/agenda-015-ten-hour-earned-routes-and-guard-repairs.md
labels: []
dependencies: []
parent_id: is-01m1g7btz9tbnfvpxdtkc0rqd1
created_at: 2026-09-02T15:56:56.207Z
updated_at: 2026-09-02T16:34:33.812Z
closed_at: 2026-09-02T16:34:33.811Z
close_reason: Terminal-clock selection, live-session exclusion and standalone-bead handoff regressions pass the exact-tree full gate.
resolution: null
duplicate_of: null
---
The records gate selects the session with the latest start time rather than the latest terminal deadline, so session-082 masks the later session-078 closeout. It also requires every terminal handoff to name an agenda cell, but agenda-015 legitimately hands off to standalone continuation bead think-5j8d after PR publication. Select the authoritative terminal session by terminal clock and validate either exactly one agenda-cell handoff or exactly one standalone bead, with regression tests and no weakening of link/evidence checks.
