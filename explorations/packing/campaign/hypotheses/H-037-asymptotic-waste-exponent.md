---
title: H-037 — what is the asymptotic waste exponent?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-037
  kind: open_question
  claim: >-
    Can the gap between W(x) not in o(x^(1/2)) and W(x) = O(x^(3/5)) be narrowed, and
    which synchronization or geometric obstruction determines the true exponent?
  lane: proof
  derived_from: [X-002]
  strategy_refs: ['search:9', 'proof:12', 'proof:13', 'proof:14']
  instrument: >-
    Reproduce the current lower-bound and construction error balances; use symbolic
    parameter searches to falsify proposed balances, and finite constructor experiments
    only as diagnostics for boundary overhead and synchronization.
  instrument_ready: false
  regime: x tending to infinity, with fractional part and inclination conditions explicit
  instance: {axis: asymptotic-scale, point: x-to-infinity}
  priority: 3
  cost_estimate: parallel paper-mathematics lane; finite diagnostics tier S per parameter family
  prereqs: []
  replication: true
  registered: '2026-08-24'
  notes: >-
    Bui's good-square reduction and the 2025-2026 O(x^(3/5)) constructions are the
    current primary starting points. No finite-n search result determines this question.
---
# H-037 — keep the global frontier visible

This open question prevents the campaign’s common-`n` tooling from becoming the whole
definition of square-packing research.
Its intermediate artifacts are checked derivations and finite synchronization
experiments, not overnight basin counts.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
