---
type: is
id: is-01m0qxpbheswp54a9p12640g1z
title: Separate atlas observations from certified basins
kind: bug
status: open
priority: 0
version: 11
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - pr-14
  - technical-error
dependencies:
  - type: blocks
    target: is-01m0qxpc5jrdzfn205qfxfvg44
  - type: blocks
    target: is-01m0qxpd3pnhvjh5s55b2w5gq8
  - type: blocks
    target: is-01m0qxpe517zsenj91xmydctg5
  - type: blocks
    target: is-01m0qxpefk4ge1r6mrab9rhbad
  - type: blocks
    target: is-01m0r51fbqgm0y4tb2d09fcb82
parent_id: is-01m0qxka8ebkztq7erex50vvr2
child_order_hints:
  - is-01m0r50x1ms53tfamwwmc5qw2z
created_at: 2026-08-23T18:21:28.493Z
updated_at: 2026-08-23T20:45:33.118Z
---
Category: technical errors. Atlas.add currently counts non-converged quench endpoints as basins and local optima; accepts keys for the wrong n; merges incompatible quantization regimes; can double count the same shard; lacks schema-validated provenance; and discards first-seen order, so it cannot produce the discovery curve H-011 requires.

Acceptance: the append-only unit is a provenance-complete observation with run, engine, proposer distribution, quench definition, budget, validity and convergence tiers, pose archive, seed, first-seen order, and regime digest. Only independently checked converged observations may be promoted to basin representatives. Load, save, merge, and self-merge enforce n, schema, regime, nonnegative counts, shard identity, and idempotence. Discovery curves and censoring are derived reproducibly. Reconcile with think-eq6l, think-ogv7, and think-ugt1.

## Notes

2026-08-23 merged-state reconciliation: D-030 fixed one cold-quench failure, but non-converged observations are still stored and the exact n=3 family proves endpoint rows are not component counts. D-037, not merged D-035, is the review-found historical checker summary that mixed census proposals with synthetic re-offers. Wrong-n adds, regime merges, event order, shard identity, pose-free validity, terminal-component promotion, and ambiguity bounds remain open. Child think-aans owns classification of unrecognised endpoints.
