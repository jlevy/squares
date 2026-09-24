---
title: H-236 — Trump is globally optimal at its own angle (rung 0 of the H-112 ladder)
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-236
  kind: hypothesis
  claim: >-
    In the family of six unit squares at actual orientation 0 and five sharing one
    orientation theta modulo pi/2, with centres and contacts free, every packing whose
    half-tangent t = tan(theta/2) lies in [t* - 10^-6, t* + 10^-6], t* Trump's tilt, has
    container side at least U, and every such packing at side U lies in the
    Z/4 x S6 x S5 orbit of Trump's pose.
  lane: proof
  derived_from: [X-046, X-045]
  criterion:
    shape: determination
    metric: >-
      A complete fixed-shape cell tree over the box, using rotational cores, whose
      every leaf carries an exact rational Farkas infeasibility vector or an exact dual
      bound strictly above U compared through U's isolating interval, or is
      Trump-degenerate and closed by the BC-240 local theorem with an explicit labelled
      matching
    direction: >-
      Confirm only when an independent reader that re-derives every leaf's cell
      constraints accepts the certificate, the n=5 positive control closes at
      2 + 1/sqrt 2 and the U + 10^-3 negative control does not close. Kill with a leaf
      whose exact bound is below U and which is not Trump-degenerate, verified as a
      feasible packing before it is called a counterexample. An unresolved leaf list at
      the declared node or wall cap is a bounded negative on the instrument.
    threshold: U
  instrument: >-
    packing/cases/trump11/fixed_angle_tree.py with its independent reader
    fixed_angle_tree_check.py: HiGHS float proposals through scipy, every decision in
    exact Fraction arithmetic; frozen by git hash-object before the n=11 run, with a
    resume-only amendment; producer and reader share cases/trump11/packing.py and
    sqpack.field.NumberField
  instrument_ready: false
  regime: >-
    n=11; six squares at orientation 0, five at one common orientation in the stated
    half-tangent box; exact rational leaf certificates; side compared with the exact
    algebraic U
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: >-
    Four to five hours to build and control the driver and reader, then at most two
    hours or 10^6 nodes on the box
  prereqs: [think-nbij]
  replication: false
  registered: '2026-09-23'
  notes: >-
    Rung 0 of the H-112 ladder in X-046. It is the first optimality statement with an
    equality case for a family containing Trump's packing (Stromquist 2003's 0/45-degree
    bound is an earlier restricted-orientation statement), and its node count prices
    every later rung.
    Outcome note (2026-09-24): confirmed by exp-232; after the Fable max W2 review,
    registered as T-035, the machine-verified reduction to the BC-240 ball, and T-036,
    the composed theorem.
---
# H-236: Trump Is Globally Optimal at Its Own Angle

X-046 found no provable dimension-reduction lemma that is not the conjecture itself, and
recommended a ladder of restricted-family theorems instead.
This is its first rung: freeze the angles at Trump’s, up to a box of half-width
$10^{-6}$ in the half-tangent, and prove that no placement of centres does better than
$U$. Rotational cores make the box relaxation exact-shape, so every leaf is a rational
LP certificate; only the cells that contain a Trump image need the local theorem.

The measurement that matters as much as the verdict is the node count, which decides
whether H-112 is a one-week program or an infeasible one.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
