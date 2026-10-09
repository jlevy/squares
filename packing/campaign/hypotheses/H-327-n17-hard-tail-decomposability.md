---
title: H-327 — most distance-2 residue orbits contain an infeasible sub-pattern of arity at most ten
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-327
  kind: hypothesis
  claim: >-
    At least 60 of the 95 distance-2 residue orbits of the 60-entry ledger contain a
    sub-pattern of at most ten of their seventeen cells that the retained float
    selector cannot place at U = 1169/250 with best penetration at least 5e-3, so the
    hard tail is mostly decomposable into sub-pattern exclusions rather than jointly
    infeasible.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      For each of the 95 orbits, the minimal-arity sub-pattern the survey's
      minimal-sub-pattern search fails to place, with its best penetration, from
      devtools.survey_n17_residue on the current partition with the default rounds and
      three seeds.
    direction: >-
      Confirm when at least 60 orbits report a minimal infeasible sub-pattern of arity at
      most ten with penetration at least 5e-3 under every seed. Fewer than 60 refutes the
      claim and says the tail needs whole-state or coupled methods.
    threshold: 60 of 95; arity at most 10; penetration at least 5e-3; three seeds.
  instrument: >-
    devtools.survey_n17_residue --distance 2 --sample 0 with its minimal-sub-pattern
    stage, run from a clean worktree on the exp-259 partition, with a receipt per orbit;
    the endpoint's own state as the positive control, which must place.
  instrument_ready: true
  regime: >-
    n = 17; the H-266 cover at U; the 95 distance-2 orbits of the exp-259 partition;
    float search only, three seeds; no exact certificate is produced.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: About 95 orbits at 205 s per shard of the survey, 5 to 15 CPU-hours with three seeds.
  prereqs: [H-276]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route F. The stall classification of 5 October found a 14-cell sub-pattern
    of the distance-2 state m1964767 placeable, so that state needs at least fifteen
    cells jointly, and m851903's minimal sub-pattern had arity 15. If that is typical,
    sub-pattern branch and bound (H-331) cannot reach the tail and the tail is a
    whole-state problem; if it is not, the tail is a sub-pattern problem with a known
    engine. Either answer routes the next exclusion slice.
---
# H-327: Does the Hard Tail Decompose?

**Mechanism.** A state is excluded by containment when any of its sub-patterns is
infeasible, and small sub-patterns have the small trees and small certificates.
The two distance-2 stalls diagnosed on 5 October needed fifteen or more cells jointly,
which is the worst case for every per-pattern engine.
The survey’s minimal-sub-pattern search gives, per orbit, a float lower bound on the
arity any certificate must have.

**Falsifier.** Fewer than 60 of the 95 orbits with a minimal infeasible sub-pattern of
arity at most ten.

**Expected information.** Whether the tail is a sub-pattern problem (route the branch
and bound and the contributors’ rules at it) or a joint one (route grammar changes, the
state-conditioned charge of H-338, or the cap ladder’s pricing at it).

**Limits.** Float search gives a lower bound on the arity, never an upper one, and a
placeable sub-pattern says nothing about the whole state.
The penetration threshold is the selector’s own scale; it does not predict closure.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
