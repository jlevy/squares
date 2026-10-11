---
type: is
id: is-01m48w7bvnkmbrxxx6fdnqa348
title: Review the sqverify-fast census route for format L, then add independent replay entries to T-076 n82, T-073 n83 and T-080 n101
kind: task
status: open
priority: 3
version: 1
labels:
  - result-import
  - verifiers
dependencies: []
created_at: 2026-10-06T15:09:59.541Z
updated_at: 2026-10-06T15:09:59.541Z
---
Optional confirmation beside rungs that already stand. The census route (review-2026-10-05-wand125-october-5-and-independent-replays.md, Carrying the Route) admits a sqverify-fast census row as a complete replay only for format M rectangle densities with no point or segment; tests/test_sqverify_fast_census.py holds that. Three linear (format L: points, segments and rectangles) certificates are verified here by the source's own checker only: T-076 mixed_n82_L932 (V3/C3), T-073 mixed_n83_L935 and T-080 mixed_n101_L1028. sqverify-fast decides format L (Milestone B, lemmas B1-B3) and all three have VERIFIED census rows, but n82's is from the reviewed build 9985c465 while n83's (71f83e7e) and n101's (f8c7373c) are from unreviewed builds.

To give them independent replay entries: (1) a separately prompted review of the route for format L (the point and segment lemmas, the domain Tokoharu's format uses, the control mutation for points and segments), the conditions a records lane checks per certificate, and the change to the census test; (2) re-run n83 and n101 from reviewed source (main's d97758bb), about 3,200 CPU-s; (3) --control on all three; (4) evidence entries and records as for T-075 (commit b3e917247 on claude/ecstatic-pascal-pothtx-r4). No bound moves: each count already rests on a complete replay of the source's checker. Found by lane R4 of think-wyf4 (think-r7yt's linear part).
