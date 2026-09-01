---
title: H-059 — the frozen n = 50 producer refuses before every downstream seam
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-059
  kind: hypothesis
  claim: >-
    For the frozen n = 50 source-semantics producer and immutable existing exp-050
    result, the existing-result branch refuses before binding observation, fixture
    loading, receipt evaluation or publication, producing a canonical zero-call stage
    trace under normal and optimized Python.
  lane: search
  derived_from: [X-011]
  strategy_refs: ['search:20']
  criterion:
    shape: determination
    metric: >-
      producer-runner digest, immutable result digest, exact refusal text, canonical
      stage-sentinel trace and per-seam call counts under normal and optimized Python,
      plus runner-hash, reordered-stage, changed-result and overwrite mutations
    direction: >-
      accepted only if both runtimes bind the frozen producer and result, emit the same
      refusal and zero-call trace, leave exp-050 byte-identical and reject every mutation;
      rejected if a bound downstream seam fires before refusal; unresolved if provenance,
      injection, equivalence or independent verification is incomplete
    threshold: zero calls to every downstream seam before the existing-result refusal
  instrument: >-
    Agenda-014 BC-125 builds a separate injected sentinel harness, binds the producer
    before import, injects bomb functions into all four downstream seams, independently
    admits the frozen harness, executes one fresh prospective control result and verifies
    it without importing the producer.
  instrument_ready: false
  regime: >-
    Producer SHA-256
    52baeb1b6ad52aa504498ba21aeb6b3d361aaaec2461c76904a357d8d95cf29d and exp-050
    result SHA-256
    ab00e50debe0bc60279ce3472ed0c09eb062e8271a481a38c6ac65036aff4a02 are fixed.
    Exp-050 is read-only. No source, n = 19 geometry or n = 50 geometry is inspected.
  instance: {axis: n, point: 50}
  priority: 1
  cost_estimate: >-
    one 150-minute preregistration, target-blind harness, independent admission,
    prospective control and review block in 15--25-minute cells
  prereqs:
  - independently reviewed Packet C bounded caveat
  - frozen producer and exp-050 result hashes
  - injectable downstream seams and normal/optimized execution
  replication: false
  registered: '2026-09-01'
  notes: >-
    A pass validates this prospective protocol only. It cannot retroactively bind the
    producer to exp-050, clear exp-050 review, change H-054, establish n = 50 feasibility
    or serve as an H-055 source-cell control.
---
# H-059 — `n = 50` Producer Refusal Ordering

The claim makes the W5 provenance lesson falsifiable without rewriting the frozen result
that exposed it. Ordering is tested by executable sentinels, not inferred from source
layout.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
