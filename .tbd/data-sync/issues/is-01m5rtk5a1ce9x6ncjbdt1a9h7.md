---
type: is
id: is-01m5rtk5a1ce9x6ncjbdt1a9h7
title: "Answer and close #811, the owner's tracker of exact side polynomials"
kind: task
status: open
priority: 3
version: 6
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: blocked
hold_until: null
created_at: 2026-10-25T06:05:01.633Z
updated_at: 2026-11-17T21:52:51.888Z
---
Owns the replies and the close of https://github.com/jlevy/squares/issues/811, the owner's tracker for exact side values (opened 2026-10-25T05:41:58Z, labels intake and tracker): the minimal polynomials of record sides and the exact forms built from them.

The issue lists seven items, each owned elsewhere: Evan Daniel's s(29) degree-7213 polynomial (#545, think-6gti; registered as T-246 on PR #812 (first numbered T-244 on branch n29-minpoly-1025)), Hyukdong Kim's exact minimal polynomials at n = 88, 126, 172, 199, 263 (#804, think-9vai), the draft PR stack #403 -> #435, the numeric sides at n = 29, 55, 71 (think-je8y, think-phh8, think-1blg), n = 83's degree-672 polynomial (think-chsu), the reported roots at 106, 152, 177 (#419, #420), and the algebraic house writer (think-ot5c).

The issue says "We will update this issue as each item lands on main." A follow-up is owed when T-246 reaches main. Close when every listed item has landed, been declined or moved to an issue of its own. packing/campaign/result-requests.yaml's entry for #811 names this bead as its answer bead and the owner of its queued ask.

## Notes

2026-10-31 (intake think-3guf, from #817's review A6): #811's s(29) row still shows the withdrawn 5.43e-20 figure; the record's value is 3.90143354777e-799 (S* and sigma below T-195's exact value). #811 is the owner's tracker: the pass does not edit its body; say it in #811's next follow-up, or the owner edits the row.
2026-10-31 (intake think-3guf, from #858's review A6): #816's own status table and log, a child of #811, still read as of 25 October (21:15Z): step 6 "Not written" (the review of 31 October is on main), step 3's price "about 717 CPU-hours" with no modular CPU-hours (now 6.6 / 436.8 exact on the round-2 host, register "about 440 to 720"; modular about 8.8 million CPU-hours), step 4 "The 11 rows outside the solved basis vanish at t*" (the receipt decides 16 rows off the basis, 6 divisible by an F_k and 10 identically zero, 11 of them used by touching constraints), and no 31 October log line. #816 is the owner's tracker: the pass does not edit its body. The follow-up of 31 October (issuecomment-6543105784) states the current status; the owner or the coordinator updates the table.

2026-11-17 w5-audit-1117r (think-uz0m, the stalled-bead audit of the 17 November intake pass, think-p02d; read against main f9ddfeeef): (c)/(d). #811 (the owner's tracker) closes when every item it lists has landed, been declined or moved. Landed: T-246 (#812, #817), Kim's polynomials (#804, think-9vai closed), the numeric side at 29 (think-je8y closed); #403 and #435 are closed. Not landed, and nobody is on them: n = 55 and n = 71 eliminations (think-phh8, think-1blg) and n = 83's root count (think-chsu), all untouched since 8 October, and the algebraic house writer (think-ot5c, claimed by c-houses-1023, silent since 31 October). Put to the owner: fund those four or move them out of #811 to issues of their own so it can close; the next follow-up also owes the s(29) row correction (3.90e-799, not 5.43e-20). Held on the four beads, so the sweep names the quiet one at the root.
blocked_on: think-phh8, think-1blg, think-chsu, think-ot5c
