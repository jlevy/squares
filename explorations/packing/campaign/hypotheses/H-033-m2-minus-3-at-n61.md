---
title: H-033 — can the m-squared-minus-3 theorem be extended to n = 61?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-033
  kind: open_question
  claim: >-
    Can Bentz's moving unavoidable-resource method or a strict generalization prove
    s(61) = 8, the m = 8 case of s(m^2 - 3) = m; if not, what retained
    counterconfiguration blocks the m = 7 argument from extending?
  lane: proof
  derived_from: [X-002]
  strategy_refs: ['proof:2', 'proof:6', 'proof:7', 'proof:21']
  instrument: >-
    Express the m = 7 proof as checked moving point/segment resources, substitute m = 8,
    and use a continuous escaping-pose falsifier at each failed forcing step before
    inventing a new resource.
  instrument_ready: false
  regime: unit squares in every side smaller than 8; theorem target n = 61
  instance: {axis: n, point: 61}
  priority: 1
  cost_estimate: paper and symbolic agent-days; numerical falsifiers should remain tier S
  prereqs: [machine-readable Bentz m = 7 certificate]
  replication: true
  registered: '2026-08-24'
  notes: >-
    Bašić-Slivkova gives a specialized piercing lower bound near 7.8906, weaker than the
    Nagamochi value already stored for n = 61. It does not settle this exact-value
    question. H-005 is a distinct upper-bound construction claim at n = 97.
---
# H-033 — attack the next theorem case, not the easiest large search case

The required output is either a replayable proof skeleton or the first explicit pose
that defeats a named generalized forcing step.
Both move the family question forward.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
