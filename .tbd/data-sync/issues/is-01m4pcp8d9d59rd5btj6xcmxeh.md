---
type: is
id: is-01m4pcp8d9d59rd5btj6xcmxeh
title: Adopt the register's lower exact certificates as atlas witnesses before the full regularization run (T-146 at 15 counts; imports in flight)
kind: task
status: open
priority: 2
version: 6
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m4mdbq6bhkv71fxeeckawsbt
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
created_at: 2026-10-11T21:07:52.361Z
updated_at: 2026-10-12T10:34:08.068Z
---
The pilots of 2026-10-11 show the exact solve rediscovering T-146's registered certificates at 70, 102, 129, 146 (1e-10 below the case records' verified bounds), so the same-side re-solve refuses unmatched-rotation there and the views become row-3 candidates. Adopting those certificates as the atlas witnesses (blocked on the case-record rewrite #403 and RG-7 custody, per T-146) lets the run regularize the credited packing at its own side. Also sequence the full run after the in-flight imports at the same counts (#470 think-jpre, #476 think-m8ck incl. 267, #481 think-ac4h, #483 think-8m3u, #488 think-6uv7, #489 think-xm4h), since a changed witness lapses any review (policy section 5).

## Notes

2026-10-12, owner answer q5 "as recommended": adopt T-146's certificates as atlas witnesses, sequenced after the case-record rewrite #403, RG-7 custody, and the in-flight imports at the same counts. Until then the full run decides 70, 102, 129, 146 as row 3 (held, register first) and they are re-run after adoption.

2026-10-12 (session_017JNnKDwL74rnktr9s8BdjP), overlap found: PR #518 (intake 2026-10-11 layer 3/5, stack #517, session_01UXZs37jGv5vqVGADH7Gkn8) adopts 42 reviewed V3/C3 houses on the case records now, citing an owner decision of 2026-10-11 not to wait for #403, with private-worker custody closed (RG-7 among them). It replaces 42 known-best witnesses and their axis-tool regularized views, incl. T-146 at 70, 102, 103, 123, 129, 236, 258, 263, 269, 292, 295, 302, 303 and T-150 at 146, 261. This bead's work is done there if #518 merges; the 2026-10-12 note above ("after #403") is superseded pending the owner's confirmation. Consequence for think-ux1v: the full run's results at those 42 counts were measured against the old witnesses and must be re-run once #518 lands.

2026-10-12, regularization on #518's houses (scratch tree, driver at dab4de76f, report $SP/adopt518-report.md in session_017JNnKDwL74rnktr9s8BdjP's scratchpad): of the 42 re-housed counts, 19 admit, 7 no change (T-146 houses are already Daniel's regularized views), 9 refuse (a total falls), 2 held (146, 261), 2 review (131, 232), 3 solve timeouts at the 600 s default (211, 263, 267). Concern for the owner before #518 merges: several new houses draw worse than the witnesses they replace (light squares old -> new: 308 0 -> 127, the grid replaced by T-141; 126 26 -> 75; 232 0 -> 134; 237 60 -> 144; 259 118 -> 183); the regularizer recovers much where it admits (126 75 -> 7, 259 183 -> 49) but refuses 308, 154, 292 and others. Re-run with the current driver (tolerance, solve retries, digit-limit fix) and 1800 s limits under way: $SP/runs/adopt518-v2.

2026-10-12 ~10:40 UTC: the 42 counts re-run on #518's houses with the current driver (wider rotation tolerance, solve retry ladder, digit-limit fix; 1800 s limits): $SP/runs/adopt518-v2 (37) + $SP/runs/adopt518-v2b (5), from the scratch tree $SP/wt-518-code (#518 merged with #511). Decisions: 18 admit (all at the witness's own side: 84 86 108 126 127 129 132 153 180 207 209 228 236 237 259 270 302 306), 7 no change (70 102 103 258 269 295 303), 7 refuse (105 123 154 175 292 305 308), 7 held (146 155 156 211 232 261 307), 2 no view (263 267), 1 review (131). Follow-up once #518 is on main and the regularization stack (#548's v2 contract) is too: merge main into the stack, `reclassify --refresh-bounds` on copies of these runs in the merged tree, `regularize_evand layer --select admitted` for the 42, regenerate `regularized_drawings`, render, re-pin DATA_REVISION, and register the held 7 the way T-151 did (devtools/register_regularized_bounds.py). The refusals include 308, whose new house (T-141) draws 127 light squares where today's grid draws none; the grid-slack generator is the next thing to try there.
