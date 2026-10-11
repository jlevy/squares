---
type: is
id: is-01m45gcwkj0q9bbbms9z82vxfy
title: "Stage 4 of T-094: review and replay wand125's mixed_n67_L848 and mixed_n84_L9411 (#282)"
kind: task
status: closed
priority: 2
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
created_at: 2026-10-05T07:45:34.322Z
updated_at: 2026-10-06T02:41:34.941Z
closed_at: 2026-10-06T02:41:34.940Z
close_reason: Done in jlevy/squares#369 (merged 34e87a86b); verdict replies posted 2026-10-06
resolution: null
duplicate_of: null
---
Stage 4 (W2) for T-094, the two mixed rectangle-measure certificates wand125/square-packing-bounds published on 5 October 2026 (s(67) >= 212/25, s(84) >= 9411/1000), retained in packing/resources/web/wand125-mixed-bounds-2026-10-05 at a541afb. Two lanes. Review: a mapped review under docs/project/reviews/ of the two certificates, as review-2026-10-05-wand125-october-4-certificates.md read T-090 and T-091 (checker byte-identical to the one already read, the tarball binding without a completion-audit.json, margins and supersessions in exact arithmetic); recorded as external_review on E-n067-wand125-mixed-848-report and E-n084-wand125-mixed-9411-report, which takes T-094 to C1. Replay: the complete 201-angle replays, 26.5 CPU-hours planned (23.7 by mixed-price, 21.2 by the source's own oblique seconds), mixed-shard wand125-mixed-bounds-2026-10-05 --runners 2 (two hosts of four workers, about 3.3 wall hours each), mixed-replay per range and mixed-merge per certificate, receipts committed to the packet. Held for a compute budget the owner sets, as the T-090 and T-091 replays are. Not started.

## Notes

2026-10-05 19:05 Done by lane C (think-7fxu) on branch claude/ecstatic-pascal-pothtx-mixed-verify, not by a source-checker replay: sqverify-fast decided mixed_n67_L848 and mixed_n84_L9411 at all 201 directions (VERIFIED, 1,388 and 1,878 CPU-s at two threads; controls refused), and the separately prompted review docs/project/reviews/review-2026-10-05-wand125-october-5-and-independent-replays.md (claude-opus-5-5) accepted both certificates' mathematics and the route (IR-1 to IR-5, none blocking). T-094 at V3/C3; verified lower bounds n = 67 -> 212/25, n = 84 -> 9411/1000. The 26.5 CPU-h source-checker replay was not run; it would add a reproduction with the producer's code beside the rung. Close at the lane's merge.
