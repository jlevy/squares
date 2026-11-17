---
type: is
id: is-01m486y7zs8jxrkcd4qc2xs05m
title: Carry the sqverify-fast format T route to T-046's 27 and 28 September rectangle certificates
kind: task
status: closed
priority: 3
version: 4
delegate: w-backlog-1025
labels:
  - result-import
  - verifiers
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
hold: null
hold_until: null
created_at: 2026-10-06T08:58:00.568Z
updated_at: 2026-10-26T02:15:08.509Z
started_at: 2026-10-25T16:27:10.309Z
closed_at: 2026-10-26T02:15:08.509Z
close_reason: "22 rows re-run on reviewed source and 46 controls refused; review and evidence entries moved to think-buaj; PR #821"
resolution: null
duplicate_of: null
---
Carry the sqverify-fast format T census route (accepted for T-068's 34 certificates by docs/project/reviews/review-2026-10-06-sqverify-fast-format-t-route.md, section 5) to T-046's 48 standing certificates of the 27 and 28 September packets, so that T-046 itself can derive V3/C3. The census verified all 50 standing certificates of the 39d8ecc revision on 3 October, but the route does not carry as things stand:

1. 23 of the 82 rows of those packets were built from source bc2a6201 (not reviewed source) and rect_n18_L4695 records no build; re-run them on reviewed source with `devtools.sqverify_fast_census --packets 2026-09-27,2026-09-28 --only ...` (about 1.4 CPU-hours at the census's per-certificate times), then `--control` (about 30 s each).
2. T-046 has no mapped review of these certificates' mathematics (the 27 September scaling review is recorded only on a replay entry); a retained, accepted review that reads the 27 and 28 September certificates is needed and must be listed on T-046.
3. rect_n21_L4985, rect_n27_L56 and rect_n21_L49875 have mass n - 1/1000; tests/test_sqverify_fast_census.py's format_t_problems requires n - 1/100. Widening it is a change to the route's conditions that the review in (2) should read.

Then `--evidence` per certificate (audit_record that review), T-046 cites them, check_results derives the rungs. Not a condition of any verified bound: every count T-046 reports is held by a replayed entry or by later bounds.

## Notes

2026-10-26 w-backlog-1025: step 1 done in PR https://github.com/jlevy/squares/pull/821 (commit dcde87d28). The 22 standing T-046 certificates whose census rows came from bc2a6201, or recorded no build (rect_n18_L4695), were re-run at all 201 directions on reviewed source d97758bb (binary 567a0fd5, rustc 1.98.0). All are VERIFIED, with node counts equal to the earlier rows'. --control on all 46 standing certificates: 46 CONTROLS_REFUSED. --check: 46 of 46 VERIFIED. CPU: 5,040 s of re-runs, 568 s of controls and 60 s of build, about 1.57 CPU-hours (the bead priced 1.4 plus controls). rect_n31_L592 and rect_n32_L595 (bc2a6201) are not T-046's certificates and were not re-run. Steps 2 and 3 move to think-buaj, opened unclaimed at the coordinator's request: a mapped review of the 28 September certificates, which also reads the widening of format_t_problems to n - 1/1000 for rect_n27_L56, then the --evidence entries.
