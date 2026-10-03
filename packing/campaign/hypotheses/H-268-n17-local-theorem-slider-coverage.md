---
title: H-268 — with square 6 in its cover cell, the n17 endpoint family's slides stay inside the certified box
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-268
  kind: hypothesis
  claim: >-
    Every packing of 17 unit squares in [0,S]^2 with S <= S* whose occupancy state is the
    endpoint's state on the H-266 cover, and whose 45 non-slider coordinates lie within
    1/5000 of the endpoint family, has slides a <= 1/4 and z >= -1/8 (and b <= 1/12), so
    that the box B_W certified in exp-244 contains its slider coordinates and the exp-244
    local minimum applies to it.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: >-
      An exact or outward-interval proof that square 6 confined to its H-266 cell, with the
      other squares within the declared radius of the family, bounds square 5's slide and
      square 13's slide inside B_W, with the bounds' margins reported
    direction: >-
      Confirm if the bounds hold with strict margin, with synthetic controls and an
      independent review. Reject if a configuration in the endpoint's occupancy state
      places a slide outside B_W; then B_W must be widened (cheap in a, costly in z,
      where the 13/14 face degenerates near z = -0.79) and exp-244 re-run.
    threshold: Strict margins on a <= 1/4 and z >= -1/8
  instrument: >-
    A small exact geometric check to be built: square 6's cell from
    devtools.check_n17_capacity_one_cover, separating-axis bounds on the 5/6 and 6/13
    pairs over square 6's cell and orientations, and the 11/13 bound on b
  instrument_ready: true
  regime: >-
    n=17; the exact H255 root; the H-266 24-cell cover and the endpoint's occupancy
    state; the exp-244 radius and box
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: One short build and review slice
  prereqs: [H-261, H-266]
  replication: false
  registered: '2026-10-02'
  notes: >-
    Registered after the exp-244 review found that the H-261 claim as worded covers the
    whole physical slider domain while the certified box does not: with square 6 dropped,
    square 5 can slide to a = 1.074 and square 13 to z = -0.9165 (float scan, one axis at a
    time). With square 6 at its centroid the review's scan gives a <= 0.037 and
    z >= -0.0235, well inside B_W, so the bound plausibly comes from square 6's cell.
---
# H-268: The Certified Slider Box Is Enough for Capture

The local theorem drops square 6, so on its own it cannot stop squares 5 and 13 sliding
outside the box it certifies.
A capture step knows more: it knows which cover cell holds square 6. This hypothesis
turns that knowledge into the bound the local theorem needs, so that the certified box
and the captured state fit together.

## Progress

*Added 2026-10-02 by Session 167.* `devtools.check_n17_slider_coverage` proves
$a\le21/100$, $z\ge-1/20$ and $b\le3/40$ exactly, with square 6 in the tabbed design’s
cell side-S2. The unique-state design shifts that cell left by $0.01$, so the bound must
be re-run on it before review.
The exp-244 box also has faces $a\ge0$, $b\ge0$ and $z\le1/16$, which this claim does
not cover; $b\ge0$ rests on the 9/11 contact, which the local theorem drops.

## Outcome

*Added 2026-10-02 by Session 168.* The bounds quoted under Progress were for the earlier
tabbed design. On the unique-state cover the certified slides are $a\in[0,23/200]$,
$b\in[b^\ast,37/500]$ with $b^\ast=-1.685r$, and $z\in[-49/1000,0.0241]$.
[exp-248](../series/series-000-smoke-and-calibration/experiments/exp-248-h268-n17-local-half-composition.md)
accepts this hypothesis after an
[independent composition review](../../../docs/project/reviews/review-2026-10-02-n17-local-half-composition.md).
It records one deviation: the slides lie in $B_W'$, which has a $b$ floor of $-1/2500$,
not in $B_W$, and the local theorem is certified over $B_W'$ in the same experiment.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
