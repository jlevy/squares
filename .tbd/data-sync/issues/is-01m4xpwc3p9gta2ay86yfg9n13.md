---
type: is
id: is-01m4xpwc3p9gta2ay86yfg9n13
title: "Validate: regenerate and replay Fang's 53 table-only composites (replay ~59-119 CPU-h, regeneration unmeasured; HELD)"
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4xmr1psrjaabyjsp60ccn67
created_at: 2026-10-14T17:20:39.542Z
updated_at: 2026-10-14T17:20:39.542Z
---
Validation part of think-rn2y (Kevin Fang's Section 5 composites, bef5c42; tracked in jlevy/squares#603): the 53 counts where the smallest report is a table row the source does not ship. Its cost is not established: regeneration is unmeasured.

## Validation
- Claim: at 53 counts the smallest report is a composites/table.csv row with status reproducible-only (the certificate is not shipped): 420, 462, 506, 552, 600, 650, 702, 756, 757, 812, 813, 870, 871, 930, 931, 992, 993, 1057, 1058, 1123, 1124, 1191, 1192, 1261, 1262, 1333, 1334, 1407, 1408, 1484, 1561, 1562, 1641, 2258, 2354, 2452, 2453, 2552, 2553, 2654, 2655, 2759, 2760, 2865, 2866, 2974, 3084, 3195, 3196, 3309, 3425, 3543, 3663. Each row names its pieces A and B, its side rounded up at 15 places and the SHA-256 of the certificate it regenerates.
- Run: regenerate each certificate, preferably first-party with the rebuild program the 14 October review kept (packing/resources/web/fang-excess-theorem-2026-10-13/review/programs/, which rebuilt all 76 inventory certificates byte for byte), else the source's composites/reproduce.sh (a source program, read before it runs); check each digest against table.csv; then certify and check --replay on both maintained routes as for the shipped composites.
- Cost: not established. Regeneration is unmeasured. The replay alone is 59.4 CPU-h for certify at 0.69 ms per pair and job, 118.9 with check --replay; 28 of the 53 (1,333 squares and up) exceed the 600 s job ceiling.
- Budget status (owner, 2026-10-14): HELD (> 40 CPU-h, awaiting the owner).
- Possible <= 40 CPU-h subset (proposal only; never to be run without the owner's word): the 25 counts from 420 to 1,262, inside the job ceiling: 5.9 CPU-h for certify, 11.9 with check --replay, plus regeneration (unmeasured; the review rebuilt 76 larger certificates in about a minute).
- Depends on: a decision to regenerate (first-party program or the source's script); the composites built on de Winter's 211-square piece were left out of the release for licence reasons (review MR-4), so check each row's pieces; for 28 counts, the W7 bucketed route; the owner's budget.
- Done when: each regenerated certificate's digest equals table.csv, each passes both routes with controls refused, and its row enters the claims record; noted on think-rn2y and #603.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate.
