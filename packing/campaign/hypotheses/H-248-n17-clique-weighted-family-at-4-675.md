---
title: H-248 — a clique-weighted family of unit squares with fractional stability at least 17 fits at side 4.675, then 4.67, the n17 architecture ceiling
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-248
  kind: hypothesis
  claim: >-
    A finite family F of unit squares inside [0, 4675/1000]^2, at any angles, and
    rational weights y >= 0 exist with y(K) <= 1 on every clique K of F's
    interior-overlap graph and sum y >= 17. By the capacity-one ceiling lemma, proved in
    the 4.640020 review, it follows that no parent-core certificate built from point
    atoms, floor-one threshold atoms (coefficients included) and pairwise-intersecting
    winning-subset rules proves s(17) > 4675/1000. A triangle-free family of 34 squares
    with y = 1/2 is the special case. The second target is 467/100.
  lane: proof
  derived_from: [X-047]
  criterion:
    shape: determination
    metric: >-
      The verdict of an exact rational checker on a proposed family with rational poses
      and weights: every square inside [0, 4675/1000]^2; the conservative overlap graph
      from geometric_graph_certificate (an edge is removed only by an exact separating
      axis); check_weighted_clique_certificate proving every clique of that graph has
      weight at most 1; and the exact sum of weights at least 17. Then the same at
      467/100.
    direction: >-
      Confirm only when the exact checker accepts a family. No family found at the
      search budget is inconclusive and never a refutation. The claim is refuted only by
      a proof that no such family fits, for example a certificate of the named
      architecture proving s(17) > 4675/1000, as Kleddamag v1.1.0 refuted H-243's
      463/100 and Kleddamag's 4.66001 certificate refuted this hypothesis's first
      targets, 465/100 and 466/100.
    threshold: 4675/1000
  instrument: >-
    A heuristic family search (the attic/planning-160/n17/triangle_free_probe.py
    anneal, promoted to a devtool) with an exact driver over
    devtools.geometric_graph_certificate and devtools.check_weighted_clique_certificate
    plus an exact containment check, built under BC-387
  instrument_ready: false
  regime: >-
    n=17 architecture ceiling; families of unit squares at free angles in a square of
    side 4675/1000, then 467/100; exact rational decision of containment, every pair
    and every clique weight; at most 64 squares per family, the clique tool's ceiling
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    About three hours of Opus extra-high build for the search and driver; runs of
    minutes wherever a slot is free
  prereqs: [think-68la]
  replication: false
  registered: '2026-09-27'
  notes: >-
    The successor of H-243 after Kleddamag v1.1.0 (s(17) > 4.640020), from the
    2026-09-27 planning block
    (docs/project/specs/archive/plan-2026-09-27-after-4640020-overnight.md). Every atom
    in v1.1.0 has capacity one, so a valid certificate at 4.640020 shows no such family
    fits at any side up to 4.640020. Registered at 465/100 and 466/100, where a
    two-minute anneal at 4.65 ended at two triangles among 34 squares with fractional
    stability 16 from both a two-Bidwell-copies start and a random start. The ceiling
    lies in [4.66001, s(17)], so below 4.67553; retargeted 2026-09-27 after Kleddamag's
    4.66001 certificate, every atom of capacity one, refuted 465/100 and 466/100
    (docs/project/reviews/review-2026-09-27-n17-kleddamag-466001.md, section 7). The
    file was renamed from H-248-n17-clique-weighted-family-at-4-65.md with the retarget.
---
# H-248: Where the n17 Certificate Architecture Stops, Sharpened

Kleddamag’s v1.1.0 certificate settled H-243 at $4.63$ from the other side: a valid
certificate whose every atom has capacity one is itself a proof that no triangle-free
family of 34 squares fits at $4.640020$ or below.
Kleddamag’s $4.66001$ certificate, again with every rule of capacity one, did the same
to this hypothesis’s first targets, $4.65$ and $4.66$, on 2026-09-27. The ceiling lies
in $[4.66001,\thinspace s(17)]$, inside $[4.66001,\thinspace4.67553]$.

The sharp form of the lemma weights a family by any $y\ge 0$ with $y(K)\le 1$ on every
clique of the overlap graph, since every set of cores that fires one atom is pairwise
overlapping. A family with $\alpha^{\ast}(G_F)\ge 17$ at side $S$ caps every certificate
of this architecture at $S$; the triangle-free family with $y=\tfrac12$ is the case the
previous plan stated.
The lemma is monotone in the side, so the search runs at $4.675$ first, just under
Bidwell’s packing, where a family is easiest to fit, and at $4.67$ second.
A found family is checked exactly by the graph and clique tools this repository already
has, which prove a weighted-clique bound on a conservative overlap graph.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
