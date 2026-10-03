---
title: H-266 — a D4-symmetric capacity-one n17 cover of at most 25 cells holds the endpoint family in one state
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-266
  kind: hypothesis
  claim: >-
    At cap U = 1169/250 there is a D4-symmetric closed cover of the centre box
    [1/2, U - 1/2]^2 by at most 25 cells, each of proved capacity one (interior cells by
    diameter below 1; wall and corner cells by the depth-width wall lemma
    g <= c d + s w - 1 - (c/2)(c + s - 1) over the quarter circle), such that the whole
    H256 endpoint family, sliders included and embedded concentrically, lies inside one
    occupancy state with every centre at least 1e-3 from every seam of its cell.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: >-
      Exact rational verification of coverage of the centre box, every cell's capacity
      argument, the D4 invariance of the cover, the Burnside count of closed
      capacity-one assignments of 17 centres, and the endpoint family's seam margin over
      the H256 slider domain
    direction: >-
      Confirm if a cover with N <= 25 passes every item exactly or by outward bounds,
      with synthetic controls (the H259 falsifier pair refused as a capacity-one cell; a
      cell of diameter at least 1 refused) and an independent review of the depth-width
      wall lemma. Reject if no D4-symmetric cover with N <= 25 holds the family in one
      state. A cover with the family straddling a seam is inconclusive and returns the
      seam to design.
    threshold: N <= 25, at most 135,196 D4 orbits
  instrument: >-
    devtools.check_n17_capacity_one_cover, to be built: rational cells, the
    depth-width wall lemma on closed rational angle intervals, exact squared diameters,
    exact coverage, the D4 action and Burnside count, and the endpoint family's seam
    margins, with an independent proof review of the wall lemma
  instrument_ready: true
  regime: >-
    n=17; cap 1169/250; the H256 endpoint family with its slider domain; closed cells
    with the H259 deterministic seam rule
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: One build and review slice; the check itself runs in seconds
  prereqs: [H-259, H-256]
  replication: false
  registered: '2026-10-02'
  notes: >-
    From the bulk-exclusion design review
    (docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md, its H-F1). The
    exploratory 24-cell design (4 corner cells 0.78 square, 12 side cells of depth 0.911
    and width 0.7053, 8 interior Voronoi cells of diameter 0.960) has 346,104 states and
    43,593 D4 orbits, 177 times below the cut H259 count, but square 13 sits 0.0023
    below the ring seam and slides across it. n11's cover was 16 capacity-one cells for
    11 squares.
---
# H-266: A Minimal Capacity-One Cover for n17

The H259 grid behaves like a 30-cell capacity-one cover, and its 7.7 million orbits
after the free cuts are more than any per-case engine can absorb.
n11 succeeded with a minimal capacity-one cover and isolated sub-pattern exclusions.
This hypothesis asks whether n17 has a comparably small cover that also keeps the
endpoint family in one occupancy state, so that capture works on a single case.

## Outcome

*Added 2026-10-02 by Session 167.*
[exp-246](../series/series-000-smoke-and-calibration/experiments/exp-246-h266-n17-capacity-one-cover.md)
certifies a 24-cell D4-symmetric capacity-one cover with 43,593 orbits, and the
[wall-lemma review](../../../docs/project/reviews/review-2026-10-02-n17-depth-width-wall-lemma.md)
proves the lemma its wall cells rely on.
The verdict is unresolved: under the overlapping-cell convention the endpoint family
also realises a second state through side cell S1, and square 6’s range is declared
rather than derived.
A small design change and a derived square-6 range would close both.

*Later on 2026-10-02.* Session 167’s lane G2 added a `unique_state` check, which the
tabbed design fails on squares 13 and 11. It also built
`ring-3-voronoi-8-tabbed-unique`, which passes every check with a unique family state
(least margin $0.002111$) and keeps 43,593 orbits.
It awaits review and a recorded run.

*Accepted 2026-10-02 in Session 168.*
[exp-247](../series/series-000-smoke-and-calibration/experiments/exp-247-h266-n17-unique-state-cover.md)
records the unique-state design passing every item after an
[independent review](../../../docs/project/reviews/review-2026-10-02-n17-unique-state-cover.md).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
