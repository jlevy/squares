---
type: is
id: is-01m0qxpb7634zbzt638d239jks
title: Make canonical basin identity invariant, stable, and scalable
kind: bug
status: open
priority: 0
version: 6
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - pr-14
  - technical-error
dependencies:
  - type: blocks
    target: is-01m0qxpbheswp54a9p12640g1z
  - type: blocks
    target: is-01m0qxpc5jrdzfn205qfxfvg44
  - type: blocks
    target: is-01m0qxpd3pnhvjh5s55b2w5gq8
  - type: blocks
    target: is-01m0qxpefk4ge1r6mrab9rhbad
parent_id: is-01m0qxka8ebkztq7erex50vvr2
created_at: 2026-08-23T18:21:28.165Z
updated_at: 2026-08-23T18:52:23.219Z
---
Category: technical errors. The contact certificate is not invariant under container reflection because folded-angle classes are ranked by angle value; tolerance grouping is order-dependent; exact tuple identity splits geometrically equivalent packings at quantization boundaries; and exhaustive individualization becomes factorial on sparse symmetric graphs.

Acceptance: property tests cover all D4 images, every square permutation, boundary perturbations, circular angle wraparound, near-tolerance chains, and graph automorphisms for both keys. Identity is an explicit equivalence or ambiguity relation rather than exact equality of two hashes. The n <= 100 runtime is benchmarked under sparse worst cases and uses a graph-canonicalization algorithm with a declared complexity envelope. Reconcile with think-t1s9 and think-hhon.

## Notes

2026-08-23 stacked-review progress: the contact certificate is minimized across all eight D4 images, and the independent checker now asserts both geometric and contact keys across D4, relabelling, and a one-square quarter-turn. Remaining acceptance work includes order-independent circular angle clustering, ambiguity-aware identity, quantization-boundary handling, and replacing or bounding factorial graph canonicalization.
