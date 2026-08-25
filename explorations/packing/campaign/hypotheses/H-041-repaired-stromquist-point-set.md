---
title: H-041 — a one-coordinate repair restores Stromquist's Theorem 2 mechanism
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-041
  kind: hypothesis
  claim: >-
    At s = 2 + 4/sqrt(5), replacing the printed Figure 14 point
    G = (4/5, 37/20) by G' = (79/100, 37/20) yields an unavoidable twelve-point
    set and restores all five implications needed for Stromquist's lower bound on
    eleven freely oriented unit squares.
  lane: proof
  derived_from: [X-001]
  strategy_refs: ['proof:2', 'proof:3', 'proof:15']
  criterion:
    shape: conditions
    metric: complete independently replayed finite cover and five-node implication chain
    direction: every cover cell, strict inequality, conditional triple, and capacity implication certifies
  instrument: >-
    cases.stromquist.repaired_cover binds the source-distinct repaired Figure 14 tuple,
    exactly tiles the Figure 13 and Figure 14 center spaces, certifies every lemma
    premise and boundary, checks the finite resource count, and regenerates the complete
    retained record. Its mutation suite removes cells and edges, restores the printed
    failing point, changes thresholds and capacity, and corrupts source scope.
  instrument_ready: true
  regime: >-
    Stromquist's exact Figure 13 geometry and strict open-box semantics at
    s = 2 + 4/sqrt(5), with only G moved from x = 4/5 to x = 79/100 in Figure 14
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [11]}
  priority: 1
  cost_estimate: tier S once the finite face cover is encoded
  prereqs: [exact terminal rejection of H-010 on the printed Figure 14 set]
  replication: true
  registered: '2026-08-24'
  notes: >-
    This is a post-falsification successor, not a correction silently attributed to
    Stromquist. Defeating the known H-010 escape witness is necessary but insufficient:
    acceptance requires the complete repaired unavoidability cover and the other four
    proof nodes. Any uncovered pose rejects the claim. Exact exhaustive coverage, not a
    failed numerical escape search, decides the result.
---
# H-041 — test the smallest visible repair

The printed point `G = (0.8, 1.85)` leaves a narrow escape through the adjacent Lemma 4
quadrilateral.
Moving only its x-coordinate left by `0.01` is the smallest simple decimal
repair currently proposed.

This claim was registered after finding the printed-set witness and before checking the
repaired cover. It therefore tests a new construction; it does not rescue H-010’s
source-faithful claim after the fact.

The checker must certify every face in the reconstructed Figure 13 and Figure 14
partitions. A fresh escape would refute the proposal, but failure to find one is not
evidence; only the complete exact cover can accept H-041. Passing the one witness that
killed H-010 is likewise insufficient.

**Confirmed, 2026-08-24.**
[Exp-017](../series/series-000-smoke-and-calibration/experiments/exp-017-h-041-stromquist-repaired-figure14.md)
certifies all five implications exactly.
The repaired Figure 14 complex has 26 faces, 28 vertices, and 53 edges; all thirteen
source, geometry, boundary, sign, capacity, and record mutations pass.
The result proves `s(11) >= 2 + 4/sqrt(5)` with a computer-assisted, source-distinct
certificate. It does not repair the paper *as printed*, attribute `G'` to Stromquist,
close the gap to Trump, or claim external peer review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
