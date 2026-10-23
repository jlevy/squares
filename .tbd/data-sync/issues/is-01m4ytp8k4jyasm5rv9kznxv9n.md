---
type: is
id: is-01m4ytp8k4jyasm5rv9kznxv9n
title: Beyond-horizon rows above Göbel's classical constructions
kind: task
status: in_progress
priority: 2
version: 9
delegate: c-answers-1023
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-15T03:46:28.067Z
updated_at: 2026-10-23T09:40:47.065Z
started_at: 2026-10-23T07:54:25.898Z
---
**Owner question:** do Frits Göbel's classical constructions count as earlier reports, and so as the baseline beyond n = 324, so that a beyond-horizon row above one is not recorded? The record holds no Göbel construction beyond the corpus; its standing side there is the beyond-horizon row or the grid. Until the owner answers, draft register plans mark the affected rows `undecided-goebel` rather than recorded.

Method and tables: packing/resources/web/couzo-verified-bounds-2026-10-14/review/goebel-beyond-horizon.md, with goebel-beyond-horizon.json (every row) and goebel_beyond_horizon.py, on branch claude/wizardly-meitner-wqn4x3-reads-1015 (reads lane, 2026-10-15).

**How Göbel's side is computed (exact).** The three closed-form families the Kingbird catalogue states, archived as [Kingbird-Göbel-squares] (packing/resources/web/kingbird-squares-in-squares-gobel-squares.md) and [Kingbird-Göbel-strips] (kingbird-squares-in-squares-gobel-strips.md), both archived 2026-09-07, generalizing [Göbel 1979]:
- Göbel square: n = 2(a+1)a + b², side a + 1 + (b/2)√2, for positive integers with a − 1 < (b/2)√2 < a + 1;
- Göbel strip: n = (a+1)a + 2 + b, side a + 1 + √2/2, b = 1 + ⌊(a−1)√2⌋;
- corner-touching strip: n = (a+1)a + 3 + b, side 2 + (b+1)√2/2, the same b, from s(18) on.
Göbel's side at m is the least member side at any count ≥ m (deletion). Sides are held as p + q√2 with p, q rational and compared with a rational side by exact sign; no row can equal one. Cross-check: the author's 58a7833 gobel_bounds.json (an exact ℚ(√2) check of each construction it uses, up to 975) gives the same least closed form at all 661 table rows it reaches.

**Results (counts above Göbel; margins exact, printed from √2 to 60 places):**
- franciscouzo@487b058 (think-nj7h), 296 rows: 42 above, 254 below. Above at 408, 415, 416, 445, 449, 488, 489, 492, 493, 537, 538, 585, 586, 634-636, 685-688, 738-740, 793-795, 851-853, 860, 861, 910-912, 919-921, 964, 971-974, by 2.8e-11 to 5.7e-10: rational witnesses of Göbel packings (dilated about 1e-12). Below by 2.9e-3 to 0.83.
- #607 at 43ac7d2 (think-qik6), 22 rows beyond 324 (339, 342, 382, 409, 419, 450, 461, 542, 552, 599, 648, 649, 651, 757, 804 and the seven Fang composites 703, 812, 930, 931, 992, 993, 994): none above; below by 3.2e-2 to 0.65.
- the 4e4c8ce index's 341 rows below 487b058 and #607 (think-yfoo): 47 above, 294 below. Above at 487b058's 42 counts and at 331, 368, 407, 448 and 491, by 1.9e-23 (PingYou-derived exact enclosures of Göbel's closed forms at 331, 407, 448, 491 and Couzo's at 408, 415, 449, 492, 537) to 5.6e-10.
- the record's current beyond-horizon rows on main 6964362b5 (40 rows): 2 above: 369, couzo-extended-range-reports-2026-10-08 at its print 19.740417287556077, 3.33e-2 above the Göbel strip 19 + √2/2; 376, couzo-certificates-2026-10-13 (4596670's certificate) 19.904068025746006, 4.57e-3 above the Göbel square 10 + 7√2. 38 below by 1.7e-2 to 0.65.

**Draft plans.** couzo-verified-bounds-2026-10-14's register-plan.yaml now lists 252 rows to add and 42 `undecided-goebel`; its comparison marks the 42 `undecided-goebel` and its claims record leaves them out. think-yfoo's plan (not yet drafted) should mark its 47 the same way. #607's rows are unaffected. If the owner says Göbel counts, the record's own rows at 369 and 376 would need a Göbel row (or the grid) beside them, which is a records question too.

## Notes

2026-10-15: committed as 8cf42e177da4530f2d95c505854d48f304682782 on claude/wizardly-meitner-wqn4x3-reads-1015 (pushed; no PR), through the hooks. packing-validate --records exit 0; focused tests 319 passed (test_upper_bound_reports_487b058 holds the four set tallies and the undecided-goebel rule).

2026-10-15T04:00Z, coordinator: tracked on GitHub as https://github.com/jlevy/squares/issues/613 (labelled bug; owner decision on Göbel as the beyond-horizon baseline; registered rows 369 and 376 above Göbel by 3.33e-2 and 4.57e-3).

2026-10-22 c-triage-1022b (read-only; coordinator scratchpad triage-1022b/residue-held.tsv).

**Göbel-above publications at 325 to 1024.** The retained `goebel_beyond_horizon.py`
decided each exactly, in the report-order walk of Couzo's whole history. The Couzo history
records PR would hold 101 of them for #613:

- **`4e4c8ce`: 47.** These are exactly this bead's 47. 45 would be current rows; 860 and
  919 would be superseded.
