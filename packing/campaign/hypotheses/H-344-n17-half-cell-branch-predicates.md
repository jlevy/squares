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
      mutants. Both children stalling as the parent did on two or more states refutes
      the claim for this predicate and says the mechanism is not the missing seed core.
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
    consistency-limited stalls are exactly the states where owners own nothing from the
    seed (half-diagonal above 1/2 on the side cells) and every partner has a clearing
    pose for every owner pose individually; halving the side cell is the one grammar
    change aimed at that mechanism, and the verifier already accepts n11's predicate
    grammar while the n17 node and consumer do not. It is registered blocked and should
    be built only if H-343 finds the tail to be a grammar problem.
---
# H-344: Give the Owners Something to Own

**Mechanism.** An ownership induction cuts a pose only when every partner pose collides
with it; on the diagnosed stalls every owner is at least 63 per cent supported and
nothing is ever cut.
A closed half-cell child confines one square to half its cell, which gives that square
an owned core from the seed and gives its partners a region they cannot all clear.
Two children covering the parent, seam included in both, is the complete-cover rule the
record asked for.

**Falsifier.** Both children stall as the parent did on two or more of the three states.

**Expected information.** Whether the diagnosed mechanism is the missing seed core or
the joint structure of the wall crowds; an engine for consistency-limited states if the
former.

**Limits.** Unbuilt; a split multiplies the per-state cost; the consumer rule, not the
producer, is what makes a split sound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
