---
type: is
id: is-01m4k11tz4tg1smpwmeknqjs9y
title: "Couzo 02f9690 beyond-horizon certificates: 15 below the tracked rows (n375 by 4.29e-5, n378 by 4.00e-4), 5 above"
kind: task
status: in_progress
priority: 2
version: 8
delegate: coord-intake-1021b
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T13:46:45.604Z
updated_at: 2026-10-22T20:36:14.855Z
started_at: 2026-10-22T02:18:23.092Z
---
Found by the importer lane (think-md2i) in packing/resources/web/couzo-exact-certificates-2026-10-09/acquisition/claims.json: franciscouzo/square-packing 02f969075f79 holds 20 certificates beyond the n <= 324 horizon. 15 are below the tracked dated beyond-horizon rows (332, 336-341, 369, 373-379; 375 at 9953490883645300797660281830293/(5*10^29) by 4.29e-5, 378 at 9973230520053043026984980967643/(5*10^29) by 4.00e-4) and 5 above by about 1.8e-11 (327, 335, 342, 364, 372). think-1545 (another session) owns Couzo's extended-range rows; this bead holds the 02f9690 update for it: dated beyond_horizon_claims rows keyed (n, source_id) with dated supersession, as PR #479 did for 2d32a6e.

## Notes

2026-10-10: the description cites jlevy/squares#479 as the precedent for the row shape, not as a wait; nothing gates this bead.
blocked_on: none

2026-10-22 coord-intake-1021b: #715 (Couzo, 1285 rows; PR #717 imports the 109 new rows <= 1024) re-certifies some of this bead's earlier-commit certificates byte for byte. The #715 acknowledgement (issuecomment-6329883508) told the author those 64 rows will be recorded from their first commits; this bead records its share (#717 review A2). 30 sub-print re-certifications of 4e4c8ce are held on think-fwa9. The filtered two-route replay (couzo_715_replay) re-prices this bead's replay at about 40 CPU-minutes (triage-715 price.md).
blocked_on: jlevy/squares#717

2026-10-22 12:25Z coord-intake-1021b: #717 merged (and #720, #721). The rest of this import is the next records change after #719's (PR on claude/intake-2026-10-22, think-xyhn): it edits the same registers, and #719's ledger walks Couzo's 5a299b4 as a dated publication. A read-only re-plan against main 76496462b and #719's head is running (c-triage-1022b, scratchpad triage-1022b/).
blocked_on: think-xyhn

2026-10-22 c-triage-1022b (read-only re-plan against main 76496462b and #719's head
f9cee4736; coordinator scratchpad triage-1022b/: couzo-residue-plan.md, residue-rows.tsv).

**Reproduced exactly.** The report-order walk over all of Couzo's history
(tools/residue.py) finds the counts in this bead's title:

- 15 of `02f9690`'s 20 beyond-horizon certificates are below the rows that stood on 9
  October.
- 5 are above: 327, 335, 342, 364 and 372.
- 375 is below by 4.29e-5, and 378 by 4.0e-4.

**Disposition.**

- **12 become rows.** The `couzo-exact-certificates-2026-10-09` packet already retains
  all 12 byte for byte (verified by blob id).
  - **6 current:** 332, 336, 337, 341, 373 and 374. Each is below the 8 October decimal
    row by 4.5e-12 to 1.6e-11. Five of them are among the 32 rows #715's import reply
    left to this bead.
  - **6 history:**
    - 338, superseded by `3ef7634`;
    - 339, by `couzo-certificates-2026-10-11`;
    - 340, by `3ef7634`;
    - 377, by #686;
    - 378 and 379, by `f311f08`.
- **3 are held: 369, 375 and 376**, above Göbel's construction at their counts. They go
  to #613 (`think-8krd`). `main` already records superseded rows above Göbel at 375 and
  376, so the owner's answer there should say whether history rows above Göbel are kept.
- **Replay and closure.** The filtered replay of the 12 is about 1.5 CPU-min with controls.
  It lands in the one Couzo history records PR (couzo-residue-plan.md), after #719's PR.
  That PR closes this bead, and its reply on #715 covers this bead's share of the
  promise.

blocked_on: think-xyhn

2026-10-22 (c-lane-couzo-residue-1022): The records change is PR #730 (branch claude/intake-couzo-history-2026-10-22, lane c-lane-couzo-residue-1022), records commit a91c70907, 22 October 2026. The history walk (packing/campaign/issue-intake/upper-bounds-couzo-history-20261022) walks every count from 325 to 1024 from starts frozen at main a97b712b9. It covers every row source since then and every publication in a watched repository below the start. It reproduces the c-triage-1022b walk's recorded chain at every count. The one difference is that #715's 30 re-certifications are attributed to #715 rather than to 5a299b4, and they are held either way. 319 rows are recorded at assurance reported, 107 current and 212 superseded on entry; 236 existing rows are repointed. 340 publications are held back, each with its decision's bead (beyond_horizon_replay.HISTORY_HELD). The filtered two-route replay with six controls covers all 319 rows.

For this bead (02f9690): 12 rows of the source couzo-02f9690-2026-10-09, dated 2026-10-09 by the commit, retained in the couzo-exact-certificates-2026-10-09 packet: 6 current (332, 336, 337, 341, 373, 374) and 6 superseded on entry (338, 339, 340, 377, 378, 379). They supersede first the 8 October decimal rows (11) and 2d32a6e's (1). Held: 369, 375 and 376, above Göbel's construction (#613, think-8krd). The 3ef7634 updates at 338 and 340 are rows of couzo-3ef7634-2026-10-10 (both superseded). The franciscouzo read through 9bf90e7, which held these for think-1545, is removed; the read through 7b6c87e covers it. #715's restatements at 336, 337, 341, 373 and 374 now name these rows (result-requests.yaml). Filtered replay: 12 verified, 72 controls refused, 5.6 positive CPU s. The bead stays open until the PR merges; the coordinator closes it.

2026-10-22 20:45Z coord-intake-1021b: #730 (https://github.com/jlevy/squares/pull/730, branch claude/intake-couzo-history-2026-10-22): three tooling slices pushed on top of #722; 319 rows declared (107 current, 212 superseded), 340 held; filtered replay running; certificates (10.27 MB stored) stay in Git under OR-18. Also covers think-yfoo, think-tmwt, think-om5l.
