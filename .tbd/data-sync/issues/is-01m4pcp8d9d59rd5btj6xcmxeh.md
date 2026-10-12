---
type: is
id: is-01m4pcp8d9d59rd5btj6xcmxeh
title: Adopt the register's lower exact certificates as atlas witnesses before the full regularization run (T-146 at 15 counts; imports in flight)
kind: task
status: open
priority: 2
version: 3
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m4mdbq6bhkv71fxeeckawsbt
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
created_at: 2026-10-11T21:07:52.361Z
updated_at: 2026-10-12T01:03:10.806Z
---
The pilots of 2026-10-11 show the exact solve rediscovering T-146's registered certificates at 70, 102, 129, 146 (1e-10 below the case records' verified bounds), so the same-side re-solve refuses unmatched-rotation there and the views become row-3 candidates. Adopting those certificates as the atlas witnesses (blocked on the case-record rewrite #403 and RG-7 custody, per T-146) lets the run regularize the credited packing at its own side. Also sequence the full run after the in-flight imports at the same counts (#470 think-jpre, #476 think-m8ck incl. 267, #481 think-ac4h, #483 think-8m3u, #488 think-6uv7, #489 think-xm4h), since a changed witness lapses any review (policy section 5).

## Notes

2026-10-12, owner answer q5 "as recommended": adopt T-146's certificates as atlas witnesses, sequenced after the case-record rewrite #403, RG-7 custody, and the in-flight imports at the same counts. Until then the full run decides 70, 102, 129, 146 as row 3 (held, register first) and they are re-run after adoption.
