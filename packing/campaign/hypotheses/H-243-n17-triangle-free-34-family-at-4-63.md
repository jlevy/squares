---
title: H-243 — a triangle-free family of 34 unit squares fits at side 4.63, the n17 capacity-one ceiling
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-243
  kind: hypothesis
  claim: >-
    A family of 34 unit squares inside [0, 463/100]^2, at any angles, exists whose
    interior-overlap graph is triangle-free. If the capacity-one ceiling lemma survives
    review, it follows that no parent-core certificate with point atoms and capacity-one
    threshold atoms proves s(17) > 463/100. The second target is 465/100.
  lane: proof
  derived_from: [X-047]
  criterion:
    shape: determination
    metric: >-
      The verdict of an exact rational checker on a proposed family of 34 squares with
      rational poses: every square inside [0, 463/100]^2, and in each of the 5,984
      triples at least one of the 561 pairs certified interior-disjoint; then the same at
      465/100
    direction: >-
      Confirm the geometric claim only when the exact checker accepts a family; the
      certificate-architecture consequence holds only while the capacity-one ceiling
      lemma has an accepting Fable extra-high review, and without one the family is
      recorded as a geometric fact alone. No family found at the search budget is
      inconclusive and never a refutation. The claim is refuted only by a proof that no
      such family fits, for example a point or capacity-one certificate proving
      s(17) > 463/100 while the lemma stands.
    threshold: 463/100
  instrument: >-
    A triangle-free family search and an exact rational checker for containment and
    pairwise interior-disjointness, to be built under BC-387 after the lemma review
  instrument_ready: false
  regime: >-
    n=17 architecture ceiling; 34 unit squares at free angles in a square of side
    463/100, then 465/100; exact rational decision of every pair and triple
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    About one hour of Fable extra-high lemma review, four to six hours of Opus
    extra-high build, then runs of minutes
  prereqs: [think-68la]
  replication: false
  registered: '2026-09-25'
  notes: >-
    From the Session 159 n17 assessment
    (docs/project/specs/active/plan-2026-09-25-after-r052-planning.md). Every atom R052
    and Kleddamag use has capacity one, and two cores that trigger a capacity-one atom
    overlap; so a triangle-free family of N squares makes the dual weight 1/2 per square
    feasible for every point or capacity-one certificate, and N = 34 refutes all of them
    at that side. R052 itself shows no such family fits at 4.62002; two copies of
    Bidwell's packing give a bipartite one at 4.6755. The lemma is derived but not yet
    reviewed.
---
# H-243: Where the n17 Certificate Architecture Stops

R052’s certificate is nearly saturated: most of its rows sit within a relative $10^{-3}$
of the binding charge, and reweighting would buy about $0.0014$ of side at most.
The question that decides whether a first-party producer is worth building is how far
this architecture could reach in principle.

If the capacity-one ceiling lemma holds, a family of 34 unit squares with no three
pairwise overlapping bounds every point and capacity-one certificate from above.
The architecture’s ceiling lies between R052’s $4.62002$ and two copies of Bidwell’s
packing at $4.6755$; a family at $4.63$ or $4.65$ locates it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
