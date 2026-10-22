---
type: is
id: is-01m4yr8jtj1znqhx7fva8g60bw
title: "Import Francisco Couzo: 4e4c8ce beyond-horizon index, 341 counts 325-1023 below 487b058 and #607 (no issue)"
kind: task
status: in_progress
priority: 2
version: 7
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
updated_at: 2026-10-22T06:48:14.501Z
started_at: 2026-10-22T02:18:23.107Z
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
