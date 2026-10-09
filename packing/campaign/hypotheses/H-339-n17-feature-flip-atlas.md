---
title: H-339 — a small feature-flip atlas doubles the terminal region's radius
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-339
  kind: hypothesis
  claim: >-
    At most eight of the 135 unavailable owner-axis options of the retained pairs have a
    corner-gap margin below 1/10 anywhere on the slider box, and for every subset of
    those options that can become available on the angle-and-centre box of radius 2e-2
    around the family (angles within 2e-2, centres within 2e-2, sliders in the H256
    domain plus 2e-2), the fixed-feature LP with that option's separating row in place
    of the endpoint's has side above U' throughout the box; hence the widened
    projection theorem of H-329 extends from radius 5e-3 to 2e-2 by an atlas of at most
    2^8 feature branches.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      The 135 option margins minimised over the box by H-278's forcing bounds; the
      number of options with margin below 1/10; for each realisable flipped feature set,
      the minimum of the fixed-feature LP side over the box by sampled directions and
      then exact duals on patches.
    direction: >-
      Confirm when at most eight options fall below the margin and every flipped branch
      has LP side above U' on the whole box with exact duals. More than eight, or a
      flipped branch whose side falls below U' inside the box, refutes it and bounds the
      terminal radius below 2e-2.
    threshold: at most 8 options; every flipped branch certified; radius 2e-2.
  instrument: >-
    Unbuilt: H-329's patch certifier run per feature branch; the option-margin scan of
    devtools/check_n17_local_minimum.py extended to the larger box; a branch enumerator
    over the near-margin options.
  instrument_ready: false
  regime: >-
    n = 17; the exact root's frame; the family's state; cap U'; sliders in the H256
    domain plus 2e-2; square 6 coarse.
  instance: {axis: n, point: 17}
  priority: 3
  cost_estimate: Numeric scan in minutes; exact branches at H-329's cost per branch, at most 2^8 branches of which most are unrealisable.
  prereqs: [H-329, H-278]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route C, second stage. At the centroid the least option margin is 0.0558
    (pairs 14/17 and 7/14), then 0.0707 (12/16) and 0.094 (3/11 at b = 1/12); the
    feature-forcing radius of about 1e-2 is set by these, not by the LP. Enumerating the
    few options that can flip within 2e-2 and certifying each flipped LP is the cheapest
    way to double the terminal radius, and the branch count is the risk.
---
# H-339: Past the Feature-Forcing Radius

**Mechanism.** The widened projection theorem stops where an unavailable owner-axis
option can become available, because the LP’s rows change there.
Only a handful of options have margins small enough to flip within $2\times10^{-2}$;
each flip is a different LP with the same structure, and the union of the certified
branches is a theorem on the larger box.

**Falsifier.** More than eight near-margin options, or a flipped branch whose LP side
falls below $U'$ inside the box.

**Expected information.** The terminal radius the composed argument can claim, which
sets how far the exclusion engines must reach along the directions H-330 maps.

**Limits.** Branches multiply; an unrealisable branch must be shown unrealisable by an
exact argument, not skipped; and the atlas inherits every premise of H-329.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
