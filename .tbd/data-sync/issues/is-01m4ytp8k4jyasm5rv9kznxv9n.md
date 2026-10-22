---
type: is
id: is-01m4ytp8k4jyasm5rv9kznxv9n
title: Beyond-horizon rows above Göbel's classical constructions
kind: task
status: open
priority: 2
version: 4
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-15T03:46:28.067Z
updated_at: 2026-10-22T13:13:10.971Z
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
