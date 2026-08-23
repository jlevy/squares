---
type: is
id: is-01m0qxpbheswp54a9p12640g1z
title: Separate atlas observations from certified basins
kind: bug
status: open
priority: 0
version: 7
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
parent_id: is-01m0qxka8ebkztq7erex50vvr2
created_at: 2026-08-23T18:21:28.493Z
updated_at: 2026-08-23T19:50:07.198Z
---
Category: technical errors. Atlas.add currently counts non-converged quench endpoints as basins and local optima; accepts keys for the wrong n; merges incompatible quantization regimes; can double count the same shard; lacks schema-validated provenance; and discards first-seen order, so it cannot produce the discovery curve H-011 requires.

Acceptance: the append-only unit is a provenance-complete observation with run, engine, proposer distribution, quench definition, budget, validity and convergence tiers, pose archive, seed, first-seen order, and regime digest. Only independently checked converged observations may be promoted to basin representatives. Load, save, merge, and self-merge enforce n, schema, regime, nonnegative counts, shard identity, and idempotence. Discovery curves and censoring are derived reproducibly. Reconcile with think-eq6l, think-ogv7, and think-ugt1.

## Notes

2026-08-23 PR14-head reassessment: D-030 repairs the cold n=5 fixture, now six of six converged, but the new n=3 golden stores one non-converged stopping point among four proposals as a basin and the guard permits up to half the sample to be censored. D-032 showed the same missing boundary in the checker output: it originally printed four synthetic deduplication re-offers as census proposals. The line is fixed, but wrong-n adds, incompatible-regime merges, missing event order, shard double counting, and pose-free validity remain. The stack records per-basin converged frequency and verifies the pose matching the stored minimum side; the observation-versus-basin model is still open.
