---
type: is
id: is-01m41cyj83ab8xn2pb5wkbdv5w
title: Record the complete n101 linear replay (966fb9752, FULL_REPLAY_MATCHES_SHIPPED, controls refused) and register n101–105 as a replayed entry
kind: task
status: closed
priority: 1
version: 3
labels:
  - records
dependencies:
  - type: blocks
    target: is-01m41crc9rnphq77swdexdmgtx
parent_id: is-01m41cr1mz526vz5b2a5e4z100
created_at: 2026-10-03T17:28:21.507Z
updated_at: 2026-10-03T19:04:04.882Z
closed_at: 2026-10-03T19:04:04.882Z
close_reason: null
resolution: null
duplicate_of: null
---
Found by the records lane 2026-10-03: receipts/n101/merged.json (all 201 directions, 7.69 CPU-h) and control.json (CONTROLS_REFUSED) were committed on 2 Oct (think-m7cm) but no evidence entry cites them; T-073 prose still says only index 150 replayed; n101-105 hold old verified bounds. Fix: E-n101-wand125-linear-1028-source-replay; new replayed entry V3/C3 for n101-105 (precedent T-045/T-070/T-074); T-073 next_rung narrows to n83; counts move. Own commit right after the restack push, before the stack merges.
