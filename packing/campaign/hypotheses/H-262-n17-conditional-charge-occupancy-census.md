---
title: H-262 — free cuts and conditional charge floors leave at most 10^4 n17 occupancy orbits
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-262
  kind: hypothesis
  claim: >-
    On the H259 closed grid at cap 1169/250, the subcontainer cuts from s(6) = 3 (at
    most five centres in any 2 by 2 block of cells) and s(10) = 3 + 1/sqrt(2) (at most
    nine in any 3 by 3 block), together with exact per-cell charge floors from an
    R068-type charge rebuilt on [0,U]^2, exclude all but at most 10^4 of the 20,155,518
    H260 closed-assignment D4 orbits. A pattern is excluded when the sum over its
    occupied cells of occupancy times the cell's charge floor exceeds the available
    charge.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: >-
      The exact number of surviving closed-assignment D4 orbits after the two
      subcontainer cuts and the charge-floor test, each floor the exact minimum charge
      over every pose whose centre lies in that closed cell and every orientation row,
      with an independent recount of the survivors
    direction: >-
      Confirm if at most 10^4 orbits survive, with the endpoint's own occupancy pattern
      surviving as the positive control and an independent checker agreeing on every
      floor and the count. More than 10^5 survivors rejects this engine as the bulk
      exclusion step of the hybrid route; between the two is inconclusive and returns
      the question to W3. No geometric exclusion or bound is inferred.
    threshold: 10000
  instrument: >-
    A census tool to be built under BC-408: exact cut counting by signature bucketing
    (as in the exploratory route/census.py), an R068-type charge with strict cores on
    [0,U]^2, exact per-cell floors, and an independent floor and count auditor
  instrument_ready: false
  regime: >-
    H259 grid: cap 1169/250, centre box [1/2, U - 1/2]^2, cell side 919/1250, sixteen
    capacity-one boundary cells and nine capacity-two interior cells; existential
    closed-cell assignments as in H260; settled s(6) and s(10) on the trust base
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    One build and review slice; about six R068-sized charge sweeps (R068 replayed in
    1,265 s on two workers), hours in all; the pattern test itself is milliseconds by
    dynamic programming over 25 cells
  prereqs: [H-259, H-260, think-j1uw]
  replication: false
  registered: '2026-10-01'
  notes: >-
    From the PR 265 route review
    (docs/project/reviews/review-2026-10-01-n17-route-after-pr265.md). Exploratory exact
    counts in packing/campaign/explorations/X048-route-review/receipts/route-census.txt: the two
    cuts alone leave about 61.6 million states, about 7.7 million orbits (38.2%). A cap
    of four per boundary row is not established and must not be used. At an estimated
    1-2 CPU-hours per geometric leaf, 10^3 to 10^4 residual leaves are affordable.
---
# H-262: How Many Occupancy Cases Survive Cheap Exclusion

PR 265 counted the n17 occupancy cases but excluded none.
Geometric exclusion is likely to cost one to two CPU-hours per case, so the global route
is affordable only if a cheaper engine removes almost all of the 20.2 million orbits
first. This hypothesis measures the cheapest candidate: two settled small cases as
subcontainer cuts, and per-cell floors of a charge certificate.

## Outcome

*Added 2026-10-02 by Session 167.*
[exp-243](../series/series-000-smoke-and-calibration/experiments/exp-243-h262-n17-charge-floor-pilot.md)
rejects this hypothesis without building the exact instrument.
R068’s dictionary at $U$ excludes nothing: the smaller square slips between sites spaced
for R068’s cores, and the 7,703,312 orbits the cuts leave all survive.
For the registered class, a single D4-symmetric linear per-cell floor vector from any
charge, an antipodal-pair argument leaves at least 30,966 orbits, so the claim of at
most $10^4$ cannot hold.
Asymmetric, multi-charge, orientation-refined and nonlinear floors escape that bound and
are not tested here; the
[pilot review](../../../docs/project/reviews/review-2026-10-02-n17-charge-floor-pilot.md)
states the scope.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
