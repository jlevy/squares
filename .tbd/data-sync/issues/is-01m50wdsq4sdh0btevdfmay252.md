---
type: is
id: is-01m50wdsq4sdh0btevdfmay252
title: "Root cause: how n = 176 (and any others) became unregularized - which import/adoption path replaced a regularized drawing without re-regularizing"
kind: task
status: closed
priority: 1
version: 4
delegate: ecstatic-edison-reg-audit
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdrbfnwsq05w150az5z88
hold: null
hold_until: null
created_at: 2026-10-15T22:55:16.707Z
updated_at: 2026-10-15T23:18:05.541Z
started_at: 2026-10-15T22:55:54.624Z
closed_at: 2026-10-15T23:18:05.541Z
close_reason: "Done: audit/root cause/map recorded in notes and scratchpad regularization-audit.md (2026-10-15)"
resolution: null
duplicate_of: null
---

## Notes

ROOT CAUSE (ecstatic-edison-reg-audit, 2026-10-15, origin/main 22a67ce4a).

1. House adoption refreshes the atlas with the axis tool only. adopt_houses: "the atlas is refreshed after it runs". regularize_axis_components --update-atlas (update_atlas, around lines 2030-2042) keeps another generator's view only while kept["source"] == record["source"]. Otherwise it prints "n=N: the <gen> view lapsed: its witness changed" to stdout and writes the axis tool's record of the new witness in its place. The lapse is recorded nowhere: not in the index, a bead or a receipt.
   - PR #553 (3e24adeb2, 12 Oct) re-housed 272 and 304, among others. The layer merge 7d4d9b437 fell back to the axis tool, and #580 redrew 270 and 305 but never 272 or 304.
   - PR #598 (merged 14 Oct 11:45Z): 8a4d26fea (T-154/T-158 at 175, 232, 264) and 34e62125f (T-156/T-160 at 154). Its description says "regularized views (axis tool at the four new houses)". The layer merge 5d294db7c dropped 175's grid-slack view (grid-slack-on518).
   - PR #614 (merged 15 Oct 09:58Z): 3b9fab84a (153 154 207 211 237 241 302 304) and 60aa1d39e (105 129 146 156 176 204 261 271 272 303). At 176 this replaced the grid-slack-deg5-1013-c view with an axis view that loses to the house on uneven_axis (73 vs 71), so the raw T-165 house is drawn.
2. The remedy exists only as a manual step. regularization-process.md "When a Witness Changes" says to run both generators on the new witness, then select and admit. result-import.md has no such step (Stage 5 step 4 only checks the drawing against its source), and policy section 8 keeps generator runs on request, never as a gate. After #518 both generators were re-run (771933f54); after #553, #598 and #614 they were not, except for #580's repairs.
3. No gate catches it. Run here on main: regularize_axis_components --check-atlas, "regularized atlas check passed in 2.74s". The axis tool rewrote source.sha256, so the stale check ("the witness changed since its view was derived") cannot fire. default_drawings --check passes ("82 of 92 ... 10 keep the house"), with "n=176 keeps the house picture: worse on uneven_axis" printed as information only. results rungs / regularized_drawings checks only hold the notes to the index. Nothing compares the drawn picture with the previous one or requires a strong-generator decision on the current witness digest.
4. The record reads as regularized. The index says status: regularized at 176. The case note starts "Regularized by the Squares Project with its own axis tool" and calls the house "its source's regularization of T-161's packing" (the register sense, an exact re-solve). Only the rendered page says the house is drawn.
