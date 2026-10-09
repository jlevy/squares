---
title: H-331 — learned-weight angle splits bring branch and bound to the hard tail
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-331
  kind: hypothesis
  claim: >-
    With the B2 branching rule of issue 367 (Farkas multiplier shares accumulated per
    square, the widest-eligible square of largest learned weight bisected), the interval
    branch and bound at cap U = 1169/250 closes at least three of the ten
    smallest-margin sub-patterns of arity at most ten drawn from the 95 distance-2
    residue orbits within 10^6 nodes each, with certificates the standing BB verifier
    passes in full.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      Node count, outcome and verifier verdict for each of ten targets, the targets being
      the ten distance-2 orbits whose H-327 minimal infeasible sub-pattern has the largest
      penetration among those of arity at most ten; the default rule run on the same ten
      as the matched control.
    direction: >-
      Confirm when at least three targets close within 10^6 nodes under B2 and pass full
      verification. Fewer than three refutes the claim for this rule and node ceiling.
      Closures under the default rule count toward the control, not the claim.
    threshold: 3 of 10; 10^6 nodes; full-mode verifier pass.
  instrument: >-
    devtools/pilot_n17_subpattern_bb.py with an opt-in B2 module (about 200 lines
    wrapping Solver.children and Solver.assess, as issue 367 describes, unmerged), the
    native evaluator for search and the Python path for certificate recording;
    devtools/verify_n17_bb_certificate.py in full mode with the PR 452 lifetime repair;
    the think-t41a source-cell enclosure guard on every certificate.
  instrument_ready: false
  regime: >-
    n = 17; the H-266 cover at U; ten frozen targets from H-327's receipts; one run per
    target per rule; a certificate size ceiling of 2 GB per target, above which the run is
    recorded incomplete rather than admitted.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: >-
    Twenty runs at about a thousand nodes a second natively, up to 20 CPU-hours of
    search; verification at 37 ms a node, up to 10 CPU-hours per closed certificate; one
    W7 slice plus review for the B2 module.
  prereqs: [H-327]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route E. The contributor reports trees 11 and 14 times smaller on two
    arity-7 classes and 30,822 against 41,958 nodes on pattern A, and row 33's estimated
    116-million-node tree shows the rule does not make every tree small. The rule
    changes search order only; closure arithmetic is the unchanged outward-rounded dual
    bound. A certificate too large to verify is recorded as such; size per orbit
    excluded is the routing figure.
---
# H-331: Aimed Splits on the Tail

**Mechanism.** On the flagged classes the contradiction lives among a few squares along
a wall, and the default rule refines squares that never appear in the closing
certificates, roughly doubling the tree per such split.
Accumulated Farkas shares aim the angle splits at the squares the duals use, which the
contributor measured at depth 12 to 14 against 25 for random dives.
The hard tail is where the margins are smallest and the trees largest; whether the rule
reaches it is the question.

**Falsifier.** Fewer than three of ten targets closed within $10^6$ nodes.

**Expected information.** Whether branch and bound, the only engine that closed interior
crowds, is an engine for the tail at an affordable certificate size.

**Limits.** The rule is unmerged and must be reviewed on frozen small inputs first;
verification cost per node, not search speed, bounds admission; and a closure of a
sub-pattern excludes the orbit only through the ordinary containment join.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
