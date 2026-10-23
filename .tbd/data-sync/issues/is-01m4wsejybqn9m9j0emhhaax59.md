---
type: is
id: is-01m4wsejybqn9m9j0emhhaax59
title: Review the draft significance scores of T-154, T-155 and T-156
kind: task
status: in_progress
priority: 3
version: 4
delegate: c-signif-1023
labels:
  - packing
  - result-import
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-14T08:46:19.082Z
updated_at: 2026-10-23T08:21:37.601Z
started_at: 2026-10-23T06:43:58.413Z
---
PR #563's significance review (docs/project/reviews/review-2026-10-11-significance-scores.md) confirmed every draft score of T-001 to T-146; T-147 to T-156 were registered after it. Three remain drafts on main: T-154 (S5, 'draft for the owner', a second route to T-153's s(17) value, which the record holds at V0), T-155 (S1, exact regularized sides of credited packings, the registering lane's draft) and T-156 (S1, derived from T-155). Review B of #563 (B4) found T-155 and T-156 against that review's reading: S1 'is for an entry that establishes nothing the record did not hold', and its proposed working-rules paragraph scores a regularization or exact closed form of a credited packing S2 (T-011, T-065, T-088, T-098, T-101, T-117, T-137, T-146). Review A (A3): the paragraph's second-route rule, now qualified 'at V3 or above', would otherwise have moved T-154 from S5 to S2. Settle T-155 and T-156 against T-098, T-117 and T-146, and T-154 against T-054 and T-055, by an independent reviewing lane; set significance.by to the review. Context: #543 (Policy paragraph), #563 reviews A and B.

## Notes

2026-10-15, evening intake pass (think-wnsv), lane D (think-ykg6): the sweep read "did not hold", in the description's quotation of review B, as a wait on #563 (merged 2026-10-14T10:46Z). This bead waits on nothing. T-154 (S5, "draft for the owner"), T-155 and T-156 (S1, "the registering lane's draft") are still drafts in results.yaml on the base of #616, so the independent reviewing lane can run now.

blocked_on: none

2026-10-23, intake pass (coordinator coord-intake-1023), lane c-signif-1023, branch claude/intake-2026-10-23-significance-review: the independent review. All three scores kept; each significance block now states its comparison, scored 2026-10-23, and by names this review.
- T-154: S5 confirmed by the review. Scored as its claim: it settles n = 17, a central open case, as T-153 (S5, V0) and T-194 (S5) do. The second-route rule (S2, T-054 and T-055) covers values held at V3 or above (#563 review A, A3), and the record holds s(17) = L only as T-153's V0 candidate. Owner's confirmation, which the registration proposed, is outstanding and recorded so in rationale and by.
- T-155: S1 confirmed. selection.json recounted: 33 counts at exactly T-101's side (bound already proved), 25 at 6.6e-20 to 1.8e-19 below it, n = 29 at 5.4e-20 below T-009's endpoint; no printed verified value changes. Against T-098, T-117, T-146 (S2): those lower best known sides at the printed precision (up to 5.0e-11, 4.3e-11, 7.82e-10); T-011, T-065, T-101 (S2) are first exact certificates. Six reviewed entries since 14 October (T-166, T-170, T-171, T-174, T-186, T-195) are S1 "as T-155", and T-193 (S2, closed forms) names the rational refinements S1.
- T-156: S1 confirmed: derived from T-155 (S1); its own certificate is the same padding, 1.8e-19 below T-101's side.
- News: none owed or revised. T-154's S5 item is fitzharding-n17-reported-proof (#588); nothing lowered below S4.
- Owner question (already on #543, "Policy paragraph", bead think-qh3s): the proposed paragraph, adopted as written, scores regularizations of credited packings S2 and would move T-155, T-156, T-166, T-170, T-171, T-174, T-186 and T-195 to S2; adopted with the line the 14 and 16 October reviews drew (a second certificate tighter only below the printed precision is S1) it moves none.
- PR: https://github.com/jlevy/squares/pull/749 (draft, S1, intake), head e0634f9cb (commits 195373889 review, 26339a13c merge of origin/main 598d23289, e0ca03be3 paper record re-measured, e0634f9cb re-pin).
