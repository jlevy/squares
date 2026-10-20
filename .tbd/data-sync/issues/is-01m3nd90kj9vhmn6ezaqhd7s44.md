---
type: is
id: is-01m3nd90kj9vhmn6ezaqhd7s44
title: "audit_wand125_rectangles: merge replay receipts from several batch output directories into one packet receipt"
kind: task
status: closed
priority: 1
version: 2
labels:
  - packing
  - wand125-update
  - tooling
dependencies: []
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-29T01:43:10.706Z
updated_at: 2026-10-12T23:38:29.576Z
closed_at: 2026-10-12T23:38:29.576Z
close_reason: "Completed: audit_wand125_rectangles --merge DIR... folds batch replay receipts into one packet receipt; landed with the 21 stranded receipts merged in f5003d1da (2026-10-02)."
resolution: null
duplicate_of: null
---
Session 161 runs the 45 pending rectangle replays in ten cloud batches (branches claude/replay-wand125-rect-b01..b10, transfer/wand125-rect-bNN/ with audit.json and rect_n*/ per packet). --resume keeps only PASS cases already in the output's audit.json and removes a case directory it does not know, so copying directories and resuming would replay them again. Add a --merge DIR... mode (OR-1) that validates each batch receipt (same source_revision and packet, PASS with a replay block, files present and hashed) and folds the cases into resources/web/wand125-rectangle-certificates-2026-09-2{7,8}/receipts/replay/audit.json deterministically, refusing duplicates that disagree; test it; then run it on the batches as they land and promote with apply_wand125_rectangles.
