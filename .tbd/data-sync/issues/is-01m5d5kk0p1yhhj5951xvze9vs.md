---
type: is
id: is-01m5d5kk0p1yhhj5951xvze9vs
title: "Import Evan Daniel: s(154) <= 12.921100940762 (#694)"
kind: task
status: open
priority: 1
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m5c0fwsxga70rszkjy1zbp2f
created_at: 2026-10-20T17:26:36.822Z
updated_at: 2026-10-20T17:26:36.822Z
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
