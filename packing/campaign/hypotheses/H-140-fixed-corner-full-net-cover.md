---
title: "H-140 \u2014 fixed-corner rational cover survives the full net"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-140
  kind: hypothesis
  claim: The unchanged rationalized residual-cover atoms from exp136 assign mass at least one to every
    admissible fixed-four-flush-corner residual B-core on all181folded net directions.
  lane: proof
  derived_from: []
  criterion:
    shape: determination
    metric: Exact minimum covered mass over all181directions and their full residual centre domains
    direction: at least one without rescaling
    threshold: '1'
  instrument: packing/devtools/verify_residual_cover_pilot.py
  instrument_ready: true
  regime: L=96/25,B=9977/10000; exp136 residual88atoms of total7804903/1000000, unchanged from Gitblob2b34bdc8842edc836402bd42fe8362e9103ab253;181foldednet
    withD4 symmetry, strict-core transfer.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: One five-minute exact reader,1000atom and2millionperdirectionevent guards; noLP or newweights.
  prereqs:
  - source-binding and independent exact reader controls
  - fullnet transfer proof and nonnegative symmetric source measure
  - published exp139 protocol before exact target replay
  replication: false
  registered: '2026-09-09'
  notes: If raw minimum is positive but belowone, reject the unscaled claim and report the exact normalized
    feasible mass total/minimum as a distinct derived bound. This gives a feasible conditionalcover, not
    an optimum-gap proof or an exclusion unless its mass is belowseven.
---
# H140: Full-Net Fixed-Corner Cover

The numerical nine-direction pilot is positive.
This separate claim tests whether its unchanged rationalized residual weights already
cover every omitted net direction.
No full-net target minimum was inspected to choose the claim.
The exact reader never resolves the LP or edits the atom weights.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
