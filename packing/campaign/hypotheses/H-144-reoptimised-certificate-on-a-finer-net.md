---
title: H-144 — a re-optimised point certificate on a finer net approaches the cap
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-144
  kind: hypothesis
  claim: >-
    The covering LP re-optimised on a net of 720 or more directions at the sharpened
    shrink limit B_max(N), with site generation and row generation rather than the frozen
    T-018 atoms, yields a certificate whose T-022 dilation supremum exceeds 3.8200 --
    within about 0.006 of the point method's own cap of 3.8288 B_max(N), which the exact
    depth-one family at 191/50 fixes for every net containing its six directions.
  lane: proof
  derived_from: [X-023]
  strategy_refs: ['proof:15', 'proof:22']
  criterion:
    shape: determination
    metric: >-
      the T-022 dilation supremum L sqrt(1 + D_N^2) / (B (1 + D_N)) of a frozen
      certificate at (L, B, N) with B at most B_max(N) and N at least 720
    direction: >-
      Confirm with such a certificate decided from its frozen bytes by
      devtools.decide_certificate with both routes agreeing -- the exact event-cell sweep
      and the interval branch and bound -- whose dilation supremum exceeds 3.82. Refute
      with a converged restricted covering value at or above eleven on a site set that has
      been separated to exact depth at that (L, B, N), which is an exact ceiling family
      there and closes the side for the point method the way 191/50 is closed. An
      unconverged LP value bounds nothing and settles neither direction.
    threshold: 3.82
  instrument: >-
    devtools.run_fractional_colgen (--direction-steps) and devtools.run_fractional_cutting
    (--steps) generate sites and rows at any net; devtools.measure_net_refinement supplies
    B_max(N), the crossing shrink and the dilation supremum as exact rationals and surds;
    devtools.decide_certificate is the two-route retention gate on the frozen result.
  instrument_ready: true
  regime: >-
    n = 11, sides at and above 381/100, nets of 720, 1440 and 2880 steps of the retained
    angle limit 207107/500000, shrink at or below the sharpened B_max(N); D4-symmetric
    point atoms with nonnegative weights
  instance: {axis: n, point: 11}
  sweep:
    axis: direction_steps
    points: [720, 1440, 2880]
  priority: 1
  cost_estimate: >-
    one session of four to six hours; a 720-direction row solve costs several times the
    181-direction one and the sweep is the dominant term
  prereqs:
  - the retention packet for the frozen atoms at the crossing shrink on the finer net
  replication: true
  registered: '2026-09-09'
  notes: >-
    The frozen 1121 atoms already reach a dilation supremum of 3.81660950 at N = 1440
    without any re-optimisation, against T-022's 3.810025723614703 on the retained
    181-direction net; the claim is that re-optimising the measure on the finer net is
    worth another 0.0034 or more. What bounds the whole family from above is lane T's
    sandwich lemma: no one-body core choice -- octagon kernels, parent-feasible centre
    domains, non-concentric or open cores -- passes unit side 3.8288, so the cap this
    claim approaches is the cap on every core-choice idea at once and not merely on the
    retained construction. The measured reading that motivates it is that a finer net
    costs no coverage on the frozen atoms: with the sharpened shrink of each net the
    least mass stays 4001/4000 at every net up to 2880 steps.
---
# H-144 — What the Finer Net Is Worth Once the Measure Moves

The shrink is a tax of `L(1/B - 1)` in side, paid once, and a finer direction net buys
it back: `0.0088` at `3.82` on the retained net, `0.0011` at 1440 steps.
[X-023](../explorations/X-023-three-losses-and-a-new-atom.md) separates that loss from
the two that follow it, and this claim is about the first one after the measure has been
allowed to move.

The frozen atoms transfer to every finer net without losing coverage, which is what
makes the re-optimisation worth running rather than merely worth pricing: their dilation
supremum rises to `3.81660950` at 1440 directions with the weights untouched.
The ceiling at `191/50` says where that road ends.
Scaled to unit squares it caps the one-body point method at side `3.8288`, so a
certificate on a finer net has about `0.012` of unit side left, and the question this
claim asks is how much of it the LP takes.

[Lane T](../series/series-000-smoke-and-calibration/results/agenda-033/lane-t-theory-cuts-and-routes.md)
proves the cap applies to every sound core rule, not only to the concentric square core,
so a refutation here is a refutation of the whole one-body family at that side.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
