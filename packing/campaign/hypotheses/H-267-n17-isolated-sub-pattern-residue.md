---
title: H-267 — isolated sub-pattern exclusion leaves at most 10^4 n17 occupancy orbits on the minimal cover
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-267
  kind: hypothesis
  claim: >-
    On the H-266 cover, forbidden occupancy sub-patterns of arity at most seven, each
    certified infeasible at cap U by the n11 kernel adapted to n17 or by a
    majority-feature packet, exclude by containment all but at most 10^4 of the D4
    orbits of closed capacity-one assignments, and never exclude the endpoint's state.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: >-
      The exact number of D4 orbits not containing any certified forbidden sub-pattern,
      with the endpoint state surviving as positive control and n11's mask-0 field
      replayed through the same adapter as the method control
    direction: >-
      Confirm if the certified residue is at most 10^4 orbits with every certificate
      independently checked; reject if it exceeds 10^4 at arity seven, or if any
      certified pattern excludes the endpoint state.
    threshold: 10000
  instrument: >-
    A heuristic selector (the bulk-exclusion lane's sampling and descent proxy as a
    retained tool), the n11 v9 kernel adapted to the n17 frame as prover, and an exact
    set-union consumer, to be built after H-266
  instrument_ready: true
  regime: >-
    n=17; cap 1169/250; the H-266 cover; sub-patterns of arity at most seven
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: About a week to adapt the kernel; hours of CPU for the certificates
  prereqs: [H-266]
  replication: false
  registered: '2026-10-02'
  notes: >-
    From the bulk-exclusion design review (its H-F2). n11 excluded 1,904 of its 2,180
    cases with 59 isolated sub-pattern certificates of arity five to seven. An
    exploratory proxy at arity at most five on the 24-cell design flags ten D4 classes
    and leaves 11,939 orbits with the endpoint surviving; arity six already finds the
    analogue of n11's mask-0 wall-row field. Not a certificate: the proxy is a float
    penetration heuristic.
---
# H-267: Isolated Sub-Pattern Exclusion on the Minimal Cover

n11’s census became affordable because most cases contain one of a few small
sub-patterns that cannot be realised at all, so one certificate excludes hundreds of
cases. This hypothesis tests whether the same mechanism brings n17 to a residue that
geometric exclusion at one to two CPU-hours per case can absorb.

## Correction and Selector Results

*Added 2026-10-02 by Session 168.* The exploratory arity-five numbers in the notes above
are false: the retained selector `devtools.select_n17_sub_patterns` places every one of
the proxy’s arity-five flags, and on the unique-state cover it flags nothing at arity
five or below. At arity six it flags three interior-crowd classes; if all three are
certified, 23,354 orbits survive, above this hypothesis’s threshold, so arity seven is
the next measurement.
At arity seven it flags 41 more, 44 in all; if all are certified, 5,084 orbits survive,
below the threshold, with the endpoint surviving.
A second seed flags exactly the same 44 classes.
The thinnest flags (penetration $6.2\times10^{-5}$) are the likeliest to be false.
A priority subset of arity eight adds 46 flags; with all 90 certified, 2,256 orbits
would survive, and the top five arity-eight classes carry 81% of that gain.
The [selector receipts](../explorations/X048-session-168-pilots/README.md) hold the
counts; none of them is a certificate.

## First Certificates

*Added 2026-10-02 by Session 168.* The first two flagged classes are certified and
admitted in
[exp-249](../series/series-000-smoke-and-calibration/experiments/exp-249-h267-n17-first-certified-sub-patterns.md):
W7 by the kernel and A by an interval branch and bound, each re-proved in full by an
independent verifier.
The certified census is 17,690 orbits with the endpoint surviving.
A’s prover is not one this claim names; its review admits the certificate as equivalent,
and exp-249 records that as a deviation in the instrument.

*Added 2026-10-03 by Session 168.*
[exp-250](../series/series-000-smoke-and-calibration/experiments/exp-250-h267-n17-standing-verifier-admissions.md)
admits two more kernel certificates on the standing verifier’s full pass: flag 3, an
arity-9 class named SW9, and N1, a whole 17-cell residue state.
The certified census is 15,953 orbits with the endpoint surviving.
Neither certificate is of arity at most seven, so they move the census but not this
claim’s criterion.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
