---
type: is
id: is-01m0qxpg0nryz3nwhedeqgwm1g
title: Certify and structurally constrain the n = 11 optimum
kind: task
status: open
priority: 1
version: 6
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - pr-14
  - open-question
  - focus-insight
dependencies: []
parent_id: is-01m0r7q4h688g8gx54wk0vmrhp
child_order_hints:
  - is-01m0sd9662q9t69eyaxcxgx2j3
  - is-01m0sg2venckvcs3q1cr5v1qzc
created_at: 2026-08-23T18:21:33.076Z
updated_at: 2026-08-24T09:02:15.750Z
---
Category: tractable open questions. Separate three questions currently blurred together: exact verification of Trump’s construction, local optimality or rigidity of its active set, and global optimality among all packings. Build interval KKT or nonsmooth directional certification for the known cell, then prove or computationally certify structural necessities for any packing below selected side thresholds.

Acceptance: the exact upper-bound witness is generated from the promotion pipeline; local optimality has a machine-checkable active-set and interval certificate; restricted global results state their orientation, contact or neighborhood assumptions precisely; and searches outside the Trump neighborhood use the same observation and budget contracts. Reconcile with think-n39a, think-i50h, and think-c4xs.

## Notes

Exp-013 confirms H-026 at commit faba023: 11 wall incidences expand to 20 rows, 14 contacts yield 24 raw SAT features, 512 nonlinear selections reduce to 128 derivative-distinct 42-by-33 exact matrices, and every matrix has rank 33 plus a strictly positive Q(u) left-kernel stress. Separate replay validates all 128 with zero unresolved branches. A finite-branch subsequence lemma proves qualitative local isolation and strict local side optimality modulo finite symmetry. This does not prove global optimality or give a radius. think-kfb4 owns the quantitative radius, minimal-support, and side-perturbation successor; H-034 tests the pure ten-point fractional ceiling; H-036 asks for a robust 0/45-degree neighborhood theorem.
