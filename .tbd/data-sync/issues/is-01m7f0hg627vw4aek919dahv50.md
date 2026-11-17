---
type: is
id: is-01m7f0hg627vw4aek919dahv50
title: "Decide: do L-border extensions of Göbel's members join Göbel's construction beyond 324 (#613 follow-up, beside think-zkxy)? Four current rows (534, 581, 741, 796) lie within 6.2e-11 above a bordered side (#992 review F11)"
kind: task
status: open
priority: 3
version: 3
labels:
  - result-import
  - decision
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-11-15T07:07:58.018Z
updated_at: 2026-11-15T08:23:04.964Z
---
Found in the import of jlevy/squares#992 (lane L175, think-ud9e). `devtools.goebel_construction` takes Göbel's side at a count as the least member of the three Kingbird families at that count or above, deletion included. It applies no L-border. Friedman's survey DS7 (packing/resources/web/friedman-ds7-survey-2009-html.md, section 2) states, beside Göbel's family, that n + 2s(n) + 1 squares pack in side s(n) + 1 by an L around a packing of n, and builds 82 from Göbel's 65 that way.

**At 977.** `goebel_construction.side(977)` is 17 + 11 sqrt 2, about 32.556 (the Göbel square (16, 22) of 1028). The Göbel square (15, 21) packs 921 at 16 + (21/2) sqrt 2, and one L-border holds 2 floor(16 + (21/2) sqrt 2) + 1 = 61 more: 982 at 17 + (21/2) sqrt 2, about 31.849, lower by sqrt(2)/2. #992's author states this route himself. His own layout is the (16, 21) arrangement, outside the family's condition (a - 1 = 15 > (21/2) sqrt 2), with each corner staircase cut to depth 15: 441 + 4 x 134 = 977 at the same side, decided exactly in lane L175 (devtools.diamond_staircases, the lara-s977-upper-bound-2026-11-15 packet). It is not recorded: Couzo's #763 row at 977, 31.765989508190, is below it.

**Related holds.** Couzo's 23aff0c index states 27 L-border extensions of Göbel's squares, 981 and 982 among them at 31.849242404918, which the history walk holds as recipes under D2 and think-zkxy (`beyond_horizon_replay.HISTORY_HELD`); `devtools.construction_checker` refuses a classical parent.

**The question, the owner's.** #613's answer (think-8krd) named "Goebel's classical constructions", and the record reads it as the three families. Do L-border extensions of Göbel's members, one layer or more, join Göbel's construction? If yes, the module grows an L-border closure, proved final as now, and every count beyond 324 whose side falls is read again: a row above the new side is marked above-classical-construction, and walks read from that day start from the new side. If no, nothing changes, and the 27 held recipes stay with D2 and think-zkxy.

**Measured once** by the #992 review's program (F11, docs/project/reviews/review-2026-11-15-lara-992.md): with 0 to 3 L-borders, bordered members undercut the module's side at 910 of the 1,676 counts from 325 to 2000, and four current rows (534, 581, 741, 796, couzo-index-2026-10-15) lie within 6.2e-11 above a bordered side, so a yes would mark them above a classical construction. Measure again with a maintained tool before the owner is asked (OR-1).

**Neither answer releases the 27 held recipes by itself.** A no leaves them with D2 and think-zkxy, and `devtools.construction_checker` refuses a classical parent either way.

**Beside think-zkxy, not a duplicate.** think-zkxy asks about Friedman's off-centre family; it lists the 27 L-border extensions of Göbel squares under where the question arises, but its question does not cover them. Put the two to the owner as one two-part question.

## Notes

2026-11-15 L175 (bold-ritchie-l175): the blind stage 4 review of #992 (lane L174, think-u58c; docs/project/reviews/review-2026-11-15-lara-992.md, F11) measured what this bead says was not measured, with its own retained program (packing/resources/web/lara-s977-992-review-2026-11-15/programs/l174_border_audit.py, out/border-audit.json): zero to three L-borders on every member undercut devtools.goebel_construction's side at 910 of the 1,676 counts from 325 to 2000, 975 to 982 among them (17 + 21/sqrt 2 against 2 + 43 sqrt(2)/2 at 975 and 17 + 11 sqrt 2 at 976 to 982). 28 rows of source-coverage.yaml lie at or above a bordered side and below the module's: 24 superseded, among them Couzo's 981 and 982 of 14 and 15 October, and four current, couzo-index-2026-10-15 at 534, 581, 741 and 796, each within 6.2e-11 above a bordered Göbel side. A yes here would mark those four above a classical construction. The audit is a review program, not a maintained tool: measure again with one before the owner is asked (OR-1).
