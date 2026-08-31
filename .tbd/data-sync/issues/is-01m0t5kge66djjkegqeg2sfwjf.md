---
type: is
id: is-01m0t5kge66djjkegqeg2sfwjf
title: Separate LP solver rejection from mathematical cell infeasibility
kind: bug
status: closed
priority: 0
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - focus-correctness
dependencies: []
parent_id: is-01m0t4phe1905yy2jk7czp1391
child_order_hints:
  - is-01m0t9capk4djgs9r9d9vvrr84
created_at: 2026-08-24T15:18:12.677Z
updated_at: 2026-08-24T16:34:34.597Z
closed_at: 2026-08-24T16:34:34.595Z
close_reason: Fixed in f933887. Cell outcomes are typed as optimal, infeasible, solver_failure, or postcheck_rejection with solver status, failing row, residual, repair, and actual call count. The retained n=3 failing cell replays exactly. A preregistered single-row/single-retry policy restored n=3, n=10, and n=11 controls without changing the 1e-10 acceptance screen. Independent sqpack.verify validation accepts the n=10 result at the proved side within 1.33e-15, all 45 pairs checked. D-165 remains separately open until a new BasinEvent derives and replays all-probes-accounted evidence.
resolution: null
duplicate_of: null
---
D-164. solve_cell currently returns one None outcome for mathematical infeasibility, HiGHS failure, and a successful LP whose returned point misses the post-check tolerance. A retained n=3 calibration witness shows an optimal solve with 1.19996e-10 worst residual being mislabeled re-read cell infeasible at a 1e-10 cutoff; raising only the internal cutoff to 2e-10 lets that start converge exactly to side 2. Acceptance: typed solve outcomes distinguish infeasible, solver failure, and post-check rejection; the n=3 fixture is retained; retry or repair policy is preregistered and independently screened; no solver-boundary rejection is described as mathematical infeasibility.

## Notes

2026-08-24 bounded diagnosis: exact n=3 seed-1 trace found HiGHS success at side 2.405678412790218 with worst returned residual 1.1999601312595587e-10. The 1e-10 post-check collapses this into None and the fixed-point layer calls it infeasible. A controlled run with only LP_FEASIBLE_EPS=2e-10 then reached side 2 with a clean free pass in 9.5s. This is diagnostic evidence, not authorization to loosen the tolerance; implement typed cell-solve outcomes first.
