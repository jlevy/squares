---
type: is
id: is-01m57xskzp84r50zqxn5cp8b7b
title: "W2 #669: replay original and regularized n155 certificates with source controls"
kind: task
status: in_progress
priority: 2
version: 6
delegate: lane-new
labels:
  - result-import
dependencies: []
parent_id: is-01m5733t1298tmxrt5h2pw772s
hold: null
hold_until: null
created_at: 2026-10-18T16:33:53.653Z
updated_at: 2026-10-19T22:23:56.837Z
started_at: 2026-10-18T16:34:04.361Z
---
Owned follow-up source replay lane: Codex de_winter_668_replay, after #668 lane think-8xr0. Retained evand-n155-explorer-2026-10-17 at59326b86291b76c39d843f3f156e8f25fa0f6e3f contains s155_ex2.cert and s155_ex2_regularized.cert (155 squares each; 52400 total certificate bytes). Run each complete certificate with both retained standalone verify_cert.py and verify_cert2.py, after reading them; exactly 4 positive source invocations and at least 8 mutant invocations (duplicate square and wall violation for each certificate/checker). All three Daniel packets share identical checker digests. Source imports only sys and Fraction. No source timing receipt accompanies these claims. Conservative static price: expected60-180 wall seconds serial (0.0167-0.05CPUh); total one-worker wall ceiling600seconds (0.166667CPUh), counting each mutant as a full pass because verify_cert.py computes all pair margins before rejecting. At most143220 pair-loop iterations across12 invocations; pair geometry uses rational predicates and circumscribed-disc pruning. This is an estimate, not a run or verified status. Use projectPython3.14.7 without optimization, standard library, no network, retained source in external scratch, explicit TMPDIR/CARGO_TARGET_DIR/UV_CACHE_DIR. Root holds producer execution and checkout until #665 slot is released. Retain source digests, commands, stdout/stderr/timings and refusal receipts; durable controls test. Separate replay-specific files/branch after #668; no #676 edits, provisional T IDs, author messages, rung changes, adoption or strong-regularization claim. blocked_on: jlevy/squares#665

## Notes

2026-10-19 20:54Z lane-new: taken over from the 19 October handoff (#684) with its import beads. The earlier replay and review outputs were left on the Mac and are not in Git; this lane re-runs the replays here (devtools.upper_bound_reports certify / check --replay) and has the stage 4 review written by a separate reviewer session.

2026-10-19 21:40Z lane-new: import declaration and certify receipt for the packet(s), check --replay passed on both maintained routes (d7413ccdb, claude/intake-2026-10-19-evand-singles). Stage 4 review requested (covers T-197, T-198, T-199, T-218, T-219). Adoption at the count written locally after the review; strong runs under think-ip1p.

2026-10-19 22:23Z lane-new: V3/C3 after the 19 October review (0466eb5aa); house adopted at the count (be6aa80aa, claude/intake-2026-10-19-evand-singles); regularization runs under think-ip1p finishing.
