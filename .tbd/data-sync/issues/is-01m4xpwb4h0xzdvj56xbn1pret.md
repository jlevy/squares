---
type: is
id: is-01m4xpwb4h0xzdvj56xbn1pret
title: "Validate: Fang's 38 shipped Section 5 composites, both exact routes (~122 CPU-h with check --replay, 61 certify only; HELD)"
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4xmr1psrjaabyjsp60ccn67
created_at: 2026-10-14T17:20:38.545Z
updated_at: 2026-10-14T17:20:38.545Z
---
Validation part of think-rn2y (Kevin Fang's Section 5 composites at TheSnakeFang/squarepack-certs bef5c42, unchanged at 078789a; tracked in jlevy/squares#603). HELD by the owner's cap.

## Validation
- Claim: the 38 shipped composite certificates of composites/ (table.csv rows with status shipped, 703 to 4,035 squares). At 28 counts the shipped certificate is the smallest report and becomes a beyond-horizon row: 703, 994, 1125, 1193, 1263, 1335, 1409, 1485, 1563, 1642, 1724, 1808, 1894, 1982, 2072, 2164, 2259, 2355, 2454, 2554, 2656, 3310, 3426, 3544, 3664, 3785, 3909, 4035. At the other 10 (757, 813, 871, 931, 1058, 2760, 2866, 2974, 3084, 3196) a table-only row is smaller.
- Run: the 38 are pinned by digest in packing/resources/web/fang-excess-theorem-2026-10-13/ (23 MB, not retained); retain them (hosted data or the import's own packet), then `devtools.upper_bound_reports PACKET certify --jobs-dir DIR --workers 1` (positive and two controls, both maintained routes) and `check --replay`; or the W7 bucketed exact route.
- Cost: 122.3 CPU-h as think-rn2y prices it: 106,362,158 pairs x 0.69 ms x 3 jobs x 2, which is certify plus check --replay at the 0.69 ms per pair and job the theorem sample measured (certify alone 61.2 CPU-h). The 28 smallest-report: 94.5 CPU-h (certify alone 47.3). Largest job n = 4,035, about 5,616 s per job. 28 of the 38 exceed the kernel's 600 s job ceiling (all above 1,263 squares), so the all-pairs kernel cannot run them at any budget; the W7 bucketed route would.
- Budget status (owner, 2026-10-14): HELD (> 40 CPU-h, awaiting the owner).
- Possible <= 40 CPU-h subset (proposal only; never to be run without the owner's word): the five smallest-report shipped composites inside the job ceiling, 703, 994, 1125, 1193 and 1263: 1.7 CPU-h for certify, 3.3 with check --replay; each verifies a beyond-horizon row. The other 23 rows need the W7 bucketed route.
- Depends on: retention of the shipped certificates (OR-18); for 28 of 38, the W7 bucketed exact route (no bead owns it yet); the owner's budget.
- Done when: every replayed certificate passes both routes with both controls refused, the receipt is kept, and the rows of the replayed counts enter the claims record at verified (the other rows at reported); noted on think-rn2y and #603.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. The five-count subset is about 2 wall-h on one worker under load.
