---
type: is
id: is-01m859v2drzgkxas4z184he310
title: Diagnose failed grid-slack rows and test localized grid repairs
kind: task
status: in_progress
priority: 2
version: 3
delegate: codex-exact-grid-repair-1123
labels:
  - regularization
  - validation
dependencies: []
child_order_hints:
  - is-01m85bk7fexs4he29m1qhwwy17
hold: null
hold_until: null
created_at: 2026-11-23T22:53:46.287Z
updated_at: 2026-11-23T23:24:26.476Z
started_at: 2026-11-23T23:20:33.404Z
---
The manual review of the deployed defaults measured 232 (112 uneven aligned squares),
259 (65), 290 and 291 (31 each), 131 (21), 305 (13), and 127 (2). The retained
selected-default grid census is under agent evidence at
drawing-audit-20261122/axis-five-20261123/manual-grid-review-20261123/selected-default-grid-census.json.
The square-grid controls at 100 and 324 reported zero, and none of the nine cases had
a contact-classifier disagreement.

First improve the receipts. A rejected reconstruction should keep a bounded list of
violated pair or wall constraints, their selected face normals and signed gaps, and
the reconstruction variant. A timed-out attempt should preserve the current stage,
the last completed stage, the snap set, and any incumbent and bound without treating
an incomplete run as a candidate. Reuse the existing exact row labels and the contact
sweep. Confirm that a fixture with a known violated row and a forced timeout produces
the expected diagnostics and that ordinary successful selection is identical.

Then run one controlled local repair at a time:

- Start with the two misaligned faces at 127 as a small control. Its existing
  0.5-degree solve reached the optimum of its fixed-contact model with no meaningful
  motion. Try freeing the affected component's contacts before raising the angle
  threshold. At 131, 24 of the affected faces are misaligned and five are offsets.
- At 290 and 291 all three angle runs used the same fixed model and tied the house.
  Offsets explain all 34 soft open faces in each. Use the retained translation screen
  as a seed for a limited component realignment with selected contacts allowed to
  change. Solve one first and check the adaptation on the other.
- At 232 and 259 all three angle thresholds selected the same snaps. Individual exact
  reconstructions violated relaxed rows. The already cleaner contracted poses finish
  about 1.787e-34 and 2.021e-34 above their respective exact bounds. Try a coupled
  center and rotation adjustment near binding pairs (3,11) and (22,26), or test a
  distinct contact basis. A fixed-angle rounding repair at 232 has already failed.
- At 305 the upstream solve timed out before polishing, and the grid timeout retained
  no stage. The 5-degree run is the distinct snap branch (three squares near 1.61
  degrees). Use the current witness to seed a local experiment once the diagnostics
  show which stage needs work.

The control is the currently selected, certified drawing at each count. Keep the
same or a smaller exact side, require both independent maintained routes to accept
the full placement, and apply the existing improvement rule to the measured drawing.
A time limit or a failed search with a restricted model does not settle feasibility.
Coordinate residual angle work with think-huum and manual review tooling with think-nijx.
