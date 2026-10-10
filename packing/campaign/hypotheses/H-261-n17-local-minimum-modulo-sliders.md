---
title: H-261 — the n17 endpoint is a strict local minimum modulo its slider cone
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-261
  kind: hypothesis
  claim: >-
    For an explicit rational radius r > 0, every packing of 17 unit squares in [0,S]^2
    whose 45 non-slider coordinates lie within r of the accepted n17 endpoint family,
    with slider coordinates anywhere in the physical slider domain, has S >= S*, with
    equality only on the family. The slider coordinates are square 6's three, xi_5 <= 0,
    square 11 along -v and square 13 along +-v; the kernel of the 52 positively weighted
    H-258 rows is exactly their span.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: >-
      An exact rational basis of the kernel of the 52 positive H-258 rows; exact
      nonnegative duals for all 90 signed non-slider coordinate directions; per-row
      curvature bounds by the n11 focused-rectangle recipe; Taylor checks that the 135
      unavailable owner alternatives stay negative; nonnegativity of the stress and the
      duals uniformly over the slider domain; and the ratio test (1/2) M_j < r_j at one
      declared rational radius vector.
    direction: >-
      Confirm only if H-258 is accepted, every item above is certified exactly or by
      outward intervals, synthetic controls pass, and an independent Fable max review
      of the composition (in particular the angle-chart reduction modulo pi/2 and the
      product form of the neighbourhood) finds no blocking defect. A failed ratio test
      at the declared radius is inconclusive for local minimality and selects interval
      enlargement along omega_11 - omega_12 and omega_16; it refutes nothing.
    threshold: >-
      Kernel dimension exactly 6 with the six named generators; every dual exact and
      nonnegative; worst ratio below 1 at the declared radius. Exploratory first-order
      estimate: worst ratio 0.86 at uniform radius 3e-4.
  instrument: >-
    devtools.check_n17_local_minimum, to be built: exact Fraction linear algebra and
    LP duals over the H-258 rows, the n11 curvature-bound recipe, and outward interval
    checks over the slider domain, with an independent kernel and dual checker
  instrument_ready: true
  regime: >-
    The H255 root box and H256 centroid endpoint; the H257 feature inventory; the H-258
    allocation; angles reduced modulo pi/2 in the H254 labelling; the l-infinity norm on
    non-slider coordinates
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    One controlled build and review slice of about two hours; target arithmetic in
    seconds to minutes on one worker
  prereqs: [H-258, think-wrgx]
  replication: false
  registered: '2026-10-01'
  notes: >-
    From the PR 265 route review
    (docs/project/reviews/review-2026-10-01-n17-route-after-pr265.md). Exploratory
    receipts in packing/campaign/explorations/X048-route-review/receipts/: kernel rank
    46 of 52 with the six slider generators, coordinate duals with largest coefficient
    175.8 for -omega_11 (ten minor duals need exact redo), radius ratios 0.86, 1.43, 2.9
    and 8.6 at 3e-4, 5e-4, 1e-3 and 3e-3. The certified radius is the target the global
    capture step must reach.
---
# H-261: Local Minimum Modulo the Slider Cone

The known n17 packing cannot be isolated: three squares slide and one rotates freely.
The terminal theorem must therefore say that nothing near the endpoint family is
smaller, with the slider coordinates left free.
Exploratory checks find a first-order conical minimum outside the six slider directions,
so the n11 focused-rectangle method applies once those directions are quotiented out.

The certified radius matters as much as the verdict: it is what the global capture step
must reach.

## Outcome

*Added 2026-10-02 by Session 167.*
[exp-244](../series/series-000-smoke-and-calibration/experiments/exp-244-h261-n17-local-minimum.md)
certifies the local minimum modulo sliders at $r=1/5000$ over the declared slider box
$B_W=[0,\tfrac14]\times[0,\tfrac1{12}]\times[-\tfrac18,\tfrac1{16}]$. The worst ratio is
$0.925818$, and an
[independent review](../../../docs/project/reviews/review-2026-10-02-n17-local-theorem-instrument.md)
found no blocking defect in the mathematics, the instrument or the certificates.
The verdict is unresolved, because the claim above covers the whole physical slider
domain and $B_W$ does not once square 6 is dropped.
[H-268](H-268-n17-local-theorem-slider-coverage.md) registers the capture-side bound
that would close the gap.
The criterion’s 135 unavailable alternatives are checked as the 125 of the retained
pairs, a recorded deviation.

*Session 168.* The local theorem now holds over $B_W'$, with the $b$ floor at $-1/2500$
([exp-248](../series/series-000-smoke-and-calibration/experiments/exp-248-h268-n17-local-half-composition.md)).
Composed with H-268 and the H-266 cover, it gives the capture-target theorem.
This hypothesis stays unresolved as worded: the composition review exhibits a packing at
side $S^\ast$ that meets every premise outside $B_W'$, the family with squares 5 and 6
exchanged.

*Note of 2026-10-09 (X-052).* The local-side review checked that witness exactly: for
$a = 1$ and $a = 1.07$ the exchanged configuration is, as a set of seventeen squares
with rational corners, the family member $w = (0, 0, 0)$ with square 6 on the bottom
wall at $x = x_5^\ast - a$, inside square 6’s box.
It is a relabelled family member, not a packing off the family, as X-048’s 5 October
note already says; under the state-induced labelling (the square in `side-S2` is “6”)
the equality clause holds for it.
What fails is only that the certified box does not cover the labelled slider domain,
which is disconnected ($a \in [0, 0.115] \cup [1, 1.074]$ at $z = 0$ by the review’s
float scan). The verdict stays unresolved as worded, a process choice rather than a
mathematical gap; the usable theorem carries the state premise.
See [X-052](../explorations/X-052-n17-status-survey-and-completion-plan.md).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
