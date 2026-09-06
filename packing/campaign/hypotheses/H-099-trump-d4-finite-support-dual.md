---
title: H-099 — Trump's D4 placement support admits dual mass above eleven
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-099
  kind: hypothesis
  claim: >-
    At the exact Trump side U, the deduplicated D4 images of the eleven exact Trump
    squares admit nonnegative rational placement weights with total mass D > 11 and
    overlap depth at most one Lebesgue-almost everywhere in the container.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:11', 'proof:17', 'proof:22']
  criterion:
    shape: determination
    metric: verified dual mass above eleven or an exact ceiling for the specified support
    direction: >-
      Accept with D > 11 only after exact containment, complete a.e.-depth verification,
      and independent BC-243 soundness controls pass. Reject this support claim with
      an exact finite necessary-row LP upper certificate at most 11. A sampled
      objective above 11, an invalid candidate, or an incomplete run is inconclusive.
    threshold: 11
  instrument: >-
    Proposed exact geometric support deduplication, necessary-row LP ceiling certificate,
    and, only for a surviving candidate, BC-243's complete a.e.-depth arrangement
    verifier with independent replay. The exact ceiling route passed its source and
    independent readiness controls; this does not authorize acceptance
    of a D > 11 candidate without the complete depth verifier.
  instrument_ready: true
  regime: >-
    n = 11; exact algebraic Trump side; only the geometric D4 closure of the retained
    Trump witness, with no added placements or assumed strong duality
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: price the finite-row ceiling screen before funding a full BC-243 verifier
  prereqs: [reviewed BC-242 semantics, frozen exact support and row-generation rule]
  replication: true
  registered: '2026-09-06'
  notes: >-
    Freeze initial test rows, their deterministic extension rule, and the run bound
    before execution. Exact LP or cutting-plane search is a candidate method, not the
    accept rule. Extending the geometric support requires a separately registered claim.
    The uniform average of eight D4 copies of the complete Trump packing has D = 11;
    reproducing this control is not evidence for D > 11.
---
# H-099 — A Finite-Support Ceiling Before the Arrangement Build

Session 089 accepts readiness for the finite-row ceiling route only, after the
[independent review](../series/series-000-smoke-and-calibration/results/agenda-026/bc-254-target-readiness-independent-review.md)
and its parser correction.
A target still requires prospective freeze and separate exact replay.
Complete almost-everywhere depth verification is not implemented here.

[Exp-113](../series/series-000-smoke-and-calibration/experiments/exp-113-h-099-trump-support-screen.md)
subsequently returned a separately replayed finite-row ceiling of $56/5$ on this support.
Together with the feasible mass-eleven average, it gives the bracket $[11,56/5]$ for
the full fixed-support supremum. H-099 remains unresolved: the matching finite-row
primal weights have not passed complete almost-everywhere depth verification.

Let F be the distinct geometric squares in all eight container symmetries of the
[exact Trump witness](../../cases/trump11/packing.py), identifying local quarter-turn
reparameterizations and duplicate placements.
For each D4 orbit O, let a_O be the weight of each distinct member: D = sum |O| a_O.
Symmetrization preserves full feasibility and D, so orbit weights lose no full-support
solutions; a test row has coefficient |{S in O : x lies in int S}|, not merely 0 or 1.

Every necessary test point must be off all square boundaries, with a certified
positive-area neighborhood of constant incidence.
These rows relax full a.e. feasibility: an exact LP ceiling at most eleven rejects the
support; a larger optimum still needs every positive-area arrangement face checked.

[BC-242](../series/series-000-smoke-and-calibration/results/agenda-026/bc-242-full-size-density-proof-contract.md)
supplies the weak-duality semantics.
[Agenda 026](../agendas/agenda-026-density-stationarity-and-trump-capture.md) routes the
screen through think-01q4 and any justified BC-243 certification through think-mt6q. A
verified D > 11 rules out mass-eleven area density at U, not below-U density.
This is the finite discriminator for
[X-016’s closure route](../explorations/X-016-after-381-two-managers-one-proof-boundary.md#closure-route).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
