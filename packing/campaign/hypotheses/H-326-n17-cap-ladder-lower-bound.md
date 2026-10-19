---
title: H-326 — a verified lower bound one hundredth below S* by exclusion alone
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-326
  kind: hypothesis
  claim: >-
    s(17) > V_1 with V_1 = S* - 1/100 rounded down to a rational below the H-255 root
    box: every one of the 4,683 residue orbits of the H-266 cover, the family's own
    state included, is excluded in the centred container at cap V_1 by a certificate the
    standing verifiers pass in full, and the 60 admitted certificates at U = 1169/250
    carry down to V_1 by monotone embedding, so the composition over all 43,593 orbits
    proves that no packing of side at most V_1 exists.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      First a stratified pilot: a seeded draw of 30 residue orbits (10 at distance 2, 10
      at distance 4, 10 at distance 6 or more), each run once at V_1 under the H-325
      kernel recipe and, on a kernel stall, the branch and bound to 10^6 nodes; closures
      counted only with a full-mode verifier pass. Then, if the pilot passes, the full
      residue, and a census consumer that reads per-entry caps and reports zero
      surviving orbits at V_1.
    direction: >-
      The pilot passes with at least 27 of 30 closures. Confirm only when the consumer
      reports zero surviving orbits at V_1 over the union of the U-admissions and the
      V_1-admissions, every V_1 certificate has a full-mode pass, and a W2 review of the
      composition (centred placement, monotone carry-down, per-entry caps) finds no
      defect; the bound is then registered as a new T-item at V3/C3.
    threshold: >-
      Pilot: 27 of 30; full: 0 surviving orbits; any unresolved or stalled orbit leaves
      the bound unproved and the record says which.
  instrument: >-
    The H-325 producers and verifiers at cap V_1; a per-entry-cap extension of
    devtools/census_n17_certified.py that admits an entry at cap c for every cap at or
    below c and refuses an entry whose cap is above the composition's cap; the result
    import procedure for the T-item.
  instrument_ready: false
  regime: >-
    n = 17; the H-266 cover in the U frame; centred placement of every packing of side at
    most V_1; the full residue of the 60-entry ledger at registration, frozen as a
    partition receipt; two workers; stalls recorded, never extrapolated.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: >-
    Pilot: 30 orbits at up to 11,000 s each, about 90 CPU-hours worst case, 30 typical.
    Full residue: 4,682 orbits at the measured per-orbit cost of about one CPU-hour, 100
    to 4,000 CPU-hours depending on how many close under sub-pattern certificates first;
    two to six weeks of two to ten workers. Consumer extension: one W7 slice plus
    review.
  prereqs: [H-325, H-266, H-267]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route B. A rung of the cap ladder is a published theorem (kind lower-bound)
    and the largest numerical movement available soon: R071's step was 2.75e-6. Its
    certificates are not part of the optimality proof, which needs exclusions at a cap
    at least S*; the same engines and the same states are exercised, so every stall met
    here is a stall the final proof must also resolve. Registered as blocked until the
    per-entry-cap consumer exists and H-325 reports its margin.
---
# H-326: A Cap-Ladder Rung

**Mechanism.** A certificate that excludes a state at cap $U$ excludes it at every cap
below $U$, because a packing of side $S\le V\le U$ placed concentrically in the
$U$-container is a packing in the $U$-container whose centres lie in the same cells.
So the 60 admissions stand at any $V_1<U$ and only the residue needs new certificates.
Below $S^\ast$ the family’s own state is no longer special: it is infeasible by margin
$S^\ast-V_1$ and is excluded like any other, so no capture and no local theorem enter.
The composition over all 43,593 orbits is then the n11 global half with the terminal
step removed.

**Falsifier.** The 30-orbit pilot closing fewer than 27, or any residue orbit that
neither engine closes at $V_1$ within its ceilings.

**Expected information.** A verified bound about $5\times10^{-3}$ above R071’s, and a
measured closure rate and cost on the actual tail, distance stratum by stratum, which is
exactly the cost the final proof’s exclusion stage will face at $U'$.

**Limits.** Certificates at $V_1$ do not enter the optimality proof.
The composition needs the centred placement stated once and the consumer to carry
per-entry caps; both are small changes that must be reviewed before the first rung is
registered. If H-325 reports a reach margin above $10^{-2}$, $V_1$ is moved to that
margin before the pilot, as a registration decision, not after a result.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
