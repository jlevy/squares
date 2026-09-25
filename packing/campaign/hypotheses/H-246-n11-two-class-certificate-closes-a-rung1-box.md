---
title: H-246 — a two-class parent-core counting certificate closes the rung-1 box at 20 degrees
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-246
  kind: hypothesis
  claim: >-
    Every packing of eleven unit squares with six axis-parallel and five at one common
    tilt whose half-tangent lies in [0.1758, 0.1768] has side greater than U, shown by a
    two-class parent-core counting certificate, 6 Gamma_a + 5 Gamma_t > M, decided by
    this repository's native sweep.
  lane: proof
  derived_from: [X-046, X-045]
  criterion:
    shape: determination
    metric: >-
      The native sweep's exact verdict on a frozen two-class parent-core certificate for
      the half-tangent box [0.1758, 0.1768] at a rational target of at least U compared
      through U's isolating interval, with point and k-of-m atoms and Kleddamag-style
      adaptive rows whose window is the box
    direction: >-
      Confirm only when the native sweep certifies every row at or above its class charge
      with total budget strictly below the charge, and a Fable extra-high review accepts
      the two-class counting lemma. Stop the method, not the claim, when the mass stays
      above 11 after site column generation with two-of-three and three-of-five atoms; a
      seam refusal or timeout decides nothing. A verified packing in the box below U
      would kill the claim and would be reported as a counterexample candidate to H-112.
    threshold: U
  instrument: >-
    A two-class parent-core producer and certificate built on sqpack.fractional.classcert,
    the parent-core and threshold separators, and the native coverage sweep, to be built
    under BC-389
  instrument_ready: false
  regime: >-
    n=11; six squares at orientation 0, five at one common tilt with half-tangent in
    [0.1758, 0.1768]; exact rational certificate; side compared with the exact algebraic U
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: >-
    One to two days of Opus extra-high build and hours of CPU, with a Fable extra-high
    review of the two-class lemma
  prereqs: [think-nho8]
  replication: false
  registered: '2026-09-25'
  notes: >-
    R052's lesson carried to rung 1, from the Session 159 n11 assessment
    (docs/project/specs/active/plan-2026-09-25-after-r052-planning.md). Stromquist's
    fixed-orientation counting is tight at 3.8856 > U and exp-131's class counts decide
    exactly at 3877084/10^6; against it, exp-064 measured the shrink alone at 0.0089 of
    side, and the Session 159 probe of the existing class certificate refuted no one-degree
    band. A closed box needs no cell tree, which is the payoff; near Trump's tilt the
    ceiling is at most U, so that region still needs a tree. Related to idea row 239,
    which aims the same producer at angle sets away from Trump's rather than at a box.
---
# H-246: Closing a Rung-1 Box Without a Tree

Exp-234 showed that the rung-0 cell tree cannot close a rung-1 box at any practical cap,
because its per-node bound ignores every pair it has not branched on.
A counting certificate prices every pair at once.
This claim tests whether the two-class version of the parent-core architecture that
carried R052 closes one box away from Trump’s tilt, at $20°$, outright.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
