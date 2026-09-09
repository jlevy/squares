---
title: "H-151 \u2014 some sixth site completes the fixed five-dot cover"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-151
  kind: hypothesis
  claim: For the fixed D and wall tuple (0,0,0,7), some additional site covers every original-D-missed
    residual B-core on the complete retained direction net.
  lane: proof
  derived_from: []
  criterion:
    shape: determination
    metric: A site survives all exact support constraints and passes independent full-net six-dot coverage
    direction: positive
    threshold: '1'
  instrument: packing/devtools/wall_owner_sixth_site_feasibility.py
  instrument_ready: true
  regime: Original five unit sites, same four exp146 selected patches, q=96/25 and B=9977/10000; all 361
    directions; initial site region is the reconstructed two-core intersection.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: One 300-second external process plus two-second grace, one shared 240-second internal
    guard after inputs, at most one final full-net union confirmation.
  prereqs:
  - Complete-domain closure/support proof and independent source admission.
  - Point/segment-safe exact support clipping; augmented-site union confirmation on the same shared absolute
    clock.
  - Clean published prospective protocol and fixed endpoint, wall, exp149 and exp151 bindings.
  replication: false
  registered: '2026-09-09'
  notes: Empty prefix of necessary support constraints completely refutes the fixed-D-plus-one-site family.
    Full-net nonempty intersection supplies a candidate, but acceptance requires independent all-361 exact
    union confirmation. Incomplete support or incomplete confirmation is unresolved; disagreement is invalid.
    This does not decide arbitrary six-site or weighted covers.
---
# H151: Solve for Any Sixth Site

A sixth site must belong to every closed core missed by D. This converts the placement
question into an exact convex intersection in two coordinates.
The [design proof](../../cases/n11_five_dot_cover/direct-sixth-site-contract.md) shows
how complete-domain extrema provide its constraints.

The two-core screen was nonempty.
This experiment now asks about the entire finite-direction, continuous-centre family,
with a separate independent cover confirmation for a surviving candidate.
Source implementation and independent admission are complete;33 combined controls passed
independently in3.41seconds. No target has run; clean prospective publication remains
required.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
