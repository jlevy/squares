---
type: is
id: is-01m5mp0zc3m66a3bqmdjpaq000
title: "Decide: does D6's 'no rows, except where an issue claims the count' write the 4e4c8ce deletion rows at 743 and 985?"
kind: task
status: open
priority: 2
version: 2
labels:
  - decision
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T15:28:13.698Z
updated_at: 2026-10-23T16:25:17.918Z
---
**The question.** The owner answered D6 on 23 October (think-f2io): a side obtained by deleting squares from a published certificate at a larger count is an earlier report in report order. The owner-answers branch (PR #754) applies it on think-f2io's recommended terms, "no rows, except where an issue claims the count": each such bound is recorded in the walk, a later equal or higher side is not recorded (#732's 985), and the index's scope covers it with no row. Does the exception stand, and if so whose row is it?

**Where it arises.** Two of Couzo's 4e4c8ce deletion bounds at or below 1024 are claimed by issues at the same side: 743 (27.798989873256, n744's certificate less one square; #715 claims it) and 985 (31.920310216821, n986's less one; #715 and #732 claim it). In the walks each is the earliest report of that side, so the issues' claims tie it and are not recorded.

**What the register shows now.** At 743 the chain is couzo-verified-bounds-2026-10-14's row, superseded by #719's current row, which is below the bound: nothing is stale. At 985 the current row is couzo-verified-bounds-2026-10-14's 31.920310217041 of 14 October, 2.2e-10 above the 4e4c8ce bound, which the walks record as the standing side and which has no row. This is the one count at or below 1024 where a deletion bound settled by D6 is the best side and the register's current row is above it.

**The answer either way.**
- No rows at all: 985's register row stays current while the walk's standing side is the bound; say so in the rule text.
- The exception stands: write couzo-index-2026-10-15 deletion rows at 743 (superseded on entry by #719's) and 985 (current, superseding the 14 October row), declared with the next count's certificate less one square (declared rows gain `deleted`), replayed on both routes (n744 and n986 are couzo-index rows read whole, so their controls stand), with the claims record, register and walks updated.

## Notes

2026-10-23 coord-intake-1023: from #754 review A1: the owner's D6 answer covers deleting one square from the next count's published certificate. Three 4e4c8ce bounds delete more: 751 (three squares from 754), 752 (two from 754) and 927 (two from 929). They stay held and are part of this question: do multi-square deletion bounds also count as earlier reports? Nothing rests on them today.
