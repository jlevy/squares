---
type: is
id: is-01m5h5w3jq53jn76r07a24jpyx
title: "#719's 8 rows above 1024 (1061-1568): record once the owner answers D1"
kind: task
status: in_progress
priority: 3
version: 4
delegate: coord-intake-1021b
labels:
  - result-import
dependencies: []
parent_id: is-01m5h3rxsgydmfjazs3vmw05wp
hold: null
hold_until: null
created_at: 2026-10-22T06:48:13.655Z
updated_at: 2026-10-31T11:18:11.100Z
started_at: 2026-10-22T06:48:16.087Z
---
Each is below #666 and Couzo's 5a299b4 (#715) at all eight counts (triage-719/claim-map.md); ~4.4 CPU-min replay.
blocked_on: think-f2io

## Notes

2026-10-22 c-lane-719-import: the 8 rows above 1024 (1061, 1128, 1196, 1266, 1339, 1413, 1489, 1568) are pinned by SHA-256 in resources/web/mishapolk-issue719-2026-10-22 (certificates/n-N.cert at 12fc466, first committed at 1851c2c, receipts/first-commits.json) and not derived, replayed or recorded; the requests record queues each on this bead, blocked on think-f2io. The ledger upper-bounds-issue719-20261022 walks them: #666 (17 October) recorded below the grid, then #715 (21 October; at 1061, 1266, 1339, 1413, 1489 and 1568, exact sides from the 5a299b4 certificates its table links) and Couzo's 5a299b4 publication (ties with #666 at 1128 and 1196), then #719 recorded at all eight. On D1 = A: derive the eight facts (upper_bound_reports derive --checkout at 12fc466; about 0.8 MB of facts), raise beyond_horizon_replay's LIMIT or add the counts, run filtered on them (about 4.4 CPU-min), and record them with #666's and #715's in report order.

2026-10-31 bold-ritchie-l6 (stalled-bead triage of the 31 October intake pass, think-ztcy): Waits on the owner: these eight rows are recorded by think-llit's walk (bold-ritchie-l4, live on 31 October) once D4 (hosting) and D5 (per-row credit beyond the horizon, think-f2io) are decided and zenodo.org is reachable for the #836 and #847 deposits; then about 4.4 CPU-minutes of replay.
