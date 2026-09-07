---
title: H-104 — the fixed-side point formulas satisfy the exact-angle auxiliaries
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-104
  kind: hypothesis
  claim: >-
    At q = 1939/500, the frozen P10, P12 and A-triple point formulas satisfy all
    seven BC255 auxiliary clauses for contained closed unit squares at exactly
    zero and45 degrees, including boundary placements and the four K4 reflections.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:9', 'proof:10', 'proof:15']
  criterion:
    shape: determination
    metric: conjunction of the seven fixed-side exact-angle auxiliary clauses
    direction: >-
      Accept only when all seven clauses are completely checked by the reviewed
      exhaustive algorithm and independent receipt review passes. Reject on any
      independently checked exact counterexample to one clause, even if other
      clauses remain unchecked. Otherwise leave unresolved.
    threshold: all seven clauses
  instrument: >-
    packing/devtools/run_restricted_orientation_discriminator.py at e45c8a63,
    source-preserving exact event strata with a ten-second child cap. Independent
    source/toy review passed; returned escapes are directly rechecked. Positive
    coverage relies on the reviewed exhaustive algorithm, not counts alone.
  instrument_ready: true
  regime: fixed q=1939/500, fixed point formulas, exact zero and45 degrees only
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: one ten-second producer and a separately bounded ten-second output review
  prereqs: [independent BC255 adapter readiness, prospectively committed experiment]
  replication: false
  registered: '2026-09-06'
  notes: >-
    This is a sufficient proof-mechanism discriminator, not H036's full packing
    statement. Acceptance does not cover nearby angles; rejection does not refute
    H036. A changed point formula, side or angle family requires a new claim.
---
# H-104 — Test the Fixed Point-Cover Mechanism First

Accepted by
[exp-114](../series/series-000-smoke-and-calibration/experiments/exp-114-h-104-fixed-side-auxiliaries.md):
all seven clauses passed the reviewed exact computation and an independent input/receipt
check. This is only the fixed-formula exact-angle precursor; H-036 remains unresolved.

This claim tests the smallest concrete precursor to
[H-036](H-036-robust-restricted-orientation.md), under the
[H-102](H-102-complete-restricted-angle-support-families.md) restricted-family agenda.
It does not change H-036’s side threshold or quarter-degree neighborhoods.

Set $q=1939/500$. The frozen `point_sets(q)` formulas in
[the source module](../../cases/stromquist/restricted_orientation.py), committed at
`e45c8a63`, define the ten-point set $P_{10}$, twelve-point set $P_{12}$, and
distinguished points $A_1,A_2,A_3$ in their original order (the first three entries of
$P_{12}$). Substitute $q$ into the formulas; do not homothetically scale the source
point sets. The canonical region is $R=[1,q/2]\times[0,1]$; $K_4$ consists of the
identity and reflections in the container’s horizontal and vertical midlines.
The seven clauses are:

- Every contained axis-aligned closed unit square hits $P_{10}$.
- Every such axis-aligned square hits $P_{12}$.
- Every contained 45-degree closed unit square avoiding $P_{10}$ has its center in a
  $K_4$ image of $R$.
- Every such avoider with center in $R$ contains $A_1$.
- Every such avoider with center in $R$ contains $A_2$.
- Every such avoider with center in $R$ contains $A_3$.
- Every contained 45-degree closed unit square hits $P_{12}$.

Containment and point hits include the boundary.
Source-control avoider counts are not requirements on this target; a universally
quantified clause can hold vacuously.
Incomplete receipts are not positive results.
Any retained negative witness must be independently checked against its exact square
corners, point membership, and relevant region.
One valid falsifier rejects the conjunction even if the remaining clauses are unchecked.

The
[adapter review](../series/series-000-smoke-and-calibration/results/agenda-026/bc-255-fixed-side-discriminator-independent-review.md)
explains the exhaustive source algorithm and its independence limits.
The all-true result is computationally verified for these exact angles, not a standalone
certificate of H-036 or of a continuous-angle theorem.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
