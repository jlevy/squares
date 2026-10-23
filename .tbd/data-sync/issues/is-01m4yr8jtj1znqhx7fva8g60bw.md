---
type: is
id: is-01m4yr8jtj1znqhx7fva8g60bw
title: "Import Francisco Couzo: 4e4c8ce beyond-horizon index, 341 counts 325-1023 below 487b058 and #607 (no issue)"
kind: task
status: closed
priority: 2
version: 12
delegate: coord-intake-1021b
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
child_order_hints:
  - is-01m5h5w4d59h67ckp28qgzbere
hold: null
hold_until: null
created_at: 2026-10-15T03:04:02.641Z
updated_at: 2026-10-23T02:26:17.489Z
started_at: 2026-10-22T02:18:23.107Z
closed_at: 2026-10-23T02:26:17.488Z
close_reason: |
  2026-10-23 (c-lane-couzo-residue-1022): Done. #730 (https://github.com/jlevy/squares/pull/730) merged at 02:10Z on 23 October 2026 as fcf2f96a5, recording 4e4c8ce's 253 rows as couzo-index-2026-10-15 (91 current, 162 superseded on entry). The 89 held publications (47 above Göbel, 39 index deletion bounds, 3 sub-print) are owned by think-8krd, think-f2io and think-fwa9. #732's manifest reader (the N1 proposal in the c-triage-1022d note) is a #732 records-PR matter, not this bead's. No record on main names this bead as a deferral (check_bead_tree.deferrals). Replies: #715 https://github.com/jlevy/squares/issues/715#issuecomment-6355894334, #607 https://github.com/jlevy/squares/issues/607#issuecomment-6355894824, #624 https://github.com/jlevy/squares/issues/624#issuecomment-6355895083.
resolution: null
duplicate_of: null
---
Stage 1 triage, read-only, by the 15 October reads lane (think-mq0k), from the 02:30Z sweep at main 6964362b5. No issue reports any of it.

