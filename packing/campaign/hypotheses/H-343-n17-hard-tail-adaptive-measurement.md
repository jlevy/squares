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
    kernel at U = 1169/250 with SW9's adaptive-row recipe (64 bins, octagon core,
    adaptive rows with floor 1/512) and its row cap raised from 1,152 to 2,304 rows,
    within a 2-hour production ceiling each, with certificates the standing verifier
    passes in full; and a uniform seeded draw of 60 orbits from the rest of the residue,
    run the same way, closes at the same rate within a factor of two.
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
      Confirm when at least 47 of the 94 close with full-mode passes and the 60-orbit
      draw closes at a rate within a factor of two of the 94's. Fewer than 47 refutes the
      claim and makes the tail a grammar problem (H-344, H-331, H-338); 47 or more makes
      it a throughput problem for the engines in hand, and a draw rate outside the factor
      of two then refutes only the draw conjunct, saying the tail and the rest of the
      residue differ in kind. The draw's rate is recorded either way as the per-state
      stall fraction of the current residue.
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
    At most 308 CPU-hours of production (154 orbits at up to 2 hours each) plus
    full-mode verification, whose cost at a 2,304-row cap is unmeasured: the only
    2,304-row run in the record (flag 2) ended INCOMPLETE at its 12,000 s ceiling.
    Typically far less at the measured medians (0.44 CPU-hour per closure); no build;
    about 6 agent-hours for the launches, the classification and the admission rounds.
  prereqs: [H-275, H-276, H-341]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-052's direction 2, as corrected by the W2 review of 9 October. The record's claim
    that the distance-2 orbits resist the kernel at every row width rests on per-state
    runs on four distance-2 orbits. One, u8 (mask 3078077, exp-257), closed and was
    admitted as s182-bc428-u8, so it left the residue and is not one of the 95. Three
    are among the surviving 95: u1 (mask 1900509), incomplete at the 7,001 s ceiling,
    and m1964767 and m851903, fixed points under 32 uniform bins, both diagnosed
    consistency-limited. No surviving distance-2 orbit has ever closed per state, and
    the adaptive recipe that closed 26 of 29 counted H-275 draws has run on one of the
    95 (u1), at SW9's 1,152-row cap. The 22 distance-2 orbits outside the residue are
    excluded 11 by W7, 10 by s182-bc425-t1 and 1 by u8's own whole-state certificate.
    This measures the tail instead of inferring it; the threshold is the point at which
    the record would call the tail a grammar problem rather than a throughput problem.
---
# H-343: Measure the Tail

**Mechanism.** Whole-state closure under the adaptive recipe is the one engine with a
measured closure rate on residue states, and it has been pointed at two distance-2
orbits: u8, which closed and left the residue, and u1, one of the surviving 95, which
did not finish.
The float penetrations at $U$ of distance-2 states ($0.009$ to $0.012$ of
a side) are the margins W7 and A closed at, and above the engine’s loss floor; what is
unknown is how many of the 94 are like the two diagnosed states, where float evidence
puts the infeasibility across many squares jointly (an inclusion-minimal infeasible
sub-pattern of arity 15, which does not bound the size of other infeasible subsets).

**Falsifier.** Fewer than 47 of the 94 close within the ceilings.

**Expected information.** The real size of the hard tail and the per-state stall
fraction on the current residue, neither of which exists in the record, and a stall
classification for every state that resists.

**Limits.** Per-state closure removes at most eight states per certificate and is a tail
method; the 60-orbit draw prices the rest of the residue, it does not close it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
