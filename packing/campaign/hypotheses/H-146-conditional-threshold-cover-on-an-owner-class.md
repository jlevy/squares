---
title: H-146 — threshold atoms cover an owner class's residual domain where point atoms do not
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-146
  kind: hypothesis
  claim: >-
    For at least one four-owner class of PR 137's sixteen-per-corner structure at
    q = 96/25 whose residual point cover, on a declared finite site set with the rows
    complete, has value at least seven, a conditional threshold certificate exists: a
    D4-symmetric family of point and threshold atoms charging every admissible core that
    avoids the class's guaranteed occupied union at least one, with total budget below
    seven, decided from its frozen bytes by both routes of the threshold gate restricted
    to the strict residual domain.
  lane: proof
  derived_from: [X-024]
  strategy_refs: ['proof:22', 'proof:23']
  criterion:
    shape: determination
    metric: >-
      the total budget of a frozen conditional threshold certificate on one owner class
      at (96/25, 9977/10000, 361 directions), against the rows-complete value of the
      point cover on the same site set and residual domain
    direction: >-
      Confirm with a frozen conditional threshold certificate of budget below seven on a
      class whose point cover on the same sites is at least seven with rows complete,
      accepted by both routes on the residual domain. Refute with an exact depth-one
      family of residual cores of weight at least seven that is feasible for every
      rank-one threshold atom on the residual domain, decided exactly. A class whose
      point cover is already below seven decides nothing about this claim, and a
      numerical LP value decides neither direction.
    threshold: 7
  instrument: >-
    sqpack.fractional.threshold and sqpack.fractional.threshold_interval decide
    threshold certificates on the full centre domain; PR 137's devtools.owner_footprints
    and devtools.multi_owner_domains produce the strict residual domain of a class as
    polygons per direction; joining them, a forbidden region and a budget threshold in
    one certificate format with one two-route gate, is the instrument this claim needs
    and is X-024's efficiency slice E1.
  instrument_ready: false
  regime: >-
    n = 11, side 96/25, shrink 9977/10000, the 361-direction doubled net, one four-owner
    class with its guaranteed occupied union; rank-one atoms, nonnegative weights
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: >-
    one session to join the domain restriction to the gate with controls; then one
    bounded loop of about an hour per class on three cores
  prereqs:
  - the unified certificate format and gate (X-024 slice E1)
  - a declared uncovered class from PR 137's covered/uncovered ledger, with its rows-complete point value
  replication: true
  registered: '2026-09-09'
  notes: >-
    PR 137's decisive stopping test for a class is an exact feasible fractional
    residual-core family of mass at least seven with depth at most one everywhere; that
    is the weak-duality ceiling this branch proved at 191/50 for the unconditional
    problem, where a family of mass exactly eleven stops every point cover and the
    two-of-three atoms cut it by 1/4. The one class PR 137 certified needed only five
    dots, so the conditional tree may be easy where owner patches are large; this claim
    is about the classes where it is not, and it is the measurement that decides whether
    threshold atoms make the conditional route feasible or leave the unconditional route
    as the only fractional way to 3.84.
---
# H-146 — Threshold Atoms Where Five Dots Are Not Enough

PR 137’s five-dot certificate excludes one four-owner class at `96/25` because four
guaranteed occupied patches leave a residual domain that five points pierce.
Its own analysis says the missing global step is coverage of every other class, that the
feasibility of exhausting them is unknown, and that the test which would close a class
against every point cover is a depth-one residual family of mass at least seven.
[X-024](../explorations/X-024-two-lines-at-eleven.md) reads that test as the same
integrality gap the unconditional line crossed at `191/50`, and this claim is the
discriminator: on a class whose point cover is stuck at seven or above, do threshold
atoms bring the budget below seven?

The instrument is a join, not a new theorem.
The threshold theorem’s counting argument is unchanged when the admissible cores are
restricted to those avoiding a fixed closed set, since the residual cores of an actual
packing avoid the occupied union by PR 137’s transfer argument, and the sweep decides
Condition 5' on whatever centre domain it is given.
What has to be built is the domain: PR 137’s polygons per direction, handed to this
branch’s sweep and interval route, with controls that refuse a domain that is not the
strict residual one.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
