---
type: is
id: is-01m5e6pbr0vtzj4w53c7r4v5zp
title: "Register candidates at 227 and 260: Evan Daniel's solved views below T-196 (review B6 of #704)"
kind: task
status: open
priority: 3
version: 2
labels:
  - regularization
dependencies: []
created_at: 2026-10-21T03:04:50.688Z
updated_at: 2026-10-21T03:04:59.347Z
---
Register candidates (regularization policy, decision table row 3) from the adoption of T-196 (#668, PR #704, think-qdcc) at 227 and 260, recorded here as review B6 of #704 asked. Not registered and not admitted.

Evan Daniel's driver, run `evand-regularize-adopt-2026-10-20-n227-260-evand` on the new witnesses, solved to views below the new house best packings' sides:
- n = 227: side - U = -1.66e-08 (view `evand:adopt-2026-10-20-n227-260-evand:solved`)
- n = 260: side - U = -1.81e-08 (the same run's solved view)

Evidence: packing/cases/regularized_drawings/think-qdcc-2026-10-20/selection-n227-n260.md, "Register candidates", and selection-n227-n260.json beside the run's receipt, blocks and reports.

What the rules say: result-import.md, "The House Rule", and the regularization guide's "Register Candidates": a view below the house best packing's side is a smaller packing, registered as a result (row 3) through stages 3 and 4, crediting the packing's finder and the regularizer, adopted once validated; such views are registered as one batch result through devtools.register_regularized_bounds, as T-155 registered 59 counts.

Why it waits: both views are moot for adoption. At 227 Couzo's #672 is 1.71e-04 below T-196 and not yet registered; at 260 Couzo's T-223 (#678, registered at V0/C0 by #701) is 2.56e-05 below it, and #706 validates and adopts it. Each smaller packing is far below these views (1.66e-08 and 1.81e-08 below T-196). Once a smaller packing is adopted at a count, the view there is above the new U (row 4, not a drawing frame) and stops being a candidate. Under the guide, the bound is new only where no earlier certificate states that side or a smaller one. #672 and T-223 already do, once registered.

Done when either (a) both counts have a validated house best packing below these views and this bead closes with that reason, or (b) one count stays at T-196 and its view is registered as a batch result through register_regularized_bounds, with a regularizations item, and adopted under the House Rule.
