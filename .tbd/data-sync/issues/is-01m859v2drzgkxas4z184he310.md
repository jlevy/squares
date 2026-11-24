---
type: is
id: is-01m859v2drzgkxas4z184he310
title: Diagnose failed grid-slack rows and test localized grid repairs
kind: task
status: in_progress
priority: 2
version: 10
delegate: codex-exact-grid-repair-1123
labels:
  - regularization
  - validation
dependencies: []
child_order_hints:
  - is-01m85bk7fexs4he29m1qhwwy17
  - is-01m85bmw6rhtgxkj2vbngwkzf6
  - is-01m85f8bbsspr36sk83c2p6agb
hold: null
hold_until: null
created_at: 2026-11-23T22:53:46.287Z
updated_at: 2026-11-24T01:32:32.134Z
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

## Notes

Astra review B approved PR #1107 at b237acb437. The two-square 127 stack keeps T-341's exact side and passes both 8001-pair routes and row 10. Uneven aligned 2 to 0, house and stage totals 259/293 to 266/300, no individual losses. At 259 the fixed-tilt fully anchored variant had 21 negative selected rows. All-axis exact verification confirmed overlap 227–228. The overlap row depends on four pair equations (228–229, 200–201, 200–231, 201–227) and fixed y on 229 and 231. Swapping 200–231 out for 227–228 closes the overlap exactly, opens the outgoing gap, moves four centers and leaves 20 negative selected rows with no new ones. A 12-swap screen found no further monotone move within eight changed centers. Other swaps reducing the count to 14 propagated to 39–45 centers. Next compare bounded coupled components or alternative true separating axes on remaining 259 rows. At 232 and 305 float placement finished and the first exact settling variant reached the wall limit. Use small component reconstruction with anchored boundaries for the next pass. All raw trials are retained under grid-repair-20261123 in the external drawing audit evidence. No 232, 259 or 305 view admitted.

131 control: placement in 1.22 s, first global settle timed out. Moving 23, 35, 40 only, anchored-first held 128 exact source poses, left six candidate coordinates and nine selected boundary rows, and settled in 0.047 s. Both exact routes accepted all 8,515 pairs at the registered exact side. It ties the current selected drawing on all seven measures. A separate screen targeted 15 diagnosed open-face pairs on the selected view. Two valid one-square moves of 65 (to 64/66) reduce uneven 21 to 19, but lose an existing house and stage contact for 72. Holding the contact by translating 72 merely transfers the regression to 86, then 79. Continuing the contact-chain translation encounters exact overlaps 79–80 or 36–48. Refuse both uniform-translation branches. Next targeted model should allow coupled nonuniform movements at most one small patch at a time, keep exact exterior anchors and include current neighbor contact floors. Raw evidence in n131-targeted-*, n131-contact-chain-trials.json and replay-131-anchored-first, under the same external grid-repair-20261123 directory. No 131 replacement admitted.

Follow-up narrow screen: 232 had 7 geometrically clear one-square snaps. The three misalignment moves lost contacts; of four slack closures, only 87→137 preserved all contact counts and its full exact replay exceeded the guarded wall before a verdict, so no candidate admitted. At 305 the exact T-342 source has 35 literal axis rotations and 178 nonzero rotations within the deep near-axis screen (component below 1e-60). Eight distinct visible soft pairs gave 16 directional candidate snaps to the anchor's native exact basis and each had a physical overlap with an adjacent square. Meaningful next local patch: 87→136 is blocked by 89, 89→137 by 104, and 104→139 by 103; allow coupled placements, check both exact routes and comparison with current public house. At 259 the exact verified combined 118→114, 99→101, 104→108 repair is in draft PR #1108 and child think-q3yr. Light aligned 23→19, house full sides 545→551, uneven 65 and stage 727 hold. The parent stays active for residual 131 / 232 / 259 / 305 and broader corpus work. Retained candidate and screen receipts are in grid-repair-20261123.

Published and independently checked on 23 November Pacific. #1107 merged e2ec6b234f, green exact-head and full Pages audit 45299275264, followed by #1108 at b5c0bf6020 with green exact-head checks. Direct live SVGs and attribution match both certified renders at b5c0bf6020; live evidence under grid-repair-20261123/live-{127,259}-verification.json. The 259 exact base replays from the official house by semantic geometry. Same exact sides and no contact losses. The 127 completed diagnostics and atlas-consumer children and 259 adoption child are closed. Keep this parent open for residual grid work.
