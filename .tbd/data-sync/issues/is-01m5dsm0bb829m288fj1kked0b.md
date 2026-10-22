---
type: is
id: is-01m5dsm0bb829m288fj1kked0b
title: "Owner review at 260: admit a strong view of T-223 (row 7) or keep the axis tool's view drawn"
kind: task
status: closed
priority: 2
version: 3
delegate: coord-intake-1021b
labels:
  - regularization
  - owner-decision
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-20T23:16:21.987Z
updated_at: 2026-10-22T04:29:20.638Z
started_at: 2026-10-22T04:29:19.848Z
closed_at: 2026-10-22T04:29:20.638Z
close_reason: "Moot after #718 (merged 2026-10-22T04:28:54Z as 7359fa8b6): T-225 replaced T-223 as the house at 260, so the row-7 choice among strong views of T-223 no longer arises; 260's new witness is settled in #718 (#718 review A7; default_drawings.py on main no longer names this bead)."
resolution: null
duplicate_of: null
---
Owner review owed at n = 260 since the house best packing adoption of 20 October 2026 (issue 678, T-223; stage 4 and adoption under think-xu4d, the PR stacked on #701). The house best packing is Francisco Couzo's exact rational certificate, side 146417594016514621500994169/8796093022208000000000000.

The strong generators ran on its witness (run directories adopt-2026-10-20-n204-260-*), and `regularize_select` admits no view at 260; every one goes to row 7, the owner's review, because some squares' contact counts fall while no total does:
- Evan Daniel's same-side view: 2 light, 16 uneven, 0 near-axis, 2 classes, house sides 780; 29 per-square counts fall.
- grid-slack at 0.5, 1 and 5 degrees: 2 / 28 / 0, 2 classes, house sides 769; 2 per-square counts fall.
- The drawn axis-tool view: 5 / 36 / 0, 2 classes, house sides 736.
His solved view lies 2.51e-11 below the witness's side: a register candidate (policy row 3), not drawn, for the owner.

Evidence: packing/cases/regularized_drawings/think-xu4d-2026-10-20/ (the selection's report and table beside the runs' receipt, blocks and reports), and `default_drawings.SETTLED[260]`, which names this bead in `owed`.

Done when the owner's answer is recorded. If a view is admitted, record it in packing/atlas/known-best/regularized/reviews.yaml as #657 did for 211, lay the view and run `default_drawings --update`. Either way, clear `owed` on SETTLED[260] (or take 260 off SETTLED once a strong view is drawn), so that `check_bead_tree` no longer holds this bead open.
