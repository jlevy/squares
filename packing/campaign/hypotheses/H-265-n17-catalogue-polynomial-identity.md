---
title: H-265 — the certified n17 chart endpoint is a root of the catalogue's degree-18 polynomial
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-265
  kind: hypothesis
  claim: >-
    The side S* of the H255 chart root is a root of the degree-18 polynomial recorded as
    the catalogue's minimal polynomial in packing/frontier/n-017.md, and that polynomial
    is irreducible over Q, so S* equals the catalogue's reported side and has algebraic
    degree 18.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: >-
      The exact resultant eliminating b from the two H255 chart polynomials, the
      substitution S = (6 + 4t)/(1 + 2t - t^2), exact factorization over Q, exact root
      isolation identifying the factor that vanishes inside the H255 box, and an
      irreducibility certificate for the catalogue polynomial
    direction: >-
      Confirm only if the vanishing factor equals the catalogue polynomial up to a
      rational unit, the polynomial is certified irreducible, and an independent check
      (a second computer-algebra route or exact evaluation) agrees. A different factor
      refutes the identification without affecting the admitted rational ceiling.
    threshold: Exact polynomial equality; no tolerance
  instrument: >-
    A small identification tool to be built under BC-409, using exact polynomial
    arithmetic (sympy.polys or python-flint) with an independent recheck
  instrument_ready: true
  regime: The unchanged H255 polynomials and box; the polynomial as recorded in n-017.md
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: One short build slice; seconds to minutes of algebra
  prereqs: [H-255, think-e6y1]
  replication: false
  registered: '2026-10-01'
  notes: >-
    From the PR 265 route review. Closes the identification blocker recorded in
    n-017.md and the morning report; it is not a prerequisite for the optimality proof
    and does not change the admitted rational ceiling.
---
# H-265: Identity With the Catalogue Polynomial

The certified chart endpoint and the catalogue’s degree-18 side agree to every printed
digit, but no one has shown they are the same algebraic number.
An exact resultant settles it cheaply.

## Outcome

*Added 2026-10-02 by Session 167.*
[exp-245](../series/series-000-smoke-and-calibration/experiments/exp-245-h265-n17-catalogue-polynomial.md)
accepts this hypothesis after an independent review: the certified side is a root of the
catalogue’s degree-18 polynomial, which is irreducible over $\mathbb{Q}$.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
