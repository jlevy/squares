---
title: H-346 — an angle branch and bound with Taylor-at-centre LP bounds prices the outer capture bridge
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-346
  kind: hypothesis
  claim: >-
    A branch and bound over the sixteen non-free angles and the feature choices of the
    family's occupancy state at cap U', which bounds each angle box by the fixed-feature
    LP of the widened-projection scope review evaluated at the box centre plus an
    outward interval remainder for the second-order terms, closes a box when the bound
    exceeds U', and stops when a box lies inside the widened terminal region (angles
    within 5e-3 and centres within 1e-2 of the family, features forced), has a Knuth
    estimate below 10^8 nodes from the cells; and with the 1/1216 per-coordinate vector
    as the leaf instead, below 10^10.
  lane: proof
  derived_from: [X-052]
  criterion:
    shape: determination
    metric: >-
      The Knuth estimator (random root-to-leaf probes with branching-factor products)
      over at least 2,000 probes on the built tree, at both leaves, with the sampled
      remainder constant (about 0.3 per squared radian near the family) and the
      per-box LP time; the fraction of probes ending at a closed box, a terminal leaf or
      a feature disjunction.
    direction: >-
      Confirm when the estimate at the widened leaf is below 10^8 nodes with a standard
      error under a factor of three. An estimate above 10^8 refutes the claim for this
      relaxation and says capture needs a terminal theorem along the soft directions
      before any engine; between 10^8 and 10^10 at the 1/1216 leaf is recorded as the
      price.
    threshold: below 1e8 nodes at the widened leaf; below 1e10 at the 1/1216 leaf.
  instrument: >-
    Unbuilt: devtools/pilot_n17_subpattern_bb.py with its relaxation swapped for the
    fixed-feature LP at the box centre (the 19 chain pairs, 64 containment rows and the
    slider domain of the scope review) plus an interval remainder, a feature-disjunction
    branch, and a Knuth probe mode; HiGHS proposals with exact re-checks are not needed
    for an estimate.
  instrument_ready: false
  regime: >-
    n = 17; the family's state at U'; the exact root's frame; angles as H254 lifts;
    square 6 coarse; the estimate only, no certificate; the widened leaf as H-329
    specifies it and the 1/1216 leaf as H-340 specifies it.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: >-
    Days of build on the existing branch and bound (about 25 agent-hours), minutes to
    estimate; no verification cost, since nothing is certified.
  prereqs: [H-329, H-340]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-052's direction 5, the after-pilot review's route (b) made a registered claim.
    It is the only candidate in the record with a soundness story for the
    cells-to-feature-forced bridge: second-order-convergent bounds remove the cluster
    problem X-046 cites, and near the family the remainder 0.3 rho^2 against the softest
    slope 0.0155 rho allows boxes of radius comparable to their distance along the
    softest direction. Far from the family the feature disjunctions multiply (256
    branches at the forced features, far more at cell scale), which is what the estimate
    measures. A Knuth estimate is the cheapest honest price; a run is not funded by this
    hypothesis.
---
# H-346: Price the Bridge Before Building It

**Mechanism.** At fixed angles the containment and separating-axis constraints are
linear in the centres, so the side at fixed angles is an LP; a box of angles is bounded
below by the LP at its centre minus an interval second-order term.
Such bounds converge quadratically, which is what lets boxes near the family be as wide
as their distance from it.
The cost is the number of boxes and feature branches between the cells and the terminal
region, which nobody has estimated.

**Falsifier.** A Knuth estimate above $10^8$ nodes at the widened leaf.

**Expected information.** Whether capture is a computation of $10^6$, $10^8$ or
$10^{12}$ nodes with this relaxation, which decides whether it is engineering or
mathematics.

**Limits.** An estimate, not a run; its leaf depends on H-329, and the $1/5000$ leaf can
stand in pessimistically; the remainder constant is sampled, not proved, for the
estimate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
