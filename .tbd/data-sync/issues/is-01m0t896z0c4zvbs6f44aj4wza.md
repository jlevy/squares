---
type: is
id: is-01m0t896z0c4zvbs6f44aj4wza
title: Recognize finite equal-objective adjacent-cell closures
kind: bug
status: closed
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - focus-correctness
dependencies: []
parent_id: is-01m0t4phe1905yy2jk7czp1391
created_at: 2026-08-24T16:05:01.023Z
updated_at: 2026-08-24T16:13:40.676Z
closed_at: 2026-08-24T16:13:40.675Z
close_reason: "Fixed in a6fc8e0. Repeated fixed-angle cells now trigger a bounded row-choice closure with a hard 64-cell cap; every cell must solve, all rereads must remain inside the closed set, and the objective spread must stay within LP_FEASIBLE_EPS. The largest-side representative is retained and labeled adjacent cell closure, with no global-optimum claim. The real n=10 D-029 control exercises 2/4/8-cell closures and reaches the proved side; equal-objective and unequal-objective mutation controls pass. Normal gate: all 30 steps pass in 36s; atlas improves to 5/6 converged. D-165 remains open because 16 other angle probes still have no typed outcome."
resolution: null
duplicate_of: null
---
A fixed-angle n=10 control reaches a two-cycle because two pair rows swap their separating-axis owners. Exact finite enumeration of the two differing rows gives four adjacent cells; all solve successfully, their objectives agree within 4.44e-16, and every reread remains inside the four-cell closure. The current solver labels this conservative degeneracy an unsettled cell cycle. Acceptance: enumerate the complete product of differing row alternatives under a hard cap; require every cell solve to pass, all objectives to agree within the declared LP screen, and every reread to remain inside the enumerated closure; return a distinct adjacent-cell-closure settlement reason; retain n=10 and mutation controls; never call this a global fixed-angle or basin optimum.
