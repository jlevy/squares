---
type: is
id: is-01m687bj11pzvr48e6pm14abna
title: "Review Polkovskyi's 23 October and #846 refinements (stage 4): adopt 130; owner's question on the other fourteen counts"
kind: task
status: in_progress
priority: 1
version: 5
delegate: bold-ritchie-l2
labels:
  - validation
  - regularization
dependencies: []
parent_id: is-01m685njhfc113wb8prbg15npb
hold: null
hold_until: null
created_at: 2026-10-31T05:36:40.481Z
updated_at: 2026-10-31T13:44:44.045Z
started_at: 2026-10-31T08:37:28.980Z
---
Stage 4 review of Mykhailo Polkovskyi's certificates of 23 October (T-252 on the lane's branch: 154, 155, 183, 211, 227, 236, 237, 241 and 271, each about 1.3e-19 to 1.7e-19 below its house) and of #846 (T-258: 105, 146, 156, 229 and 308, 1e-21 to 1e-41 below each house, and 130, a 2e-14 dilation of Couzo's #843 packing 2.08e-12 below it), and the adoption at each of the fifteen counts where it is the smallest validated side, crediting each packing to its finder and the refinement to Polkovskyi.

## Validation
- Claim: the fifteen exact headers of certificates/0000-0999/nN.cert at Mishapolk/square-packing-records 52aa267 (packets mishapolk-1023-refinements-2026-10-30 and mishapolk-issue846-2026-10-30); checkers: the two maintained exact routes (done, with sharp controls, whose contact margins at 1e-20 to 1e-40 are what the review should read) and a clean-room exact checker written by the reviewer.
- Run: a tbd-strong-max review sub-agent in its own worktree reading both packets as data, with the identity of each certificate against its house (measure/identity-nNNN.json); then the adoption at the fifteen counts with both strong generators (regularize_evand run; regularize_grid_slack at 0.5, 1 and 5 degrees), regularize_select and layer, the render step and the flip, in one pull request, or split by the runbook if the runs pass the cap.
- Cost: the review about 0.1 CPU-hours for fifteen certificates; the regularization 75 to 375 CPU-minutes (1.25 to 6.25 CPU-hours) for fifteen counts by the runbook's receipts; an estimate.
- Budget status: runnable, under the owner's standing 40 CPU-hour item cap.
- Possible subset under the cap: not needed.
- Depends on: a strong-tier review lane the coordinator launches; the owner may rule that sub-print re-certifications in the corpus are restatements (think-fwa9's answer was given for rows beyond 324), which would drop these entries instead.
- Done when: the review is mapped on both entries, check_results derives V3/C3, and each count is adopted and regularized with default_drawings --check-state --base-ref origin/main and flip_regularization --check passing.
- Machine note: the regularization runs are hours of CPU on a shared 4-core host; at most two cores, apart from a gate.

## Notes

2026-10-31: renumbered on the branch after #851's T-252: the 23 October refinements are T-253 and #846's are T-259 (were T-252 and T-258).

2026-10-31 (bold-ritchie-l2), the owner's question, recorded as a question and not a verdict. The stage 4 review (docs/project/reviews/review-2026-10-31-polkovskyi-846-and-23-oct.md, lane bold-ritchie-rv-polk, tbd-strong at xhigh) accepted all fifteen certificates for finite feasibility. At 130 (T-259, issue 846's re-solve of Couzo's #843 packing, 2.08e-12 below it, a different 12-place print) it is accepted for adoption, and the case adopts it on #852 with the packing's credit Couzo's (T-254).

At the other fourteen counts, 105, 146, 154, 155, 156, 183, 211, 227, 229, 236, 237, 241, 271 and 308, each certificate is a sub-print re-certification of the house certificate: below it by 1e-41 to 1.7e-19, the same 12-place print, the margin the house certificate's padding (RV-2). The owner's ruling of 23 October (think-fwa9) makes such re-certifications restatements, and the record applies it beyond the horizon only (intake_ledger.Ruling.applies; result-import.md's rulings paragraph); its words name no horizon. RV-1 (major) asks the owner:

QUESTION FOR THE OWNER: does the 23 October restatement ruling reach counts inside the corpus, n <= 324?
- (a) Yes: the fourteen are not recorded; T-253 and T-260 are withdrawn, T-259 keeps 130, no house moves, and the ledger's ruling gains a reach into the corpus. The review recommends (a).
- (b) No: record and adopt all fourteen, with both regularizations (75 to 375 CPU-minutes), and the runbook's refinement bullet gains the beyond-horizon limit.
- (c) Only a holder's own re-certifications: 105 and 156 (Polkovskyi's own houses) are not recorded; the other twelve wait on think-oqjd.

Record on #852: T-253 (the nine of 23 October) and T-260 (issue 846's five, split from T-259 so the question holds only them) stay at V0/C1, below the stage 4 exit, with the review mapped and their replay evidence not entered; nothing adopts them. #846's requests entry is blocked: owner-decision naming this bead. When the owner answers, the record follows: (a) withdraw both entries and add the ledger's ruling reach; (b) enter the replay evidence E-mishapolk-1023-exact-feasibility and E-mishapolk-846 at the five counts, raise both to V3/C3 and adopt with both regularizations; (c) split again by holder.

2026-10-31 coordinator: the think-ruu2 stage-4 review (tbd-strong-max) widens this owner question (its RV-3): project re-certifications of a house's own packing with padding trimmed (130: 2.50e-13, same print; 293: 8.98e-13 and 307: 3.75e-12, print changes) are the same operation as the 14 Polkovskyi counts. Options: (a) no new result at any margin (reviewer's recommendation), (b) only across the 12-place print, (c) any margin. The same contraction takes T-257's own 260 cert 2.0e-11 below its house across the print, so (b)/(c) open an unbounded series. 293 also raises RV-4: S+1 may already be #845's own report via its stated '260 + L' recipe. All three registered as recorded only, not adopted, pending this decision.
