---
title: H-064 — an exact-depth fractional packing puts the n = 11 covering value at eleven by side 3.85
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-064
  kind: hypothesis
  claim: >-
    At container side 77/20 = 3.85, on the retained 181-direction net at B = 9977/10000,
    there is a finite family of closed B-square placements at net directions carrying
    non-negative rational weights whose depth -- the weighted count of listed placements
    containing a point -- is at most 1 at every vertex of the arrangement of their edges
    and the container boundary, and whose total weight is at least 11. By weak duality
    that puts the fractional packing value nu*(3.85) at or above eleven, hence the
    covering value tau*(3.85) at or above eleven, so no weighted fractional
    unavoidable-set certificate of this shape exists at 3.85 or at any larger side, and
    the n = 11 certificate ladder's top lies strictly below 3.85.
  lane: proof
  derived_from: [X-014]
  strategy_refs: ['proof:21', 'proof:22', 'proof:23']
  criterion:
    shape: determination
    metric: >-
      the exact depth-scaled total weight of a frozen ceiling certificate at side 77/20,
      decided by sqpack.fractional.ceiling with every vertex of the arrangement checked
      exactly
    direction: >-
      accepted only if verify_ceiling accepts the frozen bytes -- maximum pointwise depth
      at most 1 at every arrangement vertex, every placement inside the container, exact
      rational weights -- with a total weight of at least 11; rejected only by a
      certificate at 77/20 with total mass strictly below eleven retained through
      devtools.decide_certificate, which by weak duality puts nu*(3.85) below eleven and
      is a rung rather than a failure; a cutting-plane loop that stalls with a
      depth-scaled total below eleven is a bounded negative for the loop and leaves the
      claim unresolved, because a lower bound that fails to reach a threshold is not an
      upper bound
    threshold: 11
  instrument: >-
    The column generator's site loop run in the other direction: cutting planes on the
    vertices of the current family's arrangement, with sqpack.fractional.ceiling's
    maximum_depth as the separation oracle, scaled_to_unit_depth for the scaling and
    verify_ceiling as the decision. The start is the object T-018 already built and
    decided at 3.82 -- the converged dual, 76 squares and 608 after the D4 images, raw
    total exactly eleven, exact maximum pointwise depth 1925/1152 = 1.671007 across
    1650944 arrangement vertices of which 272244 were checked in exact arithmetic, giving
    a feasible total of 1152/175 = 6.5829 -- warm-started to 3.85 after 3.82 is pushed.
    The instrument exists and has been run once; what is new is the loop around it. Its
    one recorded failure mode is the reason the loop is needed: the 3.82 family's weights
    came from a dual that enforced depth at the sites and not at the arrangement's
    vertices.
  instrument_ready: true
  regime: >-
    Exact rational arithmetic throughout; closed B-square placements at net directions and
    their D4 images, inside the closed container; depth decided at arrangement vertices
    and never at a grid sample. That last is not a preference. At 3.82 column generation
    priced against a grid sample and reported a depth of 12/11 = 1.0909, which would have
    made the feasible total 121/12 = 10.08; the exact maximum was 1925/1152, 53 per cent
    higher, because depth peaks at vertices no grid samples. A ceiling judged on a sampled
    depth flatters itself and is refused.
    Both nu* and tau* are non-decreasing in the side -- a measure on the larger container
    restricts to the smaller one, and a family in the smaller container is a family in the
    larger -- so a value at or above eleven at 3.85 forecloses every larger side too.
  instance: {axis: side, point: '77/20'}
  sweep:
    axis: container side
    points: ['191/50', '77/20', '387/100']
  priority: 1
  cost_estimate: >-
    110 elapsed minutes inside agenda-021's BC-200, 3.82 first and 3.85 warm-started from
    it; the exact vertex check is the cost and it reached 1650944 vertices on a
    608-placement family at 3.82
  prereqs:
  - the 3.82 dual and its exact depth check, retained in T-018's next_rung
  replication: true
  registered: '2026-09-05'
  notes: >-
    Why 3.85 is the side the claim is made at. The ladder's retained top is 381/100, the
    reach table's packing cap for n = 11 is 3.8690 -- X-014's U * B * max(cos delta + sin
    delta) = 3.868983, which no certificate of this shape can pass whatever the site set
    -- and 3.82 is where two independent site sets already stop at exactly 11.000000.
    A wall confirmed at 3.85 would leave 0.027084 of the side gap below Trump's 3.877084
    that no certificate will close, and would say the last stretch belongs to the case
    analysis or to nothing. A rejection at 3.85 is a rung and moves the smallest open case
    again.
    What this decides and what it does not. Weak duality is one line and is proved in
    ceiling.py's docstring; the claim's accepted direction is therefore a genuine
    foreclosure. Its unresolved direction is not the opposite: nu* is a lower bound on
    tau*, and the gap between them is exactly the integrality question that Caoduro and
    Sebo bound in general -- the piercing-to-packing ratio of families of unit squares
    under rotation reaching 3 and never exceeding 6 -- and that the 2026 counterexamples
    to Wegner's conjecture put at 5/2 - epsilon for rectangles. Both concern finite
    families given in advance rather than the covering value of a container, so they make
    a plateau unsurprising and decide nothing.
    X-014 lists this as its first measurement and says of it that nothing kills the idea:
    either outcome sets the ladder's top and the tree's working side. That is why the
    claim is registered with a rejection route that is itself a result.
---
# H-064 — Measuring the `n = 11` Covering Value From Below

The `n = 11` ladder stopped at `381/100` and the next side up was attacked from both
ends. Neither closed.
Two independent site sets stop at exactly `11.000000` at `3.82` — one converged over
twelve rounds, one standing through twenty-four while its least covered mass climbed
from `0.8490` to `0.9997` — and the rejection route reached only `1152/175 = 6.5829` of
the eleven a ceiling needs.

`T-018` records what that leaves: if `τ*(3.82)` is exactly eleven then this is the one
configuration where neither pre-registered route can close, since a certificate needs
mass below `n` and a ceiling needs the scaled dual to reach `n`, and both fail by an
infinitesimal at exactly `n`.

This claim is the measurement that would settle which side of that the truth sits on,
and the reason it is worth making is that the rejection route was never run properly.
The `3.82` family’s weights came from a dual that enforced depth at the sites, not at
the vertices of the arrangement, and the two numbers differ by 53 per cent.
Adding the violating vertices as constraints and re-solving is the cutting-plane loop
the column generator already runs in the other direction; the instrument for the depth
check exists and has decided `1650944` vertices once already.

A value at or above eleven proves the ladder cannot pass that side, and the distance
from there to Trump’s `3.877084` is the part of the side gap that no certificate of this
shape will ever close.
That number is the input every part of X-014’s proposed proof shape needs and none of
them can be priced without.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
