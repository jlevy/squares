---
title: H-247 — rung 0 widened, Trump is globally optimal on a half-tangent box of half-width 10^-4
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-247
  kind: hypothesis
  claim: >-
    In the family of six unit squares at actual orientation 0 and five sharing one
    orientation theta modulo pi/2, with centres and contacts free, every packing whose
    half-tangent t = tan(theta/2) lies in [t* - 10^-4, t* + 10^-4], t* Trump's tilt, has
    container side at least U, and every such packing at side U lies in the
    Z/4 x S6 x S5 orbit of Trump's pose.
  lane: proof
  derived_from: [X-046, X-045]
  criterion:
    shape: determination
    metric: >-
      A complete fixed-shape cell tree over the widened box, using rotational cores,
      whose every leaf carries an exact rational Farkas infeasibility vector or an exact
      dual bound strictly above U compared through U's isolating interval, or is
      Trump-degenerate and closed by the BC-240 local theorem with an explicit labelled
      matching whose enclosure lies within the radius rho = 808514697/200000000000
    direction: >-
      Confirm only when the unchanged independent reader accepts the complete tree on a
      declared box covering the registered one at a target of at least U, with at least
      one Trump-degenerate leaf. Stop, without a verdict on the claim, if the enclosure
      reach of a Trump-degenerate leaf meets rho, since the local theorem then no longer
      closes it. Kill with a leaf whose exact bound is below U and which is not
      Trump-degenerate, verified as a feasible packing before it is called a
      counterexample. Unresolved leaves at the declared node or wall cap are a bounded
      negative on the instrument.
    threshold: U
  instrument: >-
    packing/cases/trump11/fixed_angle_tree.py box preset (--t-lo, --t-hi), which admits
    a box holding t* while its angle reach stays below rho, with the unchanged
    independent reader fixed_angle_tree_check.py; only a launcher is new
  instrument_ready: true
  regime: >-
    n=11; six squares at orientation 0, five at one common orientation in the
    half-tangent box of half-width 10^-4 about t*; exact rational leaf certificates; side
    compared with the exact algebraic U
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: About 1.7e8 nodes, one night on nine workers, then the reader
  prereqs: [think-7c17]
  replication: false
  registered: '2026-09-25'
  notes: >-
    H-236 (T-035, exp-232) at a box one hundred times wider, from the Session 159 n11
    assessment (docs/project/specs/active/plan-2026-09-25-after-r052-planning.md). Its
    cost was set by the margins near Trump's pose, not by the box width, and exp-234
    found no width dependence, so the node count should be close to rung 0's. The
    measured enclosure reach was about fifteen times the half-width, which puts the rho
    limit near a half-width of 2.7e-4.
---
# H-247: Rung 0, Widened

T-035 holds on a half-tangent box of half-width $10^{-6}$ around Trump’s tilt.
The same instrument, unchanged, should hold on a box a hundred times wider for about the
same cost, because the cost came from resolving margins near Trump’s pose rather than
from the width. The widened statement is the part of rung 1 nearest Trump’s tilt, where
no counting certificate can reach.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
