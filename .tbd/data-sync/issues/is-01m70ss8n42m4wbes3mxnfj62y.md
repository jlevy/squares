---
type: is
id: is-01m70ss8n42m4wbes3mxnfj62y
title: Register or settle Evan Daniel's certified solves below T-282 (172) and T-283 (270), held at row 3 pending RV-3; 270's held near-axis tilts
kind: task
status: open
priority: 3
version: 3
labels:
  - validation
  - regularization
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: blocked
hold_until: null
created_at: 2026-11-09T18:40:30.371Z
updated_at: 2026-11-09T19:56:37.506Z
---
The adoption of 9 November 2026 (think-he66, PR #937) ran both strong generators on T-282's (172) and T-283's (270) new witnesses. Evan Daniel's regularizer solved each witness to a certified KKT point below its side, by 2.635e-12 at 172 and 3.253e-12 at 270, 1.04 and 1.01 times each certificate's own uniform-contraction margin (2.533e-12 and 3.212e-12), and the selection held each at policy row 3 as a register candidate: register and review first, never admitted by the layer.

Both counts are drawn regularized: Evan Daniel's view at 172, and grid-slack's 0.5-degree view at 270 (re-run after the senior review of #937 found the first runs' row 7 measured against T-224's lapsed view). The axis tool refuses 270's witness (slide limits pass 4,300 digits, refusal slide-digits), so compare_evand_regularization's refused-tilts tally reads the axis record at 270, whose witness holds 13 near-axis squares 1.05e-12 to 2.38e-7 degrees off the axis; KNOWN_TILTS holds them under this bead (OWNER_270).

## Validation
- Claim: the two solved views as smaller rational packings at 172 and 270, below T-282 and T-283 by 1.04 and 1.01 times each certificate's padding.
- Run: register them as results (stage 3) and review them (stage 4); the runs are retained in packing/cases/regularized_drawings/think-he66-2026-11-09/.
- Cost: minutes (a replay of two views on both routes), plus a review lane.
- Budget status: gated on decision: whether a solve at a certificate's own padding is a new result is the owner's open question (RV-3; think-ruu2, think-ikku).
- Depends on: think-ruu2, think-ikku.
- Done when: the views are registered and decided, or the owner rules them restatements; and the KNOWN_TILTS entries at 270 leave when the axis tool reads the witness or the house moves.
- Machine note: light.

## Notes

2026-11-09 coordinator: registering Daniel's certified solves below T-282 (2.635e-12; certificate margin 2.533e-12) and T-283 (3.253e-12; margin 3.212e-12) also waits on the owner's RV-3 answer, like think-5c9z for T-275..T-279.
blocked_on: think-ruu2, think-ikku
