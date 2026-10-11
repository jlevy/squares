---
title: "H-288 \u2014 exact frozen numeric capture cap"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-288
  kind: hypothesis
  claim: The frozen numeric cap bounds the endpoint side over the complete accepted
    root inclusion with strictly positive excess no greater than1e-12, using exact
    monotone and outward consumer enclosures.
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: exact_capture_cap_full_root_join
    direction: criterion_met
    threshold: Fresh accepted full root R and exact endpoint side/derivative identities;
      0<t_lo<=t_hi<1, positive denominator, negative derivative numerator; exact monotone
      [F(t_hi),F(t_lo)] and unchanged outward consumer side enclosure; fixed Uprime=935106018721/200000000000
      strictly above both upper endpoints with Uprime-minus-each-lower endpoint <=1e-12,
      and Uprime<=1169/250. Generation and new-process checker agree, cap_certified=true,
      all capture/leaf/global/relabel/producer flags false.
  instrument: packing/devtools/check_n17_capture_cap.py and focused synthetic controls;
    corrected pilot side.lo upper-excess guard. Defect think-p13m.
  instrument_ready: true
  regime: Root-only fresh accepted R, frozen Uprime935106018721/200000000000 and outer
    U1169/250; no H278 dependency, producer or relabelling of old None/U objects.
  instance:
    axis: n
    point: 17
  priority: 1
  cost_estimate: 180s combined exact generation and fresh checker; TERM180/KILL190.
  prereqs:
  - H-255
  replication: false
  registered: '2026-10-07'
  notes: SoleAstra mathematicalsourceclear; independentSol26controls2.87s. Registered
    beforeactualroot/cap evaluation; fixed180s combinedgenerator/freshchecker, root/caponly
    no oldobjectrelabel or capture/globalclaim.
---
# H-288: Exact Root/Cap Join

Certify only the frozen rational cap against the full fresh accepted root inclusion.
Bind $F(t)=(6+4t)/(1+2t-t^2)$ to the endpoint layout symbolically and verify
$F'(t)=4(t^2+3t-2)/(1+2t-t^2)^2$. Retain both the monotone side box and the outward
consumer box. Require the cap strictly above both upper endpoints and its excess over
each lower endpoint at most $10^{-12}$.

The defect tracked by `think-p13m` is the distinction between `cap-side.hi` (minimum
excess) and `cap-side.lo` (maximum all-root excess).
A small minimum alone cannot prove the stated bound.
The pilot correction preserves the strict minimum and checks the maximum.

This receipt proves no endpoint cell containment, captured leaf, exclusion or census
change. Old None/U objects keep their original frame; a later numeric-cap producer
requires new seed, registration and fresh saved-state replay.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
