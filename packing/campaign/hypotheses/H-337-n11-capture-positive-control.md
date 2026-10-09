---
title: H-337 — the repaired n17 capture producer reproduces n11's contraction from the cells
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-337
  kind: hypothesis
  claim: >-
    With the owned-hull compression pull reduced from 2^-12 to 2^-18 of the vertex
    distance (the exact membership checks kept), the n17 capture producer run on n11's
    case-438 occupancy state from its sixteen cells, in the pilot's n11 frame at 64 live
    rows per owner with the octagon core and hull limit 48, brings the worst two-sided
    position extent below one half of its round-0 value by round 15.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      The scorer's per-round worst two-sided position extent over all eleven owners,
      relative to round 0, through round 15; the one-link residual on a wall-side bound,
      which the pull repair predicts falls from 1.26e-4 to under 1e-5 at n17's scale.
    direction: >-
      Confirm at or below 0.5 by round 15. At or above 0.9 the producer stalls where the
      n11 proof's own capture did not, the producer is defective, and no n17 reading is
      drawn. Between 0.5 and 0.9 is inconclusive and recorded as such.
    threshold: worst two-sided extent <= 0.5 of round 0 at round 15.
  instrument: >-
    devtools/pilot_n17_capture.py --system n11 --max-live 64 --max-rounds 15 with the
    pull repair of PR 402 (think-juy9) merged, from a clean worktree; devtools/
    score_n17_capture.py for the reading.
  instrument_ready: false
  regime: >-
    n = 11; the n11 proof's case-438 state and sixteen cells; the n17 producer and
    checker; the frozen thresholds 0.5 and 0.9 of the R9 review's stage 0.
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: Under 2 hours at 64 rows, about 4 hours at 128; one run.
  prereqs: [H-281]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route I, the R9 review's stage 0 that the 6 October consolidation selected
    and that has not run. H-281 (exp-268) established first-round readiness of the
    repaired producer on n11 without the contraction verdict. A pass reinstates the
    kernel route for a measured stage 1; a fail closes it with a number. Either answer
    ends a question that has consumed three sessions.
---
# H-337: The Positive Control Pilot 2 Omitted

**Mechanism.** The n11 proof’s capture contracted at about $g=0.84$ per round from its
cells. If the same producer, with its one measured first-order defect repaired, does not
contract on n11, every n17 reading of pilot 2 is a reading of a defective producer.
If it does, the n17 stall is a fact about n17.

**Falsifier.** The worst two-sided extent at or above $0.9$ of its round-0 value at
round 15.

**Expected information.** Whether the box-set reading of pilot 2 (R9’s reading B) is
about the architecture or about the code.

**Limits.** A pass on n11 says nothing about n17’s soft slope or wall crowds; it only
licenses stage 1 of R9 as a measurement of n17.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
