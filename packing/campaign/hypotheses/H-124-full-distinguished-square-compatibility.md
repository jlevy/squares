---
title: H-124 — full distinguished-square compatibility
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-124
  kind: hypothesis
  claim: >-
    At q=1939/500, every contained closed unit square Q in the actual near45
    angle band, with center in [1,q/2] times [0,1] and avoiding all ten original
    Stromquist P10 marks, intersects every contained closed unit square S in
    either actual near-axis or near45 band that avoids the nine unchanged B–J marks.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:9', 'proof:10', 'proof:15']
  criterion:
    shape: determination
    metric: complete full-square compatibility in both actual closed angle bands
    direction: >-
      Accept only a complete independently checked implication over every
      admissible Q and S, including all seams. Reject only one independently
      checked closed-disjoint pair meeting every stated condition. Finite
      no-witness output, failed sufficient guards, errors and timeouts are unresolved.
    threshold: every admissible pair intersects
  instrument: >-
    Source-free-controlled exact event-cell discriminator for one fixed S and
    one Q frame, with an independently implemented corner/SAT witness reader.
    A complete continuous-angle proof instrument is not yet available.
  instrument_ready: true
  regime: Fixed q, unchanged P10 and B–J coordinates, canonical Q center and both full closed angle bands; closed tangency counts as intersection.
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: Two twenty-minute source-free authors in parallel, independent reviews, then a separately capped prospective discriminator if ready.
  prereqs: [independent instrument controls and review, committed prospective target protocol, actual-angle and all-mark witness validation]
  replication: false
  registered: '2026-09-07'
---
# H-124 — Keep the Full Distinguished Square

This is the changed BC255 obligation selected under `think-7e72` after H110 and H123
were accepted and H122 was refuted.
No H124 target has run.
The producer and independent reader passed27 source-free controls and independent
reviews by08:09:33UTC. A committed prospective protocol remains required before
scientific execution.

Write q=1939/500. The actual angle bands, modulo square quarter turns, are
[-pi/720,pi/720] and [pi/4-pi/720,pi/4+pi/720]. Both closed unit squares must lie in
[0,q]^2. Q uses the second band and the canonical center region [1,q/2] x [0,1].
Avoiding a mark means the mark is outside the closed square, not on its boundary.
Q avoids all ten P10 marks; S avoids all nine unchanged B–J marks.

The coordinates are the original `point_sets(q)` definitions in
[restricted_orientation.py](../../cases/stromquist/restricted_orientation.py), not the
different fixed-side `source_points(field)` calibration.
The B–J formulas also appear in
[H122](H-122-diamond-conditional-nine-point-cover.md#fixed-domain-and-data).

## What a Complete Proof Would Buy

The reviewed
[counting reduction](../series/series-000-smoke-and-calibration/results/agenda-026/bc-255-conditional-compatibility-assessment.md#the-counting-reduction)
scales any hypothetical strict-sublevel eleven-square packing to side q and takes
pairwise-disjoint closed unit cores.
One core avoids P10. H106 makes it near45; H123 and a global coordinate-midline
reflection put it in the canonical region.
Call that core Q. Each other core must then contain one of the nine B–J marks if H124
holds, contradicting ten disjoint cores and nine marks.

No forced-anchor or fixed-diamond lemma is required for this full-square implication.
Those lemmas remain valid optional pruning facts.
Replacing Q by a common obstacle forgets correlations between its shape and position;
H122’s negative result does not settle H124.

A verified disjoint Q/S pair would refute this sufficient compatibility statement only.
It is not an eleven-square packing and does not refute H036 or change the global bound.

## First Proposed Discriminator

Keep the exact S from the retained exp122 packet unchanged and use the single exact45
frame for Q. Enumerate Q’s exact event strata against all ten marks, intersect their
closures with the canonical region, and reconstruct a strict-stratum witness after
clipping.
For each signed edge-normal axis of either square, the separating gap is affine
in Q’s center. A positive closure-vertex gap can be retained while moving into the
required strict stratum.
Degenerate clipped strata and open boundaries need explicit source-free controls.

The independent reader reconstructs unit-square geometry and all mark-edge tests from
exact ordered corners, verifies actual angles and containment, binds unchanged S to the
retained source, and requires a strict separating-axis gap.
There are76 point-edge determinants for the ten plus nine marks.
Across eight corners there are16 coordinate containment checks, or32 lower/upper scalar
wall inequalities. Tangency is not a witness.

This finite slice can refute the hypothesis but cannot accept it.
Even exhaustive no-witness output for this S and frame leaves all other S and continuous
Q angles open. There is no automatic second frame, changed S, larger cap or
completed-target retry.
The exact invocation and budgets belong in a separate prospective experiment.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
