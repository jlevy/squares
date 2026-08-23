---
type: is
id: is-01m0qxpd3pnhvjh5s55b2w5gq8
title: Add event-level measurement and a statistical census contract
kind: feature
status: open
priority: 1
version: 5
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - pr-14
  - omission
dependencies:
  - type: blocks
    target: is-01m0qxpe517zsenj91xmydctg5
  - type: blocks
    target: is-01m0qxpefk4ge1r6mrab9rhbad
  - type: blocks
    target: is-01m0qxpf8pe8qze02qp1nrz58x
  - type: blocks
    target: is-01m0qxpgm5e4gx92d9f1r4bqgj
parent_id: is-01m0qxka8ebkztq7erex50vvr2
created_at: 2026-08-23T18:21:30.101Z
updated_at: 2026-08-23T18:21:57.939Z
---
Category: key omissions. Current artifacts retain only winners or aggregate basin counts. They cannot distinguish a grid fallback from a trajectory trapped in the grid basin, measure pair tests exactly, reconstruct discovery order, estimate unseen basins, or support uncertainty claims.

Acceptance: proposer, quench, validity, promotion and atlas events use a versioned append-only schema with exact pair-test and proposal counters, censored and failed outcomes, full poses or content-addressed references, regime hashes and timestamps. H-011 uses independent replicates and a preregistered coverage estimator such as Good-Turing or Chao with confidence intervals; a visual plateau alone is never called completeness. H-012 includes n = 11 explicitly. Reconcile with think-b4jc, think-w6on, think-ogv7, and think-19gf.
