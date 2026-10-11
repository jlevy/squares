---
type: is
id: is-01m41hjrm7a3vdmbhtbyj9rq71
title: "Import wand125's 22 certificates posted on #282 on 3 October (mixed_n95_L996 … mixed_n69_L8612)"
kind: task
status: closed
priority: 1
version: 11
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
hold: null
hold_until: null
created_at: 2026-10-03T18:49:17.703Z
updated_at: 2026-10-06T23:14:27.446Z
started_at: 2026-10-06T07:50:57.086Z
closed_at: 2026-10-06T23:14:27.446Z
close_reason: "T-082 at V3/C3 at all 22 counts, merged in #396 (75195561f); answered on #282, issuecomment-6027158015"
resolution: null
duplicate_of: null
---
Found by the final-reply lane: check_requests --github lists 22 comments on #282 after 2 Oct 15:16 UTC carrying new mixed rectangle-measure certificates. None is retained, reviewed or registered. Runbook stages 1-3 (retain, preflight, blind review, register at V0), then replay runners as for T-075. Also check whether their Green comparisons use proper upper enclosures (audit finding MX-2/AF-1). #282 stays open for these.

## Notes

2026-10-03 20:50 IM282b done: claude/import-282-oct3 @bce32635b, PR #324. T-082 at V0/C1 (S3 proposed), 22 counts n = 51..96, packet wand125-mixed-bounds-2026-10-03 at 2aff2076, all 22 pass exact audit and pre-replay checks; blind review accepted (OC-1 improvement_lower at n = 88, 93 not lower bounds; OC-2 six uncertified comparison values; OC-3 exit 0 on ANGLE_UNRESOLVED; OC-4 corrects MV-2; OC-5 README). Replay plan: 8 runners x 4 workers, ~162 CPU-h (budget 165-225), ranges in the packet README. Runners HELD pending the owner's answer on load (weekly limit warning). Findings to post on #282 once merged.2026-10-03 22:55 PR #324 merged into main at 4949d1439: T-082 at V0/C1, S3 (stages 1-3, blind review accepted, OC-1..OC-5). Findings OC-1/OC-2 posted to @wand125 on #282 (issuecomment-5974294911). Remaining: the 8 replay runners (about 162 CPU-h; held until after the 7 Oct usage reset per owner), mixed-merge per certificate, then a replayed entry moving each count to V3/C3.

2026-10-06 07:50Z lane R4 of think-wyf4 (worktree squares-lanes/r4, branch claude/ecstatic-pascal-pothtx-r4 from ebf232767): owner released the hold under think-3ok2. None of T-082's 22 or T-090's 16 is in the 149-certificate census (census-mixed has none from the 10-03 or 10-04 packets), so all 38 need sqverify-fast rows. Built sqverify-fast at main's reviewed crate source d97758bb (binary 567a0fd5, rustc 1.98.0), the binary of T-099/T-100. Running the census then --control, one certificate at a time, largest verified-bound gain first: T-090's 16 (12 with a gain, n = 93, 57, 51, 86, 75, 72, 69, 42, 44, 43, 56, 95; then n = 84, 67, 88, 94, dominated by T-094 and T-091). 1 thread while process group 8378 runs, then 2.

2026-10-06 09:45Z lane R4: n93_L988 (1,317 CPU-s) and n57_L78725 (1,816 CPU-s) VERIFIED with controls refused, at 1 thread on a host at load 11-18 (~0.5 core). Coordinator decision: finish T-090's 16 whole (no split), go to 2 threads once PG 8378 exits or load5 < 8; then T-082's 22 on the same branch (no longer a priced remainder). Queue after n51: the other 13 of T-090, then T-082's 22, gain first (n89, n74, n55, n52, n96, n92, then the 16 dominated by T-090/T-091). Also done: T-075's six afternoon certificates got controls and independent replay entries (2bda0d5a4, b3e917247, re-pin b2d94b082); the census tool states a row's own threads (5f8d9994f).

2026-10-06 15:30Z lane R4: T-090 exit committed on claude/ecstatic-pascal-pothtx-r4: be3364eab census (16/16 VERIFIED, controls refused, 26,382 CPU-s), 794a2d123 records (T-090 V3/C3; verified lower bound moves at n = 42, 43, 44, 51, 56, 57, 69, 72, 75, 86, 93, 95 and 96), ec173e301 re-pin, 65a8dcbce tests. T-082's 22 now running (started 15:00Z with n89, gain first), same rules.

2026-10-06 18:30Z lane R4: T-082 so far 9 of 22 VERIFIED with controls refused, except mixed_n96_L997: VERIFIED (least 1.0000000000057894 at r=139) but its v1 control CONTROL_FAILED, the 99/100 mutant verified at r=139 (FC-1, think-0uia). Coordinator chose to fix FC-1 here: devtools.sqverify_fast_census --control now runs the 99/100 mutant at every direction (fix worktree r4-fc1, commits 9f36ede38 + f1ddc2379, not yet on the branch). Separately prompted review (claude -p tbd-strong): accept with fixes, CC-1 blocking (count only coverage refusals), CC-2..CC-8 non-blocking; all addressed in f1ddc2379; re-check running. Re-control of n96_L997 with the fixed code at 2 threads: CONTROLS_REFUSED (v2), 187 of 201 refused with exact witnesses in the per-bin domain, 14 directions verify the mutant (slack). Plan: commit T-082 in (b) state (21 replay entries) when the census ends, then the FC-1 commits and n96's admission as follow-ups.

2026-10-06 22:00Z lane R4: T-082 exit committed on claude/ecstatic-pascal-pothtx-r4, after fast-forwarding to the FC-1 fix (9f36ede38, f1ddc2379, 03174112b).

- 9d69d4488 census: all 22 VERIFIED at 201 directions, 2 threads, 28,705 CPU-s (551 to 2,069 each). v1 controls refused on 21; n96's v1 failed closed (FC-1) and is kept as control-failed-v1.json.
- da07cbbe1 records, (b) state: T-082 at V3/C3 with 21 replay entries. The verified lower bound moves at n = 52 (151/20), 55 (966/125), 74 (3547/400), 89 (193/20) and 92 (977/100). T-070 is superseded. VERIFIERS.md is regenerated (CR-1).
- e02e0557e: the two FC-1 reviews, stored byte-identical.
- 2a6585a9d: n96 admitted under the v2 control (187 of 201 refused). T-082 holds all 22 replays, and n = 96 moves to 997/100.
- c0249ef16: re-pin.

At the other 16 counts the source's later certificates (T-090, T-091) are higher, and the case records cite T-082's replays beside them. The source checker's replay (about 162 CPU-h) was not spent.
