---
title: H-344 — closed half-cell branch predicates close the consistency-limited stalls
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-344
  kind: hypothesis
  claim: >-
    With a branch predicate that halves one named side cell along its long axis into two
    closed children whose seam belongs to both, each child seeded with the owned core
    the halved cell now provides, and a consumer rule that admits the parent only when
    every child is admitted, the 17-owner kernel at U = 1169/250 under the SW9 adaptive
    recipe closes both children of at least two of the three diagnosed
    consistency-limited states (m1964767, m851903, m1949551) within four times the
    parent's stalled run time each, with certificates the standing verifier passes in
    full.
  lane: proof
  derived_from: [X-052]
  criterion:
    shape: determination
    metric: >-
      Per state and child: the halved cell, the child's seed core, the producer outcome,
      rounds, production CPU relative to the parent's stall, the full-mode verifier
      verdict; the consumer's refusal of a parent with one child missing, one child at a
      different cap, or a seam assigned to one child only.
    direction: >-
      Confirm when at least two of the three states have both children closed within 4x
      the parent's time and the consumer admits the parent and refuses the three
      mutants. Fewer than two states with both children verified closed within each
      child's ceiling refutes the registered closure-budget claim for this predicate
      and configuration. A failed consumer control rejects the instrument. Either result
      alone does not disprove a seed-core mechanism or every refinement of the kernel.
    threshold: 2 of 3 states; both children each; 4x parent time; full-mode pass; 3 of 3 consumer mutants refused.
  instrument: >-
    Unbuilt: the n17 node grammar and devtools/census_n17_certified.py extended with a
    closed half-cell predicate in the pattern the verifier already accepts for n11's
    predicate grammar; devtools/check_n17_subpattern.py seeding from the child's cell;
    devtools/verify_n17_kernel_certificate.py in full mode; a consumer mutation suite.
  instrument_ready: false
  regime: >-
    n = 17; the H-266 cover at U; the three diagnosed states of the stall-classification
    review (two at distance 2, one at distance 4) as frozen targets; the halved cell
    chosen as the side cell whose owner is least supported in the diagnostics.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: >-
    One build slice plus review (one to two weeks of one agent); runs at two to four
    times a parent's cost, about 2 CPU-hours per state; the consumer suite in the same
    slice.
  prereqs: [H-343]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-052's direction 7, the record's candidate C5 made a registered claim. The
    diagnosed consistency-limited stalls have side-cell owners with no owned seed
    (half-diagonal above 1/2 on their unsplit cells), while every partner has a clearing
    pose for every owner pose individually; halving the side cell is the one grammar
    change aimed at that mechanism, and the verifier already accepts n11's predicate
    grammar while the n17 node and consumer do not. It is registered blocked and should
    be built only if H-343 misses the declared closure budget or its scoped diagnostics
    otherwise justify this comparison; that trigger is an operational choice, not a
    proof that the tail has a grammar obstruction.
---
# H-344: Give the Owners Something to Own

**Mechanism.** An ownership induction cuts a pose only when every partner pose collides
with it; on the diagnosed stalls every owner is at least 63 per cent supported and
nothing is ever cut.
A closed half-cell child confines one square to half its cell, which gives that square
an owned core from the seed and gives its partners an additional region to avoid.
The run measures whether this removes poses.
Two children covering the parent, seam included in both, is the complete-cover rule the
record asked for.

**Falsifier.** Fewer than two of the three states have both children verified closed
within the per-child ceiling.
A child timing out misses this budget without proving a fixed point; a failed consumer
control rejects the instrument rather than the geometry.

**Expected information.** Whether adding the registered seed cores improves closure
within this budget, and whether it supplies verified exclusions for the diagnosed
states.

**Limits.** Unbuilt; a split multiplies the per-state cost.
The complete-cover consumer rule makes the split sound.
Timed stalls provide comparative evidence for this predicate and configuration, without
establishing a structural impossibility.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
