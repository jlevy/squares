---
type: is
id: is-01m4k11tz4tg1smpwmeknqjs9y
title: "Couzo 02f9690 beyond-horizon certificates: 15 below the tracked rows (n375 by 4.29e-5, n378 by 4.00e-4), 5 above"
kind: task
status: in_progress
priority: 2
version: 4
delegate: coord-intake-1021b
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T13:46:45.604Z
updated_at: 2026-10-22T02:18:24.361Z
started_at: 2026-10-22T02:18:23.092Z
---
Found by the importer lane (think-md2i) in packing/resources/web/couzo-exact-certificates-2026-10-09/acquisition/claims.json: franciscouzo/square-packing 02f969075f79 holds 20 certificates beyond the n <= 324 horizon. 15 are below the tracked dated beyond-horizon rows (332, 336-341, 369, 373-379; 375 at 9953490883645300797660281830293/(5*10^29) by 4.29e-5, 378 at 9973230520053043026984980967643/(5*10^29) by 4.00e-4) and 5 above by about 1.8e-11 (327, 335, 342, 364, 372). think-1545 (another session) owns Couzo's extended-range rows; this bead holds the 02f9690 update for it: dated beyond_horizon_claims rows keyed (n, source_id) with dated supersession, as PR #479 did for 2d32a6e.

## Notes

2026-10-10: the description cites jlevy/squares#479 as the precedent for the row shape, not as a wait; nothing gates this bead.
blocked_on: none

2026-10-22 coord-intake-1021b: #715 (Couzo, 1285 rows; PR #717 imports the 109 new rows <= 1024) re-certifies some of this bead's earlier-commit certificates byte for byte. The #715 acknowledgement (issuecomment-6329883508) told the author those 64 rows will be recorded from their first commits; this bead records its share (#717 review A2). 30 sub-print re-certifications of 4e4c8ce are held on think-fwa9. The filtered two-route replay (couzo_715_replay) re-prices this bead's replay at about 40 CPU-minutes (triage-715 price.md).
blocked_on: jlevy/squares#717
