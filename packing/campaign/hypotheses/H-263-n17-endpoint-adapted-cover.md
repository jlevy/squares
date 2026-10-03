---
title: H-263 — which closed cover keeps the n17 endpoint family inside one occupancy state
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-263
  kind: open_question
  claim: >-
    Which closed centre cover with proved cell capacities keeps every endpoint-family
    centre at least the H-261 radius from a seam, and leaves the fewest surviving orbits
    under the H-262 instrument: a shifted or re-capped 5 by 5 mixed grid, or a
    capacity-one Voronoi or hexagonal cover of 26 to 27 cells?
  lane: proof
  derived_from: [X-048]
  instrument: >-
    The H-262 census tool applied to each candidate cover, after each cover's capacity
    lemmas are proved and reviewed
  instrument_ready: false
  regime: >-
    n=17; caps at or above S*; endpoint family as accepted under H-256 and H-261
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: One W3 design slice, then one H-262 census per candidate cover
  prereqs: [H-262, think-j1uw]
  replication: false
  registered: '2026-10-01'
  notes: >-
    From the PR 265 route review. On the H259 grid all 17 endpoint centres lie in
    distinct cells (11 boundary, 6 interior), no capacity-two cell is used, and square
    9's centre is 0.0012 below the seam y = 1/2 + 3a. Raw orbit counts for a 26- or
    27-cell capacity-one cover are about C(26,17)/8 = 0.4 million to C(27,17)/8 = 1
    million, but survivors after cuts, not raw counts, decide.
---
# H-263: An Endpoint-Adapted Cover

The H259 grid was chosen before anyone looked at where the endpoint’s centres fall, and
one of them sits 0.0012 from a seam.
A capture step is simplest when the whole endpoint family lies inside one occupancy
state. This question selects the cover by measured survivors.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
