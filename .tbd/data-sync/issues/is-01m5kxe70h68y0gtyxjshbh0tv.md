---
type: is
id: is-01m5kxe70h68y0gtyxjshbh0tv
title: "Decide: do Friedman's off-centre constructions count as earlier reports beyond 324, as Göbel's now do (#613 follow-up)?"
kind: task
status: open
priority: 3
version: 1
labels:
  - decision
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T08:18:33.105Z
updated_at: 2026-10-23T08:18:33.105Z
---
**The question.** The owner answered #613 on 23 October (think-8krd): Göbel's classical constructions are earlier reports beyond n = 324, so a rational row above Göbel's exact side at its count is not recorded. Do Erich Friedman's off-centre constructions count the same way?

**Where it arises.** Couzo's 23aff0c index (upper_bounds.json, pinned by digest in the couzo-issue670-2026-10-17 packet) states 61 constructions with no certificate file that the history walk holds (beyond_horizon_replay.HISTORY_HELD): 46 constructions (27 L-border extensions of Göbel's squares, 14 of Friedman's off-centre family, and bare Friedman constructions at 368, 543, 626, 752 and 849) and 15 bounds deleting one or two squares from Friedman's constructions at 368, 407, 448, 543, 590, 639, 752, 849, 908 and 969. #730's review named #613 (think-8krd) beside D2 and D6 (think-f2io) on both holds. Every one is below Göbel's construction at its count, so the Göbel answer leaves all 61 to D2 and D6; the Friedman part of the question was not asked.

**The answer either way.**
- No: the 61 wait on D2 (recipe rows through a maintained checker, answered yes) and D6 (deletion bounds, open) alone.
- Yes: Friedman's construction at each count joins the start as Göbel's does (devtools.intake_ledger's classical-constructions ruling would need the family, read exactly), so 23aff0c's bare Friedman constructions and the deletions from them restate earlier reports; only extensions below them could be rows under D2.
