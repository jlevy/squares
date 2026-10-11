---
type: is
id: is-01m471mzy4w6jycg53h50v68zc
title: "Stage 4 of T-097: the complete replay of wand125's mixed_n66_L843 (#282), about 15.5 CPU-hours"
kind: task
status: open
priority: 2
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-05T22:06:20.098Z
updated_at: 2026-10-06T03:05:29.762Z
---
T-097 (provisional id; s(66) >= 843/100, packet wand125-mixed-bounds-finer-net-2026-10-05, pinned 43050ed) is at V0/C1 after the 5 October review (docs/project/reviews/review-2026-10-05-wand125-declared-net-n18-n66.md, no defect). Lane B ran the source's checker at 12 of 201 directions (receipts/n66-L843/range-*/ in the packet, all matching) and sqverify-fast at all 201 (census-mixed), neither of which moves the rung. The exit: from packing/, devtools.audit_wand125_point_and_mixed mixed-replay n66-L843 over the remaining ranges (1 to 23, 26 to 99, 102 to 146, 149 to 155, 158 to 198; the six sampled ranges are done and resume), then mixed-merge n66-L843 must print FULL_REPLAY_MATCHES_SHIPPED; then an E-n066-wand125-mixed-843-source-replay entry, T-097 to V3/C3, and n = 66's verified lower bound from 421/50 to 843/100 with its consumers (case record, views, piercing survey, bound citations, tests). Priced at 15.5 CPU-hours (16.2 by the source's oblique seconds; the sample ran at 1.24x the source's seconds). Held for a compute budget.

## Notes

2026-10-06: stale gate. T-097 moved to V3/C3 by sqverify-fast at the reviewed source (think-e60e, jlevy/squares#369). The complete source-checker replay (~15.5 CPU-hours) no longer gates the n = 66 move; it would add a second confirmation, by the producer's own checker, beside the rung.
