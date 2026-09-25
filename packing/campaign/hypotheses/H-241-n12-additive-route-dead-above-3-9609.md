---
title: H-241 — every additive route at n12 is dead above 3.9609
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-241
  kind: hypothesis
  claim: >-
    At n=12, side 39609/10000, shrink 9977/10000, a depth-one family of closed cores
    exists whose total divided by its maximum depth is at least 12, so no nonnegative
    point measure of mass below 12 certifies s(12) above 3.9609.
  lane: search
  derived_from: [X-047, X-044]
  criterion:
    shape: determination
    metric: >-
      The CeilingResult of colgen.check_ceiling after run_fractional_cutting at
      (n, L, B) = (12, 39609/10000, 9977/10000), seeded from T-017's certificate
    direction: >-
      Confirm on a proved ceiling with feasible_total at least 12, accepted by
      verify_ceiling and the independent ceiling reader. Reject when the loop settles
      with a converged value below 12, which reopens a window-enriched point run. An
      unsettled loop decides nothing.
    threshold: 12
  instrument: >-
    devtools/run_fractional_cutting.py with --seed-certificate, colgen.check_ceiling,
    verify_ceiling and independent_ceiling_reader
  instrument_ready: true
  regime: >-
    n=12; side 39609/10000; shrink 9977/10000; point atoms; exact ceiling decision
  instance: {axis: n, point: 12}
  priority: 2
  cost_estimate: One cutting run of about 90 minutes plus the readers
  prereqs: [think-nbij]
  replication: false
  registered: '2026-09-23'
  notes: >-
    A confirm is a decisive negative about a method: it closes rows 216 and 217's point
    control, H-228's additive form and density transfer at n12 from 3.961 up, and
    leaves n12 to threshold or structural arguments.
---
# H-241: Every Additive Route at n12 Is Dead Above 3.9609

X-047 estimates n12’s remaining additive headroom at about $0.001$ above T-017’s $3.96$.
One cutting run with the ceiling reader decides that in one direction, for every site
set, and so settles which n12 routes are worth an instrument.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
