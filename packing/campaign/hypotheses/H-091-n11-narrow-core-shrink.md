---
title: H-091 — a core above the lost corner event retains a usable mass floor
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-091
  kind: hypothesis
  claim: >-
    With the frozen T-018 atoms, weights, outer side and 181 net directions, every
    admissible core of side 997696/1000000 has mass strictly greater than
    434547/440000. Normalization by the exact minimum and dilation by
    1000007/1000000 then produce a standard certificate at side 381002667/100000000,
    strictly above T-022.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:21']
  criterion:
    shape: determination
    metric: exact minimum covered mass over every admissible net-core placement
    direction: >-
      Pass only if the exact minimum exceeds 434547/440000, the source replay
      succeeds, and the fresh normalized and dilated bytes pass both production
      decision routes and the source-distinct standalone verifier.
    threshold: '434547/440000'
  instrument: packing/devtools/core_shrink.py and the existing certificate verifiers
  instrument_ready: true
  regime: >-
    Frozen source SHA-256 b121edbd044b6f326022d8783551efd947c95eec2738269857d039358ac6ae6a;
    exact rational arithmetic; fixed sites and relative weights; core side
    997696/1000000; dilation 1000007/1000000; at most two sweep workers.
  instance: {axis: n, point: 11}
  sweep: {axis: core side, points: ['997696/1000000']}
  priority: 1
  cost_estimate: About thirty seconds for the two exact sweeps, plus independent retention if positive.
  prereqs: [T-018 frozen certificate, retained exp-110 corner obstruction]
  replication: true
  registered: '2026-09-06'
  notes: >-
    Coordinator satellite think-jthr under think-zq2u, allocated H-091 and exp-111
    outside both managers' ranges. Nonblocking for T-022. Chosen after exp-110,
    prospectively frozen before this point is measured. Never overwrite exp-110
    or change H-090's rejected scope.
---
# H-091 — Test Above the Lost Corner Event

[Exp-110](../series/series-000-smoke-and-calibration/experiments/exp-110-h-090-core-shrink.md)
rejects every fixed-weight core side below $e=1849127/1853400$. It leaves
$e\le b<9977/10000$ open.
This follow-up tests one point in that interval, $b=997696/1000000$. Its distance above
the lost event is $1729/1158375000>0$; passing that necessary condition does not predict
that the other cells retain enough mass.

The acceptance threshold remains $M/11=434547/440000$, not one.
If the exact minimum $m(b)$ exceeds that threshold, divide each weight by $m(b)$ and
dilate the coordinates, core side and outer side by $q=1000007/1000000$. The ordinary
containment slack is exactly $1-qb(1+D)=1565306862839/1406250000000000000>0$. The
resulting side would be $qL=381002667/100000000=3.81002667$. Its squared difference from
T-022’s algebraic endpoint squared is
$58412715474651718514831542282277169/8099933517838416541585210000000000000000>0$. Both
sides are positive, so this exact comparison proves the proposed improvement.

The source and candidate core sweeps are run by the same instrument as H-090. If
coverage fails, retain the new minimum and its admissible worst witness.
If it passes, retain the constructed bytes only after the production sweep and interval
routes and the source-distinct standalone verifier accept those bytes.
An independent mathematical review remains necessary before promoting a new bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
