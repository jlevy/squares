---
title: H-106 — the frozen ten-set covers the full near-axis neighborhood
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-106
  kind: hypothesis
  claim: >-
    At q=1939/500, every contained closed unit square with angle in
    [-pi/720,pi/720], modulo quarter turns, contains at least one point of the
    unchanged BC255 P10 source formulas evaluated at q.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:9', 'proof:10', 'proof:15']
  criterion:
    shape: determination
    metric: complete closed near-axis ten-point coverage
    direction: >-
      Accept only complete coverage of both closed angle signs and the whole
      contained-center domain, verified by an independent exact reader. Reject
      only an independently checked contained square in the actual angle range
      avoiding all ten points. Incomplete certificate assignments are unresolved.
    threshold: every contained square throughout the declared angle neighborhood
  instrument: >-
    BC255 fixed6x3 center-grid near-axis driver and a separately reviewed
    continuous-angle rectangle reader; both clear positive denominators and
    prove polynomial signs over complete closed rational outer slabs.
  instrument_ready: true
  regime: Fixed q=1939/500 and unchanged P10 formulas; no point movement or angle narrowing.
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: One ten-second producer and one separately bounded ten-second independent file replay after instrument readiness.
  prereqs: [prospectively committed experiment]
  replication: false
  registered: '2026-09-07'
  notes: >-
    This is one sufficient auxiliary clause for H036, not its full restricted
    packing theorem. H104 covers exact source angles only. Success here does not
    cover near45 degrees, localization, forced multiplicity or twelve-set clauses.
---
# H-106 — Continuous Near-Axis Ten-Point Coverage

This is the next independently measurable clause after
[H-104’s exact-angle result](H-104-fixed-side-point-cover-auxiliaries.md).
It belongs to BC-255 under [H-102](H-102-complete-restricted-angle-support-families.md)
and does not replace [H-036](H-036-robust-restricted-orientation.md).

Set `q=1939/500`. Reflect the four seeds `(1,1)`, `(q/2,1)`, `(3/2-q/4,q/2)`, and
`(1/2+q/4,q/2)` in the container’s horizontal and vertical midlines, then deduplicate
the resulting ten points.
These are the unchanged source formulas, evaluated at `q`, not homothetically scaled
from the source side.
All square containment and point-hit inequalities include the boundary.

For the proposed certificate, write `t=tan(theta/2)` and use both closed slabs `[-T,0]`
and `[0,T]`, where `x=11/5040` and `T=x/(1-x*x/2)`. The
[BC-255 design](../series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-instrument-design.md)
proves that this is an outward enlargement of the actual angle neighborhood.
A complete certificate on the larger domain accepts this claim.
An escape only in the added outer sliver does not reject it; rejection needs a separate
certified comparison with the actual angle endpoint.

The first instrument uses a complete six-by-three grid in normalized center coordinates
and the fixed labels already justified on the original zero-angle source control.
Each rectangle is checked throughout both angle slabs.
This sufficient representation can fail even when the geometric claim holds: an
unresolved point assignment is not a ten-set avoider.
Any richer grid or assignment search needs a separately priced and prospectively frozen
continuation. No target has run at registration.

The continuous producer and source-distinct rectangle reader passed separate
mathematical review in Session 090. The reader’s 16 source-free controls include exact
corner polynomials, closed interval signs, source/packet identity, malformed bytes,
incomplete positive claims and timeout refusal.
This establishes instrument readiness, not the claim.
The first target protocol must still be committed before dispatch.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
