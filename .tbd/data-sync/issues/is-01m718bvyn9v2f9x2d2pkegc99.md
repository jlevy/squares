---
type: is
id: is-01m718bvyn9v2f9x2d2pkegc99
title: "Import #939: Joost de Winter's s(199) <= 14.6146898532835806, T-282's arrangement re-solved to its exact local optimum (quintic root) plus the L of 27"
kind: task
status: in_progress
priority: 1
version: 4
delegate: bold-ritchie-l78
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-09T22:55:20.020Z
updated_at: 2026-11-09T23:10:55.417Z
started_at: 2026-11-09T22:55:23.747Z
---
#939 (JoostdeWinter, 2026-11-09T22:03:57Z): s(199) side 14.61468985328358057514628890087947061619 (rounded up), <1e-98 above the real root near 14.6147 of 62x^5 - 4426x^4 + 125017x^3 - 1746146x^2 + 12052670x - 32855154, claimed the local optimum of the arrangement (130-digit numerical solution; quintic identified numerically). Certificate: JoostdeWinter/square-packing @ 702c7af2 folder n199 (n199_witness.yaml center-basis rational; n199_exact.json; verify_exact.py). Construction: T-282's 172 arrangement (Daniel, Özden) re-optimized (core side 13.61468985328358..., 2.63e-12 below T-282) plus the same L of 27 as #938 (kenaznia-doga, 20:31Z, earlier). Gain over #938: ~2.63e-12, the same as Daniel's held KKT point below T-282 (think-wju3, 2.635e-12) -> RV-3 class (think-ruu2); but #938's own contraction margin is 0 (exact grid contacts), so the padding-share test needs care. Implied s(172) witness from the core (not claimed). AI assistance: Claude under the author's direction. Sequencing: after #938 (think-1goz) merges.

## Notes

2026-11-09 bold-ritchie-l78 (lane L78, phase 1), branch claude/bold-ritchie-xo28us-l78 from origin/main 200f2ebc1:

- Custody: JoostdeWinter/square-packing cloned to scratch (l78/src), HEAD = main = 702c7af2db04c9b69696455ee3d33883a2935e8a (committed 2026-11-09T21:54:59Z, 9 min before #939). n199/SHA256SUMS matches all 5 files. MIT LICENSE (added 9bf5d9be, 17 Oct). No source program run.
- Adapter finding: n199_witness.yaml is not a schema-valid Witness/v2 (no softschema block, no claim, a notes field, id W-n199-de-Winter-... with capitals), so witness-center-basis refuses it ("not a witness document"); n199_exact.json is [cx, cy, cos, sin] rows, a format no adapter reads. Phase 1 adds two adapters for the packet.
- Exact facts (scratch l78/out/facts.json): YAML and JSON state the same packing; side S = .../10^111, ceil 38 = the issue's print, ceil 16 = 14.6146898532835806, ceil 12 = 14.614689853284. Quintic irreducible over Q, 3 real roots (9.670, 14.6147, 19.065), exactly one in [13,16] and in [S-1e-98, S] (Sturm); S - r = 1.36146898533e-99 (exact enclosure), S above r.
- Construction: #939 == construction_checker.write_out(L step, its own 172 core at S - 1) exactly; the L is #938's L, square for square.
- Gaps: T-284(#938) - S = 2.634529e-12 = T-282 - core; T-127 - S = 2.88232e-3.
- Contraction (devtools.contraction_margin): #938 margin 0 and #939 margin 0 (pair 173/174, grid squares); core vs T-282: T-282 margin 2.533458e-12, gain 2.634529e-12, share 1.0399; core own margin 1.36e-99 (1 - lambda* ~ 1e-100), contracted core 1.12e-124 ABOVE r - 1 (consistent with the local-optimality claim). T-282 contracted is 1.0107e-13 above the core; both ceil12 13.614689853284.
- Identity: core vs T-282 one to one under the identity, 84 squares beyond 1e-6 (max 1.414e-4), none beyond 1e-3; 88 squares moved only 1e-13..1e-12. 16 of the 84 are the KKT solve's free squares (rattlers), moved (-1e-4,-1e-4) and turned 1e-4 rad.
- think-wju3: Daniel's held KKT side prints 13.614689853283580575146288900879470616189727302001757698814980269, equal to r - 1 in all 63 printed places; its certified side is 1.3615e-19 above #939's core. Regenerated the held solve from main's n-172.yaml: view-solved.yaml has the recorded blob d641e969.
