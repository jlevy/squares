---
title: H-090 — smaller cores preserve a usable mass floor on the T-018 atoms
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-090
  kind: hypothesis
  claim: >-
    With the frozen T-018 atoms, weights, outer side and 181 net directions, every
    admissible core of side 99769/100000 has mass strictly greater than
    434547/440000. Normalization by the exact minimum and dilation by
    100001/100000 then produce a standard certificate at side 38100381/10000000.
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
    99769/100000; dilation 100001/100000; at most two sweep workers.
  instance: {axis: n, point: 11}
  sweep: {axis: core side, points: ['99769/100000']}
  priority: 1
  cost_estimate: One source replay, one candidate replay, and independent retention if positive.
  prereqs: [T-018 frozen certificate]
  replication: true
  registered: '2026-09-06'
  notes: >-
    Coordinator satellite think-zq2u, allocated H-090 and exp-110 outside the two
    managers' reserved ranges. Nonblocking for T-022. A failure at this rational
    side does not rule out a smaller reduction or reoptimized weights.
---
# H-090 — Shrink the Core Before Dilating

Write $M=434547/40000$ for the fixed total mass and $m(b)$ for the least mass of an
admissible side-$b$ core over the retained net.
If $m(b)>M/11$, dividing every weight by $m(b)$ gives least covered mass one and total
mass below eleven. This permits a decrease of $5563/440000$ from the source minimum
$4001/4000$.

The first candidate uses $b=99769/100000$ and $q=100001/100000$. Its ordinary
containment slack is exactly $1-qb(1+D)=3714298841717/900000000000000000>0$. If coverage
passes, the resulting bound $qL=38100381/10000000=3.8100381$ exceeds T-022’s algebraic
endpoint by more than $1/100000$; this comparison is by squares of positive exact
quantities, not floating-point subtraction.

This hypothesis is frozen before its first measurement.
The [idea board](../ideas.md) locates it within the strategy portfolio.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
