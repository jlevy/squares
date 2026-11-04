---
type: is
id: is-01m6f36643h3c14ttaabspvn0n
title: "Stage 4 review of T-132's mixed_n29_L582 (wand125 s(29) >= 291/50, #446): the review that reads the certificate, owed before its census evidence can be mapped"
kind: task
status: open
priority: 2
version: 2
labels:
  - result-import
  - validation
dependencies: []
parent_id: is-01m4jk4cae8514p87y79gsh17n
created_at: 2026-11-02T21:38:31.171Z
updated_at: 2026-11-04T15:59:10.112Z
---
T-132 (wand125's s(29) >= 291/50, mixed_n29_L582, reported on jlevy/squares#446) has no review that reads its certificate: the 11 October final review read only the record and premises (its F1-2 says the stage 4 review that reads the certificates is still owed), and the 23 October #446 review read n = 19, 20 and 26. The declared-net route's checklist (docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md, For the Records Lane, item 7) needs "a review under docs/project/reviews/ [that] read this certificate and accepted it" before a census replay's evidence can be mapped, and check_results' verified_lane_review_problems holds an adoption at n = 29 to a mapped review. So T-132 cannot leave V0/C0 by a census alone.

## Review
- What: the stage 4 mathematical review of mixed_n29_L582 (result-import.md, Stage 4: Validate, "The review"), by the 6 October declared-net checklist: re-derive the argument from the certificate to s(29) >= 291/50 (lemma N0 on the declared net, step 1/5002, core 4999/5000, 2,073 directions, the per-bin domain, mass 2899999/100000), recompute every exact premise apart from the crate and the tools, read the source's check2 receipt, run log and 197/200 control, and decide sampled directions or poses exactly with the reviewer's own code; a summary for the author, findings graded, mapped under docs/project/reviews/, recorded as external_review on E-wand125-fine-net-n29-582-followup-report and in T-132's reviews, covers [T-132].
- Who: a tbd-strong-max sub-agent at maximum reasoning in its own worktree, sharing no context with the replay lane (result-import.md), as the 14 October review was for T-176 to T-179.
- Inputs retained (2 November, commit 219bc1268): the release asset's six data members in packing/resources/web/wand125-fine-net-n29-2026-10-10/release/certificates/mixed_n29_L582/ (candidate 182,193 B, c9171c92..., check2 receipt, run log, control and control log, pre-publication receipt), the pinned documents' digests in source-manifest.json, receipts/premises.json and receipts/sample-diagnostic.json; the census reads the candidate from release/ (sqverify_fast_census MIXED_ROOTS).
- Then: the census capture and whole-net control (priced 4.3 to 5.5 CPU-hours; n29's axis gap 5.2e-10 is inside AXIS_ROUNDING, so its control can end CONTROLS_REFUSED), --evidence with this review as the audit record, and the adoption at n = 29 the house rule derives (both lanes from T-108's 581/100).

## Notes

2026-11-04 bold-ritchie-l32 (PR #889, review F4): this bead says n = 29's axis gap, 5.2e-10, is "inside the census's axis allowance". That no longer holds as a criterion. #892 (merged at 0bc5a08c5) removed the constant AXIS_ROUNDING: a whole-net control's axis refusal is now judged by the vertex sweep's own enclosure, recomputed from the candidate, with the crate's bound as its lower end to the bit and the exact capture inside it. That is how T-176's n39 control passed. T-132's next_rung in packing/frontier/results.yaml is reworded to say so on #889. The gap figure stays as a measurement only.
