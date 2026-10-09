---
title: H-328 — centre-only relaxations exclude no distance-2 orbit at the cap
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-328
  kind: hypothesis
  claim: >-
    At U = 1169/250 on the H-266 cover, relaxations that keep only each centre's
    assigned cell and pairwise centre distances at least one exclude no distance-2
    residue orbit. Each of the 95 distance-2 orbit representatives, the frozen
    first-eight states included, has exact rational centres inside its own closed cells
    pairwise at distance at least one, and build_model and check_primal of
    devtools/n17_shared_centre_lp.py accept them; so the frozen first-eight shared-centre
    LP has eight exact primal survivors and no Farkas certificate. Every one of the 2,024
    cell triples has a product vertex at which all three pairwise squared distances are
    at least 562823713/423200000; that vertex is a feasible point of the triple's encoded
    system, so no weighted-vertex certificate and no incircle SOS certificate of any
    order, with or without a ball generator, exists for any triple of original cells.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      A replay of the retained evidence. For each of the 96 vectors in
      packing/campaign/explorations/X051-centre-survivors/centre-survivors.json (the
      endpoint control, the first eight and the other 87 distance-2 representatives):
      check_primal's acceptance against build_model's rows, the row count, and the exact
      minimum pairwise squared distance. Over the 2,024 cell triples: the exact minimum
      of the best product vertex's smallest pairwise squared distance.
    direction: >-
      Confirm when every retained vector is accepted with its recorded row count and an
      exact minimum squared distance at least 1, and the triple minimum is at least 1.
      The outcome is already known from the W2 review and the replay in X-051; a round
      only registers it. A Farkas certificate cannot exist for a state with an exact
      feasible primal, so the earlier Farkas-count falsifier is moot. A rejected vector
      or a triple minimum below 1 would expose a defect in the retained vectors or the
      checker; it refutes the record and reopens that state or triple.
    threshold: >-
      96 of 96 vectors accepted with minimum squared distance at least 1 (8 of 8
      first-eight states, 95 of 95 distance-2 representatives, the endpoint control);
      triple minimum 562823713/423200000, at least 1, over 2,024 of 2,024 triples.
  instrument: >-
    The two python -c replays in X-051 sections 3.1 and 3.2, run from packing/ with the
    project interpreter: devtools.n17_shared_centre_lp.build_model and check_primal over
    the retained vectors and the exp-247 receipt's cells, and an exact Fraction
    computation over the same cells.
  instrument_ready: true
  regime: >-
    n = 17; the H-266 cover in the U frame, every cell inside the centre box
    [1/2, U - 1/2]^2; the 95 distance-2 orbit representatives of the exp-308 descriptor,
    among them the frozen first-eight masks 849919, 850943, 851839, 851903, 916351,
    980927, 981887 and 1630207, with the endpoint's state 1900015 as a control; exact
    rational arithmetic throughout.
  instance: {axis: n, point: 17}
  priority: 3
  cost_estimate: >-
    Under a minute for both replays on one core; no producer run, since the vectors are
    retained.
  prereqs: [H-266, H-324]
  replication: false
  registered: '2026-10-09'
  notes: >-
    Re-scoped on 9 October after the W2 review of X-051
    (https://github.com/jlevy/squares/pull/473#pullrequestreview-5469083247). The first
    version predicted the first-eight LP's outcome from a twenty-point witness in the
    centre box. That witness cannot decide a per-state LP, which keeps each centre's
    cell, and the old falsifier ("two or more Farkas certificates") left exactly one
    certificate as neither outcome. The W2 review settled both: it found exact per-state
    primals for the first eight (755, 755, 758, 758, 811, 811, 811 and 752 rows; the
    endpoint control gives 810, as in exp-316), found unit-separated centres for all 95
    distance-2 representatives, and replayed the triple computation exactly. The X-051
    correction regenerated the other 87 vectors with the same search and retained all
    96; the replay accepts them. No W6 round has registered any of this, so the
    hypothesis reads as open until one does, and its expected information is
    registration only. A survivor is relaxation survival: not a packing, an exclusion or
    an admission.
---
# H-328: What Cells and Centre Distances Can See

**Mechanism.** Every unit square contains the open disk of radius $1/2$ about its
centre, so two centres are at least one apart.
The shared-centre LP, the weighted-vertex screen and the incircle SOS generators keep
that fact and each centre’s assigned cell, and nothing about orientation.
Such a relaxation can exclude a state only when its seventeen cells cannot host
seventeen unit-separated centres.
The distance-2 states can host them, and every cell triple has a product vertex at which
all three incircle generators are nonnegative, a point at which no certificate identity
of any order can hold.

**Status.** Determined by the W2 review and the replay retained with X-051, pending a
round that registers it.
The ledger reads it as open because no round has.

**Falsifier.** Moot as a prediction: a Farkas certificate cannot exist for a state whose
relaxation has an exact feasible primal, and an SOS identity cannot hold at a feasible
point. A replay can still expose a defect: a retained vector that `check_primal` rejects
or whose minimum squared distance is below one, or a triple minimum below one.

**Expected information.** None about the mathematics, since the outcome is known.
A round turns a review computation into a registered verdict with its replay retained.

**Limits.** Relaxation survival is not a packing: squares centred at these points may
overlap. The claim says nothing about relaxations whose generators see orientation, such
as the eight separating-axis branches per pair.
Its per-state part says nothing about states at distance 4 or more, where only the
triple part applies, and nothing about the LP’s value as a calibration of the exact
adapter, which exp-316 already established.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
