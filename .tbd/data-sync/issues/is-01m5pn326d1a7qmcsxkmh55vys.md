---
type: is
id: is-01m5pn326d1a7qmcsxkmh55vys
title: "Slow test near the 45 s backstop: tests/test_beyond_horizon_replay.py::test_the_receipts_records_and_coverage_rows_hold runs 42-45 s hosted (44.19 s on main e5c1c64e3; 45.07 s failed suite-c on #736 at 5c71b2f94); speed it up or mark it slow under the registry"
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T09:50:22.413Z
updated_at: 2026-10-24T11:06:47.563Z
---

## Notes

2026-10-24 coord-intake-1024: PR #789 (think-ptkk, cd46d04ef) splits the receipts check into one test per release, the largest 8.9 s, after it reached 53.6 s on that branch. This bead closes once #789 merges and main's hosted runs show the split tests under the guard.
