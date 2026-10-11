---
type: is
id: is-01m3xvdvhf7hsd6x6svf0x81zj
title: "Import wand125: rectangle certificate s(93) >= 973/100 at 06eeb40 (no request; found in triage of #294)"
kind: task
status: in_progress
priority: 3
version: 4
delegate: claude-code@vm
labels:
  - result-import
  - packing
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
hold: null
hold_until: null
created_at: 2026-10-02T08:24:24.879Z
updated_at: 2026-10-06T09:18:20.301Z
started_at: 2026-10-06T07:53:23.869Z
---
Unrequested claim (runbook stage 1, step 2): wand125/square-packing-bounds 06eeb40 adds rect_n93_L973, s(93) >= 973/100, raising the reported 9.7225 (T-068's rect_n93_L9725), checked by Tokoharu's verify.cpp a75140df (the 09-28 rectangle packet's checker). Same commit adds rect_n59_L79375 and rect_n77_L894, both below values the record already holds (no entry). Import: a packet at 06eeb40, a new entry (a later release raising a count), replay ~upstream per-angle CPU.

## Notes

2026-10-06 (lane R5, think-wyf4): nothing to import. rect_n93_L973 (06eeb40) was superseded the same afternoon by rect_n93_L9735 (4318bdf, 1947/200 = 9.735), which the 2 October rectangle packet at b00fc70 retains and E-wand125-rectangle-2026-10-02-report reports; the sqverify-fast census verified it at all 201 directions (3 October). It is below the record at n = 93 in both lanes: verified 781/80 = 9.7625 (T-091, from n91) and T-075's 39/4 = 9.75. Stage 1 table: below the standing bound and asking for no work, so no entry; it stays in the packet. No record names this bead. Ready to close.
