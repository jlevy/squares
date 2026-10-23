---
type: is
id: is-01m57xskzp84r50zqxn5cp8b7b
title: "W2 #669: replay original and regularized n155 certificates with source controls"
kind: task
status: open
priority: 2
version: 14
delegate: c-close-1023
labels:
  - result-import
dependencies: []
parent_id: is-01m5kcx4ampkzwwy5h447fcb2e
hold: null
hold_until: null
created_at: 2026-10-18T16:33:53.653Z
updated_at: 2026-10-23T07:45:54.340Z
started_at: 2026-10-18T16:34:04.361Z
closed_at: 2026-10-23T07:11:32.156Z
close_reason: "Source checkers re-run on the four certificates of #669 and #674 (8 accepted, 24 controls refused); receipts committed in the three packets and the request notes edited on PR #747 (77872bd02, c4f86cbca, e4ea7beb4); no rung change."
resolution: null
duplicate_of: null
---
Owned follow-up source replay lane: Codex de_winter_668_replay, after #668 lane think-8xr0. Retained evand-n155-explorer-2026-10-17 at59326b86291b76c39d843f3f156e8f25fa0f6e3f contains s155_ex2.cert and s155_ex2_regularized.cert (155 squares each; 52400 total certificate bytes). Run each complete certificate with both retained standalone verify_cert.py and verify_cert2.py, after reading them; exactly 4 positive source invocations and at least 8 mutant invocations (duplicate square and wall violation for each certificate/checker). All three Daniel packets share identical checker digests. Source imports only sys and Fraction. No source timing receipt accompanies these claims. Conservative static price: expected60-180 wall seconds serial (0.0167-0.05CPUh); total one-worker wall ceiling600seconds (0.166667CPUh), counting each mutant as a full pass because verify_cert.py computes all pair margins before rejecting. At most143220 pair-loop iterations across12 invocations; pair geometry uses rational predicates and circumscribed-disc pruning. This is an estimate, not a run or verified status. Use projectPython3.14.7 without optimization, standard library, no network, retained source in external scratch, explicit TMPDIR/CARGO_TARGET_DIR/UV_CACHE_DIR. Root holds producer execution and checkout until #665 slot is released. Retain source digests, commands, stdout/stderr/timings and refusal receipts; durable controls test. Separate replay-specific files/branch after #668; no #676 edits, provisional T IDs, author messages, rung changes, adoption or strong-regularization claim. blocked_on: jlevy/squares#665

## Notes

2026-10-19 20:54Z lane-new: taken over from the 19 October handoff (#684) with its import beads. The earlier replay and review outputs were left on the Mac and are not in Git; this lane re-runs the replays here (devtools.upper_bound_reports certify / check --replay) and has the stage 4 review written by a separate reviewer session.

2026-10-19 21:40Z lane-new: import declaration and certify receipt for the packet(s), check --replay passed on both maintained routes (d7413ccdb, claude/intake-2026-10-19-evand-singles). Stage 4 review requested (covers T-197, T-198, T-199, T-218, T-219). Adoption at the count written locally after the review; strong runs under think-ip1p.

2026-10-19 22:23Z lane-new: V3/C3 after the 19 October review (0466eb5aa); house adopted at the count (be6aa80aa, claude/intake-2026-10-19-evand-singles); regularization runs under think-ip1p finishing.

2026-10-21 coord-intake-1021b: ownership transferred to the 21 October intake coordinator (no update since the previous owner's last note; the 19 October machine-transfer handoff #684 and the owner's instruction of 21 October to resume the intake). Triage of the 21 October sweep follows.

2026-10-21 c-triage-sweep-1021b (read-only triage of the 21 October sweep): #665 merged on 19 October; the description's "until #665 slot is released" is what the sweep read as a wait. T-197 is V3/C3 on main and the house at 155; the parent import (#669) closed on 21 October. The remaining work is think-0lu6's, shared: integrate the 18 October source-checker replay (receipt cab73c96…, not in Git) or re-run it (about 1 CPU-minute), then close both beads in one records PR, editing #669's request notes, which name this bead.
blocked_on: none

2026-10-23 c-close-1023: the 18 October receipt (cab73c96...) was never committed; re-run instead. devtools.evand_source_checkers run (2026-10-23T06:33Z, CPython 3.14.7, 2 workers): the packets' own verify_cert.py and verify_cert2.py, unchanged, python -I, on s155_ex2.cert, s155_ex2_regularized.cert, s229.cert and s229_v2.cert and three controls each (duplicate square, square outside, sharp wall at 1e-30): 8 accepted, 24 refused with INVALID, 32 invocations, 6.5 CPU-s. Receipts receipts/source-checker-replay.json in the three packets (77872bd02, check reworked for OR-16 in e4ea7beb4); #669 and #674 request notes edited (c4f86cbca); no rung change. https://github.com/jlevy/squares/pull/747. Closed: the record names this bead as owning nothing.
blocked_on: none
