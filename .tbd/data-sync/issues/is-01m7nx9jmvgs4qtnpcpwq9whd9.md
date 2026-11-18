---
type: is
id: is-01m7nx9jmvgs4qtnpcpwq9whd9
title: "Import #1015, #1017: Joost de Winter's s(127) <= 11.800795682214 and then <= 11.800793726616 (both 17 Nov, report order), from JoostdeWinter/square-packing (head 838c5ea at 00:00Z 18 Nov)"
kind: task
status: in_progress
priority: 1
version: 13
delegate: w6-dewinter-1118
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-17T23:25:53.691Z
updated_at: 2026-11-18T02:39:22.085Z
started_at: 2026-11-18T01:19:03.008Z
---

## Notes

2026-11-18T01:27Z w6-dewinter-1118: claimed; worktree /home/user/wt/w6-import-1015, branch claude/intake-2026-11-18-import-1015. Triage: #1015 (22:14:33Z, pin 35b576a, cert first committed 689bc79 22:07:57Z) side 11.80079568221357 (ceil12 11.800795682214), 9.582e-4 below T-305; #1017 (22:27:04Z, pin cc20a26 22:26:24Z) exact 5900396863307571/500000000000000, 1.9556e-6 below #1015 (not 1.96e-9); #1020 (22:49:35Z, pin a1ba501 22:48:48Z, folded in by the coordinator) 11.80079372661496 (ceil12 ...615), 1.798e-13 below #1017. Controls plan for all three, written before any route or measuring program read a certificate: packing/campaign/issue-intake/upper-bounds-1015-1020-20261118/controls-plan-127.txt, SHA-256 7f287382016b993970e1162a06b0d7faea75f560bcbd2fed9cf5be80b34743ff, hashed 2026-11-18T01:26:53Z.

R-127 (blind review), 2026-11-18 01:42Z: lane r127-1118 started on branch claude/intake-2026-11-18-review-1015 (worktree /home/user/wt/r127, from main 2980557a2). Six certificate files fetched twice at the three pins, bytes equal. Writing the clean-room checker and controls plan; nothing run on a certificate yet.

2026-11-18T02:05Z w6-dewinter-1118: stages 1-2 and the replay done, pushed at 128d28c94 on claude/intake-2026-11-18-import-1015. Packets de-winter-s127-issue1015/1017/1020-2026-11-17. Replay: 9 jobs on both routes, 144,018 pair decisions, all positives accepted and gross controls refused; 33 sharp controls all as planned (verdicts), the near-wall branch differing from the plan's expectation at #1015 and #1020, which clear every wall. Margins T-305 1.2099e-10, #1015 7.74e-63, #1017 4.19e-14, #1020 1.82e-58; steps outside padding (narrowest #1020 over #1017 at 4.29x), so option D makes all three new results. Identity: none one to one with T-305 (10/11/9 beyond 0.1); #1017 = #1015 moved, #1020 = #1017 moved. Ledger upper-bounds-1015-1020-20261118 records all three. Next: register as T-327..T-329 after import-1009 merges; map R-127 when it lands, adopt #1020's at 127, regularize. CPU so far about 0.3 h.

2026-11-18T01:50Z w6-dewinter-1118: correction: the previous note's time, 02:05Z, was wrong; it was written at about 01:47Z.

R-127 (blind review), 2026-11-18 02:03Z: checker and controls plan frozen and pushed at 950cf3106 (branch claude/intake-2026-11-18-review-1015), before any program read a certificate. Next: the runs (priced under one CPU-hour).

2026-11-18T02:21Z w6-dewinter-1118: records committed and pushed at d4d2866de (merged main a1a8d0aae, #909): T-314..T-316 PROVISIONAL ids for #1015/#1017/#1020 (S3/S2/S1, V3/C3 on the replay); renumber to T-327..T-329 when import-1009 (T-314..T-326) merges first. Records tier passed but for the synopsis count (fixed). No-public-change record written (explainer differs only by register count 316 vs 313). Waiting on: R-127 review to map; import-1009 merge; then adoption at 127 (house -> #1020's) and regularization.

R-127 (blind review), 2026-11-18 02:40Z: runs done and pushed (branch claude/intake-2026-11-18-review-1015). Writing the findings; freeze next.

2026-11-18T02:31Z w6-dewinter-1118: draft PR https://github.com/jlevy/squares/pull/1024 opened at d4d2866de (labels intake, S3), provisional ids T-314..T-316 (to be T-327..T-329 after #1023, import-1009, merges).

R-127 (blind review), 2026-11-18 02:27Z: findings frozen and pushed at 3db7ac1fe (checker freeze 950cf3106 at 02:02Z). Verdict: all three certificates (#1015, #1017, #1020) accepted, both files each; every report-order step beats its predecessor's contraction margin (closest #1017 to #1020: gain 1.79761e-13, margin 4.19030e-14, ratio 4.29). Significance confirmed here: #1015 S3, #1017 S2, #1020 S2. (Correction: the previous note's 02:40Z should read 02:20Z.) Next: post-freeze comparison, doc map, synopsis, draft PR.

2026-11-18T02:28:01Z w6-dewinter-1118: correction: the note headed 02:31Z (PR #1024 opened) was written at about 02:24Z, and the one headed 02:21Z at about 02:20Z; times were mistyped.

R-127 (blind review), 2026-11-18 02:40Z: draft PR #1025 opened (labels intake, S2), head b11797085 (main a1a8d0aae merged in), base a1a8d0aae; coordinator messaged for a senior review; hosted CI pending at handoff. Review: docs/project/reviews/review-2026-11-18-de-winter-1015-1017-1020.md; packet packing/resources/web/de-winter-1015-1017-1020-review-2026-11-18/. About 0.55 CPU-hours in all. Lane r127-1118 stops here; worktree /home/user/wt/r127 is left untouched for the review round.