- **`58a7833`: 49.** These are index entries that are Göbel's own closed forms as rational
  upper enclosures. At 369 and 376 they are below `main`'s current rows, so recording them
  is the correction #613 describes.
- **`02f9690`:** 369, 375 and 376.
- **`f311f08`:** 376.
- **`5a299b4`:** 331.

`487b058`'s 44 are unchanged.

**A question for the owner's answer.** `main` already records superseded rows above
Göbel's side at 375 (the 8 October, `2d32a6e`, 11 and 12 October rows) and at 376 (8, 11,
12 and 13 October). Should held history rows above Göbel be recorded likewise, or should
those rows be marked?

2026-10-23 (c-lane-couzo-residue-1022, review A of #730, A1 and A2): two additions to #613's question.

**23aff0c's 61 classical constructions now wait on #613 too.** The #730 history walk holds 23aff0c's 46 D2 constructions and 15 proposed-D6 deletion bounds (think-f2io). All 61 are classical constructions that `upper_bounds.json` states with no certificate file:
- Göbel's squares: 27.
- Friedman's off-centre family: 19. 41 of the 46 constructions are L-border extensions, and 368, 543, 626, 752 and 849 are bare Friedman.
- 15 deletions of one or two squares from Friedman's constructions.

Whether a classical construction counts as an earlier report is #613's question, so `HISTORY_HELD` names think-8krd beside think-f2io on both holds. A "yes" to D2 or D6 alone would credit the 23aff0c commit with Göbel's and Friedman's constructions, with no certificate file to replay.

**An answer that leaves a hold out reruns the walk.** 66 history verdicts rest only on Göbel holds (`HISTORY_RESTING`). A rerun without the Göbel holds would record each of those steps, but every one of them is itself above Göbel's construction, so this decision holds it again (`refusal_flips`). If 23aff0c's classical constructions are left out under #613, the D2/D6 consequences recorded on think-f2io apply: 56 new records, which need a rerun of the history walk and new rows.

2026-10-23 coord-intake-1023: OWNER DECISION (in conversation, 23 October): YES, Goebel's classical constructions count as earlier reports beyond n = 324 (the baseline): a rational row above Goebel's exact side is not recorded. Applies below 1024 (331, 369, 376 holds) and above (467 publications per the think-llit triage). Implementation: the walks' Goebel holds become 'not recorded' verdicts; rerun with think-temp's sub-print change after #742.

2026-10-23 c-addr-742-1023 (PR #742 review A, A6): in the #732 walk, leaving the
publications above Göbel's construction out decides 17 of the author's 1851c2c files (416,
445, 488, 489, 493, 538, 585, 586, 634, 635, 636, 686, 687, 688, 739, 740, 795) and #732's
331, 369 and 376 again, and each is itself above Göbel's construction, so the same answer
holds it in turn (refusal_flips marks them goebel, not new records). Packet README, Held Back
and Not Recorded.

2026-10-23 c-answers-1023 (PR https://github.com/jlevy/squares/pull/754, branch claude/intake-2026-10-23-owner-answers).

**Done.** Göbel's construction is an earlier report in the history, #719 and #732 walks,
through 1024 (`devtools.intake_ledger` ruling `classical-constructions`): at each count
beyond 324 the least side of the three Kingbird families at that count or by deletion, as
the 15 October packet's retained program computes it, joins the start as a rigorous
90-digit enclosure, so a side at or above it is not recorded. The GOEBEL_ABOVE hold class
is gone. Rerun: every Göbel hold became `not recorded` against Göbel's construction
(history: 02f9690 at 369, 375, 376; 49907ec 964; f311f08 376; a7067d7 and 93570ef 375;
487b058's 44; 4e4c8ce's 47; 58a7833's 49; 5a299b4 331; #732 walk likewise, #732's own 331,
369 and 376 among them). The rerun also takes out of the record four steps that were
recorded and never held, all rows of 11 to 13 October: couzo-certificates-2026-10-11 and
-12 at 375 and 376, and couzo-certificates-2026-10-13 at 376.

**Rows on main above Göbel (today's main c1115c095), marked by a new register
disposition.** `above-classical-construction` with `construction: p + q*sqrt(2)`
(check_source_coverage holds it above exactly and not current; the schema admits it;
beyond_horizon_replay.construction_problems holds every row from 325 to 1024 to Göbel's
construction). Nine rows: 369 couzo-extended-range-reports-2026-10-08 (was current,
19.740417287556077, 3.33e-2 above 19 + sqrt(2)/2); 375 the 8 October report and update and
the 11 and 12 October certificates (superseded rows, above 10 + 7 sqrt(2) less one square);
376 the 8 October report and the 11, 12 and 13 October certificates (the 13 October row,
19.904068025747, was current, 4.57e-3 above 10 + 7 sqrt(2)). **Current rows change at 369
and 376: neither count has a current row now; the standing side there is Göbel's
construction.** At 375 the 13 October row (below Göbel) still leads to Evan Daniel's
current row.

**Not done here.** 23aff0c's 61 holds (D2/D6) named think-8krd as a further decision; all
61 are below Göbel's construction, so they now name think-zkxy instead (whether Friedman's
off-centre constructions count as Göbel's do; opened under think-ezt8). The counts above
1024 are think-llit's: the retained Göbel program stops at 1100.

**Do not close this bead before #613 is closed**: #613's requests entry names think-8krd as
its answer_bead, a live deferral (check_bead_tree); the entry's ask is now `done` and its
close_when holds once the PR merges. The coordinator closes #613 (the project's own issue;
no acknowledgement owed) and then this bead.

**Follow-up drafted** for #732 on think-temp; #613 needs only the closing.
