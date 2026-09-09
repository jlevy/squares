---
title: H-136 — a threshold certificate exists at 191/50 with the retained shrink and net
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-136
  kind: hypothesis
  claim: >-
    The rank-one threshold-atom closure -- point atoms together with (S, k) threshold
    atoms charging weight w to every core holding at least k points of S, at budget
    w floor(|S| / k) -- admits a D4-symmetric certificate of total budget below eleven at
    L = 191/50, B = 9977/10000 on the retained 181-direction net, on some finite site set
    and atom set with the coverage rows complete. The point-atom closure admits none: the
    exact depth-one family of weight exactly eleven at that (L, B, net) caps it at eleven.
  lane: proof
  derived_from: [X-023]
  strategy_refs: ['proof:22', 'proof:23']
  criterion:
    shape: determination
    metric: >-
      the total budget of a frozen threshold certificate decided exactly at
      (191/50, 9977/10000, 181 directions), against the exact weight of the heaviest
      depth-one family that is feasible for every rank-one threshold atom on the container
    direction: >-
      Confirm only with a frozen threshold certificate of budget below eleven accepted by
      devtools.decide_threshold_certificate with both of its routes agreeing -- the dense
      grid and the slab sweep, at every direction -- and by an independent reader written
      from the theorem rather than from the module. Refute with an exact depth-one family
      of weight at least eleven that is feasible for every rank-one threshold atom on the
      container, charging at most its budget for every (S, k), decided exactly. A
      restricted LP value below eleven with rows still incomplete decides neither
      direction, which is exactly what the loop below produced.
    threshold: 11
  instrument: >-
    sqpack.fractional.threshold carries the theorem, the atoms and the exact
    inclusion-exclusion sweep, and devtools.decide_threshold_certificate decides a frozen
    record by two routes required to agree. What does not exist is the search: the
    combined cut-and-site loop that produced the readings below is spike B's scratch
    driver with the interior-vertex 2-of-3 generator, unpromoted, and there is no
    independent threshold reader to stand beside the decision as
    devtools.independent_ceiling_reader stands beside the ceiling.
  instrument_ready: false
  regime: >-
    n = 11, side 191/50, shrink 9977/10000, the retained net t_k = (207107/500000) k/180,
    k = 0..180; rank-one atoms only, D4-symmetric, weights nonnegative
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: >-
    one session of three to four hours on one core for the loop; the freeze and decision
    step is minutes
  prereqs:
  - the combined cut-and-site loop promoted into devtools with its interior-vertex generator
  - an independent reader for threshold certificates
  replication: true
  registered: '2026-09-09'
  notes: >-
    The point-atom ceiling at 191/50 is a theorem, not a search artefact: 88 closed
    B-squares at six net directions, weight 1/8 each, total exactly 11, exact maximum
    depth 1 over 20,376 arrangement vertices, decided by the repository verifier and
    again by an independent reader. That is what makes this hypothesis the live one --
    the threshold language is not capped by it. The ceiling family is separated by 2-of-3
    atoms with their points at interior vertices of the pairwise-intersection polygons,
    at charge 5/4 against budget 1, and its heaviest corner clique carries weight 11/8
    with fractional piercing number 5/3 < 2, which is the condition that makes a clique
    cut a rank-one atom at all. Spike B's combined loop on BC-200's 12,761 sites read
    10.926982, 10.948526 and 10.956244 after each atom round and refilled to exactly
    11.000000 every time the coverage rows completed, three cycles in 46 minutes on one
    core; the dual collapsed each time onto a near-integral family of nine to fourteen
    rows whose overlaps sit in slivers no site samples. The loop had not converged at its
    budget, so nothing here is evidence either way about the claim.
---
# H-136 — A Certificate the Ceiling Does Not Cap

The exact depth-one family at `191/50` closes the point-atom route there: no
D4-symmetric measure of mass below eleven covers every closed `9977/10000`-square at a
net angle, on that net or any net containing its six directions.
Every site set that stopped at exactly eleven was reading that ceiling.

The threshold atoms of [X-023](../explorations/X-023-three-losses-and-a-new-atom.md) are
the rank-one Chvátal–Gomory cuts of the point-depth system, stated on the measure side
and decided by the same exact event-cell sweep, and the ceiling family violates them:
`5/4` of charge against a budget of one, once the atom points are placed at interior
vertices of the pairwise intersections rather than at pair centroids.
So the object that caps the point method is itself cut by the language this claim is
about, and the question is whether the cuts hold once the coverage rows are complete.
Spike B’s loop pushed the restricted value below eleven three times and watched the rows
refill it three times; that is the measurement this claim was compressed out of, and it
decides nothing.

The two lane reports behind it are
[lane E](../series/series-000-smoke-and-calibration/results/agenda-032/lane-e-lp-runs-61-16-and-191-50.md),
which shows the point-side loop descending to a floor it cannot cross, and
[lane M0](../series/series-000-smoke-and-calibration/results/agenda-032/lane-m0-fixed-support-polish-191-50.md),
which prices the clique that the threshold language expresses.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
