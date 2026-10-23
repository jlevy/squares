---
type: is
id: is-01m5kxdfbwvzz2rx2m6r6eh8gh
title: "Decide: does the restatement ruling reach #719's 631, another holder's re-certification #722 recorded (think-fwa9 follow-up)?"
kind: task
status: open
priority: 2
version: 2
labels:
  - decision
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T08:18:08.892Z
updated_at: 2026-10-23T16:57:39.962Z
---
**The question.** The owner's answer of 23 October (think-fwa9) is that a side below an earlier report at its count by less than the 12-place print, with both rounding up to the same 12-place print, restates that report: the earlier report stays the row. Does it also reach a re-certification by another holder that an earlier ledger recorded?

**Where it arises.** One claim at or below 1024 is in the answer's words and not among the publications it was asked about: Mykhailo Polkovskyi's #719 at 631, 2.73e-13 below Francisco Couzo's 4e4c8ce certificate (and #715's re-certification of it, 2.57e-23 below that), all three rounding up to 25.656854249519. #722 recorded it (the #719 walk, campaign/issue-intake/upper-bounds-issue719-20261022), since #719 states its sides at 16 places and its row records 25.6568542495182812; the source's own answer on #719 calls such rows "precision continuous Newton/SQP quenches of the predecessor reported topologies". On main the row is superseded by #732's 25.656854249516 (mishapolk-issue732-2026-10-22), which is current and is not in the answer's words (3.43e-12 below 4e4c8ce, another print).

**What the walks do now.** The owner-answers branch (c-answers-1023) applies the restatement ruling in the history, #719 and #732 walks, and lists #719's 631 under the ruling's awaiting_owner in the history and #719 walks: it is walked by the rule before the ruling, recorded, so no row changes.

**The answer either way.**
- No (the ruling covers a holder's re-certification of an earlier report, the class it was asked about, and a refinement by another holder stays recorded as a regularization by the runbook's rule): drop nothing; the awaiting entries become a stated exception in the rule text.
- Yes: #719's 631 is not recorded; its superseded row goes, couzo-index-2026-10-15's row at 631 names #732's as its successor, mishapolk-issue719's claims record loses 631 (111 rows to 110), and the #732 walk's start at 631, frozen at main fcf2f96 as #719's row, needs a rule for a start row a later ruling takes out. No current row changes.

## Notes

2026-10-23 c-answers-1023 (PR https://github.com/jlevy/squares/pull/754, review A, A4): a second boundary of the restatement ruling, which no answer sets. The record now names it here as an open question:

- **Does a side within the print below Göbel's construction restate it?** `intake_ledger.restated` measures a claim against the least member of the standing side and refuses when that member is a construction. So a side below Göbel's construction by less than one unit in the 12th place, at the same 12-place print, would be recorded, not a restatement.
- **The two answers read together** (think-fwa9's restatements, think-8krd's "Goebel's classical constructions count as earlier reports beyond n = 324") could say the opposite: such a side restates an earlier report.
- **No such side exists to 1024.** In the history, #719 and #732 walks the closest side below Göbel's construction is #675's at 919, 1.0e-05 below it (measured from the three ledger.json files at #754's head).
- **Pinned by** `test_goebel_s_construction_is_an_earlier_report_beyond_the_horizon` (test_intake_ledger.py) and stated as open in result-import.md (Several Reports at One Count). An answer of "yes" changes `restated` and that test, and changes no verdict to 1024. It matters once think-llit raises the rulings' `through` past 1024; the retained Göbel program reaches 1073, and `goebel_form` refuses beyond.
