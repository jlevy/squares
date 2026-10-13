---
type: is
id: is-01m3vbj2m44gt7t72ncesjh52d
title: Intake independent wand125 point-only s61 certificate from its primary source
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3v9vq36ykk2jdzce75req44
created_at: 2026-10-01T09:08:37.122Z
updated_at: 2026-10-12T23:40:14.524Z
closed_at: 2026-10-12T23:39:22.432Z
close_reason: "Completed in c96b2df09 (2026-10-03): packet retained, zmx2 replay certifies all 6,400 D4 roots, evidence E-n061-wand125-point-cover-zmx2-replay on T-063."
resolution: null
duplicate_of: null
---
Evand Oct1 audit cites wand125/square-packing-bounds f8846cec9661773dbd0cc7cbeee7d01ddb12a2b8 point_n61_L8 and secondary s61_wand125/MANIFEST.txt. Acquire primary pinned proof/certificate/credits and checker contract; assign a distinct result/evidence lineage after intake, review and select replay. Existing evand s60-derived s61 is not independent verification of this source.

## Notes

2026-10-02: Daniel reports (comment on #238) zeromargin.py certifies all 12,800 D4 roots of wand125's point-only s(61) cover (2 after a depth-30 rerun) and zmcheck --d4 ZM_MIXPAIR=1 all 6,400. Records retained in packing/resources/web/evand-square-packing-2026-10-02/ (commit bb4861536). The cover equals the evand-retained blob cb6797c8 (wand125 point_n61_L8 at f8846cec). All checkers already retained; replay here costs ~0.13 CPU-h (zmx2 --d4), 0.85 h zeromargin, 1.07 h zmcheck. Register as reported evidence on T-063 (point-only route).
