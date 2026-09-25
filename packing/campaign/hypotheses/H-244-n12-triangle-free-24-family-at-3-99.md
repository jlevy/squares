---
title: H-244 — a triangle-free family of 24 unit squares fits at side 3.99, the n12 capacity-one ceiling
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-244
  kind: hypothesis
  claim: >-
    A family of 24 unit squares inside [0, 399/100]^2, at any angles, exists whose
    interior-overlap graph is triangle-free. If the capacity-one ceiling lemma survives
    review, it follows that no parent-core certificate with point atoms and capacity-one
    threshold atoms proves s(12) > 399/100. The second target is 397/100.
  lane: proof
  derived_from: [X-047]
  criterion:
    shape: determination
    metric: >-
      The verdict of an exact rational checker on a proposed family of 24 squares with
      rational poses: every square inside [0, 399/100]^2, and in each of the 2,024
      triples at least one of the 276 pairs certified interior-disjoint; then the same at
      397/100
    direction: >-
      Confirm the geometric claim only when the exact checker accepts a family; the
      certificate-architecture consequence holds only while the capacity-one ceiling
      lemma has an accepting Fable extra-high review, and without one the family is
      recorded as a geometric fact alone. No family found at the search budget is
      inconclusive and never a refutation. The claim is refuted only by a proof that no
      such family fits, for example a point or capacity-one certificate proving
      s(12) > 399/100 while the lemma stands.
    threshold: 399/100
  instrument: >-
    The H-243 triangle-free family search and exact rational checker, run at n=12,
    built under BC-387 after the lemma review
  instrument_ready: false
  regime: >-
    n=12 architecture ceiling; 24 unit squares at free angles in a square of side
    399/100, then 397/100; exact rational decision of every pair and triple
  instance: {axis: n, point: 12}
  priority: 2
  cost_estimate: Runs of minutes once the H-243 instrument exists
  prereqs: [think-68la]
  replication: false
  registered: '2026-09-25'
  notes: >-
    The n12 sibling of H-243, from the Session 159 n17 assessment
    (docs/project/specs/active/plan-2026-09-25-after-r052-planning.md). It prices the
    n12 parent-core transfer, which waits on this price and on BC-380's parent clip.
    Chains alone give only 18 squares at n12, so the search needs genuinely
    two-dimensional families.
---
# H-244: Where the n12 Certificate Architecture Stops

The same lemma that prices the n17 architecture in H-243 prices n12 with 24 squares
below side 4. A family at $3.99$ would make every point and capacity-one certificate at
n12 stop short of the known packing at side 4, and a family at $3.97$ would bound the
transfer’s whole payoff at about $0.01$ above T-017’s $3.96$.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
