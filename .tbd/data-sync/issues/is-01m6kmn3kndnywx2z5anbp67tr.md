---
type: is
id: is-01m6kmn3kndnywx2z5anbp67tr
title: "Stage 4 review of T-142's mixed_n28_L57425 and T-143's mixed_n30_L58925 (wand125 s(28) >= 2297/400, s(30) >= 2357/400): the review that reads the certificates, owed before their census evidence can be mapped"
kind: task
status: open
priority: 2
version: 2
labels:
  - result-import
  - validation
dependencies: []
parent_id: is-01m4kbxmtaqt87tdw33cs19ah8
created_at: 2026-11-04T16:00:43.636Z
updated_at: 2026-11-04T17:45:42.275Z
---
T-142 (wand125's s(28) >= 2297/400, mixed_n28_L57425) and T-143 (s(30) >= 2357/400, mixed_n30_L58925), reported on no issue and registered at V0/C0, have no review that reads their certificates: the 11 October final review read the record and premises only. The declared-net route's checklist (docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md, For the Records Lane, item 7) needs a review under docs/project/reviews/ that read the certificate and accepted it before a census replay's evidence can be mapped, and check_results' verified_lane_review_problems holds an adoption at n = 28 or 30 to a mapped review. So neither can leave V0/C0 by a census alone, as think-1lri says of T-132.

## Review
- What: the stage 4 mathematical review of mixed_n28_L57425 and mixed_n30_L58925 (result-import.md, Stage 4: Validate, "The review"), by the 6 October declared-net checklist: re-derive the argument from each certificate to its claim (lemma N0 on the declared net, step 1/5002, core 4999/5000, 2,073 directions, the per-bin domain, masses 2799999/100000 and 2999999/100000), recompute every exact premise apart from the crate and the tools, read the source's check2 receipts, run logs and 197/200 controls, and decide sampled directions or poses exactly with the reviewer's own code; a summary for the author, findings graded, mapped under docs/project/reviews/, recorded as external_review on E-wand125-fine-net-n28-57425-report and E-wand125-fine-net-n30-58925-report and in T-142's and T-143's reviews.
- Who: a tbd-strong-max sub-agent at maximum reasoning in its own worktree, sharing no context with the replay lane (result-import.md).
- Inputs: the release assets certificates__mixed_n28_L57425.tar.gz and certificates__mixed_n30_L58925.tar.gz are pinned by size and digest in packing/resources/web/wand125-fine-net-n28-n30-2026-10-10/ and not retained; the review needs their data members retained first, as think-r333 retained n29's on 2 November (devtools.fine_net_followup retain; jlevy/squares#543 still asks the owner whether the three check2 candidates are kept in Git).
- Then: the census capture and whole-net control of each, priced on think-i85v (T-142 3.3 to 4.5 CPU-hours, T-143 4.5 to 6.1), --evidence with this review as the audit record, and the adoptions at n = 28 and 30 the house rule derives (both lanes from T-107's 1147/200 and T-109's 11767/2000). The census packet needs MIXED_PACKETS and MIXED_ROOTS entries in sqverify_fast_census. T-142's axis gap of 2.15e-9 no longer holds its control: #892's enclosure rule judges it.

## Notes

2026-11-04 bold-ritchie-l42: the inputs are retained (branch claude/bold-ritchie-xo28us-l42, commit 7ccb06b3c, PR #903). devtools.fine_net_followup retain held certificates__mixed_n28_L57425.tar.gz (627,191 B, 7d0f9107...3bf3) and certificates__mixed_n30_L58925.tar.gz (638,622 B, 0d11fe05...61ba) to their pins and copied six data members each into packing/resources/web/wand125-fine-net-n28-n30-2026-10-10/release/certificates/ (candidates 178,089 B 5ef20511... and 130,050 B 981a17db..., every member equal to source-manifest.json). check-retained: 0 problems. The census reads the packet (MIXED_PACKETS, MIXED_ROOTS, SHARED_CRATE_PACKETS); no census row yet. The owner answered #543's retention question on 17 October (retain fine-net candidates where the census reads them), so the description's Inputs line is now met. The coordinator launched the review on 4 November against 78729cfc2; the census, controls, evidence and adoptions follow in a PR after #903.
