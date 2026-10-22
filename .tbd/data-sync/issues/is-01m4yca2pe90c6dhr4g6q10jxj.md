---
type: is
id: is-01m4yca2pe90c6dhr4g6q10jxj
title: "Import Francisco Couzo: 14 campaign upper bounds (237, and 13 beyond 324), 7 replayed Kevin Fang composites, 2 precision refinements (#607)"
kind: task
status: in_progress
priority: 1
version: 11
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-14T23:35:08.750Z
updated_at: 2026-10-22T13:13:29.350Z
started_at: 2026-10-14T23:35:12.236Z
---
Francisco Couzo (@franciscouzo) reports, in jlevy/squares#607 (filed 2026-10-14T23:18:36Z), 21 finite upper bounds plus two precision refinements, certificates at franciscouzo/square-packing 43ac7d29cfeb7b71ea1eb09939cb30b9f71850f2 submissions/2026-10-14/certificates/ (first committed 2026-10-14T19:15:09Z), comparison index upper_bounds.json at 487b05809099d8f7d006aaeb6bfc1ebe95cb8d0d. Stages 1, 2 and the stage 4 replay in the 14 October evening intake lane (branch claude/wizardly-meitner-wqn4x3-intake-607); no register, case, request, coverage, bibliography, resources README or intake-watch record edited. Registration waits for a records PR.

GitHub issue: https://github.com/jlevy/squares/issues/607

## Notes

