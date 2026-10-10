---
type: is
id: is-01m4k11tz4tg1smpwmeknqjs9y
title: "Couzo 02f9690 beyond-horizon certificates: 15 below the tracked rows (n375 by 4.29e-5, n378 by 4.00e-4), 5 above"
kind: task
status: open
priority: 2
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T13:46:45.604Z
updated_at: 2026-10-10T16:38:02.348Z
---
Found by the importer lane (think-md2i) in packing/resources/web/couzo-exact-certificates-2026-10-09/acquisition/claims.json: franciscouzo/square-packing 02f969075f79 holds 20 certificates beyond the n <= 324 horizon. 15 are below the tracked dated beyond-horizon rows (332, 336-341, 369, 373-379; 375 at 9953490883645300797660281830293/(5*10^29) by 4.29e-5, 378 at 9973230520053043026984980967643/(5*10^29) by 4.00e-4) and 5 above by about 1.8e-11 (327, 335, 342, 364, 372). think-1545 (another session) owns Couzo's extended-range rows; this bead holds the 02f9690 update for it: dated beyond_horizon_claims rows keyed (n, source_id) with dated supersession, as PR #479 did for 2d32a6e.

## Notes

2026-10-10: the description cites jlevy/squares#479 as the precedent for the row shape, not as a wait; nothing gates this bead.
blocked_on: none
