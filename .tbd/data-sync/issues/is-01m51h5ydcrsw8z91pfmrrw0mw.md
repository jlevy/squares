---
type: is
id: is-01m51h5ydcrsw8z91pfmrrw0mw
title: Owner decisions pending from the 2026-10-15/16 intake passes (each blocks a reply or a record change)
kind: task
status: open
priority: 1
version: 5
labels: []
dependencies: []
parent_id: is-01m50gnwbxd5kxbynyx9nd162p
created_at: 2026-10-16T04:57:59.468Z
updated_at: 2026-10-16T07:52:06.142Z
---
Collected by the coordinator 2026-10-16 so another agent can pick them up. Each item names the bead that owns it; act only on the owner's word.
1. #574 (BuddenPing, 148 certificate refinements, a PR): merge it and adopt T-174? (think-9v2k). WARNING: adopting T-174 re-houses 35 counts (68, 84, 86, 88, 108, 126, 127, 130, 131, 132, 172, 181, 182, 199, 206, 208, 209, 210, 228, 238, 239, 240, 259, 266, 267, 268, 270, 273, 292, 297, 301, 305, 306, 307, 308); since #636 the gate will fail unless each is re-regularized or added to PENDING_ALLOWED with a bead (think-g3q7 documents the step). The #574 reply is held until the decision.
2. #570: does a printed side with no retained certificate get a beyond-horizon row (379)? (think-rfce). Reply held.
3. #557 and #565: replies reserved for the owner (drafts in think-sdsl, think-mxhc). #557 also carries a wrong n-18 label and 'n=18' title (its subject is n = 17); removing a label / editing a title is outside the github-workflows grant.
4. #624 (mstrmg, n = 366): not recorded because franciscouzo 4e4c8ce's index published a smaller 366 certificate first. If watched-repo publications should NOT count as earlier reports, #624 would be recorded (and its printed side differs from its certificate by 3.9e-7: ask the author which is meant). (think-hd6a)
5. #627 owner calls: decision 5 (T-189 kept S2), 9 (#607 dated by its issue, not first commit), 10 (T-188 recorded as a regularization of T-182 though seeded from T-175; T-190 of T-183 though close to T-189).
6. #575: reopen promise if the owner rules on 176 / the 'Certificate Committed Before' list (think-qag2).
7. Case labels: create n-59, n-76, n-95 (for #536, #594, #610) and n-19 (for #640)? None exist; no pass created them.
8. Holds: think-sk6b (publish hosted data release data/squarepacker-k2-minus-c-upper-certificates-v1), think-wu73 (complete replay4d replay, ~5,250 CPU-h here).
9. think-ckjc is done (#503 thank-you posted 14 Oct, recorded) but claimed by claude-code@vm; close it.
10. #532: the regularization PRs the replays waited on merged; may the T-142/T-143/T-144 replays start now (think-ux1v; tooling only on branch claude/wand125-confirmations-2026-10-11)?
11. think-abcm: check_requests lists owner-opened issues (#550, #554, #613) as owing an acknowledgement; decide the rule.

## Notes

2026-10-16 05:35Z (#641 review A12): 19 of the 20 PENDING_ALLOWED counts are among T-174's 68 counts (all but 154). If the owner adopts T-174 (#574), those counts get new witnesses and would need re-regularizing again; deciding #574 before running think-kpm3/think-3zi3 avoids doing those runs twice. 176 (think-la7h) is being done first regardless, because its live drawing is the raw house today.

12. (added 2026-10-16 ~06:55Z by user-eb, from the T-185..T-190 review, PR #648, finding RT-4): should T-161's 271 be listed as a regularization of SQUISH's T-151, as the pose measurement supports? Owner. Also for information: T-186 is below T-174 at all nine counts they share, so decision 1's hold decides none of those houses. 13. Site edition collision: #644 (lane I), #646 (codex/news-chooser-states) and #648 (review) each cut site v0.7.15; whichever merges second re-cuts. 14. Four final comments (#432, #470, #529, #584) are rendered and checked but unposted: the session's permission system refused GitHub comments/closes for the lane (think-klm7, think-jpre, think-s2i8, think-x333).

15. (user-eb ~07:10Z) PR #649 (lane E, think-ccjt) is red only on release impact: it needs a site patch cut (devtools.cut_release v0.7.15 --component site --impact patch; dry run clean), which this session's permission check refused for the lane as 'Production Deploy'. Not worked around. Since #644, #648 and #649 all need v0.7.15 (and #646 holds one too), the cut is a merge-time step for whichever merges after the first; the owner either allows the command for this session or makes the cut at merge.

16. (user-eb ~07:55Z, from the T-184/T-191 review, PR #652, F8) does a zm_mixed.py refusal at depth limit 12 meet stage 4's mutated-certificate rule (two mutated certificates refused by every checker that accepted the original)?
