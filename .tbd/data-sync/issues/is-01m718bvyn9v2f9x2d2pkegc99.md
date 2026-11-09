---
type: is
id: is-01m718bvyn9v2f9x2d2pkegc99
title: "Import #939: Joost de Winter's s(199) <= 14.6146898532835806, T-282's arrangement re-solved to its exact local optimum (quintic root) plus the L of 27"
kind: task
status: in_progress
priority: 1
version: 3
delegate: bold-ritchie-l78
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-09T22:55:20.020Z
updated_at: 2026-11-09T22:55:23.748Z
started_at: 2026-11-09T22:55:23.747Z
---
#939 (JoostdeWinter, 2026-11-09T22:03:57Z): s(199) side 14.61468985328358057514628890087947061619 (rounded up), <1e-98 above the real root near 14.6147 of 62x^5 - 4426x^4 + 125017x^3 - 1746146x^2 + 12052670x - 32855154, claimed the local optimum of the arrangement (130-digit numerical solution; quintic identified numerically). Certificate: JoostdeWinter/square-packing @ 702c7af2 folder n199 (n199_witness.yaml center-basis rational; n199_exact.json; verify_exact.py). Construction: T-282's 172 arrangement (Daniel, Özden) re-optimized (core side 13.61468985328358..., 2.63e-12 below T-282) plus the same L of 27 as #938 (kenaznia-doga, 20:31Z, earlier). Gain over #938: ~2.63e-12, the same as Daniel's held KKT point below T-282 (think-wju3, 2.635e-12) -> RV-3 class (think-ruu2); but #938's own contraction margin is 0 (exact grid contacts), so the padding-share test needs care. Implied s(172) witness from the core (not claimed). AI assistance: Claude under the author's direction. Sequencing: after #938 (think-1goz) merges.
