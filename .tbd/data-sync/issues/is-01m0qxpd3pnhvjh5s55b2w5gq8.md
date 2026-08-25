---
type: is
id: is-01m0qxpd3pnhvjh5s55b2w5gq8
title: Add event-level measurement and a statistical census contract
kind: feature
status: open
priority: 1
version: 9
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - pr-14
  - omission
  - focus-process
dependencies:
  - type: blocks
    target: is-01m0qxpe517zsenj91xmydctg5
  - type: blocks
    target: is-01m0qxpefk4ge1r6mrab9rhbad
  - type: blocks
    target: is-01m0qxpf8pe8qze02qp1nrz58x
  - type: blocks
    target: is-01m0qxpgm5e4gx92d9f1r4bqgj
  - type: blocks
    target: is-01m0r7sk41gsj2yjh80tx6324h
parent_id: is-01m0r7q3zk8x6cg4e30d149698
child_order_hints:
  - is-01m0r51fbqgm0y4tb2d09fcb82
created_at: 2026-08-23T18:21:30.101Z
updated_at: 2026-08-25T11:16:45.852Z
---
Category: key omissions. Current artifacts retain only winners or aggregate basin counts. They cannot distinguish a grid fallback from a trajectory trapped in the grid basin, measure pair tests exactly, reconstruct discovery order, estimate unseen basins, or support uncertainty claims.

Acceptance: proposer, quench, validity, promotion and atlas events use a versioned append-only schema with exact pair-test and proposal counters, censored and failed outcomes, full poses or content-addressed references, regime hashes and timestamps. H-011 uses independent replicates and a preregistered coverage estimator such as Good-Turing or Chao with confidence intervals; a visual plateau alone is never called completeness. H-012 includes n = 11 explicitly. Reconcile with think-b4jc, think-w6on, think-ogv7, and think-19gf.

## Notes

Session-011 order 7 remeasured the D-054 budget edge at a9330d6: --steps 7 --budget-moves 8 completes two full anneals and reports 14 moves, confirming the documented overshoot. The new exact meter reports 142 pair tests, so measurement is repaired but enforcement and trajectory/event retention remain outstanding. Zero-budget reports the intended final-scan count C(5,2)=10. D-283/think-dprg separately owns steps=0 nontermination.
