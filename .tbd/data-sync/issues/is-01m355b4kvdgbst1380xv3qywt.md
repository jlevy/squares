---
type: is
id: is-01m355b4kvdgbst1380xv3qywt
title: Add independent rectangle-density verification and preserve continuous coverage slack
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies: []
created_at: 2026-09-22T18:16:40.819Z
updated_at: 2026-10-06T08:35:04.560Z
closed_at: 2026-10-06T08:35:04.550Z
close_reason: |
  Duplicate (bead review 2026-10-06, origin/main eb43ffe9a): duplicate of think-bmf3 (native exact rectangle-density coverage verifier, with think-aqne for a complete replay); ck07's transport-error and admission-guard constraints copied to bmf3's notes
resolution: duplicate
duplicate_of: is-01m3p04ndehpya7g3mbmmad36g
---
Session 152 fully replayed Tokoharu rectangle densities at n11=3.81, n26=5.508 and n29=5.71. Exact mass, orbit expansion, net/shrink, axis partitions and candidate-to-interval enclosures pass independent preflight; sampled exact polygon and derivative controls are not a second global coverage proof. Develop an independently implemented complete rectangle-density coverage decision, preserving continuous translation and rotation domains and rigorously outward arithmetic. Keep densities as their own certificate type. Any conversion to point masses must bound transport error and pay it from actual coverage slack; placing rectangle mass at cell centres is unsound without that proof. Input admission must include the guards in think-c0xc. Evidence: docs/project/reviews/review-2026-09-22-tokoharu-density-mathematics.md.

## Notes

The completed source replays and mathematical review already qualify the fixed density bounds for the verified Frontier fields. This follow-up supplies an additional complete method and native reusable coverage, not a prerequisite for those adoptions.
