---
type: is
id: is-01m21c5wgz0kwdqgb7rnehpm5e
title: "PR127 R1: correct the rounded-cover and enlargement helper lemmas"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m21badm7ednkkxzwgcjmgaam
created_at: 2026-09-08T20:43:29.181Z
updated_at: 2026-09-08T23:03:18.392Z
closed_at: 2026-09-08T23:03:18.390Z
close_reason: Corrections are committed in ef8a2e72 and cbe9fd76 and documented in docs/project/reviews/review-2026-09-08-pr127-research-readiness.md. The completed checkpoint combines actual passing cbe9fd76 fast, negative-control, slow and exhaustive receipts with four unchanged geometry passes from the failed ef8a2e72 full run. Scientific limits and unrun complements remain explicit.
resolution: null
duplicate_of: null
---
Lane E 143-164 and exp-132 320-328: scaled T018 at q gives Q=[0,1]^2 rounded by 3/500 only 85353/100000 mass, not at least 1; the unscaled control gives 4001/4000. Two independent rational distance formulas agree over all 1121 atoms. E2 enlargement by 1+2delta fails at rotated corners; two 45-degree squares separated by more than 2delta can overlap after this enlargement. Withdraw unsupported no-LP and no-eleven conclusions and restrict point-mark claims. E4 independently replayed successfully and does not use these helpers. Audit packet: /private/tmp/squares-pr127-review.
