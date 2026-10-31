---
type: is
id: is-01m69gm3pppqh2b22d2g3t3h91
title: "Result status: does a defect-found read stay open after a review that ends defects-resolved? (T-261 reads incomplete; owner question)"
kind: task
status: open
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-10-31T17:37:52.341Z
updated_at: 2026-10-31T18:43:09.428Z
---
Owner question on the result-status vocabulary (plan-2026-10-01-result-status, provisional), raised by review A of #861 (A4, https://github.com/jlevy/squares/pull/861#pullrequestreview-5724017016).

**The case.** T-261 (#545's grade-C local minima, registered by #861; T-264 on the branch before review A) is at V3/C1. Its report entry E-evand-gradec-local-minima-233-report carries `external_review.state: defect-found` from the 23 October review (C-1, a gap in grade-C.md's paper proof at side-end rows, which that review repaired with gradec.py's checks unchanged), and its register entry lists that review with verdict `defects-resolved`. `devtools.result_status.open_issues` rule 1 fires on any defect-found read while the result stands below C2, and does not read the review's verdict, so the results page shows T-261 as *incomplete*, beside T-007 (whose read has no review). T-261 is the only incomplete entry whose latest review ends `defects-resolved`.

**Why the status is wrong one way or the other.** C-1 is a proof gap, not a computation: think-mtah's replay of gradec.py over all 233 would raise T-261 to C3 and flip it to *confirmed* mechanically, without touching C-1. T-261's own next_rung says the author's adoption of the repaired step in grade-C.md closes C-1 at the source.

**Options (the owner's choice; no rule is changed until answered):**
1. **The record's repair counts.** A defect-found read is dispositioned by a later review of the same result that ends `defects-resolved` (or `accepted`), as rule 1 already lets a passing replay do. T-261 would read *reviewed* now; T-007 is unaffected.
2. **Only the source's adoption counts.** A defect-found read stays open until the source adopts the repair (or a later read of the source finds it fixed), whatever the rung. Then think-mtah's replay must not clear T-261's *incomplete*: rule 1 stops being rung-gated for defects a review repaired rather than a replay passed over, and the defect needs a recorded close (for example `external_review.state` moving on to a resolved state with its date and source).

## Validation
- Claim: result_status's rule 1 gives the status the owner chooses for a defect-found read whose latest review ends defects-resolved.
- Run: the owner's answer; then `devtools/result_status.py` rule 1 and its tests (tests/test_result_status.py, tests/test_site_result_filters.py's incomplete list), and epistemics.md's Status section.
- Cost: under an hour of agent time after the answer; no compute.
- Budget status: gated on decision (owner).
- Depends on: the owner's answer.
- Done when: rule 1 and epistemics.md say which of the two holds, and T-261's status follows it.

## Notes

2026-10-31 bold-ritchie-l8, from review A of #864 (A2, no change made): the #545 reply of 31 October (https://github.com/jlevy/squares/issues/545#issuecomment-6547240858) says "The replay would clear the label by moving T-261 to C3, not by settling the gap", true under today's rule 1, and the next bullet says the label will follow this bead's answer. **If the owner picks option 2** (the replay must not clear T-261's *incomplete*), T-261's status stops moving with C3, and the #545 follow-up that change owes must say that the replay no longer clears the label.
