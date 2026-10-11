---
type: is
id: is-01m18qcgw90k296pkg1wcpn6k3
title: "agenda-008 block 1: reconcile the agenda queue and make discharge an edge"
kind: task
status: closed
priority: 0
version: 2
labels: []
dependencies: []
created_at: 2026-08-30T06:58:20.167Z
updated_at: 2026-10-06T08:28:12.073Z
closed_at: 2026-10-06T08:28:12.072Z
close_reason: "Done: agenda-008 (status completed) records BC-081, this block, as complete, and the agenda schema on main carries the discharged_by edge."
resolution: null
duplicate_of: null
---
Four agenda-005 commitments (BC-043, BC-044, BC-045, BC-048) were discharged by agenda-006 (BC-054, BC-060, BC-053, BC-061) and still read 'ready'. Add a discharged_by edge to the agenda schema, mark them, set agenda-006 complete, name or remove the four unnamed blockers, and make render_agenda_map refuse a ready commitment carrying a discharge.
