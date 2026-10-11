---
type: is
id: is-01m3z64p1mx8yrv14xk2e77xz2
title: "n17 capture route: reconcile pilot2 falsifier and select controlled successor"
kind: task
status: in_progress
priority: 1
version: 10
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
child_order_hints:
  - is-01m45ncp7p0yab6vmn2x4358d2
  - is-01m4agrv4m0a14g3qcqvnvktsw
hold: null
hold_until: null
created_at: 2026-10-02T20:50:53.101Z
updated_at: 2026-10-07T06:28:18.196Z
started_at: 2026-10-03T22:35:10.737Z
---
Session 168. Pilot 1 (cea300a4) met the capture falsifier (position g=1.000), but review-2026-10-02-n17-capture-after-pilot.md (3f90fc2d) finds it producer-limited by the 24 live-row cap. Pilot 2: max-live 128/256, all live rows bisected to 2^-22, end-angle core, hull cap 48, per-side bounds, widest-row/extent ratio, n11 case-438 contraction control. Falsifier: 3 rounds with widest row < 1/20 of extent and no two-sided extent falling 10%. In-flight uncommitted edits to packing/devtools/pilot_n17_capture.py and its test; runs and receipts in the session scratchpad lanes/c1/p2. Next: integrate receipts into X048-session-168-pilots, record per-round g, decide the capture route.

## Notes

2026-10-03 05:00 UTC. 128 rows (box1024, tool 85e8d2ab): 13 rounds, 208 certified updates, endpoint control held; worst two-sided position extent stays 2*rho (g = 1.000) every round; only one-sided wall movement, frozen since round 10. Widest-row-to-extent ratio max stuck at 0.200 (side-N2, tilted, angle range ~0.03 rad), so the review's 1/20 falsifier is undecidable at this cap; ~512 rows needed. Cost at the cap ~155 CPU-s per update, ~42 min per round. 256-row run started 04:54 from round 0 (checkpoint refused across the 841e368dd kernel digest change), 3-hour ceiling. Capture is angular-resolution and exact-arithmetic bound, so F2's gmpy2 port and X1's Rust checker apply directly.

2026-10-03 evening. The 256-row run (rounds 1-13) is UNDECIDED (77624e8f5). The new scorer devtools/score_n17_capture.py reads it: by round 10, 15 of 16 owners were under a tenth; side-N2 held at 0.1002. No two-sided position extent moved off the box in 13 rounds. Side-N2 needs about 528 rows to reach the falsifier's twentieth, side-W2 377 and side-N0 299. Its process was killed in round 14 with the helper task that launched it; runs are now detached with setsid. Per-owner caps are committed (b43f4ca74, --max-live-for CELL=N). Two runs resumed from the round-13 checkpoint: a uniform 576-row run (restarted 20:50 after the OOM killer took it during a whole-suite gate) and a run with rows by need (256; side-N2 576, side-W2 416, side-N0 320; started 21:39). At step 217 the by-need run was 2.3 times faster (2,094 s against 4,914 s). Score each with devtools.score_n17_capture as rounds land.

2026-10-04 02:28 UTC: the after-pilot review's falsifier is MET (1525d4e03). The run with rows by need (256; side-N2 576, side-W2 416, side-N0 320; resumed from round 13) had every owner under a tenth at round 14 and under a twentieth at round 15. Rounds 15-17 were fine and flat (largest ratio 0.0499; least g 0.988). The pilot stopped with outcome "falsified", and devtools.score_n17_capture agrees. No two-sided position extent moved off the 1/1024 box in 17 rounds. Lane R9 (independent review) is testing other producer limits (hull cap 48, core, partner pruning; a --hull-limit 0 resume from the round-16 checkpoint) and whether the box is already inside U′'s first-order feasible set, before the architecture verdict is adopted. The uniform 576-row run continues as a cross-check.

2026-10-05 (PR 347 status survey). Receipt capture-pilot2-box1024-need/receipt.json records outcome: falsified. Lane R9's review has no record on any ref. Open a dedicated R9 bead, or name its deliverable file here.