Source: franciscouzo/square-packing 4e4c8ce23cb5e87f033021687010992c40575480 ("Update all verified bounds for n < 1024", 2026-10-15T00:31:53Z), unchanged at the head 58a783368d4b7e70bb800f0009ea9ca03e578739 (01:25:11Z) apart from the index files and the Göbel bounds. 4e4c8ce writes certificates/best/ (515 finite witnesses, manifest.json with credits and two checkers' receipts, SHA256SUMS, README), certificates/ copies, upper_bounds.json and bound_sources.json for n = 1..1023; 58a7833 adds gobel_bounds.json, GOBEL_COMPARISON.md and gobel_comparison.csv (102 exact Göbel square and strip constructions over Q(sqrt 2), "no new discovery or optimality claim"), correcting 73 index entries to the closed forms.

Inside the corpus: one new claim, s(237), imported as think-7j8o; 211 is 487b058's (think-nj7h); the other 147 in-corpus certificates are other reports' (credited to them) or no smaller than the smallest earlier report.

Beyond the corpus (n = 325..1023), against the author's own 487b058 index (upper_bounds.json, verified lane) and #607's 43ac7d2 submissions only, not yet against the record's beyond_horizon_claims rows or the grid: 341 counts are smaller, 358 equal (333 of them grid), none larger. By the manifest's credit and category: about 280 Francisco Couzo (73 local search, 67 ct105 campaign, about 140 "derived exact" by deletion, L-borders or tiling), 45 derived exact from PingYou Ltd's pieces, 5 from Evan Daniel's, 8 "derived exact gluing" with Kevin Fang's rectangles (703, 757, 813, 931, 932, 992, 993, 994; the README says these differ from Fang's table rows), 19 elimination. Most margins are 4e-12 to 6e-12 (tightened rationalizations of 487b058's 1e-12-dilated witnesses); about twenty are material (2.9e-1 at 368, 2.1e-2, 9.4e-3, 7.5e-3, 4.5e-3, 3.7e-3 and smaller). Several hundred counts touch rows the record already tracks (think-a4wq, think-1545, think-nj7h, think-qik6, think-rn2y, think-7bw3).

Next: decide with think-nj7h whether one beyond-horizon import at 58a7833 replaces 487b058's (report order still dates each certificate by its first commit), retain a packet, compare against the record's beyond-horizon rows, and draft the ask on #607 or a new issue (S2 at most, so no tracking issue is required).

Price: the exact all-pairs replay of 341 certificates of 325 to 1023 squares is about 3 n(n-1) pair decisions each, near 5e8 in all, at 0.33 ms a decision on the #586 packet's measure: about 45 CPU-h, more where the derived certificates carry PingYou-size rationals, and the larger jobs exceed the kernel's 600 s job ceiling. Over the 40 CPU-h cap: HELD for a whole replay; a subset (the 20 material margins, or the Couzo-local ones) is a few CPU-h.

## Notes

2026-10-15 (Göbel review, think-8krd): of this bead's 341 rows, 47 are above Göbel's classical construction at their count (487b058's 42 counts and 331, 368, 407, 448, 491; nine by about 2e-23, exact enclosures of the closed forms). When this import drafts its register plan, mark those 47 `undecided-goebel` pending the owner. Table: packing/resources/web/couzo-verified-bounds-2026-10-14/review/goebel-beyond-horizon.json (set "4e4c8ce index, below 487b058 and #607"). The earlier count of 341 stands (the #607 comparison in this bead's triage keyed #607 by string; rerun with integer keys, nothing changes).

2026-10-16 coordinator (from #627's 616/A1 disposition): Couzo's 4e4c8ce index is smaller than all 238 rows T-188 records as current (3.79e-12 at 381 to 2.38e-02 at 749) and 7 of T-189's (339, 382, 450, 552, 599, 648, 757). Any comparison at these counts must declare the index's side (#627 owner decision 3). #624 (n = 366, mstrmg) is a later report at 366 that this import must list.

2026-10-16 coordinator (#627 review C, C1): at #607's 15 counts the index's own certificates beat 7 rows; its upper_bounds.json also gives a deletion bound at 542 (from its 543 certificate, 7.461e-14 below #607's row) that the manifest records as a tie. This import must decide whether the index's deletion bounds become rows, and then restate T-189's notes, the #607 source note and the packet README count (7 or 8).

2026-10-22 coord-intake-1021b: #715 (Couzo, 1285 rows; PR #717 imports the 109 new rows <= 1024) re-certifies some of this bead's earlier-commit certificates byte for byte. The #715 acknowledgement (issuecomment-6329883508) told the author those 64 rows will be recorded from their first commits; this bead records its share (#717 review A2). 30 sub-print re-certifications of 4e4c8ce are held on think-fwa9. The filtered two-route replay (couzo_715_replay) re-prices this bead's replay at about 40 CPU-minutes (triage-715 price.md).
blocked_on: jlevy/squares#717

2026-10-22 12:25Z coord-intake-1021b: #717 merged (and #720, #721). The rest of this import is the next records change after #719's (PR on claude/intake-2026-10-22, think-xyhn): it edits the same registers, and #719's ledger walks Couzo's 5a299b4 as a dated publication. A read-only re-plan against main 76496462b and #719's head is running (c-triage-1022b, scratchpad triage-1022b/).
blocked_on: think-xyhn

2026-10-22 c-triage-1022b (read-only re-plan against main 76496462b and #719's head
f9cee4736; coordinator scratchpad triage-1022b/: couzo-residue-plan.md, residue-rows.tsv,
residue-held.tsv).

**The walk.**

- `tools/residue.py` walks every count from 325 to 1024 in report order from the grid.
- The events are all 950 rows on #719's head and every certificate and index bound in the
  Couzo, Daniel, Fang and de Winter histories, compared exactly.
- It finds `4e4c8ce` below the standing side at 342 counts. This bead counted 341. The 47
  above Göbel are exactly `think-8krd`'s 47.

**Disposition by report order.**

- **253 certificate rows.**
  - **91 current:**
    - 36 at counts where `main` holds only the grid, 0.177 to 0.464 below it: 325, 326,
      329, 333, 334, 362, 363, 366, 367, 371, 401, 402, 405, 442, 443, 446, 485, 486, 530,
      531, 577, 578, 626, 627, 677, 678, 730, 731, 785, 786, 842, 843, 901, 902, 962 and
      963;
    - 55 below `487b058`'s rows, 13 of them by 1e-10 to 1.04e-9 and 42 by 4e-12 to
      1e-10.
  - **162 history**, superseded by #670 (55), #719 (38), #715 (20), #686 (16), `5a299b4`
    (10), #678 (9), #672 (5), #675 (4), `23aff0c` (4) and #666 (1).
  - **The 26 rows #715's import reply left to this bead:** 24 are among these, 6 current
    (850, 862, 914, 976, 986, 988) and 18 history under #719. 743 and 985 are index
    deletion bounds.
- **Held:**
  - 47 above Göbel (`think-8krd`);
  - 39 index deletion bounds with no file at their count. This is this bead's #627 C1
    question, proposed as D6 on `think-f2io`. Recommended: no rows (the claim table's
    monotonicity line), except 743 and 985, which #715 claimed (the #675 precedent).
  - 3 sub-prints, 327, 332 and 542 (`think-fwa9`);
  - `58a7833`'s 49 index entries, Göbel's own closed forms as rational enclosures (#613).

**In the corpus.** Nothing new.

- 18 of `4e4c8ce`'s certificates are below today's case lanes: 70, 88, 102, 106, 123, 126,
  152, 153, 177, 199, 207, 258, 259, 266, 267, 292, 295 and 301.
- Each is at or above an exact side the register already states (T-174's algebraic
  supplement and the like). For example, 207 is 3.6e-31 above
  14.880960371555579594696691574923….

**The packet.**

- New: `couzo-index-2026-10-15` at `4e4c8ce`. Its 253 certificates are 42.7 MB in a
  checkout, about 8 MB as Git packs them. The Göbel files are pinned by digest.
- Retention is owner decision O5: all of them, or the 91 current ones (17.2 MB, about
  2 MB packed) with digests for the rest.
- The replay by the filtered two-route decision is about 60 CPU-min with controls. That
  re-prices this bead's 45 CPU-hour all-pairs figure.

**Closure.** The one Couzo history records PR closes this bead, after #719's PR; its
reply on #715 keeps this bead's share of the promise. The held items move to
`think-8krd`, `think-fwa9` and D6 before it closes.

blocked_on: think-xyhn

2026-10-22 (c-lane-couzo-residue-1022): The records change is PR #730 (branch claude/intake-couzo-history-2026-10-22, lane c-lane-couzo-residue-1022), records commit a91c70907, 22 October 2026. The history walk (packing/campaign/issue-intake/upper-bounds-couzo-history-20261022) walks every count from 325 to 1024 from starts frozen at main a97b712b9. It covers every row source since then and every publication in a watched repository below the start. It reproduces the c-triage-1022b walk's recorded chain at every count. The one difference is that #715's 30 re-certifications are attributed to #715 rather than to 5a299b4, and they are held either way. 319 rows are recorded at assurance reported, 107 current and 212 superseded on entry; 236 existing rows are repointed. 340 publications are held back, each with its decision's bead (beyond_horizon_replay.HISTORY_HELD). The filtered two-route replay with six controls covers all 319 rows.

For this bead (4e4c8ce/58a7833): 253 rows of the new source couzo-index-2026-10-15, dated 2026-10-15T00:31:53Z by the commit, retained in the new couzo-index-2026-10-15 packet (253 certificates; manifest, indexes, 47 Göbel-held and 2 sub-print files pinned by digest): 91 current and 162 superseded on entry (by #670 55, #719 38, #715 20, #686 16, 5a299b4 10, #678 9, #672 5, #675 4, 23aff0c 4, #666 1). They supersede first 487b058's rows at 199 counts (64 of them current until then) and #607's at 7; at 41 counts no row stood before them. Held at 89 counts: 47 above Göbel (think-8krd), 39 index deletion bounds (proposed D6, think-f2io; 743 and 985, which #715 restates, among them) and 3 sub-print re-certifications (327, 332, 542; think-fwa9). 58a7833's Göbel bounds stay with #613: its read in intake-watch.yaml now names think-8krd. #715's restatements of 24 of these certificates now name the rows. Filtered replay: 253 verified, 1,518 controls refused, 333.2 positive CPU s; the all-pairs kernel at 366 and 703 (313,548 pairs, 117.7 CPU s) agreed exactly. Custody is Git (OR-18). The bead stays open until the PR merges; the coordinator closes it.

2026-10-22 c-triage-1022d (read-only).

- #732's recorded rows supersede 14 of the current rows #730 plans, all Couzo's `4e4c8ce`:
  411, 451, 494, 495, 539, 540, 587, 854, 856, 857, 913, 915, 916 and 977.
- They tie #730's planned deletion row at 985.
- At 369 and 376, they are above `58a7833`'s held recipe bounds by 3.5e-31 and 2.3e-30.
- #732's records PR should land after #730.

## Proposed New Beads

None is needed if the coordinator folds the tool slice into `think-0gp6`. Should it be
split out:

- **N1 (task, P2, child of `think-0gp6`): "beyond_horizon_replay: a release whose rows
  come from a pinned manifest (#732)".**
  - #732's body has no row table. Its 5,468 rows are in `certificates/manifest.json` at
    the pin.
  - Add a reader of the packet's retained manifest (`UP` at 12 places), or extend #730's
    declared-rows path to an issue's release.
  - Tests: the reader refuses a manifest row whose path, digest or side disagrees with the
    derived fact.
  - Seconds of CPU.
  - Blocked on #730.
