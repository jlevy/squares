---
type: is
id: is-01m4pcp8d9d59rd5btj6xcmxeh
title: Adopt the register's lower exact certificates as atlas witnesses before the full regularization run (T-146 at 15 counts; imports in flight)
kind: task
status: open
priority: 2
version: 4
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m4mdbq6bhkv71fxeeckawsbt
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
created_at: 2026-10-11T21:07:52.361Z
updated_at: 2026-10-12T02:45:18.908Z
---
The pilots of 2026-10-11 show the exact solve rediscovering T-146's registered certificates at 70, 102, 129, 146 (1e-10 below the case records' verified bounds), so the same-side re-solve refuses unmatched-rotation there and the views become row-3 candidates. Adopting those certificates as the atlas witnesses (blocked on the case-record rewrite #403 and RG-7 custody, per T-146) lets the run regularize the credited packing at its own side. Also sequence the full run after the in-flight imports at the same counts (#470 think-jpre, #476 think-m8ck incl. 267, #481 think-ac4h, #483 think-8m3u, #488 think-6uv7, #489 think-xm4h), since a changed witness lapses any review (policy section 5).

## Notes

2026-10-12, owner answer q5 "as recommended": adopt T-146's certificates as atlas witnesses, sequenced after the case-record rewrite #403, RG-7 custody, and the in-flight imports at the same counts. Until then the full run decides 70, 102, 129, 146 as row 3 (held, register first) and they are re-run after adoption.

2026-10-12 (session_017JNnKDwL74rnktr9s8BdjP), overlap found: PR #518 (intake 2026-10-11 layer 3/5, stack #517, session_01UXZs37jGv5vqVGADH7Gkn8) adopts 42 reviewed V3/C3 houses on the case records now, citing an owner decision of 2026-10-11 not to wait for #403, with private-worker custody closed (RG-7 among them). It replaces 42 known-best witnesses and their axis-tool regularized views, incl. T-146 at 70, 102, 103, 123, 129, 236, 258, 263, 269, 292, 295, 302, 303 and T-150 at 146, 261. This bead's work is done there if #518 merges; the 2026-10-12 note above ("after #403") is superseded pending the owner's confirmation. Consequence for think-ux1v: the full run's results at those 42 counts were measured against the old witnesses and must be re-run once #518 lands.
