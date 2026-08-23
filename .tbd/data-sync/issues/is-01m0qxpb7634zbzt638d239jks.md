---
type: is
id: is-01m0qxpb7634zbzt638d239jks
title: Make canonical basin identity invariant, stable, and scalable
kind: bug
status: open
priority: 0
version: 13
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - pr-14
  - technical-error
  - focus-correctness
dependencies:
  - type: blocks
    target: is-01m0qxpbheswp54a9p12640g1z
  - type: blocks
    target: is-01m0qxpc5jrdzfn205qfxfvg44
  - type: blocks
    target: is-01m0qxpd3pnhvjh5s55b2w5gq8
  - type: blocks
    target: is-01m0qxpefk4ge1r6mrab9rhbad
parent_id: is-01m0r7q3f92dgx66d30wwrasbn
child_order_hints:
  - is-01m0r50mrppgcvsp2ewrac0x6z
  - is-01m0r516kvkaaa5bbf9nm948qa
created_at: 2026-08-23T18:21:28.165Z
updated_at: 2026-08-23T21:17:48.396Z
---
Category: technical errors. The contact certificate is not invariant under container reflection because folded-angle classes are ranked by angle value; tolerance grouping is order-dependent; exact tuple identity splits geometrically equivalent packings at quantization boundaries; and exhaustive individualization becomes factorial on sparse symmetric graphs.

Acceptance: property tests cover all D4 images, every square permutation, boundary perturbations, circular angle wraparound, near-tolerance chains, and graph automorphisms for both keys. Identity is an explicit equivalence or ambiguity relation rather than exact equality of two hashes. The n <= 100 runtime is benchmarked under sparse worst cases and uses a graph-canonicalization algorithm with a declared complexity envelope. Reconcile with think-t1s9 and think-hhon.

## Notes

2026-08-23 merged-state reconciliation: PR #14 fixed D4 reflection and the angle seam, while D-034 exposed a separate isolation failure. The exact n=3 side-2 sliding family proves the current two-hash atlas splits one connected terminal component. At n=5, two rows share side/contact descriptors but remain an unresolved connectivity question; the merged branch's five-dimensional claim was not rank-certified. think-1s0h measures fixed-cell and full-Jacobian nullity/connectivity; child think-0yo9 defines component identity; child think-3szr calibrates numerical ambiguity. Remaining original work is order-independent circular clustering, quantization-boundary handling, and scalable canonical labeling.
