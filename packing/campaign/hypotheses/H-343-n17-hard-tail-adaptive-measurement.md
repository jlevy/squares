---
title: H-343 — at least half of the distance-2 residue orbits close under the adaptive-row kernel
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-343
  kind: hypothesis
  claim: >-
    At least 47 of the 94 distance-2 orbit representatives of the 60-entry ledger that
    issue 472's row 23 does not cover close under the 17-owner ownership-induction
    kernel at U = 1169/250 with the SW9 adaptive-row recipe (64 bins, octagon core,
    adaptive rows with floor 1/512 and cap 2,304 rows) within a 2-hour ceiling each,
    with certificates the standing verifier passes in full; and a uniform seeded draw of
    60 orbits from the rest of the residue, run the same way, closes at the same rate
    within a factor of two.
  lane: proof
  derived_from: [X-052]
  criterion:
    shape: determination
    metric: >-
      Per orbit: the producer outcome (closed, fixed point, time cap), rounds, finest
      live row, live rows at the end, production CPU, the full-mode verifier verdict
      and time; for every stall, the support and domains diagnostics of the stall
      classification review (per-owner support fraction, minimal float-placeable
      sub-pattern arity); the closure rate on the 94 and on the 60-orbit draw.
    direction: >-
      Confirm when at least 47 of the 94 close with full-mode passes. Fewer than 47
      refutes the claim and makes the tail a grammar problem (H-344, H-331, H-338);
      more than 47 makes it a throughput problem for the engines in hand. The draw's
      rate is recorded either way as the per-state stall fraction of the current residue.
    threshold: 47 of 94 closures; 2 hours each; full-mode pass; 60-orbit draw within 2x.
  instrument: >-
    devtools/check_n17_subpattern.py on all 17 cells (the per-state path of exp-257)
    with the SW9 adaptive-row recipe; devtools/verify_n17_kernel_certificate.py in full
    mode; devtools/diagnose_n17_flag.py and the stall-classification diagnostics for
    every stall; the exp-274 current partition for the orbit lists, re-partitioned after
    H-341.
  instrument_ready: true
  regime: >-
    n = 17; the H-266 cover at U in the U frame; the distance-2 representatives of the
    current partition after H-341 (94 orbits, 736 states) and a seeded uniform draw of
    60 orbits at distance 4 or more; one run per orbit; stalls recorded, never
    extrapolated.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    At most about 300 CPU-hours (154 orbits at up to 2 hours each) and typically far
    less at the measured medians (0.44 CPU-hour per closure); no build; about 6
    agent-hours for the launches, the classification and the admission rounds.
  prereqs: [H-275, H-276]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-052's direction 2. The record's claim that the distance-2 orbits resist the
    kernel at every row width rests on four runs: one closure (u8, mask 3078077,
    exp-257), one incomplete at the 7,000 s ceiling (u1, mask 1900509), and two fixed
    points at 32 uniform bins (m1964767, m851903), the last two diagnosed
    consistency-limited. The adaptive recipe that closed 26 of 29 counted H-275 draws
    has run on two of the 95 and never at the 2,304-row cap. This measures the tail
    instead of inferring it; the threshold is the point at which the record would call
    the tail a grammar problem rather than a throughput problem.
---
# H-343: Measure the Tail

**Mechanism.** Whole-state closure under the adaptive recipe is the one engine with a
measured closure rate on residue states, and it has been pointed at the distance-2 tail
twice. The float penetrations at $U$ of distance-2 states ($0.009$ to $0.012$ of a side)
are the margins W7 and A closed at, and above the engine’s loss floor; what is unknown
is how many of the 94 are like the two diagnosed states, where the infeasibility is
joint across fifteen or more squares.

**Falsifier.** Fewer than 47 of the 94 close within the ceilings.

**Expected information.** The real size of the hard tail and the per-state stall
fraction on the current residue, neither of which exists in the record, and a stall
classification for every state that resists.

**Limits.** Per-state closure removes at most eight states per certificate and is a tail
method; the 60-orbit draw prices the rest of the residue, it does not close it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
