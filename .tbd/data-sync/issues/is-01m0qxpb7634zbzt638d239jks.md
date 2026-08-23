---
type: is
id: is-01m0qxpb7634zbzt638d239jks
title: Make canonical basin identity invariant, stable, and scalable
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
    target: is-01m0qxpbheswp54a9p12640g1z
  - type: blocks
    target: is-01m0qxpc5jrdzfn205qfxfvg44
  - type: blocks
    target: is-01m0qxpd3pnhvjh5s55b2w5gq8
  - type: blocks
    target: is-01m0qxpefk4ge1r6mrab9rhbad
parent_id: is-01m0qxka8ebkztq7erex50vvr2
created_at: 2026-08-23T18:21:28.165Z
updated_at: 2026-08-23T20:22:28.299Z
---
Category: technical errors. The contact certificate is not invariant under container reflection because folded-angle classes are ranked by angle value; tolerance grouping is order-dependent; exact tuple identity splits geometrically equivalent packings at quantization boundaries; and exhaustive individualization becomes factorial on sparse symmetric graphs.

Acceptance: property tests cover all D4 images, every square permutation, boundary perturbations, circular angle wraparound, near-tolerance chains, and graph automorphisms for both keys. Identity is an explicit equivalence or ambiguity relation rather than exact equality of two hashes. The n <= 100 runtime is benchmarked under sparse worst cases and uses a graph-canonicalization algorithm with a declared complexity envelope. Reconcile with think-t1s9 and think-hhon.

## Notes

2026-08-23, from PR #14 branch claude/packing-overnight-strategy-queue: a distinct root cause was measured that this bead's framing would send someone past.

This bead attributes basin splitting to quantization boundaries and to identity being exact equality of two hashes. Both are real. But the splitting measured at n = 5 is NEITHER: the angle steps of the two split rows are identical ([0, 0, 0, 785398, 785398]) and the positions differ by 0.06 in x and 0.21 in y -- real distance, not a straddled cell. The configuration is NOT RIGID: 11 contact constraints against 16 degrees of freedom, so the optimum is a five-dimensional family and the two rows are two genuine members of it.

So tightening or loosening the quantum cannot fix that case, and an ambiguity-aware identity relation only helps if it knows the optimum is flat. Track that as think-1s0h and D-034; do these two together, because a quantization-boundary fix validated against a flat optimum will look like it works and will not.

Also relevant to this bead's own acceptance list: the contact-certificate reflection-invariance fix on origin/codex/pr14-square-packing-review (commit c170743) is a real defect fix in code this branch also touched, and the two branches conflict. The n = 5 split rows have IDENTICAL contact certificates, so reflection invariance is not what splits them -- the two findings are independent and both need to land.
