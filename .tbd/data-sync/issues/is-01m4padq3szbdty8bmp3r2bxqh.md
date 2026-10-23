---
type: is
id: is-01m4padq3szbdty8bmp3r2bxqh
title: "Import Francisco Couzo: 304, 305 and nine beyond-horizon counts 338-381 (#506)"
kind: task
status: in_progress
priority: 1
version: 10
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T20:28:15.353Z
updated_at: 2026-10-23T02:26:18.334Z
started_at: 2026-10-11T20:28:27.023Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
https://github.com/jlevy/squares/issues/506 (2026-10-11T18:06Z). franciscouzo/square-packing 337078ca3e05153aceb099237b175cf64af5748a certificates/nN.cert. 304 and 305 below SQUISH #500; 338, 339, 344, 375, 376, 378, 379, 380, 381 beyond the case corpus. Stages 1-4 replay through devtools.upper_bound_reports.

## Notes

## Stage 1 triage (2026-10-11, lane B of the 2026-10-11 intake pass, read at main 3a5a91a90)

- Pin: franciscouzo/square-packing 337078ca3e05153aceb099237b175cf64af5748a (master head when read, committed 2026-10-11T17:29:19Z, tree 2766f6aa, parent f311f08 of 2026-10-11T03:39:54Z, itself the child of #488's pin 3ef7634). No licence in the tree. Issue filed 2026-10-11T18:06:50Z.
- Every claim of the release (certificates README at the pin: 68 certificates; its SHA-256 prefix, exact side and 12-place ceiling agree with every file). Since 3ef7634: f311f08 adds 308, 343, 380 and changes 175, 340, 376, 378, 379; 337078c adds 344, 381 and changes 304, 305, 338, 339, 375, 376, 378, 379, 380. 15 differ from 3ef7634; 53 unchanged (132, 209, 237, 270, 303 as the issue-488 packet's copies; 48 as the issue-476 packet's).
  - Requested, in corpus: 304 = 8964782973424250487190982671787/5e29 (17.929565946849), 305 = 3590093296427542454697714045223/2e29 (17.950466482138). Both exact optima (Evan Daniel's solver).
  - Requested, beyond n <= 324 (beyond-horizon list): 338, 339, 344, 375 (rational witness, centres dilated 1+1e-11; side excess 1.89e-10 over n375.txt agrees), 376, 378, 379, 380, 381.
  - Not named (each an import of its own): 175 = 27534238048396728577781532581/2e27 (13.767119024199, README "best known"); 308 = 17.998459831024 ("superseded"); 340 = 18.939649632892; 343 = 18.993870589750 ("superseded").
- Map (stage 1 table): 304 and 305 are bounds the record does not hold -> one new upper-bound entry, scope [304, 305], V0/C0 at registration. The nine beyond the horizon -> dated beyond-horizon rows of the new source, superseding the current rows at 338, 339, 375, 376, 378, 379 (Couzo's own ffd900d/2d32a6e rows, think-1545) and at 344 (Evan Daniel's verified Hunt 3 row, think-xm4h, 9.73e-5 above); new rows at 380 and 381. 175 (new smallest at 175, 1.70e-6 below T-140) and 340 (below its row by 2.30e-4) are imports of their own; 308 (above T-141 by 1.90e-4) and 343 (above Hunt 3's row by 1.56e-2) are beaten by results already held and marked superseded by the source; they stay in the packet, decided but not registered.
- Who else holds each value: 304 case T-098 17.934650018390681724105084929881 (below by 5.08e-3); #500 SQUISH prints 17.929657042170880 (above by 9.11e-5); #476 = T-098. 305 case T-098 17.952959459015527962875662582531 (below by 2.49e-3); #500 prints 17.950544853925636 (above 7.84e-5); T-140 (#488) and #489 hunt3_n305, one side, above 6.73e-4; T-136 (#481) above 7.30e-4. No other 2026-10-11 report (#501, #503, #504, #505) shares a count. Beyond: see the packet README table; all nine are the smallest known at their counts.
- Validation plan, priced: the two maintained exact routes (sqpack.verify and check_rational_witness_independent via devtools.evand_arrangement_reports) on all 15 changed certificates, positive + duplicate-square + outside-container each = 45 jobs; precedent #488 was 27 jobs in 388 route CPU s, so about 15-25 min serial at --workers 1 under this machine's load. Then check --replay (same again). Nothing here needs the source's code (verify_cert.py not run). Third route check_half_angle_area is a separate review lane, not run here.

## Acknowledgement draft (stage 1; not posted)

@franciscouzo, thank you. Received: the eleven certificates of #506 at [franciscouzo/square-packing@337078c](https://github.com/franciscouzo/square-packing/tree/337078ca3e05153aceb099237b175cf64af5748a/certificates) (committed 2026-10-11T17:29:19Z), pinned at that commit. The 15 certificates that commit and f311f08 add or change since #488's pin are retained here as factual data, including four the issue does not name (175, 308, 340 and 343); each of those is compared and is an import of its own.

What will be checked: every one of the 15 is decided by both maintained exact routes, `sqpack.verify` and the independent rational corner checker, with a duplicate-square and an outside-container control each, and its exact side is held to the side you print. 304 and 305 are compared with their case records and with every pending report at those counts, including SQUISH's #500 and your #488; the nine above 324 are compared with the beyond-horizon rows the record tracks and are recorded as author reports outside the case corpus, as you ask. A separate review follows. Your `verify_cert.py` and `sqpack` runs are recorded as your statements.

---
_Generated by [Claude Code](https://claude.ai/code)_

## Stages 2 and 4 replay (2026-10-11, lane B worktree branch worktree-agent-ac023df3fbe3880aa, commits 80f4a3708 and 0df40a7db, not pushed)

- Packet packing/resources/web/couzo-certificates-2026-10-11 (acquire_source from a clone at the pin; --check PACKET_MATCHES_ITS_CONTRACT): 15 certificates retained (771,778 bytes), 53 pinned identical_to the issue-476 (48) and issue-488 (5) copies, two READMEs and 15 nN.txt pinned by digest; manifest 85 files, 3,066,594 bytes. report.json, claims.json (read at main 3a5a91a90) and beyond-horizon-claims.json (the nine requested beyond 324). Source key [Couzo certificates 2026-10-11]; upper_bound_reports gains its exact HOUSES reader.
- certify --workers 1: 45 jobs, 15 positives pass both routes, 30 controls refused (each on its overlap or wall), 5,234,106 pair decisions, 2,540.17 route CPU s, 5,568.25 job wall s summed, longest 287.72 s (379 positive); least wall clearance 1/2e20 and pair gap just under 1e-20 in the 14 exact optima, 1e-15 and 7.05e-12 in the 375 witness. The run was stopped by the 90-minute background limit after 42 jobs (load 9-20 on four cores); the three 381 jobs ran by the same decide-job command and certify --finished assembled and admitted the receipt.
- check --n N --replay, once per count, serial: all 15 exit 0, every row equal apart from timing, 4,516 s (75 min 16 s) summed.
- register-plan printed (T-NNN placeholders); shared records not edited. The records lane must mark the current beyond-horizon rows at 338, 339, 375, 376, 378, 379 (Couzo's) and 344 (Hunt 3, verified) superseded_by couzo-certificates-2026-10-11.
- Checks: packing-validate --records 49/107 steps, exit 0, 178 s; tests/test_upper_bound_reports.py 157 passed; ruff, ruff format and basedpyright clean on the two touched files. Third route (check_half_angle_area) not run (separate lane); verify_cert.py not run.

Reopened: Reopened by the 2026-10-12 reconciliation (think-va12): packing/campaign/intake-watch.yaml still names this bead as the owner of its repository's read-through, and check_bead_tree requires a record that declares a deferral to name an open bead. The import itself is complete; close this bead in the change where the next intake pass updates that intake-watch entry.

2026-10-22 c-triage-1022b (read-only; coordinator scratchpad triage-1022b/couzo-residue-plan.md).

**`f311f08`'s beyond-horizon certificates by report order.** The publication is
2026-10-11T03:39:54Z.

- **340 is current.** 18.939649632892 is below the 8 October decimal row by 2.3e-4. It is
  one of the 32 rows #715's import reply left to the imports of their commits.
- **378, 379 and 380 are history**, superseded by `couzo-certificates-2026-10-11` (#506,
  `337078c`).
- **376 is held**, above Göbel's construction (`think-8krd`). `main` already records
  superseded rows above Göbel at 376, so the owner's #613 answer decides it.
- **Packets.**
  - 340's bytes (blob `5bcda593`) are the copy `couzo-certificates-2026-10-11` retains.
  - 378, 379 and 380 need a small packet at `f311f08`: `couzo-extended-certificates-2026-10-11`,
    0.17 MB.
- **Closure.** All four rows land in the one Couzo history records PR after #719's, which
  closes this bead's beyond-horizon remainder.

blocked_on: think-xyhn

2026-10-22 (c-lane-couzo-residue-1022): The records change is PR #730 (branch claude/intake-couzo-history-2026-10-22, lane c-lane-couzo-residue-1022), records commit a91c70907, 22 October 2026. The history walk (packing/campaign/issue-intake/upper-bounds-couzo-history-20261022) walks every count from 325 to 1024 from starts frozen at main a97b712b9. It covers every row source since then and every publication in a watched repository below the start. It reproduces the c-triage-1022b walk's recorded chain at every count. The one difference is that #715's 30 re-certifications are attributed to #715 rather than to 5a299b4, and they are held either way. 319 rows are recorded at assurance reported, 107 current and 212 superseded on entry; 236 existing rows are repointed. 340 publications are held back, each with its decision's bead (beyond_horizon_replay.HISTORY_HELD). The filtered two-route replay with six controls covers all 319 rows.

For this bead (f311f08): 4 rows of the new source couzo-extended-certificates-2026-10-11, dated 2026-10-11T03:39:54Z by the commit, retained in the new couzo-extended-certificates-2026-10-11 packet: 340 current, and 378, 379 and 380 superseded on entry by #506 (337078c). Held: 376, above Göbel (think-8krd). #715's restatement at 340 now names the row. The 337078c read in intake-watch.yaml still names this bead; this PR leaves it, since its other items (the in-corpus updates the triage lists) are outside this lane. Filtered replay: 4 verified, 24 controls refused, 2.1 positive CPU s. The bead stays open until the PR merges; the coordinator closes it.

2026-10-23 (c-lane-couzo-residue-1022): #730 (https://github.com/jlevy/squares/pull/730) merged at 02:10Z on 23 October 2026 as fcf2f96a5 and recorded f311f08's four rows (couzo-extended-certificates-2026-10-11: 340 current; 378, 379, 380 superseded by #506). The beyond-horizon remainder of this bead is done. It stays open: packing/campaign/intake-watch.yaml on main still names this bead for the franciscouzo/square-packing read through 337078c, so closing it would leave a dead deferral (check_bead_tree invariant 3) and fail the next change to intake-watch.yaml. Close it in the change where the next intake pass updates that entry, with the in-corpus items the triage lists.
