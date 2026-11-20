---
type: is
id: is-01m7w07nbcjc2d1w1t4g8am1k3
title: "Stage 4 blind review of #1038's s(228) certificate (46ab8bf)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: r1038
labels: []
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-20T08:12:43.244Z
updated_at: 2026-11-20T09:11:00.334Z
started_at: 2026-11-20T08:14:07.359Z
---

## Notes

Lane r1038 (blind stage 4 review of issue 1038, s(228) <= 15.596043116632), 2026-11-20.

Branch claude/intake-2026-11-20-review-1038 (no PR; the coordinator opens one or merges the branch into an import lane).
- Checker and controls plan frozen 08:32:15Z, pushed 08:33:03Z (4d8bb9f): frozen/checker-frozen-digests.txt sha256 b22ca6238265da9b9fd9b13f2fa0403794929d7a07165c474779386dad40c5c6.
- Findings frozen 08:41:53Z, pushed 08:42:10Z (3cc5e67): frozen/findings-frozen-digest.txt sha256 708efc33d15b790153e35b434938c2ef4c674f6d593363422a957d22387e542b; frozen text sha256 c6008b980022502a93cf4799266d4494dff7c60975021f9fe419b43b9ee6bf75.
- Review: docs/project/reviews/review-2026-11-20-ozden-1038.md (mapped in document-map.yaml and SYNOPSIS.md); packet packing/resources/web/ozden-s228-1038-review-2026-11-20/.

Verdict: accepted as an upper bound. Both methods (integer separating axes; GMP clipping) accept every square, wall and pair: 25,878 pairs all apart, least margin 3.6267e-23 (156,166); 33 exact wall contacts (10 L, 8 B, 8 R, 7 T); claim = 12-place ceiling of S = 15.59604311663176650670114683218812228. 36 of 36 pre-stated controls as stated.
Findings: F6/F15 minor (author): the factor 2500000000000011391221/2500000000000000000000 is 1 + 4.5564884e-15, not "1 + 4.6e-18" (issue, README, certificate limitations). Others notes.
After the freeze: identity vs T-301 one to one, 86 beyond 1e-3, 5 beyond 0.1, max 0.238073; gain 4.289025e-9 = 1.2298 x T-301 contraction margin 3.487511e-9 (8.015e-10 below T-301 shrunk to first contact); own margin 4.39e-22; both maintained routes accept. Side is 9.6587e-14 above the KKT point held at row 3 (think-17ex; = 6.65e-14 factor + 6.33e-15 13-place rounding + 2.375e-14 jazivxt's print); that point's pose is not retained (blob e9e5bfe0), and the record's statements about its certificate differ (report outputs.solved routes true vs "certificate invalid"). Significance proposed S2. Option D facts in the review's "What Option D Implies"; the import lane decides.
Validation: packing-validate --edit 71 of 71 selected steps passed (rc 0; 675 s wall on 4 CPUs, reported against its 240 s ceiling, not failed); --records 55 of 55 passed (rc 0); the four document steps rerun on the final text passed. Branch head 1da77172022d0f13852efaa28a666d806ba43147, pushed 09:10:50Z. No PR opened (coordinator).
