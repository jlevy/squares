---
type: is
id: is-01m0t9capk4djgs9r9d9vvrr84
title: Replay containment as well as pair rows after every cell solve
kind: bug
status: closed
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - focus-correctness
dependencies: []
parent_id: is-01m0t5kge66djjkegqeg2sfwjf
created_at: 2026-08-24T16:24:11.730Z
updated_at: 2026-08-24T16:34:33.977Z
closed_at: 2026-08-24T16:34:33.976Z
close_reason: Fixed in f933887. solve_cell now replays the complete original A_ub/b_ub residual vector after both the initial solve and the single bounded repair, retains the maximum row index and containment/pair kind, and rejects the synthetic n=1 upper-x wall violation as containment row 1. Full normal gate passed before the test-only fixture optimization; focused regressions and all static/schema checks passed afterward.
resolution: null
duplicate_of: null
---
D-169. solve_cell's post-check claimed to replay every imposed LP constraint but iterated only the pair-separation rows; 4n containment rows were unchecked. A HiGHS optimum outside a wall by more than LP_FEASIBLE_EPS could therefore be accepted as an optimal cell. Acceptance: compute residuals from the complete A_ub/b_ub system; retain the maximum row index and containment/pair kind; apply the same bounded one-row retry; reject a synthetic containment-row violation; independently screen resulting poses.
