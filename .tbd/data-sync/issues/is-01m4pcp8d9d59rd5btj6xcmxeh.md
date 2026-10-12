---
type: is
id: is-01m4pcp8d9d59rd5btj6xcmxeh
title: Adopt the register's lower exact certificates as atlas witnesses before the full regularization run (T-146 at 15 counts; imports in flight)
kind: task
status: in_progress
priority: 2
version: 10
delegate: claude-code@vm
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m4mdbq6bhkv71fxeeckawsbt
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
hold: null
hold_until: null
created_at: 2026-10-11T21:07:52.361Z
updated_at: 2026-10-12T18:36:24.959Z
started_at: 2026-10-12T18:36:24.204Z
---
The pilots of 2026-10-11 show the exact solve rediscovering T-146's registered certificates at 70, 102, 129, 146 (1e-10 below the case records' verified bounds), so the same-side re-solve refuses unmatched-rotation there and the views become row-3 candidates. Adopting those certificates as the atlas witnesses (blocked on the case-record rewrite #403 and RG-7 custody, per T-146) lets the run regularize the credited packing at its own side. Also sequence the full run after the in-flight imports at the same counts (#470 think-jpre, #476 think-m8ck incl. 267, #481 think-ac4h, #483 think-8m3u, #488 think-6uv7, #489 think-xm4h), since a changed witness lapses any review (policy section 5).

## Notes

2026-10-12, owner answer q5 "as recommended": adopt T-146's certificates as atlas witnesses, sequenced after the case-record rewrite #403, RG-7 custody, and the in-flight imports at the same counts. Until then the full run decides 70, 102, 129, 146 as row 3 (held, register first) and they are re-run after adoption.

2026-10-12 (session_017JNnKDwL74rnktr9s8BdjP), overlap found: PR #518 (intake 2026-10-11 layer 3/5, stack #517, session_01UXZs37jGv5vqVGADH7Gkn8) adopts 42 reviewed V3/C3 houses on the case records now, citing an owner decision of 2026-10-11 not to wait for #403, with private-worker custody closed (RG-7 among them). It replaces 42 known-best witnesses and their axis-tool regularized views, incl. T-146 at 70, 102, 103, 123, 129, 236, 258, 263, 269, 292, 295, 302, 303 and T-150 at 146, 261. This bead's work is done there if #518 merges; the 2026-10-12 note above ("after #403") is superseded pending the owner's confirmation. Consequence for think-ux1v: the full run's results at those 42 counts were measured against the old witnesses and must be re-run once #518 lands.

2026-10-12, regularization on #518's houses (scratch tree, driver at dab4de76f, report $SP/adopt518-report.md in session_017JNnKDwL74rnktr9s8BdjP's scratchpad): of the 42 re-housed counts, 19 admit, 7 no change (T-146 houses are already Daniel's regularized views), 9 refuse (a total falls), 2 held (146, 261), 2 review (131, 232), 3 solve timeouts at the 600 s default (211, 263, 267). Concern for the owner before #518 merges: several new houses draw worse than the witnesses they replace (light squares old -> new: 308 0 -> 127, the grid replaced by T-141; 126 26 -> 75; 232 0 -> 134; 237 60 -> 144; 259 118 -> 183); the regularizer recovers much where it admits (126 75 -> 7, 259 183 -> 49) but refuses 308, 154, 292 and others. Re-run with the current driver (tolerance, solve retries, digit-limit fix) and 1800 s limits under way: $SP/runs/adopt518-v2.

2026-10-12 ~10:40 UTC: the 42 counts re-run on #518's houses with the current driver (wider rotation tolerance, solve retry ladder, digit-limit fix; 1800 s limits): $SP/runs/adopt518-v2 (37) + $SP/runs/adopt518-v2b (5), from the scratch tree $SP/wt-518-code (#518 merged with #511). Decisions: 18 admit (all at the witness's own side: 84 86 108 126 127 129 132 153 180 207 209 228 236 237 259 270 302 306), 7 no change (70 102 103 258 269 295 303), 7 refuse (105 123 154 175 292 305 308), 7 held (146 155 156 211 232 261 307), 2 no view (263 267), 1 review (131). Follow-up once #518 is on main and the regularization stack (#548's v2 contract) is too: merge main into the stack, `reclassify --refresh-bounds` on copies of these runs in the merged tree, `regularize_evand layer --select admitted` for the 42, regenerate `regularized_drawings`, render, re-pin DATA_REVISION, and register the held 7 the way T-151 did (devtools/register_regularized_bounds.py). The refusals include 308, whose new house (T-141) draws 127 light squares where today's grid draws none; the grid-slack generator is the next thing to try there.

2026-10-12 (morning): the follow-up recipe above stands; #549 now carries reclassify --refresh-bounds and the /1 grid contract, so the 17 grid choices among #518's counts join that admission.

2026-10-12 12:25 UTC: precomputed on #518's witnesses (#518 at 1bc770d34; re-run any count whose witness or case record changes before it merges). Evan Daniel runs reclassified with --refresh-bounds: no bound or decision moved (18 admitted). Grid pass on 35 counts (7 skipped by the all-count rule), 35 exact views, 39.6 min wall. Choice (same rule as the all-count lane): grid at 105 131 146 156 175 211 232 267 292 305 307 308; Evan Daniel at 84 86 108 126 127 129 132 153 180 207 209 228 236 237 259 270 302 306; keep #518's drawing at 70 102 103 123 154 155 258 261 263 269 295 303. Census over the 42: light 230 -> 133, uneven 588 -> 361, near-axis 182 -> 6, house sides 21,701 -> 23,038 (as admitted, without 232). 302 under the new witness already draws 0/0/0 (Evan Daniel's view 980 house sides is chosen); 303 keeps 4 light squares no generator closes. 232's grid view is row 7 (review). Admission once main (with #518) is merged up the stack, from packing/: regularize_axis_components --update-atlas --n <the 42> --workers 2; then PYTHONINTMAXSTRDIGITS=0 python -m devtools.regularize_evand layer --run-dir $SP/runs/refreshed-adopt518-v2 $SP/runs/refreshed-adopt518-v2b --repo-root .. --grid-run $SP/grid/runs/on518 --grid-counts 105 131 146 156 175 211 267 292 305 307 308 (dry run on a layer copy: 29 views written, check_atlas 0 problems). Report: grid-518-report.md in the session scratchpad.

2026-10-12 18:00 UTC: #518 merged (e10fd85d4) and main was merged up the stack. The follow-up is jlevy/squares#559 (layer 7, stacked on #549): 29 of the 42 counts drawn (18 Evan Daniel, 11 grid /1), 12 keep #518's drawing, 232 left for review. No witness changed between 1bc770d34 and the merge, so nothing was re-run. Census over the 42: light 230 -> 133, near-axis 182 -> 6. The layer draws 89 views; atlas house-light 5,382. adopt518-v2's reconstructed cost is labelled in the index (run_block now carries a receipt's measured_by). Closes when #559 merges.
