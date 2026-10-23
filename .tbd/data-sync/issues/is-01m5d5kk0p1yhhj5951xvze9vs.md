---
type: is
id: is-01m5d5kk0p1yhhj5951xvze9vs
title: "Import Evan Daniel: s(154) <= 12.921100940762 (#694)"
kind: task
status: closed
priority: 1
version: 5
labels:
  - result-import
dependencies: []
parent_id: is-01m5c0fwsxga70rszkjy1zbp2f
created_at: 2026-10-20T17:26:36.822Z
updated_at: 2026-10-23T05:32:47.365Z
closed_at: 2026-10-23T05:32:47.365Z
close_reason: "Tracker audit 2026-10-23 (c-audit-c-1023, think-lrg9), checked by coord-intake-1023: DONE. T-222 V3/C3 (#699); #694 CLOSED 2026-10-21; ask done"
resolution: null
duplicate_of: null
---
Stage 1 to 3 import of jlevy/squares#694 (Evan Daniel, filed 2026-10-20T03:56:43Z), lane c-lane-evand-2 under think-eizi.

## Claim map
- Source: evand/square-packing at 1d2bb82035af4b7eb4658488543e46b67d1099ca (committed 2026-10-20T03:54:48Z), search/packer/candidates/s154_sw.cert, SHA-256 c2242dcda1ae3d4c9d580af14ed9adf425780320d94846c3c96f5c3ee486d78d, and its same-side regularized view s154_sw_regularized.cert, SHA-256 7fb7f288a864e9d3190e7b1b01f2491e7ce97f5e2e9e7de9b1dae3768580d2bd. Both digests match the issue.
- One claim: s(154) <= 12.921100940761680549856582087576 (the certificate's exact rational side), printed 12.921100940762 (rounded up at 12 places). Register action: a new entry.
- Standing at 154: house T-186 (Mishapolk's 14 October KKT refinement of Couzo's #586 packing, found by Daniel), exact side 12.92120657713263105...; T-182 (#586) at the same side to 12 places. No open report states a smaller side at 154 (open issues through #698 read on 2026-10-20).
- Source statements not decided here: a KKT point, not shown to be a strict local minimum (one negative-curvature direction, inconclusive), 9 rattlers, 38 tilted squares; a different KKT point from #586's, with no continuous path found up to 1e-2 above #586's side (heuristic).
- Ask: credit Francisco Couzo's #586 arrangement (continued from Daniel's #552) and Daniil Ostashev's s(156) packing as its starts.

## Validation plan (priced)
- Exact certification on the two maintained routes with the duplicate-square and outside-container controls, via devtools.upper_bound_reports certify: about 1 CPU-minute, run in this lane.
- Stage 4 mathematical review (tbd-strong-max), run by the coordinator. Then V3/C3, adoption at 154 and regularization of the new house in the stage 4 pull request.

## Notes

2026-10-20 (c-lane-evand-2): stages 1 to 3 done on claude/intake-2026-10-20-evand-308-154, draft PR https://github.com/jlevy/squares/pull/699 (head 34d72a95a; data commits 277bcd50a and the suite-a fix 938e5f573; hosted Packing validation run 39476391860 green). Packet packing/resources/web/evand-n154-sweep-2026-10-20 at 1d2bb82; digests match the issue. Both maintained exact routes accept the positive and refuse both controls (receipt retained). Registered as T-222, V0/C0, 1.05636370950500e-4 below T-186 at 154. n-154.md has no note: it is the adoption writer's (not HAND_MARKED), so the stage 4 adoption writes its prose. Credit ask queued on this bead until adoption. Reply draft: scratchpad/replies-new/694.md (post after merge; asks about dgen.py and the regularized view's "by" field).
Next: stage 4 mathematical review (coordinator, with Fable), then V3/C3, adoption at 154 and regularization of the new house in the stage 4 PR.


2026-10-20 23:40Z coordinator (review B1 of #699). Stage 7 reply to #694, drafted in replies-new/694.fixed.md, owes the same three questions as think-h8jm: (1) A4: the views' 'by' field, with no reading stated (RW-4: drop 'The record reads the field as your regularizer's, not as a credit'); (2) binary64 rows; (3) KKT precision and second-order statements.
