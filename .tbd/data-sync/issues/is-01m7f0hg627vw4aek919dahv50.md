---
type: is
id: is-01m7f0hg627vw4aek919dahv50
title: "Göbel's construction omits L-border extensions of its own members: at 977 the Göbel square (15, 21) of 921 plus one L-border gives 17 + (21/2) sqrt 2, below devtools.goebel_construction's 17 + 11 sqrt 2 (#992)"
kind: task
status: open
priority: 3
version: 1
labels:
  - result-import
  - decision
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-11-15T07:07:58.018Z
updated_at: 2026-11-15T07:07:58.018Z
---
Found in the import of jlevy/squares#992 (lane L175, think-ud9e). `devtools.goebel_construction` takes Göbel's side at a count as the least member of the three Kingbird families at that count or above, deletion included. It applies no L-border. Friedman's survey DS7 (packing/resources/web/friedman-ds7-survey-2009-html.md, section 2) states, beside Göbel's family, that n + 2s(n) + 1 squares pack in side s(n) + 1 by an L around a packing of n, and builds 82 from Göbel's 65 that way.

**At 977.** `goebel_construction.side(977)` is 17 + 11 sqrt 2, about 32.556 (the Göbel square (16, 22) of 1028). The Göbel square (15, 21) packs 921 at 16 + (21/2) sqrt 2, and one L-border holds 2 floor(16 + (21/2) sqrt 2) + 1 = 61 more: 982 at 17 + (21/2) sqrt 2, about 31.849, lower by sqrt(2)/2. #992's author states this route himself. His own layout is the (16, 21) arrangement, outside the family's condition (a - 1 = 15 > (21/2) sqrt 2), with each corner staircase cut to depth 15: 441 + 4 x 134 = 977 at the same side, decided exactly in lane L175 (devtools.diamond_staircases, the lara-s977-upper-bound-2026-11-15 packet). It is not recorded: Couzo's #763 row at 977, 31.765989508190, is below it.

**Related holds.** Couzo's 23aff0c index states 27 L-border extensions of Göbel's squares, 981 and 982 among them at 31.849242404918, which the history walk holds as recipes under D2 and think-zkxy (`beyond_horizon_replay.HISTORY_HELD`); `devtools.construction_checker` refuses a classical parent.

**The question, the owner's.** #613's answer (think-8krd) named "Goebel's classical constructions", and the record reads it as the three families. Do L-border extensions of Göbel's members, one layer or more, join Göbel's construction? If yes, the module grows an L-border closure, proved final as now, and every count beyond 324 whose side falls is read again: a row above the new side is marked above-classical-construction, and walks read from that day start from the new side. If no, nothing changes, and the 27 held recipes stay with D2 and think-zkxy.

**Not measured.** How many counts from 325 the closure lowers, and whether any current row lies between the two sides. Measure with a tool before the owner is asked (OR-1); nothing in lane L175 measured it.