**Lane.** 14 October evening intake lane under think-mq0k, branch `claude/wizardly-meitner-wqn4x3-intake-607` from `main` 9b32da04d (#602 merged, T-161 to T-184 on main). Stages 1, 2 and the stage 4 replay; no register, case, request, coverage, bibliography, resources README or intake-watch record edited (the records PR of think-3aum owns those). Packet: `packing/resources/web/couzo-certificates-2026-10-14/`. Tests: `packing/tests/test_upper_bound_reports_607.py`.

**Pin.** franciscouzo/square-packing 43ac7d29cfeb7b71ea1eb09939cb30b9f71850f2 (2026-10-14T19:15:09Z, tree 17312eac), head of master when retrieved at 23:30Z; it adds only submissions/2026-10-14/ (50 files) to its parent 487b058 (17:45:39Z), whose upper_bounds.json (blob 58710e5c, the same at both) is the index the issue compares against. Issue filed 23:18:36Z; no comments or edits when read; labelled intake. All 49 SHA256SUMS lines and the manifest's 23 certificate digests agree with the bytes at the pin.

**Claims (every one the issue makes).**
- 14 campaign bounds (Couzo's own): s(237) <= 15.902603638284 (continues Mykhailo Polkovskyi's #593), and beyond 324: 339 18.915818555470, 382 19.987621154241, 409 20.767428349966, 419 20.959997582079, 450 21.767428350587, 461 21.973183753375, 552 23.968034845503, 599 24.968034846127, 648 25.968034846328, 649 25.976974088403, 651 25.984515068279, 757 27.991000865994, 804 28.920398747577.
- 7 Kevin Fang composites, credited to Fang, replayed by Couzo: 703 26.999256308447, 812 28.988287236851, 930 30.988287236851, 931 30.994048655032, 992 31.997220361783, 993 31.991327887692, 994 31.999256308447.
- 2 precision refinements listed separately: 342 18.964706723173, 542 23.828427124774.
- Checker statements (sqpack verify at 37e6757; Evan Daniel's verify_cert.py at 622cd2e, SHA-256 3299ca0c; the campaign's Rust checker for the 16 own certificates) are the author's. No optimality claim.
Each certificate's exact header side rounds up at 12 places to the printed side (read_facts admits all 23).

**Fang's composites (for think-rn2y).** All seven certificates are Fang's byte for byte: each SHA-256 equals the sha256 column of its row in composites/table.csv (blob 04094421, the same at bef5c42 and 078789a), and each row is Fang's smallest at its count. 703 (L1_n27_703_r17x16_n0257+n-110) and 994 (L1_n32_994_r17x16_n0257+n-241) are shipped files, whose digests the fang-excess-theorem packet pins (0ba5cd28..., aef770c7...); 812, 930, 931 (r19x18 row; Fang's shipped 931 is 5.21e-3 larger), 992 and 993 are table-only rows the author regenerated with Fang's glue.py, and the bytes have the table's digests. They cover 2 of the 28 shipped-smallest counts (703, 994) and 5 of the 53 table-only-smallest counts (812, 930, 931, 992, 993). This packet retains all seven and replays them.

**Comparison (main 9b32da04d; claims.json frozen by check-claims --write).**
- 237: case ceiling T-140 (Chaoweeraprasit, improved by Couzo) 15.9029496076778317, below by 3.46e-4. Below every other report: #593 / T-183 (Polkovskyi) by 1.014e-4 (the smallest earlier report); #561 / T-161 and PR #574 / T-174 by 3.44e-4; #573 by 3.46e-4; T-136 by 3.86e-4; T-098, T-115, T-127, T-134, #505, #470 by 1.07e-3 or more. Mishapolk 70a033f has no 237.
- Beyond 324 (current row, or grid): 339 below the current row (#586) by 9.50e-3 and Couzo's 487b058 by 2.29e-4; 342 below the current row (Couzo 8 Oct report) by 2.68e-10 and #476 (= 487b058's 342) by 2.86e-10; 382 below #586 by 9.20e-5, 487b058 by 1.34e-7, Fang c284cd0 by 1.86e-3; 409 / 450 below 487b058 by 5.07e-5; 419 by 1.50e-3; 461 by 1.29e-3; 542 by 1.02e-9; 552 by 5.73e-3 (Fang composite by 2.03e-2); 599 / 648 by 5.55e-3; 649 by 8.12e-4; 651 below the current row (Fang e646c47) by 7.03e-3 and 487b058 by 3.79e-4; 757 below 487b058 by 1.47e-3 and Fang's composites by 6.55e-3; 804 below 487b058 by 6.78e-3. At 703, 812, 930, 931, 992, 993, 994: the claim record is undecided against Fang's 15-place print (differences < 1e-15); the digests decide: the same file.

**Report order and the per-count rule.** The certificates are reported at 43ac7d2's commit, 19:15:09Z (watched repository), before the issue. Recorded at 16 counts: 237 (a refinement of Polkovskyi's #593 packing, credited Couzo after Polkovskyi), and 339, 342, 382, 409, 419, 450, 461, 542, 552, 599, 648, 649, 651, 757, 804 (342 and 542 refine the author's own packings; 382 and 651 continue Fang's). Not recorded at 7 counts: 703, 812, 930, 931, 992, 993, 994 tie Fang's earlier rows (bef5c42, 2026-10-12T19:13:41Z), so Fang keeps them; this packet's bytes and replay are evidence for Fang's rows (think-rn2y). 487b058's own certificates are earlier reports at 16 of these counts and an import of their own (think-nj7h).

**Not this import (think-nj7h).** 487b058 adds 290 certificates (370, 403-991), changes 7 (211, 339, 378-382) and deletes 22, with no issue. Its n211.cert states 7496774813149710519467765230441/5e29 = 14.993549626299..., 9.29e-6 below #586 (best now at 211): an in-corpus report nobody has imported.

**Replay.** All 69 jobs (a positive, a duplicate-square control and an outside-container control per count) decided one at a time by the decide-job command certify runs, --workers 1, 23:41Z 14 Oct to 03:55Z 15 Oct (the runner was stopped once by the two-hour background limit, during 812's duplicate-square control, and resumed from there); `certify --workers 1 --finished` assembled and admitted the receipt, kept as 23 shards receipts/exact-certification-nNNN.json.xz. Both routes accept all 23 positives and refuse all 46 controls. 31,386,744 pair decisions, 12,425.76 route CPU-s (3.45 CPU-h), 14,795.58 job wall-s, longest job 632.89 s (994 outside control); load average 2 to 11 on 4 shared cores. Margins (both routes equal): the 16 own certificates clear every wall by exactly 1e-15 and every pair by 9.76e-13 (419) to 1.60e-12 (339); the 7 composites every wall by exactly 2^-65 and every pair by exactly 2^-64, as the author's logs of Daniel's checker print. A fresh serial check --replay follows in chunks (update below).

## Acknowledgement draft (not posted)

Thanks, Francisco. We have #607 and have retained the 23 certificates at franciscouzo/square-packing 43ac7d29cfeb7b71ea1eb09939cb30b9f71850f2 (submissions/2026-10-14/), with their digests; your SHA256SUMS and manifest agree with the bytes.

Each certificate's exact side rounds up to the side you print. Against the record and every earlier report at each count, in the order they reached us (your certificates count from their commit at 19:15Z):

- s(237) <= 15.902603638284 is 1.01e-4 below Mykhailo Polkovskyi's #593, the smallest earlier report there, and we'll credit it as your refinement of his packing, as you ask.
- The 13 campaign bounds and the two precision refinements beyond 324 are each below every earlier report, your own 487b058 certificates included.
- The seven composites at 703, 812, 930, 931, 992, 993 and 994 have exactly the SHA-256 Kevin Fang's table lists, so they are his certificates, published on 12 October. They'll be recorded as Fang's results, as you ask, with your files and our replay as evidence for them.

Both of this repository's exact routes accept all 23 certificates, and refuse a duplicated-square and a moved-outside mutation of each. A records pull request will register the results; we'll reply here when it merges.

One question: 487b058 also changes certificates/n211.cert, to 14.993549626299..., below your #586 certificate, and adds certificates at 370 and 403 to 991 that no issue reports. We'll take those up as a separate import, reading each from its commit; tell us if any should wait. Your later 4e4c8ce certificate at 237 is a further 2.4e-11 below the issue's; we retain it as a separate report, so tell us if you want it registered in place of the issue's.

2026-10-15 reads lane (think-mq0k, branch claude/wizardly-meitner-wqn4x3-reads-1015): franciscouzo/square-packing moved past this import's pin. Head 58a783368d4b7e70bb800f0009ea9ca03e578739 (2026-10-15T01:25:11Z), two commits after 43ac7d2: 4e4c8ce (00:31:53Z, "Update all verified bounds for n < 1024") and 58a7833 (Göbel square and strip bounds). #607 has not been edited since 2026-10-14T23:27Z, so it still names 43ac7d2.

At 237, 4e4c8ce adds certificates/n237.cert (and the same bytes at certificates/best/n237.cert), a different file from #607's submissions/2026-10-14/certificates/n237.cert: s(237) <= 7951301819129798440089572127137/5e29 = 15.9026036382595969, 2.40e-11 below #607's 15.902603638284 (exact; at least 2.34e-11 below every number the print may be). Its metadata calls it an exact optimum seeded from #593, so it is the author's exact refinement of his own #607 packing. Under the per-count rule #607's 237 is still recorded at its first commit (19:15:09Z), and 4e4c8ce's is recorded after it, as a later and strictly stronger report. Imported separately: think-7j8o, packet couzo-n237-2026-10-15 (retained, compared, replayed on both routes: positive passes, both controls refused, 50.9 route CPU-s). The #607 acknowledgement could mention it ("your 4e4c8ce certificate at 237 is a further 2.4e-11 below; we retain it as a separate report, tell us if you want it registered in place of the issue's").

The seven Fang composites and the beyond-horizon submissions: 4e4c8ce's certificates/best/ index restates them; at 703, 757, 813, 931, 932, 992, 993 and 994 its README says eight new glued witnesses use Fang's rectangles, which this lane did not compare with #607's files (beyond the horizon; see the 4e4c8ce beyond-horizon triage bead).

**2026-10-15 replay update (this lane).** Branch claude/wizardly-meitner-wqn4x3-intake-607 at 77cec4292 holds the packet, the 23 receipt shards, register-plan.yaml (the raw plan with a header applying the per-count rule) and packing/tests/test_upper_bound_reports_607.py (9 tests, admitted to the suite record with suite_files admit-local). Main moved to 6964362b5 (#609) during the replay: merged into the branch, the claim record re-frozen there, every relation unchanged. packing-validate --records passes (51 of 109 steps, the named tier); acquire_source --check passes. Register plan: one T-NNN at 237 (V0/C0, pending adoption below T-183), evidence E-couzo-607-certificate-report, source row couzo-certificates-2026-10-14 with beyond-horizon rows; the records lane keeps the rows at 339, 342, 382, 409, 419, 450, 461, 542, 552, 599, 648, 649, 651, 757 and 804 and registers 703, 812, 930, 931, 992, 993 and 994 as Fang's rows (think-rn2y) with this packet as evidence.

**2026-10-15 check --replay (this lane).** A fresh serial check --replay decided all 69 jobs again, equal to the retained rows apart from timing, in four --n runs (237-651, 703-812, 930-992, 993-994), 04:04Z to 08:09Z, each under the two-hour limit: 14,683.9 s wall, 13,125.2 s CPU (3.65 CPU-h); every run exit 0. Branch head 1af5267f6 (pushed). Main has since moved to c4c690a3e (#612, T-185 to T-187): nothing at these counts changed, so the claim record frozen at 6964362b5 stands. Lane complete: no run pending.

## 2026-10-15 records-1016 lane (think-mq0k), branch claude/wizardly-meitner-wqn4x3-records-1016, https://github.com/jlevy/squares/pull/616

Registered as T-189 (V0/C0, draft S2) at 237, with 15 beyond-horizon rows (339, 342, 382, 409, 419, 450, 461, 542, 552, 599, 648, 649, 651, 757, 804), each superseding 487b058's row (T-188's source) or, at 342, Couzo's 8 October report. The declaration now lists T-056 at 237 and labels its reports without commit ids (487b058's as couzo-verified-bounds-2026-10-14, Fang's as "Fang composite ..."/"Fang theorem/..."), and its `requested` roster is the 16 counts recorded as Couzo's, so the beyond-horizon claims record holds the 15 rows; claims refrozen at main c4c690a3e, no relation moved. #607 has a request entry (answer bead: this one); no reply posted. The 7 Fang composites are not recorded: Fang's rows are not on main. What think-rn2y needs: a Fang composites source with a claims record and rows at 703, 812, 930, 931, 992, 993, 994 at his table sides, citing this packet's retained bytes and replay (each file has the table's SHA-256) and, at 703 and 994, the shipped files the fang-excess-theorem packet pins. Reply owed after merge (T-189, and T-188/T-190 per the draft above). Keep open until #607 is answered.

2026-10-16 coordinator: per #627 (616/A4), this bead owns the review and adoption of T-189 and T-190 (T-189's next rung already weighs T-190); T-190's review moves here from think-7j8o.

2026-10-16 coordinator (#627 review C, C3): when T-188 is reviewed, cite the seed's sha256 7d35edaa..., equal to the SHA-256 of T-175's retained dostashev-merged-bands-2026-10-13/source/records/n0211.sqcert, so the #575 credit rests on matching bytes.

2026-10-16 12:40Z user-eb-records-185-190: DRAFT replies (not posted; after PR #657 merges). #607:  @franciscouzo, the independent review of 16 October accepted, for finite feasibility only: - #607's 237 (T-189, V3/C3, S3); its fifteen beyond-horizon rows rest on the import lane's replays and were not reviewed; - the 211 of `487b058` (T-188, V3/C3, S2), now the house at 211: a further arrangement of Daniil Ostashev's #575 design, five squares moving more than a tenth, so it is recorded with no regularization item; - the 237 of `4e4c8ce` (T-190, V3/C3, S2), now the house at 237, 2.40e-11 below #607's, which stays recorded as history. Two questions from the review: `certificates/n211.json` at `487b058` labels its seed issue #501, but the seed file is byte for byte Ostashev's #575 `records/n0211.sqcert`: is #575 the seed you meant? And should the `4e4c8ce` 237 be recorded after #607's, as now, or in its place? Regularization on the new witnesses: at 211 every view of both generators goes to the owner's review, so the axis tool's view is drawn for now; at 237 the selection is pending (think-r3cl).   || #506 (its answer bead think-9fjl is closed, so drafted here):  @franciscouzo, an update on the 175 of your #506 release (first committed in `f311f08`, held at `337078c`), registered as T-185. The independent stage 4 review of 16 October (docs/project/reviews/review-2026-10-16-upper-bound-imports-506-607.md) accepted it for finite feasibility only: the three retained jobs at 175 reproduced on both of this repository's maintained exact routes, and a third exact route agreed. T-185 is now V3/C3, S2 (a refinement of your #488 packing at 175, no square moving more than 0.012). Confirmed, re-implemented: one maintained route is the sqpack verifier you report running, so the independence rests on the independent rational corner checker. The bound stays superseded at 175, now by Mykhailo Polkovskyi's T-186, the case's house since 16 October. The record no longer calls your #488 packing a refinement of Ryan Xu's: measured pose by pose, it started from Xu's packing and does not pair with it one to one.

2026-10-22 c-triage-1022b (read-only; coordinator scratchpad triage-1022b/couzo-residue-plan.md).

**What the Couzo history records PR (after #719's) changes for #607.**

- 8 of #607's rows (`couzo-certificates-2026-10-14`) become superseded first by Couzo's
  `4e4c8ce` (339, 382, 450, 552, 599, 648, 757) or `5a299b4` (409).
- **542**, the deletion bound #627 review C raised, has two parts:
  - `4e4c8ce`'s index bound is 7.46e-14 below #607's row with the same 12-place print,
    which puts it in the sub-print class (O1, `think-fwa9`);
  - `23aff0c`'s later deletion bound, 1.47e-2 lower, waits on O2/D6.
  #607's row stays current at 542 until those are decided.
- `think-yfoo`'s triage planned "the ask on #607". A state note there, after the merge,
  covers it.
