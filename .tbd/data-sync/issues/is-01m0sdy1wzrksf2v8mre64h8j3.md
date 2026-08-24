---
type: is
id: is-01m0sdy1wzrksf2v8mre64h8j3
title: Separate Trump linearized cones from true Bouligand motions
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/campaign/hypotheses/H-026-trump-first-order-rigidity.md
labels:
  - packing
  - focus-soundness
dependencies: []
parent_id: is-01m0sd9662q9t69eyaxcxgx2j3
created_at: 2026-08-24T08:24:32.404Z
updated_at: 2026-08-24T08:48:53.644Z
closed_at: 2026-08-24T08:48:53.630Z
close_reason: Corrected every H-026 claim surface to branchwise one-sided linearized cones in open real angle charts; nonzero vectors now route to continuation, zero coverage carries only the separately stated finite-branch implication. Logged as D-136 and bound the scope into exact replay.
resolution: null
duplicate_of: null
---
H-026 and its claimed exp-013 used branchwise tangent/Bouligand language symmetrically, but the derived one-sided linearized cones are outer approximations to the true tangent. A zero union proves the true tangent is zero; a nonzero linearized vector only refutes the linearized-cone claim and requires nonlinear continuation before it is called a feasible motion. Correct the hypothesis, stop rules, checker output, and review language before execution; state that orientations use open real charts rather than folded angle representatives; record the error in defects.yaml.
