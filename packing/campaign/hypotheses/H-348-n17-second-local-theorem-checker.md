---
title: H-348 — a second, LP-free checker reproduces the local theorem's certificates and refuses mutants
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-348
  kind: hypothesis
  claim: >-
    An independent checker of the local family theorem's certificate data (the 52-row
    roster, the 45 coordinate lifts, the cells of the slider box, the dyadic duals, the
    curvature constants and the radius vector), written without importing
    devtools/check_n17_local_minimum.py or devtools/check_n17_local_radius.py and using
    only exact rational linear algebra and the ratio inequality with no LP, reproduces
    the worst ratios 0.925818092269 on B_W, 0.925931049178 on B_W', and 0.999316555505
    and 0.999368209930 for the 1/1216 vector on B_c, and refuses every one of at least
    20 doctored certificates (a dual sign flipped, a dual residual perturbed, a
    curvature constant lowered, a radius enlarged, a row dropped, a lift mislabelled, a
    cell vertex moved outside the box) with a named reason.
  lane: proof
  derived_from: [X-052]
  criterion:
    shape: determination
    metric: >-
      The four worst ratios and the per-cell counts (93, 93, 109, 117) from the second
      checker; the refusal verdict and reason on each mutant; agreement of every
      per-coordinate ratio with the standing instrument to the exact rational.
    direction: >-
      Confirm when all four ratios and cell counts agree exactly and 20 of 20 mutants
      are refused. A disagreement names a defect in one checker and refutes the claim
      until it is found; an accepted mutant refutes it outright.
    threshold: 4 of 4 ratios exact; 20 of 20 mutants refused.
  instrument: >-
    Unbuilt: a standalone checker in another language or a separately written Python
    module sharing no code with the standing instruments, reading the exp-244 and
    exp-248 certificates and the local-radius review's vector; a mutation generator in
    the pattern of the kernel verifier's suite.
  instrument_ready: false
  regime: >-
    n = 17; the retained certificates of exp-244, exp-248 run-002 and the 1/1216
    composition; exact rational arithmetic; the hand lemmas taken as given.
  instance: {axis: n, point: 17}
  priority: 3
  cost_estimate: 20 to 30 agent-hours to build and review; seconds to run.
  prereqs: [H-261, H-268, H-340]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-052's direction 6, the local half of two-verifier parity (H-335 covers the kernel
    format). The local theorem's certificate is a few hundred kilobytes of rational
    data, its check is linear algebra and one inequality, and the HiGHS proposals are
    never trusted; so a second implementation is cheap and the foolproof package should
    have it. The local-side review of 9 October replayed the standing instrument and
    re-derived the curvature bound by hand; this makes that second derivation a program.
---
# H-348: Two Checkers for the Local Half

**Mechanism.** The local theorem is data plus a small checker: rank, residuals,
nonnegativity, Taylor margins and the ratio $M_j / (2(r_j - \varepsilon_j R)) < 1$ at
every cell vertex. A second implementation that agrees on every exact value, and refuses
what the first refuses, reduces the trust in either to the trust in the recipe’s six
hand lemmas.

**Falsifier.** A disagreement on any ratio or an accepted mutant.

**Expected information.** Whether the local half rests on two implementations or one.

**Limits.** The hand lemmas and the curvature formula are shared premises; H-333 is
where they stop being hand lemmas.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
