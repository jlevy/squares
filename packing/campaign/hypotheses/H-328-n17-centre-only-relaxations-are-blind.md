---
title: H-328 — centre-only relaxations exclude nothing at the cap
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-328
  kind: hypothesis
  claim: >-
    Every relaxation of the n17 problem at U = 1169/250 that keeps only the centre box
    and pairwise centre distances at least one is blind to the packing: twenty such
    centres fit in the box, and on the H-266 cover every one of the 2,024 cell triples
    has a product vertex at which all three pairwise squared distances are at least
    1.3299, so no weighted-vertex certificate and no no-ball order-2 incircle SOS
    certificate exists for any triple of original cells; accordingly the frozen
    first-eight shared-centre LP returns an exact primal survivor for every one of its
    eight states.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      Three exact computations: the twenty-point witness checked in rationals; for every
      cell triple, an exact product vertex with all three squared distances at least 1
      (the float computation of X-051 found margin 0.3299); and the eight exact
      dispositions of the first-eight LP (primal survivor, Farkas certificate,
      unresolved) as the think-dvcs pilot records them.
    direction: >-
      Confirm when the witness and the triple check pass exactly and the pilot records
      eight exact primal survivors. Two or more exact Farkas certificates among the eight
      refute the LP part; a triple without such a vertex refutes the triple part and
      revives the weighted screen for that triple.
    threshold: 20 points, minimum squared distance exactly 1; 2,024 triples, all with margin; 0 Farkas certificates of 8.
  instrument: >-
    A small exact script over devtools.check_n17_capacity_one_cover.build_cover for the
    witness and the triples (to be retained as a devtools check under OR-1); the
    first-eight pilot of devtools/n17_shared_centre_lp.py once its producer is
    implemented and registered.
  instrument_ready: false
  regime: >-
    n = 17; the H-266 cover in the centre box [1/2, U - 1/2]^2; the frozen first-eight
    masks 849919, 850943, 851839, 851903, 916351, 980927, 981887, 1630207; exact rational
    arithmetic throughout.
  instance: {axis: n, point: 17}
  priority: 3
  cost_estimate: >-
    Minutes for the two geometric checks; the LP pilot's own registered allocation
    (120 s construction, 120 s fresh check per phase) for the eight states.
  prereqs: [H-266, H-324]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051 section 3. The witness is x = 1/2 + c + (1/2 if the row is odd), y = 1/2 +
    r * 8661/10000, r = 0..4, c = 0..3; max y = 9911/2500 < 522/125; minimum squared
    distance exactly 1 over 190 pairs. The triple result applies PR 464's mixture
    obstruction with a point mass at the found vertex. A confirmation retires centre-only
    relaxations as proof engines for n17 and leaves orientation-aware generators (full
    separating-axis branches, ball-augmented or higher-order recipes) unpriced rather
    than refuted.
---
# H-328: What Centre Distances Alone Can See

**Mechanism.** Every unit square contains the open disk of radius $1/2$ about its
centre, so its centre lies in the centre box and two centres are at least one apart.
A relaxation that keeps only these facts is a disk-packing problem, and twenty unit
disks fit in the box of side $3.676$ (hexagonal rows at pitch $8661/10000$). Exclusion
of a cell assignment can then come only from the shapes of the seventeen named cells,
and the triple computation shows that no three cells are tight enough for the
weighted-vertex screen.

**Falsifier.** Two or more exact Farkas certificates among the first eight states, or a
cell triple with no product vertex at which all three pairwise distances are at least
one.

**Expected information.** Whether the shared-centre LP and the incircle SOS deserve any
further mathematical investment, decided by a prediction frozen before the pilot runs.

**Limits.** The claim says nothing about relaxations whose generators see orientation,
such as the eight separating-axis branches per pair, and nothing about the LP’s value as
a calibration of the exact adapter, which exp-316 already established.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
