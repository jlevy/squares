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
  notes: Exp139 rejected this claim. The complete exact181direction replay found minimum760979/800000
    at directions27through32 for the unchanged88atoms. The separately declared normalized feasible mass
    is31219612/3804895, above seven; it is not an optimum-gap proof or packing exclusion.
---
# H140: Full-Net Fixed-Corner Cover

Exp139 rejected this claim after the source-bound exact reader completed
all181directions. The unchanged rationalized residual weights attain minimum
`760979/800000` at direction indices27through32, below the required massone.

No full-net target minimum was inspected before registration, and the reader did not
resolve the LP or edit the atom weights.
The positive minimum gives normalized feasible mass `31219612/3804895`, above seven,
without an optimum-gap or packing claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
