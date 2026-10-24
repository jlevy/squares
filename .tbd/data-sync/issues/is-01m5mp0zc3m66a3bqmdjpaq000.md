---
type: is
id: is-01m5mp0zc3m66a3bqmdjpaq000
title: "Decide: does a D6 deletion bound get a row (all 36, or where an issue claims the count: 743, 798, 855, 985), and are multi-square deletions (751, 752, 927) earlier reports?"
kind: task
status: open
priority: 2
version: 7
labels:
  - decision
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T15:28:13.698Z
updated_at: 2026-10-23T23:17:18.420Z
---
**The question.** The owner answered D6 on 23 October (think-f2io) by selecting the option labelled "Yes, an earlier report (Recommended)". The rest is the question the coordinator asked, not the owner's words: as coord-intake-1023 relayed it, the question was "a side obtained by deleting a square from a neighbour's certificate (e.g. Couzo's 985 from his 986)", and the selected option's description read "A published deletion bound counts like any stated bound; a later equal or higher side is not recorded". The owner-answers branch (PR #754) applies that: each such bound is recorded in the walk, and a later equal or higher side is not recorded (#732's 985). It gives the bound no row of its own, which is think-f2io's recommendation ("no rows, except where an issue claims the count"), not the owner's word. Three questions follow:
1. Does a one-square deletion bound get a row of its own, as a stated bound with a certificate has? The selected option's description, the coordinator's words, said it "counts like any stated bound".
2. If not, does the recommendation's exception stand where an issue claims the count, and if so, whose row is it?
3. Are bounds that delete two or three squares (751, 752, 927) earlier reports too?

**Where it arises.** Four of Couzo's 4e4c8ce one-square deletion bounds at or below 1024 are claimed by #715:
- 743 (27.798989873256, n744's certificate less one square) and 985 (31.920310216821, n986's less one), at the bound's own side. #732 also claims 985 at that side.
- 798 and 855, where #715's certificates are 2.88e-23 and 2.98e-23 below the bound at the same 12-place print, so they restate it (think-fwa9).
In the walks each bound is the earliest report of its side, so the issues' claims there are not recorded.

Three 4e4c8ce bounds delete more than one square (certified_bounds.json at 4e4c8ce): 751, three from 754's certificate; 752, two from 754's; and 927, two from 929's. #754 keeps them held on this bead. Each count's later steps are recorded below them, so nothing rests on them.

**What the register shows now.**
- 743: #719's current row is below the bound.
- 798 and 855: #732's current rows are below the bound.
- 985: the current row is couzo-verified-bounds-2026-10-14's 31.920310217041 of 14 October, 2.2e-10 above the bound. The walks record the bound as the standing side, and it has no row. This is the one count at or below 1024 where a settled deletion bound is the best side.
- At 11 more settled counts the current row is couzo-verified-bounds-2026-10-14's of 14 October, also above the bound: 533, 580, 589, 629, 638, 680, 733, 788, 845, 904 and 965. At each, 23aff0c's held side, a Friedman construction or a deletion from one, is lower still (D2, think-zkxy).

**The answer either way.**
- No rows at all: 985's register row stays current while the walk's standing side is the bound; say so in the rule text.
- Only where an issue claims the count: write couzo-index-2026-10-15 deletion rows at 743, 798, 855 and 985. The first three are superseded on entry by #719's and #732's; 985's is current and supersedes the 14 October row.
- A row for each of the 36 (the option description's "counts like any stated bound"): the same, and at the 11 counts above, each row supersedes the 14 October row until a row for 23aff0c's construction lands.
- Either way with rows: each is declared with the next count's certificate less one square (declared rows gain `deleted`) and replayed on both routes. n744 and n986 are couzo-index rows read whole, so their controls stand; each other row needs its next count's certificate read whole the same way (`deletion_problems`). The claims record, register and walks are updated.
- Multi-square bounds: "yes" settles 751, 752 and 927 the same way as the 36; "no" leaves them out of the walk, which reruns it (`held-dependents`).

## Notes

2026-10-23 coord-intake-1023: from #754 review A1: the owner's D6 answer covers deleting one square from the next count's published certificate. Three 4e4c8ce bounds delete more: 751 (three squares from 754), 752 (two from 754) and 927 (two from 929). They stay held and are part of this question: do multi-square deletion bounds also count as earlier reports? Nothing rests on them today.

2026-10-23 c-answers-1023 (PR https://github.com/jlevy/squares/pull/754, review A, A1): rewrote the description in the words coord-intake-1023 relayed (corrected by c-fix-754b-1023 below: only the selected label is the owner's). The earlier text said the owner answered that "a side obtained by deleting squares from a published certificate at a larger count" is an earlier report, which is broader than the question asked. Changes:
- The no-row reading is marked as the recommendation, and the description asks whether "counts like any stated bound" means a row.
- Added #715's 798 and 855, which restate the bound (think-fwa9), beside 743 and 985.
- Added the three multi-square bounds from the note above.
- Corrected the register facts. 985 is still the one count where a settled bound is the best side. At 11 more settled counts the 14 October row is above the bound, with 23aff0c's held side lower still.

In #754 the 36 one-square bounds are settled (`beyond_horizon_replay.DELETION_ANSWER`). 751, 752 and 927 stay held on this bead: in beyond_horizon_replay.HISTORY_HELD's second 4e4c8ce entry, and in test_deletions_of_two_or_three_squares_stay_held_for_the_owner. No verdict or row changes.

2026-10-23 c-fix-754b-1023 (PR https://github.com/jlevy/squares/pull/754, review B, "Not verified"). coord-intake-1023 confirmed that the owner answered D6 by selecting the option labelled "Yes, an earlier report (Recommended)" in a multiple-choice question; the question text and the option's description were the coordinator's, not the owner's. The description's first paragraph, question 1 and the "row for each of the 36" line now quote only the label as the owner's answer and attribute the rest to the question the coordinator asked. The questions themselves are unchanged. #754 corrects the repository the same way (commit 8775445cd; think-f2io's note).
