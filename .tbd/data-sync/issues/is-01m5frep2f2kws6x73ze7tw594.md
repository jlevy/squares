---
type: is
id: is-01m5frep2f2kws6x73ze7tw594
title: "PR #704 B6: Evan Daniel's solved views below T-196 at 227 and 260 (register candidates, policy row 3) have no disposition"
kind: bug
status: open
priority: 3
version: 1
labels:
  - result-import
  - regularization
dependencies: []
parent_id: is-01m5fre23qy5rq285h9tsarhz0
created_at: 2026-10-21T17:34:27.918Z
updated_at: 2026-10-21T17:34:27.918Z
---
Low. The selection cases/regularized_drawings/think-qdcc-2026-10-20/selection-n227-n260.json lists his solved views of T-196, 1.66e-8 below at 227 (side 486368646470642329014092781873/31250000000000000000000000000) and 1.81e-8 below at 260 (side 4161444696515435316429350771309/250000000000000000000000000000), run evand-regularize-adopt-2026-10-20-n227-260-evand, as register candidates (regularization policy row 3). The House Rule says such a view is registered as a result and taken through stages 3 and 4 (regularization-process.md, Register Candidates: one batch result with a regularizations item per count, as T-155 via devtools.register_regularized_bounds, crediting de Winter for the packing and Evan Daniel for the regularization). Deferred, not done in PR #704: at both counts a smaller packing than the view is already reported. At 260 Couzo's T-223 (V0/C0, registered by #701) is 2.56e-5 below T-196, and #706 validates and adopts it after #704 lands; at 227 Couzo's #672 (not yet registered) is 1.71e-4 below T-196. Waits on: #706 at 260 and #672's import at 227. Done when, for each count, either the house best packing has moved below the view (record that the view is no longer a register candidate, with the side relation, and close) or the view is registered and taken through stages 3 and 4. Review B: https://github.com/jlevy/squares/pull/704#issuecomment-6306759614
