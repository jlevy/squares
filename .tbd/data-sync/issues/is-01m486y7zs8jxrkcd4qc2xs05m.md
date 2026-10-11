---
type: is
id: is-01m486y7zs8jxrkcd4qc2xs05m
title: Carry the sqverify-fast format T route to T-046's 27 and 28 September rectangle certificates
kind: task
status: open
priority: 3
version: 1
labels:
  - result-import
  - verifiers
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-06T08:58:00.568Z
updated_at: 2026-10-06T08:58:00.568Z
---
Carry the sqverify-fast format T census route (accepted for T-068's 34 certificates by docs/project/reviews/review-2026-10-06-sqverify-fast-format-t-route.md, section 5) to T-046's 48 standing certificates of the 27 and 28 September packets, so that T-046 itself can derive V3/C3. The census verified all 50 standing certificates of the 39d8ecc revision on 3 October, but the route does not carry as things stand:

1. 23 of the 82 rows of those packets were built from source bc2a6201 (not reviewed source) and rect_n18_L4695 records no build; re-run them on reviewed source with `devtools.sqverify_fast_census --packets 2026-09-27,2026-09-28 --only ...` (about 1.4 CPU-hours at the census's per-certificate times), then `--control` (about 30 s each).
2. T-046 has no mapped review of these certificates' mathematics (the 27 September scaling review is recorded only on a replay entry); a retained, accepted review that reads the 27 and 28 September certificates is needed and must be listed on T-046.
3. rect_n21_L4985, rect_n27_L56 and rect_n21_L49875 have mass n - 1/1000; tests/test_sqverify_fast_census.py's format_t_problems requires n - 1/100. Widening it is a change to the route's conditions that the review in (2) should read.

Then `--evidence` per certificate (audit_record that review), T-046 cites them, check_results derives the rungs. Not a condition of any verified bound: every count T-046 reports is held by a replayed entry or by later bounds.
