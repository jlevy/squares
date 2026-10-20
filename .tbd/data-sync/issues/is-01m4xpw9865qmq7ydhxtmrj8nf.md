---
type: is
id: is-01m4xpw9865qmq7ydhxtmrj8nf
title: "Validate: Fang's 70 unreplayed theorem/ inventory certificates, both exact routes (~99 CPU-h all-pairs, 44 beyond the job ceiling; HELD)"
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wv278cdppm9155311gb6y5
created_at: 2026-10-14T17:20:36.614Z
updated_at: 2026-10-14T17:20:36.614Z
---
Validation part of think-0esw (Kevin Fang's Theorems 1 and 2 and the theorem/ inventory certificates at TheSnakeFang/squarepack-certs 078789a; T-178 in the 14 October records PR #602; tracked in jlevy/squares#603). HELD by the owner's cap, and the all-pairs kernel cannot run most of it at all.

## Validation
- Claim: the 70 unreplayed inventory certificates of theorem/ and theorem/best/ (343 to 4,038 squares, each at side (20000n - 1)/20000), pinned by digest in packing/resources/web/fang-excess-theorem-2026-10-13/acquisition/inventory-headers.json. 29 of them are the only report below the grid at their count (1486, 1564, 1643, 1644, 1725, 1726, 1809, 1810, 1895, 1896, 1983, 2073, 2165, 2356, 2975, 3085, 3197, 3311, 3427, 3545, 3546, 3665, 3666, 3787, 3788, 3911, 3912, 4037, 4038) and become beyond-horizon rows once retained and replayed; the other 41 are above another row. The replays move no rung of T-178; they are the rows' evidence.
- Run: retain the 70 certificates first (a hosted-data release or the W7 checker's packet, from the frozen digests), then `devtools.upper_bound_reports fang-excess-theorem-2026-10-13 certify --jobs-dir DIR --workers 1` (positive and two controls, both maintained routes) and `check --replay`. Alternatively the W7 bucketed exact route (decide a pair only where centres are at most sqrt 2 apart, an exact rational test), with its own soundness review and a receipt that keeps verdicts and digests in place of every input.
- Cost: 99.2 CPU-h for certify with the all-pairs kernel at 0.69 ms per pair and job (both routes), measured on the six-certificate sample on 2026-10-14 (1,278.6 route CPU s for 616,298 pairs x 3 jobs; packet README, What Was Not Run); about twice that with check --replay. The 29 record-relevant certificates alone are 70.0 CPU-h for certify (140 with check --replay). The 44 certificates above 1,263 squares, which include all 29, exceed the kernel's 600 s job ceiling and the largest its 4 MB receipt bound, so they cannot run on this kernel at any budget. The bucketed route is priced at under 1 CPU-h for all 76 once written and reviewed (the 14 October review's own bucketed program decided all 76 rebuilt certificates strict-valid in 60 CPU s; that is review evidence, not a maintained route).
- Budget status (owner, 2026-10-14): HELD (> 40 CPU-h, awaiting the owner).
- Possible <= 40 CPU-h subset (proposal only; never to be run without the owner's word): (a) the 26 certificates of 343 to 1,263 squares, inside the job ceiling: 4.5 CPU-h for certify, 9.0 with check --replay (about 13 at the 380-382 replay's loaded rate); none of them is the smallest report at its count, so it moves no row. (b) Better: write the W7 bucketed route (engineering plus a soundness review), then all 76 for under 1 CPU-h, which would bring the whole item under the cap.
- Depends on: retention of the 70 certificates (hosted-data release, OR-18); for the 29 that matter, the W7 bucketed route (no bead owns it yet); the owner's budget for the all-pairs path.
- Done when: every one of the 70 passes both routes with both controls refused, the receipt is kept, the 29 beyond-horizon rows are added to the claims record at verified, and the result is noted on think-0esw and #603.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. The all-pairs subset (a) is about 5 wall-h on one worker.
