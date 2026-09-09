---
title: H-149 — sixteen owner sectors fatten the patch enough to break neutrality
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-149
  kind: hypothesis
  claim: >-
    Refining the corner-owner angular bins from eight to sixteen makes every guaranteed
    patch reach at least 0.015 further than its eight-sector parent, so that at q = 96/25
    every refined subclass of the four neutral eight-sector classes (m1:j3, m1:j4, m2:j3,
    m2:j4) deletes strictly more than one unit from the transported mass-eleven ceiling
    family: exact survivor weight at most 79/8 = 9.875, strictly below the conditional
    requirement of 10. Neutrality is then a property of the eight-sector patches rather
    than of conditioning, and Step 3 of X-026's ladder no longer holds at sixteen
    sectors.
  lane: proof
  derived_from: [X-026]
  strategy_refs: ['proof:10', 'proof:22']
  criterion:
    shape: determination
    metric: >-
      the exact survivor weight of the mass-eleven ceiling family, transported to 96/25
      and screened against each refined sixteen-sector patch, minimised over the refined
      subclasses of the four neutral eight-sector classes; equivalently the reach the
      refined patch gains over its parent, against the 0.014978 separating gap of the
      nearest survivor
    direction: >-
      Confirm when every refined subclass of every neutral class has exact survivor
      weight strictly below 10. Refute when any refined subclass still has survivor
      weight exactly 10, since a case split needs every class closed and one surviving
      class defeats it; that outcome leaves X-026's Step 3 standing at sixteen sectors as
      it stands at eight. A float reading of the separating gap decides neither
      direction, and a gain measured on any family other than the mass-eleven ceiling
      family decides nothing at all (D-489).
    threshold: 10
  instrument: >-
    devtools.owner_footprints builds the patches but hard-codes eight bins
    (owner_branch_manifest iterates range(8); triangle_footprint and endpoint_footprint
    reject sector >= 8), so the one missing piece is a bin-count parameter and the
    rational wedge vectors at multiples of pi/8 that go with it. Everything downstream
    exists and runs in seconds: devtools.transport_ceiling_family moves
    ceiling-family-191-50.json to 96/25, screen_footprint from
    devtools.screen_corner_dual_salvage does the deletion with the ownership line's own
    filter, and the lane X1 scripts (lane-x1-ceiling11-screen.py.txt, lane-x1-gap.py.txt)
    are the screen and the gap reader as run.
  instrument_ready: false
  regime: >-
    n = 11, side 96/25, shrink 9977/10000, the 361-direction doubled net; sixteen closed
    angular bins per mark and two marks per corner, so thirty-two classes per corner;
    exact rational arithmetic throughout, screened against the retained depth-one
    mass-eleven ceiling family
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: >-
    under an hour: the bin-count parameter and its wedge vectors, then one screen of
    seconds per class over the eight refined subclasses that matter
  prereqs:
  - a bin-count parameter in devtools.owner_footprints, with the pi/8 wedge vectors and
    the containment argument of the sector-footprint proof restated at sixteen bins
  replication: true
  registered: '2026-09-09'
  notes: >-
    This is the one escape that could overturn Step 3 of X-026 and it has never been run.
    Lane X1 measured why it is live: the closest survivor to the j3 footprint is a
    weight-1/8 wall placement centred at (1.50658, 0.50885) at a Euclidean separating gap
    of 0.014978, so a patch reaching 0.015 further deletes 1/8 more and the class stops
    being neutral. The mechanism of the gain is in the sector-footprint proof: an owner
    anchored at angle phi covers the wedge of directions [phi, phi + pi/2], and
    intersecting over a closed bin of width w leaves a guaranteed wedge of width
    pi/2 - w. At eight bins w = pi/4 and the guaranteed wedge is pi/4 wide; at sixteen
    bins it is 3pi/8 wide, half again as wide, and the inscribed rational fan can reach
    further in the directions between the parent's two rays. Nothing about that argument
    is new mathematics -- it is the same containment argument with different rational
    vectors -- which is why this is priced in minutes rather than in sessions.
    What it would and would not buy is worth stating before it runs. A confirmation
    reopens single-corner point-cover conditioning at sixteen sectors and no more: the
    global ceiling slack at 96/25 is 0.262 (tau <= 11.262), the refined split costs
    thirty-two classes per corner instead of sixteen, and X-026's Step 6, the rank-one
    cap of 3.868983 on the conditional method at every m, is untouched by any patch
    refinement because it never used the patch. A refutation closes the conditional
    point-cover line at both resolutions and is the cheaper of the two outcomes to
    record. Either way this decides a scope question in the record rather than a bound.
    Registered from X-026 section 5, escape 1, and carried as `think-dm0f`; escapes 2
    (empty classes) and 3 (compatibility pruning of the four neutral sectors) are
    unregistered and belong to the ownership line's own branch.
---
# H-149 — Sixteen Sectors, a Fatter Patch, and the 0.015 That Would Decide It

[Lane X1](../series/series-000-smoke-and-calibration/results/agenda-033/lane-x1-corner-conditioning-is-mass-neutral.md)
measured corner conditioning as exactly mass-neutral: the transported mass-eleven
ceiling family carries weight exactly one on each corner-mark clique, four of the
sixteen classes per corner have a patch that reaches nothing beyond the mark, and the
deletion at those classes is exactly the one unit of threshold the conditioning costs.
[X-026](../explorations/X-026-what-conditioning-does-and-does-not-buy.md) states that as
a six-step ladder and marks Step 3 — deletion exactly one, survivor exactly ten, against
a requirement strictly below ten — as the step that carries the whole result.

**Step 3 is a statement about the current eight-sector patches, not about
conditioning.** The nearest survivor to the `j3` patch sits at a separating gap of
`0.014978`. A patch reaching `0.015` further deletes that weight-`1/8` placement too,
the survivor falls to `79/8`, and the class is no longer neutral.
Sixteen bins instead of eight is how one would reach it, and the sector-footprint proof
already contains the reason it should work: halving the bin widens the guaranteed wedge
from `pi/4` to `3pi/8`.

**It is cheap and it is unrun.** The screen is the one lane X1 ran, at a different bin
count; the transport, the filter and the gap reader are all in the repository, and the
missing piece is a bin-count parameter with the rational wedge vectors that go with it.
Lane X1 named this measurement and declined to spend it; it is carried as `think-dm0f`.
It should be run before the conditional line is closed in the record, because it is the
only measurement that can overturn Step 3 — and because a refutation, which is the
likely outcome, is worth having on the record at the resolution where somebody would
next ask.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
