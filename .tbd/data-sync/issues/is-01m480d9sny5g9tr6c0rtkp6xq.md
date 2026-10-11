---
type: is
id: is-01m480d9sny5g9tr6c0rtkp6xq
title: "T-081: register the k2m4 Lean build of 3 October as a replayed proof-assistant entry (bentz4_of_validTilt9)"
kind: task
status: closed
priority: 2
version: 5
delegate: claude-code@vm
labels:
  - result-import
  - packing
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-06T07:03:53.908Z
updated_at: 2026-10-06T15:55:41.086Z
started_at: 2026-10-06T07:56:06.234Z
closed_at: 2026-10-06T15:55:41.086Z
close_reason: "Done: recorded by lane R5 (T-070, T-046 next_rung) / lane R3 (E-k2m4-evand-bentz4-lean-build) on 6 October, merged in #382"
resolution: null
duplicate_of: null
---
T-081's reduction from ValidTilt9 to every k >= 8 is cited only as the source's report (E-k2m4-evand-lean-report), although lake build Sqpack.ValidSplit9 passed here on 2026-10-03 from retained bytes (packing/resources/web/evand-square-packing-2026-10-03/receipts/lean/build_bentz4.log, exit 0, 8,721 jobs; axioms_bentz4.log prints only propext, Classical.choice and Quot.sound for bentz4_of_validTilt9 and the theorems under it), staged by devtools.stage_evand_bentz4_lean. A replayed-here proof-assistant evidence entry with axioms_receipt, modelled on E-k2m3-evand-bentz-lean-build, is the second half of T-081's next rung: a full replay of ValidTilt9 (think-4uir for qx2_zm.py, think-hwpr for wand125's run) lifts only the finite premise (review-2026-10-06-wand125-validtilt9-independent-check.md, W-13). Found by lane R3 (think-dsz4).

## Notes

2026-10-06 lane R3: registered E-k2m4-evand-bentz4-lean-build (replayed-here, proof-assistant-checked, axioms_receipt axioms_bentz4.log, replay_status passed) from the 3 October build receipts in the evand-square-packing-2026-10-03 packet; cited on T-081, V-evand-lean gains the 2eb15455 version, E-k2m4-evand-lean-report and source coverage carry the update. T-081 stays V0/C1: ValidTilt9 is unreplayed and sets the minimum. Done in cd14f8999 and 6af3a3552 (case records cite it); close at merge.
